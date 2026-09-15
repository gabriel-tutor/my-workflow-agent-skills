# 05: Past the merge

**What to build:** The workflow continues to production. A new `release` skill takes an integrated candidate through readiness (a table: integrated candidate, suite green on that SHA, artifact built and identified, config and variable names per environment, migration and rehearsed restore when data changes shape, abort conditions and rollback path, the applicable checks, the smoke plan; anything unmet blocks), deploys only after an explicit yes naming target, environment and candidate (staged environment first when one exists, through the platform's own skill or CLI), verifies (running version equals the candidate, smoke journeys, a short watch, the abort path on failure), and hands over operations (monitoring and alert owner, runbook, follow-ups, stage reached), with a target table that scales the steps to a web host, container or VPS, mobile store, CLI or library registry, browser extension store, or desktop, handing person-only store steps to the user. `foundations` surveys deploy target and pipeline, environments and config, backups and restore, monitoring and alerts, dependency and secret scanning, skipping them for libraries and scripts, and offers to write the CI or deploy workflow, `.env.example` and a runbook skeleton. `to-spec` adds a Release subsection when the work ships anywhere. `to-tickets` makes the walking skeleton ticket 01 for a new app, turns the lens's negative cases into acceptance criteria, and ends with a release ticket when the spec ships. `implement`'s handover names the stage reached.

**Blocked by:** 04

**Status:** done

- [x] `release` has the gate, the readiness table with the blocking rule, the explicit-yes deploy step, the verify step with the abort path, the operations handover, and the target table.
- [x] `release` never deploys on an inherited yes: the deploy question names target, environment and candidate every time.
- [x] `foundations` has the five production rows with their "what counts as present" and their skip rule, and the new offers.
- [x] `to-spec` has the Release subsection rule; `to-tickets` has the walking skeleton, negative-criteria and release-ticket rules; `implement`'s Next section names the stage reached from the six stages.
- [x] Content guards for the required headings of `release` and the new rows of `foundations`.
- [x] A headless `foundations` run on `tests/fixture` reports the five new rows (as not applicable or missing) without writing anything.
- [x] A headless `release` run on `tests/fixture` stops at readiness with "no deploy target" and asks, deploying nothing.

**How to verify:** `scripts/test.sh`; then `claude -p` in a fixture copy with "/matt-pocock-workflow:foundations" and with "release this": the first prints a survey table with the five new rows and asks; the second prints a readiness table whose target row is unmet and asks for the target.

## Comments

Done in `427e033` and its review-fix commit. Evidence: `scripts/test.sh` 8/8 suites (content guards for `release`'s six sections in order and its rules, the five `foundations` rows, the three flow-skill additions; the static test also under `/bin/bash` 3.2). Headless on the fixture (`tests/runs/ticket-05/`, gitignored): `/matt-pocock-workflow:foundations` reported all five production rows (four not applicable with the reason, scanning missing) and wrote nothing; "release this" invoked `matt-pocock-workflow:release` first, reported the target row as "unmet, no deploy target", asked for the target, deployed and wrote nothing. Both re-run on the review-fix candidate.

Review found and fixed: `release`'s Gate had facts but no question (now asks "check readiness now?", skipped when the user asked for the release); an unmerged branch was called "not a candidate" (it is a candidate at stage *built*; release from the base branch); no rule said which stage a readiness stop reaches (the recorded run wrote *built* for a candidate on `main`); "ships" and "the integrated work" against the glossary's avoid lists; the walking skeleton and the release ticket now both go through `release` to the environments the Release section names; `foundations`' skip rule narrowed (a published package has a target, a pipeline and scanning) and "not applicable, never left out" for every row; the runbook skeleton is `foundations`' offer, `release` names the runbook; *Operations handover* added to the glossary; the README's three survey sentences name the production rows; the static test's loops are two helpers.

Decisions the ticket left open: the stage rule (*release-ready* when every row is ready, *deployed* when Verify passed, *operated* when monitoring, alert owner and runbook exist; a readiness stop keeps the arriving stage). Left to their tickets: the bootstrap row for `release` (07); README lifecycle section and CHANGELOG (10).
