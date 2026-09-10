# Prompt playbook: Revelstoke resort capacity and workforce housing

Paste prompts in order, one at a time. Review the diff and commit before moving on. Text in [brackets] is yours to fill. Each prompt is self-contained, so you can edit any of them without breaking the others.

Prefixes: **CC** runs in Claude Code from the repo root. **CW** runs in the Cowork project. **CH** is for chat.

---

## Before the first prompt (manual)

1. Create an empty GitHub repo and clone it to a folder outside OneDrive or any other synced folder.
2. Copy the three handed-over files into place: `tools/verify_sources.py`, `research/sources.csv`, `research/claims.csv`.
3. Make a free OpenAlex account, copy the key from openalex.org/settings/api, and add `export OPENALEX_API_KEY=[key]` to `~/.bashrc` in Git Bash.
4. Confirm Python is 3.10 or newer (`python --version`). Papermill requires it.
5. Open Claude Code in the repo folder.

---

## Claude Code

### CC-1 Scaffold and CLAUDE.md

```
This repo is a planning analysis of Revelstoke Mountain Resort and the City of Revelstoke. One chain: terrain and lifts set skier capacity (CCC), snow reliability adjusts capacity, capacity sets workforce size, workforce sets housing demand, land capacity shows where housing could go.

I work on Windows in Git Bash. Python only, no R.

Create this layout and a CLAUDE.md. Do not write analysis code yet.

steps/            one markdown file per step, the source of truth for decisions
notebooks/        all analysis, one notebook per step, outputs cleared in git
src/resort/       helpers used by more than one notebook
tools/            scripts: source verifier, citation checker, pipeline runner, hooks
research/         sources.csv, claims.csv (already present), inbox/ for Cowork output
data/raw/         gitignored downloads
data/processed/   intermediate files each notebook writes for the next one
runs/             executed notebook copies, gitignored
docs/             GitHub Pages root: index.html, notebooks/ HTML exports, report/

CLAUDE.md must stay under 200 lines and include these rules verbatim:

Rules on facts
1. Never state a fact, figure, date, or citation from memory. Every factual statement in steps/ or notebooks/ points to a claim ID in research/claims.csv, which points to a source ID in research/sources.csv.
2. Only add a source you retrieved in this session or that exists in research/inbox/. Record the exact URL. If you only saw a search snippet, say so in the claim's notes.
3. Never edit verified_exists, verified_on, or verify_note. tools/verify_sources.py fills them.
4. human_verified in sources.csv and the human-verified claim status are mine. Never write them.
5. When sources disagree, record both claims, fill conflicts_with, and list the conflict under Open issues in the step file. Do not pick one.
6. If nothing supports a statement, leave it out and say so. Decisions without evidence are labelled "judgment call".
7. Never type a computed number into markdown. Report text that contains numbers is built in code cells from data/processed files.

Notebook rules
- One notebook per step, named NN_short_name.ipynb, matching steps/NN-*.md.
- First code cell is tagged "parameters" and holds every value a reader might change.
- Each notebook reads only from data/raw, data/processed, and research/, and writes its results to data/processed/NN_*.
- Cells stay under 100 lines. A markdown cell above each code cell says what the cell does and why.
- Last cell prints Python and package versions using importlib.metadata.
- Code reused by two or more notebooks moves to src/resort/.
- Always open text files with encoding="utf-8". The Windows default encoding breaks on names like Nüst.

Working rules
- Ask before adding any package. State what it does that the current environment cannot.
- Before using a CLI flag or config format for any tool, check that tool's current official docs.
- Only change code for the step being worked on. Note needed changes to other steps under their Open issues.
- Commit after each completed step. Never push. I push.
- Prose follows my writing rules: no em dashes, no semicolons, no inflated language, plain statements of fact.

Show me the tree and CLAUDE.md, then stop.
```

### CC-2 Environment

