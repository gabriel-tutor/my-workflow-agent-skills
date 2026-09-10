# Benchmark runbook

Compares three arms on six scenarios against the OrderKit fixture:

| Config | Skill the subagent is told to read | Agent name |
| --- | --- | --- |
| `new_skill` | `skills/matt-pocock-superpowers-workflow/SKILL.md` | `e<id>-combo` |
| `old_skill` | `skills/matt-pocock-workflow/SKILL.md` | `e<id>-mp` |
| `without_skill` | none ("work as you normally would") | `e<id>-none` |

All arms still see every installed skill (Superpowers plugin + Matt Pocock's) through the Skill tool. Subagents ignore the `using-superpowers` bootstrap (`<SUBAGENT-STOP>`), so each arm is tested on its own routing.

## One iteration, end to end

1. **Neutralise the skills dir** so no arm gets a router for free: `scripts/activate.sh status` (remember what was active), then `scripts/activate.sh none`.
2. **Prepare**: `python3 scripts/init_iteration.py benchmark/runs/iteration-N` (add `--only 1,2` or `--runs 2` to narrow or repeat), then `git add benchmark/runs/iteration-N && git commit -m "bench: scaffold iteration N"` so a stray `git clean` cannot remove the scaffold. Read `benchmark/runs/iteration-N/runs.json`.
3. **Dispatch** every entry in one turn from the orchestrating Claude Code session: `Agent(subagent_type="general-purpose", name=<agent_name>, prompt=<prompt_for_agent>)`.
4. **On each completion notification** — it carries `total_tokens` and `duration_ms`, which exist nowhere else:
   ```bash
   printf '{"total_tokens": %d, "duration_ms": %d, "total_duration_seconds": %.1f}\n' T MS S > <run_dir>/timing.json
   scripts/finalize_run.sh <run_dir> <agent_name> <session_id>   # -> agent.jsonl, transcript.md, events.json, metrics.json, objective.json, outputs/*
   ```
   Pass your own session id as the third argument — the UUID in your scratchpad path (`/private/tmp/claude-<uid>/<project>/<session_id>/scratchpad`) — rather than relying on the default newest-session-directory discovery: the transcripts live under `~/.claude/projects/<project>/<session_id>/subagents/agent-a<agent_name>-<hash>.jsonl`.
5. **Grade** each run with a grader subagent (`model: sonnet` is enough) using the brief below; it writes `<run_dir>/grading.json`.
6. **Normalise**: `python3 scripts/merge_grading.py benchmark/runs/iteration-N`.
7. **Aggregate**: `cd ~/.claude/skills/skill-creator && python3 -m scripts.aggregate_benchmark <repo>/benchmark/runs/iteration-N --skill-name matt-pocock-superpowers-workflow` → `benchmark.json`, `benchmark.md` (delta = `new_skill` − `old_skill`). The aggregator hard-codes placeholder metadata: patch `benchmark.json` `metadata.executor_model` (the model the subagents ran on) and `metadata.runs_per_configuration` (the `--runs` value, 1 by default) with the real values before writing `analysis.md`.
8. **Analyse**: follow "Analyzing Benchmark Results" in `~/.claude/skills/skill-creator/agents/analyzer.md`; write `benchmark/runs/iteration-N/analysis.md` (non-discriminating assertions, variance, token/time trade-offs, per-arm routing patterns from `objective.json` `skills_invoked`).
9. **Review**: `nohup python3 ~/.claude/skills/skill-creator/eval-viewer/generate_review.py benchmark/runs/iteration-N --skill-name matt-pocock-superpowers-workflow --benchmark benchmark/runs/iteration-N/benchmark.json > /dev/null 2>&1 &` (add `--previous-workspace benchmark/runs/iteration-<N-1>` from iteration 2). Feedback lands in `benchmark/runs/iteration-N/feedback.json`.
10. **Restore** the skill that was active in step 1, commit the iteration (workspaces and `agent.jsonl` are gitignored), and tag.

## Grader brief

```
You are grading one benchmark run. Read ~/.claude/skills/skill-creator/agents/grader.md and follow it.

- expectations (grade each, keep the text verbatim): <assertions from eval_metadata.json>
- transcript_path: <run_dir>/transcript.md
- outputs_dir: <run_dir>/outputs
- objective checks already computed: <run_dir>/objective.json — when an expectation names one (e.g. "objective: tests_pass"), cite that check's evidence; the transcript decides the judged parts. `report_exists` and `no_writes_outside_workspace` are informational: no expectation names them, so they are not graded.
- `objective.json`'s `files_changed` is authoritative for what the agent changed; `outputs/diff.txt` and `git-status.txt` also show scenario-setup state (e.g. the pre-dirtied `src/format.ts` in review-scope).

Write <run_dir>/grading.json with `expectations` (fields exactly: text, passed, evidence), `summary`, `claims`, `user_notes_summary`, and `eval_feedback`. Do NOT include a `timing` field. Reply with the pass count only.
```

## Tests

```bash
scripts/tests/test_prepare_run.sh
scripts/tests/test_finalize_run.sh
python3 -m unittest discover -s scripts/tests -p 'test_*.py'
```
