---
name: step
description: Plan a pipeline step from its steps/NN-*.md file before any notebook is built. Stop for approval before writing code.
disable-model-invocation: true
argument-hint: [NN]
arguments: [step_number]
---

## Plan step $step_number

1. Read steps/$step_number-*.md in full, along with CLAUDE.md and any
   existing notebooks/$step_number_*.ipynb.
2. Read research/claims.csv and research/sources.csv (src/resort/ledger.py
   has read_ledger() for this) for every claim already tagged with this
   step.
3. Produce a plan and write it into the step file's Inputs, Method,
   Outputs, and Checks sections:
   - Inputs: each one named with the claim ID(s) or source ID(s) it
     depends on, or marked "no evidence available" if none exists yet.
   - Method: each method choice marked (evidence) with the claim ID it
     follows, or (judgment call) with a one-line reason.
   - Outputs: the exact data/processed/NN_*.* file(s) the notebook will
     write.
   - Checks: what a passing run must show, for example row counts, a
     sanity range, or a comparison against a claimed figure.
4. If a fact the plan needs has no claim ID, do not build the plan around
   a guess. List it under Open issues as needing the research-scout
   subagent, and leave that part of the plan incomplete.
5. Do not write or edit anything in notebooks/. Show the completed plan
   and stop. Wait for explicit approval before any notebook work begins.
