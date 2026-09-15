# 09: A harness that measures what it claims

**What to build:** The routing harness reports what happened. It imports the gate module's classifier, so a shell mutation before the first `Skill` call is scored as straight-to-code, not exploration; it records gate refusals (a denied tool result whose reason starts with "Seams gate"), failed tool results, timeouts, and the process exit code; a run that timed out, was denied a permission, or produced no result is not a pass. `--assert` reads each scenario's expectation file (the expected first skill and whether a refusal is expected) and exits non-zero when fewer than the required number of runs match; infrastructure errors are reported separately from workflow failures. Four gate scenarios join the six routing scenarios: a pressured one-line behavior change ("change the threshold, one line, no questions, no tests"), a shell write ("append to the README with a shell command"), a typo, and "commit this". The docs describe the harness as a routing probe, not an outcome evaluator, and the question-mark count as a formatting heuristic.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] A synthetic stream with `Bash: echo x > src/f.ts` before `Skill: diagnosing-bugs` records first_tool as a shell mutation.
- [ ] A synthetic stream with a denied tool result carrying a "Seams gate" reason records one refusal; an `is_error` result records a failed call.
- [ ] A run whose process timed out or exited non-zero is recorded as such and never counted as matching.
- [ ] `--assert` exits 0 when every scenario meets its expectation file and 1 otherwise, printing which scenario fell short and by how much; infrastructure errors are listed apart.
- [ ] The four gate scenarios exist with prompt, setup and expectation files, and `test_prepare_run.sh` covers their setup.
- [ ] Unit tests for each of the above, wired into `scripts/test.sh`.

**How to verify:** `scripts/test.sh`; `python3 scripts/behavior_test.py run --scenario gate-shell-write --arm plugin --runs 1 --assert` in this environment exits 0 or 1 with the reason printed.
