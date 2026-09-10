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

## Activate one skill

Only one of the two should be installed at a time — both trigger "before the first edit of any development task" and would compete.

```bash
scripts/activate.sh status
scripts/activate.sh matt-pocock-superpowers-workflow   # or matt-pocock-workflow, or none
```

The script only ever creates or removes symlinks that point into this repo's `skills/`; it refuses to touch a real directory or a foreign symlink.

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
python3 -m unittest discover -s scripts/tests -p 'test_*.py'
```
