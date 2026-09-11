"""Consolidate data/processed outputs into docs/data/summary.json for
docs/index.html to fetch. Run after the pipeline so it reflects the
latest data/processed state.

Usage:
    python tools/build_docs_data.py
"""

import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED = os.path.join(ROOT, "data", "processed")
DOCS_DATA = os.path.join(ROOT, "docs", "data")

sys.path.insert(0, os.path.join(ROOT, "src"))
from resort.ledger import read_ledger  # noqa: E402


def read_csv_rows(name):
    path = os.path.join(PROCESSED, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_json(name):
    path = os.path.join(PROCESSED, name)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ledger = read_ledger()
    claims = ledger["claims"]
    status_counts = {}
    for c in claims.values():
        status_counts[c["status"]] = status_counts.get(c["status"], 0) + 1

    summary = {
        "evidence": {
            "n_sources": len(ledger["sources"]),
            "n_claims": len(claims),
            "claims_by_status": status_counts,
        },
        "scenario_table": read_csv_rows("08_scenario_table.csv"),
        "elevation_bands": read_csv_rows("04_elevation_bands.csv"),
        "historical_snowfall": read_json("04_historical_snowfall.json"),
        "zoning_top10": sorted(
            read_csv_rows("07_zoning_by_parcel_count.csv"),
            key=lambda r: int(r["parcel_count"]),
            reverse=True,
        )[:10],
        "resort_lands_dpa": read_json("07_resort_lands_dpa.json"),
        "housing_need_by_component": read_csv_rows("02_housing_need_by_component.csv"),
        "rental_vacancy": read_json("06_rental_vacancy.json"),
    }

    os.makedirs(DOCS_DATA, exist_ok=True)
    out_path = os.path.join(DOCS_DATA, "summary.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"wrote {os.path.relpath(out_path, ROOT)}")


if __name__ == "__main__":
    main()
