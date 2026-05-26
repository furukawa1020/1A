import argparse
from common import SCALE_ITEMS, add_scale_scores, group_by, mean, read_rows, to_float, write_rows


def write_cell_means(rows, output):
    scored = [add_scale_scores(row) for row in rows]
    results = []
    for key, group in sorted(group_by(scored, ["processing", "visibility", "output"]).items()):
        result = {
            "processing": key[0],
            "visibility": key[1],
            "output": key[2],
            "n": len(group),
        }
        for scale in SCALE_ITEMS:
            result[f"{scale}_score_mean"] = f"{mean([to_float(row.get(f'{scale}_score')) for row in group]):.4f}"
        results.append(result)
    write_rows(output, results)


def try_statsmodels(rows, output_text):
    try:
        import pandas as pd
        import statsmodels.formula.api as smf
    except ImportError:
        return False

    scored = [add_scale_scores(row) for row in rows]
    df = pd.DataFrame(scored)
    lines = []
    for scale in SCALE_ITEMS:
        score = f"{scale}_score"
        df[score] = pd.to_numeric(df[score], errors="coerce")
        formula = f"{score} ~ C(processing) * C(visibility) * C(output)"
        lines.append(f"\n## {scale.upper()}\n")
        lines.append(f"Formula: {formula} + (1 | participant_id)\n")
        model = smf.mixedlm(formula, data=df, groups=df["participant_id"])
        fit = model.fit(reml=False)
        lines.append(str(fit.summary()))
        lines.append("\n")

    with open(output_text, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--model-output", default="analysis/outputs/mixed_models.txt")
    parser.add_argument("--cell-means", default="analysis/outputs/mixed_model_cell_means.csv")
    args = parser.parse_args()

    rows = read_rows(args.input)
    if try_statsmodels(rows, args.model_output):
        print(f"Wrote mixed model summaries to {args.model_output}")
    else:
        write_cell_means(rows, args.cell_means)
        with open(args.model_output, "w", encoding="utf-8") as handle:
            handle.write(
                "statsmodels is not installed. Primary model formulas:\n"
                "score ~ C(processing) * C(visibility) * C(output) + (1 | participant_id)\n"
                f"Cell means were written to {args.cell_means}.\n"
            )
        print(f"statsmodels unavailable; wrote cell means to {args.cell_means}")


if __name__ == "__main__":
    main()

