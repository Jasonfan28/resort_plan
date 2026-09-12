# 07 Land capacity

## Question

Under current zoning, how many units can vacant and underused parcels
hold, including City priority sites and resort base lands?

## Decision

[left for the user]

## Alternatives considered

- Estimate unit capacity by assuming a typical density per zone type
  (e.g. "apartment zones average N units/ha"). Rejected: no source for
  Revelstoke's actual bylaw density provisions was found this session,
  and a typical/assumed figure would be exactly the kind of unsourced
  number CLAUDE.md rule 6 rules out.

## Evidence

- [C015]/[C038]/[C046] agent-checked/needs-review. Oscar Lands Master
  Plan approved Feb 2024 (S012); the OCP Resort Lands DPA is a
  separate, RMR-specific development permit area (S047).
- [C045] The City's ArcGIS Hub publishes a live, queryable Zoning
  FeatureServer.
- [C047] The City's ArcGIS Hub also publishes a live PMBC Parcel Fabric
  view (parcel geometry and legal descriptions, no zoning attributes).
- [C049] Live zoning-by-parcel-count query: 39 zone codes; R-LD1
  (single-family-style) dominates, with several multi-unit and mixed-
  use zones also present.
- [C050] The OCP Resort Lands DPA is a single ~811 ha polygon.
- [C054] (new, needs-review) The City's ArcGIS Hub lists exactly 54
  datasets total, including OCP Floodplain, OCP Environmentally
  Hazardous DPA, OCP Agricultural Land Reserve (ALR), and others, each
  with its own live FeatureServer and blank licence.
- [C056]-[C062] (new, needs-review) Buildings, OCP Floodplain, OCP
  Environmentally Hazardous DPA, OCP Agricultural Land Reserve (ALR),
  Water Mains, Sanitary Mains, and Centreline each confirmed as their
  own live FeatureServer.
- [C065] (new, needs-review) ParcelMap BC (S030) is queryable as a live,
  bbox-filterable WFS, EPSG:3005 (NAD83 / BC Albers), with real parcel
  attributes (PID, PARCEL_CLASS, FEATURE_AREA_SQM, MUNICIPALITY). This is
  the geometry the user has directed be used for the public website
  (docs/), since the City's own layers carry no stated licence.
- [C071] (new, needs-review) ParcelMap BC's MUNICIPALITY attribute
  returns 5,989 parcels for 'Revelstoke, City of'; 2 are ~90 km south
  near Nakusp and excluded from the funnel's working set.
- [C072] (new, needs-review) The Revelation Gondola's lower terminus
  (OSM way 1361895818) has its base station at 50.9583206N/118.1631845W,
  identified by matching step 03's DEM-sampled bottom elevation (513.5m).
- [C073] (new, needs-review) The OCP Environmentally Hazardous DPA
  FeatureServer is 110,545 individual ~1 sq m polygons city-wide, not
  hand-drawn hazard zones -- consistent with a rasterized slope layer.
- [C074] (new, needs-review) A third-party ski-resort directory states
  the Trans Canada Highway exit to the Revelation gondola's lift
  entrance is "8 km ... approx. 14 Minutes driving time" -- used as an
  independent spot check on this step's own network-distance figures.

## Inputs

- research/claims.csv (C049, C050, C054, C056-C062, C065) — all queried
  live this session via REST/WFS APIs, not just described from a
  landing page.
- research/inbox/ checked and confirmed empty: no zoning bylaw density
  extraction exists, so unit capacity stays unanswered per the user's
  own instruction, not silently estimated.

## Method

- (evidence) Classify each zone code as multi-unit-eligible or not,
  strictly from what its own name states (rowhouse/apartment/
  condominium/downtown/corridor/live-work vs. single-family-style
  ground-oriented or rural zones). This is a factual read of the zone
  name, not a density estimate.
- (judgment call, incomplete) Does not convert parcel counts or the
  Resort Lands DPA's area into a unit-capacity number, and does not
  identify which specific parcels are vacant or underused. Both need
  data this session did not find: the zoning bylaw's density
  provisions, and a vacancy/improvement-value indicator (e.g. from BC
  Assessment) joined to the parcel fabric.

