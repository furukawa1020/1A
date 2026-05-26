"""Validate the 2x2x2 PSTT condition file.

PSTTの2x2x2条件定義ファイルを検証する。
"""

import argparse
import json
from pathlib import Path


REQUIRED_KEYS = {
    "condition_id",
    "processing",
    "visibility",
    "output",
    "processing_text",
    "visibility_text",
    "output_text",
    "audit",
}

AUDIT_KEYS = {
    "data_asset",
    "data_asset_ja",
    "data_transmission",
    "processing_location",
    "storage",
    "third_party_visibility",
    "identifiability",
    "secondary_use",
    "output_claim",
    "trust_boundaries",
    "observers",
    "secondary_use_channels",
    "policy_profile",
}

EXPECTED_COMBINATIONS = {
    ("cloud", "manager_visible", "assertive"),
    ("cloud", "manager_visible", "non_assertive"),
    ("cloud", "self_only", "assertive"),
    ("cloud", "self_only", "non_assertive"),
    ("local", "manager_visible", "assertive"),
    ("local", "manager_visible", "non_assertive"),
    ("local", "self_only", "assertive"),
    ("local", "self_only", "non_assertive"),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("conditions_json", nargs="?", default="app/conditions/conditions_2x2x2.json")
    args = parser.parse_args()

    path = Path(args.conditions_json)
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    conditions = data.get("conditions", [])
    if len(conditions) != 8:
        raise SystemExit(f"Expected 8 conditions, found {len(conditions)}")

    if "audit_schema" not in data or "weights" not in data["audit_schema"]:
        raise SystemExit("Missing audit_schema.weights")

    ids = [condition.get("condition_id") for condition in conditions]
    expected_ids = [f"C{index}" for index in range(1, 9)]
    if sorted(ids, key=lambda value: int(value[1:])) != expected_ids:
        raise SystemExit(f"Condition IDs are not C1-C8: {ids}")

    combos = set()
    line_counts = set()
    for condition in conditions:
        missing = REQUIRED_KEYS - set(condition)
        if missing:
            raise SystemExit(f"{condition.get('condition_id')} missing keys: {sorted(missing)}")
        audit_missing = AUDIT_KEYS - set(condition["audit"])
        if audit_missing:
            raise SystemExit(f"{condition.get('condition_id')} missing audit keys: {sorted(audit_missing)}")
        for key in [
            "data_transmission",
            "processing_location",
            "storage",
            "third_party_visibility",
            "identifiability",
            "secondary_use",
            "output_claim",
        ]:
            value = condition["audit"][key]
            if value not in [0, 1, 2]:
                raise SystemExit(f"{condition.get('condition_id')} audit {key} must be 0, 1, or 2")
        combos.add((condition["processing"], condition["visibility"], condition["output"]))
        line_counts.add(len(condition["output_text"].splitlines()))

    if combos != EXPECTED_COMBINATIONS:
        raise SystemExit(f"Unexpected factor combinations: {sorted(combos)}")

    if len(line_counts) != 1:
        raise SystemExit(f"Output line counts differ across conditions: {sorted(line_counts)}")

    print("OK: condition file has 8 controlled 2x2x2 conditions with audit manifests.")


if __name__ == "__main__":
    main()
