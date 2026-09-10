# Matt Pocock workflow rules

Verbatim from `sources/MATT-POCOCK-AGENT-INSTRUCTIONS.md` §6 (Matt Pocock skills 1.2.3 @ 3cca18b, inspected 2026-09-10). Open it when `SKILL.md` §7 "Read next" points here.

## 6. Apply the important workflow rules

### Implementation and TDD

- Establish the observable behavior and test seams before tests. A seam is the public interface at which the behavior is exercised. Reuse seams already approved in the current spec or conversation; if a necessary seam is new and unconfirmed, present a concrete proposal for confirmation.
- Read `tdd/tests.md` and `tdd/mocking.md`. Prefer behavior through real interfaces. Mock genuine external boundaries when needed, and keep expected results independent of the implementation.
- Work one vertical slice at a time: a failing test, the minimum implementation that passes it, then the next slice. Confirm the red failure concerns the intended behavior.
- In this snapshot, the detailed TDD instructions place refactoring in the review stage, even though some descriptions say “red-green-refactor.” Follow the detailed installed instructions.
- Run targeted checks during implementation. When using `implement`, run typechecking regularly, individual test files regularly, and the full test suite at the end. Preserve project-required gates and report checks that could not run.
- For a pure refactor, establish behavior-preserving verification at the relevant interface. Avoid tests that merely assert the new internal structure. For static copy or formatting changes, use checks appropriate to the change.

### Diagnosis

- Build a runnable feedback loop that detects the reported symptom before developing a theory. Run it and preserve the useful output with secrets redacted.
- Reproduce and minimize, form ranked falsifiable hypotheses, then instrument one variable at a time. For performance work, measure a baseline before optimization.
- Write a regression test before the fix when a correct seam exists. Rerun the original scenario afterward; a passing minimized example alone is insufficient.
- If no correct seam exists, state that limitation. If no reliable reproduction can be built, report the attempts and request the concrete missing evidence or access required by the skill.
- Remove temporary instrumentation before completion. Explain any skipped phase; do not present an unverified guess as a proven cause.

### Design and domain documentation

- Use `codebase-design` for the module's interface, depth, seams, adapters, and locality. It is a reference, not authorization to redesign the entire application.
- Load `DEEPENING.md` when evaluating dependencies and changing module structure. Load `DESIGN-IT-TWICE.md` only when comparing alternative interfaces is part of the task.
- Reading a glossary is ordinary context gathering. Invoke `domain-modeling` when actively changing terminology, writing the glossary, or recording a decision.
- Keep `CONTEXT.md` focused on domain vocabulary and relationships. Put implementation requirements in specs and meaningful trade-offs in ADRs. Create these documents when there is resolved material to record.
- Offer an ADR when the choice is hard to reverse, surprising without context, and the result of a real trade-off. Respect existing decisions or explicitly identify why they need reconsideration.

### Planning and tickets

- `grilling` works through rounds of currently answerable decisions, with recommendations. Look up facts rather than asking the user to research the codebase. Reuse decisions already settled.
- `to-spec` synthesizes the discussion; it is not another discovery interview. It still explicitly checks the proposed test seams with the user.
- `to-tickets` creates complete vertical slices with blockers. A broad mechanical migration may use expand–migrate–contract instead. Get the breakdown agreed before publication.
- Local implementation tickets are separate files under `.scratch/<feature>/issues/<NN>-<slug>.md`, not one combined tickets file. Follow the configured tracker when it differs.
- Treat `wayfinder` tickets as questions that resolve decisions by default. Charting stops after building the map; work sessions normally resolve one decision ticket, with the skill's research exception. Do not silently convert planning into a production build.
- Do not re-triage tickets already made ready by `to-tickets`, or assume `implement` automatically closes issues. Tracker updates follow the user's requested workflow.

### Review the changes that actually exist

Load Matt Pocock's `code-review`, identify the standards and spec sources, and pin a valid review baseline. If no baseline is already supplied or agreed, propose a concrete one and obtain the required decision before running that review.

**Working-tree adaptation supplied by this guide:** the archive's `git diff <fixed-point>...HEAD` reviews committed changes only. Before claiming a current change was reviewed, check `git status` and include relevant staged, unstaged, and untracked work in the review scope. Resolve the merge-base with the confirmed fixed point; a diff from that base to the working tree captures tracked current changes, while untracked files require explicit inspection. Preserve unrelated user changes. State the exact comparison used. Do not commit merely to make an empty review appear nonempty.

Keep findings in two groups:

- **Standards:** cite a documented repository rule or identify a code smell as a judgment call. The repository's standards override the smell baseline.
- **Spec:** compare against the request, issue, or spec. Report missing, partial, incorrect, and extra behavior. If no spec source exists, state that instead of inventing one from the implementation.

Address actionable findings and verify the affected work. Do not repeat broad review indefinitely to chase a subjective zero-findings result. Report what was checked, what changed, and what remains.

### Delegation and capability limits

Some skills explicitly use subagents: `research`, `code-review`, architecture exploration, interface alternatives, and the beta `implement-spec`. Use them only when the current harness supports and permits that workflow.

**Delegation adaptation supplied by this guide:** make reviewer and researcher briefs bounded leaf tasks: “Perform this assigned work directly. Do not invoke the parent orchestration skill again or spawn additional agents.” Give them the source pointers, scope, required output, and stopping criterion. A worker does not restart the coordinator's workflow.

If parallel agents are unavailable, report the limitation. Where governing instructions permit an equivalent fallback, perform the work sequentially with separate outputs and label it as an adapted workflow. Never claim independent parallel reviews occurred when they did not. If the missing capability is essential to the requested outcome, report that specific blocker.

