#!/usr/bin/env bash
# Install/uninstall against a throwaway settings file; the real ~/.claude is never touched.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
export CLAUDE_SETTINGS="$TMP/settings.json"
fail() { echo "FAIL: $*" >&2; exit 1; }

# A pre-existing hook of the user's own, plus an unrelated key, must both survive.
cat > "$CLAUDE_SETTINGS" <<'JSON'
{"model":"opus","hooks":{"SessionStart":[{"matcher":"startup","hooks":[{"type":"command","command":"/usr/bin/true"}]}]}}
JSON
cp "$CLAUDE_SETTINGS" "$TMP/original.json"

"$REPO/scripts/hooks/install.sh" >/dev/null
python3 - <<'PY' || fail "install damaged settings"
import json, os
d = json.load(open(os.environ["CLAUDE_SETTINGS"]))
g = d["hooks"]["SessionStart"]
mine = [h for e in g for h in e["hooks"] if h.get("_mpsw")]
assert len(mine) == 1, f"expected 1 managed hook, got {len(mine)}"
assert mine[0]["command"].endswith("scripts/hooks/session-start"), mine[0]["command"]
assert d["model"] == "opus", "unrelated key lost"
assert any(h.get("command") == "/usr/bin/true" for e in g for h in e["hooks"]), "user hook lost"
PY
[[ -f "$CLAUDE_SETTINGS.mpsw-backup" ]] || fail "no backup written"

"$REPO/scripts/hooks/install.sh" >/dev/null   # idempotency
N=$(python3 -c "
import json,os
d=json.load(open(os.environ['CLAUDE_SETTINGS']))
print(sum(1 for e in d['hooks']['SessionStart'] for h in e['hooks'] if h.get('_mpsw')))")
[[ "$N" == "1" ]] || fail "not idempotent: $N managed hooks after second install"

"$REPO/scripts/hooks/uninstall.sh" >/dev/null
export TMP_ORIGINAL="$TMP/original.json" TMP="$TMP"
python3 - <<'PY' || fail "uninstall did not restore the original settings"
import json, os, sys
a = json.load(open(os.environ["TMP_ORIGINAL"]))
b = json.load(open(os.environ["CLAUDE_SETTINGS"]))
sys.exit(0 if a == b else 1)
PY

# The hook itself: valid JSON, correct event name, real skill body, safe preamble.
"$REPO/scripts/hooks/session-start" <<< '{}' > "$TMP/out.json"
python3 - <<'PY' || fail "malformed hook output"
import json, os
raw = open(os.environ["TMP"] + "/out.json").read()
if raw.strip():                       # empty output is valid: no router active
    d = json.loads(raw)
    hso = d["hookSpecificOutput"]
    assert hso["hookEventName"] == "SessionStart", hso["hookEventName"]
    c = hso["additionalContext"]
    assert c.startswith("<EXTREMELY_IMPORTANT>"), "preamble missing"
    assert "process owner" in c, "skill body missing from injection"
PY

# No router active -> no output at all.
EMPTY_HOME="$TMP/empty"; mkdir -p "$EMPTY_HOME/.claude/skills"
OUT=$(HOME="$EMPTY_HOME" "$REPO/scripts/hooks/session-start" <<< '{}')
[[ -z "$OUT" ]] || fail "expected no injection when no router is active, got: $OUT"

echo "test_hooks: OK"
