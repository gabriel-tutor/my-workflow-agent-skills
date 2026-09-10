# my-agent-workflow-skills

Two Claude Code skills that route development work through installed skill collections, plus the benchmark that compares them.

| Skill | What it routes | Version |
| --- | --- | --- |
| `skills/matt-pocock-workflow` | Matt Pocock's skills only | see CHANGELOG |
| `skills/matt-pocock-superpowers-workflow` | Superpowers owns the lifecycle; Matt Pocock's skills supply the disciplines; explicit conflict rules | see CHANGELOG |

Both are routers: they invoke the *installed* `superpowers:*` plugin skills and Matt Pocock skills by name and never copy their content.

## Activate one skill

Only one of the two should be installed at a time — both trigger "before the first edit of any development task" and would compete.

```bash
scripts/activate.sh status
scripts/activate.sh matt-pocock-superpowers-workflow   # or matt-pocock-workflow, or none
```

The script only ever creates or removes symlinks that point into this repo's `skills/`; it refuses to touch a real directory or a foreign symlink.

## Benchmark

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
scripts/tests/test_prepare_run.sh
scripts/tests/test_finalize_run.sh
python3 -m unittest discover -s scripts/tests -p 'test_*.py'
```
