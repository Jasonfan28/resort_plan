---
name: add-source
description: Ingest material named in research/inbox/ into sources.csv and claims.csv, verify sources, and hand new claims to source-verifier.
disable-model-invocation: true
argument-hint: [file]
arguments: [inbox_file]
---

## Add source: $inbox_file

1. Read research/inbox/$inbox_file, and its companion markdown note if the
   Cowork output produced one.
2. Follow CLAUDE.md's rules on facts. Add one row to research/sources.csv
   per new source named in the file, and one row to research/claims.csv
   per fact worth recording, with status=needs-review and a locator (page,
   table, or section). Continue the existing S###/C### numbering. Leave
   verified_exists, verified_on, verify_note, and human_verified blank.
3. Run `python tools/verify_sources.py` and show its output. If it reports
   failures, fix or flag the offending rows. Do not delete a row silently.
4. Hand every claim ID you just added to the source-verifier subagent and
   report back its table of verdicts.
