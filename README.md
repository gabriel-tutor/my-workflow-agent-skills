# my-agent-workflow-skills

A Claude Code plugin that makes [Matt Pocock's engineering skills](https://github.com/mattpocock/skills) lead every session, the way Superpowers does for its own skills: a session bootstrap that routes each development task, a grill that asks one clickable question at a time, and gated spec, tickets and implement steps. Plus the benchmark and the two earlier router skills that led here.

## The workflow

Every session starts with the routing policy in context. Claude classifies each request and takes the matching path:

| Request | Path |
| --- | --- |
| Trivial: copy, typo, config, rename | edit, then verify |
| Broken, failing, throwing, slow | `diagnosing-bugs`, then verify and finish |
| Bounded change to existing code | short `grill`, then `tdd`, then verify and finish |
| New behavior that fits one session | `grill` + `domain-modeling`, then `implement`, then verify and finish |
| A build spanning several sessions | grill, then `to-spec`, `to-tickets`, and `implement` one ticket per session |
| Foggy effort, issues someone else wrote, upkeep | Claude suggests `/wayfinder`, `/triage`, `/improve-codebase-architecture` |

Matt Pocock's skills own design, planning, tests, bugs, review and execution. Four Superpowers skills cover what they don't: `using-git-worktrees`, `verification-before-completion` (verify), `finishing-a-development-branch` (finish) and `receiving-code-review`. They ship inside this plugin as unmodified, MIT-attributed copies (`plugin/THIRD_PARTY_NOTICES.md`), so the Superpowers plugin itself can stay disabled and there is only one bootstrap per session.

Three rules apply on every path: questions go through the clickable question tool with the recommended answer first; test seams are settled in the grill, so `tdd` doesn't ask again; and every chained step (`to-spec`, `to-tickets`, `implement`) asks before it starts and before it publishes anything.

## How to use it

### 1. Install Matt Pocock's skills

The plugin contains none of his skills. It invokes the installed ones by name, so they must be under `~/.claude/skills/<name>/SKILL.md`:

```bash
npx skills@latest add mattpocock/skills   # or skills-manager, or a git clone symlinked in
```

Don't install his official `mattpocock-skills` Claude Code plugin alongside: you'd have every skill twice.

### 2. Install this plugin

```bash
git clone https://github.com/gabriel-tutor/my-workflow-agent-skills.git
claude plugin marketplace add ./my-workflow-agent-skills
claude plugin install matt-pocock-workflow@my-workflow-agent-skills
claude plugin disable superpowers@claude-plugins-official    # if you have it; one bootstrap per session
```

Restart Claude Code. Every new session now opens with the routing policy, plus two lines computed for that session: where Matt Pocock's skill files are, and a nudge to run `/setup-matt-pocock-skills` when the repo has no `docs/agents/issue-tracker.md` yet.

Give Claude read access to the skill files it loads. The `to-spec`, `to-tickets` and `implement` steps read Matt Pocock's own `SKILL.md` for that step, and the bootstrap points at a reference file inside the plugin. Add these to `permissions.allow` in `~/.claude/settings.json` (the second rule matters because `~/.claude/skills` entries are usually symlinks and the check uses the resolved path):

```json
"Read(~/.claude/skills/**)",
"Read(~/.skills-manager/**)",
"Read(~/.claude/plugins/**)"
```

### 3. Once per repo

```text
/setup-matt-pocock-skills
```

It configures the issue tracker (local markdown under `.scratch/` works for solo repos), the triage labels and where `CONTEXT.md` and ADRs live. `to-spec`, `to-tickets`, `code-review` and `triage` read that configuration.

### 4. Then just work

> *"Add gift card support: customers should be able to pay part of an order with a gift card balance."*

Claude invokes the grill before touching anything, asks one question at a time, and offers the next step when the design converges. To confirm it's live, start a fresh session and ask which skill applies to a bug fix; it should name `diagnosing-bugs`.

### Turning it off

```bash
claude plugin disable matt-pocock-workflow@my-workflow-agent-skills
claude plugin enable superpowers@claude-plugins-official
```

## Does it actually route?

`docs/plugin-behavior-tests.md` records the headless tests behind every wording decision, following the RED-GREEN-REFACTOR method from Superpowers' `writing-skills`. Each scenario ran 5 times with the plugin and 5 times without, in fresh copies of the benchmark fixture, and the verdict is the first committing tool call:

| Prompt | Without the plugin | With the plugin |
| --- | --- | --- |
| Overselling bug in `reserve` | edited the source first, 5/5 | `diagnosing-bugs` as the first tool call, 5/5 |
| Two typo fixes | edited, 5/5 | edited, 5/5 (no process skill) |
| Add coupon codes | edited the source first, 5/5 | `grill` as the first tool call, 5/5 |
| Add gift card support | wrote new files after ~100 s of exploring, 5/5 | `grill` as the first tool call, 5/5 |
| Agreed multi-session design, "let's get going" | started writing code, 5/5 | asked "Write the spec now?" before reading anything, 5/5 |

The grill's one-question-at-a-time format took three wording revisions to reach 5/5 on both feature prompts; the doc shows what leaked each time.

Run the harness yourself:

```bash
python3 scripts/behavior_test.py run --scenario concurrency-bug --arm plugin --runs 5
python3 scripts/behavior_test.py run --scenario concurrency-bug --arm control --runs 5
```

## Benchmark results (v1 routers)

Before the plugin, this repo held two *router skills*: `matt-pocock-workflow` v1 (Matt Pocock only) and `matt-pocock-superpowers-workflow` (Superpowers leads, Matt Pocock's skills as disciplines). They still live under `skills/` and `scripts/activate.sh` still installs them, but they are legacy: the plugin replaces both for daily use.

They were benchmarked over 18 runs (6 scenarios × 3 arms) executed by Claude Opus 5 on a sandbox TypeScript project, graded by objective checks on the real workspace plus one independent Sonnet grader per run.

| Arm | Graded | Cost vs. baseline | Wall time |
| --- | --- | --- | --- |
| `matt-pocock-superpowers-workflow` (combo) | **35/35** | 4.1× | 67 min |
| `matt-pocock-workflow` v1 (MP only) | 34/35 | 2.6× | 60 min |
| no router (all skills still installed) | 32/35 | 1.0× | 18 min |

**The finding that shaped the plugin: the routers won on process compliance, not on outcomes.** Every arm's code passed the hidden acceptance tests. All three failures were ordering assertions (test-before-code, diagnosis-before-edit), and only the concurrency-bug and small-feature scenarios discriminated at all. The single costliest run was the combo invoking Superpowers' full `brainstorming` on a small bounded change (11.3 M tokens). Hence the plugin's rules: ceremony scales with the change, and Matt Pocock's lighter grill replaces `brainstorming`.

Caveats: n = 1 per cell, so nothing here is statistically significant, and wall time is contaminated by 18 concurrent runs. Full write-up: [`benchmark/runs/iteration-1/analysis.md`](benchmark/runs/iteration-1/analysis.md); raw transcripts and grades are committed under `benchmark/runs/iteration-1/`. `benchmark/README.md` is the runbook for reproducing it.

## Layout

- `plugin/` — the plugin: `.claude-plugin/plugin.json`, `hooks/` (SessionStart bootstrap), `skills/` (bootstrap, `grill`, the three pointer skills, the four Superpowers copies), `THIRD_PARTY_NOTICES.md`
- `.claude-plugin/marketplace.json` — makes this repo a single-plugin marketplace
- `docs/plugin-behavior-tests.md` — headless behavior-test evidence; `docs/superpowers/` — design specs and plans
- `scripts/behavior_test.py` — the behavior-test harness; `scripts/tests/` — all test suites
- `skills/`, `scripts/activate.sh`, `scripts/hooks/` — the legacy v1 routers and their installer
- `benchmark/` — fixture project, scenarios, eval set, iteration-1 results
- `sources/` — pinned upstream archives (never loaded by agents)

## Tests

```bash
scripts/tests/test_plugin.sh          # manifests validate, skills well-formed, Superpowers copies pinned
scripts/tests/test_plugin_hook.sh     # the bootstrap hook against fixture homes and repos
scripts/tests/test_activate.sh
scripts/tests/test_skills.sh
scripts/tests/test_prepare_run.sh
scripts/tests/test_finalize_run.sh
scripts/tests/test_hooks.sh
python3 -m unittest discover -s scripts/tests -p 'test_*.py'
```
