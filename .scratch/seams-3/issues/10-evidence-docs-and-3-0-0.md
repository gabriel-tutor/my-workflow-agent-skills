# 10: Evidence, docs, and 3.0.0

**What to build:** The README says only what the run records support, and the plugin ships as 3.0.0. Run the six routing scenarios at five runs each on the new bootstrap and the four gate scenarios at three runs each, through `--assert`; write the results to `docs/plugin-behavior-tests.md` as counts (runs matching, refusals seen, failed calls, exclusions with their reasons). Rewrite the README's workflow and evidence sections: what a refusal looks like and how to turn the gate off (disable the plugin), the lifecycle past the merge, the three flow graphs updated for the gate, release and incident, a compatibility section pointing at `docs/compatibility.md`, and "what it won't do" (the shell mesh, the outcome matrix not evidenced, model judgment inside a skill). Update the CHANGELOG with a 3.0.0 entry grouped by the review's finding ids, and set 3.0.0 in `plugin.json` and `marketplace.json`. CI is green on both platforms before the push; the push happens only on the user's yes.

**Blocked by:** 02, 03, 07, 08, 09

**Status:** ready-for-agent

- [ ] `docs/plugin-behavior-tests.md` reports the ten scenarios with counts that match the run records under `tests/runs/`.
- [ ] README: gate section, lifecycle section, updated graphs, evidence tables, compatibility pointer, what it won't do; no cost figures; no claim beyond the records.
- [ ] CHANGELOG 3.0.0 entry; version 3.0.0 in both manifests; `claude plugin validate --strict` passes for both.
- [ ] `scripts/test.sh` green locally; CI green on macOS and Ubuntu for the pushed commit.
- [ ] The local install reports 3.0.0 after `claude plugin update`, and a new session shows the 3.0 bootstrap.

**How to verify:** `scripts/test.sh`; `python3 scripts/behavior_test.py run --all --arm plugin --assert` exits 0; `gh run list --limit 2` shows green for both jobs; `claude plugin list` shows `matt-pocock-workflow@my-workflow-agent-skills 3.0.0`.

## Comments

From ticket 03: README's evidence section says "the plugin's guard line gives Matt Pocock's skills every overlap" about the 2.x runs; since ticket 03 that sentence lives in `routing.md` and the gate (ticket 01) enforces the precedence. The rewrite should describe the 3.0 mechanism and cite the 3.0 runs.
