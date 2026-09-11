#!/usr/bin/env python3
"""Headless behavior tests for the matt-pocock-workflow plugin (spec section 7).

A run's verdict is its first committing call: a Skill or AskUserQuestion call (a process
choice) or an Edit/Write (straight to code). Everything before it is exploration.

  behavior_test.py run --scenario S --arm plugin|control [--runs 5] [--jobs 5]
                       [--prompt TEXT] [--label NAME] [--timeout 300] [--out DIR]
      Runs `claude -p` in fresh fixture workspaces (scripts/prepare_run.sh S) with Superpowers
      disabled through --settings, adding --plugin-dir plugin for the plugin arm. Each run
      stops at its first committing call, at the end of the reply, or at the timeout. Keeps
      every raw stream, appends one record per run to <out>/results.jsonl, prints a summary.
      The prompt defaults to benchmark/scenarios/S/prompt.md.

  behavior_test.py scan STREAM
      Prints the record for a saved stream-json file.
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
SETTINGS = json.dumps({"enabledPlugins": {"superpowers@claude-plugins-official": False}})
STOP_TOOLS = {"Skill", "AskUserQuestion", "Edit", "Write", "MultiEdit", "NotebookEdit"}


class Scanner:
    """Follows one run's stream-json events up to its first committing call."""

    def __init__(self):
        self.record = {"model": None, "first_tool": None, "skill": None, "questions": None,
                       "before": [], "text": "", "result": None, "cost_usd": None}
        self.stopped = False

    def feed(self, event) -> bool:
        """Take one event; True once the first committing call has been seen."""
        if self.stopped or not isinstance(event, dict):
            return self.stopped
        kind = event.get("type")
        if kind == "system" and event.get("subtype") == "init":
            self.record["model"] = event.get("model")
        elif kind == "result":
            self.record["result"] = event.get("result")
            self.record["cost_usd"] = event.get("total_cost_usd")
        elif kind == "assistant":
            for block in (event.get("message") or {}).get("content") or []:
                if block.get("type") == "text" and block.get("text"):
                    self.record["text"] = "\n".join(filter(None, (self.record["text"], block["text"])))
                elif block.get("type") == "tool_use" and self._commit(block):
                    return True
        return False

    def _commit(self, block) -> bool:
        name, inputs = block.get("name"), block.get("input") or {}
        if name not in STOP_TOOLS:
            self.record["before"].append(name)
            return False
        self.record["first_tool"] = name
        if name == "Skill":
            self.record["skill"] = inputs.get("skill")
        elif name == "AskUserQuestion":
            self.record["questions"] = len(inputs.get("questions") or [])
        self.stopped = True
        return True


def scan(stream: Path) -> dict:
    scanner = Scanner()
    for line in stream.read_text().splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if scanner.feed(event):
            break
    return scanner.record


def stop(proc: subprocess.Popen, sig: int) -> None:
    """Signal the run's whole process group (claude plus the MCP servers it started)."""
    try:
        os.killpg(proc.pid, sig)
    except ProcessLookupError:
        pass


def run_once(scenario: str, arm: str, prompt: str, run_dir: Path, timeout: float) -> dict:
    run_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(["bash", str(PREPARE), scenario, str(run_dir)], check=True, capture_output=True)
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "acceptEdits", "--settings", SETTINGS]
    if arm == "plugin":
        cmd += ["--plugin-dir", str(PLUGIN)]
    scanner, expired = Scanner(), threading.Event()
    started = time.monotonic()
    with open(run_dir / "stream.jsonl", "w") as raw, open(run_dir / "stderr.txt", "w") as err:
        proc = subprocess.Popen(cmd, cwd=run_dir / "workspace", stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=err, text=True, start_new_session=True)
        timer = threading.Timer(timeout, lambda: (expired.set(), stop(proc, signal.SIGKILL)))
        timer.start()
        try:
            for line in proc.stdout:
                raw.write(line)
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if scanner.feed(event):
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
    return "timeout" if record.get("timed_out") else "no commit"


def print_summary(label: str, arm: str, out: Path, records: list) -> None:
    print(f"{label} [{arm}] x{len(records)} -> {out}")
    for r in records:
        before = ",".join(r["before"]) or "-"
        print(f"  run {r['run']}: {verdict(r):44} before={before:32.32} {r['seconds']:>4}s")
    counts = Counter(verdict(r) for r in records)
    print("  first committing call: " + ", ".join(f"{k} x{v}" for k, v in counts.most_common()))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Headless behavior tests for the plugin.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    scan_p = sub.add_parser("scan", help="print the record for a saved stream")
    scan_p.add_argument("stream", type=Path)
    run_p = sub.add_parser("run", help="run headless sessions and record their first commits")
    run_p.add_argument("--scenario", required=True)
    run_p.add_argument("--arm", choices=("plugin", "control"), required=True)
    run_p.add_argument("--runs", type=int, default=5)
    run_p.add_argument("--jobs", type=int, default=5)
    run_p.add_argument("--prompt")
    run_p.add_argument("--label")
    run_p.add_argument("--timeout", type=float, default=300)
    run_p.add_argument("--out", type=Path)
    args = parser.parse_args(argv)

    if args.cmd == "scan":
        print(json.dumps(scan(args.stream)))
        return 0

    prompt = args.prompt or (SCENARIOS / args.scenario / "prompt.md").read_text().strip()
    label = args.label or args.scenario
    out = args.out or Path(tempfile.mkdtemp(prefix=f"mpw-{label}-{args.arm}-"))
    out.mkdir(parents=True, exist_ok=True)

    def one(n: int) -> dict:
        record = run_once(args.scenario, args.arm, prompt, out / f"{args.arm}-{n}", args.timeout)
        return {"label": label, "scenario": args.scenario, "arm": args.arm, "run": n, **record}

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        records = list(pool.map(one, range(1, args.runs + 1)))
    with open(out / "results.jsonl", "a") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")
    print_summary(label, args.arm, out, records)
    return 0


if __name__ == "__main__":
    sys.exit(main())
