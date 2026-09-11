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
  formula is not itself backed by a claim.

### Spatial + climate method

- (evidence) **Elevation-band area and run length**: using step 03's AOI
  and DEM (via the shared src/resort/dem.py module), computed real area
  per elevation band x aspect class, and run length by elevation band
  from step 03's 116 OSM runs. Aspect binning (4-way vs. 8-way compass
  bins) is a judgment call, sensitivity-tested by reporting both -- they
  agree closely (see Outputs), so the binning choice does not change the
  picture here.
- (evidence) **Climate, now that access works (C064)**: pulled 30-year-
  mean annual total snowfall (sntot, the indices/ensemble-percentiles
  product) for ssp245 and ssp585, at a 1991-2020 baseline and a
  2041-2070 mid-century period, via OPeNDAP subsetting (no full-file
  download) from S015's corrected path. Did **not** resolve the
  C035/C064 conflict over whether the base archive's raw prsn variable
  should also be used -- sntot was built on its own since it is the
  product this step's evidence already pointed to and does not depend
  on that conflict's answer. Left open (see Open issues).
- (evidence) **Grid-cell-vs-terrain elevation gap**: overlaid the
  climate grid cell nearest the AOI centroid (derived from step 03's
  AOI, C063 -- not a separately hardcoded coordinate) on the DEM and
  reported the gap between the grid cell's own terrain elevation range
  and the AOI's own (see Outputs). No lapse-rate adjustment was
  attempted, per this step's scope -- a lapse rate remains an
  unresolved judgment call (see Open issues).
- (judgment call, sensitivity-tested) **Snow-to-water density**: sntot
  is in mm of snow water equivalent; C034's historical baseline is in
  metres of snow depth. No source ties a specific snow-to-water ratio to
  Revelstoke, so the reliability ratio was computed across three
  plausible ratios (8, 10, 13 cm snow per 10 mm SWE) and both historical
  bounds, for both the baseline and mid-century periods -- not a single
  picked value. Running the same ratios against the baseline period
  (which has no climate-change trend) doubles as a sanity check on the
  whole conversion approach; see Checks for the result.
- (not built) **Sentinel-2 snow presence**: out of scope for this step;
  would need separate approval, and even then only validates snow
  presence/absence on a date, not annual snowfall depth.

## Outputs

- data/processed/04_elevation_bands.csv
- data/processed/04_historical_snowfall.json
- data/processed/04_elevation_aspect_bands.csv (area by elevation band x
  aspect, 4-way and 8-way). Last run: base-to-lift-top band totals
  1,230.94 ha (4-way) / 1,230.95 ha (8-way); lift-top-to-sub-peak 16.88 /
  16.87 ha; sub-peak-to-summit 0.44 / 0.43 ha -- the two aspect schemes
  agree to within rounding.
