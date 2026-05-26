import argparse
import math
from common import group_by, mean, read_rows, scale_score, write_rows


def stdev(values):
    if len(values) < 2:
        return math.nan
    avg = mean(values)
    return math.sqrt(sum((value - avg) ** 2 for value in values) / (len(values) - 1))


def paired_differences(rows, reference):
    diffs = []
    for _, group in group_by(rows, ["participant_id"]).items():
        by_condition = {row.get("condition_id"): row for row in group}
        if "C8" in by_condition and reference in by_condition:
            c8 = scale_score(by_condition["C8"], "sous")
            ref = scale_score(by_condition[reference], "sous")
            if not math.isnan(c8) and not math.isnan(ref):
                diffs.append(c8 - ref)
    return diffs


def summarize(reference, diffs, margin):
    avg = mean(diffs)
    sd = stdev(diffs)
    if diffs and not math.isnan(sd):
        se = sd / math.sqrt(len(diffs))
        lower95 = avg - 1.96 * se
    else:
        lower95 = math.nan
    return {
        "comparison": f"C8 - {reference}",
        "n_pairs": len(diffs),
        "margin": margin,
        "mean_difference": "" if math.isnan(avg) else f"{avg:.4f}",
        "lower95_normal_approx": "" if math.isnan(lower95) else f"{lower95:.4f}",
        "pass_mean_rule": int((not math.isnan(avg)) and avg >= -margin),
        "pass_lower95_rule": int((not math.isnan(lower95)) and lower95 >= -margin),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output", nargs="?", default="analysis/outputs/noninferiority_sous.csv")
    parser.add_argument("--margin", type=float, default=0.5)
    args = parser.parse_args()

    rows = read_rows(args.input)
    results = [
        summarize("C7", paired_differences(rows, "C7"), args.margin),
        summarize("C1", paired_differences(rows, "C1"), args.margin),
    ]
    write_rows(args.output, results)
    print(f"Wrote SOUS non-inferiority results to {args.output}")


if __name__ == "__main__":
    main()

