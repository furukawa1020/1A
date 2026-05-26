"""Compute researcher-audited ESS for PSTT conditions.

PSTT条件に対する研究者監査ESSを計算する。
"""

import argparse
import json
from pathlib import Path

from common import write_rows


WEIGHTS = {
    "data_transmission": 1.0,
    "processing_location": 1.0,
    "storage": 1.0,
    "third_party_visibility": 2.0,
    "identifiability": 1.0,
    "secondary_use": 2.0,
    "output_claim": 1.5,
}


def score_condition(condition):
    processing = condition["processing"]
    visibility = condition["visibility"]
    output = condition["output"]

    scores = {
        "data_transmission": 2 if processing == "cloud" else 0,
        "processing_location": 2 if processing == "cloud" else 0,
        "storage": 0,
        "third_party_visibility": 2 if visibility == "manager_visible" else 0,
        "identifiability": 2 if visibility == "manager_visible" else (1 if processing == "cloud" else 0),
        "secondary_use": 2 if visibility == "manager_visible" else 0,
        "output_claim": 2 if output == "assertive" else 0,
    }
    weighted = {
        f"{name}_weighted": score * WEIGHTS[name]
        for name, score in scores.items()
    }
    ess = sum(weighted.values())
    return {
        "condition_id": condition["condition_id"],
        "processing": processing,
        "visibility": visibility,
        "output": output,
        **scores,
        **weighted,
        "ess": f"{ess:.2f}",
        "audit_note_en": "ESS is a design audit score, not a participant-rated scale.",
        "audit_note_ja": "ESSは設計監査スコアであり、参加者評価尺度ではない。",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("conditions_json", nargs="?", default="app/conditions/conditions_2x2x2.json")
    parser.add_argument("output", nargs="?", default="analysis/outputs/ess_audit.csv")
    args = parser.parse_args()

    with Path(args.conditions_json).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    rows = [score_condition(condition) for condition in data["conditions"]]
    write_rows(args.output, rows)
    print(f"Wrote ESS audit to {args.output}")


if __name__ == "__main__":
    main()

