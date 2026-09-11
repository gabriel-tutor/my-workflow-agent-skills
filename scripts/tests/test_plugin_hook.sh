#!/usr/bin/env bash
# The plugin's SessionStart hook, run against fixture homes, working directories and a
# fixture copy of the plugin. The real ~/.claude is never touched.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HOOK="$REPO/plugin/hooks/session-start"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
fail() { echo "FAIL: $*" >&2; exit 1; }
[[ -x "$HOOK" ]] || fail "hook missing or not executable: $HOOK"

# A fixture copy of the plugin whose bootstrap body is a known literal.
FIX="$TMP/plugin"
mkdir -p "$FIX/hooks" "$FIX/skills/using-matt-pocock-skills"
cp "$HOOK" "$FIX/hooks/session-start"
cat > "$FIX/skills/using-matt-pocock-skills/SKILL.md" <<'MD'
---
name: using-matt-pocock-skills
description: fixture description that must not be injected
---

Fixture routing policy line.
Routing details: ${CLAUDE_PLUGIN_ROOT}/skills/using-matt-pocock-skills/references/routing.md
MD
FIX_REAL=$(cd "$FIX" && pwd -P)

MP_HOME="$TMP/home-mp"; mkdir -p "$MP_HOME/.claude/skills/grilling"; : > "$MP_HOME/.claude/skills/grilling/SKILL.md"
BARE_HOME="$TMP/home-bare"; mkdir -p "$BARE_HOME/.claude/skills"
PLAIN="$TMP/plain"; mkdir -p "$PLAIN"
REPO_UNSET="$TMP/repo-unset"; mkdir -p "$REPO_UNSET/sub/dir"; git -C "$REPO_UNSET" init -q
REPO_SET="$TMP/repo-set"; mkdir -p "$REPO_SET/docs/agents"; git -C "$REPO_SET" init -q
: > "$REPO_SET/docs/agents/issue-tracker.md"

# context <plugin-dir> <home> <cwd>: the injected context, or nothing when the hook prints nothing.
context() {
  local out
  out=$(HOME="$2" "$1/hooks/session-start" <<< "{\"hook_event_name\":\"SessionStart\",\"source\":\"startup\",\"cwd\":\"$3\"}") \
    || fail "hook exited non-zero"
  [[ -z "$out" ]] && return 0
  python3 -c '
import json, sys
h = json.loads(sys.stdin.read())["hookSpecificOutput"]
assert h["hookEventName"] == "SessionStart", h
print(h["additionalContext"])' <<< "$out" || fail "malformed hook output: $out"
}

# The injection wraps the bootstrap body, without its frontmatter.
C=$(context "$FIX" "$MP_HOME" "$PLAIN")
[[ "$C" == "<EXTREMELY_IMPORTANT>"* && "$C" == *"</EXTREMELY_IMPORTANT>" ]] || fail "wrapper missing: $C"
[[ "$C" == *"Fixture routing policy line."* ]] || fail "bootstrap body missing: $C"
[[ "$C" != *"fixture description"* && "$C" != *"name: using-matt-pocock-skills"* ]] || fail "frontmatter leaked: $C"

# ${CLAUDE_PLUGIN_ROOT} in the body becomes the plugin's absolute path, so the injected
# bootstrap can point at its own reference files.
[[ "$C" == *"Routing details: $FIX_REAL/skills/using-matt-pocock-skills/references/routing.md"* ]] \
  || fail "plugin root not substituted: $C"
[[ "$C" != *'${CLAUDE_PLUGIN_ROOT}'* ]] || fail "placeholder left in the injection: $C"

# The MP-location line names the installed skills directory, or says MP was not found.
C=$(context "$FIX" "$MP_HOME" "$PLAIN")
[[ "$C" == *"$MP_HOME/.claude/skills"* && "$C" != *"not found"* ]] || fail "MP location line wrong for an MP home: $C"
C=$(context "$FIX" "$BARE_HOME" "$PLAIN")
[[ "$C" == *"not found"* && "$C" == *"npx skills add mattpocock/skills"* ]] || fail "MP not-found line missing for a bare home: $C"

# The repo-setup line appears only inside a git repo that lacks docs/agents/issue-tracker.md.
C=$(context "$FIX" "$MP_HOME" "$REPO_UNSET/sub/dir")
[[ "$C" == *"/setup-matt-pocock-skills"* ]] || fail "setup line missing in a repo that is not set up: $C"
C=$(context "$FIX" "$MP_HOME" "$REPO_SET")
[[ "$C" != *"/setup-matt-pocock-skills"* ]] || fail "setup line shown in a set-up repo: $C"
C=$(context "$FIX" "$MP_HOME" "$PLAIN")
[[ "$C" != *"/setup-matt-pocock-skills"* ]] || fail "setup line shown outside a git repo: $C"

# Without a cwd in the event, the hook falls back to its own working directory.
C=$(cd "$REPO_UNSET" && HOME="$MP_HOME" "$FIX/hooks/session-start" <<< '{}' \
  | python3 -c 'import json, sys; print(json.load(sys.stdin)["hookSpecificOutput"]["additionalContext"])') \
  || fail "hook failed on an event without cwd"
[[ "$C" == *"/setup-matt-pocock-skills"* ]] || fail "no fallback to the process working directory: $C"

# Fail open: bad input or a broken plugin prints nothing, on stdout or stderr, and exits 0.
OUT=$(HOME="$MP_HOME" "$FIX/hooks/session-start" <<< 'not json' 2> "$TMP/err") \
  || fail "hook exited non-zero on garbage stdin"
[[ -z "$OUT" && ! -s "$TMP/err" ]] || fail "hook was not silent on garbage stdin: $OUT $(cat "$TMP/err")"
BROKEN="$TMP/broken"; cp -R "$FIX" "$BROKEN"; rm "$BROKEN/skills/using-matt-pocock-skills/SKILL.md"
OUT=$(HOME="$MP_HOME" "$BROKEN/hooks/session-start" <<< '{}' 2> "$TMP/err") \
  || fail "hook exited non-zero without its bootstrap file"
[[ -z "$OUT" && ! -s "$TMP/err" ]] || fail "hook was not silent without its bootstrap file: $OUT $(cat "$TMP/err")"

# Guard: the real bootstrap stays within the 3,000-byte budget with both dynamic lines,
# in either MP-location variant.
for H in "$MP_HOME" "$BARE_HOME"; do
  C=$(context "$REPO/plugin" "$H" "$REPO_UNSET")
  N=$(printf '%s' "$C" | wc -c | tr -d ' ')
  (( N <= 3000 )) || fail "injection is $N bytes, over the 3,000-byte budget (HOME=$H)"
done

echo "test_plugin_hook: OK"
