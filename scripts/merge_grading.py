#!/usr/bin/env python3
"""Normalise every grading.json in an iteration so aggregate_benchmark.py reads consistent inputs.

- drops `timing` (aggregate_benchmark reads tokens from timing.json only when grading.json has no timing)
- sets `execution_metrics` from metrics.json (+ output_chars = size of outputs/REPORT.md)
- recomputes `summary` from `expectations`

Usage: merge_grading.py <iteration-dir>
"""
import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 1
    count = 0
    for grading in sorted(Path(argv[1]).glob("eval-*/*/run-*/grading.json")):
        run = grading.parent
        data = json.loads(grading.read_text())
        data.pop("timing", None)
        metrics = json.loads((run / "metrics.json").read_text()) if (run / "metrics.json").exists() else {}
        report = run / "outputs" / "REPORT.md"
        data["execution_metrics"] = {
            "tool_calls": metrics.get("tool_calls", {}),
            "total_tool_calls": metrics.get("total_tool_calls", 0),
            "total_steps": metrics.get("total_steps", 0),
            "errors_encountered": metrics.get("errors_encountered", 0),
            "output_chars": report.stat().st_size if report.exists() else 0,
            "transcript_chars": metrics.get("transcript_chars", 0),
        }
        expectations = data.get("expectations", [])
        passed = sum(1 for e in expectations if e.get("passed") is True)
        total = len(expectations)
        data["summary"] = {"passed": passed, "failed": total - passed, "total": total,
                           "pass_rate": round(passed / total, 4) if total else 0.0}
        grading.write_text(json.dumps(data, indent=1))
        count += 1
    print(f"normalised {count} grading files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
