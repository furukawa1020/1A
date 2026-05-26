#!/usr/bin/env python3
"""PRESENCE audit CLI.

PRESENCE監査CLI。
"""

import argparse
import base64
import copy
import hashlib
import hmac
import json
import re
import sys
from pathlib import Path


CLAIM_SCORES = {
    "C0": 0,
    "C1": 1,
    "C2": 2,
    "C3": 3,
    "C4": 4,
    "C5": 5,
    "C6": 6,
}

AUTHORITY_AUDIENCES = {"manager", "teacher", "employer", "evaluator", "admin", "organization"}
HEALTH_SIGNALS = {"heart_rate", "sleep", "fatigue", "mood", "self_report", "health_status"}
DIAGNOSTIC_TERMS = [
    "stress",
    "depression",
    "anxiety",
    "burnout",
    "fatigue",
    "高ストレス",
    "うつ",
    "不安",
    "燃え尽き",
    "疲労",
    "危険状態",
    "要対応",
]

PATTERN_NAMES = {
    "P1": "Support-to-Assessment",
    "P2": "Self-Observation-to-Self-Surveillance",
    "P3": "Cue-to-Claim Escalation",
    "P4": "Local Insight-to-Organizational Visibility",
    "P5": "Temporary State-to-Persistent Record",
    "P6": "Health Signal-to-Productivity Label",
    "P7": "Care-to-Compliance",
    "P8": "Voluntary Reflection-to-Mandatory Monitoring",
    "P9": "Context Collapse",
    "P10": "Ambiguous State-to-Actionable Flag",
    "P11": "Individual Support-to-Group Benchmarking",
    "P12": "Non-Diagnostic Tool-to-Quasi-Diagnosis",
}

MITIGATIONS = {
    "P1": ["remove manager/evaluator visibility", "separate self-support outputs from assessment systems"],
    "P2": ["cap feedback frequency", "avoid comparative scores", "make reflection user-controlled"],
    "P3": ["cap claims at C2 pattern-level cues", "show uncertainty and context limits"],
    "P4": ["keep local insights on-device", "disable organizational dashboards"],
    "P5": ["disable long-term retention", "delete raw data by default"],
    "P6": ["prohibit productivity labels from health or unwellness signals"],
    "P7": ["separate care suggestions from compliance workflows"],
    "P8": ["make use voluntary with full opt-out"],
    "P9": ["preserve user interpretation space", "avoid single-state labels"],
    "P10": ["avoid actionable flags unless evidence and consent are strong"],
    "P11": ["remove group benchmarking for self-support data"],
    "P12": ["ban medical/psychological labels unless clinically validated and ethically governed"],
}

SCAN_RISK_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
SCAN_EXTENSIONS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".dart",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".html",
    ".vue",
    ".svelte",
}
SCAN_IGNORED_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    "node_modules",
    "target",
    "analysis",
    "paper",
    "docs",
    "presence-audit",
    "presence-security",
}
CLAIM_SCAN_RULES = [
    {
        "rule_id": "CLAIM-C4-PSYCHOLOGICAL",
        "severity": "C4",
        "risk": "HIGH",
        "claim_type": "psychological",
        "terms": ["high stress", "stress detected", "anxiety", "burnout", "高ストレス", "ストレス状態", "不安傾向"],
        "mitigation": "route psychological claims through requestClaim() and cap default output at C2",
    },
    {
        "rule_id": "CLAIM-C3-BEHAVIORAL",
        "severity": "C3",
        "risk": "MEDIUM",
        "claim_type": "behavioral",
        "terms": ["focus decreased", "concentration has decreased", "集中力低下", "集中が低下", "注意低下"],
        "mitigation": "rewrite behavioral assertions as non-assertive C2 cues",
    },
    {
        "rule_id": "CLAIM-C5-PRODUCTIVITY",
        "severity": "C5",
        "risk": "CRITICAL",
        "claim_type": "productivity",
        "terms": [
            "reduced work efficiency",
            "reduced productivity",
            "low productivity",
            "productivity decreased",
            "作業効率低下",
            "作業効率が低下",
            "生産性が低い",
            "生産性低下",
        ],
        "mitigation": "prohibit productivity labels from health or self-observation signals",
    },
    {
        "rule_id": "CLAIM-C6-ADMINISTRATIVE",
        "severity": "C6",
        "risk": "CRITICAL",
        "claim_type": "administrative",
        "terms": ["needs attention", "requires manager action", "manager report", "要注意", "要対応", "管理者対応", "管理者に共有"],
        "mitigation": "remove administrative flags and authority-visible routing",
    },
]


