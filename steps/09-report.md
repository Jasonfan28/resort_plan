# 09 Report

## Question

What prose, built entirely from data/processed files and citing every
claim with cite(), presents this analysis for publication?

## Decision

[left for the user]

## Alternatives considered

- Cite every claim individually inline, even when several land on the
  same source. Rejected once rendered: back-to-back identical citation
  labels (e.g. two copies of "(City of Revelstoke)") read as a
  transcription mistake, not a deliberate multi-source citation. A
  `cite_many()` helper (defined in the notebook) still calls `cite()`
  on every claim ID individually, so each is still checked, but prints
  only the distinct labels.

## Evidence

No claims are tagged to this step directly; it cites claims already
established elsewhere. Every human-verified claim used is listed in
data/processed/09_cited_claims.json.

## Inputs

- research/claims.csv, research/sources.csv (via read_ledger() and
  cite())
- data/processed/02_*, 03_*, 04_*, 05_*, 06_*, 07_*, 08_* (every prior
  step's outputs)

## Method

- (evidence) Every factual sentence's numbers are f-string
  interpolations from a data/processed variable, never a literal typed
  into the template; every factual sentence carries at least one
  cite()/cite_many() call.
- (judgment call) Only cite claims that are human-verified with a
  passed source. Several related claims (C037-C039, C048) restate or
  refine facts this report already cites via other, verified claims;
  they are not yet human-verified themselves and are simply not used,
  rather than cited and immediately failing the gate.

## Outputs

- data/processed/09_cited_claims.json (the exact claim IDs cited, for
  audit)

## Checks

- Every cited claim ID must pass cite() without raising (human-verified
  + source verified_exists=pass). tools/check_citations.py --report
  passes.
- Last run: all checks passed, 29 distinct claims cited.

## Open issues

- This report does not answer the snow-projection or land-unit-capacity
  halves of the project's original questions, and says so explicitly in
  its own "What this report does not claim" section, rather than
  reading as complete.
- C004 (demand-factor conflict), C008 (could not check), C023 (JS-only
  portal, could not check), C037-C039 and C048 (never independently
  verified, though closely related to cited claims) are not cited.
- The RMR headcount conflict (C009 vs. C010) is stated as unresolved,
  per CLAUDE.md rule 5, rather than picked.

## Status

built

## Changelog

- 2026-09-10: created.
- 2026-09-10: reassessed once steps 01-08 were built; left blocked on
  human-verified sign-off.
- 2026-09-10: user promoted all 43 then-agent-checked claims to
  human-verified; built notebooks/09_report.ipynb citing 29 of them;
  `check_citations.py --report` passes. Fixed two ledger bugs surfaced
  while writing this report: cite() left a trailing space when a
  source's year was blank, and several sources' authors fields
  (embedded parentheticals/commas) produced garbled or oddly verbose
  citation labels.
