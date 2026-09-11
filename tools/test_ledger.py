"""Standard-library tests for src/resort/ledger.py.

Every test writes its own throwaway copies of sources.csv and claims.csv
under a temporary directory. The real files in research/ are never opened.

Usage:
    python tools/test_ledger.py
"""

import csv
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from resort.ledger import LedgerError, cite, read_ledger  # noqa: E402

SOURCE_FIELDS = [
    "id", "type", "title", "authors", "year", "doi", "url", "accessed",
    "licence", "local_copy", "verified_exists", "verified_on", "verify_note",
    "human_verified", "notes",
]
CLAIM_FIELDS = [
    "claim_id", "step", "claim", "source_id", "locator", "status",
    "conflicts_with", "notes",
]


def _source(id, authors, year, verified_exists="pass", title="A title", doi=""):
    row = {field: "" for field in SOURCE_FIELDS}
    row.update(
        id=id, type="paper", title=title, authors=authors, year=year, doi=doi,
        verified_exists=verified_exists,
    )
    return row


def _claim(claim_id, source_id, status, claim="A claim", step="01"):
    row = {field: "" for field in CLAIM_FIELDS}
    row.update(
        claim_id=claim_id, step=step, claim=claim, source_id=source_id,
        locator="p1", status=status,
    )
    return row


def _write_csv(path, fields, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.sources_path = os.path.join(self.tmp.name, "sources.csv")
        self.claims_path = os.path.join(self.tmp.name, "claims.csv")

    def _ledger(self, sources, claims):
        _write_csv(self.sources_path, SOURCE_FIELDS, sources)
        _write_csv(self.claims_path, CLAIM_FIELDS, claims)
        return read_ledger(self.claims_path, self.sources_path)

    def test_needs_review_claim_raises(self):
        ledger = self._ledger(
            sources=[_source("S001", "Smith, J.", "2020")],
            claims=[_claim("C001", "S001", "needs-review")],
        )
        with self.assertRaises(LedgerError):
            cite("C001", ledger)

    def test_human_verified_but_source_manual_raises(self):
        ledger = self._ledger(
            sources=[_source("S002", "Smith, J.", "2020", verified_exists="manual")],
            claims=[_claim("C002", "S002", "human-verified")],
        )
        with self.assertRaises(LedgerError):
            cite("C002", ledger)

    def test_author_count_labels(self):
        ledger = self._ledger(
            sources=[
                _source("S010", "City of Revelstoke", "2024"),
                _source("S011", "Smith, J.; Doe, A.", "2020"),
                _source(
                    "S012",
                    "Pimentel, J. F.; Murta, L.; Braganholo, V.; Freire, J.",
                    "2019",
                ),
            ],
            claims=[
                _claim("C010", "S010", "human-verified"),
                _claim("C011", "S011", "human-verified"),
                _claim("C012", "S012", "human-verified"),
            ],
        )
        self.assertEqual(cite("C010", ledger), "(City of Revelstoke 2024)")
        self.assertEqual(cite("C011", ledger), "(Smith and Doe 2020)")
        self.assertEqual(cite("C012", ledger), "(Pimentel et al. 2019)")

    def test_author_name_with_umlaut(self):
        ledger = self._ledger(
            sources=[_source("S013", "Nüst, D.", "2018")],
            claims=[_claim("C013", "S013", "human-verified")],
        )
        self.assertEqual(cite("C013", ledger), "(Nüst 2018)")

    def test_missing_year_omits_trailing_space(self):
        ledger = self._ledger(
            sources=[_source("S014", "Environment and Climate Change Canada", "")],
            claims=[_claim("C014", "S014", "human-verified")],
        )
        self.assertEqual(cite("C014", ledger), "(Environment and Climate Change Canada)")

    def test_unclosed_quote_raises_row_count_error(self):
        _write_csv(
            self.sources_path,
            SOURCE_FIELDS,
            [_source("S001", "Smith, J.", "2020")],
        )
        # C001's claim field opens a quote it never closes, so the CSV
        # reader swallows the C002 line into C001's field instead of
        # parsing it as its own row.
        with open(self.claims_path, "w", newline="", encoding="utf-8") as f:
            f.write(",".join(CLAIM_FIELDS) + "\n")
            f.write('C001,01,"unterminated,S001,p1,needs-review,,notes1\n')
            f.write("C002,01,Another claim,S001,p2,needs-review,,notes2\n")
        with self.assertRaises(LedgerError):
            read_ledger(self.claims_path, self.sources_path)

    def test_duplicate_source_id_raises(self):
        # Two unrelated rows sharing an ID (e.g. two agents each picking
        # the next free-looking number without seeing each other's write)
        # would otherwise silently shadow one another in the sources dict.
        with self.assertRaises(LedgerError):
            self._ledger(
                sources=[
                    _source("S001", "Smith, J.", "2020", title="First source"),
                    _source("S001", "Doe, A.", "2021", title="Second source"),
                ],
                claims=[_claim("C001", "S001", "needs-review")],
            )

    def test_duplicate_claim_id_raises(self):
        with self.assertRaises(LedgerError):
            self._ledger(
                sources=[_source("S001", "Smith, J.", "2020")],
                claims=[
                    _claim("C001", "S001", "needs-review", claim="First claim"),
                    _claim("C001", "S001", "needs-review", claim="Second claim"),
                ],
            )


if __name__ == "__main__":
    unittest.main()
