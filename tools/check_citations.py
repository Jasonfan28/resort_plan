"""Validate research/claims.csv against research/sources.csv, and scan
steps/*.md and notebooks/*.ipynb for citation IDs that do not exist.

Usage:
    python tools/check_citations.py            # validate ledger, scan for unknown IDs
    python tools/check_citations.py --report    # also require every claim cited in
                                                 # notebooks/09_report.ipynb to be
                                                 # human-verified with a passed source
"""

import csv
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAIMS = os.path.join(ROOT, "research", "claims.csv")
SOURCES = os.path.join(ROOT, "research", "sources.csv")
REPORT_NOTEBOOK = os.path.join(ROOT, "notebooks", "09_report.ipynb")
STATUSES = {"needs-review", "agent-checked", "human-verified", "rejected"}
ID_RE = re.compile(r"\bC\d+\b")


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_duplicate_ids(rows, key, label):
    errors = []
    seen = set()
    for row in rows:
        value = row[key]
        if value in seen:
            errors.append(f"duplicate {label} {value!r}: two rows share this ID")
        seen.add(value)
    return errors


def check_ledger(claims, sources):
    errors = []
    errors += check_duplicate_ids(sources, "id", "source id")
    errors += check_duplicate_ids(claims, "claim_id", "claim id")
    source_ids = {s["id"] for s in sources}
    claim_ids = {c["claim_id"] for c in claims}
    for c in claims:
        if c["source_id"] not in source_ids:
            errors.append(
                f"{c['claim_id']}: source_id {c['source_id']!r} not found in sources.csv"
            )
        if c["status"] not in STATUSES:
            errors.append(
                f"{c['claim_id']}: status {c['status']!r} is not one of {sorted(STATUSES)}"
            )
        conflicts = [x.strip() for x in c.get("conflicts_with", "").split(";") if x.strip()]
        for other in conflicts:
            if other not in claim_ids:
                errors.append(
                    f"{c['claim_id']}: conflicts_with {other!r} not found in claims.csv"
                )
    return errors


def notebook_text(path):
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)
    chunks = []
    for cell in nb.get("cells", []):
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)
        chunks.append(source)
    return "\n".join(chunks)


def scan_for_unknown_ids(claim_ids):
    errors = []
    for path in sorted(glob.glob(os.path.join(ROOT, "steps", "*.md"))):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for cid in sorted(set(ID_RE.findall(text))):
            if cid not in claim_ids:
                errors.append(f"{os.path.relpath(path, ROOT)}: references unknown claim {cid}")
    for path in sorted(glob.glob(os.path.join(ROOT, "notebooks", "*.ipynb"))):
        text = notebook_text(path)
        for cid in sorted(set(ID_RE.findall(text))):
            if cid not in claim_ids:
                errors.append(f"{os.path.relpath(path, ROOT)}: references unknown claim {cid}")
    return errors


def check_report(claims_by_id, sources_by_id):
    errors = []
    if not os.path.exists(REPORT_NOTEBOOK):
        return errors
    text = notebook_text(REPORT_NOTEBOOK)
    for cid in sorted(set(ID_RE.findall(text))):
        claim = claims_by_id.get(cid)
        if claim is None:
            continue  # already reported by scan_for_unknown_ids
        if claim["status"] != "human-verified":
            errors.append(
                f"09_report.ipynb cites {cid} but its status is {claim['status']!r}, "
                "not human-verified"
            )
            continue
        source = sources_by_id.get(claim["source_id"])
        if source is None or source["verified_exists"] != "pass":
            got = "missing source" if source is None else f"verified_exists={source['verified_exists']!r}"
            errors.append(f"09_report.ipynb cites {cid} but its source has not passed verification ({got})")
    return errors


def main():
    report_mode = "--report" in sys.argv
    claims = read_csv(CLAIMS)
    sources = read_csv(SOURCES)
    claim_ids = {c["claim_id"] for c in claims}
    claims_by_id = {c["claim_id"]: c for c in claims}
    sources_by_id = {s["id"]: s for s in sources}

    errors = check_ledger(claims, sources)
    errors += scan_for_unknown_ids(claim_ids)
    if report_mode:
        errors += check_report(claims_by_id, sources_by_id)

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print(f"{len(errors)} problem(s) found.", file=sys.stderr)
        sys.exit(1)

    print("check_citations: OK" + (" (report mode)" if report_mode else ""))


if __name__ == "__main__":
    main()
