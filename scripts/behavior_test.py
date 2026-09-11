#!/usr/bin/env python3
"""Headless behavior tests for the matt-pocock-workflow plugin (spec section 7).

A run's verdict is its first committing call: a Skill or AskUserQuestion call (a process
choice) or an Edit/Write inside the run's workspace (straight to code). Everything before it
is exploration, including writes outside the workspace (a throwaway script in /tmp).

  behavior_test.py run --scenario S --arm plugin|control [--runs 5] [--jobs 5] [--past-skill]
                       [--superpowers] [--prompt TEXT] [--label NAME] [--timeout 300] [--out DIR]
      Runs `claude -p` in fresh fixture workspaces (scripts/prepare_run.sh S), with --settings
      allowing reads of Matt Pocock's skill files and disabling Superpowers (--superpowers
      keeps the user's own Superpowers setting instead), adding --plugin-dir plugin for the
      plugin arm. Each run stops at its first committing call, at the end of the reply, or at
      the timeout. Keeps every raw stream, appends one record per run to <out>/results.jsonl,
      prints a summary. The prompt defaults to benchmark/scenarios/S/prompt.md.

  behavior_test.py scan [--past-skill] [--workspace DIR] STREAM
      Prints the record for a saved stream-json file.

With --past-skill, Skill calls are recorded (in order, as `skills`) but do not stop the run,
so a test can see what the skill does next: for the grill, its first question. Headless runs
have no AskUserQuestion, so that question arrives as the reply; `text_questions` counts the
question marks in it. `superpowers_skills` counts the superpowers: skills the run loaded.
"""
import argparse
import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "plugin"
PREPARE = REPO / "scripts" / "prepare_run.sh"
SCENARIOS = REPO / "benchmark" / "scenarios"
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
STOP_TOOLS = {"Skill", "AskUserQuestion"} | EDIT_TOOLS


def settings(superpowers: bool) -> str:
    """--settings for a run. Read access to Matt Pocock's skill files (the entries in
    ~/.claude/skills are symlinks, and permission checks use the resolved ~/.skills-manager
    path) and to the plugin's own reference files; a leading // makes a Read rule absolute.
    Superpowers is forced off unless the run keeps the user's own setting."""
    allow = ["Read(~/.claude/skills/**)", "Read(~/.skills-manager/**)", f"Read(/{PLUGIN}/**)"]
    config: dict = {"permissions": {"allow": allow}}
    if not superpowers:
        config["enabledPlugins"] = {"superpowers@claude-plugins-official": False}
    return json.dumps(config)


class Scanner:
    """Follows one run's stream-json events up to its first committing call."""

    def __init__(self, past_skill: bool = False, workspace: Path | None = None):
        self.past_skill = past_skill
        self.workspace = workspace.resolve() if workspace else None
        self.record = {"model": None, "superpowers_skills": None, "first_tool": None,
                       "skill": None, "skills": [], "questions": None, "before": [], "text": "",
                       "result": None, "text_questions": None, "cost_usd": None}
        self.stopped = False

    def feed_line(self, line: str) -> bool:
        """Take one raw stream line, skipping anything that is not a JSON object."""
        try:
            event = json.loads(line)
        except ValueError:
            return False
        return self.feed(event)

    def feed(self, event: object) -> bool:
        """Take one event; True once the first committing call has been seen."""
        if self.stopped or not isinstance(event, dict):
            return self.stopped
        kind = event.get("type")
        if kind == "system" and event.get("subtype") == "init":
            self.record["model"] = event.get("model")
            self.record["superpowers_skills"] = sum(
                1 for s in event.get("skills") or [] if isinstance(s, str) and s.startswith("superpowers:"))
        elif kind == "result":
            self.record["result"] = event.get("result")
            self.record["text_questions"] = (event.get("result") or "").count("?")
            self.record["cost_usd"] = event.get("total_cost_usd")
        elif kind == "assistant":
            content = (event.get("message") or {}).get("content")
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and block.get("text"):
                    self.record["text"] = "\n".join(filter(None, (self.record["text"], block["text"])))
                elif block.get("type") == "tool_use" and self._commit(block):
                    return True
        return False

    def _commit(self, block: dict) -> bool:
        name, inputs = block.get("name"), block.get("input") or {}
        if name not in STOP_TOOLS:
            self.record["before"].append(name)
            return False
        if name in EDIT_TOOLS and self._outside_workspace(inputs):
            self.record["before"].append(f"{name}(outside)")
            return False
        if name == "Skill":
            self.record["skills"].append(inputs.get("skill"))
            self.record["skill"] = self.record["skill"] or inputs.get("skill")
            if self.past_skill:
                return False
        elif name == "AskUserQuestion":
            self.record["questions"] = len(inputs.get("questions") or [])
        self.record["first_tool"] = name
        self.stopped = True
        return True

    def _outside_workspace(self, inputs: dict) -> bool:
        """True for an edit whose target lies outside the run's workspace."""
        raw = inputs.get("file_path") or inputs.get("notebook_path")
        if self.workspace is None or not raw:
            return False
        path = Path(raw)
        if not path.is_absolute():
            path = self.workspace / path
        return not path.resolve().is_relative_to(self.workspace)


