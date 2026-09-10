#!/usr/bin/env bash
# Remove the SessionStart hook installed by install.sh, leaving every other hook untouched.
set -euo pipefail
SETTINGS="${CLAUDE_SETTINGS:-$HOME/.claude/settings.json}"
SETTINGS="$SETTINGS" python3 <<'PY'
import json, os
from pathlib import Path

settings = Path(os.environ["SETTINGS"])
if not settings.is_file():
    print("no settings file; nothing to remove"); raise SystemExit(0)
data = json.loads(settings.read_text())
groups = data.get("hooks", {}).get("SessionStart", [])
before = len(groups)
groups[:] = [g for g in groups if not any(h.get("_mpsw") for h in g.get("hooks", []))]
if not groups:
    data.get("hooks", {}).pop("SessionStart", None)
if data.get("hooks") == {}:
    data.pop("hooks")
settings.write_text(json.dumps(data, indent=2) + "\n")
print(f"removed {before - len(groups)} managed SessionStart entr{'y' if before-len(groups)==1 else 'ies'}")
PY
