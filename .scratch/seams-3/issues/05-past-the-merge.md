# 05: Past the merge

**What to build:** The workflow continues to production. A new `release` skill takes an integrated candidate through readiness (a table: integrated candidate, suite green on that SHA, artifact built and identified, config and variable names per environment, migration and rehearsed restore when data changes shape, abort conditions and rollback path, the applicable checks, the smoke plan; anything unmet blocks), deploys only after an explicit yes naming target, environment and candidate (staged environment first when one exists, through the platform's own skill or CLI), verifies (running version equals the candidate, smoke journeys, a short watch, the abort path on failure), and hands over operations (monitoring and alert owner, runbook, follow-ups, stage reached), with a target table that scales the steps to a web host, container or VPS, mobile store, CLI or library registry, browser extension store, or desktop, handing person-only store steps to the user. `foundations` surveys deploy target and pipeline, environments and config, backups and restore, monitoring and alerts, dependency and secret scanning, skipping them for libraries and scripts, and offers to write the CI or deploy workflow, `.env.example` and a runbook skeleton. `to-spec` adds a Release subsection when the work ships anywhere. `to-tickets` makes the walking skeleton ticket 01 for a new app, turns the lens's negative cases into acceptance criteria, and ends with a release ticket when the spec ships. `implement`'s handover names the stage reached.

**Blocked by:** 04

**Status:** ready-for-agent

- [ ] `release` has the gate, the readiness table with the blocking rule, the explicit-yes deploy step, the verify step with the abort path, the operations handover, and the target table.
- [ ] `release` never deploys on an inherited yes: the deploy question names target, environment and candidate every time.
- [ ] `foundations` has the five production rows with their "what counts as present" and their skip rule, and the new offers.
- [ ] `to-spec` has the Release subsection rule; `to-tickets` has the walking skeleton, negative-criteria and release-ticket rules; `implement`'s Next section names the stage reached from the six stages.
- [ ] Content guards for the required headings of `release` and the new rows of `foundations`.
- [ ] A headless `foundations` run on `tests/fixture` reports the five new rows (as not applicable or missing) without writing anything.
- [ ] A headless `release` run on `tests/fixture` stops at readiness with "no deploy target" and asks, deploying nothing.

**How to verify:** `scripts/test.sh`; then `claude -p` in a fixture copy with "/matt-pocock-workflow:foundations" and with "release this": the first prints a survey table with the five new rows and asks; the second prints a readiness table whose target row is unmet and asks for the target.
