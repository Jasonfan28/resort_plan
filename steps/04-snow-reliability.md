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
  product is a separate, derived dataset. **Conflicts with [C064].**
- [C036] S015's own listed THREDDS catalog URL 404s; the base CanDCS-M6
  archive (26 GCM folders) is reachable at a different, found path, but
  the SWE/indices product's current path is not yet found.
- [C064] (new, needs-review) **The SWE/indices path now works.**
  Retried this session: birdhouse/disk3/cccs_portal/indices/Final/
  CanDCS-M6/sntot/YS/{ssp126,ssp245,ssp370,ssp585}/simulations_30yAvg/
  serves real, individually downloadable NetCDF files -- 30-year-mean
  annual total snowfall per GCM, all 4 SSPs, 1951-2100, with
  baseline-period deltas in the same file, and OPeNDAP subsetting
  confirmed working (no full download needed). Also found the base
  per-model archive itself contains a raw prsn (snowfall) variable,
  which appears to conflict with C035. **Conflicts with [C035].**

## Inputs

- S034 (data/raw/rmr_master_plan_update_final.pdf): elevation table and
  historical snowfall table.
- **Proposed addition:** S015 via the corrected THREDDS path (C064),
  read by OPeNDAP subsetting (no full-file download), for at least two
  SSP scenarios (e.g. ssp245 and ssp585, a middle and a high-emissions
  case, satisfying the step's "two emissions scenarios" ask) at a
  baseline and a mid-century 30-year-mean period.
- S048 (HRDEM 1m mosaic) and the AOI (step 03) for the grid-cell-vs-
  terrain elevation comparison.

## Method

- (evidence) Build elevation bands between the plan's own stated points
  rather than arbitrary cutoffs; validated by checking the base band's
  vertical (1,713 m) against the plan's separately stated lift-accessed
  vertical figure, which match exactly.
- (judgment call) Define the reliability indicator as projected seasonal
  snowfall divided by the historical baseline, per elevation band. This
  formula is not itself backed by a claim; it was recorded as a method,
  not evaluated, before C064. See the proposed method below for how it
  would now actually be run.

### Proposed spatial + climate method (not yet built)

- (evidence) **Elevation-band area and run length**: using step 03's AOI
  and DEM, replace the current 3-row band table with real area (and, if
  step 03's runs layer exists by then, run length) per elevation band x
  aspect class. Aspect binning (e.g. 4-way vs. 8-way compass bins) is a
  judgment call, sensitivity-tested by reporting both.
- (evidence) **Climate, now that access works (C064)**: pull 30-year-
  mean annual total snowfall (sntot) for at least ssp245 and ssp585, at
  a baseline period and a mid-century period, via OPeNDAP subsetting
  (no full-file download). Overlay the grid cell(s) covering RMR on the
  DEM/AOI and report the gap between the grid cell's own nominal
  elevation and the AOI's actual terrain elevation range, before
  applying any lapse-rate adjustment. A lapse rate to adjust grid-cell
  snowfall to actual terrain elevation is a judgment call needing a
  source or a labelled, sensitivity-tested value (e.g. a standard
  environmental lapse rate vs. a snow-specific one), not yet chosen.
  First resolve the C035/C064 conflict about which variable (the
  indices product's sntot, vs. the base archive's raw prsn) is the
  right input, since build should not silently pick one.
- (optional, separate approval required) **Sentinel-2 snow presence**:
  not part of this proposal. Only to be attempted if approved
  separately after Phase 1, and even then it validates snow cover
  (presence/absence on a date), not annual snowfall depth -- C034 is a
  different quantity and cannot be used to validate it quantitatively,
  only for a plausibility check (e.g. no snow in July, snow present at
  high elevation in April).

## Outputs

- data/processed/04_elevation_bands.csv
- data/processed/04_historical_snowfall.json
- (not yet produced: any projected-snowfall or reliability-ratio output)
- **Proposed additions:**
  - data/processed/04_elevation_aspect_bands.csv (area, and run length
    once step 03 provides it, by elevation band x aspect)
  - data/processed/04_climate_grid_overlay.csv or .json (grid cell(s)
    over the AOI, nominal grid elevation vs. actual terrain elevation
    range, before any adjustment)
  - data/processed/04_snow_projection.csv (sntot by SSP x period, once
    the C035/C064 variable question and the lapse-rate judgment call are
    resolved) -- or, if either blocks it, an explicit note of exactly
    what is still missing, not a filled-in number.

## Checks

- Band boundaries strictly increasing; base band's vertical equals the
  plan's stated lift-accessed vertical; historical range's low bound
  under its high bound; a `projections_available` flag stays False so a
  downstream step cannot mistake an unrun projection for a zero result.
- Last run: all checks passed.
- **Proposed additions:**
  - Elevation-aspect band areas sum to the AOI's total area (an
    independent-number check against step 03's own AOI area).
  - Grid-cell-vs-terrain elevation gap reported explicitly (a number,
    not just a claim it exists), before any lapse-rate adjustment.
  - If the OPeNDAP read fails when actually attempted in a notebook,
    record the exact error and stop that part, the same discipline this
    step already applied once to the dead THREDDS link.

## Open issues

- **Largely resolved (2026-09-10):** the SWE/indices access blocker is
  gone (C064). What remains before projections can actually be pulled:
  (a) resolve the C035/C064 conflict over which snowfall variable is
  authoritative, and (b) choose and source (or label as a sensitivity-
  tested judgment call) a lapse rate to adjust grid-cell snowfall to
  actual terrain elevation.
- A 10 km grid (C006) is coarse relative to a single resort's elevation
  bands; the grid-cell-vs-terrain elevation gap check (proposed above)
  is meant to make exactly how coarse it is visible as a number, not
  just a general caveat.
- The historical snowfall figures (C034) give no year range or
  measurement method, which limits how precisely a reliability
  indicator could ever be validated against them even once projections
  exist.
- Sentinel-2 snow-cover work is explicitly out of scope for this
  proposal; it needs separate approval and, even then, only validates
  snow presence/absence, not the annual snowfall depth C034 states.

## Status

draft (elevation bands + historical baseline built; climate access now
confirmed working; spatial + climate method proposed, not yet built)

## Changelog

- 2026-09-10: created.
- 2026-09-10: built elevation bands and recorded the historical
  snowfall baseline from S034; defined but did not evaluate the
  reliability indicator; confirmed a real (if incomplete) THREDDS access
  path for CanDCS-M6. Left as draft, not built, since the step's central
  question is still open.
- 2026-09-10: retried the dead THREDDS link and found the correct path
  (C064) -- the climate-access blocker is resolved. Verified real DEM
  access (step 03, C051) that this step's elevation-band work depends
  on. Proposed a spatial + climate method above, awaiting approval
  before any notebook changes. Flagged a new C035/C064 conflict and an
  unresolved lapse-rate judgment call as remaining before an actual
  projected-snowfall number can be produced.