def parse_scalar(value):
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def simple_yaml_load(text):
    """Parse the small YAML subset used by PRESENCE examples.

    PRESENCE例で使う小さなYAMLサブセットを読む。
    """
    rows = []
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        rows.append((indent, raw_line.strip()))

    def parse_block(index, indent):
        if index >= len(rows):
            return {}, index
        if rows[index][1].startswith("- "):
            return parse_list(index, indent)
        return parse_dict(index, indent)

    def parse_dict(index, indent):
        result = {}
        while index < len(rows):
            current_indent, content = rows[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ValueError(f"Unexpected indentation before: {content}")
            if content.startswith("- "):
                break
            if ":" not in content:
                raise ValueError(f"Expected key-value line: {content}")
            key, value = content.split(":", 1)
            key = key.strip()
            value = value.strip()
            index += 1
            if value:
                result[key] = parse_scalar(value)
            elif index < len(rows) and rows[index][0] > current_indent:
                result[key], index = parse_block(index, rows[index][0])
            else:
                result[key] = {}
        return result, index

    def parse_list(index, indent):
        result = []
        while index < len(rows):
            current_indent, content = rows[index]
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ValueError(f"Unexpected indentation before: {content}")
            if not content.startswith("- "):
                break
            item_text = content[2:].strip()
            index += 1
            if not item_text:
                if index < len(rows) and rows[index][0] > current_indent:
                    item, index = parse_block(index, rows[index][0])
                else:
                    item = None
                result.append(item)
                continue
            if ":" in item_text:
                key, value = item_text.split(":", 1)
                item = {key.strip(): parse_scalar(value) if value.strip() else {}}
                if index < len(rows) and rows[index][0] > current_indent:
                    child, index = parse_block(index, rows[index][0])
                    if isinstance(child, dict):
                        item.update(child)
                    else:
                        item[key.strip()] = child
                result.append(item)
            else:
                result.append(parse_scalar(item_text))
        return result, index

    parsed, final_index = parse_block(0, rows[0][0] if rows else 0)
    if final_index != len(rows):
        raise ValueError("Could not parse complete YAML document")
    return parsed


def load_spec(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except ImportError:
        return simple_yaml_load(text)
    return yaml.safe_load(text)


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def severity_score(claim):
    return CLAIM_SCORES.get(str(claim.get("severity", "C0")), 0)


def authority_visible(visibility):
    return any(visibility.get(name, False) for name in ["manager", "teacher", "employer", "evaluator"])


def authority_names(visibility):
    return [name for name in ["manager", "teacher", "employer", "evaluator", "supporter", "researcher"] if visibility.get(name, False)]


def detect_patterns(spec):
    data = spec.get("data", {})
    visibility = spec.get("visibility", {})
    claims = spec.get("claims", [])
    actions = set(spec.get("actions", []))
    controls = spec.get("controls", {})
    system = spec.get("system", {})

    max_claim = max([severity_score(claim) for claim in claims] or [0])
    claim_types = {claim.get("type") for claim in claims}
    signals = set(data.get("signals", []))
    detected = []

    if authority_visible(visibility) and (max_claim >= 3 or actions & {"manager_report", "teacher_flag", "weekly_summary"}):
        detected.append("P1")
    if visibility.get("user", False) and max_claim >= 4 and not controls.get("non_assertive_output", False):
        detected.append("P2")
    if max_claim >= 3 and (signals or claim_types & {"psychological", "productivity", "administrative"}):
        detected.append("P3")
    if data.get("processing") == "local" and authority_visible(visibility):
        detected.append("P4")
    if data.get("retention") == "long_term":
        detected.append("P5")
    if claim_types & {"productivity"}:
        detected.append("P6")
    if actions & {"manager_report", "teacher_flag", "attendance_follow_up"} and ("support" in " ".join(system.get("intended_use", [])) or max_claim >= 4):
        detected.append("P7")
    if system.get("mandatory_use", False) or controls.get("opt_out") in {"none", None}:
        detected.append("P8")
    if claim_types & {"psychological", "productivity", "administrative"}:
        detected.append("P9")
    if actions & {"manager_report", "teacher_flag", "attention_flag", "administrative_action"} or max_claim >= 6:
        detected.append("P10")
    if actions & {"weekly_team_summary", "team_benchmark"}:
        detected.append("P11")
    if claim_types & {"psychological"} and not system.get("clinical_governance", False):
        detected.append("P12")

    return list(dict.fromkeys(detected))


def compute_boundaries(spec):
    data = spec.get("data", {})
    visibility = spec.get("visibility", {})
    claims = spec.get("claims", [])
    actions = set(spec.get("actions", []))
    max_claim = max([severity_score(claim) for claim in claims] or [0])

    data_boundary = "local"
    if data.get("processing") == "cloud":
        data_boundary = "cloud"
    elif data.get("processing") in {"edge", "limited_server"}:
        data_boundary = "limited_server"

    authority = "self_only"
    names = authority_names(visibility)
    if any(name in names for name in ["manager", "teacher"]):
        authority = "manager_or_teacher_visible"
    if any(name in names for name in ["employer", "evaluator"]):
        authority = "evaluator_visible"

    interpretation = "user_interpretation"
    if max_claim >= 6 or actions & {"manager_report", "teacher_flag", "administrative_action"}:
        interpretation = "administrative_flag"
    elif max_claim >= 4:
        interpretation = "system_label"
    elif max_claim >= 2:
        interpretation = "system_suggestion"

    violations = []
    if data_boundary == "cloud":
        violations.append("data crosses from local context into cloud processing")
    if authority != "self_only":
        violations.append("self-observation claim crosses into authority-visible boundary")
    if interpretation in {"system_label", "administrative_flag"}:
        violations.append("system claim narrows or overrides user interpretation")
    if data.get("retention") == "long_term":
        violations.append("temporary state can become persistent record")
    if actions & {"csv_export", "excel_export", "raw_export", "claim_export"} and max_claim >= 4:
        violations.append("high-severity claim records can be exported outside the guard context")

    return {
        "data_boundary": data_boundary,
        "authority_boundary": authority,
        "interpretation_boundary": interpretation,
        "violations": violations,
    }


def score_presence(spec, patterns, boundaries):
    data = spec.get("data", {})
    visibility = spec.get("visibility", {})
    controls = spec.get("controls", {})
    claims = spec.get("claims", [])
    score = 0
    if data.get("processing") == "cloud":
        score += 3
    elif data.get("processing") in {"edge", "limited_server"}:
        score += 1
    if data.get("retention") == "long_term":
        score += 3
    elif data.get("retention") in {"session", "short_term"}:
        score += 1
    if authority_visible(visibility):
        score += 4
    if any(action in spec.get("actions", []) for action in ["manager_report", "teacher_flag", "weekly_summary", "team_benchmark"]):
        score += 3
    max_claim = max([severity_score(claim) for claim in claims] or [0])
    score += max_claim
    if not controls.get("non_assertive_output", False) and max_claim >= 3:
        score += 2
    if controls.get("opt_out") == "partial":
        score += 1
    elif controls.get("opt_out") in {"none", None}:
        score += 3
    score += min(len(patterns), 6)
    score += min(len(boundaries["violations"]), 4)
    return score


def risk_level(score):
    if score >= 22:
        return "CRITICAL"
    if score >= 15:
        return "HIGH"
    if score >= 8:
        return "MEDIUM"
    return "LOW"


def analyze(spec):
    validate_spec(spec)
    patterns = detect_patterns(spec)
    boundaries = compute_boundaries(spec)
    score = score_presence(spec, patterns, boundaries)
    high_risk_claims = [
        claim for claim in spec.get("claims", [])
        if severity_score(claim) >= 4 or claim.get("type") in {"productivity", "administrative"}
    ]
    mitigations = []
    for pattern in patterns:
        mitigations.extend(MITIGATIONS.get(pattern, []))
    if any(severity_score(claim) > 2 for claim in spec.get("claims", [])):
        mitigations.append("cap claims at C2 pattern-level cues")
    if authority_visible(spec.get("visibility", {})):
        mitigations.append("make output self-only")
    if spec.get("data", {}).get("retention") == "long_term":
        mitigations.append("disable long-term retention")
    if any(action in spec.get("actions", []) for action in ["csv_export", "excel_export", "raw_export", "claim_export"]):
        mitigations.append("disable raw export for claim-level records")
        mitigations.append("aggregate organizational analytics above a k-anonymity threshold")
    return {
        "system_name": spec.get("system", {}).get("name", "unknown"),
        "presence_score": score,
        "risk_level": risk_level(score),
        "detected_patterns": [{"id": pattern, "name": PATTERN_NAMES[pattern]} for pattern in patterns],
        "claim_flow": build_claim_flow(spec),
        "high_risk_claims": high_risk_claims,
        "boundaries": boundaries,
        "recommended_mitigations": list(dict.fromkeys(mitigations)),
    }


def validate_spec(spec):
    required = ["system", "data", "visibility", "claims", "actions", "controls"]
    missing = [key for key in required if key not in spec]
    if missing:
        raise ValueError(f"Missing required top-level keys: {', '.join(missing)}")
    for key in ["name", "domain", "intended_use"]:
        if key not in spec["system"]:
            raise ValueError(f"Missing system.{key}")
    for key in ["signals", "processing", "retention", "identifiability"]:
        if key not in spec["data"]:
            raise ValueError(f"Missing data.{key}")
    for index, claim in enumerate(spec.get("claims", []), start=1):
        for key in ["id", "text", "type", "severity"]:
            if key not in claim:
                raise ValueError(f"Missing claims[{index}].{key}")
        if claim["severity"] not in CLAIM_SCORES:
            raise ValueError(f"Unknown claim severity: {claim['severity']}")


def build_claim_flow(spec):
    actions = spec.get("actions", [])
    visibility = spec.get("visibility", {})
    observers = [name for name, enabled in visibility.items() if enabled]
    flows = []
    for claim in spec.get("claims", []):
        sources = claim.get("source") or spec.get("data", {}).get("signals", [])
        flows.append(
            {
                "claim_id": claim.get("id"),
                "path": {
                    "signal": sources,
                    "feature": "derived_feature",
                    "state_estimate": claim.get("type"),
                    "label": claim.get("text"),
                    "claim": claim.get("severity"),
                    "recommendation_or_action": actions,
                    "observer": observers,
                },
            }
        )
    return flows


def render_text(result):
    lines = [
        f"PRESENCE Audit: {result['system_name']}",
        f"Risk level: {result['risk_level']}",
        f"PRESENCE score: {result['presence_score']}",
        "",
        "Detected patterns:",
    ]
    if result["detected_patterns"]:
        lines.extend([f"- {item['id']} {item['name']}" for item in result["detected_patterns"]])
    else:
        lines.append("- none")
    lines.extend(["", "High-risk claims:"])
    if result["high_risk_claims"]:
        for claim in result["high_risk_claims"]:
            lines.append(f"- {claim.get('text')} -> {claim.get('severity')} {claim.get('type')} claim")
    else:
        lines.append("- none")
    lines.extend(["", "Claim-flow:"])
    if result["claim_flow"]:
        for flow in result["claim_flow"]:
            path = flow["path"]
            lines.append(
                "- "
                + " -> ".join(
                    [
                        ",".join(path["signal"]),
                        path["feature"],
                        str(path["state_estimate"]),
                        str(path["label"]),
                        str(path["claim"]),
                        ",".join(path["recommendation_or_action"]),
                        ",".join(path["observer"]),
                    ]
                )
            )
    else:
        lines.append("- none")
    lines.extend(["", "Boundary violations:"])
    if result["boundaries"]["violations"]:
        lines.extend([f"- {item}" for item in result["boundaries"]["violations"]])
    else:
        lines.append("- none")
    lines.extend(["", "Recommended mitigations:"])
    if result["recommended_mitigations"]:
        lines.extend([f"- {item}" for item in result["recommended_mitigations"]])
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def render_markdown(result):
    lines = [
        f"# PRESENCE Audit Report: {result['system_name']}",
        "",
        f"- Risk level: **{result['risk_level']}**",
        f"- PRESENCE score: **{result['presence_score']}**",
        "",
        "## Detected Patterns",
    ]
    if result["detected_patterns"]:
        lines.extend([f"- `{item['id']}` {item['name']}" for item in result["detected_patterns"]])
    else:
        lines.append("- None")
    lines.extend(["", "## High-Risk Claims"])
    if result["high_risk_claims"]:
        for claim in result["high_risk_claims"]:
            lines.append(f"- `{claim.get('severity')}` {claim.get('type')}: {claim.get('text')}")
    else:
        lines.append("- None")
    lines.extend(["", "## Claim-Flow"])
    if result["claim_flow"]:
        for flow in result["claim_flow"]:
            path = flow["path"]
            lines.append(
                f"- `{flow['claim_id']}` "
                f"{', '.join(path['signal'])} -> {path['feature']} -> {path['state_estimate']} -> "
                f"{path['label']} -> {path['claim']} -> {', '.join(path['recommendation_or_action'])} -> "
                f"{', '.join(path['observer'])}"
            )
    else:
        lines.append("- None")
    lines.extend(["", "## Boundary Analysis"])
    lines.append(f"- Data boundary: `{result['boundaries']['data_boundary']}`")
    lines.append(f"- Authority boundary: `{result['boundaries']['authority_boundary']}`")
    lines.append(f"- Interpretation boundary: `{result['boundaries']['interpretation_boundary']}`")
    lines.extend(["", "## Boundary Violations"])
    if result["boundaries"]["violations"]:
        lines.extend([f"- {item}" for item in result["boundaries"]["violations"]])
    else:
        lines.append("- None")
    lines.extend(["", "## Recommended Mitigations"])
    if result["recommended_mitigations"]:
        lines.extend([f"- {item}" for item in result["recommended_mitigations"]])
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def audit_command(args):
    spec = load_spec(args.config)
    result = analyze(spec)
    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    elif args.format == "markdown":
        output = render_markdown(result)
    else:
        output = render_text(result)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    if args.fail_on and risk_order(result["risk_level"]) >= risk_order(args.fail_on):
        return 2
    return 0


def risk_order(level):
    order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
    return order[level.upper()]


def normalize_policy(policy):
    defaults = {
        "mode": "deny_by_default",
        "max_allowed_severity": "C2",
        "allowed_audiences": ["self"],
        "allowed_retention": ["none", "session"],
        "allowed_actionability": ["self_reflection", "none"],
        "capabilities": {},
        "invariants": {},
        "claim_minimization": {
            "default_rewrite_severity": "C2",
            "default_suggested_text": "The work flow may have changed slightly. It may be worth briefly checking how you feel.",
            "default_suggested_text_ja": "作業の流れに少し変化があるかもしれません。一度、自分の感じを見てもよさそうです。",
        },
    }
    merged = copy.deepcopy(defaults)
    for key, value in policy.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key].update(value)
        else:
            merged[key] = value
    return merged


def has_health_signal(request):
    return any(signal in HEALTH_SIGNALS for signal in request.get("sourceSignals", []))


def authority_audience(audience):
    if isinstance(audience, list):
        return any(item in AUTHORITY_AUDIENCES for item in audience)
    return audience in AUTHORITY_AUDIENCES


def contains_diagnostic_term(text):
    normalized = str(text or "").lower()
    return any(term.lower() in normalized for term in DIAGNOSTIC_TERMS)


def guard_decision(policy, request):
    policy = normalize_policy(policy)
    reasons = []
    severity = request.get("proposedSeverity", "UNKNOWN")
    severity_score_value = CLAIM_SCORES.get(severity)
    max_score = CLAIM_SCORES.get(policy.get("max_allowed_severity", "C2"), 2)
    claim_type = request.get("claimType") or request.get("type") or "unknown"
    audience = request.get("audience", "unknown")
    retention = request.get("retention", "unknown")
    actionability = request.get("actionability", "unknown")
    capabilities = policy.get("capabilities", {})
    invariants = policy.get("invariants", {})
    minimization = policy.get("claim_minimization", {})

    def decision(kind, extra=None):
        result = {
            "decision": kind,
            "allowed": kind == "allow",
            "reason": reasons,
            "suggestedText": minimization.get("default_suggested_text"),
            "suggestedTextJa": minimization.get("default_suggested_text_ja"),
            "suggestedSeverity": minimization.get("default_rewrite_severity", "C2"),
        }
        if extra:
            result.update(extra)
        return result

    if severity_score_value is None:
        reasons.append("unknown claim severity")
        return decision("deny")

    if audience not in policy.get("allowed_audiences", ["self"]):
        reasons.append("audience is not allowed by policy")
    if retention not in policy.get("allowed_retention", ["none", "session"]):
        reasons.append("retention is not allowed by policy")
    if actionability not in policy.get("allowed_actionability", ["self_reflection", "none"]):
        reasons.append("actionability is not allowed by policy")
    if severity_score_value > max_score:
        reasons.append(f"claim severity exceeds policy cap {policy.get('max_allowed_severity', 'C2')}")

    if invariants.get("health_signal_must_not_become_productivity_claim", True) and has_health_signal(request) and claim_type == "productivity":
        reasons.append("health signal must not become productivity claim")
        return decision("deny")
    if invariants.get("self_observation_claim_must_not_cross_authority_boundary", True) and authority_audience(audience):
        reasons.append("self-observation claim crosses authority boundary")
        return decision("deny")
    if (
        invariants.get("temporary_state_must_not_become_persistent_administrative_record", True)
        and retention == "long_term"
        and claim_type in {"administrative", "productivity", "psychological"}
    ):
        reasons.append("temporary state must not become persistent administrative record")
        return decision("deny")
    if (
        invariants.get("psychological_claim_requires_explicit_capability", True)
        and claim_type == "psychological"
        and not capabilities.get("psychological_claims", False)
    ):
        reasons.append("psychological claim requires explicit capability")
    if claim_type == "productivity" and not capabilities.get("productivity_claims", False):
        reasons.append("productivity claims are disabled")
    if claim_type == "administrative" and not capabilities.get("administrative_claims", False):
        reasons.append("administrative claims are disabled")
    if (
        invariants.get("non_diagnostic_system_must_not_produce_quasi_diagnostic_labels", True)
        and contains_diagnostic_term(request.get("proposedText", ""))
        and not capabilities.get("diagnostic_labels", False)
    ):
        reasons.append("non-diagnostic system must not produce quasi-diagnostic labels")
    if invariants.get("user_must_retain_interpretation_authority", True) and severity_score_value > 2:
        reasons.append("user must retain interpretation authority")

    if not reasons:
        return decision("allow", {"text": request.get("proposedText"), "severity": severity})
    if audience == "self" and retention != "long_term":
        return decision("rewrite")
    return decision("deny")


def canonical_json(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign_bundle(policy, secret):
    payload = copy.deepcopy(policy)
    payload.pop("signature", None)
    digest = hmac.new(secret.encode("utf-8"), canonical_json(payload), hashlib.sha256).digest()
    payload["signature"] = {
        "algorithm": "HMAC-SHA256",
        "value": base64.b64encode(digest).decode("ascii"),
        "note": "Prototype signing for local research use; production should use asymmetric signatures."
    }
    return payload


def verify_bundle(policy, secret):
    signature = policy.get("signature", {})
    expected = sign_bundle(policy, secret).get("signature", {}).get("value")
    return bool(signature.get("value") and hmac.compare_digest(signature["value"], expected))


def guard_command(args):
    policy = load_json(args.policy)
    if args.verify_secret and not verify_bundle(policy, args.verify_secret):
        raise SystemExit("Policy signature verification failed")
    request = load_json(args.request)
    result = guard_decision(policy, request)
    if args.log_output:
        write_json(args.log_output, minimal_audit_event(result, request))
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


def compile_policy_command(args):
    policy = load_json(args.policy)
    if args.sign_secret:
        policy = sign_bundle(policy, args.sign_secret)
    write_json(args.output, policy)
    print(f"Wrote policy bundle to {args.output}")
    return 0


def verify_policy_command(args):
    policy = load_json(args.policy)
    ok = verify_bundle(policy, args.sign_secret)
    print("Policy signature OK" if ok else "Policy signature FAILED")
    return 0 if ok else 2


def should_scan_path(path):
    parts = set(path.parts)
    if parts & SCAN_IGNORED_DIRS:
        return False
    return path.suffix.lower() in SCAN_EXTENSIONS


def iter_scan_files(paths):
    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            continue
        if path.is_file():
            if should_scan_path(path):
                yield path
            continue
        for candidate in path.rglob("*"):
            if candidate.is_file() and should_scan_path(candidate):
                yield candidate


def scan_file(path):
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="ignore")
    if "presence-scan: ignore-file" in "\n".join(text.splitlines()[:10]):
        return []
    findings = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        normalized_line = line.lower()
        guard_context = "requestclaim" in normalized_line or "presenceguard" in normalized_line
        for rule in CLAIM_SCAN_RULES:
            for term in rule["terms"]:
                index = normalized_line.find(term.lower())
                if index < 0:
                    continue
                findings.append(
                    {
                        "path": str(path),
                        "line": line_number,
                        "column": index + 1,
                        "term": term,
                        "rule_id": rule["rule_id"],
                        "severity": rule["severity"],
                        "risk": rule["risk"],
                        "claim_type": rule["claim_type"],
                        "context": "guarded" if guard_context else "unguarded_literal",
                        "mitigation": rule["mitigation"],
                    }
                )
    return findings


def scan_paths(paths):
    findings = []
    for path in iter_scan_files(paths):
        findings.extend(scan_file(path))
    max_risk = "LOW"
    for finding in findings:
        if SCAN_RISK_ORDER[finding["risk"]] > SCAN_RISK_ORDER[max_risk]:
            max_risk = finding["risk"]
    return {
        "scanner": "presence-static-claim-scanner",
        "risk_level": max_risk if findings else "LOW",
        "finding_count": len(findings),
        "findings": findings,
        "policy": {
            "purpose": "detect direct claim rendering and build-time bypass risk",
            "log_minimization": "findings store source location, rule id, severity, and mitigation; they do not store user state or runtime observations",
        },
    }


def render_scan_text(result):
    lines = [
        "PRESENCE Static Claim Scan",
        f"Risk level: {result['risk_level']}",
        f"Findings: {result['finding_count']}",
        "",
    ]
    if not result["findings"]:
        lines.append("No dangerous claim literals found.")
        return "\n".join(lines) + "\n"
    for finding in result["findings"]:
        lines.append(
            f"- {finding['path']}:{finding['line']}:{finding['column']} "
            f"{finding['rule_id']} {finding['severity']} {finding['risk']} "
            f"term={finding['term']!r} context={finding['context']}"
        )
        lines.append(f"  mitigation: {finding['mitigation']}")
    return "\n".join(lines) + "\n"


def render_scan_markdown(result):
    lines = [
        "# PRESENCE Static Claim Scan",
        "",
        f"- Risk level: **{result['risk_level']}**",
        f"- Findings: **{result['finding_count']}**",
        "",
        "## Findings",
    ]
    if not result["findings"]:
        lines.append("- None")
        return "\n".join(lines) + "\n"
    for finding in result["findings"]:
        lines.append(
            f"- `{finding['path']}:{finding['line']}:{finding['column']}` "
            f"`{finding['rule_id']}` `{finding['severity']}` `{finding['risk']}` "
            f"term `{finding['term']}`; context `{finding['context']}`"
        )
        lines.append(f"  - Mitigation: {finding['mitigation']}")
    return "\n".join(lines) + "\n"


def scan_command(args):
    result = scan_paths(args.paths)
    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    elif args.format == "markdown":
        output = render_scan_markdown(result)
    else:
        output = render_scan_text(result)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    if args.fail_on and SCAN_RISK_ORDER[result["risk_level"]] >= SCAN_RISK_ORDER[args.fail_on]:
        return 2
    return 0


def minimal_audit_event(result, request):
    return {
        "event_type": "presence_guard_decision",
        "decision": result.get("decision"),
        "allowed": result.get("allowed"),
        "reason_count": len(result.get("reason", [])),
        "reason_rules": result.get("reason", []),
        "proposed_severity": request.get("proposedSeverity", "UNKNOWN"),
        "claim_type": request.get("claimType") or request.get("type") or "unknown",
        "audience": request.get("audience", "unknown"),
        "retention": request.get("retention", "unknown"),
        "stores_claim_text": False,
        "stores_source_signals": False,
        "stores_user_identifier": False,
    }


def mutation_test_command(args):
    spec = load_spec(args.config)
    base = analyze(spec)
    mutations = [
        ("manager_visible", lambda s: s.setdefault("visibility", {}).__setitem__("manager", True)),
        ("long_term_retention", lambda s: s.setdefault("data", {}).__setitem__("retention", "long_term")),
        ("severity_to_C5", lambda s: s.setdefault("claims", [{}])[0].__setitem__("severity", "C5")),
        ("audience_to_employer", lambda s: s.setdefault("visibility", {}).__setitem__("employer", True)),
        ("productivity_label", lambda s: s.setdefault("claims", [{}])[0].update({"type": "productivity", "text": "Reduced work efficiency", "severity": "C5"})),
    ]
    rows = []
    for name, apply_mutation in mutations:
        mutated = copy.deepcopy(spec)
        apply_mutation(mutated)
        result = analyze(mutated)
        rows.append(
            {
                "mutation": name,
                "base_score": base["presence_score"],
                "mutated_score": result["presence_score"],
                "score_increased": result["presence_score"] > base["presence_score"],
                "risk_level": result["risk_level"],
            }
        )
    output = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0 if all(row["score_increased"] for row in rows) else 2


def main(argv=None):
    parser = argparse.ArgumentParser(prog="presence-audit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Audit a PRESENCE YAML/JSON spec.")
    audit.add_argument("config")
    audit.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    audit.add_argument("--output")
    audit.add_argument("--fail-on", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    audit.set_defaults(func=audit_command)

    guard = subparsers.add_parser("guard", help="Enforce a single claim request against a PRESENCE policy.")
    guard.add_argument("policy")
    guard.add_argument("request")
    guard.add_argument("--verify-secret")
    guard.add_argument("--output")
    guard.add_argument("--log-output", help="Write a minimized audit event without claim text or source signals.")
    guard.set_defaults(func=guard_command)

    compile_policy = subparsers.add_parser("compile-policy", help="Compile/sign a PRESENCE Guard policy bundle.")
    compile_policy.add_argument("policy")
    compile_policy.add_argument("--output", required=True)
    compile_policy.add_argument("--sign-secret")
    compile_policy.set_defaults(func=compile_policy_command)

    verify_policy = subparsers.add_parser("verify-policy", help="Verify a signed PRESENCE Guard policy bundle.")
    verify_policy.add_argument("policy")
    verify_policy.add_argument("--sign-secret", required=True)
    verify_policy.set_defaults(func=verify_policy_command)

    mutation_test = subparsers.add_parser("mutation-test", help="Run simple policy/design mutation tests.")
    mutation_test.add_argument("config")
    mutation_test.add_argument("--output")
    mutation_test.set_defaults(func=mutation_test_command)

    scan = subparsers.add_parser("scan", help="Scan source files for direct dangerous claim literals.")
    scan.add_argument("paths", nargs="+")
    scan.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    scan.add_argument("--output")
    scan.add_argument("--fail-on", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    scan.set_defaults(func=scan_command)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
