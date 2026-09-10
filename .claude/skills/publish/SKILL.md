---
name: publish
description: Run the full pipeline fresh, enforce the report citation gate, and export docs/ for GitHub Pages. Stops before committing.
disable-model-invocation: true
---

## Publish

1. Run `python tools/run_pipeline.py` for every step, fresh, with no cached
   runs.
2. Run `python tools/check_citations.py --report`. If it exits non-zero,
   stop here and report the failures. Do not export anything.
3. Export every notebooks/*.ipynb to docs/notebooks/ as HTML with
   `jupyter nbconvert --to html`, and export notebooks/09_report.ipynb to
   docs/report/index.html with `--no-input` so code cells are hidden.
4. Show a summary of what changed under docs/.
5. Stop. Do not commit or push. That is for the user to review first.
