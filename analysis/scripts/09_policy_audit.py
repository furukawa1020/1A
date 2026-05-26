"""Audit PSTT conditions for policy-relevant exposure findings.

PSTT条件をポリシー上重要な曝露所見について監査する。
"""

import argparse
import json
from pathlib import Path

from common import write_rows


def findings_for(condition):
    audit = condition.get("audit", {})
    findings = []

    if audit.get("third_party_visibility", 0) >= 2 and audit.get("output_claim", 0) >= 2:
        findings.append(
            {
                "severity": "high",
                "code": "manager_visible_assertive_label",
                "finding_en": "Manager-visible output and assertive labeling co-occur.",
                "finding_ja": "管理者可視性と断定ラベルが同時に存在する。",
            }
        )

    if audit.get("secondary_use", 0) >= 2:
        findings.append(
            {
                "severity": "high",
                "code": "secondary_use_enabled",
                "finding_en": "The scenario includes a report or channel that enables secondary use.",
                "finding_ja": "レポート等により二次利用可能性がある。",
            }
        )

    if audit.get("processing_location", 0) >= 2 and audit.get("data_transmission", 0) >= 2:
        findings.append(
            {
                "severity": "medium",
                "code": "cloud_processing_boundary",
                "finding_en": "The data crosses the device-to-cloud trust boundary.",
                "finding_ja": "データが端末からクラウドへの信頼境界を越える。",
            }
        )

    if audit.get("output_claim", 0) >= 2:
        findings.append(
            {
                "severity": "medium",
                "code": "assertive_internal_state_claim",
                "finding_en": "The output makes an assertive claim about the user's internal state.",
                "finding_ja": "出力がユーザーの内部状態について断定的に主張する。",
            }
        )

    if not findings:
        findings.append(
            {
                "severity": "info",
                "code": "no_policy_finding",
                "finding_en": "No configured policy finding was triggered.",
                "finding_ja": "設定済みポリシー所見は発火しなかった。",
            }
        )

    return findings


def rows_for_conditions(conditions):
    rows = []
    for condition in conditions:
        audit = condition.get("audit", {})
        for finding in findings_for(condition):
            rows.append(
                {
                    "condition_id": condition["condition_id"],
                    "processing": condition["processing"],
                    "visibility": condition["visibility"],
                    "output": condition["output"],
                    "trust_boundaries": " ".join(audit.get("trust_boundaries", [])),
                    "observers": " ".join(audit.get("observers", [])),
                    "secondary_use_channels": " ".join(audit.get("secondary_use_channels", [])),
                    **finding,
                }
            )
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("conditions_json", nargs="?", default="app/conditions/conditions_2x2x2.json")
    parser.add_argument("output", nargs="?", default="analysis/outputs/policy_audit.csv")
    args = parser.parse_args()

    with Path(args.conditions_json).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    rows = rows_for_conditions(data["conditions"])
    write_rows(args.output, rows)
    print(f"Wrote policy audit to {args.output}")


if __name__ == "__main__":
    main()

