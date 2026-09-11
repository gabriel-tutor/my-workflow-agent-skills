# Design: `matt-pocock-workflow` v2, a Matt Pocock–led workflow plugin

**Date:** 2026-09-11
**Status:** approved in conversation; awaiting written-spec review
**Repo:** `~/my-agent-workflow-skills` (GitHub: `gabriel-tutor/my-workflow-agent-skills`)
**Replaces for daily use:** the `matt-pocock-superpowers-workflow` router (retired 2026-09-11) and the `matt-pocock-workflow` v1.1.0 router skill. Both stay in `skills/` so the iteration-1 benchmark remains reproducible.

## 1. Goal

Make Matt Pocock's (MP) skills behave in Claude Code the way Superpowers (SP) does: loaded at every session start, reached without the user remembering commands, chained stage to stage, and interactive at every checkpoint. MP owns the engineering method; SP contributes only the four skills MP has no counterpart for.

Done means, in a fresh session with this plugin enabled and SP disabled:

1. `Add <feature>` starts a grill that asks one clickable question at a time.
2. `<thing> is broken` starts `diagnosing-bugs`.
3. A typo or copy fix runs no process skill.
4. When a grill converges, Claude offers the next MP step (`to-spec` or `implement`) and waits for a yes.
5. No plan contains full code: MP's planners forbid code snippets, and `writing-plans` is not available.

## 2. Context and constraints

| Fact (verified 2026-09-11) | Consequence |
| --- | --- |
| 20 of the 35 installed MP skills are `disable-model-invocation: true`, including the main flow's `grill-with-docs`, `to-spec`, `to-tickets` and `implement`. | Claude cannot start the main flow. Add model-invocable pointer skills for the three flow steps. |
| MP ships no hooks: its upstream `.claude-plugin/plugin.json` lists skills only. | MP has no session bootstrap. This plugin adds one. |
| SP 6.3.0's SessionStart hook (`startup\|clear\|compact`) injects `using-superpowers`, which routes "build X" to `brainstorming` and "fix this bug" to `systematic-debugging`. | With SP enabled, every session carries competing first moves. Disable SP and copy the four kept skills. |
| MP `grilling` asks the whole frontier per round as a numbered text block. SP `brainstorming` asks one question per message. | New `grill` skill: MP's method, SP's presentation. |
| MP skill files are managed by skills-manager (`content_hash`, auto-update, `source_revision 3cca18b`). | Never edit them. `grill` and the pointer skills read them at runtime, so MP stays the single source of truth. |
| SP `writing-plans` requires a code block in every code step; MP `to-spec` and `to-tickets` forbid file paths and code snippets. | MP-led planning removes full-code plans structurally. |
| The four SP skills to copy (`using-git-worktrees` 6.8 KB, `verification-before-completion` 3.6 KB, `finishing-a-development-branch` 7.8 KB, `receiving-code-review` 6.2 KB) contain no references to other SP skills. SP is MIT, © 2025 Jesse Vincent. | Verbatim copies work standalone; attribution goes in a notices file. |
| `claude plugin details`: SP's always-on cost is ~688 tokens. | Disabling SP is about conflicting routing, not token cost. |
| `using-superpowers` (3,108-byte body plus wrapper) inlines fully as hook `additionalContext`; a 23.8 KB injection was spilled to a file with a ~2 KB preview. | Bootstrap injection budget: ≤ 3,000 bytes. |
| `claude --plugin-dir <path>` loads a plugin for one session; `--settings <json>` overrides settings such as `enabledPlugins`. | Behavior tests run headless without installing anything or touching `~/.claude/settings.json`. |
| SP and MP each ship `.claude-plugin/marketplace.json`, making their repo a single-plugin marketplace (`plugins[].source`). | This repo does the same. |
| Benchmark iteration 1: process paid off only on the bug and small-change scenarios; the largest single cost was full brainstorming on a small change (11.3 M tokens). | Routing scales ceremony with task size; TRIVIAL runs no process skill. |
| This repo has no `docs/agents/issue-tracker.md`, which `to-spec`, `to-tickets`, `code-review` and `triage` read. | The bootstrap suggests `/setup-matt-pocock-skills` when a repo lacks it. |

