#!/usr/bin/env bash
# After a benchmark subagent finishes: locate its JSONL transcript, convert it, and run objective grading.
#   scripts/finalize_run.sh <run-dir> <agent-name> [<session-id>]
# The session id defaults to the newest session directory of this project.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$(cd "${1:?usage: finalize_run.sh <run-dir> <agent-name> [session-id]}" && pwd)"
NAME="${2:?usage: finalize_run.sh <run-dir> <agent-name> [session-id]}"
PROJ="$HOME/.claude/projects/-Users-gabrieltutor-my-agent-workflow-skills"
if [[ -n "${3:-}" ]]; then
  SESSION="$3"
else
  SESSION="$(cd "$PROJ" && ls -td -- */ | grep -v '^memory/' | head -1 | tr -d /)"
fi
JSONL="$(ls -t "$PROJ/$SESSION/subagents/agent-$NAME-"*.jsonl 2>/dev/null | head -1 || true)"
[[ -n "$JSONL" ]] || { echo "no transcript for agent '$NAME' under $PROJ/$SESSION/subagents" >&2; exit 1; }
SCENARIO="$(basename "$(dirname "$(dirname "$RUN_DIR")")" | sed -E 's/^eval-[0-9]+-//')"
cp "$JSONL" "$RUN_DIR/agent.jsonl"
python3 "$REPO/scripts/jsonl_to_transcript.py" "$RUN_DIR/agent.jsonl" "$RUN_DIR"
python3 "$REPO/scripts/grade_run.py" "$RUN_DIR" --scenario "$SCENARIO"