```
Set up the Python environment for this project. Expected needs: geopandas, rasterio or rioxarray for the DEM, jupyter, papermill, nbconvert, pandas, matplotlib. Check what is already installed on this machine first.

Propose one approach (venv with pinned requirements.txt, or conda-forge environment.yml) and explain why for geospatial packages on Windows, citing the official install docs you checked. Do not install anything until I approve.

After approval, create the environment, pin versions, and confirm geopandas and rasterio import and can read a small test file.

Also propose the lightest way to keep outputs out of committed notebooks in notebooks/, and name any package it adds.
```

### CC-3 Ledger module and citation guard

```
Build src/resort/ledger.py with:

read_ledger(): loads research/claims.csv and research/sources.csv with encoding="utf-8", merges claims to sources on source_id, and raises if the number of rows read does not equal the number of lines starting with an ID (C### or S###). A broken quote once caused a CSV reader to silently drop rows in this project, so the guard is required.

cite(claim_id, ledger): returns a short label like "(Pimentel et al. 2019)" or "(City of Revelstoke 2024)". Raises LedgerError if the claim is missing, if its status is not human-verified, or if its source's verified_exists is not pass.

references(ledger): formatted reference list of sources behind human-verified claims, DOI links where present.

Write tools/test_ledger.py using only the standard library (no pytest unless I approve) that checks:
- a needs-review claim raises
- a human-verified claim whose source is "manual" raises
- a fully verified claim returns the right label for 1, 2, and 3+ authors
- an author name with ü reads correctly
- a CSV with one unclosed quote raises the row-count error

Use temporary copies of the CSVs in the tests. Never modify the real ledgers. Run the tests and show me the output.
```

### CC-4 Citation checker and hooks

```
Build tools/check_citations.py (standard library only):
- every claim's source_id exists in sources.csv
- every conflicts_with ID exists
- claim status is one of: needs-review, agent-checked, human-verified, rejected
- scan steps/*.md for [C###] references and notebooks/*.ipynb (markdown and code cells) for C### references. Unknown IDs are errors.
- with --report, every claim cited in notebooks/09_report.ipynb must be human-verified with a source that passed. Otherwise exit 1.

Then read the current Claude Code hooks docs and add to .claude/settings.json:
1. PostToolUse on Edit, Write, and NotebookEdit: if the edited file is research/sources.csv, run tools/verify_sources.py. If it is research/claims.csv, a step file, or a notebook, run tools/check_citations.py. Report failures back to you. Check in the docs which field holds the file path for NotebookEdit, since it may differ from Edit.
2. PreToolUse on Bash: block any git push with a message telling you to ask me.

Put hook logic in tools/hooks/*.py, not inline shell. I'm on Windows with Git Bash, so confirm how the hook command should call Python and reference the project directory there.

Then test each hook: edit a throwaway row, trigger a failure on purpose, try git push. Revert the test edits and show me what happened.
```

### CC-5 Subagents

```
Read the current Claude Code subagent docs, then create three project subagents in .claude/agents/.

research-scout
Finds candidate sources for a question I give. Uses WebSearch and WebFetch. Adds rows to research/sources.csv with the exact URL it fetched and claims to research/claims.csv with status needs-review and a locator (page, table, or section). Never cites from memory. If it only saw a snippet, the claim notes say so. Never touches verification columns.

source-verifier
Must not see the scout's reasoning, so it only works from the CSVs. For each needs-review claim: fetch the source, find the locator, and decide whether the source supports the claim as worded. If yes, set status agent-checked and tighten the locator. If no, leave status alone and write the mismatch in notes. Never sets human-verified. Returns a table of claim ID, verdict, and reason.

notebook-reviewer
Read-only. Checks a notebook against the notebook rules in CLAUDE.md and against Rule et al. 2019 (source S007): parameters at top, one task per cell, cells under 100 lines, markdown explaining why, intermediate results written to disk, no numbers typed into markdown, versions cell at the end. Runs the notebook fresh through papermill into runs/ to confirm it executes top to bottom. Returns a list of problems with cell references.

Keep tool lists as narrow as each job allows. Show me all three files.
```

### CC-6 Skills

