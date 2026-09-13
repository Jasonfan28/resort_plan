# 03 Terrain and capacity

## Question

What does slope-by-ability-class from LiDAR say about the mountain's
terrain, what do the runs and lifts inventory show, and can the master
plan's stated existing CCC be reproduced from its own stated inputs?

**Answered below** using a real DEM and real lift/run geometry
(C051-C053, C063): DEM-derived slope and aspect by ability class,
lift-by-lift vertical rise against the master plan's own figures, and
OSM's runs by length, vertical drop, slope, and difficulty against a
DEM-derived slope class.

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
- S048 (HRDEM 1m mosaic, STAC, EPSG:3979 native) -- windowed reads only,
  clipped to the AOI's bounding box, never a full tile download.
- S050 (OSM aerialway + piste ways near RMR, via Overpass), saved as
  data/raw/S050_overpass_lifts_pistes.json this session.
- The AOI polygon from S050 (landuse=winter_sports way 475720359, C063),
  saved as data/raw/S050_overpass_aoi.json.

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
### Spatial method

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
- (judgment call, resolved) **Ability-class slope thresholds**:
  research-scout confirmed no source states numeric downhill-ski
  thresholds (checked both master plan PDFs directly -- no "gradient"
  or "degree" hits; checked NSAA, OSM's own piste:difficulty wiki, and
  ski-planning references). C066-C070 record what was actually found:
  NSAA says ratings are resort-relative with no number at all (C066);
  OSM's piste:difficulty wiki has a numeric scale only for a different
  tag value, ski_touring, via the Swiss Alpine Club scale (C067);
  Colorado's Ski Safety Act legally defines "extreme terrain" at 50 deg
  average pitch, a narrow, US-specific category (C068); a weak consumer
  source repeats an uncredited folk banding (C069); the master plan
  itself states one zone's average grade (South Bowl, 35-55%) but not a
  general table (C070). Sensitivity-test both real candidate bands
  found: C067's SAC scale (Novice <30 deg / Easy 30-35 / Intermediate
  35-40 / Advanced 40-45 / Expert >45, steeper, meant for ski touring
  not groomed terrain) against C069's folk banding (green <25% / blue
  25-40% / black >40%, i.e. roughly <14 deg / 14-22 deg / >22 deg,
  gentler, weakly sourced). Report both splits side by side, label each
  with its real provenance, and do not present either as "the" correct
  threshold.
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
- data/processed/03_aoi.gpkg (AOI polygon, EPSG:26911)
- data/processed/03_lift_crosswalk.csv (OSM-to-plan lift mapping,
  match_basis, confirmed_by_jason, DEM vs. plan vertical rise)
- data/processed/03_runs.gpkg (116 runs: length, vertical drop, mean/max
  DEM slope, OSM difficulty tag)
- data/processed/03_terrain_slope_aspect_summary.csv (AOI area by slope
  class x 4-way aspect, for both threshold sets)

## Checks

- Every per-lift CCC and every phase total must reproduce within a small
  rounding tolerance (2 skiers).
- Last run: largest per-lift diff was 0.5 skiers, largest phase-total
  diff was 1 skier (Phase 2 and Phase 3 each came out 1 skier under the
  stated total; Phase 1 and Buildout matched exactly). All within
  tolerance: the master plan's stated CCC does reproduce from its own
  stated per-lift inputs.
- AOI area within a stated tolerance (5%) of C032's 1,263 ha.
  Last run: 1,248.3 ha, 1.2% off -- an independent-number validation
  check, not just an internal consistency check.
- DEM-derived vertical rise within 5 m for every lift the crosswalk
  proposes as its closest match; report, do not hide, any disagreement
  between the vertical-rise match and a separate name-similarity signal.
  Last run: all 7 lifts matched within 5 m (largest delta 2.5 m); one
  lift (OSM "Little Bit") shows a genuine disagreement, reported not
  hidden -- vertical rise alone points to map_ref "24" (delta 0.9 m),
  while name similarity (difflib, ratio 0.78) points to "Lil' Bit"
  instead. Left for confirmed_by_jason, not resolved by the notebook.
- Terrain slope-class area split reported against C032's own split, with
  both threshold-sensitivity results shown, not just one number. Last
  run: the two threshold sets disagree substantially (as expected, since
  neither is sourced for groomed downhill terrain) -- C067's steeper SAC
  scale puts 74.4% of AOI area under its gentlest class, while C069's
  gentler folk banding puts only 22.9% under its gentlest class. This
  gap is itself the finding: no defensible single number exists without
  a real source for downhill-specific thresholds.
- Aspect (computed alongside slope but originally left unused --
  caught by a Phase-3 review) is cross-tabulated with slope class, not
  just computed and discarded. Last run: south-facing terrain clearly
  dominates the gentlest SAC class (40.1 of 74.4 percentage points), a
  real finding about this AOI's orientation, not just a completeness
  formality.
