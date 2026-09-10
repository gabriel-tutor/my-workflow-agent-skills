#!/usr/bin/env python3
"""Extract the agent's final `# REPORT` section from its JSONL transcript into outputs/REPORT.md.

Usage: report_from_jsonl.py <run-dir>     (expects <run-dir>/agent.jsonl; writes <run-dir>/outputs/REPORT.md)

The executor prompt asks the subagent to end its final message with a `# REPORT` section; the
harness delivers that message truncated, so the transcript is the reliable source. The whole final
message is kept (review-style answers put their verdict before the section). An existing REPORT.md
is left untouched.
"""
import json
import sys
from pathlib import Path


def extract(jsonl: Path) -> str:
    """The agent's final message: every text block of the last assistant message (grouped by message id).

    The review-style scenarios put their substance *before* the `# REPORT` section, so the whole final
    message is kept rather than just the section.
    """
    groups: dict[str, list[str]] = {}
    order: list[str] = []
    anonymous = 0
    for raw in jsonl.read_text().splitlines():
        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict) or record.get("type") != "assistant":
            continue
        message = record.get("message") or {}
        key = message.get("id")
        if not key:
            anonymous += 1
            key = f"_anon_{anonymous}"
        if key not in groups:
            groups[key] = []
            order.append(key)
        for block in (message.get("content") or []):
            if isinstance(block, dict) and block.get("type") == "text" and block.get("text", "").strip():
                groups[key].append(block["text"].strip())
    for key in reversed(order):  # last message that actually carried text
        if groups[key]:
            return "\n\n".join(groups[key])
    return ""


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 1
    run_dir = Path(argv[1])
    out = run_dir / "outputs" / "REPORT.md"
    if out.exists():
        print(f"{out} already present; left untouched")
        return 0
    text = extract(run_dir / "agent.jsonl")
    if not text:
        print(f"no assistant text found in {run_dir / 'agent.jsonl'}", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text + "\n")
    print(f"wrote {out} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