### Parcel suitability funnel

- (evidence) **Base geometry**: ParcelMap BC (S030/C065) parcels filtered
  by ParcelMap BC's own MUNICIPALITY attribute (not a separately-sourced
  boundary polygon), reprojected to EPSG:26911. 5,989 parcels returned;
  2 (C071, Crown Agency "Subdivision" parcels ~90 km south near Nakusp)
  sit far outside the zoned area and are excluded from the working set
  as not part of the built-up area a housing funnel is meant to cover.
  City layers (Zoning, Floodplain, Hazardous DPA, ALR, Buildings, mains,
  Centreline) join to these parcels by spatial overlay, used for
  analysis only -- never as the geometry that ends up in docs/ (see
  step 10 and the rule not to publish City geometry before its licence
  is confirmed).
- (evidence) **Filter 1, zoning**: each parcel's representative point
  (guaranteed inside the parcel, unlike a centroid) is spatially joined
  to the live Zoning FeatureServer; the existing
  MULTI_UNIT_ELIGIBLE_PREFIXES classification is applied to the
  resulting zone code. 10 parcels' representative points fall inside
  two overlapping zoning polygons (a real quirk in the Zoning layer's
  own geometry, kept the first match and reported, not hidden); 138
  parcels have no zoning polygon at their representative point at all
  and are correctly excluded as non-eligible rather than silently
  dropped from the count.
- (evidence) **Filters 2-4, constraints**: exclude parcels intersecting
  OCP Floodplain (S053/C057), OCP Environmentally Hazardous DPA
  (S054/C058), or OCP Agricultural Land Reserve (S055/C059). The
  Hazardous DPA layer turned out to be 110,545 individual ~1 sq m
  raster-derived polygons city-wide (C073), not hand-drawn zones;
  dissolved into one geometry before the intersection test.
- (judgment call, sensitivity-tested) **Filter 5, service distance**:
  parcels within a stated distance of both Water Mains (S056/C060) and
  Sanitary Mains (S057/C061). No source states what distance counts as
  "serviced"; tested at 50 m / 100 m / 200 m, with 100 m carried forward
  as the primary scenario.
- (judgment call, sensitivity-tested) **Filter 6, underuse**: building
  coverage (Buildings/S052 footprint area, clipped to its actual overlap
  with each parcel via a geometric intersection -- not the whole
  building's area, which would over-credit a building straddling two
  parcels -- over parcel area) under a stated cutoff. No source states
  this cutoff either; tested at 10% / 20% / 30%, with 20% carried
  forward.
- (judgment call, sensitivity-tested) **Filter 7, DEM slope**: parcels
  under a stated mean-slope cutoff, from step 03's DEM (via the shared
  src/resort/dem.py module), clipped only to the parcels still in play
  after Filters 1-6. Tested at 15% / 20% / 25% / 30%, with 20% carried
  forward.
- (evidence, explicit gap) **Unit capacity**: research/inbox/ is
  confirmed empty of any zoning bylaw density extraction (checked again
  this session). Unit capacity is not present in any output file, with
  a note saying so, rather than estimated from an assumed density.
- (evidence) **Network distance**: for parcels surviving the full
  funnel, distance via a graph built from Centreline (S058/C062) to the
  gondola base station and to a downtown reference point (the Zoning
  layer's own "MU-1 - Downtown Zone" parcels' centroid). The gondola
  base station's location is not a hand-typed coordinate: it is
  identified (C072) by cross-referencing OSM way geometry (S050)
  against step 03's own DEM-sampled bottom elevation for that lift. The
  Centreline network is genuinely fragmented (87 connected components);
  routing is restricted to the largest component (a documented judgment
  call), and each reference point's snap distance to reach it is
  reported explicitly rather than absorbed silently into the result
  (see Checks). Built with networkx (approved earlier); no new package
  was needed for nearest-node lookup (a scipy KD-tree was tried and
  dropped since scipy is not in this project's environment -- a plain
  numpy nearest-neighbour search over ~4,900 nodes is fast enough).

