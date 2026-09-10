#!/usr/bin/env python3
"""Fold the token usage of nested subagents into a run's timing.json.

Usage: nested_usage.py <run-dir> <session-subagents-dir>

A benchmark subagent may dispatch its own subagents (reviewers, researchers); their transcripts sit
beside the parent's in the session's subagents/ directory with a `parentAgentId` in `.meta.json`.
This finds every descendant of the run's agent (by agentId, recursively), converts each transcript
with jsonl_to_transcript.convert to get deduplicated usage, and rewrites timing.json so that
`total_tokens` = coordinator + nested; the coordinator-only figure is kept as `coordinator_tokens`.
Idempotent: re-running recomputes from `coordinator_tokens` when present.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jsonl_to_transcript import convert  # noqa: E402


def agent_id_of(jsonl: Path) -> str:
    for raw in jsonl.read_text().splitlines():
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict) and rec.get("agentId"):
            return rec["agentId"]
    return ""


def descendants(root_id: str, subagents: Path) -> list[Path]:
    parent_of = {}
    for meta in subagents.glob("agent-*.meta.json"):
        try:
            data = json.loads(meta.read_text())
        except json.JSONDecodeError:
            continue
        pid = data.get("parentAgentId")
        if pid:
            parent_of[meta.name[len("agent-"):-len(".meta.json")]] = pid
    found, frontier = [], [root_id]
    while frontier:
        current = frontier.pop()
        for child, pid in parent_of.items():
            if pid == current:
                jsonl = subagents / f"agent-{child}.jsonl"
                if jsonl.exists():
                    found.append(jsonl)
                    frontier.append(child)
    return found


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 1
    run_dir, subagents = Path(argv[1]), Path(argv[2])
    timing = json.loads((run_dir / "timing.json").read_text())
    coordinator = timing.get("coordinator_tokens", timing["total_tokens"])
    root_id = agent_id_of(run_dir / "agent.jsonl")
    nested_tokens, nested = 0, []
    for jsonl in descendants(root_id, subagents):
        tmp = Path(tempfile.mkdtemp())
        convert(jsonl, tmp)
        usage = json.loads((tmp / "metrics.json").read_text())["usage"]
        tokens = sum(int(usage.get(k, 0)) for k in
                     ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
        nested_tokens += tokens
        nested.append({"agent": jsonl.name, "tokens": tokens})
    timing.update({
        "coordinator_tokens": coordinator,
        "nested_agents": len(nested),
        "nested_tokens": nested_tokens,
        "nested": nested,
        "total_tokens": coordinator + nested_tokens,
    })
    (run_dir / "timing.json").write_text(json.dumps(timing, indent=1))
    print(f"{run_dir.name}: coordinator {coordinator:,} + nested {nested_tokens:,} ({len(nested)} agents) = {coordinator + nested_tokens:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
