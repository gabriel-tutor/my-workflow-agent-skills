# 03: Session-start knows what's installed

**What to build:** The startup hook tells the truth about the machine it runs on. It resolves the Claude config directory from `CLAUDE_CONFIG_DIR`, else `~/.claude`; checks every required Matt Pocock skill (grilling, domain-modeling, tdd, diagnosing-bugs, code-review, codebase-design, setup-matt-pocock-skills, setup-pre-commit, setup-ts-deep-modules) and, when any is missing, lists the missing names with the install command instead of reporting "installed" from one sentinel file. The "This session" section otherwise stays as it is (the setup nudge when the repo has no issue-tracker config).

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] With `CLAUDE_CONFIG_DIR` set to a directory holding the skills, the section reports them installed; with the directory containing spaces, the same.
- [ ] With a partial install (grilling present, tdd missing), the section names `tdd` as missing and gives the install command.
- [ ] With no install, the section says so with the install command.
- [ ] Symlinked skill directories are accepted.
- [ ] The injected bootstrap stays within the byte budget in every case above.
- [ ] Hook-suite cases for each, wired into `scripts/test.sh`.

**How to verify:** `scripts/test.sh` (the hook suite covers the fixture homes); then start a real session and confirm the "This session" section lists no missing skills on this machine.
