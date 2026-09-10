"""PreToolUse hook for Bash. Blocks any git push so the user pushes, not Claude.

Matches `git push` as a command word, not just a substring, so it does not
false-positive on something like a commit message containing the words.
"""

import json
import re
import sys


def main():
    payload = json.load(sys.stdin)
    command = payload.get("tool_input", {}).get("command", "")
    if re.search(r"(?:^|[;&|\n]|&&|\|\|)\s*git\s+push\b", command):
        sys.stderr.write(
            "Blocked: this repo's rule is 'Never push. I push.' Ask the user "
            "to run git push themselves instead.\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
