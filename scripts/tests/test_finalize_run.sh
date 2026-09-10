#!/usr/bin/env bash
# Tests scripts/finalize_run.sh: session-dir discovery must skip memory/ and pick the newest
# real session without piping through head (SIGPIPE-safe), and transcript lookup must match
# the agent name exactly rather than as a glob prefix, under both filename conventions:
# agent-a<name>-<hash>.jsonl (Claude Code 2.1.x: agent id = "a" + name + "-" + hash) and the
# legacy agent-<name>-<hash>.jsonl.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
fail() { echo "FAIL: $*" >&2; exit 1; }

FIXTURE="$REPO/scripts/tests/fixtures/sample-subagent.jsonl"

# Fake project tree: memory/, an older session s-old/, and a newer session s-new/subagents/
# holding three transcripts in the real 2.1.x convention (agent id "a" + name + "-" + hash).
# agent-ae2-none-r2-bbbbbbbb.jsonl is a newer file whose name is only a glob-prefix match for agent
# name "e2-none" (it's really "e2-none-r2"); agent-ae2-none-aaaaaaaa.jsonl is the older file that is
# the exact-name match. Exact-name matching must pick the latter. agent-e2-mp-cccccccc.jsonl uses the
# legacy convention (no "a" prefix) and must still be found for agent name "e2-mp".
PROJ="$TMP/proj"
mkdir -p "$PROJ/memory" "$PROJ/s-old/subagents" "$PROJ/s-new/subagents"

cp "$FIXTURE" "$PROJ/s-new/subagents/agent-ae2-none-aaaaaaaa.jsonl"
touch -t 202601010003 "$PROJ/s-new/subagents/agent-ae2-none-aaaaaaaa.jsonl"
cp "$FIXTURE" "$PROJ/s-new/subagents/agent-ae2-none-r2-bbbbbbbb.jsonl"
touch -t 202601010004 "$PROJ/s-new/subagents/agent-ae2-none-r2-bbbbbbbb.jsonl"
cp "$FIXTURE" "$PROJ/s-new/subagents/agent-e2-mp-cccccccc.jsonl"
touch -t 202601010005 "$PROJ/s-new/subagents/agent-e2-mp-cccccccc.jsonl"

# Set directory mtimes last, after the copies above may have touched their parents: memory/ is the
# newest of all three (must still be skipped), s-new/ is the newest real session (must be picked),
# s-old/ is older still.
touch -t 202601010101 "$PROJ/s-old"
touch -t 202601010102 "$PROJ/s-new"
touch -t 202601010103 "$PROJ/memory"

RUN_DIR="$TMP/it/eval-2-cosmetic-edit/without_skill/run-1"
"$REPO/scripts/prepare_run.sh" cosmetic-edit "$RUN_DIR" >/dev/null

BENCH_PROJECT_DIR="$PROJ" "$REPO/scripts/finalize_run.sh" "$RUN_DIR" e2-none >/dev/null

cmp -s "$RUN_DIR/agent.jsonl" "$PROJ/s-new/subagents/agent-ae2-none-aaaaaaaa.jsonl" \
  || fail "agent.jsonl should be byte-identical to the exact-name match, not the newer prefix match"
[[ -f "$RUN_DIR/transcript.md" ]] || fail "transcript.md missing"
[[ -f "$RUN_DIR/events.json" ]] || fail "events.json missing"
[[ -f "$RUN_DIR/metrics.json" ]] || fail "metrics.json missing"
[[ -f "$RUN_DIR/objective.json" ]] || fail "objective.json missing"
grep -q '"scenario": "cosmetic-edit"' "$RUN_DIR/objective.json" || fail "objective.json missing scenario key"

# Legacy convention: a second run dir for agent "e2-mp" must resolve to agent-e2-mp-cccccccc.jsonl.
RUN_DIR2="$TMP/it/eval-2-cosmetic-edit/old_skill/run-1"
"$REPO/scripts/prepare_run.sh" cosmetic-edit "$RUN_DIR2" >/dev/null
BENCH_PROJECT_DIR="$PROJ" "$REPO/scripts/finalize_run.sh" "$RUN_DIR2" e2-mp >/dev/null
cmp -s "$RUN_DIR2/agent.jsonl" "$PROJ/s-new/subagents/agent-e2-mp-cccccccc.jsonl" \
  || fail "agent.jsonl should be the legacy-named transcript for agent e2-mp"
[[ -f "$RUN_DIR2/objective.json" ]] || fail "objective.json missing for the legacy-named run"

# timing.json is derived from the transcript (fixture spans 7 s) and never overwritten
grep -q '"duration_ms": 7000' "$RUN_DIR/timing.json" || fail "derived duration_ms should be 6000, got: $(cat "$RUN_DIR/timing.json")"
grep -q '"total_tokens": ' "$RUN_DIR/timing.json" || fail "derived total_tokens missing"
printf '{"total_tokens": 1, "duration_ms": 1, "total_duration_seconds": 0.0}\n' > "$RUN_DIR/timing.json"
python3 "$REPO/scripts/timing_from_run.py" "$RUN_DIR" >/dev/null
grep -q '"total_tokens": 1,' "$RUN_DIR/timing.json" || fail "existing timing.json must be left untouched"

echo "test_finalize_run: OK"
