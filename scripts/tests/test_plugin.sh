#!/usr/bin/env bash
# Static checks on the plugin: manifests validate, skills are well-formed and model-invocable,
# the three adapted flow skills carry their required sections and attribution, the upstream files
# they came from are compared with the installed ones (a warning on drift), and the copied
# Superpowers skills are byte-identical to what THIRD_PARTY_NOTICES.md records.
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

# The three flow skills are Seams' own adaptations of Matt Pocock's (ADR-0002): self-contained, so
# none names a SKILL.md to read at runtime; the sections the ticket requires, in order; the wording
# each must keep; and a last line attributing the upstream skill, the MIT license and the commit
# recorded in the notices.
NOTICES="$PLUGIN/THIRD_PARTY_NOTICES.md"
MP_SECTION=$(awk '/^## Matt Pocock/{p=1; next} /^## /{p=0} p' "$NOTICES")
[[ -n "$MP_SECTION" ]] || fail "no 'Matt Pocock' section in THIRD_PARTY_NOTICES.md"
MP_COMMIT=$(grep -oE '\b[0-9a-f]{40}\b' <<< "$MP_SECTION" | sort -u)
[[ $(wc -l <<< "$MP_COMMIT") -eq 1 ]] || fail "the notices should name one upstream commit, got: $MP_COMMIT"
for s in to-spec to-tickets implement; do
  f="$PLUGIN/skills/$s/SKILL.md"
  grep -q 'SKILL\.md' "$f" && fail "$s still names a SKILL.md file to read"
  case $s in
    to-spec)    headings="## Gate|## Process|## Spec template|## Next"
                needles="grill|Alternatives considered|Risks and failure modes|Rollout and migration|Observability|title|ready-for-agent" ;;
    to-tickets) headings="## Gate|## Process|## Ticket templates|## Next"
                needles="How to verify|Blocked by|granularity|ready-for-agent" ;;
    implement)  headings="## Gate|## Build|## Commit|## Review|## Review fixes|## Definition of done|## Handover"
                needles="tdd|by name|excluded|merge-base|empty|code-review|verification-before-completion|Run it|Try it|What changed|Next" ;;
  esac
  prev=0
  while IFS= read -r h; do
    n=$(grep -nxF "$h" "$f" | head -1 | cut -d: -f1)
    [[ -n $n ]] || fail "$s lacks the heading: $h"
    (( n > prev )) || fail "$s: heading out of order: $h"
    prev=$n
  done <<< "$(tr '|' '\n' <<< "$headings")"
  while IFS= read -r needle; do
    grep -q -- "$needle" "$f" || fail "$s should mention: $needle"
  done <<< "$(tr '|' '\n' <<< "$needles")"
  last=$(grep -v '^[[:space:]]*$' "$f" | tail -1)
  [[ $last == *"Matt Pocock"* && $last == *"MIT"* && $last == *"$MP_COMMIT"* ]] \
    || fail "$s: the last line does not attribute the upstream skill, license and commit: $last"
done

# The upstream files those three were adapted from: SHA-256 recorded at the upstream commit and
# compared with the installed copies. Drift is a warning, never a failure: the port is a manual
# review (ADR-0002), and a machine without his skills has nothing to compare.
MP_SUMS=$(grep -E '^[0-9a-f]{64}  skills/engineering/[a-z-]+/SKILL\.md$' <<< "$MP_SECTION") \
  || fail "no upstream checksums in the Matt Pocock section of THIRD_PARTY_NOTICES.md"
[[ $(wc -l <<< "$MP_SUMS") -eq 3 ]] || fail "expected 3 recorded upstream checksums, got: $MP_SUMS"
upstream_drift() {   # $1 = the Claude config directory; prints WARN lines, exit status always 0
  local skills="$1/skills" sum path name have
  while read -r sum path; do
    name=$(basename "$(dirname "$path")")
    if [[ ! -f "$skills/$name/SKILL.md" ]]; then echo "note: $skills/$name/SKILL.md is not installed; drift not checked"; continue; fi
    have=$(shasum -a 256 "$skills/$name/SKILL.md" | cut -d' ' -f1)
    [[ $have == "$sum" ]] || echo "WARN: installed $name/SKILL.md differs from the hash recorded in THIRD_PARTY_NOTICES.md" \
      "(Matt Pocock's $name has moved on since commit ${MP_COMMIT:0:7}; review the port)"
  done <<< "$MP_SUMS"
  return 0
}
upstream_drift "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
FIX=$(mktemp -d); mkdir -p "$FIX/skills/to-spec"; echo "a newer upstream to-spec" > "$FIX/skills/to-spec/SKILL.md"
DRIFT=$(upstream_drift "$FIX"); rm -rf "$FIX"
[[ $DRIFT == *"WARN: installed to-spec/SKILL.md differs"* ]] || fail "the drift check did not warn on a changed upstream file: $DRIFT"
[[ $DRIFT == *"note: $FIX/skills/implement/SKILL.md is not installed"* ]] || fail "the drift check did not note a missing upstream file: $DRIFT"

# The grill's design lens: present, and referenced from the grill.
[[ -f "$PLUGIN/skills/grill/references/design-lens.md" ]] || fail "design-lens.md missing"
grep -q "references/design-lens.md" "$PLUGIN/skills/grill/SKILL.md" || fail "grill does not reference the design lens"
[[ $(grep -cE '^[0-9]+\. \*\*' "$PLUGIN/skills/grill/references/design-lens.md") -eq 10 ]] || fail "design lens should list 10 axes"

# The trivial declaration: the cheap way through the gate, carrying the test of what is not trivial.
TRIV="$PLUGIN/skills/trivial/SKILL.md"
[[ -f "$TRIV" ]] || fail "trivial skill missing"
for needle in "behavior" "data" "auth" "migration" "verification-before-completion" "grill" "diagnosing-bugs"; do
  grep -qi "$needle" "$TRIV" || fail "trivial skill should mention: $needle"
done

# The four kept Superpowers skills: present, and matching the checksums recorded in the notices.
KEPT="using-git-worktrees verification-before-completion finishing-a-development-branch receiving-code-review"
for s in $KEPT; do [[ -f "$PLUGIN/skills/$s/SKILL.md" ]] || fail "missing copied skill: $s"; done
SP_SECTION=$(awk '/^## Superpowers/{p=1; next} /^## /{p=0} p' "$NOTICES")
SUMS=$(grep -E '^[0-9a-f]{64}  skills/[a-z-]+/SKILL\.md$' <<< "$SP_SECTION") \
  || fail "no checksums in the Superpowers section of THIRD_PARTY_NOTICES.md"
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
