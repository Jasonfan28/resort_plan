"""Check that every source in research/sources.csv exists.

A pass means the DOI resolves in OpenAlex with a matching title and year,
or the URL answers without an error. It does NOT mean the source supports
any claim. That check happens in research/claims.csv and needs a person.

Usage:
    python tools/verify_sources.py          # only rows with blank verified_exists
    python tools/verify_sources.py --all    # recheck every row

Set OPENALEX_API_KEY in your environment. OpenAlex requires a key since
February 2026, and the free key covers single-work lookups.
"""

import csv
import datetime
import difflib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "research", "sources.csv")
UA = "resort-housing-revelstoke source check (github research repo)"
TITLE_MATCH = 0.85


def normalize(text):
    return re.sub(r"[^a-z0-9 ]", "", (text or "").lower()).strip()


def bare_doi(doi):
    return re.sub(r"^(https?://(dx\.)?doi\.org/|doi:)", "", doi.strip(), flags=re.I)


def check_doi(row):
    doi = bare_doi(row["doi"])
    url = "https://api.openalex.org/works/doi:" + urllib.parse.quote(doi, safe="/")
    key = os.environ.get("OPENALEX_API_KEY")
    if key:
        url += "?api_key=" + urllib.parse.quote(key)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            work = json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "fail", "DOI not found in OpenAlex"
        return "manual", f"OpenAlex HTTP {e.code}"
    except (urllib.error.URLError, TimeoutError) as e:
        return "manual", f"network error: {e}"

    ratio = difflib.SequenceMatcher(
        None, normalize(work.get("title")), normalize(row["title"])
    ).ratio()
    problems = []
    if ratio < TITLE_MATCH:
        problems.append(f"title mismatch ({ratio:.2f}): OpenAlex has '{work.get('title')}'")
    if row.get("year") and str(work.get("publication_year")) != row["year"].strip():
        problems.append(f"year mismatch: OpenAlex has {work.get('publication_year')}")
    if problems:
        return "fail", "; ".join(problems)
    return "pass", "DOI, title, and year match OpenAlex"


def check_url(row):
    req = urllib.request.Request(row["url"], headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if "html" not in ctype:
                return "pass", f"reachable ({ctype or 'unknown type'}), title not checked"
            page = normalize(resp.read(3_000_000).decode("utf-8", errors="ignore"))
    except urllib.error.HTTPError as e:
        if e.code in (404, 410):
            return "fail", f"URL gone (HTTP {e.code})"
        # Many sites refuse scripted requests. That says nothing about whether the page exists.
        return "manual", f"HTTP {e.code}, open it in a browser"
    except (urllib.error.URLError, TimeoutError) as e:
        return "manual", f"network error: {e}"

    # Some sites answer 200 for pages that no longer exist, so check the page is the one recorded.
    words = [w for w in normalize(row["title"]).split() if len(w) > 3]
    if not words:
        return "manual", "reachable, but title too short to check"
    found = sum(w in page for w in words) / len(words)
    if found < 0.6:
        return "manual", f"reachable, but only {found:.0%} of title words appear on the page"
    return "pass", f"reachable, {found:.0%} of title words found on page"


def main():
    recheck_all = "--all" in sys.argv
    with open(SOURCES, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    today = datetime.date.today().isoformat()
    failures = 0
    for row in rows:
        if row["verified_exists"] and not recheck_all:
            continue
        if row["doi"].strip():
            status, reason = check_doi(row)
        elif row["url"].strip():
            status, reason = check_url(row)
        else:
            status, reason = "fail", "no DOI or URL"
        row["verified_exists"] = status
        row["verified_on"] = today
        row["verify_note"] = reason
        failures += status == "fail"
        print(f"{row['id']}: {status} - {reason}")

    with open(SOURCES, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    if failures:
        print(f"{failures} source(s) failed. Fix or remove them.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
