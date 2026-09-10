#!/usr/bin/env bash
# Tests scripts/activate.sh against a throwaway repo layout and skills dir.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

# Throwaway repo: the script derives its repo root from its own location.
mkdir -p "$TMP/repo/scripts" "$TMP/repo/skills/matt-pocock-workflow" "$TMP/repo/skills/matt-pocock-superpowers-workflow"
cp "$REPO/scripts/activate.sh" "$TMP/repo/scripts/activate.sh"
echo "---" > "$TMP/repo/skills/matt-pocock-workflow/SKILL.md"
echo "---" > "$TMP/repo/skills/matt-pocock-superpowers-workflow/SKILL.md"
A="$TMP/repo/scripts/activate.sh"
export CLAUDE_SKILLS_DIR="$TMP/skills"
MP="$CLAUDE_SKILLS_DIR/matt-pocock-workflow"
COMBO="$CLAUDE_SKILLS_DIR/matt-pocock-superpowers-workflow"
fail() { echo "FAIL: $*" >&2; exit 1; }

# 1. activate MP -> exactly one link, pointing into the repo
"$A" matt-pocock-workflow >/dev/null
[[ -L "$MP" ]] || fail "mp link missing"
[[ "$(readlink "$MP")" == "$TMP/repo/skills/matt-pocock-workflow" ]] || fail "mp link points elsewhere: $(readlink "$MP")"
[[ ! -e "$COMBO" ]] || fail "combo should be absent"

# 2. switch -> only the other link remains
"$A" matt-pocock-superpowers-workflow >/dev/null
[[ ! -e "$MP" && ! -L "$MP" ]] || fail "mp should be unlinked"
[[ -L "$COMBO" ]] || fail "combo link missing"

# 3. status reports the active one
STATUS_OUT="$("$A" status)"
grep -q "matt-pocock-superpowers-workflow -> " <<<"$STATUS_OUT" || fail "status should show combo link"
grep -q "matt-pocock-workflow : not installed" <<<"$STATUS_OUT" || fail "status should show mp not installed"

# 4. none -> nothing left
"$A" none >/dev/null
[[ ! -e "$COMBO" && ! -L "$COMBO" ]] || fail "combo should be gone"

# 5. refuses to touch a real directory (exit 2), leaves it intact
mkdir -p "$MP"; touch "$MP/SKILL.md"
set +e; "$A" matt-pocock-superpowers-workflow >/dev/null 2>&1; rc=$?; set -e
[[ $rc -eq 2 ]] || fail "expected exit 2 for real dir, got $rc"
[[ -f "$MP/SKILL.md" ]] || fail "real dir must survive"
[[ ! -e "$COMBO" ]] || fail "must not link combo when refusing"
rm -rf "$MP"

# 6. refuses a foreign symlink (exit 2), leaves it intact
ln -s /tmp "$MP"
set +e; "$A" none >/dev/null 2>&1; rc=$?; set -e
[[ $rc -eq 2 ]] || fail "expected exit 2 for foreign link, got $rc"
[[ -L "$MP" && "$(readlink "$MP")" == "/tmp" ]] || fail "foreign link must survive"
rm "$MP"

# 7. unknown skill name -> exit 1
set +e; "$A" nope >/dev/null 2>&1; rc=$?; set -e
[[ $rc -eq 1 ]] || fail "expected exit 1 for bad arg, got $rc"

echo "test_activate: OK"
