#!/usr/bin/env bash
# Static checks on the plugin: manifests validate, skills are well-formed and model-invocable,
# and the copied Superpowers skills are byte-identical to what THIRD_PARTY_NOTICES.md records.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PLUGIN="$REPO/plugin"
fail() { echo "FAIL: $*" >&2; exit 1; }

claude plugin validate --strict "$PLUGIN" >/dev/null || fail "plugin manifest does not validate"
claude plugin validate --strict "$REPO" >/dev/null || fail "marketplace manifest does not validate"

# Every skill: frontmatter naming its own directory, a description, and model invocation left on.
for f in "$PLUGIN"/skills/*/SKILL.md; do
  python3 - "$f" <<'PY' || fail "bad frontmatter: $f"
import pathlib, sys
p = pathlib.Path(sys.argv[1])
text = p.read_text()
assert text.startswith("---\n"), "no frontmatter"
head = text[4:text.index("\n---\n", 4)]
fields = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in head.splitlines() if ":" in l)}
assert fields.get("name") == p.parent.name, f"name {fields.get('name')!r} != directory {p.parent.name!r}"
assert fields.get("description"), "empty description"
assert fields.get("disable-model-invocation", "false") != "true", "user-only skill"
PY
done

# Pointer skills: each loads its own Matt Pocock skill file and stops when his skills are missing.
# A static guard: checking this headless would mean running Claude under a fixture HOME.
for s in to-spec to-tickets implement; do
  f="$PLUGIN/skills/$s/SKILL.md"
  grep -q "\`$s/SKILL.md\`" "$f" || fail "$s does not load Matt Pocock's $s/SKILL.md"
  grep -q "aren't installed" "$f" || fail "$s has no stop for a missing Matt Pocock install"
done

# The four kept Superpowers skills: present, and matching the checksums recorded in the notices.
KEPT="using-git-worktrees verification-before-completion finishing-a-development-branch receiving-code-review"
for s in $KEPT; do [[ -f "$PLUGIN/skills/$s/SKILL.md" ]] || fail "missing copied skill: $s"; done
SUMS=$(grep -E '^[0-9a-f]{64}  skills/[a-z-]+/SKILL\.md$' "$PLUGIN/THIRD_PARTY_NOTICES.md") \
  || fail "no checksums in THIRD_PARTY_NOTICES.md"
[[ $(wc -l <<< "$SUMS") -eq 4 ]] || fail "expected 4 recorded checksums, got: $SUMS"
(cd "$PLUGIN" && shasum -a 256 -c <<< "$SUMS" >/dev/null) || fail "a copied skill differs from its recorded checksum"

# ...and identical to the Superpowers 6.3.0 originals whenever that cache is present.
SP="$HOME/.claude/plugins/cache/claude-plugins-official/superpowers/6.3.0/skills"
if [[ -d "$SP" ]]; then
  for s in $KEPT; do
    cmp -s "$SP/$s/SKILL.md" "$PLUGIN/skills/$s/SKILL.md" || fail "$s differs from Superpowers 6.3.0"
  done
fi

echo "test_plugin: OK"
