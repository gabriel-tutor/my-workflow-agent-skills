# The development loop, stages A–H

Verbatim from `sources/MATT-POCOCK-SUPERPOWERS-WORKFLOW.md` §6 (Superpowers 6.3.0 @ b36e082; Matt Pocock skills 1.2.3 @ 3cca18b; written 2026-09-10). Open it when `SKILL.md` §8 "Read next" points here. `SP/name` = Superpowers skill (`superpowers:name` in Claude Code); `MP/name` = Matt Pocock skill.

## 6. Run the development loop

### A. Establish the task contract

Read the request, applicable instructions, relevant code, existing changes, and current verification commands. Read `CONTEXT-MAP.md` or `CONTEXT.md` and relevant ADRs where present.

Capture the following in the existing task/spec/plan, or briefly in the conversation for a small task:

- The user-visible outcome and what is out of scope.
- Observable acceptance criteria, including relevant failure behavior.
- Affected interfaces and external dependencies.
- Agreed test seams and validation commands.
- The review baseline and the workspace being changed.
- Any unresolved decision that prevents a correct implementation.

Investigate facts yourself. Bring a recommendation when a user decision is needed. Use the latest explicit direction and prior approvals; do not ask the user to approve the same resolved point repeatedly.

### B. Design with the appropriate owner

Use `SP/brainstorming` for new design decisions. Reuse the design already supplied for an implementation request. Load `MP/domain-modeling` when terms or relationships are being resolved, and `MP/codebase-design` when deciding a module's shape or test interface.

For uncertainty that evidence can settle:

- Use `MP/research` for a narrow external fact, version contract, or technical comparison grounded in primary sources.
- Use `MP/prototype/LOGIC.md` for state transitions or business logic the user needs to exercise.
- Use `MP/prototype/UI.md` for structurally different UI alternatives, grounded in the project's design system.

Keep one interview active. Make material decisions and test seams concrete before asking for approval. Capture durable domain terms as they resolve. Use ADRs selectively for consequential, non-obvious trade-offs.

### C. Plan at two resolutions when necessary

For a bounded task, proceed from the approved short design without manufacturing a large plan.

For larger work, use `SP/writing-plans` from the canonical approved design. Use MP ticket planning only when the user needs durable backlog/sprint units. Each ticket is a complete behavioral slice; each plan task is an independently testable deliverable worth reviewing. A small test-writing action is a step, not automatically a separate ticket or worker.

Before execution, check:

- Each requirement is covered by a task and a verification method.
- Tasks agree about produced and consumed interfaces.
- Shared files, data, and dependencies have an explicit ordering.
- The instructions fit the current checkout.
- Constraints from the canonical spec are carried into worker briefs.

Tracker-dependent MP workflows need the project's issue-tracker and label configuration. If required configuration is missing, tell the user to invoke `setup-matt-pocock-skills`; continue independent work. Do not treat installation as repository setup.

### D. Prepare the workspace

Use `SP/using-git-worktrees` when isolation is needed by the selected execution mode. Detect existing isolation and use native workspace tools where available. Respect the user's existing preference; do not create nested or duplicate worktrees.

Record the source baseline and run relevant baseline checks. Separate pre-existing failures from introduced failures. A failing baseline is a known limitation to resolve or explicitly account for, never evidence that new failures can be ignored.

Use the repository's existing package manager and lockfile workflow. Installing dependencies is a task-specific action, not an automatic reason to upgrade packages.

### E. Implement one coherent slice

Use `SP/test-driven-development` as the cycle owner:

1. Name the behavior and the defect the proposed test can catch.
2. Test at the agreed public interface, using MP's seam discipline.
3. Derive expectations from the spec, hand-checked examples, or fixtures independent of the implementation.
4. Run the test and observe the intended failure.
5. Implement the minimum behavior needed to pass.
6. Run the targeted check and relevant regression checks.
7. Perform small behavior-preserving cleanup if useful, keeping the checks green.

Consult MP's `tdd/tests.md` and `tdd/mocking.md`, and SP's `test-driven-development/writing-good-tests.md`. Test real behavior; mock the external boundary when justified. Do not create tests merely to satisfy a numeric coverage target or a rule that every private helper must have its own test.

A pure refactor may start with characterization tests that pass on the existing behavior. They establish a preservation baseline, not a fake feature regression. New behavior and corrected defects require the appropriate failing evidence before the change. State which kind of evidence you have.

### F. Diagnose instead of guessing

When a check fails, use `SP/systematic-debugging` before proposing a fix. Read the actual error, reproduce, compare working cases and recent changes, and test a supported hypothesis with one changed variable.

Escalate to `MP/diagnosing-bugs` when reproduction itself is difficult, the failure is intermittent or concurrent, or a performance baseline needs a tighter loop. Carry the existing evidence forward. MP then owns the diagnosis sequence: build a red-capable loop, minimize, rank falsifiable hypotheses, probe individually, fix, and rerun the original scenario.

If repeated fixes fail, revisit the model and architecture rather than attempting more of the same. A missing regression seam is a documented gap, not permission to call the bug fully protected.

Redact secrets from commands, logs, traces, and reports. Prefer presence checks or redacted values when investigating configuration. Do not copy diagnostic examples that dump entire environments or authentication payloads.

### G. Review with explicit scope

Use the active SP review process, with MP's criteria as described in section 4. Pin the base before a task starts, preserve all task commits in its review range, and include current uncommitted work when relevant. Reviewers read the real diff and required context, not only the implementer's summary.

Use `SP/receiving-code-review` before applying suggestions. Verify claims against the code and requirements. Fix valid blocking findings; support disagreement with concrete evidence. Reviewer preferences do not create new requirements.

Re-review the fix and its effects. Do not restart a whole-codebase review for every minor adjustment. When a retry budget is exhausted, report the unresolved state and a concrete next option. A workflow limit does not waive the release gate.

### H. Verify, integrate, and report

Use `SP/verification-before-completion` on the final source state. Use `SP/finishing-a-development-branch` for the integration action covered by the user's instructions. If integration direction is already explicit, follow it; otherwise present the prepared options when the work is ready for that decision.

Publishing, pushing, merging, modifying shared environments, and messaging people must remain within the user's authorization. Producing a release plan does not execute a release.

If a merge/rebase conflicts, `MP/resolving-merge-conflicts` can own conflict resolution. Preserve each side's intended behavior, run the applicable checks on the integrated result, and complete the authorized operation.

Report the actual status using precise terms: implemented, verified, blocked, ready for review, merged, deployed, or validated after deployment. These are different states. Include the evidence and any remaining limitations.

