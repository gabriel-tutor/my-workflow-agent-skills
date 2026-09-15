---
name: incident
description: Use when users are affected now, production down, degraded, erroring or slow; contains and restores before any diagnosis and asks before any outward action, then the cause through diagnosing-bugs, the fix through the normal route with a regression test first, a post-mortem note and a handover
---

# Incident

An outage or degradation that users feel now. Contain and restore come before diagnosis: users stop being affected first, the cause is found second, and the fix takes the normal route with a regression test. The steps run in this order, none skipped, and nothing outward (a rollback, a redeploy, a config or flag change on the host, a restart, a message to users) happens before the user's yes to that action.

## Impact

Establish three facts before touching anything, read-only, from the platform, the repo and the user:

1. **Who is affected.** Which users or journeys, and how: down, erroring, slow, wrong data. From the platform's status page, logs or error tracker, and the user's report.
2. **Since when.** The first bad timestamp: the alert, the first error in the logs, or the user's word.
3. **What changed last.** The last deploy (the platform's deployment list, `git log` on the base branch), the last config or environment change, the last dependency change: the most recent change before the first bad timestamp. That change is the first candidate for containment, not a diagnosis.

Report them as an impact summary, three lines, with anything the sources cannot answer named as unknown rather than guessed. Redact every secret in what you show, as `diagnosing-bugs` does. No edits, no commands that change the repo or the host, and no cause named here: a cause guessed now delays the containment.

## Contain

Choose the safest reversible action that stops users being affected, the one that matches what changed last: a rollback to the last known-good deploy when a deploy did it; the previous config when config did; the flag or route turned off when one feature fails; a restart or a scale-out when the failure is capacity; a maintenance page or a message to users when nothing else is available in time. Reversible first: no forward fix under pressure, no change to data.

**Ask before any outward action.** An outward action reaches users or the host: a rollback, a redeploy, a config or flag change, a restart, a message. Ask with AskUserQuestion, recommended answer first, naming the action, the target, the environment and what it reverts to, and wait for the yes; a yes given earlier to anything else never covers it. If AskUserQuestion isn't available, write the same question in text: the question, its options as a short list, and your recommendation; then end your turn. When the target or the last known-good version is unknown, that is the question: ask for them, do not guess. The action goes through the platform's skill or CLI when it has one; steps only a person can take (a console, a phone, a credential) are handed to the user as exact steps in order.

## Restore and confirm

After the containing action, confirm with the output shown that users are no longer affected: the running version is the one rolled back to, the journeys that failed pass, the errors have stopped in the logs, and a short watch shows it holding. Report what was seen. If it did not hold, return to Contain with the next action. Diagnosis waits until users are no longer affected, or until every containing action has been tried and the user says to diagnose live.

## Diagnose

With users no longer affected, find the root cause. Invoke `diagnosing-bugs` (Matt Pocock's, bare name) with the Skill tool and follow it: its feedback loop, its ranked hypotheses, its instrumentation. Its starting facts are the impact summary and the containing action; what changed last is its first hypothesis, never its conclusion. If `diagnosing-bugs` isn't available, tell the user Matt Pocock's skills aren't installed, and stop.

## Fix

The fix takes the normal route, never a shortcut from the incident: the regression test first, at a seam that reproduces the real failure (`diagnosing-bugs`, Phase 5), watched failing, then the fix, watched passing, then its Phase 6 cleanup. When the fix changes behavior beyond restoring it, or touches anything sensitive (auth, permissions, secrets, billing, a migration, infrastructure or deploy configuration, a public API), it goes through `matt-pocock-workflow:grill` before it is written. `code-review` runs on the candidate either way. The containing action stays in place until `matt-pocock-workflow:release` has put the fixed candidate on the environment the containment protected and verified it running.

## Post-mortem

Write a note at `docs/incidents/<YYYY-MM-DD>-<slug>.md` with these headings: **Timeline** (first bad timestamp, detection, containment, restore, fix, each with its time), **Impact** (who, how, for how long), **Cause** (the hypothesis `diagnosing-bugs` confirmed), **What stopped it** (the containing action and why it was the safe one), **What prevents it** (the regression test, and any change to the pipeline, monitoring, alerting or process). Blameless: it names changes and gaps, not people. Open a follow-up ticket through the issue tracker (`docs/agents/issue-tracker.md`) for every item under What prevents it that this incident did not close, and list them in the note.

## Handover

The closing message, in this order:

1. **The service now.** What runs (version and environment), whether users are still affected, and the containing action still in place, if any.
2. **What changed.** The fix's candidate SHA, or that there is no fix yet; the post-mortem note's path; the follow-up tickets.
3. **Stage reached.** For the fix, one of the six: designed, built, integrated, release-ready, deployed, operated. *Deployed* only once `matt-pocock-workflow:release` verified the fixed candidate running. An incident handed over before a fix exists says so, and names the step it stopped at: impact, contain, restore or diagnose.
4. **Next.** The next step and who owns it: the next containing action, the diagnosis, the fix, its release, or the note's follow-ups. When the session ends before the fix, the follow-up ticket carries it, with an owner and the containing action it will replace.
