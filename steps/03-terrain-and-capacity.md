# 03 Terrain and capacity

## Question

What does slope-by-ability-class from LiDAR say about the mountain's
terrain, what do the runs and lifts inventory show, and can the master
plan's stated existing CCC be reproduced from its own stated inputs?

**Proposed addition (not yet built, awaiting approval):** now that a real
DEM and real lift/run geometry are both accessible (C051-C053, C063),
what does DEM-derived slope and aspect say about terrain by ability
class, how does DEM-derived lift vertical rise compare lift-by-lift
against the master plan's own figures, and what do OSM's runs show for
length, vertical drop, slope, and difficulty against a DEM-derived slope
class?

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
- [C051] (new, needs-review) HRDEM 1m mosaic DTM, read live via rasterio
  at all 14 OSM lift endpoints, gives Revelation Gondola's bottom as
  513.5 m and The Stoke's top as 2,223.5 m -- within a few tenths of a
  metre of C033's plan-stated 512 m base and close to its named peaks,
  a first cross-check between the DEM and the plan's own elevation
  claims.
- [C052] (new, needs-review) OSM has 7 aerialway lines and 116
  piste:type=downhill ways near RMR, all with piste:difficulty.
- [C053] (new, needs-review) OSM lift naming and segmentation differs
  from the master plan (e.g. "Little Bit" vs. "Lil' Bit"; the gondola is
  two OSM ways, not one).
- [C063] (new, needs-review) OSM's landuse=winter_sports polygon is the
  only candidate AOI boundary found; its area (1,248 ha) is within
  ~1.2% of C032's plan-stated 1,263 ha.

## Inputs

- S011 per-lift tables (Tables 1-1 to 1-4), transcribed into
  notebooks/03_terrain_and_capacity.ipynb via pdfplumber (evidence: C025).
- data/processed/02_ccc_by_phase.csv (the four stated phase totals,
  written by notebook 02 from the same claim, read here rather than
  retyped).
- **Proposed additions:**
  - S048 (HRDEM 1m mosaic, STAC, EPSG:3979 native) -- windowed reads only,
    clipped to the AOI's bounding box, never a full tile download.
  - S050 (OSM aerialway + piste ways near RMR, via Overpass), saved as
    data/raw/S050_overpass_lifts_pistes.json this session.
  - The AOI polygon from S050 (landuse=winter_sports way 475720359, C063).

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
- (judgment call, superseded by the proposed addition below if approved)
  Do not attempt the slope-by-ability-class LiDAR analysis this step's
  Question also asks for. The blocker that justified this (no accessible
  DEM) no longer holds: S048 is confirmed live and read successfully
  this session (C051).

### Proposed spatial method (not yet built)

- (evidence) **AOI**: use the OSM landuse=winter_sports polygon (C063),
  reprojected to EPSG:26911, since no dedicated ski-area or tenure
  boundary source was found. State this plainly in the notebook, not
  just here.
- (evidence) **DEM**: S048's HRDEM 1m mosaic DTM, read with windowed
  rasterio reads clipped to the AOI's bounding box (no full-tile
  download), computing slope (degrees or %) and aspect on the native
  EPSG:3979 grid, then reprojecting the clipped array to EPSG:26911 for
  area/distance work, checking that reprojected pixel size is ~1x1 m
  afterward.
- (to be resolved during build, not yet a source or a judgment call)
  **Ability-class slope thresholds**: check the master plan first. C032
  gives only area percentages (7/45.5/47.5%), not slope-degree criteria,
  so the master plan likely does not state thresholds directly. If no
  source states them, this becomes a labelled judgment call, sensitivity-
  tested across at least two published threshold sets (e.g. a
  commonly-cited ski-industry banding vs. a steeper/gentler alternative),
  reporting how much the resulting terrain split shifts between them --
  not a single silently-chosen threshold.
