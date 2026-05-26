import argparse
from common import REQUIRED_COLUMNS, condition_sort_key, read_rows, write_rows


def clean_value(value):
    if value is None:
        return ""
    return str(value).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output", nargs="?", default="analysis/outputs/clean.csv")
    args = parser.parse_args()

    rows = read_rows(args.input)
    cleaned = []
    for row in rows:
        cleaned.append({key: clean_value(value) for key, value in row.items()})

    missing = [column for column in REQUIRED_COLUMNS if cleaned and column not in cleaned[0]]
    if missing:
        raise SystemExit(f"Missing required columns: {missing}")

    cleaned.sort(key=lambda row: (row.get("participant_id", ""), condition_sort_key(row)))
    fieldnames = list(dict.fromkeys(REQUIRED_COLUMNS + [key for row in cleaned for key in row.keys()]))
    write_rows(args.output, cleaned, fieldnames=fieldnames)
    print(f"Wrote {len(cleaned)} rows to {args.output}")


if __name__ == "__main__":
    main()

