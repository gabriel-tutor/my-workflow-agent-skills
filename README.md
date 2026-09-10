# my-agent-workflow-skills

Two Claude Code skills that route development work through installed skill collections, plus the benchmark that compares them.

| Skill | What it routes | Version |
| --- | --- | --- |
| `skills/matt-pocock-workflow` | Matt Pocock's skills only | see CHANGELOG |
| `skills/matt-pocock-superpowers-workflow` | Superpowers owns the lifecycle; Matt Pocock's skills supply the disciplines; explicit conflict rules | see CHANGELOG |

Both are routers: they invoke the *installed* `superpowers:*` plugin skills and Matt Pocock skills by name and never copy their content.

## Benchmark results

18 runs — 6 scenarios × 3 arms, executed by Claude Opus 5 on a sandbox TypeScript project, graded by objective checks on the real workspace (tests, typecheck, file manifests, tool-call order taken from each agent's transcript) plus one independent Sonnet grader per run.

| Arm | Graded | Cost vs. baseline | Wall time |
| --- | --- | --- | --- |
| `matt-pocock-superpowers-workflow` (combo) | **35/35** | 4.1× | 67 min |
| `matt-pocock-workflow` (MP only) | 34/35 | 2.6× | 60 min |
| no router (all skills still installed) | 32/35 | 1.0× | 18 min |

Cost is price-weighted (cache reads are ~10% of input price), so it is lower than the raw 5.8× token ratio.

**The honest finding: the routers won on process compliance, not on outcomes.** Every arm's code passed the hidden acceptance tests in every scenario. All three failures across 18 runs were *ordering* assertions — test-before-code, diagnosis-before-edit — never "produced wrong software".

Only two of six scenarios discriminated at all:

- **Concurrency bug.** Without a router the agent scored 4/6: it produced a correct per-SKU lock, but edited the source before writing the regression test and never invoked a diagnosis skill. Both routers scored 6/6. The combo did it with **no subagents at 2.3M tokens** where MP-only spent 3.5M on a two-reviewer orchestration — the clearest case where the combined policy is both better *and* cheaper than the skill set it extends.
- **Small feature.** Combo 6/6; the other two 5/6. But the combo reached it by invoking `brainstorming` on a task its own sizing table calls a small bounded change — 11.3M tokens, the single costliest run in the benchmark.

On the other four scenarios — a cosmetic edit, a review-scope task, an approved-spec implementation, and a report-honesty task — every arm scored full marks, and the routers bought nothing but tokens.

**Caveats that matter:** n = 1 per cell, so none of this is statistically significant. Subagents ignore the `using-superpowers` session bootstrap, so each arm was tested on its own routing text — which makes the no-router baseline *harder* than a real session would be. Wall time is contaminated by 18 concurrent runs; the cost column is the reliable metric.

Full write-up with per-run detail: [`benchmark/runs/iteration-1/analysis.md`](benchmark/runs/iteration-1/analysis.md). Raw transcripts, per-expectation grades and diffs for all 18 runs are committed under `benchmark/runs/iteration-1/`.

## How to use it

### 1. Install the collections these skills route to

Neither skill contains any workflow of its own — each one *names* skills that must already be installed, and does nothing useful without them.

```bash
# Superpowers (Claude Code plugin) — needed by matt-pocock-superpowers-workflow
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace

# Matt Pocock's skills — needed by both, from github.com/mattpocock/skills
# install into ~/.claude/skills/ by whatever method you prefer
```

Superpowers is installed from inside Claude Code (the `/plugin` commands above). Matt Pocock's skills are plain skill folders under `~/.claude/skills/<name>/SKILL.md`; this repo was developed against all 37 of them, but the routers degrade gracefully — a skill that isn't installed simply never gets routed to.

### 2. Clone and activate

```bash
git clone https://github.com/gabriel-tutor/my-workflow-agent-skills.git
cd my-workflow-agent-skills
scripts/activate.sh matt-pocock-superpowers-workflow
```

That symlinks the chosen skill into `~/.claude/skills/`. Use `matt-pocock-workflow` instead if you don't run Superpowers, or `none` to uninstall both.

**Only one at a time.** Both trigger "before the first edit of any development task", so having both installed produces two competing routers. `activate.sh` enforces this: it unlinks the other one when you activate either. It only ever creates or removes symlinks pointing into this repo's `skills/` — it refuses to touch a real directory or a foreign symlink, so it can't eat an existing installation.

```bash
scripts/activate.sh status    # which one is live right now
```

### 3. Then just work

You don't invoke the skill. Its description triggers it automatically at the start of a development task, and it routes from there — so a normal request is all you do:

> *"The scraper crashes during bulk runs, can you fix it?"*

Behind that, the combined policy assigns one owner per stage: `superpowers:systematic-debugging` leads the diagnosis and escalates to Matt Pocock's `diagnosing-bugs` if reproduction turns out to be hard, `superpowers:test-driven-development` owns the test cycle with MP's seam guidance as reference, and review runs once — against the working tree, not just committed changes. The point is that no interview, test cycle or review runs twice, which is what happens when both collections are installed and nothing arbitrates between them.

To confirm it's live, start a fresh session and ask which skill applies before a bug fix; it should name the active router.

### Make it run every session

Skill invocation is normally the model's judgement call. A `SessionStart` hook removes that
uncertainty — the same mechanism Superpowers uses for `using-superpowers`:

```bash
scripts/hooks/install.sh      # adds it to ~/.claude/settings.json (backed up first)
scripts/hooks/uninstall.sh    # removes only what install.sh added
```

Every new session then opens with the policy already in context: which collection owns each
stage, the never-run-two-of-anything rule, process sizing, and which Matt Pocock skills are
user-invoked only. It follows `activate.sh` — whichever router is active gets injected, and
`activate.sh none` turns the injection off.

It injects a compact pointer (~450 tokens), not the whole skill. Claude Code inlines only about
2 KB of hook context and spills the rest to a file, so injecting all 23 KB would silently deliver
a truncated preamble and a file path. Superpowers can inline its whole skill because that one is
3 KB. The pointer carries the load-bearing rules; the skill carries the full tables.

The hook fails silent: any error prints nothing and exits 0, so it can never stop a session from
starting. **It runs a script on every session start — read `scripts/hooks/session-start` before
installing it.** That advice applies to anyone's hooks, including these.

### When it's worth using

Per the benchmark above: clearly worth it for **bugs and anything where process order matters** — that's where it beat both alternatives, and beat Matt Pocock's skills alone on cost too. For cosmetic edits, routine features and reviews, a strong model reached the same outcome without any router at roughly a quarter of the cost. If you want to be selective, run `scripts/activate.sh none` and invoke the skill by name when a task warrants it.

## Reproducing the benchmark

`benchmark/README.md` is the runbook. Short version: `scripts/activate.sh none`, `python3 scripts/init_iteration.py benchmark/runs/iteration-N`, spawn one subagent per entry in the generated `runs.json`, then convert transcripts, grade, aggregate, and open the viewer.

## Layout

- `sources/` — pinned upstream archives and the two source documents (never loaded by agents)
- `skills/<name>/SKILL.md` + `references/` — the skills
- `scripts/` — `activate.sh`, benchmark tooling, and their tests (`scripts/tests/`)
- `benchmark/` — fixture project, scenarios, eval set, run results
- `docs/superpowers/` — design spec and implementation plan

## Tests

```bash
scripts/tests/test_activate.sh
scripts/tests/test_skills.sh
scripts/tests/test_prepare_run.sh
scripts/tests/test_finalize_run.sh
scripts/tests/test_hooks.sh
python3 -m unittest discover -s scripts/tests -p 'test_*.py'
```
