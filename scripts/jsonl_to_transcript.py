#!/usr/bin/env python3
"""Convert a Claude Code subagent JSONL transcript into grader-friendly files.

Usage: jsonl_to_transcript.py <agent.jsonl> <run-dir>

Writes <run-dir>/events.json (ordered tool calls), <run-dir>/metrics.json (counts + token usage),
and <run-dir>/transcript.md (prompt, assistant text, tool calls, truncated tool results).
Thinking blocks are deliberately omitted from transcript.md.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

RESULT_TRUNCATE = 400
COMMAND_TRUNCATE = 600

# Heuristics for files a Bash command writes. Relative paths are relative to the subagent's cwd,
# which the benchmark tells it to make the workspace. Every match is kept; grade_run.py filters.
_REDIRECT = re.compile(r"(?:^|[\s;&|(])>{1,2}\s*([^\s;&|)]+)")
_TEE = re.compile(r"\btee\s+(?:-a\s+)?([^\s;&|]+)")
_CP_MV = re.compile(r"\b(?:cp|mv)\s+(?:-\S+\s+)*\S+\s+([^\s;&|]+)")
_TOUCH = re.compile(r"\btouch\s+([^\s;&|]+)")
_SED_I = re.compile(r"\bsed\s+-i\b")


def bash_writes(command: str) -> list[str]:
    writes: list[str] = []
    for line in command.splitlines():
        for rx in (_REDIRECT, _TEE, _CP_MV, _TOUCH):
            writes.extend(rx.findall(line))
        for segment in re.split(r"\s*(?:&&|\|\||;|\|)\s*", line):
            if _SED_I.search(segment):
                tokens = segment.split()
                if tokens:
                    writes.append(tokens[-1])
    seen: set[str] = set()
    out: list[str] = []
    for w in writes:
        w = w.strip("'\"")
        if w in ("/dev/null", "&1", "&2") or w.startswith("&") or w in seen:
            continue
        seen.add(w)
        out.append(w)
    return out


def _blocks(record: dict) -> list:
    message = record.get("message")
    if not isinstance(message, dict):
        return []
    content = message.get("content")
    return content if isinstance(content, list) else []


def _result_text(block: dict) -> str:
    content = block.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict))
    return ""


def convert(jsonl_path: Path, run_dir: Path) -> None:
    events: list[dict] = []
    tool_calls: Counter = Counter()
    usage: Counter = Counter()
    steps = 0
    errors = 0
    malformed = 0
    lines_md: list[str] = ["# Transcript", ""]
    call_names: dict[str, str] = {}

    for raw in jsonl_path.read_text().splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            malformed += 1
            continue
        rtype = record.get("type")
        ts = record.get("timestamp", "")

        if rtype == "user":
            message = record.get("message") or {}
            content = message.get("content")
            if isinstance(content, str):
                lines_md += ["## Prompt", "", content.strip(), ""]
                continue
            for block in _blocks(record):
                if block.get("type") != "tool_result":
                    continue
                is_error = bool(block.get("is_error"))
                errors += is_error
                text = _result_text(block).strip()
                if len(text) > RESULT_TRUNCATE:
                    text = text[:RESULT_TRUNCATE] + f"… [{len(text)} chars]"
                name = call_names.get(block.get("tool_use_id", ""), "tool")
                lines_md += [f"> **{name} result{' (error)' if is_error else ''}:** {text}", ""]

        elif rtype == "assistant":
            steps += 1
            for key, value in ((record.get("message") or {}).get("usage") or {}).items():
                if isinstance(value, int):
                    usage[key] += value
            for block in _blocks(record):
                btype = block.get("type")
                if btype == "text" and block.get("text", "").strip():
                    lines_md += [block["text"].strip(), ""]
                elif btype == "tool_use":
                    name = block.get("name", "?")
                    inp = block.get("input") or {}
                    tool_calls[name] += 1
                    call_names[block.get("id", "")] = name
                    event: dict = {"i": len(events), "ts": ts, "tool": name}
                    if name == "Skill":
                        event["skill"] = inp.get("skill", "")
                        summary = event["skill"]
                    elif name == "Bash":
                        cmd = inp.get("command", "")
                        event["command"] = cmd[:COMMAND_TRUNCATE]
                        event["writes"] = bash_writes(cmd)
                        summary = "`" + cmd.replace("\n", " ⏎ ")[:200] + "`"
                    elif name in ("Write", "Edit", "MultiEdit", "NotebookEdit", "Read"):
                        event["path"] = inp.get("file_path") or inp.get("notebook_path") or ""
                        summary = event["path"]
                    elif name == "Agent":
                        event["description"] = inp.get("description", "")
                        summary = event["description"]
                    else:
                        summary = json.dumps(inp)[:200]
                    events.append(event)
                    lines_md += [f"- [{event['i']}] **{name}** {summary}", ""]

    transcript = "\n".join(lines_md)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "transcript.md").write_text(transcript)
    (run_dir / "events.json").write_text(json.dumps(events, indent=1))
    metrics = {
        "tool_calls": dict(tool_calls),
        "total_tool_calls": sum(tool_calls.values()),
        "total_steps": steps,
        "errors_encountered": errors,
        "malformed_lines": malformed,
        "transcript_chars": len(transcript),
        "usage": {
            k: usage.get(k, 0)
            for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
        },
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=1))


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 1
    convert(Path(argv[1]), Path(argv[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
