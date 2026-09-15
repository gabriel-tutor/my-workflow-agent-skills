# Seams 3.0: an enforced workflow from a request to production

**Status:** ready-for-agent

## Problem Statement

Seams 2.1 routes every development request to the right skill and runs a senior engineer's process from design to a merged ticket, but the routing is a promise the model keeps rather than one the plugin keeps: nothing stops an edit that skipped the workflow, and nothing stops a "done" that skipped verification. The workflow also ends at the merge; getting a candidate to production, proving it is what runs, and operating it are left to the user. An outside review (2026-09-15) confirmed five defects on top of that: the review step can miss the implementation it reviews, the flow wrappers follow user-only skills by reading their files, the startup hook ignores a custom config directory, the installer's test passes only on macOS and the installer hides failed commands, and the routing harness scores a shell write as exploration. A sixth was found while closing the foundations gaps: under macOS's system Python 3.9 the hook crashes on import and, because it fails open, a machine without a newer Python first on PATH gets no bootstrap at all, silently.

## Solution

Seams 3.0 enforces the workflow with hooks: a change to the project is refused, with a reason that names the fix, until a workflow skill has been declared for the current request; a turn that changed the project cannot end until verification has run. It owns adapted copies of the three flow skills so nothing user-only is followed indirectly, and its `implement` commits before it reviews so the review sees the candidate. It carries work past the merge with a `release` skill (readiness, deploy on an explicit yes, verification of the running candidate, operations handover), an `incident` route (contain before diagnose), production rows in `foundations`, and a walking skeleton as the first ticket of any new app. Every handover names the stage reached, so "done" never implies "in production". The bootstrap routes by risk as well as size, reuses a yes that covered later steps, and stays under 3,000 bytes. The hook, the installer and the harness are corrected, everything runs on Python 3.9, and the deterministic parts are proven by tests on macOS and Ubuntu while the live parts are measured headless and reported as counts.

## User Stories

