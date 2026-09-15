# 06: Incident route and a sharper grill

**What to build:** A live outage has its own route. The `incident` skill establishes impact (who is affected, since when, what changed last: deploy, config, dependency), contains with the safest reversible action and asks before any outward action, restores and confirms, then hands root cause to `diagnosing-bugs`, routes the fix through the normal path with a regression test first, writes a post-mortem note under `docs/incidents/` (timeline, impact, cause, what stopped it, what prevents it) with follow-up tickets, and closes with a handover naming the stage reached. The grill gains one rule: a decision the code or an earlier answer already settles is not a question; the fact goes in the facts section.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] `incident` has, in order: impact, contain (with the ask-before-outward rule), restore and confirm, diagnose through `diagnosing-bugs`, fix through the normal route with the regression test first, post-mortem note and follow-ups, handover.
- [x] `grill` contains the settled-is-not-a-question rule in its presentation section.
- [x] Content guards for `incident`'s required headings and the grill line.
- [x] A headless `incident` run on `tests/fixture` with "production is down since the last deploy" produces an impact summary and stops at contain with a question, changing nothing.

**How to verify:** `scripts/test.sh`; then `claude -p` in a fixture copy with the outage prompt above: the transcript shows impact, then an AskUserQuestion (or the text form) about containment, and `git status` in the workspace is clean.

## Comments

Done in `55d8688` and its review-fix commit `8c0ebe6`. Evidence: `scripts/test.sh` 9/9 suites on `8c0ebe6` (the static test checks incident's seven sections in order and each step's rule inside its own section, and the grill line inside its Presentation section; the outward-action guard shown red when the rule is moved under Diagnose). Headless on the fixture (`tests/runs/ticket-06/`, gitignored), invoked as `/matt-pocock-workflow:incident production is down since the last deploy` because the bootstrap row that routes an outage is ticket 07's: on `8c0ebe6` the reply was a three-line impact summary (who, since when, what changed last: all unknown from a checkout with one commit, no remote and no deploy config), "no cause named", then Contain proposed a rollback to the last known-good deploy and stopped on the question "Where does production run, and what do I roll back to?" in the text form with a recommended option; seven read-only calls; `git status --porcelain` empty and HEAD at the baseline. The same on the first candidate, with nine read-only calls. The record's `skills` field is empty because a slash command loads a skill without a Skill call; the reply's headings are the evidence the skill ran.

Review found and fixed: the closing section named for the ticket handover's glossary term (now `## Incident handover`); the sensitive list missing "anything destructive"; "candidate" and "route" in senses the glossary reserves; the Fix step named no skill and no commit, so the handover's "candidate SHA" had no source and `release`'s gate would bounce an unintegrated branch (the fix is now a ticket built through `implement`, the grill first for a sensitive change, then `release`); "no longer affected" claimed without `verification-before-completion`; a missing `diagnosing-bugs` stopped without a handover; the note had no Follow-ups heading and a session ending before the fix had no note or ticket to hand over (it now writes the note with the rest pending and opens the fix ticket); upstream phase numbers; the grill guard's duplicated awk and file-wide grep. Glossary gains Containing action, Outward action, Post-mortem note, Incident handover.

Decisions the ticket left open: no gate question before Impact (it is read-only; the first yes is Contain's); the note is written at the Post-mortem step, or earlier with the rest pending when the session ends before the fix; "impact summary" kept as the ticket's term. Left to their tickets: the bootstrap row and the routing.md on-ramp for `incident` (07); README lifecycle section and CHANGELOG (10).