- CRS check after every reprojection: confirmed EPSG:26911 and ~1x1 m
  pixels after reprojecting the DEM from its native EPSG:3979.
- Every run must have a real (non-NaN) slope/drop statistic. A first
  version clipped the DEM to the AOI plus a fixed buffer and silently
  produced NaN stats for 9 of 116 runs (mostly unnamed freeride ways
  extending past the AOI polygon); fixed by clipping to the union of the
  AOI, lift, and run bounds instead of the AOI alone, caught by
  notebook-reviewer, not by an automated check -- worth adding an
  explicit no-NaN assert if this step is revisited.

## Open issues

- No dedicated ski-area or tenure boundary source was found; the AOI
  uses OSM's landuse=winter_sports polygon instead (C063), which is a
  community-mapped boundary, not an official one. It validates well
  against C032 (1.2%), which is reassuring but not proof it is the
  resort's actual legal tenure boundary.
- No source states downhill-ski slope thresholds. The two threshold
  sets tested (C067, C069) are the best real candidates found, but
  neither is authoritative for groomed downhill terrain, and they
  disagree substantially (see Checks). This step's terrain-by-ability-
  class output should be read as "here is the range depending on which
  unsourced convention you pick," not as a single confident split.
- The lift crosswalk proposes matches for all 7 currently-built OSM
  lifts, but the master plan's per-lift table has 27 distinct map_refs
  across all phases (most numbered lifts do not exist yet). One match
  (OSM "Little Bit") has two disagreeing signals and needs a human
  decision (confirmed_by_jason); the other 6 are unreviewed proposals,
  not confirmed identities, even though their deltas are small.
- C008 remains unchecked; if it can never be opened, note that
  explicitly rather than treating "could not check" as "confirmed."
- Only the 116 currently-mapped OSM runs and 7 currently-built OSM lifts
  are covered. Planned-but-unbuilt lifts/runs from later master-plan
  phases have no OSM geometry and are not part of this spatial analysis.

## Status

built

## Changelog

- 2026-09-10: created.
- 2026-09-10: transcribed S011's per-lift tables via pdfplumber, built
  notebooks/03_terrain_and_capacity.ipynb, reproduced all 4 phase CCC
  totals within rounding tolerance. LiDAR/slope analysis left open
  pending DEM access.
- 2026-09-10: verified DEM/OSM access in a Phase 1 test; proposed a
  spatial method.
- 2026-09-11: built the spatial addition. Real AOI (1,248 ha, 1.2% off
  C032), DEM slope/aspect via windowed HRDEM reads (no full-tile
  download), a 7-lift crosswalk against the plan's per-lift table (one
  genuine match ambiguity surfaced, not hidden), and per-run stats for
  all 116 OSM runs. Ability-class thresholds resolved as an explicit,
  sensitivity-tested judgment call (research-scout found no sourced
  threshold; C066-C070). notebook-reviewer (fresh subagent) found four
  real issues, all fixed: a hand-typed C032 percentage in markdown, a
  Checks cell that printed but didn't assert the lift-vertical-rise
  tolerance, missing tunable thresholds in the parameters cell, and 9
  runs silently getting NaN stats from a too-narrow DEM clip (fixed by
  clipping to the union of AOI/lift/run bounds instead of the AOI
  alone).
- 2026-09-10: verified real DEM (S048/C051) and OSM lift/run/AOI access
  (S050/C052/C053/C063) in a Phase 1 access test; proposed a spatial
  terrain method above, awaiting approval before any notebook changes.
- 2026-09-12 (Phase 3 review): a fresh, independent notebook-reviewer
  pass found four real issues in the committed notebook: (1) a second
  cell tagged "parameters" that silently defeated `--scenario`/`-p`
  pipeline overrides for the whole spatial section (same class of bug
  already fixed once in steps 04/07/10 by then, reintroduced here
  because 03 was built first) -- fixed by merging into the one real
  parameters cell; (2) `name_similarity_threshold` was defined but never
  wired into the actual name-comparison code, which hardcoded 0.5
  instead -- fixed; (3) aspect was computed but never used anywhere,
  and 03_terrain_slope_aspect_summary.csv contained no aspect data
  despite its own filename -- fixed by cross-tabulating slope class
  with 4-way aspect, which surfaced a real finding (south-facing terrain
  dominates the gentlest class); (4) the notebook's own intro markdown
  still said it "does not attempt" the spatial analysis, contradicted by
  the 30+ cells directly below it that do -- fixed. Also exposed
  `run_sample_points` (previously a hardcoded n=20 inside a function
  default) as a labelled parameter, though it was not further
  sensitivity-tested this session.
