"""Compute researcher-audited ESS for PSTT conditions.

PSTT条件に対する研究者監査ESSを計算する。
"""

import argparse
import json
from pathlib import Path

from common import write_rows


DEFAULT_WEIGHTS = {
    "data_transmission": 1.0,
    "processing_location": 1.0,
    "storage": 1.0,
    "third_party_visibility": 2.0,
    "identifiability": 1.0,
    "secondary_use": 2.0,
    "output_claim": 1.5,
}


def score_condition(condition):
    return score_condition_with_schema(condition, {"weights": DEFAULT_WEIGHTS})


def score_condition_with_schema(condition, audit_schema):
    weights = audit_schema.get("weights", DEFAULT_WEIGHTS)
    audit = condition.get("audit", {})
    scores = {name: int(audit.get(name, 0)) for name in DEFAULT_WEIGHTS}
    weighted = {
        f"{name}_weighted": score * weights.get(name, DEFAULT_WEIGHTS[name])
        for name, score in scores.items()
    }
    ess = sum(weighted.values())
    return {
        "condition_id": condition["condition_id"],
        "processing": condition["processing"],
        "visibility": condition["visibility"],
        "output": condition["output"],
        "data_asset": audit.get("data_asset", ""),
        "data_asset_ja": audit.get("data_asset_ja", ""),
        "trust_boundaries": " ".join(audit.get("trust_boundaries", [])),
        "observers": " ".join(audit.get("observers", [])),
        "secondary_use_channels": " ".join(audit.get("secondary_use_channels", [])),
        "policy_profile": audit.get("policy_profile", ""),
        **scores,
        **weighted,
        "ess": f"{ess:.2f}",
        "audit_note_en": audit_schema.get("note_en", "ESS is a design audit score, not a participant-rated scale."),
        "audit_note_ja": audit_schema.get("note_ja", "ESSは設計監査スコアであり、参加者評価尺度ではない。"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("conditions_json", nargs="?", default="app/conditions/conditions_2x2x2.json")
    parser.add_argument("output", nargs="?", default="analysis/outputs/ess_audit.csv")
    args = parser.parse_args()

    with Path(args.conditions_json).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    rows = [score_condition_with_schema(condition, data.get("audit_schema", {})) for condition in data["conditions"]]
    write_rows(args.output, rows)
    print(f"Wrote ESS audit to {args.output}")


if __name__ == "__main__":
    main()