1. As a developer, I want every change to my project to go through the workflow, so that no edit lands without the skill that should have governed it.
2. As a developer, I want a refusal to tell Claude exactly what to do next, so that a refused edit costs one skill invocation and never a stalled session.
3. As a developer, I want trivial edits to stay cheap, so that fixing a typo costs one declaration and one check, not a design interview.
4. As a developer, I want the trivial declaration to carry the test of what is not trivial, so that a one-line change to auth or a migration is routed up instead of slipped through.
5. As a developer, I want changes made through shell commands to be gated the same way as editor changes, so that "use sed instead" is not a way around the workflow.
6. As a developer, I want changes in a git worktree to be gated too, so that isolating work does not un-gate it.
7. As a developer, I want throwaway files in the temp directory and my Claude config directory left ungated, so that analysis scripts and memory notes never trigger a refusal.
8. As a developer, I want a subagent's edits gated by the same session ledger, so that delegating work is not a way around the workflow.
9. As a developer, I want a turn that changed non-documentation files to end only after verification ran, so that "done" always comes with evidence.
10. As a developer, I want the done-check to fire at most once per turn, so that a turn that legitimately ends with a question to me is delayed by one message, never trapped.
11. As a developer, I want a yes such as "go ahead" or "continue" to keep the current declaration, so that answering Claude's question does not force a re-declaration.
12. As a developer, I want a new request to need a new declaration, so that a skill invoked for feature A does not silently cover bug B.
13. As a developer, I want a slash command I type to count as a declaration, so that `/to-spec` or `/wayfinder` opens the gate without a second invocation.
14. As a developer, I want a hook that fails on its own bug to let my work through and say so in the debug log, so that a plugin defect never locks me out of my project.
15. As a developer, I want the only off switch to be disabling the plugin, so that "always" is not undermined by an environment variable.
16. As a developer, I want the ledger to hold only skill names, tool names and paths, so that no command text or prompt text with a secret in it is written to disk.
17. As a developer, I want the ledger to survive compaction and resume, so that a long ticket does not lose its declaration mid-way.
18. As a developer, I want `/clear` and a new session to start with an empty ledger, so that the first action of a fresh context is a route.
19. As a developer, I want Seams' spec, tickets and implement skills to be its own, so that nothing follows a user-only skill by reading its file.
20. As a developer, I want each of those skills to still ask before it starts and before it publishes, so that Claude never writes a spec or thirty tickets on its own initiative.
21. As a developer, I want a test that reports when Matt Pocock's upstream versions of those three skills change, so that a port is a deliberate review rather than a surprise.
22. As a developer, I want the review to cover the work it is reviewing, so that a review never certifies an empty or partial diff.
23. As a developer, I want `implement` to stage only the ticket's files and to list unrelated dirty files as excluded, so that my other work is neither swept into the commit nor silently ignored.
24. As a developer, I want an empty diff reported as "nothing to review", so that no sub-agents are spawned to review nothing.
25. As a developer, I want the definition of done to name the candidate commit its evidence refers to, so that a later change visibly invalidates it.
26. As a developer, I want the handover's Next section to name the stage reached, so that I know whether the work is built, integrated, release-ready, deployed or operated.
27. As a developer, I want a `release` skill that takes an integrated candidate to production, so that the workflow does not stop at the merge.
28. As a developer, I want release readiness reported as a table with anything unmet blocking, so that I never deploy a candidate whose checks are red.
29. As a developer, I want every deploy to require my explicit yes naming the target, the environment and the candidate, so that no earlier approval is ever stretched into a deployment.
30. As a developer, I want a staged environment used first when the target has one, so that production is never the first place a candidate runs.
31. As a developer, I want the running version checked against the candidate after a deploy, so that "deployed" means the exact commit is what runs.
32. As a developer, I want the critical journeys smoke-tested after a deploy and the abort path executed if they fail, so that a bad release is reverted rather than reported.
33. As a developer, I want a data migration planned expand–contract with a rehearsed restore when there is persistent data, so that a rollback never means data loss discovered later.
34. As a developer, I want the release to scale to the target (web host, container, mobile store, CLI package, browser extension, desktop), so that a Chrome extension is not asked for a canary and a VPS is not asked for a store listing.
35. As a developer, I want an operations handover naming monitoring, the alert owner, the runbook and the follow-ups, so that what I own after the release is written down.
36. As a developer, I want an `incident` route that contains and restores before it diagnoses, so that users stop being affected before the root cause is known.
37. As a developer, I want the incident's fix to go through the normal route with a regression test, and a post-mortem note written, so that the failure becomes coverage and a record.
38. As a developer, I want `foundations` to survey how code reaches production, environments and config, backups and restore, monitoring and alerts, and dependency and secret scanning, so that the production gaps are named as early as the lint gap.
39. As a developer starting a new app, I want the first ticket to be a walking skeleton through build, CI, deploy and a smoke check, so that every feature ticket ships on a pipeline that already works.
40. As a developer, I want the spec to carry a Release section when the work ships somewhere, so that the target and the first deploy are decided before the tickets exist.
41. As a developer, I want tickets to carry the negative cases the design lens raised as acceptance criteria, so that "access denied for another tenant" is tested, not assumed.
42. As a developer, I want a sensitive change routed to a grill with the security and failure axes and a required review, whatever its size, so that a one-line permissions change gets the scrutiny it deserves.
43. As a developer, I want a yes that covered later steps not asked again, so that "go all the way through the tickets" is honored.
44. As a developer, I want the grill to skip questions the code or my earlier answers already settle, so that a short change gets a short grill.
45. As a developer, I want the phase-boundary rule to be a judgment rule rather than a token count, so that it holds on any model and any context size.
46. As a developer, I want the durable state named (spec, tickets, glossary, ADRs), so that a ticket resumed in a fresh context reads them and never relies on chat memory.
47. As a developer, I want an unchanged candidate's suite not re-run for a second skill, so that two skills asking for evidence share one run.
48. As a developer on a second machine, I want the hook to honor `CLAUDE_CONFIG_DIR`, so that a custom config directory does not report Matt Pocock's skills as missing.
49. As a developer on a second machine, I want the hook to check every required skill and list the missing ones by name, so that a partial install is reported as what it is.
50. As a developer on a second machine, I want the hooks and the harness to run on Python 3.9, so that macOS's system Python does not silently disable the plugin.
51. As a developer on a second machine, I want the installer to stop with a message when a `claude plugin` command fails, so that a half-installed plugin is never reported as installed.
52. As a developer on a second machine, I want the installer to leave settings.json alone, so that installing Seams changes nothing but the plugin list.
53. As a developer on a second machine, I want the README to state which operating systems, Python versions and Claude Code versions were tested, so that "any machine" is a claim with a scope.
54. As a maintainer, I want the routing harness to score a shell write as a change and to record failed calls, timeouts and exit codes, so that its tables describe what happened.
55. As a maintainer, I want the harness to exit non-zero when a scenario's expectation is violated, so that it can serve as a check rather than a printout.
56. As a maintainer, I want the shell-command classifier shared between the gate and the harness, so that they cannot disagree about what a write is.
57. As a maintainer, I want the gate's logic unit-tested and each hook tested by piping JSON, so that refusals are proven, not only measured.
58. As a maintainer, I want the bootstrap's byte budget checked with a long plugin path, so that a cache install never pushes it past the limit.
59. As a maintainer, I want the test suites to run on macOS and Ubuntu in CI on every push, so that platform-dependent tests are caught before users are.
60. As a reader of the README, I want a plain account of what is evidenced, how it was measured, and what is not evidenced, so that I can decide whether to install with my eyes open.
61. As a reader of the README, I want to know what a refusal looks like and how to turn the gate off, so that the first refusal is expected rather than alarming.
62. As a user with Superpowers enabled alongside, I want Superpowers' process skills not to open the gate, so that Matt Pocock's skills lead as the README promises.
63. As a user of the 2.x plugin, I want the plugin id and marketplace name unchanged, so that `claude plugin update` is the whole upgrade.

