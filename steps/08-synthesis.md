# 08 Synthesis

## Question

Following the full chain (terrain and lifts to capacity, snow reliability
adjusting capacity, capacity to workforce, workforce to housing demand,
land capacity for supply), what does one scenario table and its
accompanying maps show?

## Decision

[left for the user]

## Alternatives considered

- Omit the snow-adjusted-capacity and land-capacity-units columns
  entirely, since neither has a value yet. Rejected: an omitted column
  reads as "not part of the chain," while an explicit null column reads
  as "part of the chain, not yet answered" — the latter is the true
  state and matches what steps 04 and 07 actually found.
- Wait to build this step until steps 04 and 07 fully answer their
  Questions. Rejected: steps 03, 05, and 06 are complete enough to
  synthesize now, and CLAUDE.md's own rule 6 (leave a statement out
  rather than guess) applies at the column level, not by blocking the
  whole step.

## Evidence

No claims are tagged to this step directly; it combines steps 03-07's
already-cited data/processed outputs rather than introducing new facts.

## Inputs

- data/processed/03_ccc_phase_reproduction_summary.csv (step 03)
- data/processed/05_employee_estimates.csv (step 05)

## Method

- (evidence) Join step 03's and step 05's phase-level tables on phase,
  and assert their CCC figures agree exactly (both trace to claim
  C025), so the two notebooks cannot silently drift apart on the same
  number.
- (judgment call, explicit) Carry `snow_adjusted_ccc` and
  `land_capacity_units` as columns filled with nulls, not values, since
  steps 04 and 07 do not yet produce them. This makes the chain's gap
  visible in the table itself rather than only in prose.
- (judgment call) Does not carry the C009/C010 workforce-headcount
  conflict into this table, since step 05's model does not use RMR's
  current headcount as an input at all (it runs off CCC and the
  Sunshine Village ratio, C040) — so that particular conflict does not
  actually propagate into this step's numbers, unlike step 05's Open
  issues originally worried it might.

## Outputs

- data/processed/08_scenario_table.csv (phase x low/mid/high
  employees and housing-demand bands, plus the two open columns)

## Checks

- Step 03's and step 05's CCC figures must match exactly at every
  phase; the two open-gap columns must remain null, not a placeholder
  number.
- Last run: all checks passed.
- No maps have been built. The step's Question also asks for
  "accompanying maps"; that needs the parcel/zoning geometry (not just
  the attribute queries done in step 07) and a mapping package (e.g.
  geopandas + matplotlib, both already installed), which has not been
  attempted this session.

## Open issues

- Two chain links have no number yet (see Method): snow-adjusted
  capacity (step 04) and land capacity in units (step 07). This table
  is complete for the links that have evidence and explicit about the
  ones that do not.
- No maps exist yet. Building them would need pulling actual geometry
  (not just attributes) from the Zoning/PMBC Parcel Fabric
  FeatureServers used in step 07.
- This step inherits step 05's single-comparator ratio caveat (Sunshine
  Village, not RMR) for every employee and housing-demand figure here.

## Status

built

## Changelog

- 2026-09-10: created.
- 2026-09-10: built notebooks/08_synthesis.ipynb combining steps 03 and
  05; ran clean via `/run 08`. Left snow-adjusted capacity, land-
  capacity units, and maps as explicit open gaps.
