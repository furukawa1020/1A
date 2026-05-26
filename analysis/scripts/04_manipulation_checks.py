"""Analyze PSTT manipulation checks and exclusion flags.

PSTTの操作チェックと除外フラグを分析する。
"""

import argparse
import math
from common import group_by, mean, read_rows, to_float, write_rows


def expected_direction(row, name):
    if name == "manip_cloud":
        return "high" if row.get("processing") == "cloud" else "low"
    if name == "manip_visibility":
        return "high" if row.get("visibility") == "manager_visible" else "low"
    if name == "manip_assertive":
        return "high" if row.get("output") == "assertive" else "low"
    if name == "manip_self_only":
        return "high" if row.get("visibility") == "self_only" else "low"
    raise ValueError(name)


def check_failed(value, direction):
    if math.isnan(value):
        return True
    if direction == "high":
        return value < 5
    return value > 3


def annotate_rows(rows):
    annotated = []
    for row in rows:
        updated = dict(row)
        failed = 0
        for name in ["manip_cloud", "manip_visibility", "manip_assertive", "manip_self_only"]:
            value = to_float(row.get(name))
            direction = expected_direction(row, name)
            fail = check_failed(value, direction)
            updated[f"{name}_expected"] = direction
            updated[f"{name}_fail"] = int(fail)
            failed += int(fail)
        updated["manip_failed_checks"] = failed
        updated["manip_condition_fail"] = int(failed >= 2)
        annotated.append(updated)
    return annotated


def factor_means(rows):
    specs = [
        ("processing", "manip_cloud"),
        ("visibility", "manip_visibility"),
        ("output", "manip_assertive"),
        ("visibility", "manip_self_only"),
    ]
    summary = []
    for factor, item in specs:
        for key, group in sorted(group_by(rows, [factor]).items()):
            values = [to_float(row.get(item)) for row in group]
            summary.append(
                {
                    "factor": factor,
                    "level": key[0],
                    "item": item,
                    "n": len(group),
                    "mean": f"{mean(values):.4f}",
                }
            )
    return summary


def participant_exclusions(rows):
    summary = []
    for key, group in sorted(group_by(rows, ["participant_id"]).items()):
        failed_conditions = sum(int(row["manip_condition_fail"]) for row in group)
        summary.append(
            {
                "participant_id": key[0],
                "n_conditions": len(group),
                "failed_conditions": failed_conditions,
                "exclude_primary": int(failed_conditions >= 5),
            }
        )
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--annotated", default="analysis/outputs/manipulation_annotated.csv")
    parser.add_argument("--summary", default="analysis/outputs/manipulation_summary.csv")
    parser.add_argument("--participants", default="analysis/outputs/manipulation_participants.csv")
    args = parser.parse_args()

    rows = annotate_rows(read_rows(args.input))
    write_rows(args.annotated, rows)
    write_rows(args.summary, factor_means(rows))
    write_rows(args.participants, participant_exclusions(rows))
    print(f"Wrote manipulation check outputs to {args.summary}")


if __name__ == "__main__":
    main()
