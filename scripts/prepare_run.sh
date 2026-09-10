#!/usr/bin/env bash
# Prepare one benchmark run workspace.
#   scripts/prepare_run.sh <scenario> <run-dir>
# Produces <run-dir>/workspace (fresh fixture copy at a git baseline with the scenario's setup applied),
# <run-dir>/baseline.txt (HEAD after setup), <run-dir>/baseline-manifest.json, <run-dir>/outputs/.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCENARIO="${1:?usage: prepare_run.sh <scenario> <run-dir>}"
RUN_DIR="$(mkdir -p "${2:?usage: prepare_run.sh <scenario> <run-dir>}" && cd "$2" && pwd)"
FIXTURE="$REPO/benchmark/fixture"
SETUP="$REPO/benchmark/scenarios/$SCENARIO/setup.sh"
[[ -f "$SETUP" ]] || { echo "no such scenario: $SCENARIO" >&2; exit 1; }
[[ -d "$FIXTURE/node_modules" ]] || { echo "run 'npm install' in $FIXTURE first" >&2; exit 1; }

WS="$RUN_DIR/workspace"
rm -rf "$WS"
mkdir -p "$RUN_DIR/outputs"
rsync -a --exclude node_modules --exclude .git "$FIXTURE/" "$WS/"
ln -s "$FIXTURE/node_modules" "$WS/node_modules"

export GIT_AUTHOR_NAME=bench GIT_AUTHOR_EMAIL=bench@example.com
export GIT_COMMITTER_NAME=bench GIT_COMMITTER_EMAIL=bench@example.com
(
  cd "$WS"
  git init -q -b main
  git add -A
  git commit -qm "baseline: OrderKit fixture"
  bash "$SETUP"
  git rev-parse HEAD > "$RUN_DIR/baseline.txt"
)
python3 "$REPO/scripts/manifest.py" "$WS" "$RUN_DIR/baseline-manifest.json"
echo "prepared $SCENARIO in $WS (baseline $(cat "$RUN_DIR/baseline.txt"))"
