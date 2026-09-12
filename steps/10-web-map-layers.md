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

- (evidence/technical) Simplify each vector layer's geometry (5 m
  tolerance, applied in the project CRS EPSG:26911 before reprojecting,
  so the tolerance means the same real-world distance for every layer)
  and export as plain GeoJSON in EPSG:4326. AOI and runs geometry come
  straight from step 03's own outputs (03_aoi.gpkg, 03_runs.gpkg, both
  OSM/DEM-derived); lifts are rebuilt from OSM's raw lift geometry
  (S050's saved Overpass result) joined to step 03's lift crosswalk,
  since the crosswalk CSV alone has no geometry column. Every vector
  layer uses an explicit column allowlist before export (not just a
  blocklist check afterward -- see Checks), so a future new column on
  an upstream file can't silently leak into a published layer.
- (evidence/technical) Elevation bands are not in any step 04 output
  (04_elevation_bands.csv is an area table, not polygons), so this step
  rebuilds them: re-clip the HRDEM over the AOI, coarsen 10x (native 1 m
  pixels would make an unusably large polygon count for a web layer),
  classify by the same band edges, vectorize, dissolve, then clip to
  the AOI's actual polygon shape (not just its bounding box, which
  clip_dem reads from and which extends well beyond the resort
  boundary), simplify, and export.
- (evidence/technical) The hillshade image uses NRCan's own pre-rendered
  hillshade-dtm STAC asset (a windowed read via the same clip_dem
  helper, just a different URL) rather than computing hillshade from
  scratch, clipped to the AOI and downsampled for a web-sized PNG.
- (judgment call, scoped down from the original proposal) Funnel
  parcels are published as a simplified ParcelMap BC (S030) polygon
  layer, not the City's own parcel geometry. Step 07, as built, only
  exported a per-parcel table for parcels that survived its *entire*
  filter chain (150 PIDs, data/processed/07_network_distances.csv) --
  not a stage-reached breakdown for every candidate parcel. This
  layer's attributes are therefore `passed_full_funnel=True` (a
  constant, since only full survivors are in scope) plus the two
  network-distance columns, not the richer per-stage attribute this
  step originally proposed. Getting stage-reached data would need a
  change to step 07's notebook, which this step did not make (only the
  step being worked on gets changed); noted under step 07's Open issues
  instead.
- (deviation, noted not left implicit) This notebook writes only to
  docs/data/, not data/processed/10_*, unlike other notebooks in this
  project. That is the explicit point of a publish-to-GitHub-Pages step
  and was already implied by this step's own approved Outputs list
  above; called out here so it reads as a conscious choice, not an
  oversight against the general notebook rule.

## Outputs

- docs/data/10_aoi.geojson (2,576 bytes)
- docs/data/10_lifts.geojson (2,362 bytes, 7 lifts, with DEM-derived
  vertical rise and the proposed master-plan map_ref as properties)
- docs/data/10_runs.geojson (79,877 bytes, 116 runs, with difficulty and
  DEM slope stats)
- docs/data/10_elevation_bands.geojson (12,620 bytes, 3 band polygons)
- docs/data/10_funnel_parcels.geojson (77,786 bytes, 144 of 150
  funnel-surviving parcels -- 6 have no PID in ParcelMap BC and could
  not be geometry-matched; `passed_full_funnel=True` plus network
  distances as properties, not a per-stage breakdown -- see Method)
- docs/data/10_hillshade.png (979,494 bytes)

All well under the 25 MB limit; nothing was excluded.

## Checks

- Every file's size reported explicitly in the notebook output (above)
  and asserted under 25 MB.
- No City-of-Revelstoke-sourced geometry or attribute appears in any
  docs/ file: checked two ways, not just one -- an explicit column
  allowlist at export time for every vector layer (Method), plus a
  blocklist scan afterward for field names unique to the City's own
  FeatureServers, as defense in depth.
- Each GeoJSON's coordinates fall in plausible longitude/latitude ranges
  for the Revelstoke area after reprojection.
- Elevation-band area cross-check: the rebuilt band polygons' total
  area is compared against the AOI's own area (an independent number
  from step 03/04, not derived from this step's own polygons). Last
  run: 1,248.1 ha (rebuilt) vs. 1,248.3 ha (AOI) -- within 0.02%. This
  check caught a real bug during build (see Changelog) and is kept as a
  permanent guard, not removed once it passed.
- Last run: all checks passed.

## Open issues

- The funnel-parcels layer only carries a constant `passed_full_funnel`
  attribute, not the stage-reached breakdown this step originally
  proposed, because step 07 (as built) only exports a per-parcel table
  for full survivors. Recorded under step 07's own Open issues as a
  possible future addition to that notebook, not fixed here.
- 6 of the 150 funnel-surviving parcels have no PID in ParcelMap BC and
  are absent from this layer entirely (not just unlabelled); consistent
  with the same PID-nullability characteristic step 07 already noted.
- Whether a single hillshade image is visually adequate at the zoom
  levels the landing page actually uses has not been checked against a
  real deployed page; the fallback (a small set of pre-rendered zoom
  levels) remains unused unless that turns out to be needed.
- This notebook writes only to docs/data/, not data/processed/10_*, a
  deliberate deviation from CLAUDE.md's general notebook-output rule
  (see Method) since publishing to docs/ is this step's entire purpose.

## Status

built

## Changelog

- 2026-09-10: created as part of the spatial-analysis proposal (Phase 1).
  Awaiting approval before any notebook changes; also depends on steps
  03, 04, and 07 being built first.
- 2026-09-12: built notebooks/10_web_map_layers.ipynb. Packaged real AOI,
  lift, and run geometry from steps 03; rebuilt elevation-band polygons
  from the HRDEM (not exported by step 04); published only step 07's
  150 full-funnel-survivor parcels against live ParcelMap BC geometry
  (144 matched; City geometry never used); clipped NRCan's own
  pre-rendered hillshade asset to the AOI. notebook-reviewer (fresh
  subagent) found one severe bug: `dem_coarse.rio.transform()` silently
  returned the pre-coarsen (1 m) transform after `xarray.coarsen()`,
  because coarsen() doesn't update the cached GeoTransform and
  `.rio.transform()` defaults to not recalculating it -- this shrank
  and mislocated every elevation-band polygon (~30x too small) while
  still passing every existing Check (file size, field blocklist,
  coordinate range), since none of them tested the polygons' actual
  area or position. Fixed with `.rio.transform(recalc=True)`; fixing it
  then surfaced a second, related bug (band polygons were clipped to
  the AOI's bounding box, not its actual polygon, spilling past the
  resort boundary) which I fixed by intersecting with the AOI polygon
  directly, and added a permanent area cross-check against step 03/04's
  own AOI area (1,248.1 vs. 1,248.3 ha) so a regression like this can't
  silently pass again. Also applied explicit column allowlists to the
  AOI/runs layers (the funnel-parcels layer already had one) as defense
  in depth alongside the blocklist check, and corrected this step's own
  Method/Outputs wording, which had overclaimed a stage-reached
  attribute step 07 doesn't actually produce.
