#!/usr/bin/env python3
"""Run the public-information PRESENCE benchmark profiles."""

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "presence-bench"
sys.path.insert(0, str(ROOT / "presence-audit" / "cli"))

import presence_audit as pa  # noqa: E402


RISK_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}


def load_expected(profile_path):
    expected_path = BENCH / "expected" / f"{profile_path.stem}.expected.json"
    return json.loads(expected_path.read_text(encoding="utf-8"))


def evaluate_profile(profile_path):
    spec = pa.load_spec(profile_path)
    result = pa.analyze(spec)
    expected = load_expected(profile_path)
    actual_patterns = {item["id"] for item in result["detected_patterns"]}
    claim_types = {claim.get("type") for claim in result["high_risk_claims"]}

    expected_patterns = set(expected.get("expected_patterns", []))
    expected_claim_types = set(expected.get("expected_high_risk_claim_types", []))
    pattern_ok = expected_patterns.issubset(actual_patterns)
    claim_ok = expected_claim_types.issubset(claim_types)

    risk_ok = True
    if "min_risk_level" in expected:
        risk_ok = RISK_ORDER[result["risk_level"]] >= RISK_ORDER[expected["min_risk_level"]]
    if "max_risk_level" in expected:
        risk_ok = risk_ok and RISK_ORDER[result["risk_level"]] <= RISK_ORDER[expected["max_risk_level"]]

    return {
        "profile": profile_path.stem,
        "risk_level": result["risk_level"],
        "presence_score": result["presence_score"],
        "detected_patterns": sorted(actual_patterns),
        "missing_patterns": sorted(expected_patterns - actual_patterns),
        "high_risk_claim_types": sorted(claim_types),
        "missing_claim_types": sorted(expected_claim_types - claim_types),
        "risk_ok": risk_ok,
        "pattern_ok": pattern_ok,
        "claim_ok": claim_ok,
        "passed": risk_ok and pattern_ok and claim_ok,
        "mitigations": result["recommended_mitigations"],
    }


def render_markdown(rows):
    lines = [
        "# PRESENCE Benchmark Report",
        "",
        "This benchmark uses reference profiles abstracted from public feature documentation. It does not assert that any named service is unsafe or non-compliant.",
        "",
        "| Profile | Risk | Score | Passed | Patterns | Missing |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['profile']}` | `{row['risk_level']}` | {row['presence_score']} | "
            f"{'yes' if row['passed'] else 'no'} | {', '.join(row['detected_patterns']) or '-'} | "
            f"{', '.join(row['missing_patterns'] + row['missing_claim_types']) or '-'} |"
        )

    lines.extend(["", "## Recommended Mitigations"])
    for row in rows:
        lines.append(f"### {row['profile']}")
        for mitigation in row["mitigations"][:8]:
            lines.append(f"- {mitigation}")
        if not row["mitigations"]:
            lines.append("- none")
        lines.append("")

    lines.extend(
        [
            "## 日本語",
            "",
            "このbenchmarkは、公開機能資料から抽象化したreference profileを用いる。実在サービスが危険または非準拠であるとは主張しない。",
            "",
            "評価対象は、claim severity、authority boundary、interpretation boundary、retention、secondary use、productivity/administrative claimへの転化である。",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(BENCH / "reports" / "benchmark_report.md"))
    parser.add_argument("--json-output", default=str(BENCH / "reports" / "benchmark_report.json"))
    args = parser.parse_args(argv)

    rows = []
    for profile_path in sorted((BENCH / "profiles").glob("*.yaml")):
        rows.append(evaluate_profile(profile_path))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(rows), encoding="utf-8")

    json_output_path = Path(args.json_output)
    json_output_path.parent.mkdir(parents=True, exist_ok=True)
    json_output_path.write_text(json.dumps({"passed": all(row["passed"] for row in rows), "rows": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"passed": all(row["passed"] for row in rows), "profiles": len(rows), "output": str(output_path)}, ensure_ascii=False))
    return 0 if all(row["passed"] for row in rows) else 2


if __name__ == "__main__":
    raise SystemExit(main())
