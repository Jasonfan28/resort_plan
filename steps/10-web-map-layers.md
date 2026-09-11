# 10 Web map layers

## Question

What simplified spatial layers, small enough to publish on GitHub Pages,
let the landing page show the area of interest, lift lines with their
DEM-derived vertical, runs by difficulty, an elevation surface, elevation
bands, and the parcels that survive step 07's suitability funnel?

## Decision

[left for the user]

## Alternatives considered

- Build a vector tile pyramid (e.g. via a tippecanoe-style tool) for the
  parcel/zoning layers. Rejected for now: the area of interest is a few
  km across and the layer counts involved (dozens to a few hundred
  parcels, ~120 runs, 7 lifts) are small enough that plain GeoJSON at a
  simplified geometry tolerance should stay well under the 25 MB limit
  without needing tiling infrastructure or a new non-Python dependency.
  Revisit if an actual exported file turns out too large.
- Publish City of Revelstoke zoning/parcel geometry directly, since it
  is already used for step 07's analysis. Rejected per the user's
  explicit instruction: City layers' licence fields are blank/none
  (C045-C047, C054, C056-C062), so none of that geometry goes in docs/
  until the licence is confirmed. ParcelMap BC (S030/C065), which does
  state a licence path, is used for any parcel geometry published here
  instead; City data still feeds the step 07 analysis, just not the
  public map.

## Evidence

No claims are tagged to this step directly; it packages steps 03/04/07's
already-cited outputs into small web-friendly files. Which underlying
claims back each layer is documented in those steps.

## Inputs

- data/processed/03_aoi.gpkg, 03_lift_crosswalk.csv, 03_runs.gpkg (step
  03, once built)
- data/processed/04_elevation_aspect_bands.csv (step 04, once built)
- data/processed/07_parcel_funnel.csv plus ParcelMap BC geometry
  (S030/C065) joined by parcel ID (step 07, once built)
- S048 (HRDEM 1m mosaic) for the hillshade image, clipped to the AOI

## Method

- (evidence/technical) Simplify each vector layer's geometry (e.g. a
  shapely/geopandas simplify tolerance in metres, chosen and reported,
  not left implicit) and export as plain GeoJSON in EPSG:4326 (the CRS
  web maps expect), reprojecting explicitly from the project CRS
  (EPSG:26911) and checking the result's coordinate ranges look like
  longitude/latitude afterward.
- (evidence/technical) Render one static hillshade image from the
  AOI-clipped, downsampled HRDEM (not the full 1 m resolution, which
  would be unnecessarily large for a small web image) rather than a
  tile pyramid, given the AOI's small size. NRCan's own STAC item
  already publishes a pre-rendered hillshade-dtm asset alongside the dtm
  asset; clipping that to the AOI instead of computing hillshade from
  scratch is worth trying first during build, since it needs no new
  computation, only a windowed read of an existing asset.
- (judgment call) Funnel parcels are published as a simplified
  ParcelMap BC (S030) polygon layer with the funnel's pass/fail and
  stage-reached as attributes, not the City's own parcel geometry, even
  though the funnel's analysis itself (step 07) uses City data for
  zoning/constraints. This keeps the analysis and the publishable
  geometry on two different, deliberately chosen sources.

## Outputs

- docs/data/10_aoi.geojson
- docs/data/10_lifts.geojson (with DEM-derived vertical rise as a
  property)
- docs/data/10_runs.geojson (with difficulty and DEM slope class)
- docs/data/10_elevation_bands.geojson
- docs/data/10_funnel_parcels.geojson (ParcelMap BC geometry, funnel
  pass/fail and stage-reached as attributes)
- docs/data/10_hillshade.png (or .webp)

## Checks

- Every file's size reported explicitly in the notebook output, not
  just asserted small; anything over 25 MB stays out of docs/ and out of
  git (gitignored), with a note explaining what was excluded and why.
- No City-of-Revelstoke-sourced geometry appears in any docs/ file (a
  grep-style check for field names/attribution unique to the City
  services, run against every exported file).
- Each GeoJSON's coordinates fall in plausible longitude/latitude ranges
  for the Revelstoke area after reprojection (a sanity check that the
  CRS conversion actually happened and produced the right units).

## Open issues

- This step depends entirely on steps 03, 04, and 07's proposed
  (not yet built) outputs; it cannot be built before them, and per the
  build order in this work, is built last.
- The exact geometry-simplification tolerance is not yet chosen; it
  will be picked during build and reported, not left as an unstated
  default.
- Whether a single hillshade image is visually adequate at the zoom
  levels the landing page actually uses is not yet checked; if not, a
  small set of pre-rendered zoom levels (still plain images, not a tile
  server) is the fallback, not a vector tile pipeline.

## Status

draft (proposed; not yet built, depends on steps 03/04/07)

## Changelog

- 2026-09-10: created as part of the spatial-analysis proposal (Phase 1).
  Awaiting approval before any notebook changes; also depends on steps
  03, 04, and 07 being built first.