```
Read the current Claude Code skills docs, then create project skills in .claude/skills/. Set disable-model-invocation: true on any skill that edits files or runs the pipeline.

/step NN
Read steps/NN-*.md. Produce a plan listing inputs with their claim or source IDs, method choices marked "evidence" or "judgment call", output files, and checks. Stop and wait for my approval before writing any notebook cells.

/add-source
Take material from research/inbox/ that I name, add sources and claims rows following CLAUDE.md, run tools/verify_sources.py, then hand the new claims to the source-verifier subagent.

/run [NN or all]
Run tools/run_pipeline.py for the given step or all steps, then report the Checks section results for each step that ran.

/publish
Run all steps fresh, run check_citations.py --report, export notebooks to docs/notebooks/ as HTML and the report notebook to docs/report/index.html with code hidden, then show me what changed in docs/. Stop before committing.
```

### CC-7 Pipeline runner

```
Build tools/run_pipeline.py. It runs notebooks/NN_*.ipynb in numeric order through papermill into runs/NN_*.ipynb with a fresh kernel each time, stops at the first failure and prints which cell failed, and accepts --only NN, --from NN, and -p name value to pass parameters. Check the current papermill docs for the API before writing it.

Add --scenario FILE, where FILE is a YAML or JSON of parameter sets (for example climate scenario and staffing ratio), running the affected notebooks once per set into runs/scenario_name/. If this needs a package I don't have, ask first.

Test it with two tiny throwaway notebooks that pass a value through data/processed, including one deliberate failure. Delete the throwaway notebooks after and show me the output.
```

### CC-8 Step files

```
Create steps/00-TEMPLATE.md with these sections: Question, Decision, Alternatives considered, Evidence (claim IDs, or "judgment call"), Inputs, Method, Outputs (files in data/processed), Checks, Open issues, Status (draft, approved, built, reviewed), Changelog.

Then create draft step files 01 to 09 from this outline. Fill Question and Open issues. Leave Decision empty for me. Where research/claims.csv already has claims for a step, reference them and copy their conflicts into Open issues.

01 Scope and data inventory: the project question, what it will not claim, and every dataset needed with its source and licence.
02 Planning documents: what the RMR master plan and City housing reports say about capacity, phasing, staff housing, and housing need.
03 Terrain and capacity: slope by ability class from LiDAR, runs and lifts, and whether the master plan's existing CCC can be reproduced from its stated inputs.
04 Snow reliability: elevation bands, baseline and mid-century climate under two emissions scenarios, one transparent reliability indicator validated against historical snowfall.
05 Workforce: converting capacity to employees with low, mid, and high ratios, seasonal versus year-round, minus resort-provided beds.
06 Housing supply and affordability: dwellings not occupied by usual residents, rents versus resort wages, short-term rental context.
07 Land capacity: units vacant and underused parcels can hold under current zoning, including City priority sites and resort base lands.
08 Synthesis: one scenario table following the chain, and the maps.
09 Report: prose built from data/processed with cite() for every claim.

Do not state any fact that is not already in claims.csv. Show me step 01 in full and a one-line summary of the rest.
```

### CC-9 Per-step loop (reuse for steps 01 to 08)

Run these as three separate prompts per step.

```
/step [NN]
```

After you edit and approve the plan:

```
Build notebooks/[NN]_[name].ipynb from the approved plan in steps/[NN]-*.md. Follow the notebook rules in CLAUDE.md. For any fact you need that isn't in claims.csv, stop and use the research-scout subagent rather than filling it in. When the notebook runs, update the step file's Outputs, Changelog, and Status, then run /run [NN] and show me the Checks results.
```

Then, in a fresh Claude Code session so the reviewer doesn't inherit the builder's context:

```
Use the notebook-reviewer subagent on notebooks/[NN]_*.ipynb and the source-verifier subagent on every needs-review claim for step [NN]. Give me one combined list of problems. Do not fix anything yet.
```

### CC-10 Merge Cowork output

```
/add-source research/inbox/[file]
```

### CC-11 Landing page

