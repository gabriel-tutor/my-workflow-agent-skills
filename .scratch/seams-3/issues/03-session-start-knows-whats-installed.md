# 03: Session-start knows what's installed

**What to build:** The startup hook tells the truth about the machine it runs on. It resolves the Claude config directory from `CLAUDE_CONFIG_DIR`, else `~/.claude`; checks every required Matt Pocock skill (grilling, domain-modeling, tdd, diagnosing-bugs, code-review, codebase-design, setup-matt-pocock-skills, setup-pre-commit, setup-ts-deep-modules) and, when any is missing, lists the missing names with the install command instead of reporting "installed" from one sentinel file. The "This session" section otherwise stays as it is (the setup nudge when the repo has no issue-tracker config).

**Blocked by:** 01

**Status:** done

- [x] With `CLAUDE_CONFIG_DIR` set to a directory holding the skills, the section reports them installed; with the directory containing spaces, the same.
- [x] With a partial install (grilling present, tdd missing), the section names `tdd` as missing and gives the install command.
- [x] With no install, the section says so with the install command.
- [x] Symlinked skill directories are accepted.
- [x] The injected bootstrap stays within the byte budget in every case above.
- [x] Hook-suite cases for each, wired into `scripts/test.sh`.

**How to verify:** `scripts/test.sh` (the hook suite covers the fixture homes); then start a real session and confirm the "This session" section lists no missing skills on this machine.

## Comments

Done in `fd311a1` and its review-fix commit. Evidence: `scripts/test.sh` 9/9 suites (the session-start suite now runs under the system Python 3.9 as well as the default `python3`). Hook-suite fixtures: a full home, a partial home (grilling alone: eight names listed), a bare home, a `CLAUDE_CONFIG_DIR` with spaces, per-skill symlinks the way skills.sh installs, and a symlinked skills directory; the budget guard runs over all six (2,762–2,977 bytes at the suite's long temp paths). On this machine the section lists no missing skills, and the injection is 2,619 bytes at the cache-length plugin path (2,845 before).

Decisions the ticket left open: the "not installed" line names the directory the hook looked in (a wrong directory was the defect); a partial install lists every missing name, so eight names is the worst case; a broken symlink counts as missing (Claude Code cannot load it either). A line naming skills and the install command could not fit the 3,000-byte budget beside the 2.x body (2,978 with the setup nudge at a cache-length path before any such line), so one item of ticket 07 with no dependency on the rest landed here: the Superpowers-overlap sentence moved from the bootstrap to `routing.md` ("Alongside Superpowers", plus one sentence saying the gate enforces it, since a Superpowers skill is not a declaration); rule 5 points there; the static test guards both directions. Nothing else of 07 came along.

Review found and fixed: the full-home assertion accepted a "missing" line; the symlinked-directory home was outside the budget loop; `context()` duplicated its invocation; the required-skills comment enumerated an incomplete set of the unchecked skills (it now states the criterion); `INSTALL` named a sentence; `scripts/test.sh` never ran this suite under the system 3.9. Not acted on, with the reason: the budget at a cache-length path is ticket 07's criterion and fails today on the partial fixture (numbers in 07's comments); the install command's wording versus what `install.sh` runs is ticket 08's.
