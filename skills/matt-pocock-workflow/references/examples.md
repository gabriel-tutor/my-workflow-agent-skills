# Matt Pocock routing: practical examples

Verbatim from `sources/MATT-POCOCK-AGENT-INSTRUCTIONS.md` §10 (Matt Pocock skills 1.2.3 @ 3cca18b, inspected 2026-09-10). Open it when `SKILL.md` §7 "Read next" points here.

## 10. Practical examples

### “Add account roles and permissions.”

Read the existing authorization design and relevant ADRs. If role definitions are unresolved, use `domain-modeling` and the appropriate user-invoked design workflow. Use `codebase-design` for the authorization interface and `tdd` for agreed observable access decisions, including denied access. Apply the project's security-specific checks. Review Standards and Spec before completion.

### “The scraper crashes during a bulk run.”

Use `diagnosing-bugs` to reproduce the actual bulk-run failure, including the relevant concurrency or input conditions. Measure resource or timing behavior where implicated. Establish a regression seam that exercises the real pattern, fix the cause, rerun the original scenario, and use `code-review`. A single-item happy-path test is insufficient if the reported problem requires concurrent jobs.

### “Revamp this dashboard.”

If the desired layout is unresolved, use `prototype/UI.md` to compare distinct structures within the project's existing styling and component system. Preserve real read behavior and stub prototype mutations. Once the user chooses a direction, implement it with production checks; the prototype's minimal-quality constraints do not carry into production.

### “Build this six-week sprint.”

If the destination and requirements are settled, use the spec/ticket/implementation route. If major decisions are still unknown across multiple sessions, recommend `wayfinder` first. Model tickets as dependencies. Use the beta `implement-spec` only if the user explicitly selects it and the required worktree, subagent, and PR capabilities are available.

### “Improve our AGENTS.md.”

Use `writing-for-agents`. Keep essential behavior and navigation pointers easy to find. Put detailed reference material behind explicit triggers. Preserve existing rules and use checkable completion criteria. A clearer instruction document should not invent features or imply that a plain Markdown file can override the harness.

