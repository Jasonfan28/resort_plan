# 05 Workforce

## Question

Converting skier capacity to employee counts under low, mid, and high
staffing ratios, split seasonal versus year-round, how many workers need
housing once resort-provided beds are subtracted?

## Decision

[left for the user]

## Alternatives considered

- Pick one side of the C009/C010 headcount conflict and build the
  ratio-based estimate off it instead. Rejected: CLAUDE.md rule 5 says
  record both and do not pick one, and in any case neither figure is
  used as an input below (the model runs off CCC and an external
  comparator ratio, not RMR's own current headcount).
- Ask research-scout for an industry-standard low/mid/high staffing
  ratio table before modeling anything. Tried: no such source was found
  (see C040-C044); the only real capacity-to-employee data point found
  was one comparator resort, not a range.

## Evidence

- [C009] agent-checked. RMR ~500 employees incl. hotel/F&B (2018-11-09,
  Revelstoke Current). Conflicts with [C010].
- [C010] agent-checked. RMR >200 winter staff (Working Holiday Club, a
  recruitment listing). Conflicts with [C009].
- [C011] agent-checked. RMR can house >400 on-site with its new
  building (2025 quote from RMR's operations VP); article also gives
  the building's own numbers: 92 units, >200 in its residential wing.
- [C012] agent-checked. 2022 plan: 3 buildings x 160 beds = 480 total,
  inside C031's 150-200/building range; the 2025 as-built building
  (C011) has a different unit mix, so C012 may not describe what was
  actually built.
- [C016] agent-checked. Big White ~1,000 employees/winter; a comparator,
  not an RMR fact.
- [C040] agent-checked. Parks Canada's Sunshine Village site guidelines:
  6,000-skier approved capacity and ~700 peak-season employees, for one
  comparator resort.
- [C041] agent-checked. Sunshine Village's on-hill staff housing is
  capped at 190 employees regardless of capacity growth; the rest must
  be housed off-site.
- [C042] agent-checked. CWSAA: 22,522 direct/indirect/induced jobs
  (2022/23) against 8.75M skier visits (2023/24) BC-wide; a whole-
  industry, mismatched-season metric, not a per-resort ratio, kept for
  the record but not used below.

## Inputs

- data/processed/02_ccc_by_phase.csv (step 02, from C025)
- data/processed/02_employee_housing_phase2.json (step 02, from C031)

## Method

- (evidence) Use C040's ratio (~700/6,000 = 0.117 employees per CCC
  skier) as the model's central value. It is the only source found
  giving both halves of a capacity-to-employee relationship for any
  resort.
- (judgment call) Apply a +/-30% sensitivity band around that one ratio
  to produce low/mid/high estimates, since no source gives RMR-specific
  or industry-wide low/mid/high ratios. This is a modeling choice about
  how much the one real ratio might vary, not three separately sourced
  figures, and the notebook's own markdown says so.
- (evidence, with a caveat) Subtract housing using C031's 450-600 total
  beds (3 buildings x 150-200), not C012's more specific 480, since
  C012's as-built status is now in doubt (see Evidence above).
- (judgment call) Does not split seasonal vs. year-round employees, as
  the step's Question asks: no source gives that split for RMR or a
  comparator, so it is left out rather than guessed (CLAUDE.md rule 6).

## Outputs

- data/processed/05_employee_estimates.csv (phase x low/mid/high
  employees x beds-needed range)

## Checks

- Employees rise with CCC; low <= mid <= high at every phase; beds-
  needed never negative.
- Last run: all checks passed. At buildout, mid-band estimate is ~2,119
  employees against 450-600 resort-provided beds, leaving roughly
  1,519-1,669 needing housing elsewhere under this ratio and band.

## Open issues

- The employees-per-CCC ratio rests on one comparator resort (Sunshine
  Village), not RMR itself and not an industry standard. If a second
  comparator or an RMR-specific figure turns up later, this estimate
  should be revisited rather than treated as settled.
- The step's Question asks for a seasonal-vs-year-round split; no
  source provides one, so it is not modeled (see Method).
- C009 vs. C010 (RMR's own current headcount) remains an open conflict
  and is not used as a model input, only as context; whether "~500" or
  ">200" is closer to today's true headcount is still unresolved.
- C012's 2022 plan (3 x 160 beds) may not match the as-built 2025
  housing (C011's article describes a different mix); the model uses
  C031's wider range instead of resolving this.
- C041's 190-employee on-site cap (from Sunshine Village) suggests beds
  may cap out well below "needed" even at Phase 1 in some models; this
  step does not import that specific cap for RMR since no source states
  RMR has an equivalent cap.

## Status

built

## Changelog

- 2026-09-10: created.
- 2026-09-10: research-scout found the one real capacity-to-employee
  comparator (C040-C042); source-verifier promoted C009-C012, C016,
  C040-C042 to agent-checked; built
  notebooks/05_workforce.ipynb and ran clean via `/run 05`.
