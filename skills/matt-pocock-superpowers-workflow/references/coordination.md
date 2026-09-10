# Agent coordination without duplicate work

Verbatim from `sources/MATT-POCOCK-SUPERPOWERS-WORKFLOW.md` §7 (Superpowers 6.3.0 @ b36e082; Matt Pocock skills 1.2.3 @ 3cca18b; written 2026-09-10). Open it when `SKILL.md` §8 "Read next" points here. `SP/name` = Superpowers skill (`superpowers:name` in Claude Code); `MP/name` = Matt Pocock skill.

## 7. Agent coordination without duplicate work

Use subagents only when allowed by the active harness and useful for the task. Default SP SDD uses a fresh implementer per meaningful task, one task reviewer covering spec and quality, scoped re-reviews, and a final whole-branch review. The inspected source's detailed templates govern this, even where a README uses an older description.

Rules for the combined policy:

- The coordinator owns scope, dependencies, workspace assignments, reviews, and integration.
- Under SP SDD, implementation workers run sequentially. Parallel investigations must be independently scoped and must not race on shared files, databases, ports, or mutable fixtures.
- Do not nest MP `implement-spec` inside SP SDD. Its separate-worktree concurrency model is an explicitly chosen alternative.
- Workers receive a task brief, relevant constraints/interfaces, needed skill pointers, and a report destination. Give them sufficient evidence to challenge a faulty plan; do not instruct them to suppress possible findings.
- Workers perform their assigned job directly. They do not dispatch another coordinator or reviewer. This also applies to MP research workers.
- Reviewers inspect without changing the checkout under review. If a separate revision is needed, use an isolated read/review location.
- Use models actually available to the harness. Match capability to task difficulty and follow applicable model-selection rules; do not invent supported model names or escalate every trivial task to the most expensive tier.
- Preserve per-plan progress and findings across compaction. Verify recorded completed work against the relevant source state instead of repeating it from memory.

A compact worker brief includes:

```text
Role and task:
Workspace and owned files:
Task/spec reference and acceptance criteria:
Required interfaces and project constraints:
Required skills/references and process owner:
Verification commands and evidence to record:
Report destination:

Perform this assigned work directly. Do not spawn additional agents.
Preserve unrelated changes. Report a missing fact or blocker explicitly.
```

If subagents are unavailable, select the permitted inline execution mode, retain separate implementation and review steps, and disclose that review was not independent. Never simulate the existence of separate reviewers in the report.

### Evidence and review budgets

Reuse completed verification when it covers the same code state, inputs, environment, and scope. Reviewers inspect that evidence and request a focused rerun for a named doubt. The final integrated state still needs the required final checks.

Track open findings through fixed, disproven, accepted/deferred, or blocked states. A concrete correctness or acceptance failure cannot be relabeled Minor to make the workflow pass. Non-blocking improvements can remain as explicit follow-up work.

Before cleaning temporary coordination data, preserve unresolved findings, rulings, their consequences, and unique evidence in a durable project record or final handoff. Do not delete the only record of a decision because the source code was committed.

