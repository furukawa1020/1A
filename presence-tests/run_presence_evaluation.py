#!/usr/bin/env python3
"""PRESENCE Guard non-human evaluation runner.

This script is intentionally dependency-light. It exercises the reference
monitor, static audit model, signed policy prototype, bypass checks, fuzz
negative tests, and lightweight overhead measurement.
"""

import argparse
import copy
import json
import random
import re
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "presence-audit" / "cli"))

import presence_audit as pa  # noqa: E402


def deep_merge(base, patch):
    result = copy.deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def pattern_ids(result):
    return {item["id"] for item in result["detected_patterns"]}


def evaluate_misuse_cases():
    fixture = json.loads(
        (ROOT / "presence-tests" / "fixtures" / "misuse_cases" / "pattern_cases.json").read_text(encoding="utf-8")
    )
    base = fixture["base_safe_spec"]
    rows = []
    passed = True
    for case in fixture["cases"]:
        danger = deep_merge(base, case["danger_patch"])
        safe = deep_merge(base, case.get("safe_patch", {}))
        danger_patterns = pattern_ids(pa.analyze(danger))
        safe_patterns = pattern_ids(pa.analyze(safe))
        danger_ok = case["id"] in danger_patterns
        safe_ok = case["id"] not in safe_patterns
        passed = passed and danger_ok and safe_ok
        rows.append(
            {
                "id": case["id"],
                "name": case["name"],
                "danger_detected": danger_ok,
                "safe_not_detected": safe_ok,
                "danger_patterns": sorted(danger_patterns),
                "safe_patterns": sorted(safe_patterns),
            }
        )
    return {"passed": passed, "cases": rows}


def evaluate_policy_mutations():
    spec = pa.load_spec(ROOT / "presence-audit" / "examples" / "noticer_local.yaml")
    base = pa.analyze(spec)
    mutations = [
        ("manager_visible", lambda s: s.setdefault("visibility", {}).__setitem__("manager", True)),
        ("long_term_retention", lambda s: s.setdefault("data", {}).__setitem__("retention", "long_term")),
        ("severity_to_C5", lambda s: s.setdefault("claims", [{}])[0].__setitem__("severity", "C5")),
        ("audience_to_employer", lambda s: s.setdefault("visibility", {}).__setitem__("employer", True)),
        (
            "productivity_label",
            lambda s: s.setdefault("claims", [{}])[0].update(
                {"type": "productivity", "text": "Reduced work efficiency", "severity": "C5"}
            ),
        ),
        ("cloud_processing", lambda s: s.setdefault("data", {}).__setitem__("processing", "cloud")),
    ]
    rows = []
    passed = True
    for name, mutate in mutations:
        mutated = copy.deepcopy(spec)
        mutate(mutated)
        result = pa.analyze(mutated)
        score_increased = result["presence_score"] > base["presence_score"]
        passed = passed and score_increased
        rows.append(
            {
                "mutation": name,
                "base_score": base["presence_score"],
                "mutated_score": result["presence_score"],
                "score_increased": score_increased,
                "risk_level": result["risk_level"],
            }
        )
    return {"passed": passed, "rows": rows}


def evaluate_guard_fixtures():
    policy = pa.load_json(ROOT / "presence-policy" / "presence.guard.policy.json")
    expectations = {
        "request_high_stress_self.json": "rewrite",
        "request_productivity_manager.json": "deny",
        "request_soft_cue_self.json": "allow",
    }
    rows = []
    passed = True
    for filename, expected in expectations.items():
        request = pa.load_json(ROOT / "presence-tests" / "fixtures" / filename)
        decision = pa.guard_decision(policy, request)
        ok = decision["decision"] == expected
        passed = passed and ok
        rows.append(
            {
                "fixture": filename,
                "expected": expected,
                "actual": decision["decision"],
                "passed": ok,
                "reasons": decision["reason"],
            }
        )
    return {"passed": passed, "rows": rows}


def evaluate_signature_and_invalid_inputs():
    policy = pa.load_json(ROOT / "presence-policy" / "presence.guard.policy.json")
    signed = pa.sign_bundle(policy, "evaluation-secret")
    signature_ok = pa.verify_bundle(signed, "evaluation-secret")
    tampered = copy.deepcopy(signed)
    tampered["max_allowed_severity"] = "C6"
    tamper_rejected = not pa.verify_bundle(tampered, "evaluation-secret")
    invalid_request = {
        "sourceSignals": ["keyboard_rhythm"],
        "proposedText": "Unknown claim",
        "proposedSeverity": "C99",
        "claimType": "psychological",
        "audience": "self",
        "retention": "session",
        "actionability": "self_reflection",
    }
    invalid_request_denied = pa.guard_decision(policy, invalid_request)["decision"] == "deny"
    invalid_spec_rejected = False
    try:
        pa.analyze({"system": {"name": "broken"}})
    except ValueError:
        invalid_spec_rejected = True
    return {
        "passed": signature_ok and tamper_rejected and invalid_request_denied and invalid_spec_rejected,
        "signature_ok": signature_ok,
        "tamper_rejected": tamper_rejected,
        "invalid_request_denied": invalid_request_denied,
        "invalid_spec_rejected": invalid_spec_rejected,
    }