- data/processed/04_run_length_by_band.csv. Last run: 115.1 km in the
  base-to-lift-top band, 1.63 km in lift-top-to-sub-peak, 0 km in
  sub-peak-to-summit (no run's sampled elevation falls that high).
- data/processed/04_snow_projection.csv (sntot p10/p50/p90, mm SWE, by
  SSP x horizon). Last run, p50: ssp245 592.3 mm (1991-2020) -> 534.8 mm
  (2041-2070); ssp585 589.3 mm (1991-2020) -> 494.9 mm (2041-2070).
- data/processed/04_climate_grid_overlay.json (grid cell vs. AOI terrain
  elevation range). Last run: grid cell DEM range 436.9-2,455.4 m vs.
  AOI DEM range 473.9-2,354.7 m -- the grid cell's footprint spans wider
  than the AOI on both ends, consistent with a ~9x6 km cell sitting over
  terrain well beyond the resort's own boundary.
- data/processed/04_reliability_sensitivity.csv (reliability ratio by
  SSP x horizon x snow-to-water ratio x historical bound). See Checks
  for the baseline sanity-check result.

## Checks

- Band boundaries strictly increasing; base band's vertical equals the
  plan's stated lift-accessed vertical; historical range's low bound
  under its high bound.
- Elevation-aspect band areas sum to the AOI's total area (1,248.26 ha),
  for both aspect schemes -- an independent-number check against step
  03's own AOI area, not just internal consistency.
- Run-length-by-band total equals the sum of every run's own geometry
  length exactly.
- Grid-cell-vs-terrain elevation gap reported as a number (above), no
  lapse-rate adjustment applied.
- **Baseline sanity check against C034**: running the same snow-to-water
  ratios against the 1991-2020 baseline (no climate-change trend
  involved) gives a reliability ratio of 0.34-0.86 across both SSPs and
  all three ratios -- never reaching 1.0 even at the most generous
  tested ratio. The mid-century ratio (0.28-0.77) is not meaningfully
  different in shape. This means the gap between C034 and the climate
  data is dominated by the unit-conversion/data mismatch, not by a
  detectable mid-century decline this method can isolate. Reported
  plainly rather than left implicit; see Open issues.
- Last run: all checks passed.

## Open issues

- **Still open:** the C035/C064 conflict over which snowfall variable
  (indices product's sntot vs. base archive's raw prsn) is authoritative
  was not resolved -- this build used sntot on its own since it is the
  product already backed by this step's evidence, but a future revisit
  should settle whether prsn changes the picture.
- **Still open:** no lapse rate was applied to adjust grid-cell snowfall
  to actual terrain elevation; this step only reports the elevation gap
  (above), by design. A lapse-rate adjustment, if attempted, needs its
  own source or sensitivity-tested judgment call.
- **New finding:** the baseline sanity check (see Checks) shows the
  climate data does not reproduce C034 even at the baseline period and
  the most generous tested snow-to-water ratio (reliability ratio tops
  out at 0.86, never reaching 1.0). This means the reliability indicator
  as currently built cannot distinguish "RMR will get less snow" from
  "the units/data don't line up the way this method assumes" -- it
  should be read as a data-comparison exercise, not a validated forecast,
  until that gap is explained (a likely candidate not yet checked: sntot
  may already be an anomaly/delta relative to some reference period
  rather than an absolute total, which would explain a low but non-zero
  ratio; not confirmed against S015's own documentation this session).
- A 10 km grid (C006) is coarse relative to a single resort's elevation
  bands; the grid-cell-vs-terrain elevation gap check makes how coarse
  it is visible as a number (436.9-2,455.4 m vs. AOI's 473.9-2,354.7 m).
- The historical snowfall figures (C034) give no year range or
  measurement method, which limits how precisely a reliability
  indicator could ever be validated against them.
- Sentinel-2 snow-cover work remains out of scope; it needs separate
  approval and, even then, only validates snow presence/absence, not
  the annual snowfall depth C034 states.
- Only the 116 currently-mapped OSM runs are covered for run-length-by-
  band; planned-but-unbuilt runs from later master-plan phases have no
  OSM geometry.

## Status

built

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
- 2026-09-11: built the spatial + climate addition. Real elevation-band
  x aspect area and run length from step 03's AOI/DEM/runs; real sntot
  projections for ssp245/ssp585 at baseline and mid-century via OPeNDAP;
  grid-cell-vs-terrain elevation gap reported; snow-to-water reliability
  ratio computed as a three-way sensitivity table against both
  historical bounds, at both horizons. notebook-reviewer (fresh
  subagent) found three real issues, all fixed: a duplicated
  "parameters" tag that silently broke `--scenario`/`-p` overrides for
  every new-section output, a hardcoded climate-grid coordinate now
  derived from step 03's own cited AOI centroid instead, and a missing
  sanity check comparing the baseline climate period against C034 --
  adding it surfaced the finding above (baseline ratio never reaches
  1.0). Did not resolve the C035/C064 variable conflict; recorded as
  still open rather than silently picked. No lapse-rate adjustment
  attempted, per this step's scope.
