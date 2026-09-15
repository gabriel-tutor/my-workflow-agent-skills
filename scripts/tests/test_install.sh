#!/usr/bin/env bash
# The installer's settings step, against a fixture home. Steps that call the claude CLI or the
# network are stubbed; the real ~/.claude is never touched.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
fail() { echo "FAIL: $*" >&2; exit 1; }

# A fixture home whose MP skills are symlinks into a manager directory, as skills-manager lays them out.
H="$TMP/home"; mkdir -p "$H/.claude/skills" "$H/.skills-manager/skills/grilling"
: > "$H/.skills-manager/skills/grilling/SKILL.md"
ln -s "$H/.skills-manager/skills/grilling" "$H/.claude/skills/grilling"
echo '{"model":"opus","permissions":{"allow":["Bash(git *)"]}}' > "$H/.claude/settings.json"

# Stub claude, node and npx so the script's other steps run without the CLI or the network.
mkdir -p "$TMP/bin"
cat > "$TMP/bin/claude" <<'SH'
#!/usr/bin/env bash
case "$*" in
  --version) echo "0.0.0-stub";;
  "plugin marketplace list") echo "  ❯ my-workflow-agent-skills";;
  "plugin list") echo "  ❯ matt-pocock-workflow@my-workflow-agent-skills";;
  *) exit 0;;
esac
SH
chmod +x "$TMP/bin/claude"
ln -sf "$(command -v node)" "$TMP/bin/node"; ln -sf "$(command -v python3)" "$TMP/bin/python3"

OUT=$(HOME="$H" CLAUDE_CONFIG_DIR="$H/.claude" PATH="$TMP/bin:/usr/bin:/bin" bash "$REPO/scripts/install.sh" </dev/null) \
  || fail "installer exited non-zero: $OUT"

python3 - "$H/.claude/settings.json" "$H" <<'PY' || fail "settings not as expected"
import json, sys
d = json.load(open(sys.argv[1])); home = sys.argv[2]
allow = d["permissions"]["allow"]
assert d["model"] == "opus", "unrelated key lost"
assert "Bash(git *)" in allow, "existing rule lost"
assert "Read(~/.claude/skills/**)" in allow and "Read(~/.claude/plugins/**)" in allow, allow
assert any(r.startswith("Read(/") and ".skills-manager" in r for r in allow), f"no rule for the resolved skills dir: {allow}"
PY
[[ -f "$H/.claude/settings.json.pre-mpw-install" ]] || fail "no backup written"

# Idempotent: a second run adds nothing.
BEFORE=$(cat "$H/.claude/settings.json")
HOME="$H" CLAUDE_CONFIG_DIR="$H/.claude" PATH="$TMP/bin:/usr/bin:/bin" bash "$REPO/scripts/install.sh" </dev/null >/dev/null
[[ "$(cat "$H/.claude/settings.json")" == "$BEFORE" ]] || fail "second run changed settings"

# Without the MP skills and no tty, the installer must stop with a clear error rather than hang.
H2="$TMP/home2"; mkdir -p "$H2/.claude/skills"
if HOME="$H2" CLAUDE_CONFIG_DIR="$H2/.claude" PATH="$TMP/bin:/usr/bin:/bin" bash "$REPO/scripts/install.sh" </dev/null >/dev/null 2>"$TMP/err"; then
  fail "installer should fail when MP skills are missing and it cannot prompt"
fi

echo "test_install: OK"