- (evidence) **Lift crosswalk**: drape OSM's 7 lift lines (C052) on the
  DEM for bottom elevation, top elevation, and vertical rise per lift
  (the exact method already proven in Phase 1's access test, C051).
  Write data/processed/03_lift_crosswalk.csv with columns for the OSM
  way id/name, the proposed master-plan map_ref match, a match_basis
  column (e.g. "name similarity", "position", "vertical rise
  similarity"), and an empty confirmed_by_jason column for sign-off.
  Compare DEM-derived vertical rise against S011's own vert_rise (in
  data/processed/03_lift_ccc_reproduction.csv) for each proposed match.
- (evidence) **Runs**: for each of OSM's 116 piste ways (C052), compute
  length, vertical drop, mean and max DEM slope, and compare the OSM
  piste:difficulty tag against the DEM slope class from the ability-
  class thresholds above.

## Outputs

- data/processed/03_lift_ccc_reproduction.csv (per-lift stated vs.
  computed CCC, all 63 phase/lift rows)
- data/processed/03_ccc_phase_reproduction_summary.csv (4 phase totals,
  stated vs. computed)
- **Proposed additions:**
  - data/processed/03_aoi.gpkg (AOI polygon, EPSG:26911)
  - data/processed/03_lift_crosswalk.csv (OSM-to-plan lift mapping,
    match_basis, confirmed_by_jason, DEM vs. plan vertical rise)
  - data/processed/03_runs.gpkg or .csv (per-run length, vertical drop,
    slope stats, OSM difficulty vs. DEM slope class)
  - data/processed/03_terrain_slope_aspect_summary.csv (area by
    ability-class slope band and aspect, compared against C032's
    7/45.5/47.5% split)

## Checks

- Every per-lift CCC and every phase total must reproduce within a small
  rounding tolerance (2 skiers).
- Last run: largest per-lift diff was 0.5 skiers, largest phase-total
  diff was 1 skier (Phase 2 and Phase 3 each came out 1 skier under the
  stated total; Phase 1 and Buildout matched exactly). All within
  tolerance: the master plan's stated CCC does reproduce from its own
  stated per-lift inputs.
- **Proposed additions:**
  - AOI area within a stated tolerance of C032's 1,263 ha (already
    ~1.2% off in the Phase 1 access test, C063; an independent-number
    validation check, not just an internal consistency check).
  - DEM-derived vertical rise within a stated tolerance of S011's
    vert_rise for every lift the crosswalk proposes as a confirmed
    match; report, do not hide, any match where they disagree
    substantially.
  - Terrain slope-class area split reported against C032's own split,
    with the threshold-sensitivity result shown, not just one number.
  - CRS check after every reprojection: report the CRS and confirm units
    are metres.

## Open issues

- **Resolved (2026-09-10):** the DEM-access blocker is gone. S048
  (NRCan HRDEM 1m, STAC, no key) reads live via rasterio; C051 already
  proves it against two of the master plan's own elevation figures. The
  spatial method above is proposed but not yet built, pending approval.
- No dedicated ski-area or tenure boundary source was found; the AOI
  uses OSM's landuse=winter_sports polygon instead (C063), which is a
  community-mapped boundary, not an official one.
- Ability-class slope-degree thresholds are not expected to be stated in
  the master plan (C032 gives area splits, not slope criteria); this
  will likely end up a labelled, sensitivity-tested judgment call rather
  than a sourced fact.
- The runs-and-lifts inventory (a plain list of named lifts/runs, as
  distinct from the CCC table) has not been separately compiled; the
  per-lift table here is organized by CCC calculation, not by trail
  network. The proposed spatial addition covers this from OSM instead.
- C008 remains unchecked; if it can never be opened, note that
  explicitly rather than treating "could not check" as "confirmed."
- OSM's own lift/run naming and segmentation differs from the master
  plan (C053); the proposed lift crosswalk's match_basis and
  confirmed_by_jason columns exist specifically to make that mapping
  auditable rather than asserted.

## Status

built (CCC reproduction); spatial terrain analysis proposed, not built

## Changelog

- 2026-09-10: created.
- 2026-09-10: transcribed S011's per-lift tables via pdfplumber, built
  notebooks/03_terrain_and_capacity.ipynb, reproduced all 4 phase CCC
  totals within rounding tolerance. LiDAR/slope analysis left open
  pending DEM access.
- 2026-09-10: verified real DEM (S048/C051) and OSM lift/run/AOI access
  (S050/C052/C053/C063) in a Phase 1 access test; proposed a spatial
  terrain method above, awaiting approval before any notebook changes.