Nothing under `~/.skills-manager/`, the SP plugin cache, or any installed MP skill is modified.

### Assumptions the build verifies first

1. A marketplace entry with `"source": "./plugin"` resolves (SP and MP both use `"./"`). Fallback: make the repo root the plugin root and move the legacy routers out of `skills/`.
2. `--plugin-dir` runs the plugin's SessionStart hook with `CLAUDE_PLUGIN_ROOT` set.
3. SessionStart stdin carries `cwd`. Fallback: the hook's process working directory.
4. AskUserQuestion is available in headless `-p` runs. Fallback: the presentation test checks for exactly one question in the reply, and AskUserQuestion use is covered by manual acceptance.

## 3. Decisions made (with the user)

| Decision | Choice | Why |
| --- | --- | --- |
| Who leads | MP owns design, planning, tests, bugs, review and execution. SP keeps `using-git-worktrees`, `verification-before-completion`, `finishing-a-development-branch` and `receiving-code-review`. | One owner per stage. The four SP skills cover isolation, evidence before claims, integration, and acting on review findings; MP has no skill for any of them. |
| Grill pace | One question per turn via AskUserQuestion, recommended answer first. | The interactive feel the user likes in SP brainstorming. |
| SP coexistence | Disable the SP plugin; ship MIT-attributed copies of the four kept skills in this plugin. | One bootstrap, no competing first moves, no `writing-plans`. One command re-enables SP. |
| Chaining | Claude may start `to-spec`, `to-tickets` and `implement` through pointer skills, asking before each step and before publishing. | SP-style chaining without forking MP. |
| Packaging | This repo becomes a single-plugin marketplace; the plugin lives in `plugin/`. | Mirrors SP and MP. `claude plugin enable` / `disable` toggles it, and anyone can install it from GitHub. `plugin/` keeps the legacy routers and the benchmark out of the shipped plugin. |
| Plan format | The implementation plan for this spec is task and interface level, shaped like MP `to-tickets` (vertical slices, blocking edges, acceptance criteria), saved to `docs/superpowers/plans/`. No full code. | User preference. |

## 4. The workflow

The SessionStart bootstrap tells Claude to classify every development request and route it:

| Path | Signal | Route |
| --- | --- | --- |
| TRIVIAL | copy, config, typo, rename | edit → verify |
| BUG | broken, failing, throwing, slow | `diagnosing-bugs` → verify → finish |
| SMALL | bounded change to an existing flow | `grill` (short: the frontier is small, and includes seams) → `tdd` → verify → finish |
| FEATURE | new behavior that fits one session | `grill` + `domain-modeling` → [`prototype`] → `implement` → verify → finish |
| BIG | a build spanning several sessions | `grill` + `domain-modeling` → `to-spec` → `to-tickets` → per ticket: `/clear`, `implement` → verify → finish |
| FOGGY | too big to see the way | `/wayfinder` → `to-spec` → as BIG |
| INBOX | issues the user didn't write | `/triage` → `ready-for-agent` → `implement` |
| UPKEEP | periodic | `/improve-codebase-architecture` → `grill` → `codebase-design` |

