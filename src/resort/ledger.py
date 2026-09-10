"""Read research/claims.csv and research/sources.csv and format citations.

Only claims with status "human-verified", whose source has
verified_exists == "pass", can be cited. That keeps every number in the
report traceable to a source someone actually checked.
"""

import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLAIMS = os.path.join(ROOT, "research", "claims.csv")
SOURCES = os.path.join(ROOT, "research", "sources.csv")


class LedgerError(Exception):
    pass


def _read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _count_id_lines(path, prefix):
    pattern = re.compile(r"^" + re.escape(prefix) + r"\d+,")
    with open(path, encoding="utf-8") as f:
        return sum(1 for line in f if pattern.match(line))


def _check_row_count(path, prefix, rows):
    expected = _count_id_lines(path, prefix)
    if len(rows) != expected:
        raise LedgerError(
            f"{path}: read {len(rows)} row(s) but {expected} line(s) start with "
            f"a {prefix}### ID. A quoting error may have merged or dropped rows."
        )


def read_ledger(claims_path=CLAIMS, sources_path=SOURCES):
    """Load and cross-check the two ledgers.

    Returns a dict with claims (by claim_id) and sources (by id). Raises
    LedgerError if either file's row count disagrees with its ID-line count.
    """
    claims = _read_csv(claims_path)
    sources = _read_csv(sources_path)
    _check_row_count(claims_path, "C", claims)
    _check_row_count(sources_path, "S", sources)

    return {
        "claims": {c["claim_id"]: c for c in claims},
        "sources": {s["id"]: s for s in sources},
    }


def _split_authors(authors_field):
    return [a.strip() for a in authors_field.split(";") if a.strip()]


def _surname(author):
    # "Last, First" -> "Last". A bare org name has no comma and passes through.
    if "," in author:
        return author.split(",", 1)[0].strip()
    return author


def _author_label(authors_field):
    authors = _split_authors(authors_field)
    if not authors:
        return "Unknown"
    if len(authors) == 1:
        return _surname(authors[0])
    if len(authors) == 2:
        return f"{_surname(authors[0])} and {_surname(authors[1])}"
    return f"{_surname(authors[0])} et al."


def cite(claim_id, ledger):
    """Return a short citation label like "(Pimentel et al. 2019)".

    Raises LedgerError if the claim is missing, not human-verified, or its
    source has not passed verification.
    """
    claim = ledger["claims"].get(claim_id)
    if claim is None:
        raise LedgerError(f"claim {claim_id} not found")
    if claim["status"] != "human-verified":
        raise LedgerError(
            f"claim {claim_id} is not human-verified (status: {claim['status']!r})"
        )
    source = ledger["sources"].get(claim["source_id"])
    if source is None:
        raise LedgerError(
            f"claim {claim_id} references unknown source {claim['source_id']!r}"
        )
    if source["verified_exists"] != "pass":
        raise LedgerError(
            f"source {source['id']} for claim {claim_id} has not passed "
            f"verification (verified_exists: {source['verified_exists']!r})"
        )
    label = _author_label(source["authors"])
    year = source["year"].strip()
    return f"({label} {year})"


def references(ledger):
    """Formatted reference list for sources behind human-verified claims."""
    cited_ids = sorted(
        {
            c["source_id"]
            for c in ledger["claims"].values()
            if c["status"] == "human-verified"
            and ledger["sources"].get(c["source_id"], {}).get("verified_exists") == "pass"
        }
    )
    entries = []
    for source_id in cited_ids:
        source = ledger["sources"][source_id]
        year = source["year"].strip()
        entry = f"{source['authors']} ({year}). {source['title']}."
        doi = source.get("doi", "").strip()
        if doi:
            url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
            entry += f" {url}"
        entries.append(entry)
    return entries