def evaluate_bypass_checks():
    app_main = (ROOT / "app" / "src" / "main.js").read_text(encoding="utf-8")
    renderer = (ROOT / "app" / "src" / "condition_renderer" / "renderer.js").read_text(encoding="utf-8")
    unsafe_fixture = (ROOT / "presence-tests" / "fixtures" / "bypass_tests" / "direct_claim_render.js").read_text(
        encoding="utf-8"
    )
    direct_output_render = bool(re.search(r"renderOutput\([^)]*condition\.output_text", renderer + app_main))
    guard_called = "requestClaim" in app_main and "guard.requestClaim" in app_main
    unsafe_fixture_detected = bool(re.search(r"render\([\"'].*(stress|efficiency|concentration|productivity)", unsafe_fixture, re.I))
    return {
        "passed": (not direct_output_render) and guard_called and unsafe_fixture_detected,
        "app_direct_condition_output_render": direct_output_render,
        "app_guard_called_before_claim_output": guard_called,
        "unsafe_fixture_detected": unsafe_fixture_detected,
    }


def evaluate_fuzz():
    policy = pa.load_json(ROOT / "presence-policy" / "presence.guard.policy.json")
    random.seed(20260526)
    severities = list(pa.CLAIM_SCORES)
    audiences = ["self", "manager", "teacher", "employer"]
    retentions = ["none", "session", "long_term"]
    claim_types = ["pattern", "behavioral", "psychological", "productivity", "administrative"]
    failures = []
    total = 500
    for index in range(total):
        severity = random.choice(severities)
        audience = random.choice(audiences)
        retention = random.choice(retentions)
        claim_type = random.choice(claim_types)
        uses_health = random.choice([True, False])
        request = {
            "sourceSignals": ["heart_rate"] if uses_health else ["keyboard_rhythm"],
            "proposedText": "High stress detected" if claim_type == "psychological" else "The work flow may have changed",
            "proposedSeverity": severity,
            "claimType": claim_type,
            "audience": audience,
            "retention": retention,
            "actionability": "self_reflection" if audience == "self" else "manager_report",
        }
        decision = pa.guard_decision(policy, request)
        should_never_allow = (
            pa.CLAIM_SCORES[severity] > 2
            or audience != "self"
            or retention == "long_term"
            or (uses_health and claim_type == "productivity")
            or claim_type in {"psychological", "productivity", "administrative"}
        )
        if should_never_allow and decision["decision"] == "allow":
            failures.append({"index": index, "request": request, "decision": decision})
    return {"passed": not failures, "total": total, "failures": failures[:10]}


def evaluate_no_network_core():
    forbidden = ["fetch(", "XMLHttpRequest", "TcpStream", "UdpSocket", "std::net", "reqwest", "curl", "socket(", "connect("]
    paths = [
        ROOT / "presence-core" / "src" / "lib.rs",
        ROOT / "presence-ffi-c" / "src" / "presence_guard.c",
        ROOT / "presence-ffi-c" / "include" / "presence_guard.h",
    ]
    hits = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in text:
                hits.append({"path": str(path.relative_to(ROOT)), "token": token})
    return {"passed": not hits, "hits": hits}


def evaluate_dependency_surface():
    cargo = (ROOT / "presence-core" / "Cargo.toml").read_text(encoding="utf-8")
    ts_pkg = json.loads((ROOT / "presence-sdk-ts" / "package.json").read_text(encoding="utf-8"))
    runtime_deps = ts_pkg.get("dependencies", {})
    rust_has_dependencies = "[dependencies]" in cargo
    return {
        "passed": not rust_has_dependencies and not runtime_deps,
        "rust_runtime_dependencies": [],
        "typescript_runtime_dependencies": runtime_deps,
        "note": "TypeScript package uses only a devDependency on typescript for declaration/build output.",
    }


def evaluate_overhead(iterations):
    policy = pa.load_json(ROOT / "presence-policy" / "presence.guard.policy.json")
    request = pa.load_json(ROOT / "presence-tests" / "fixtures" / "request_soft_cue_self.json")
    start = time.perf_counter()
    for _ in range(iterations):
        pa.guard_decision(policy, request)
    elapsed = time.perf_counter() - start
    policy_bytes = len(json.dumps(policy, ensure_ascii=False).encode("utf-8"))
    request_bytes = len(json.dumps(request, ensure_ascii=False).encode("utf-8"))
    return {
        "passed": True,
        "iterations": iterations,
        "total_seconds": elapsed,
        "mean_decision_latency_ms": (elapsed / iterations) * 1000,
        "policy_size_bytes": policy_bytes,
        "request_size_bytes": request_bytes,
        "measurement": "Python CLI engine overhead on this local machine; Rust core should be measured separately when release-built.",
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(ROOT / "analysis" / "outputs" / "presence_evaluation.json"))
    parser.add_argument("--iterations", type=int, default=10000)
    args = parser.parse_args(argv)

    results = {
        "misuse_case_detection": evaluate_misuse_cases(),
        "policy_mutation": evaluate_policy_mutations(),
        "guard_fixture_decisions": evaluate_guard_fixtures(),
        "signature_and_invalid_input": evaluate_signature_and_invalid_inputs(),
        "bypass_checks": evaluate_bypass_checks(),
        "fuzz_negative_tests": evaluate_fuzz(),
        "no_network_core": evaluate_no_network_core(),
        "dependency_surface": evaluate_dependency_surface(),
        "overhead": evaluate_overhead(args.iterations),
    }
    results["passed"] = all(item.get("passed", False) for item in results.values() if isinstance(item, dict))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": results["passed"], "output": str(output_path)}, ensure_ascii=False))
    return 0 if results["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