def scan(stream: Path, past_skill: bool = False, workspace: Path | None = None) -> dict:
    scanner = Scanner(past_skill, workspace)
    for line in stream.read_text().splitlines():
        if scanner.feed_line(line):
            break
    return scanner.record


def stop(proc: subprocess.Popen, sig: int) -> None:
    """Signal the run's whole process group (claude plus the MCP servers it started), falling
    back to claude alone when the group cannot be signalled (macOS can refuse with EPERM)."""
    try:
        os.killpg(proc.pid, sig)
    except ProcessLookupError:
        pass
    except OSError:
        try:
            proc.send_signal(sig)
        except OSError:
            pass


def run_once(scenario: str, arm: str, prompt: str, run_dir: Path, timeout: float,
             past_skill: bool, superpowers: bool) -> dict:
    run_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(PREPARE), scenario, str(run_dir)], check=True, capture_output=True)
    workspace = run_dir / "workspace"
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--settings", settings(superpowers)]
    if arm == "plugin":
        cmd += ["--plugin-dir", str(PLUGIN)]
    scanner, expired = Scanner(past_skill, workspace), threading.Event()
    started = time.monotonic()
    with open(run_dir / "stream.jsonl", "w") as raw, open(run_dir / "stderr.txt", "w") as err:
        proc = subprocess.Popen(cmd, cwd=workspace, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=err, text=True, start_new_session=True)
        timer = threading.Timer(timeout, lambda: (expired.set(), stop(proc, signal.SIGKILL)))
        timer.start()
        try:
            for line in proc.stdout:
                raw.write(line)
                if scanner.feed_line(line):
                    break
        finally:
            timer.cancel()
            if proc.poll() is None:
                stop(proc, signal.SIGTERM)
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    stop(proc, signal.SIGKILL)
                    proc.wait()
    return {**scanner.record, "seconds": round(time.monotonic() - started),
            "timed_out": expired.is_set(), "stream": str(run_dir / "stream.jsonl")}


def verdict(record: dict) -> str:
    if record["first_tool"] == "Skill":
        return f"Skill {record['skill']}"
    if record["first_tool"]:
        return record["first_tool"]
    if record.get("timed_out"):
        return "timeout"
    return "reply" if record["result"] is not None else "no commit"


def print_summary(label: str, arm: str, out: Path, records: list[dict]) -> None:
    print(f"{label} [{arm}] x{len(records)} -> {out}")
    for r in records:
        before = ",".join(r["before"]) or "-"
        skills = ",".join(s or "?" for s in r["skills"]) or "-"
        marks = "-" if r["text_questions"] is None else r["text_questions"]
        print(f"  run {r['run']}: {verdict(r):40} skills={skills:44.44} ?={marks!s:<3}"
              f" sp={r['superpowers_skills']!s:<3} before={before:24.24} {r['seconds']:>4}s")
    counts = Counter(verdict(r) for r in records)
    print("  first committing call: " + ", ".join(f"{k} x{v}" for k, v in counts.most_common()))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Headless behavior tests for the plugin.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    scan_p = sub.add_parser("scan", help="print the record for a saved stream")
    scan_p.add_argument("--past-skill", action="store_true")
    scan_p.add_argument("--workspace", type=Path)
    scan_p.add_argument("stream", type=Path)
    run_p = sub.add_parser("run", help="run headless sessions and record their first commits")
    run_p.add_argument("--scenario", required=True)
    run_p.add_argument("--arm", choices=("plugin", "control"), required=True)
    run_p.add_argument("--runs", type=int, default=5)
    run_p.add_argument("--jobs", type=int, default=5)
    run_p.add_argument("--past-skill", action="store_true")
    run_p.add_argument("--superpowers", action="store_true",
                       help="keep the user's own Superpowers setting instead of forcing it off")
    run_p.add_argument("--prompt")
    run_p.add_argument("--label")
    run_p.add_argument("--timeout", type=float, default=300)
    run_p.add_argument("--out", type=Path)
    args = parser.parse_args(argv)

    if args.cmd == "scan":
        print(json.dumps(scan(args.stream, args.past_skill, args.workspace)))
        return 0

    prompt = args.prompt or (SCENARIOS / args.scenario / "prompt.md").read_text().strip()
    label = args.label or args.scenario
    out = args.out or Path(tempfile.mkdtemp(prefix=f"mpw-{label}-{args.arm}-"))
    out.mkdir(parents=True, exist_ok=True)

    def one(n: int) -> dict:
        record = run_once(args.scenario, args.arm, prompt, out / f"{args.arm}-{n}",
                          args.timeout, args.past_skill, args.superpowers)
        return {"label": label, "scenario": args.scenario, "arm": args.arm,
                "superpowers": args.superpowers, "run": n, **record}

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        records = list(pool.map(one, range(1, args.runs + 1)))
    with open(out / "results.jsonl", "a") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")
    print_summary(label, args.arm, out, records)
    return 0


if __name__ == "__main__":
    sys.exit(main())
