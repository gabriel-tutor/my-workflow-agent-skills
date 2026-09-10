#!/usr/bin/env bash
# Register the SessionStart hook that injects the active routing skill into every session.
#
#   scripts/hooks/install.sh      add it to ~/.claude/settings.json (backed up first)
#   scripts/hooks/uninstall.sh    remove only what this script added
#
# Idempotent: running twice leaves exactly one entry. Entries are tagged "_mpsw": true so
# uninstall can find them without touching hooks you configured yourself.
# Override the settings file for tests with CLAUDE_SETTINGS.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SETTINGS="${CLAUDE_SETTINGS:-$HOME/.claude/settings.json}"

REPO="$REPO" SETTINGS="$SETTINGS" python3 <<'PY'
import json, os, shutil
from pathlib import Path

repo, settings = Path(os.environ["REPO"]), Path(os.environ["SETTINGS"])
settings.parent.mkdir(parents=True, exist_ok=True)
data = json.loads(settings.read_text()) if settings.is_file() else {}
if settings.is_file():
    shutil.copy2(settings, str(settings) + ".mpsw-backup")

entry = {"matcher": "startup|clear|compact", "hooks": [
    {"type": "command", "command": str(repo / "scripts" / "hooks" / "session-start"), "_mpsw": True}]}

groups = data.setdefault("hooks", {}).setdefault("SessionStart", [])
groups[:] = [g for g in groups if not any(h.get("_mpsw") for h in g.get("hooks", []))]
groups.append(entry)
settings.write_text(json.dumps(data, indent=2) + "\n")
print(f"installed SessionStart hook -> {entry['hooks'][0]['command']}")
print(f"settings: {settings}   backup: {settings}.mpsw-backup")
PY
