"""PostToolUse hook for Edit, Write, and NotebookEdit.

Reads the tool-call payload Claude Code sends on stdin and, depending on
which file was just edited, reruns the matching checker so a bad edit is
caught immediately instead of at the next manual check:

    research/sources.csv          -> tools/verify_sources.py
    research/claims.csv           -> tools/check_citations.py
    steps/*.md, notebooks/*.ipynb -> tools/check_citations.py

Exits 2 with the checker's output on stderr when a check fails, so Claude
Code surfaces the failure back to the assistant. Anything else is a no-op.
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def project_python():
    venv_python = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
    return venv_python if os.path.exists(venv_python) else sys.executable


def edited_path(payload):
    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input", {})
    if tool_name == "NotebookEdit":
        return tool_input.get("notebook_path")
    return tool_input.get("file_path")


def script_for(rel_path):
    if rel_path == os.path.join("research", "sources.csv"):
        return "verify_sources.py"
    if rel_path == os.path.join("research", "claims.csv"):
        return "check_citations.py"
    if rel_path.startswith("steps" + os.sep) and rel_path.endswith(".md"):
        return "check_citations.py"
    if rel_path.startswith("notebooks" + os.sep) and rel_path.endswith(".ipynb"):
        return "check_citations.py"
    return None


def main():
    payload = json.load(sys.stdin)
    path = edited_path(payload)
    if not path:
        return 0

    path = os.path.normpath(path)
    if not os.path.isabs(path):
        path = os.path.join(ROOT, path)
    try:
        rel_path = os.path.relpath(path, ROOT)
    except ValueError:
        return 0  # different drive; not a project file

    script_name = script_for(rel_path)
    if script_name is None:
        return 0

    script = os.path.join(ROOT, "tools", script_name)
    result = subprocess.run(
        [project_python(), script], cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        sys.stderr.write(f"{script_name} failed after editing {rel_path}:\n")
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
