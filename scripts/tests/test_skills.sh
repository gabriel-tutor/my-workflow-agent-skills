#!/usr/bin/env bash
# Structural checks for both skills. Content-level checks live in the benchmark.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fail() { echo "FAIL: $*" >&2; exit 1; }

check_common() {  # $1 = skill dir, $2 = max SKILL.md lines, then required reference basenames
  local dir="$1" max="$2"; shift 2
  local skill="$dir/SKILL.md"
  [[ -f "$skill" ]] || fail "$skill missing"
  local name; name="$(basename "$dir")"
  grep -q "^name: $name$" "$skill" || fail "$name: frontmatter name mismatch"
  grep -q "^description: Use " "$skill" || fail "$name: description must start with 'Use '"
  local lines; lines="$(wc -l < "$skill")"
  (( lines <= max )) || fail "$name: SKILL.md has $lines lines, budget $max"
  for ref in "$@"; do
    [[ -f "$dir/references/$ref" ]] || fail "$name: references/$ref missing"
    grep -q "references/$ref" "$skill" || fail "$name: SKILL.md never points at references/$ref"
    head -5 "$dir/references/$ref" | grep -q "Verbatim from" || fail "$name: references/$ref lacks provenance header"
  done
  # Frontmatter rules from skill-creator's quick_validate.py, re-implemented with the stdlib
  # (quick_validate needs PyYAML, which is not installed here). Keys, kebab name, description limits.
  python3 - "$skill" <<'PY' || fail "$name: frontmatter invalid"
import re, sys
text = open(sys.argv[1]).read()
m = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
assert m, "no frontmatter"
fm = {}
for line in m.group(1).splitlines():
    k, _, v = line.partition(":")
    fm[k.strip()] = v.strip()
extra = set(fm) - {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
assert not extra, f"unexpected keys {extra}"
assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm["name"]) and len(fm["name"]) <= 64, "bad name"
d = fm["description"]
assert d and "<" not in d and ">" not in d and len(d) <= 1024, f"bad description ({len(d)} chars)"
PY
}

MP="$REPO/skills/matt-pocock-workflow"
check_common "$MP" 200 skill-catalog.md workflow-rules.md examples.md
# routing table: all 20 scenario rows survive the restructure
for row in "A clear feature or behavior change" "A bug, intermittent failure, or performance regression" \
  "A vague feature in an existing project" "A clear change that fits one session" \
  "Agreed work spanning several implementation sessions" "A large effort with unresolved direction" \
  "An uncertain UI layout" "Unclear business logic, state transitions, or data shape" \
  "A module is hard to change or test" "You need to find architectural improvement candidates" \
  "Wide rename, shared type migration, or schema compatibility change" \
  "Unknown API behavior, dependency facts, or external technical decisions" \
  "Incoming bug reports, requests, or eligible external PRs" "A branch, PR, or working tree needs review" \
  "An active merge/rebase is stopped on conflicts" "Agent instructions, prompts, specs, or agent-facing docs change" \
  "A person must provision access or perform a dashboard procedure" \
  "Switching coding agents, directories, or handing work to a teammate" \
  "A stakeholder holds missing business facts" "A copy, formatting, or small static configuration edit"; do
  grep -qF "| $row |" "$MP/SKILL.md" || fail "matt-pocock-workflow: scenario row missing: $row"
done
grep -q "matt-pocock-superpowers-workflow" "$MP/SKILL.md" || fail "matt-pocock-workflow: must cross-reference the combo skill"
grep -q "Working-tree adaptation" "$MP/SKILL.md" || fail "matt-pocock-workflow: working-tree review adaptation missing"
grep -q "^## 8\. Complete skill catalog" "$MP/references/skill-catalog.md" || fail "skill-catalog.md must contain §8 verbatim"
grep -q "^## 9\. Supporting files" "$MP/references/skill-catalog.md" || fail "skill-catalog.md must contain §9 verbatim"
grep -q "^## 11\. Scan coverage" "$MP/references/skill-catalog.md" || fail "skill-catalog.md must contain §11 verbatim"
grep -q "^## 6\. Apply the important workflow rules" "$MP/references/workflow-rules.md" || fail "workflow-rules.md must contain §6 verbatim"
grep -q "^## 10\. Practical examples" "$MP/references/examples.md" || fail "examples.md must contain §10 verbatim"

COMBO="$REPO/skills/matt-pocock-superpowers-workflow"
for pair in "conflict-rules.md:^## 4\. Explicit conflict-resolution rules" \
            "development-loop.md:^## 6\. Run the development loop" \
            "coordination.md:^## 7\. Agent coordination without duplicate work" \
            "quality-gates.md:^## 8\. Quality gates" \
            "skill-catalog.md:^## 9\. All 14 Superpowers skills" \
            "skill-catalog.md:^## 10\. Where all 37 Matt Pocock skills fit" \
            "skill-catalog.md:^## 11\. Reference files to load on demand" \
            "skill-catalog.md:^## Installed-version notes" \
            "adoption-scenarios.md:^## 12\. Verify adoption"; do
  f="${pair%%:*}"; pat="${pair#*:}"
  [[ -f "$COMBO/references/$f" ]] || fail "combo: references/$f missing"
  grep -q "$pat" "$COMBO/references/$f" || fail "combo: references/$f lacks section matching: $pat"
done
grep -q "^## 13\." "$COMBO/references/adoption-scenarios.md" && fail "combo: adoption-scenarios.md must stop before §13"

check_common "$COMBO" 250 conflict-rules.md development-loop.md coordination.md quality-gates.md skill-catalog.md adoption-scenarios.md
# ownership table: all 15 stages
for stage in "Startup and skill selection" "Requirements and design" "Long-range decision planning" \
  "Durable spec and issue breakdown" "Executable implementation plan" "Workspace isolation" \
  "Multi-task execution" "Production TDD" "Ordinary debugging" \
  "Difficult reproduction, concurrency, or performance diagnosis" "Task and final review" \
  "Feedback evaluation" "Completion claim" "Integration and branch handling" "Agent-facing documentation"; do
  grep -qF "| $stage |" "$COMBO/SKILL.md" || fail "combo: ownership row missing: $stage"
done
# 12 numbered conflict rules
for n in 1 2 3 4 5 6 7 8 9 10 11 12; do
  grep -qE "^$n\. \*\*" "$COMBO/SKILL.md" || fail "combo: conflict rule $n missing"
done
# process-sizing rows
for wt in "Human-facing copy, formatting, or static cosmetic change" "Small behavior change in an existing flow" \
  "New feature or subsystem" "Bug" "Authorization, billing, data migration, shared concurrency, or operationally sensitive change" "Throwaway prototype"; do
  grep -qF "| $wt |" "$COMBO/SKILL.md" || fail "combo: process-sizing row missing: $wt"
done
# the eight loop stages and the two disclosure rules
for s in "A. Task contract" "B. Design" "C. Plan" "D. Workspace" "E. Implement one slice" "F. Diagnose" "G. Review" "H. Verify"; do
  grep -qF "**$s" "$COMBO/SKILL.md" || fail "combo: loop stage missing: $s"
done
grep -q "reference consulted" "$COMBO/SKILL.md" || fail "combo: 'reference consulted' rule missing"
grep -q "review was not independent" "$COMBO/SKILL.md" || fail "combo: non-independent review disclosure missing"
grep -q "matt-pocock-workflow" "$COMBO/SKILL.md" || fail "combo: must cross-reference the MP-only skill"
grep -q "using-superpowers" "$COMBO/SKILL.md" || fail "combo: must name the bootstrap owner"

echo "test_skills: OK"
