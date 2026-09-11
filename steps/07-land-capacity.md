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

## Inputs

- research/claims.csv (C049, C050) — both queried live this session via
  the City's ArcGIS FeatureServer REST API, not just described from a
  landing page.

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

## Outputs

- data/processed/07_zoning_by_parcel_count.csv
- data/processed/07_resort_lands_dpa.json

## Checks

- Every zone code classified into exactly one multi-unit-eligible
  group; the classified total matches the raw table's own parcel-count
  sum.
- Last run: all checks passed.

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

built

## Changelog

- 2026-09-10: created.
- 2026-09-10: found live, queryable City FeatureServers for zoning and
  parcels (resolving step 01's C023 open question); built
  notebooks/07_land_capacity.ipynb and ran clean via `/run 07`. Left the
  step's core unit-capacity question open pending bylaw density data
  and a vacancy indicator.