## Outputs

- data/processed/07_zoning_by_parcel_count.csv
- data/processed/07_resort_lands_dpa.json
- data/processed/07_parcel_funnel.csv (filter name, parcel count, and
  area remaining, at every stage). Last run:
  0. all City of Revelstoke parcels (ParcelMap BC): 5,987 / 4,804.39 ha
  1. zoned multi-unit eligible: 802 / 147.06 ha
  2. outside floodplain: 769 / 139.37 ha
  3. outside hazardous DPA: 700 / 104.91 ha
  4. outside ALR: 700 / 104.91 ha
  5. within 100 m of water + sanitary mains: 697 / 103.71 ha
  6. building coverage under 20%: 150 / 7.79 ha
  7. mean DEM slope under 20%: 150 / 7.79 ha
- data/processed/07_funnel_sensitivity.csv (all tested values for the 3
  judgment-call filters). Last run: service distance 50/100/200 m gives
  693/697/698 parcels (103.62/103.71/104.11 ha) -- barely sensitive at
  all, since most zoning-eligible parcels near the constraint-passing
  area are already close to mains; building coverage 10/20/30% gives
  105/150/207 parcels (3.98/7.79/11.19 ha) -- the filter that actually
  drives the funnel's final size; slope 15/20/25/30% gives
  149/150/150/150 parcels (7.77/7.79/7.79/7.79 ha) -- barely binding at
  all in this range, a real finding, not a flat result left unchecked.
- data/processed/07_network_distances.csv (150 rows, one per Filter-7
  survivor). Distances include both ends' own snap-to-network gap, not
  just the on-network path (see Checks).
- Unit capacity: explicitly absent from every output file, with a note
  in the notebook and this step file saying why, rather than a blank
  column that could be mistaken for zero.

## Checks

- Every zone code classified into exactly one multi-unit-eligible
  group; the classified total matches the raw table's own parcel-count
  sum.
- Funnel parcel count and area are non-increasing at every stage.
- The funnel's starting count (5,987) matches a fresh, independent
  re-query of ParcelMap BC's own count for the municipality, run at
  Checks time, not reused from the earlier fetch.
- Every per-parcel network distance is at least as long as the
  straight-line distance to the same reference point (a real geometric
  invariant, not just internal consistency).
- The downtown-to-gondola-base network distance is spot-checked against
  an independently-sourced figure, not just checked for internal
  consistency: C074 states a similar (not identical) route is "~8 km,
  14 minutes"; this step's own figure came out to 7,008 m -- a close
  order-of-magnitude match given the two routes start/end at different
  points (highway exit vs. MU-1 centroid; lift entrance vs. gondola base
  station).
- CRS check after every reprojection: DEM confirmed EPSG:26911 with
  ~1x1 m pixels; the gondola-endpoint reprojection (EPSG:4326 to
  EPSG:26911) checked for plausible UTM-11N-range coordinates, not just
  that the transform ran without error.
- Last run: all checks passed.

## Open issues

- **Needed for step 10, not made here:** this notebook only exports a
  per-parcel table for parcels that survive the *entire* filter chain
  (data/processed/07_network_distances.csv, 150 PIDs). Step 10's web
  map wanted a stage-reached attribute for every candidate parcel (not
  just full survivors), which this notebook doesn't produce; a future
  revisit could export an intermediate per-parcel table (e.g. PID plus
  which stage, if any, it failed at) for that purpose.
