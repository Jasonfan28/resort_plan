# CLAUDE.md

This repo is a planning analysis of Revelstoke Mountain Resort and the City of
Revelstoke. One chain: terrain and lifts set skier capacity (CCC), snow
reliability adjusts capacity, capacity sets workforce size, workforce sets
housing demand, land capacity shows where housing could go.

Windows, Git Bash. Python only, no R.

## Layout

```
steps/            one markdown file per step, the source of truth for decisions
notebooks/        all analysis, one notebook per step, outputs cleared in git
src/resort/       helpers used by more than one notebook
tools/             scripts: source verifier, citation checker, pipeline runner, hooks
research/         sources.csv, claims.csv (already present), inbox/ for Cowork output
data/raw/         gitignored downloads
data/processed/   intermediate files each notebook writes for the next one
runs/             executed notebook copies, gitignored
docs/             GitHub Pages root: index.html, notebooks/ HTML exports, report/
```

## Rules on facts

1. Never state a fact, figure, date, or citation from memory. Every factual
   statement in steps/ or notebooks/ points to a claim ID in
   research/claims.csv, which points to a source ID in research/sources.csv.
2. Only add a source you retrieved in this session or that exists in
   research/inbox/. Record the exact URL. If you only saw a search snippet,
   say so in the claim's notes.
3. Never edit verified_exists, verified_on, or verify_note.
   tools/verify_sources.py fills them.
4. human_verified in sources.csv and the human-verified claim status are
   mine. Never write them.
5. When sources disagree, record both claims, fill conflicts_with, and list
   the conflict under Open issues in the step file. Do not pick one.
6. If nothing supports a statement, leave it out and say so. Decisions
   without evidence are labelled "judgment call".
7. Never type a computed number into markdown. Report text that contains
   numbers is built in code cells from data/processed files.

## Notebook rules

- One notebook per step, named NN_short_name.ipynb, matching steps/NN-*.md.
- First code cell is tagged "parameters" and holds every value a reader
  might change.
- Each notebook reads only from data/raw, data/processed, and research/, and
  writes its results to data/processed/NN_*.
- Cells stay under 100 lines. A markdown cell above each code cell says what
  the cell does and why.
- Last cell prints Python and package versions using importlib.metadata.
- Code reused by two or more notebooks moves to src/resort/.
- Always open text files with encoding="utf-8". The Windows default
  encoding breaks on names like Nüst.

## Working rules

- Ask before adding any package. State what it does that the current
  environment cannot.
- Before using a CLI flag or config format for any tool, check that tool's
  current official docs.
- Only change code for the step being worked on. Note needed changes to
  other steps under their Open issues.
- Commit after each completed step. Never push. I push.
- Prose follows my writing rules: no em dashes, no semicolons, no inflated
  language, plain statements of fact.
