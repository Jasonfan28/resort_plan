# 03 Terrain and capacity

## Question

What does slope-by-ability-class from LiDAR say about the mountain's
terrain, what do the runs and lifts inventory show, and can the master
plan's stated existing CCC be reproduced from its own stated inputs?

## Decision

[left for the user]

## Alternatives considered

- Treat C008 ("resorts do not publish their CCC methodology") as a reason
  not to attempt reproduction at all. Rejected once S011 turned out to be
  reachable: RMR's own appendix does publish enough (per-lift slope
  length, vertical rise, hourly capacity, operating hours, access-role
  and misload percentages, and the resulting adjusted hourly capacity and
  CCC) to test reproduction directly, regardless of what C008's general
  claim about the industry says.

## Evidence

- [C007] agent-checked. S022 confirms CCC compares lift vertical
  transport capacity against guest demand for vertical.
- [C008] Could not check (WebFetch could not render the article body
  twice; may be paywalled). Neither confirmed nor contradicted, and
  turned out not to block this step regardless, since S011 publishes its
  own per-lift inputs.
- [C024] The appendix's stated formula: CCC = Vertical Rise x Hourly
  Capacity x Operating Hours x Loading Efficiency / Weighted Vertical
  Demand, with ability-class vertical demand from 1,000 m (Beginner) to
  10,000 m (Expert).
- [C025] The appendix's stated phase totals: 4,545 / 9,529 / 11,572 /
  18,167 skiers (Existing / Phase 2 / Phase 3 / Buildout).
- [C032] The master plan's own terrain breakdown: 1,263 ha, 7% beginner,
  45.5% intermediate, 47.5% advanced, 69 runs, 2 bowls.
- [C033] The master plan's own elevation table: 512 m (bottom) to 2,466 m
  (Mt. Mackenzie summit), 1,713 m lift-accessed vertical.

## Inputs

- S011 per-lift tables (Tables 1-1 to 1-4), transcribed into
  notebooks/03_terrain_and_capacity.ipynb via pdfplumber (evidence: C025).
- data/processed/02_ccc_by_phase.csv (the four stated phase totals,
  written by notebook 02 from the same claim, read here rather than
  retyped).

## Method

- (evidence) Reproduce each lift's CCC using C024's formula, with
  Loading Efficiency operationalized as (1 - Up-Mtn Access Role% -
  Misload Lift Stop%) applied to Hourly Capacity, since that combination
  exactly reproduces the appendix's own "Adjusted Hourly Capacity"
  column. Neither the (1 - access - misload) formula nor its role as
  "Loading Efficiency" is a sentence written in the appendix; this was
  found by testing arithmetic against the table's own columns, so it is
  this notebook's reverse-engineering, not a quoted method. It is
  checked against every one of the appendix's own 63 (phase, lift) rows
  and all 4 phase totals, not just a couple of examples.
- (judgment call) Do not attempt the slope-by-ability-class LiDAR
  analysis this step's Question also asks for. See Open issues: no DEM
  covering Mount Mackenzie/RMR is confirmed accessible yet, and getting
  one needs either a human with an OpenTopography API key or a human
  browsing LidarBC/HRDEM's JavaScript map tools directly.

## Outputs

- data/processed/03_lift_ccc_reproduction.csv (per-lift stated vs.
  computed CCC, all 63 phase/lift rows)
- data/processed/03_ccc_phase_reproduction_summary.csv (4 phase totals,
  stated vs. computed)

## Checks

- Every per-lift CCC and every phase total must reproduce within a small
  rounding tolerance (2 skiers).
- Last run: largest per-lift diff was 0.5 skiers, largest phase-total
  diff was 1 skier (Phase 2 and Phase 3 each came out 1 skier under the
  stated total; Phase 1 and Buildout matched exactly). All within
  tolerance: the master plan's stated CCC does reproduce from its own
  stated per-lift inputs.

## Open issues

- No independent LiDAR-derived slope analysis exists. C032 gives the
  resort's own stated ability-class terrain breakdown instead, which
  answers part of the step's Question but is self-reported by RMR, not
  independently computed. OpenTopography's API now requires a key (like
  OpenAlex) and returned HTTP 401 to an unauthenticated request; BC's
  LidarBC and NRCan's HRDEM (C017-C019, step 01) are both JavaScript map
  tools WebFetch cannot query by location. Someone needs to either get an
  OpenTopography API key, or open LidarBC/HRDEM in a browser and
  confirm/download a tile over Mount Mackenzie, to get an independent
  slope analysis rather than relying only on RMR's self-reported figures.
- The runs-and-lifts inventory (a plain list of named lifts/runs, as
  distinct from the CCC table) has not been separately compiled; the
  per-lift table here is organized by CCC calculation, not by trail
  network.
- C008 remains unchecked; if it can never be opened, note that
  explicitly rather than treating "could not check" as "confirmed."

## Status

built

## Changelog

- 2026-09-10: created.
- 2026-09-10: transcribed S011's per-lift tables via pdfplumber, built
  notebooks/03_terrain_and_capacity.ipynb, reproduced all 4 phase CCC
  totals within rounding tolerance. LiDAR/slope analysis left open
  pending DEM access.