## Implementation Decisions

### The gate and the done-check

- The plugin's `hooks.json` registers: PreToolUse for `Edit|Write|MultiEdit|NotebookEdit|Bash`; PostToolUse for `Skill`; UserPromptSubmit; Stop; and SessionStart for `startup|clear|compact` (bootstrap injection as today, plus ledger housekeeping).
- All hooks are Python 3.9-compatible executables that share one pure module (the *gate module*) holding the classification, the decision and the ledger format; the harness imports the same module.
- The **ledger** is one JSON file per session under the system temp directory (`TMPDIR`, else `/tmp`) in a Seams subdirectory, user-only permissions, written atomically. It records the current request: when it started, its declarations (skill name, time, subagent id if any), its changes (tool name, path or a classification label, time), and when verification last ran. It never stores command text or prompt text. `startup` and `clear` reset it; `compact` and `resume` keep it; files older than seven days are removed at session start.
- A **declaration** is recorded by PostToolUse on `Skill` (so a failed invocation does not count) when the skill is a Seams skill (`matt-pocock-workflow:` prefix) or one of Matt Pocock's process skills by bare name (the grill family, `domain-modeling`, `tdd`, `diagnosing-bugs`, `code-review`, `codebase-design`, `prototype`, `resolving-merge-conflicts`, `research`, `wizard`, the `setup-*` skills, `wayfinder`, `triage`, `improve-codebase-architecture`, `handoff`, `ask-matt`, `implement`, `to-spec`, `to-tickets`). Superpowers' and other plugins' skills do not count. A typed slash command naming one of those skills, seen by UserPromptSubmit, counts too.
- UserPromptSubmit starts a **new request** (clearing declarations, changes and verification) unless the prompt is a short continuation: at most 40 characters and matching a fixed list of go-ahead words (yes, ok, go ahead, continue, proceed, next, approved, do it, and their close variants) or a bare option letter or number. Answers given through AskUserQuestion never pass through this hook and never start a new request.
- PreToolUse **refuses** (permission decision `deny`, with a reason) a *project change* when the request has no declaration. A project change is: any `Edit`, `Write`, `MultiEdit` or `NotebookEdit` whose path is under the session's working directory, or is not under the system temp directory or the Claude config directory (so a repo checked out under the temp dir is still gated, and a worktree outside the working directory is too); or a `Bash` command the classifier labels as a mutation. Nothing else is refused. Subagent calls carry the parent session's id and follow the same rule. The refusal reason names the classification, says no skill has been declared for this request, and lists the routes: `diagnosing-bugs` for something broken, `matt-pocock-workflow:grill` for a change to behavior, `tdd` or `matt-pocock-workflow:implement` to keep building an agreed design, `matt-pocock-workflow:trivial` for a change with no effect on behavior, data shape or security.
- The **classifier** labels a shell command a mutation when, after quoted strings are stripped, any segment (split on `;`, `&&`, `||`, `|`) has: a redirection to a path other than `/dev/null`; a file-changing command (`rm`, `mv`, `cp`, `touch`, `mkdir`, `rmdir`, `ln`, `chmod`, `chown`, `truncate`, `tee`, `install`, `dd`, `patch`, `sed`/`perl`/`ruby` with an in-place flag, `find` with `-delete` or `-exec rm`, `xargs rm`); a git tree- or history-changing subcommand (`add`, `commit`, `rm`, `mv`, `checkout`, `switch`, `restore`, `reset`, `rebase`, `merge`, `cherry-pick`, `revert`, `stash`, `apply`, `am`, `clean`, `push`, `pull`, `tag`, `branch -d/-D/-m`, `worktree add/remove`); a package manager adding or removing dependencies (`npm`/`pnpm`/`yarn`/`bun` install, add, remove, uninstall, update, link, init, create; `pip`/`uv`/`poetry`/`cargo`/`go get`/`gem` equivalents); a formatter or linter write flag (`--write`, `--fix`, `-w`); a download with an output flag; or an inline interpreter program (`python -c`, `python -`, `node -e`, `ruby -e`, `perl -e`) whose text opens a file for writing, writes text, removes, renames or copies. Everything else, including builds, tests, typechecks and `git status/log/diff/show`, is not a mutation. The label is the reason shown in a refusal. This is a documented best-effort mesh.
- PreToolUse records every allowed project change in the ledger (path for editor tools; the label for shell mutations). Markdown files are recorded but marked as documentation.
- Stop **blocks once** (with a reason) when the request has at least one change that needs verification (a non-documentation project change; VCS operations such as a commit after the checks do not) after its last verification and the input's `stop_hook_active` is false. Verification is a declaration of `matt-pocock-workflow:verification-before-completion` (or Superpowers' copy, when that is what ran). The reason names the count and one example path, says to run the verification skill and show the real output, and says the check does not repeat in this turn.
- Every hook fails open: any exception prints nothing, exits 0, and writes the traceback to stderr for the debug log.

