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

### Proposed parcel suitability funnel (not yet built)

- (evidence) **Base geometry**: ParcelMap BC (S030/C065) parcels within
  the AOI's municipal extent, reprojected to EPSG:26911. City layers
  (Zoning, Floodplain, Hazardous DPA, ALR, Buildings, mains, Centreline)
  join to these parcels by spatial overlay or PID, used for analysis
  only -- never as the geometry that ends up in docs/ (see step 10 and
  the explicit rule not to publish City geometry before its licence is
  confirmed).
- (evidence) **Filter 1, zoning**: reuse the existing
  MULTI_UNIT_ELIGIBLE_PREFIXES classification (already built) against
  parcels' zone code from S045.
- (evidence) **Filter 2-4, constraints**: exclude parcels intersecting
  OCP Floodplain (S053/C057), OCP Environmentally Hazardous DPA
  (S054/C058), or OCP Agricultural Land Reserve (S055/C059).
- (judgment call, to be sensitivity-tested) **Filter 5, service
  distance**: parcels within a stated distance of Water Mains
  (S056/C060) and Sanitary Mains (S057/C061). No source states what
  distance counts as "serviced"; propose testing at least three values
  (e.g. 50 m / 100 m / 200 m) and reporting how the funnel's surviving
  count and area change at each, not picking one silently.
- (judgment call, to be sensitivity-tested) **Filter 6, underuse**:
  building coverage (Buildings/S052 footprint area over parcel area)
  under a stated cutoff. No source states this cutoff either; propose
  at least three values (e.g. 10% / 20% / 30%) with the same
  sensitivity reporting.
- (judgment call, to be sensitivity-tested) **Filter 7, DEM slope**:
  parcels under a stated mean-slope cutoff, from step 03's DEM. Same
  treatment: at least two or three plausible cutoffs, reported side by
  side.
- (evidence, explicit gap) **Unit capacity**: research/inbox/ is
  confirmed empty of any zoning bylaw density extraction. Unit capacity
  is left empty in the output, with a note saying so, rather than
  estimated from an assumed density.
- (evidence) **Network distance**: for parcels surviving the full
  funnel, distance via Centreline (S058/C062) to the gondola base
  (step 03's lift crosswalk, once built) and to a downtown reference
  point (the Zoning layer's own "MU-1 - Downtown Zone" parcels'
  centroid, an evidence-based reference rather than a guessed landmark).
  This needs a routable graph; see the package list below.

## Outputs

- data/processed/07_zoning_by_parcel_count.csv
- data/processed/07_resort_lands_dpa.json
- **Proposed additions:**
  - data/processed/07_parcel_funnel.csv (filter name, parcel count, and
    area remaining, at every stage -- never only the final number)
  - data/processed/07_funnel_sensitivity.csv (service-distance,
    building-coverage-cutoff, and slope-cutoff variants, each showing
    how the surviving count/area shifts)
  - data/processed/07_network_distances.csv (funnel-surviving parcels'
    distance to the gondola base and to the downtown reference point)
  - Unit capacity: explicitly absent from every output file, with a
    note in the notebook and this step file saying why, rather than a
    blank column that could be mistaken for zero.

## Checks

- Every zone code classified into exactly one multi-unit-eligible
  group; the classified total matches the raw table's own parcel-count
  sum.
- Last run: all checks passed.
- **Proposed additions:**
  - Funnel parcel count and area are non-increasing at every stage
    (a filter can only remove parcels, never add them).
  - The funnel's starting count/area matches the full ParcelMap BC
    extract for the AOI/municipal boundary, an independent-number check
    against the parcel fabric itself.
  - At least one network distance spot-checked against a manually
    measured or independently sourced reference distance (e.g. a known
    landmark-to-landmark distance), not just internally consistent.
  - CRS check after every reprojection: report the CRS and confirm units
    are metres.

## Open issues

- This step does not yet answer its own central question ("how many
  units can vacant and underused parcels hold"). It answers a
  narrower, real question instead: which zones exist, how many parcels
  carry each, and which zones even allow multi-unit housing. Turning
  that into a unit-capacity number needs two things not found this
  session:
  1. The zoning bylaw's actual density/FAR/minimum-lot-size provisions
     per zone (a legal document, not yet located).
  2. A vacancy or "underused" indicator per parcel (e.g. BC
     Assessment's improvement-to-land value ratio, joined against
     PMBC_Parcel_Fabric_2_view's legal descriptions/geometry via
     C047). BC Assessment's own licence page (C021) does not itself
     link to this product.
- Both FeatureServers' licence field on their item pages is literally
  "none" (unspecified), not a stated open licence like ParcelMap BC's
  province-wide equivalent (S030); worth flagging to the user before
  any public-facing reuse of the City's own copies.
- The Oscar Lands Master Plan (C015/C038) has not been read as a
  document (only its City-webpage description); whether it states its
  own unit-capacity figures directly has not been checked.

## Status

built (zoning distribution + Resort Lands DPA area); parcel suitability
funnel proposed, not yet built

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
