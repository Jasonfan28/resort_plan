# 02 Planning documents

## Question

What do the RMR master plan and the City's housing reports say about
capacity, phasing, staff housing, and housing need?

## Decision

[left for the user]

## Alternatives considered

- Have step 03/05/06 each parse the master plan and HNR PDFs themselves,
  wherever they need a figure from them. Rejected: three notebooks
  independently re-reading the same two PDFs is more places for a
  transcription error to happen, and CLAUDE.md already asks for shared
  logic to move to one place rather than being repeated.

## Evidence

- [C001] agent-checked. The Province's list-of-approved-plans page names
  three Revelstoke documents: a 2003 master plan, this 2019 update
  (S034), and a 2024 base lands update.
- [C002] agent-checked. Confirmed directly: S011's cover page reads
  "Appendix A – Comfortable Carry Capacity Tables," April 2019.
- [C030] The 2019 master plan (S034) itself states its CCC figures come
  from Appendix A's Tables 1-1 to 1-4, tying S034 and S011 to one
  planning exercise.
- [C031] S034's Phase 2 plan: a minimum of three employee housing
  buildings, 150-200 beds each, 9.19 ha in the Lower Village.

## Inputs

- S011 (data/raw/S011_rmr_appendix_a_ccc_tables.pdf, local_copy recorded)
- S034 (data/raw/rmr_master_plan_update_final.pdf, local_copy recorded)
- S013 (data/raw/S013_revelstoke_hnr_2024.pdf, local_copy recorded)

## Method

- (evidence) Transcribe only the figures already backed by a claim ID
  (C025 CCC-by-phase, C031 employee housing, C026-C029 housing need)
  into small tables, each with an assert tying it back to its claim ID
  so a future edit to claims.csv without a matching notebook update
  fails loudly instead of silently drifting.
- (judgment call) Keep the master plan's stated bed-count range (150-200)
  rather than picking a single number. Picking a midpoint would be this
  notebook making a call that belongs to step 05.

## Outputs

- data/processed/02_ccc_by_phase.csv
- data/processed/02_employee_housing_phase2.json
- data/processed/02_housing_need_by_component.csv

## Checks

- The housing-need component columns must sum to the source's own stated
  totals (814 over 5 years, 2,367 over 20 years).
- CCC must rise phase over phase (existing < buildout).
- Last run: both checks passed.

## Open issues

- S010, S011, and S013 all turned out to be reachable by WebFetch and are
  now downloaded and read, despite tools/verify_sources.py getting HTTP
  503/manual from this machine for S010 and S011. That gap between a
  scripted check and WebFetch is itself worth someone's attention;
  verify_sources.py's manual status for S011 undersells how confirmed it
  now is.
- The Oscar Lands Master Plan (C015, step 07) has not been checked
  against S034 or S012 yet. Whether it belongs in this step or stays in
  step 07 is still an open call.
- S011's per-lift Table 1-1 rows (needed if step 03 wants to reproduce
  Phase 1's CCC total from scratch, not just cite it) have not been
  transcribed; pypdf's text extraction jumbled the table's row order on a
  first look, so that needs a more careful pass (e.g. pdfplumber's table
  extraction) when step 03 is built, not a quick fix here.

## Status

built

## Changelog

- 2026-09-10: created.
- 2026-09-10: read S011, S034, S013 directly; added C030, C031; built
  notebooks/02_planning_documents.ipynb; ran clean via `/run 02`.
