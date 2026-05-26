import argparse
from common import SCALE_ITEMS, add_scale_scores, read_rows, write_rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output", nargs="?", default="analysis/outputs/scored.csv")
    args = parser.parse_args()

    rows = [add_scale_scores(row) for row in read_rows(args.input)]
    fieldnames = list(rows[0].keys()) if rows else []
    for scale in SCALE_ITEMS:
        name = f"{scale}_score"
        if name not in fieldnames:
            fieldnames.append(name)
    write_rows(args.output, rows, fieldnames=fieldnames)
    print(f"Wrote {len(rows)} scored rows to {args.output}")


if __name__ == "__main__":
    main()

