# 06 Housing supply and affordability

## Question

How many dwellings are not occupied by usual residents, how do rents
compare with resort wages, and what does the short-term rental context
look like?

## Decision

[left for the user]

## Alternatives considered

- Approximate resort wages from a generic BC tourism-sector wage
  statistic to complete the rent-vs-wage comparison. Rejected: no such
  source was found and read this session, and a generic provincial
  figure would misrepresent itself as resort-specific.

## Evidence

- [C003] agent-checked. City's 2025 Interim Report housing needs
  assessment page. Source S012.
- [C004] Could not check (S025 PDF returned HTTP 403, no local copy).
  Secondary source; its 1.6 demand factor is close to but not confirmed
  identical with C028's primary-sourced 1.63 for Revelstoke specifically.
- [C013]/[C037] agent-checked. Revelstoke (municipality and resort area)
  exempt from the STR principal residence requirement; confirmed via
  both a news article and the provincial page itself.
- [C014] agent-checked. The STR data portal page is for local
  governments.
- [C026]-[C029] agent-checked. 5-year/20-year housing need by
  component; 2021 rental vacancy 1.4% vs. 3-5% healthy.
- [C048] The HNR's owner affordability table (2024): only two of five
  family types can afford any dwelling type at 30% of income, and none
  can afford a single-detached home or townhouse.

## Inputs

- data/processed/02_housing_need_by_component.csv (step 02, from
  C026-C029)

## Method

- (evidence) Report the HNR's own rental-vacancy and ownership-
  affordability figures as given, without projecting them forward or
  combining them into a single index.
- (judgment call) Do not attempt a rent-versus-resort-wage comparison.
  No source in research/ gives a resort-specific wage figure or a
  dollar-value renter affordability table (the HNR's own affordability
  table is for ownership, not rental); approximating one from unrelated
  data would violate CLAUDE.md rule 6.
- (judgment call) Do not attempt "dwellings not occupied by usual
  residents" (a specific census metric the step's Question names). It
  was not found in the HNR pages read this session; a dedicated Census/
  StatCan check has not been done.

## Outputs

- data/processed/06_ownership_affordability_gap.csv
- data/processed/06_rental_vacancy.json
- data/processed/06_str_context.json

## Checks

- Healthy vacancy range internally consistent (low < high); the actual
  2021 vacancy rate falls below that range; at least one family type
  can afford at least one dwelling type (a sanity check that the table
  was transcribed right, not uniformly zero).
- Last run: all checks passed.

## Open issues

- The step's Question asks specifically for "dwellings not occupied by
  usual residents" (a Census/NOUR-style metric) and a rent-vs-wage
  comparison. Neither is answered here; both need either a dedicated
  Census data pull or a resort-wage source that has not been found.
- C004 (1.6) vs. C028 (1.63) remains an open, unresolved conflict per
  CLAUDE.md rule 5. C004 itself could not be re-verified this session
  (S025 now returns HTTP 403 and there is no local copy).
- The Oscar Lands Master Plan (C015/C038) overlaps with this step's
  housing-supply scope but is filed under step 07; see step 07's Open
  issues for the same cross-reference.

## Status

built

## Changelog

- 2026-09-10: created.
- 2026-09-10: source-verifier confirmed most claims (C004 still
  unreachable); built
  notebooks/06_housing_supply_and_affordability.ipynb and ran clean via
  `/run 06`. Left "dwellings not occupied by usual residents" and rent-
  vs-wage unanswered for lack of evidence.
