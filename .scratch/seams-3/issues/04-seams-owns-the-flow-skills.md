# 04: Seams owns the flow skills

**What to build:** `to-spec`, `to-tickets` and `implement` are Seams' own skills, adapted from Matt Pocock's under the MIT license, so nothing reads a user-only file at runtime. Each keeps its gate (ask before starting, ask before publishing) and its 2.1 additions, and ends with an attribution line naming the upstream skill and commit. `implement` commits the ticket's files by name before `code-review` (unrelated dirty files are listed as excluded, never staged), passes the merge-base as the fixed point with HEAD as the candidate, reports an empty diff instead of reviewing it, commits review fixes and re-runs the affected checks, and records the candidate SHA in the definition-of-done table. `THIRD_PARTY_NOTICES.md` gains a section with the three upstream files, the commit they were adapted from, and each file's SHA-256; the static test warns without failing when the installed upstream file's hash differs.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] None of the three skills instructs reading a Matt Pocock `SKILL.md`; each contains the full adapted process and template.
- [x] `to-spec` keeps: seams from the grill written in, the four Further Notes subsections, the show-title-and-location gate before publishing.
- [x] `to-tickets` keeps: the How to verify line; the quiz before publishing.
- [x] `implement` has, in order: gate, `tdd` at agreed seams with typecheck as it goes and the full suite once, commit by name with exclusions listed, `code-review` from the merge-base with the empty-diff rule, fixes committed and affected checks re-run, definition of done with the candidate SHA, the four-part handover.
- [x] Each skill's last line attributes the upstream skill, license and commit.
- [x] The notices record upstream commit and SHA-256 for the three files; the static test compares them to the installed files and prints a warning line on drift, exit code unchanged.
- [x] The static test's old "loads Matt Pocock's file" checks are replaced by required-heading checks for the three skills.
- [x] `claude plugin validate --strict` passes.

**How to verify:** `scripts/test.sh`; `grep -L "SKILL.md" plugin/skills/{to-spec,to-tickets,implement}/SKILL.md` lists all three; `shasum -a 256 ~/.claude/skills/{to-spec,to-tickets,implement}/SKILL.md` matches the notices.

## Comments

Done in `3385667` and its review-fix commit. Evidence: `scripts/test.sh` 8/8 suites; the ticket's three verify lines (`grep -L` lists all three skills; the installed files' SHA-256 equal the notices; `claude plugin validate --strict` inside `test_plugin.sh`). The upstream commit `3cca18b` was taken from the skills-manager record and checked against its clone: the three files at that commit hash to the installed copies.

Review found and fixed: under `set -euo pipefail` the static test's `fail` messages were lost on the failure path (a `$(grep … | …)` assignment exits first); `implement` had grown a step writing "status done" to the ticket after the candidate (dropped: not asked for, `done` is not a triage label, and the extra commit would move HEAD past the reviewed candidate); "gate" in the consent-question sense conflicted with the glossary's hook-only definition (the glossary now records both senses; the skills use "block" for ticket edges); the README's install step 4 now states exactly what the installer does today.

Decisions the ticket left open: on the base branch the review's fixed point is the commit `implement` started from, since the merge-base would be HEAD; `to-tickets` gained a gate question that is skipped when the user asked for tickets or said yes to `to-spec`'s offer. Left to their tickets: the installer half of ADR-0002 (08), the handover naming the stage (05).