- This step still does not answer its own central question ("how many
  units can vacant and underused parcels hold"). It answers a narrower,
  real question instead: 150 parcels (7.79 ha) pass every filter tested
  (zoning eligibility, floodplain/hazard/ALR exclusion, service
  distance, building coverage, slope), but no unit count is attached to
  them. Turning that into a unit-capacity number needs two things not
  found this session:
  1. The zoning bylaw's actual density/FAR/minimum-lot-size provisions
     per zone (a legal document, not yet located).
  2. A vacancy or "underused" indicator per parcel beyond building
     coverage (e.g. BC Assessment's improvement-to-land value ratio).
     BC Assessment's own licence page (C021) does not itself link to
     this product.
- The Centreline road network is genuinely fragmented (87 connected
  components out of 4,860 nodes); this step routes only within the
  largest (3,277 nodes) and reports each reference point's snap
  distance rather than silently absorbing it. The gondola base
  station's 1,249 m snap distance is itself a finding worth carrying
  forward: the resort base area has little or no Centreline coverage in
  the City's own road-network dataset, separate from any question about
  this step's methodology.
- The building-coverage filter is the one actually doing most of the
  funnel's work (802 to 150 parcels); the slope filter barely binds at
  all in the tested range (149-150 parcels across 15-30%), which may
  mean the multi-unit-eligible, constraint-clear, serviced parcel stock
  in Revelstoke is simply not on steep ground, rather than that slope is
  an uninformative filter choice in general.
- Both City FeatureServers' licence fields are literally "none"
  (unspecified), not a stated open licence like ParcelMap BC's (S030);
  worth flagging before any public-facing reuse of the City's own
  copies.
- The Oscar Lands Master Plan (C015/C038) has not been read as a
  document (only its City-webpage description); whether it states its
  own unit-capacity figures directly has not been checked.
- 10 parcels have an ambiguous zoning match (representative point inside
  2 overlapping zoning polygons) and 138 have no zoning match at all;
  both are reported by the notebook but not individually investigated.

## Status

built

## Changelog

- 2026-09-10: created.
- 2026-09-10: found live, queryable City FeatureServers for zoning and
  parcels (resolving step 01's C023 open question); built
  notebooks/07_land_capacity.ipynb and ran clean via `/run 07`. Left the
  step's core unit-capacity question open pending bylaw density data
  and a vacancy indicator.
- 2026-09-10: confirmed 7 more live City layers (Buildings, Floodplain,
  Hazardous DPA, ALR, Water Mains, Sanitary Mains, Centreline) and
  ParcelMap BC's own live WFS (C065), and confirmed research/inbox/ is
  still empty of any bylaw density extraction. Proposed a parcel
  suitability funnel above (zoning, floodplain, hazardous DPA, ALR,
  service distance, building coverage, slope, then network distance),
  with three judgment-call parameters explicitly marked for sensitivity
  testing rather than a single silent choice. Awaiting approval before
  any notebook changes.
- 2026-09-12: built the spatial parcel-suitability funnel. Real
  ParcelMap BC parcels (5,987 after excluding 2 outlier parcels, C071),
  a live zoning join (reporting 10 ambiguous and 138 unmatched parcels
  rather than hiding them), floodplain/hazardous-DPA/ALR exclusion (the
  DPA layer turned out to be ~110K raster-derived cells, C073), and
  three sensitivity-tested judgment-call filters (service distance,
  building coverage, slope), reaching 150 surviving parcels (7.79 ha).
  Added src/resort/arcgis.py (shared FeatureServer/WFS fetch helpers,
  reused by step 10). Built a network-distance analysis from a real but
  fragmented Centreline graph (87 components), routing only within the
  largest and reporting both reference points' snap distances rather
  than hiding the gap -- the gondola base station's 1,249 m snap
  distance is itself a finding. notebook-reviewer (fresh subagent)
  found and I fixed five real issues: two hand-typed computed figures in
  markdown, a missing independent (not just internally-consistent)
  spot-check on the network distances (added C074/S064, an independent
  ~8 km/14 min figure, and the computed 7,008 m came out a close match),
  a building-coverage calculation that over-credited whole-building area
  to any intersecting parcel instead of the actual overlap area (fixing
  it changed the final funnel from 96 to 150 parcels -- a real,
  substantive correction, not a cosmetic one), and a missing CRS check
  on a second reprojection. Unit capacity remains explicitly absent, as
  scoped.
