#!/usr/bin/env bash
# After a benchmark subagent finishes: locate its JSONL transcript, convert it, and run objective grading.
#   scripts/finalize_run.sh <run-dir> <agent-name> [<session-id>]
# The session id defaults to the newest session directory of this project.
# Set BENCH_PROJECT_DIR to override the Claude Code project directory (used by
# scripts/tests/test_finalize_run.sh; defaults to this project's real session directory).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$(cd "${1:?usage: finalize_run.sh <run-dir> <agent-name> [session-id]}" && pwd)"
NAME="${2:?usage: finalize_run.sh <run-dir> <agent-name> [session-id]}"
PROJ="${BENCH_PROJECT_DIR:-$HOME/.claude/projects/-Users-gabrieltutor-my-agent-workflow-skills}"
if [[ -n "${3:-}" ]]; then
  SESSION="$3"
else
  SESSION=""
  for d in $(cd "$PROJ" && ls -td -- */ 2>/dev/null); do
    d="${d%/}"
    if [[ "$d" != "memory" ]]; then SESSION="$d"; break; fi
  done
  [[ -n "$SESSION" ]] || { echo "no session directory found under $PROJ" >&2; exit 1; }
fi
JSONL=""
for f in $(ls -t "$PROJ/$SESSION/subagents/agent-"*.jsonl 2>/dev/null); do
  base="$(basename "$f" .jsonl)"   # agent-<name>-<hash>
  candidate="${base#agent-}"; candidate="${candidate%-*}"
  if [[ "$candidate" == "$NAME" ]]; then JSONL="$f"; break; fi
done
[[ -n "$JSONL" ]] || { echo "no transcript for agent '$NAME' under $PROJ/$SESSION/subagents" >&2; exit 1; }
SCENARIO="$(basename "$(dirname "$(dirname "$RUN_DIR")")" | sed -E 's/^eval-[0-9]+-//')"
cp "$JSONL" "$RUN_DIR/agent.jsonl"
python3 "$REPO/scripts/jsonl_to_transcript.py" "$RUN_DIR/agent.jsonl" "$RUN_DIR"
python3 "$REPO/scripts/grade_run.py" "$RUN_DIR" --scenario "$SCENARIO"
