#!/usr/bin/env python3
"""Derive timing.json for a run from its transcript when the harness supplies no completion metrics.

Usage: timing_from_run.py <run-dir>     (expects <run-dir>/agent.jsonl and <run-dir>/metrics.json)

total_tokens   = input + output + cache_read + cache_creation from metrics.json (already deduplicated
                 per assistant message id by jsonl_to_transcript.py)
duration_ms    = last record timestamp - first record timestamp in agent.jsonl
Existing timing.json files are left untouched so harness-supplied numbers always win.
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def timing(run_dir: Path) -> dict:
    metrics = json.loads((run_dir / "metrics.json").read_text())
    usage = metrics.get("usage", {})
    total_tokens = sum(int(usage.get(k, 0)) for k in
                       ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
    stamps = []
    for raw in (run_dir / "agent.jsonl").read_text().splitlines():
        try:
            ts = json.loads(raw).get("timestamp")
        except (json.JSONDecodeError, AttributeError):
            continue
        if isinstance(ts, str):
            stamps.append(datetime.fromisoformat(ts.replace("Z", "+00:00")))
    duration_ms = int((max(stamps) - min(stamps)).total_seconds() * 1000) if stamps else 0
    return {
        "total_tokens": total_tokens,
        "duration_ms": duration_ms,
        "total_duration_seconds": round(duration_ms / 1000, 1),
        "source": "derived from agent.jsonl timestamps and deduplicated usage",
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 1
    run_dir = Path(argv[1])
    out = run_dir / "timing.json"
    if out.exists():
        print(f"timing.json already present in {run_dir}; left untouched")
        return 0
    out.write_text(json.dumps(timing(run_dir), indent=1))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