```
Build docs/index.html as hand-written static HTML, CSS, and JS, no framework. Structure it in three layers to match my portfolio case studies: Quick look (the scenario table and one map), Explainer (the chain in plain language), Methods (links to each notebook's HTML export and the report). Read numbers from a JSON file the synthesis notebook writes to docs/data/. Nothing in the page is typed by hand except headings and labels. Keep every file in docs/ under 25 MB. Describe the layout and list the files before committing.
```

### CC-12 Pre-publish audit (fresh session)

```
Audit this repo before I publish it. Do not change files. Report:
1. Any statement in steps/, notebooks/, or docs/ with a fact but no claim ID.
2. Any claim in the report that is not human-verified.
3. Any source with verified_exists other than pass that a published claim depends on.
4. Any dataset in docs/ whose licence is not recorded in sources.csv.
5. Whether a fresh run of all notebooks reproduces the numbers in docs/data/.
6. Any file over 25 MB.
```

---

## Cowork

### CW-0 Project setup (once)

In Cowork, create a new project and select the repo's `research/inbox/` folder only. Paste this into the project instructions:

```
You extract information from documents for a planning analysis. You do not analyze or interpret.

Write files only to this folder. For every value you extract, record: source file name, source URL if known, page number, table or section name, and the value exactly as printed with units. If a page is unreadable or a table is ambiguous, write UNREADABLE or AMBIGUOUS with the page number instead of guessing. Never fill a value from memory or from a web search when a document is provided.

Output tables as CSV with a header row. For each document, also write a short markdown note listing what you extracted and what you could not.

Write in plain language. No em dashes, no semicolons.
```

Then run this once to confirm Cowork can write to the folder:

```
Create a file called write_test.txt in this folder containing today's date.
```

### CW-1 Master plan (download the PDFs into research/inbox/ yourself first)

```
Read [master plan file name] and its appendix [appendix file name].

Extract to CSV:
1. The plan's title, date, and author or consultant as printed on the cover.
2. Every table in the comfortable carrying capacity appendix, all columns exactly as printed, one CSV per table, with page numbers.
3. The lift inventory table and the lift capacity and utilization table.
4. The historical snowfall table.
5. Any stated existing and buildout CCC totals, and any phasing table.
6. Every passage about staff or employee housing: page number and a one-sentence description of what it covers, no quotation longer than one sentence.
```

### CW-2 City housing reports

```
Read [housing needs report file names].

Extract to CSV:
1. The 5-year and 20-year housing need totals and each component as printed, with page numbers.
2. Any demand factor or multiplier the report applies, with page number.
3. Every rent figure: value, unit type, year, and the data source the report names for it.
4. Every mention of seasonal workers, resort employees, or short-term rentals: page number and one-sentence description.
5. The list of data sources the report says it used.
```

### CW-3 Reading list

```
Search for peer-reviewed research on:
1. Snow reliability indicators for ski areas under climate change, including any day-count thresholds used to define a viable season.
2. Methods for ski area comfortable carrying capacity or skier density.
3. Workforce housing in resort or amenity communities.

Write a CSV with: topic number, title, authors, year, DOI, and the URL of the landing page you opened. Include only items whose landing page you actually opened. Do not summarize papers you did not open. Mark anything that is not peer reviewed in a notes column.
```

### CW-4 Headcount conflict

```
Two sources give different staff counts for Revelstoke Mountain Resort: about 500 including hotel and food and beverage staff (Revelstoke Current, date unknown) and over 200 winter staff (Working Holiday Club listing).

Find the publication date of the Revelstoke Current article. Then search for any other public statement of RMR's employee count from the resort, its owner, the City, or local news. Write a CSV with: figure, what it includes, date, publisher, URL opened. Do not reconcile the numbers.
```

---

## Chat

Use chat to review decisions rather than build. Paste a step file after its plan is drafted and ask:

```
Here is steps/[NN]-[name].md. Tell me which decisions are weak, which judgment calls a mountain planning consultant or City planner would challenge, and what evidence would settle each one. Don't rewrite the file.
```
