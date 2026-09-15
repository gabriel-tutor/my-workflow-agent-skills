# 04: Seams owns the flow skills

**What to build:** `to-spec`, `to-tickets` and `implement` are Seams' own skills, adapted from Matt Pocock's under the MIT license, so nothing reads a user-only file at runtime. Each keeps its gate (ask before starting, ask before publishing) and its 2.1 additions, and ends with an attribution line naming the upstream skill and commit. `implement` commits the ticket's files by name before `code-review` (unrelated dirty files are listed as excluded, never staged), passes the merge-base as the fixed point with HEAD as the candidate, reports an empty diff instead of reviewing it, commits review fixes and re-runs the affected checks, and records the candidate SHA in the definition-of-done table. `THIRD_PARTY_NOTICES.md` gains a section with the three upstream files, the commit they were adapted from, and each file's SHA-256; the static test warns without failing when the installed upstream file's hash differs.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] None of the three skills instructs reading a Matt Pocock `SKILL.md`; each contains the full adapted process and template.
- [ ] `to-spec` keeps: seams from the grill written in, the four Further Notes subsections, the show-title-and-location gate before publishing.
- [ ] `to-tickets` keeps: the How to verify line; the quiz before publishing.
- [ ] `implement` has, in order: gate, `tdd` at agreed seams with typecheck as it goes and the full suite once, commit by name with exclusions listed, `code-review` from the merge-base with the empty-diff rule, fixes committed and affected checks re-run, definition of done with the candidate SHA, the four-part handover.
- [ ] Each skill's last line attributes the upstream skill, license and commit.
- [ ] The notices record upstream commit and SHA-256 for the three files; the static test compares them to the installed files and prints a warning line on drift, exit code unchanged.
- [ ] The static test's old "loads Matt Pocock's file" checks are replaced by required-heading checks for the three skills.
- [ ] `claude plugin validate --strict` passes.

**How to verify:** `scripts/test.sh`; `grep -L "SKILL.md" plugin/skills/{to-spec,to-tickets,implement}/SKILL.md` lists all three; `shasum -a 256 ~/.claude/skills/{to-spec,to-tickets,implement}/SKILL.md` matches the notices.
