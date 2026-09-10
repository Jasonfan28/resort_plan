# 04 Snow reliability

## Question

By elevation band, what do baseline and mid-century climate projections
under two emissions scenarios say about snow, and what single transparent
reliability indicator can be validated against historical snowfall?

## Decision

[left for the user]

## Alternatives considered

- Build elevation bands at arbitrary round-number cutoffs (e.g. every
  500 m). Rejected: the master plan already states five named elevation
  points; bands built between those are traceable to a claim, a round-
  number scheme would not be.
- Fabricate a plausible-looking projected snowfall number so the
  reliability indicator would have something to run against. Rejected
  outright: CLAUDE.md rule 6 requires leaving a statement out entirely
  when nothing supports it, labelled "judgment call" only applies to
  method choices, not to inventing a figure.

## Evidence

- [C005] CCCS publishes daily snowfall water equivalent projections
  derived from PCIC's CanDCS-M6 dataset. Source S015.
- [C006] CanDCS-M6 daily data are on a 10 km grid. Source S016.
- [C033] Master plan elevation table: 512 m (bottom) to 2,466 m (Mt.
  Mackenzie summit), 1,713 m lift-accessed vertical.
- [C034] Master plan historical snowfall: RMR 9-14 m/year, Selkirk
  Mountains region 12-18 m/year.
- [C035] Base CanDCS-M6 has no snow variable directly; S015's SWE
  product is a separate, derived dataset.
- [C036] S015's own listed THREDDS catalog URL 404s; the base CanDCS-M6
  archive (26 GCM folders) is reachable at a different, found path, but
  the SWE/indices product's current path is not yet found.

## Inputs

- S034 (data/raw/rmr_master_plan_update_final.pdf): elevation table and
  historical snowfall table.

## Method

- (evidence) Build elevation bands between the plan's own stated points
  rather than arbitrary cutoffs; validated by checking the base band's
  vertical (1,713 m) against the plan's separately stated lift-accessed
  vertical figure, which match exactly.
- (judgment call) Define the reliability indicator as projected seasonal
  snowfall divided by the historical baseline, per elevation band. This
  formula is not itself backed by a claim; it is recorded as a method,
  not evaluated, because no projection data exists yet to run it against.

## Outputs

- data/processed/04_elevation_bands.csv
- data/processed/04_historical_snowfall.json
- (not yet produced: any projected-snowfall or reliability-ratio output)

## Checks

- Band boundaries strictly increasing; base band's vertical equals the
  plan's stated lift-accessed vertical; historical range's low bound
  under its high bound; a `projections_available` flag stays False so a
  downstream step cannot mistake an unrun projection for a zero result.
- Last run: all checks passed.

## Open issues

- This step's central question (baseline vs. mid-century projections
  under two emissions scenarios) is unanswered. The SWE/indices product
  S015 describes has a dead catalog link; the base CanDCS-M6 archive is
  reachable (C036) but pulling one grid cell's projected snowfall for
  Revelstoke, across a baseline and mid-century period and two SSPs,
  needs real OPeNDAP/THREDDS navigation and likely an added package
  (xarray plus a NetCDF/OPeNDAP backend) that has not been done yet.
- A 10 km grid (C006) is coarse relative to a single resort's elevation
  bands; whether that resolution is adequate is still an open method
  question once real data is in hand, not yet a judgment call.
- The historical snowfall figures (C034) give no year range or
  measurement method, which limits how precisely a reliability
  indicator could ever be validated against them even once projections
  exist.

## Status

draft

## Changelog

- 2026-09-10: created.
- 2026-09-10: built elevation bands and recorded the historical
  snowfall baseline from S034; defined but did not evaluate the
  reliability indicator; confirmed a real (if incomplete) THREDDS access
  path for CanDCS-M6. Left as draft, not built, since the step's central
  question is still open.