### Seams-owned flow skills

- `to-spec`, `to-tickets` and `implement` become Seams skills adapted from Matt Pocock's (MIT). Each ends with an attribution line; `THIRD_PARTY_NOTICES.md` gains a section naming the three upstream files, the upstream commit they were adapted from, and each upstream file's SHA-256. The static test warns, without failing, when an installed upstream file's hash differs from the recorded one.
- `to-spec` keeps its gate, the seams-from-the-grill rule, the four Further Notes subsections, and adds a **Release** subsection (target, environments, what the first deploy is) when the work ships anywhere.
- `to-tickets` keeps the verify line, and adds: the walking skeleton is ticket 01 for a new app; the negative cases the lens raised become acceptance criteria; when the spec's Release section says the work ships, the last ticket takes the integrated work through `release`.
- `implement`: gate (which ticket, worktree or branch) → `tdd` at the agreed seams, typecheck as it goes, the full suite once at the end → **commit** the ticket's files (staged by name; unrelated dirty files listed as excluded, never staged) → `code-review` with the merge-base as the fixed point, the candidate being HEAD; an empty diff is reported, not reviewed → fixes committed and the affected checks re-run → definition of done, with the candidate SHA and the commands' output → handover in four sections, Next naming the stage reached.

### New skills

- `trivial`: the declaration for a trivial change. Its body is the test (no behavior change a test could detect, no data or config shape change, nothing on the sensitive list, reversible in one commit), then: edit, run the narrowest check that proves it, verify before claiming done; if any condition fails, route up.
- `release`: gate (candidate, target, environment) → readiness table (integrated candidate; suite green on that SHA; artifact built with the repo's build and identified; config and environment variable names per environment; migration and restore plan when data changes shape; abort conditions and rollback path; applicable checks: dependency audit, secret scan, accessibility for a UI, load when the lens flagged scale; smoke plan) with anything unmet blocking → deploy only after an explicit yes naming target, environment and candidate, staged environment first when one exists, through the platform's own skill or CLI → verify (running version equals the candidate; smoke journeys; a short watch; abort path on failure) → operations handover (monitoring and alert owner, runbook, follow-ups, stage reached). A target table scales the steps: web host, container or VPS, mobile store, CLI or library registry, browser extension store, desktop; store uploads that only a person can do are handed to the user.
- `incident`: impact (who, since when, what changed last) → contain with the safest reversible action, asking before any outward action → restore and confirm → `diagnosing-bugs` → fix through the normal route with a regression test first → post-mortem note under `docs/incidents/` and follow-up tickets → handover with the stage reached.

### Bootstrap and references

- The routing table gains: Trivial → `trivial`*; Sensitive (auth, permissions, secrets, billing, migrations, infrastructure/CI/deploy config, public API, destructive operations; any size) → `grill`* with the security and failure axes, then `tdd`, `code-review` required; Down or degraded for users now → `incident`*; Several sessions or a new app → grill, `to-spec`*, `to-tickets`*, `implement`* per ticket; Ship, deploy, release, go live → `release`*. One sentence states the gate and the done-check. Rule 4 adds: a yes that covers later steps is not asked again; deploy and publish always ask. The Superpowers-overlap sentence and the minor stage owners move to `routing.md`. The injected bootstrap stays at or under 3,000 bytes with a plugin path of cache-install length, with at least 100 bytes of headroom.
- `grill` adds: a decision the code or an earlier answer already settles is not a question; the fact goes in the facts section.
- `foundations` adds rows for deploy target and pipeline, environments and config, backups and restore, monitoring and alerts, dependency and secret scanning, each skipped for libraries and scripts, and offers to write the CI or deploy workflow, `.env.example` and a runbook skeleton itself, or the platform's skill when one is installed.
- `routing.md`: the 150k-token figure is replaced by a judgment rule (continue when the next phase needs this conversation; clear when the context is mostly exploration and tool output); the durable state is named (spec, tickets, `CONTEXT.md`, ADRs; a resumed ticket reads them); evidence for an unchanged candidate is reused rather than re-run; the greenfield path is described.

### Hook, installer, harness, docs

- The session-start hook resolves the config directory from `CLAUDE_CONFIG_DIR`, else `~/.claude`; checks every required skill (grilling, domain-modeling, tdd, diagnosing-bugs, code-review, codebase-design, setup-matt-pocock-skills, setup-pre-commit, setup-ts-deep-modules) and lists the missing ones by name with the install command; optional skills named in `routing.md` are not required.
- The installer no longer touches settings.json. It checks `python3` is 3.9 or newer, stops with a message when any `claude plugin` command fails, and prints the tested platforms. `docs/compatibility.md` records the tested combinations: operating systems, Python, Claude Code version, Matt Pocock's skills commit and file hashes, Superpowers version alongside.
- The harness imports the gate module; a Bash mutation before a Skill is scored as straight-to-code; failed tool results, gate refusals, timeouts and exit codes are recorded; `--assert` reads each scenario's expectation file and exits non-zero when fewer than the required runs match. Four gate scenarios are added (a pressured one-line behavior change, a shell write, a typo, a "commit this"); expectations name the skill and whether a refusal is expected.
- Version 3.0.0 in `plugin.json` and `marketplace.json`; plugin id and marketplace name unchanged. README, CHANGELOG, `docs/plugin-behavior-tests.md` and the flow graphs are updated; the case study and the carousel stay as they are.

## Testing Decisions

A good test here checks observable behavior at a public boundary and would survive a rewrite of the internals: the gate module through its functions, a hook through its stdin/stdout contract, a skill through its text, the installer through the files it writes and the exit code it returns, the live workflow through what the model did.

Seams agreed in the grill:

1. **Gate module** (`unittest`, alongside the existing Python tests): the classifier against a table of commands (each row a command, the expected label or none); the decision for each event given a ledger; the ledger round-trip and reset rules; the continuation rule; the done-check rule including `stop_hook_active`.
2. **Hook executables** (a shell suite piping JSON on stdin, in the style of the existing hook test): session start resets on `startup` and `clear` and keeps on `compact`; refuse and allow with and without a declaration; a subagent call with the same session id; a slash command as a declaration; a continuation keeps the declaration; the done-check blocks once and not twice; a hook fed garbage exits 0 with no output. Run under the system Python 3.9 when present, as well as the default `python3`.
3. **Content guards** (extending the static test): injected bootstrap at most 3,000 bytes with a long plugin path; every Seams skill's required headings present; every Seams skill named in the bootstrap or `routing.md`; the Superpowers copies' checksums unchanged; the recorded upstream hashes compared to the installed Matt Pocock files with a warning on drift.
4. **Installer** (fixture home, stubbed `claude`): settings.json untouched; the marketplace, install and enable commands issued; a failing stub command stops the installer with a message; a second run changes nothing; a missing Matt Pocock install without a tty fails with a message.
5. **Live behavior** (`behavior_test.py --assert`): the six routing scenarios at five runs each on the new bootstrap; the four gate scenarios at three runs each. Reported as counts of runs matching the expectation, with refusals counted.

Prior art: `scripts/tests/test_behavior_test.py`, `scripts/tests/test_plugin_hook.sh`, `scripts/tests/test_plugin.sh`, `scripts/tests/test_install.sh`.

## Out of Scope

- The reviewer's thirteen-scenario outcome matrix (a greenfield app to a test deployment, a migration, tenant isolation, webhook concurrency, a failed release). Each needs a disposable app or service; the README lists it as not evidenced.
- Proving that a shell command has no side effects. The classifier is a documented mesh.
- Windows. The hooks are Python executables run through `env`; the tested platforms are macOS and Ubuntu.
- Renaming the plugin id to `seams`, which would force a reinstall on the machine using it.
- Changing Matt Pocock's installed files, Superpowers' files, or the user's settings.json.
- A visual companion, new carousel slides, or a new case study.

## Further Notes

### Alternatives considered

- Prose-only enforcement (as in 2.1): rejected because "always" has to hold on the long tail, not only in tests. ADR-0001.
- `permissionDecision: "ask"` instead of deny: rejected because every false positive would become a prompt and a hurried yes would bypass the workflow. ADR-0001.
- Keeping the runtime-read wrappers, or suggesting the user-only commands by name only: rejected; the first stays at odds with the platform's wording, the second stops Claude carrying the flow. ADR-0002.
- Gating only paths under the session's working directory: rejected because worktrees live outside it; the exemption is the temp and config directories instead.
- Resetting the declaration on every user prompt without exception: rejected because a "yes" to Claude's question would force a re-declaration; the continuation list is the compromise.
- A ledger under the Claude config directory: rejected in favour of the temp directory; a lost ledger costs one declaration and holds nothing worth keeping.
- A "release checklist in the handover" instead of a skill: rejected because a checklist nobody executes is not a gate.

### Risks and failure modes

- A misclassified shell command is refused: the refusal names the label and the `trivial` declaration opens it; one call.
- A shell write the classifier does not recognize goes through: documented as the mesh; the done-check still requires verification when the tool was Bash and the label was a mutation, and never sees an unrecognized one. Reducing the mesh is a matter of adding rows to the classifier table.
- A hook crashes: fails open, so the session continues ungated; the traceback is in the debug log; the hook suite runs under Python 3.9 to catch the most likely cause.
- The ledger is lost (reboot, temp cleanup): the next change is refused once; a declaration restores it.
- Two subagents write the ledger at once: writes are atomic (temp file and rename); the last write wins, which at worst drops one recorded change.
- The model loops on refusals: the reason names the exact next call; the live gate scenarios measure that the model recovers.
- The done-check fires on a turn that ends with a question: it fires once; the model repeats its message and stops.
- Superpowers is enabled alongside and the model invokes its process skill first: the gate stays closed until a Seams or Matt Pocock skill runs; documented.
- A user-only Matt Pocock skill typed by the user (`/implement`) writes code: the typed command is a declaration, so the gate opens; his `implement` calls `tdd` through the Skill tool, which is recorded as well.
- Upstream changes one of the three adapted skills: the static test prints a drift warning; nothing breaks.

### Rollout and migration

- What changes shape: the plugin's hook set (five events instead of one), three skills that stop reading upstream files, the installer's settings step removed, the harness's output. Nothing in the user's settings changes; the Read rules 2.x added are left in place and are harmless.
- Rollout: version 3.0.0 through the existing marketplace; `claude plugin update matt-pocock-workflow@my-workflow-agent-skills` on any machine; the new hooks apply at the next session start. The local directory install on this machine picks the change up at the next session.
- Reversal: `claude plugin disable` turns everything off; reinstalling 2.1.2 from the repo's history restores the old behavior.

### Observability

- A refusal is visible in the transcript as the denied call and its reason; the done-check's block is visible as the reason that continued the turn.
- The ledger file for the session is readable at a deterministic path, so "why was this refused" is one `cat` away.
- Hook failures go to Claude Code's debug log (`claude --debug`), never to the user's transcript.
- The harness's run records carry refusals, failed calls, timeouts and exit codes, and `docs/plugin-behavior-tests.md` reports them as counts.

### Release

- Target: the GitHub repository `gabriel-tutor/seams` (the marketplace) and this machine's local directory install.
- Environments: none beyond the repo; CI on macOS and Ubuntu is the staging check.
- First deploy: a version bump to 3.0.0, a green CI run, then the push to `main`; the plugin's own `release` skill is not required for a marketplace push, but the README's evidence section must be true at the moment of the push.
