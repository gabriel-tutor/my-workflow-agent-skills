# `matt-pocock-workflow` v2 plugin: implementation plan

**Spec:** `docs/superpowers/specs/2026-09-11-matt-pocock-workflow-plugin-design.md`. This plan argues from the spec, and any conflict resolves against the spec.
**Branch:** `build/matt-pocock-workflow-v2`, from `main`.
**Shape:** MP `to-tickets` style: tracer-bullet vertical slices, each with blocking edges and acceptance criteria. Task and interface level, with no full code (user preference). Headings use `### Task N`, so SP's `task-brief` can extract them if execution goes subagent-driven.
**Execution:** decided at plan approval, either inline in the controlling session or subagent-driven.

## Global constraints

- Never modify `~/.skills-manager/`, the Superpowers plugin cache, any installed MP skill, or `~/.claude/settings.json`. Unit tests use fixture HOME and cwd directories. Behavior tests use `--plugin-dir` and `--settings` overrides.
- The hook fails open: on any error it writes nothing to stdout and exits 0.
- The injection (wrapper, body and dynamic lines together) is at most 3,000 bytes.
- The plugin is named `matt-pocock-workflow`, at version `2.0.0`, under the MIT license. The marketplace is `my-workflow-agent-skills`, and the plugin root is `plugin/`.
- Skill names:
  - Plugin skills: `using-matt-pocock-skills`, `grill`, `to-spec`, `to-tickets`, `implement`, and the four SP copies under their upstream names.
  - Bootstrap text refers to plugin skills by namespaced name (`matt-pocock-workflow:<name>`) and to MP skills by bare name.
- The SP copies stay byte-identical to 6.3.0. Attribution goes only in `plugin/THIRD_PARTY_NOTICES.md`.
- Skill descriptions state trigger conditions only (the SP `writing-skills` rule).
- Legacy files stay untouched: `skills/*`, `scripts/activate.sh`, `scripts/hooks/*` and `benchmark/*`. The fixture and `scripts/prepare_run.sh` are reused read-only.
- Tests follow the `scripts/tests/` conventions: bash with `set -euo pipefail`, a temp dir cleaned up by a trap, a `fail()` helper, and inline Python for JSON assertions.
- Every commit ends with the session's `Co-Authored-By` and `Claude-Session` trailers.

## Tickets

### Task 1: The plugin loads and injects a bootstrap

**Blocked by:** none; can start immediately.

**What to build:** a minimal installable plugin. A headless session that loads it gets an MP bootstrap in context, with both dynamic lines working. This task also settles the spec's four open assumptions (spec §2) before any skill wording is written.

**Interfaces:**

