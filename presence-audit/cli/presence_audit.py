#!/usr/bin/env python3
"""PRESENCE audit CLI.

PRESENCE監査CLI。
"""

import argparse
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
    return {
        "system_name": spec.get("system", {}).get("name", "unknown"),
        "presence_score": score,
        "risk_level": risk_level(score),
        "detected_patterns": [{"id": pattern, "name": PATTERN_NAMES[pattern]} for pattern in patterns],
        "high_risk_claims": high_risk_claims,
        "boundaries": boundaries,
        "recommended_mitigations": list(dict.fromkeys(mitigations)),
    }


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


def main(argv=None):
    parser = argparse.ArgumentParser(prog="presence-audit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser("audit", help="Audit a PRESENCE YAML/JSON spec.")
    audit.add_argument("config")
    audit.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    audit.add_argument("--output")
    audit.add_argument("--fail-on", choices=["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    audit.set_defaults(func=audit_command)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
