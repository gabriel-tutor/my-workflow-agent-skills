#!/usr/bin/env bash
# After a benchmark subagent finishes: locate its JSONL transcript, convert it, and run objective grading.
#   scripts/finalize_run.sh <run-dir> <agent-name> [<session-id>]
# The session id defaults to the newest session directory of this project; pass the orchestrating
# session's own id (the UUID in its scratchpad path) to avoid depending on directory mtimes.
# Set BENCH_PROJECT_DIR to override the Claude Code project directory (used by
# scripts/tests/test_finalize_run.sh; defaults to this project's real session directory).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$(cd "${1:?usage: finalize_run.sh <run-dir> <agent-name> [session-id]}" && pwd)"
NAME="${2:?usage: finalize_run.sh <run-dir> <agent-name> [session-id]}"
# Claude Code names the project directory after the repo path with every "/" turned into "-":
# for this repo that is -Users-gabrieltutor-my-agent-workflow-skills.
PROJ="${BENCH_PROJECT_DIR:-$HOME/.claude/projects/$(printf %s "$REPO" | tr / -)}"
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
# Claude Code 2.1.x writes agent-a<name>-<hash>.jsonl (agent id = "a" + name + "-" + 16-hex hash);
# older versions wrote agent-<name>-<hash>.jsonl. Accept both, matching the name exactly.
JSONL=""
for f in $(ls -t "$PROJ/$SESSION/subagents/agent-"*.jsonl 2>/dev/null); do
  base="$(basename "$f" .jsonl)"   # agent-a<name>-<hash> or agent-<name>-<hash>
  candidate="${base#agent-}"; candidate="${candidate%-*}"
  if [[ "$candidate" == "$NAME" || "$candidate" == "a$NAME" ]]; then JSONL="$f"; break; fi
done
[[ -n "$JSONL" ]] || { echo "no transcript for agent '$NAME' under $PROJ/$SESSION/subagents" >&2; exit 1; }
SCENARIO="$(basename "$(dirname "$(dirname "$RUN_DIR")")" | sed -E 's/^eval-[0-9]+-//')"
cp "$JSONL" "$RUN_DIR/agent.jsonl"
python3 "$REPO/scripts/report_from_jsonl.py" "$RUN_DIR"
python3 "$REPO/scripts/jsonl_to_transcript.py" "$RUN_DIR/agent.jsonl" "$RUN_DIR"
python3 "$REPO/scripts/timing_from_run.py" "$RUN_DIR"
python3 "$REPO/scripts/grade_run.py" "$RUN_DIR" --scenario "$SCENARIO"
