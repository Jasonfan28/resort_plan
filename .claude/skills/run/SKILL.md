---
name: run
description: Run tools/run_pipeline.py for one step or all steps, and report each step's Checks results.
disable-model-invocation: true
argument-hint: [NN|all]
arguments: [target]
---

## Run pipeline: $target

1. If $target is "all", run `python tools/run_pipeline.py`. Otherwise run
   `python tools/run_pipeline.py --only $target`.
2. If the run fails, report which notebook and which cell failed, then
   stop. Do not attempt a fix as part of this skill.
3. If it succeeds, open steps/NN-*.md for every step that ran and report
   its Checks section results using the values the notebook actually wrote
   to data/processed, not remembered numbers.