- **verify** is `verification-before-completion`.
- **finish** is `finishing-a-development-branch` when the work is on a branch or worktree. On the base branch, Claude commits and stops.
- **implement** is MP `implement`. It starts in a worktree via `using-git-worktrees`, which asks consent unless the user has declared a preference. Then `tdd` builds one slice at a time at the agreed seams, followed by typecheck, the full suite, `code-review` with the branch's merge-base as the fixed point, and a commit.
- The other MP skills stay reachable as usual: `research`, `resolving-merge-conflicts`, `wizard`, `codebase-design`, `domain-modeling` and `prototype`.
- When the path is ambiguous, Claude takes the heavier one. Complexity discovered mid-task upgrades the path; nothing downgrades (SP brainstorming's one-way ratchet).

Rules on every path:

1. **Checkpoints are interactive.** Every question to the user goes through AskUserQuestion with the recommended answer first. `grill` asks exactly one question per turn.
2. **Seams are settled in the grill.** For anything that will be built, "which seams do we test at?" is a grill question, so `tdd` and `to-spec` do not ask again.
3. **Ceremony scales with size.** TRIVIAL runs no process skill. The two-subagent `code-review` runs on FEATURE and BIG; on SMALL and BUG, Claude offers it.
4. **Chaining is gated.** Claude offers the next step and waits for a yes:
   - grill converged → `to-spec` (BIG) or `implement` (SMALL, FEATURE)
   - spec written → `to-tickets`
   - tickets approved → `implement`, one ticket at a time
5. **Context hygiene.** Grill → spec → tickets stay in one context window, with `/clear` between tickets (from MP `ask-matt`).

## 5. Components

### 5.1 Layout

```text
.claude-plugin/marketplace.json            marketplace "my-workflow-agent-skills" → ./plugin
plugin/
├── .claude-plugin/plugin.json             name "matt-pocock-workflow", version 2.0.0, MIT;
│                                          description marks it an unofficial workflow built on
│                                          Matt Pocock's skills
├── hooks/hooks.json                       SessionStart startup|clear|compact → hooks/session-start
├── hooks/session-start                    builds the injection; Python 3; fails open
├── skills/using-matt-pocock-skills/       bootstrap body + references/routing.md
├── skills/grill/                          interactive grilling
├── skills/to-spec/  to-tickets/  implement/          pointer skills
├── skills/using-git-worktrees/  verification-before-completion/
│   finishing-a-development-branch/  receiving-code-review/     SP 6.3.0 copies
└── THIRD_PARTY_NOTICES.md                 MIT notices, source versions, sha256 of each copy
```

These legacy files stay untouched: `skills/matt-pocock-workflow/`, `skills/matt-pocock-superpowers-workflow/`, `scripts/activate.sh`, `scripts/hooks/` and `benchmark/`.

The plugin namespaces its skill names: `matt-pocock-workflow:grill`, `matt-pocock-workflow:to-spec`, and so on. MP's own skills keep their bare names.

### 5.2 Session bootstrap

**Hook contract:**

- Reads the SessionStart JSON on stdin.
- Writes `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": …}}` on stdout.
- Always exits 0. On any error (unreadable file, bad stdin, exception) it prints nothing.

**Injection.** The `<EXTREMELY_IMPORTANT>` wrapper, plus the body of `using-matt-pocock-skills/SKILL.md` with its frontmatter stripped, plus up to two dynamic lines. Total ≤ 3,000 bytes.

Dynamic lines:

- **MP location.** The hook finds MP's skills directory by locating `grilling/SKILL.md` under `~/.claude/skills`, and states the absolute path so the pointer skills can read from it. If MP is not found, the line says so and names the install routes: skills-manager, or `npx skills add mattpocock/skills`.
- **Repo setup.** If the session's working directory is inside a git repo that has no `docs/agents/issue-tracker.md`, this line tells Claude to suggest `/setup-matt-pocock-skills` before the first spec, tickets, review or triage.

Bootstrap body, in order:

1. **Subagent stop.** A dispatched subagent ignores the bootstrap.
2. **The rule.** Before acting on a development request, classify it and invoke the matching skill. A 1% chance that a skill applies is enough.
3. **Routing.** The §4 routing table, condensed.
4. **Stage owners**, with exact skill names. Includes one guard line: if SP is also enabled, MP wins every overlap:
   - `grill` over `brainstorming`
   - `tdd` over `test-driven-development`
   - `diagnosing-bugs` over `systematic-debugging`
   - `to-spec` / `to-tickets` over `writing-plans`
   - `code-review` over `requesting-code-review`
5. **Cross-path rules.** The five rules from §4.
6. **User-only MP commands** to suggest by name when they fit: `/wayfinder`, `/triage`, `/improve-codebase-architecture`, `/setup-matt-pocock-skills`, `/handoff`, `/ask-matt`.

`references/routing.md` holds the detail that is read on demand:

- MP's main flow and on-ramps, from `ask-matt`
- the phase-boundary order: continue → `/clear` → `/handoff` → subagent → `/compact`
- notes for each path

### 5.3 `grill` (interactive grilling)

- **Triggers** (the description):
  - before building a feature or changing behavior
  - when a plan or design needs stress-testing
  - when any skill says to call `grilling`
- **Method.** Read `<MP dir>/grilling/SKILL.md` and follow its method:
  - a design tree and its frontier
  - facts looked up by a subagent, decisions put to the user
  - done when the frontier is empty
  - no action until the user confirms shared understanding

  In a git repo, also invoke `domain-modeling` (MP's `grill-with-docs` pairing).
- **Presentation.** This overrides grilling's round format:
  - one question per turn via AskUserQuestion
  - 2–4 options, the recommended one first and marked "(Recommended)"
  - free-text answers come through "Other"
  - the next question is picked from the frontier in dependency order
- **Seams.** For anything that will be built, the seams to test at are a frontier question.
- **Fallback.** If the micro-test in §7 shows the round format leaking through:
  - copy MP grilling's text into the skill with the presentation rule applied
  - note it in `THIRD_PARTY_NOTICES.md` (MIT, © 2026 Matt Pocock)
  - record the upstream revision

### 5.4 Pointer skills: `to-spec`, `to-tickets`, `implement`

Each one is model-invocable. Its description states trigger conditions only, following the SP `writing-skills` rule of no workflow summary in descriptions.

| Skill | Trigger | Gate before running | Then |
| --- | --- | --- | --- |
| `to-spec` | a grill converged on a build spanning several sessions | ask "Write the spec now?" unless the user just asked for it; confirm before publishing to the tracker | read `<MP dir>/to-spec/SKILL.md` and follow it |
| `to-tickets` | a spec exists and needs splitting | MP's own quiz is the gate; confirm before publishing | read `<MP dir>/to-tickets/SKILL.md` and follow it |
| `implement` | an agreed design, spec or ticket is ready to build | confirm which spec or ticket, and which branch or worktree | read `<MP dir>/implement/SKILL.md` and follow it, with the merge-base against the base branch as `code-review`'s fixed point |

If the MP file is missing, the skill says MP is not installed and stops. If `docs/agents/issue-tracker.md` is missing, the skill passes on MP's own instruction to run `/setup-matt-pocock-skills`.

### 5.5 Copied Superpowers skills

These are verbatim copies of the SP 6.3.0 skills `using-git-worktrees`, `verification-before-completion`, `finishing-a-development-branch` and `receiving-code-review`. Each body stays byte-identical to upstream so drift is easy to diff.

`THIRD_PARTY_NOTICES.md` carries:

- the MIT license text
- "Superpowers 6.3.0, © 2025 Jesse Vincent"
- each file's sha256

## 6. Failure handling

| Situation | Behavior |
| --- | --- |
| Hook error of any kind | No output, exit 0. The session starts without the bootstrap. |
| MP not installed | The bootstrap says so; `grill` and the pointer skills stop with the install hint. |
| SP re-enabled | Two bootstraps load. The guard line in §5.2 gives MP precedence on overlaps. Duplicate names (`superpowers:X` and `matt-pocock-workflow:X`) are harmless. |
| Injection over budget | A unit test fails, so an over-budget bootstrap never ships. |
| Repo not set up | The bootstrap and the pointer skills suggest `/setup-matt-pocock-skills`. Nothing is created automatically. |

## 7. Testing

1. **Hook unit tests** (`scripts/tests/test_plugin_hook.sh`). They run in fixture HOME and cwd directories, never the real `~/.claude`, and check:
   - valid JSON shape
   - injection ≤ 3,000 bytes
   - the MP-location line appears when an MP dir exists, and the "not found" line when it doesn't
   - the repo-setup line appears only in a git repo that lacks `docs/agents/issue-tracker.md`
   - fail-open cases (unreadable bootstrap file, garbage stdin) print nothing and exit 0
2. **Static checks** (`scripts/tests/test_plugin.sh`):
   - `claude plugin validate` passes for `plugin/` and for the marketplace
   - every plugin skill has `name` and `description`
   - no plugin skill sets `disable-model-invocation`
   - each copied SP skill matches the sha256 recorded in `THIRD_PARTY_NOTICES.md`
3. **Behavior micro-tests** (the SP `writing-skills` method):
   - headless `claude -p` runs with `--plugin-dir plugin` and `--settings` disabling SP
   - 5 runs per scenario, plus a control run without the plugin
   - the first Skill or AskUserQuestion call is read from stream-json output, and every flagged match is also read by hand

   | Scenario | Pass |
   | --- | --- |
   | `Add <feature>` in the benchmark fixture | the first skill is `matt-pocock-workflow:grill` (`domain-modeling` may follow), 5/5 |
   | `<thing> is broken` | the first skill is `diagnosing-bugs`, 5/5 |
   | typo fix | no process skill runs, 5/5 |
   | grill presentation | the first question is a single AskUserQuestion question, not a numbered batch, 5/5 |
   | converged design spanning several sessions, without asking for a spec | Claude asks before invoking `to-spec`, 5/5 |

   A miss means revising the wording and re-running the scenario (RED → GREEN → REFACTOR). Results are recorded in `docs/plugin-behavior-tests.md`.
4. **Manual acceptance.** The user runs one fresh session in a real repo and walks through the five "done means" checks in §1.
5. **Regression.** The existing suites under `scripts/tests/` keep passing; legacy files are untouched.

## 8. Rollout and rollback

Each step runs with the user's approval, and `~/.claude/settings.json` is backed up first.

1. `claude plugin marketplace add ~/my-agent-workflow-skills`
2. `claude plugin install matt-pocock-workflow@my-workflow-agent-skills`
3. `claude plugin disable superpowers@claude-plugins-official`
4. Restart and confirm that the MP bootstrap appears once and SP's does not.
5. In each repo, on first use: `/setup-matt-pocock-skills`.

Rollback: `claude plugin enable superpowers@claude-plugins-official`, then `claude plugin disable matt-pocock-workflow@my-workflow-agent-skills`.

Docs:

- The README's "How to use it" section is rewritten around the plugin.
- The two v1 routers are labeled legacy; the benchmark section stays.
- The CHANGELOG gains an entry for `matt-pocock-workflow` 2.0.0.

## 9. Out of scope

- Editing MP or SP upstream files, or anything under `~/.skills-manager/` or the plugin cache.
- MP installed as the official `mattpocock-skills` plugin, with its namespaced names and cache paths. v2.0.0 supports `~/.claude/skills` installs (skills-manager, or skills.sh installed globally). For any other install, the bootstrap reports MP as not found.
- Hook formats for Cursor, Copilot or Codex, and Windows (`run-hook.cmd`).
- Redirecting the `grilling` calls made inside MP's `triage`, `wayfinder` and `improve-codebase-architecture`. The only redirect is the trigger in `grill`'s description, and it is not behavior-tested in v2.0.0.
- Automated syncing of the copied SP skills with upstream.
- Running each ticket in its own subagent while the user is away.
- A second benchmark iteration.