- `.claude-plugin/marketplace.json`: one plugin entry, sourced from `./plugin`.
- `plugin/.claude-plugin/plugin.json`: name, version, description (it must say this is an unofficial workflow built on Matt Pocock's skills), author, repository, license.
- `plugin/hooks/hooks.json`: a SessionStart hook with matcher `startup|clear|compact` that runs `hooks/session-start` via `${CLAUDE_PLUGIN_ROOT}`.
- `plugin/hooks/session-start` (Python 3):
  - **Input:** the SessionStart JSON on stdin. It uses `cwd`, falling back to the process working directory.
  - **Output:** `hookSpecificOutput.additionalContext`, built from:
    - the wrapper
    - the bootstrap body with its frontmatter stripped
    - the MP-location line
    - the repo-setup line, when it applies
  - It honours `HOME`, so tests can point it at a fixture home.
- `plugin/skills/using-matt-pocock-skills/SKILL.md`: a placeholder body with a unique marker line. The real content arrives in Tasks 3–5.

**Acceptance criteria:**

- [ ] `claude plugin validate` passes for `plugin/` and for the repo-root marketplace. If it doesn't, the spec §2 fallback (the repo root becomes the plugin root) is applied and recorded.
- [ ] `scripts/tests/test_plugin_hook.sh` covers:
  - valid JSON with `hookEventName: SessionStart`
  - an injection of at most 3,000 bytes
  - when the fixture's `grilling/SKILL.md` exists, the MP-location line names the fixture's MP dir; when it doesn't, the line says "not found" and names the install routes
  - the repo-setup line appears only in a git repo that lacks `docs/agents/issue-tracker.md`
  - garbage stdin and an unreadable bootstrap file both produce empty stdout and exit 0
- [ ] A headless `claude -p --plugin-dir plugin` session reports the marker line from its context, and the debug output shows the hook ran. This shows that `CLAUDE_PLUGIN_ROOT` is set under `--plugin-dir`.
- [ ] `docs/plugin-behavior-tests.md` gains an "Assumptions" section with the result for each of the four assumptions, including whether AskUserQuestion appears in the headless tool list.

### Task 2: Superpowers' four kept skills ship inside the plugin

**Blocked by:** Task 1.

**What to build:** verbatim copies of four SP 6.3.0 skills under `plugin/skills/`: `using-git-worktrees`, `verification-before-completion`, `finishing-a-development-branch` and `receiving-code-review`. They come with MIT attribution and a check that catches accidental edits.

**Interfaces:**

- `plugin/skills/<name>/SKILL.md`, four files copied byte for byte from the local SP 6.3.0 cache.
- `plugin/THIRD_PARTY_NOTICES.md`:
  - the MIT license text
  - "Superpowers 6.3.0, © 2025 Jesse Vincent"
  - the source path
  - the sha256 of each copy
- `scripts/tests/test_plugin.sh`: static checks. Later tasks extend it.

**Acceptance criteria:**

- [ ] Each copy's sha256 matches the value recorded in the notices file. When the cache is present, it also matches the SP 6.3.0 original.
- [ ] `test_plugin.sh` passes:
  - `claude plugin validate` is clean
  - every plugin skill has `name` and `description`
  - no plugin skill sets `disable-model-invocation`
- [ ] A `--plugin-dir` session lists the four skills under the `matt-pocock-workflow:` namespace, checked from the stream-json init event or by asking the session.

### Task 3: Bugs route to diagnosing-bugs, and trivial edits run no process

**Blocked by:** Task 2.

**What to build:** the bootstrap's core policy plus the behavior-test harness, proven on the two scenarios at either end of the size scale.

**Interfaces:**

- The `using-matt-pocock-skills/SKILL.md` body:
  - the subagent stop
  - the rule: classify, then invoke, with a 1% threshold
  - the TRIVIAL and BUG routing rows
  - stage owners for verify, finish and worktree (namespaced), plus the SP-overlap guard line
  - cross-path rules 1 (its general part), 3 and 5
- `references/routing.md`:
  - MP's main flow and on-ramps (from `ask-matt`)
  - the order of choices at a phase boundary
  - notes for each path
- `scripts/behavior_test.py`:
  - **Input:** scenario, prompt, arm (`plugin` or `control`), number of runs.
  - **Workspace:** each run gets a fresh fixture workspace from `scripts/prepare_run.sh <scenario>`.
  - **Headless run:** each run is headless `claude -p` with:
    - `--output-format stream-json --verbose`
    - `--settings` disabling `superpowers@claude-plugins-official`
    - `--plugin-dir plugin`, in the plugin arm only
  - **Stopping:** each run stops at the first `Skill` or `AskUserQuestion` tool call, at a wall-clock timeout, or at the end of the reply. The timeout is enforced in Python, because macOS has no `timeout` command and `claude -p` has no turn limit.
  - **Records:** per run, the first call (tool, skill name, question count) as JSON lines, plus the raw stream kept for reading by hand. It prints a summary table.
  - **Control arm:** the same, without `--plugin-dir`.

**Acceptance criteria:**

- [ ] `concurrency-bug` prompt: the first skill is `diagnosing-bugs` in 5/5 plugin runs, and the control results are recorded.
- [ ] `cosmetic-edit` prompt: no process skill (`grill`, `tdd`, `diagnosing-bugs`, `to-spec`, `implement`) runs in 5/5 plugin runs.
- [ ] Every flagged match is read by hand. Results and any wording revisions are logged in `docs/plugin-behavior-tests.md`.
- [ ] The injection is still at most 3,000 bytes (hook test).

### Task 4: Feature requests start an interactive grill

**Blocked by:** Task 3.

**What to build:** the `grill` skill and the SMALL and FEATURE routing that reaches it, proven headless.

**Interfaces:**

- `plugin/skills/grill/SKILL.md`:
  - **Description:** the three triggers from spec §5.3.
  - **Method:** read `<MP dir>/grilling/SKILL.md` for the method. The directory comes from the bootstrap's MP-location line.
  - **Presentation override:**
    - one AskUserQuestion question per turn
    - 2–4 options, with the recommended one first and marked "(Recommended)"
    - "Other" for free text
    - questions asked in dependency order
  - **Seams:** which seams to test at is a frontier question.
  - **Pairing:** `domain-modeling` runs alongside it in a git repo.
  - **Missing MP:** stop with the install hint.
- Bootstrap: the SMALL and FEATURE routing rows, rule 2, and the grill part of rule 1.

**Acceptance criteria:**

- [ ] The `small-behavior-change` prompt, plus one "add a feature" prompt: the first skill is `matt-pocock-workflow:grill` in 5/5 plugin runs. `domain-modeling` may follow.
- [ ] Grill presentation: the first question to the user is a single AskUserQuestion question in 5/5 runs. If Task 1 found AskUserQuestion unavailable headless, the check is instead for exactly one question in the text reply, and AskUserQuestion use is covered by manual acceptance.
- [ ] If the batched-round format still leaks through after two wording revisions, the spec's fallback is applied: MP grilling's text is copied into `grill` with the override, and recorded in the notices file with the upstream revision.
- [ ] Control results are recorded, and the injection is at most 3,000 bytes.

### Task 5: A converged design chains forward, with a gate at every step

**Blocked by:** Task 4.

**What to build:** the pointer skills `to-spec`, `to-tickets` and `implement`, plus the BIG path and the chaining rules in the bootstrap.

**Interfaces:**

- `plugin/skills/{to-spec,to-tickets,implement}/SKILL.md`:
  - triggers as in spec §5.4
  - the body: a gate, then read `<MP dir>/<name>/SKILL.md` and follow it
  - handling for a missing MP install and for a missing repo setup
  - `implement` starts with `using-git-worktrees` and names the merge-base as `code-review`'s fixed point
- Bootstrap:
  - the BIG, FOGGY, INBOX and UPKEEP routing rows
  - rule 4
  - the user-only MP commands to suggest by name

**Acceptance criteria:**

- [ ] A prompt that states an agreed design for a multi-session build, without asking for a spec, run in the `small-behavior-change` workspace: Claude asks before invoking `matt-pocock-workflow:to-spec` in 5/5 runs, and nothing is published to a tracker.
- [ ] A prompt that explicitly says "write the spec": `to-spec` is invoked without an extra gate question (spot check, 2 runs).
- [ ] The pointer skills stop with the install hint when MP is missing. Verified either by a headless run against a fixture home without MP or by a static assertion on the skill body; which one was used is recorded.
- [ ] With the full routing table, the injection is at most 3,000 bytes, and `test_plugin.sh` passes.

### Task 6: Docs and regression

**Blocked by:** Task 5.

**What to build:** the repo presents the plugin as the way to use it.

**Interfaces:**

- `README.md`:
  - "How to use it" is rewritten around the plugin: marketplace add, install, disabling SP, per-repo `/setup-matt-pocock-skills`, and rollback.
  - It includes the workflow table from spec §4.
  - The v1 routers and the "Make it run every session" section are labeled legacy.
  - The Layout and Tests sections are updated.
  - The Benchmark section stays unchanged.
- `CHANGELOG.md`: a `matt-pocock-workflow` 2.0.0 entry.
- `docs/plugin-behavior-tests.md`: the final results table for all five scenarios and the four assumptions.

**Acceptance criteria:**

- [ ] Every command in the README was either run (validate) or is a subcommand listed in `claude plugin --help`.
- [ ] All suites in `scripts/tests/` pass, both the existing and the new ones.
- [ ] No legacy file changes, apart from the README and CHANGELOG labeling.

### Task 7: Rollout on the user's machine (human in the loop)

**Blocked by:** Task 6 and the Finish step.

**What to build:** the plugin installed and in daily use, with SP disabled and a tested way back.

**Acceptance criteria:**

- [ ] `~/.claude/settings.json` is backed up.
- [ ] With the user's approval at each step: the marketplace is added, the plugin installed, and SP disabled.
- [ ] In a new session, the MP bootstrap appears once and SP's does not appear.
- [ ] The user walks through the five "done means" checks from spec §1 in a real repo.
- [ ] The rollback commands are documented and checked for exactness.

## Finish (after Task 6, before Task 7)

1. **Review.** Review the branch against `main` on both axes, standards and spec, using MP `code-review` with the spec as its source. Fix every Critical and Important finding.
2. **Verify.** Run `verification-before-completion`: every suite runs fresh, and the output is cited.
3. **Integrate.** Run `finishing-a-development-branch`. The user chooses between merging locally, opening a PR, or keeping the branch.

## Cost note

The behavior tests come to 5 scenarios × (5 plugin + 5 control) ≈ 50 headless runs. Each run stops at the first skill or question, and there will be re-runs after wording revisions. Estimated total: 1–3 M tokens. For comparison, benchmark iteration 1 used 41 M.
