# 01 Scope and data inventory

## Question

What question is this project answering, what will it explicitly not
claim, and what dataset does every later step need, with its source and
licence?

## Decision

[left for the user]

## Alternatives considered

- Hand-write the inventory as prose in this file instead of a notebook.
  Rejected: CLAUDE.md rule 7 forbids typing computed numbers (including
  counts) into markdown, and the inventory changes every time
  research-scout or source-verifier touches the CSVs, so it has to be
  derived in code each run, not maintained by hand.

## Evidence

research/claims.csv now has claims tagged to this step: [C017] through
[C023], recording the LiDAR/DEM (S027-S029) and parcel/zoning (S030-S033)
source candidates research-scout found for steps 03 and 07. All are
needs-review or better as of the last /run.

## Inputs

- research/sources.csv and research/claims.csv, read only through
  src/resort/ledger.py's read_ledger() (evidence: this is the same
  guarded loader CC-3 built, not a fresh csv.reader call).

## Method

- (judgment call) Report a plain inventory (per-source licence, local
  copy, verified_exists; per-step claim counts by status) rather than a
  judgment about which sources are good enough. That judgment belongs to
  source-verifier and the user, not to this step.

### Project CRS for spatial analysis (added for steps 03/04/07/10)

- (judgment call) **EPSG:26911 (NAD83 / UTM zone 11N)** is this
  project's one projected CRS for all spatial analysis. Reason: it is
  what the City of Revelstoke's own ArcGIS FeatureServers already use
  (confirmed directly on Zoning, PMBC Parcel Fabric, OCP Resort Lands
  DPA, Buildings, and every other City layer checked so far), it is in
  metres, and a single UTM zone has low distortion for an area this
  small (the whole AOI is a few km across). The alternatives were
  HRDEM's native EPSG:3979 (Canada Atlas Lambert, accurate nationally
  but not the City's own working CRS) and BC's common EPSG:3005 (BC
  Albers, similarly a province-wide compromise). Every other CRS
  (HRDEM's 3979, OSM's 4326, and whatever ParcelMap BC/S030 turns out to
  use) gets explicitly reprojected to 26911 before any distance, area,
  or slope calculation, with a check that the result reports in metres
  afterward.

## Outputs

- data/processed/01_dataset_inventory.csv
- data/processed/01_claims_by_step_status.csv
- data/processed/01_summary.json

## Checks

- read_ledger() must return at least one source and one claim (it raises
  on its own if the CSVs are unreadable).
- n_claims_human_verified must be an int, so the report step can use it
  directly without a hand-typed number.
- Last run: 30 sources, 29 claims, 2 sources with a local copy
  downloaded, 0 claims human-verified yet.

## Open issues

- The master plan appendix (S011) and the 2024 Housing Needs Report
  (S013) turned out to be reachable by WebFetch and are now downloaded to
  data/raw and read. Several other sources still return HTTP 503 to a
  scripted request (S010, S014, S017, S018) or 403 (S026) and need a
  human to open them in a browser before their licence terms can be
  recorded here. It is not yet clear whether that is a genuine block or
  just a difference between this machine's script and WebFetch's request
  path, so it should be re-tried rather than assumed permanent.
- LiDAR/DEM coverage over Mount Mackenzie/RMR specifically (LidarBC S027,
  NRCan HRDEM S029) and whether the City's Open Data Portal (S033)
  actually publishes a zoning layer are both unconfirmed. Both sites are
  JavaScript apps WebFetch cannot query by location; a human needs to
  browse them directly. See [C018], [C019], [C023].
- BC Assessment's licence page (S031) does not itself link to a
  downloadable parcel dataset; the actual product page has not been
  found yet.
- The project's explicit non-claims (what this analysis will not assert)
  have not been drafted. This needs a decision from the user, not
  evidence.

## Status

built

## Changelog

- 2026-09-10: created.
- 2026-09-10: research-scout added C017-C023 (LiDAR/DEM and parcel
  source candidates). Built notebooks/01_scope_and_data_inventory.ipynb;
  ran clean via `/run 01`. Filled Inputs/Method/Outputs/Checks.
