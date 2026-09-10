#!/usr/bin/env python3
"""Create the directory tree, eval metadata, prepared workspaces, and dispatch list for one benchmark iteration.

Usage: init_iteration.py <iteration-dir> [--evals benchmark/evals.json]
                         [--configs new_skill,old_skill,without_skill] [--runs 1] [--only 1,3]

For every eval x config x run this calls scripts/prepare_run.sh and records an entry in
<iteration-dir>/runs.json holding the exact agent name and prompt to dispatch.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL_FOR_CONFIG = {
    "new_skill": REPO / "skills" / "matt-pocock-superpowers-workflow" / "SKILL.md",
    "old_skill": REPO / "skills" / "matt-pocock-workflow" / "SKILL.md",
    "without_skill": None,
}
SHORT = {"new_skill": "combo", "old_skill": "mp", "without_skill": "none"}

PROMPT = """Execute this task in a benchmark sandbox.

Working directory: {workspace}
It is a git repository at a baseline commit. Your shell's working directory does not persist between Bash calls: prefix every command with `cd {workspace} &&` or use absolute paths, and never run git/npm commands anywhere else.

{skill_line}

Task from the user:
---
{task}
---

When you are done, write {report} describing: what changed, what you verified (exact commands and observed results), and what remains or could not be verified. Do not modify anything outside the working directory except that report file. Do not ask questions: decide, state your assumptions in the report, and proceed."""

SKILL_LINE = ("Skill to apply: read {skill} first and follow it for this task. "
              "It may direct you to invoke other installed skills; do so with the Skill tool.")
NO_SKILL_LINE = "No particular skill is assigned for this task; work as you normally would."


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("iteration_dir", type=Path)
    ap.add_argument("--evals", type=Path, default=REPO / "benchmark" / "evals.json")
    ap.add_argument("--configs", default="new_skill,old_skill,without_skill")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--only", default="", help="comma-separated eval ids to prepare")
    args = ap.parse_args()

    evals = json.loads(args.evals.read_text())["evals"]
    only = {int(x) for x in args.only.split(",") if x}
    configs = [c for c in args.configs.split(",") if c]
    if not configs:
        print(f"no configs given; --configs must name at least one of: {sorted(SKILL_FOR_CONFIG)}", file=sys.stderr)
        return 1
    unknown = [c for c in configs if c not in SKILL_FOR_CONFIG]
    if unknown:
        print(f"unknown config(s): {unknown}; known: {sorted(SKILL_FOR_CONFIG)}", file=sys.stderr)
        return 1

    iteration = args.iteration_dir.resolve()
    iteration.mkdir(parents=True, exist_ok=True)
    entries = []
    for ev in evals:
        if only and ev["id"] not in only:
            continue
        scenario = ev["scenario"]
        task = (REPO / "benchmark" / "scenarios" / scenario / "prompt.md").read_text().strip()
        eval_dir = iteration / f"eval-{ev['id']}-{scenario}"
        eval_dir.mkdir(exist_ok=True)
        metadata = json.dumps(
            {"eval_id": ev["id"], "eval_name": scenario, "prompt": task, "assertions": ev["expectations"]}, indent=1)
        (eval_dir / "eval_metadata.json").write_text(metadata)
        for config in configs:
            for n in range(1, args.runs + 1):
                run_dir = eval_dir / config / f"run-{n}"
                subprocess.run([str(REPO / "scripts" / "prepare_run.sh"), scenario, str(run_dir)],
                               check=True, capture_output=True, text=True)
                # skill-creator's eval-viewer looks for eval_metadata.json in run_dir and run_dir.parent
                # only, so each run dir gets the same copy as the eval dir two levels up.
                (run_dir / "eval_metadata.json").write_text(metadata)
                skill = SKILL_FOR_CONFIG[config]
                workspace = run_dir / "workspace"
                report = run_dir / "outputs" / "REPORT.md"
                entries.append({
                    "eval_id": ev["id"],
                    "scenario": scenario,
                    "config": config,
                    "run": n,
                    "run_dir": str(run_dir),
                    "workspace": str(workspace),
                    "skill_path": str(skill) if skill else None,
                    "agent_name": f"e{ev['id']}-{SHORT[config]}" + (f"-r{n}" if args.runs > 1 else ""),
                    "prompt_for_agent": PROMPT.format(
                        workspace=workspace,
                        skill_line=SKILL_LINE.format(skill=skill) if skill else NO_SKILL_LINE,
                        task=task,
                        report=report,
                    ),
                })
    (iteration / "runs.json").write_text(json.dumps(entries, indent=1))
    print(f"{len(entries)} runs prepared -> {iteration / 'runs.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
