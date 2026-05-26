"""Shared helpers for PSTT analysis scripts.

PSTT分析スクリプトで共通利用する補助関数。
"""

import csv
import json
import math
from pathlib import Path


SCALE_ITEMS = {
    "mfs": ["mfs_1", "mfs_2", "mfs_3", "mfs_4", "mfs_5"],
    "lis": ["lis_1", "lis_2", "lis_3", "lis_4", "lis_5"],
    "sous": ["sous_1", "sous_2", "sous_3", "sous_4", "sous_5"],
    "wu": ["wu_1", "wu_2", "wu_3"],
    "wd": ["wd_1", "wd_2", "wd_3"],
}

REQUIRED_COLUMNS = [
    "participant_id",
    "study_version",
    "condition_id",
    "processing",
    "visibility",
    "output",
    "condition_order",
    "mfs_1",
    "mfs_2",
    "mfs_3",
    "mfs_4",
    "mfs_5",
    "lis_1",
    "lis_2",
    "lis_3",
    "lis_4",
    "lis_5",
    "sous_1",
    "sous_2",
    "sous_3",
    "sous_4",
    "sous_5",
    "wu_1",
    "wu_2",
    "wu_3",
    "wd_1",
    "wd_2",
    "wd_3",
    "manip_cloud",
    "manip_visibility",
    "manip_assertive",
    "free_text",
]


def ensure_parent(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def to_float(value):
    if value is None or value == "":
        return math.nan
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def mean(values):
    numeric = [value for value in values if not math.isnan(value)]
    if not numeric:
        return math.nan
    return sum(numeric) / len(numeric)


def read_rows(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict) and "responses" in data:
            rows = []
            for response in data["responses"]:
                row = {
                    "participant_id": data.get("participant_id", ""),
                    "study_version": data.get("study_version", ""),
                    "condition_sequence": " ".join(data.get("condition_sequence", [])),
                    "order_strategy": data.get("order_strategy", ""),
                }
                row.update(response)
                rows.append(row)
            return rows
        if isinstance(data, list):
            return data
        raise ValueError(f"Unsupported JSON shape: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path, rows, fieldnames=None):
    rows = list(rows)
    ensure_parent(path)
    if fieldnames is None:
        fieldnames = []
        seen = set()
        for row in rows:
            for key in row.keys():
                if key not in seen:
                    seen.add(key)
                    fieldnames.append(key)
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def scale_score(row, scale):
    return mean([to_float(row.get(item)) for item in SCALE_ITEMS[scale]])


def add_scale_scores(row):
    updated = dict(row)
    for scale in SCALE_ITEMS:
        updated[f"{scale}_score"] = scale_score(row, scale)
    return updated


def group_by(rows, keys):
    grouped = {}
    for row in rows:
        key = tuple(row.get(name, "") for name in keys)
        grouped.setdefault(key, []).append(row)
    return grouped


def condition_sort_key(row):
    condition = str(row.get("condition_id", "C999"))
    try:
      return int(condition[1:])
    except ValueError:
      return 999
