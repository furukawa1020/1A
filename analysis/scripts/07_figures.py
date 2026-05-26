import argparse
from collections import defaultdict
from common import SCALE_ITEMS, add_scale_scores, group_by, mean, read_rows, to_float


def condition_means(rows):
    scored = [add_scale_scores(row) for row in rows]
    results = []
    for key, group in sorted(group_by(scored, ["condition_id"]).items(), key=lambda item: int(item[0][0][1:])):
        result = {"condition_id": key[0]}
        for scale in SCALE_ITEMS:
            result[scale] = mean([to_float(row.get(f"{scale}_score")) for row in group])
        results.append(result)
    return results


def bar(width, value):
    if value != value:
        return ""
    bar_width = max(0, min(width, value / 7 * width))
    return f'<span class="bar"><span style="width:{bar_width:.1f}px"></span></span>'


def html_report(means):
    width = 180
    rows = []
    for row in means:
        cells = [f"<td>{row['condition_id']}</td>"]
        for scale in SCALE_ITEMS:
            value = row[scale]
            label = "" if value != value else f"{value:.2f}"
            cells.append(f"<td>{label} {bar(width, value)}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>PSTT Figure Drafts</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 32px; color: #1c1f21; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border-bottom: 1px solid #d8d9d2; padding: 8px; text-align: left; }}
.bar {{ display: inline-block; width: {width}px; height: 12px; background: #eef2f0; vertical-align: middle; }}
.bar span {{ display: block; height: 12px; background: #0f766e; }}
</style>
</head>
<body>
<h1>PSTT Condition Means</h1>
<table>
<thead><tr><th>Condition</th>{''.join(f'<th>{scale.upper()}</th>' for scale in SCALE_ITEMS)}</tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output", nargs="?", default="analysis/outputs/figures.html")
    args = parser.parse_args()

    means = condition_means(read_rows(args.input))
    with open(args.output, "w", encoding="utf-8") as handle:
        handle.write(html_report(means))
    print(f"Wrote figure draft HTML to {args.output}")


if __name__ == "__main__":
    main()

