# 06: Incident route and a sharper grill

**What to build:** A live outage has its own route. The `incident` skill establishes impact (who is affected, since when, what changed last: deploy, config, dependency), contains with the safest reversible action and asks before any outward action, restores and confirms, then hands root cause to `diagnosing-bugs`, routes the fix through the normal path with a regression test first, writes a post-mortem note under `docs/incidents/` (timeline, impact, cause, what stopped it, what prevents it) with follow-up tickets, and closes with a handover naming the stage reached. The grill gains one rule: a decision the code or an earlier answer already settles is not a question; the fact goes in the facts section.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] `incident` has, in order: impact, contain (with the ask-before-outward rule), restore and confirm, diagnose through `diagnosing-bugs`, fix through the normal route with the regression test first, post-mortem note and follow-ups, handover.
- [ ] `grill` contains the settled-is-not-a-question rule in its presentation section.
- [ ] Content guards for `incident`'s required headings and the grill line.
- [ ] A headless `incident` run on `tests/fixture` with "production is down since the last deploy" produces an impact summary and stops at contain with a question, changing nothing.

**How to verify:** `scripts/test.sh`; then `claude -p` in a fixture copy with the outage prompt above: the transcript shows impact, then an AskUserQuestion (or the text form) about containment, and `git status` in the workspace is clean.
