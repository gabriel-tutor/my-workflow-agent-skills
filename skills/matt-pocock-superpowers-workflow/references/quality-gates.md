# Quality gates the skill bundles do not supply by themselves

Verbatim from `sources/MATT-POCOCK-SUPERPOWERS-WORKFLOW.md` §8 (Superpowers 6.3.0 @ b36e082; Matt Pocock skills 1.2.3 @ 3cca18b; written 2026-09-10). Open it when `SKILL.md` §8 "Read next" points here. `SP/name` = Superpowers skill (`superpowers:name` in Claude Code); `MP/name` = Matt Pocock skill.

## 8. Quality gates that the skill bundles do not supply by themselves

These are engineering checks added by this proposed policy, selected according to the actual change. They are not claims that either bundle automatically installs or performs them.

| Gate | Evidence to require when relevant |
| --- | --- |
| Requirements | Each acceptance criterion maps to implemented behavior and a verification result. |
| Static correctness | The project's formatter/linter, typecheck, and build checks pass on the final state. Record pre-existing noise separately. |
| Behavioral correctness | Meaningful tests of success, failure, and relevant edge cases at real interfaces. |
| Integration | Changed API, storage, queue, auth, and frontend paths work together in the representative environment. |
| UI and accessibility | Actual screen inspection, relevant viewport checks, keyboard behavior, labels/focus, and user-flow validation. A screenshot alone does not prove behavior. |
| Authorization and sensitive data | Tests for allowed and denied access, correct ownership/tenant boundaries, and safe treatment of secrets and sensitive fields where the change touches them. |
| External integrations | Contract and failure checks for the changed dependency, including malformed responses, timeouts, retries, or duplicate delivery where applicable. |
| Schema/data changes | Migration behavior tested against representative data; compatibility and recovery strategy documented. Use expand–migrate–contract when required. |
| Concurrency and performance | Measurements against agreed workloads and thresholds, including contention, duplicate work, resource growth, or rate limits implicated by the change. |
| Operations | Relevant logs/metrics, failure visibility, recovery behavior, configuration, and health checks are present and verified. |
| Release | Exact source/build identified, required CI checks satisfied, deployment/recovery steps prepared, and the user's release authorization followed. |
| Post-release behavior | If deployment is authorized, smoke checks and relevant monitoring verify the deployed state. Local success is not deployment evidence. |

Discover thresholds from the project's requirements. When a decision depends on an unknown threshold, propose a concrete target and resolve it; do not invent a performance promise or claim an unmeasured SLA.

Use specialist tooling and current primary documentation when the domain requires it. Neither skill collection replaces a security review, accessible UI evaluation, database expertise, infrastructure checks, or product acceptance.

### Definition of ready for review

- The requested behavior is implemented within scope.
- Relevant checks ran on the current source state, with results available.
- The actual diff has been reviewed and blocking findings are resolved.
- Any remaining limitation is explicit and correctly classified.
- Applicable docs, configuration, and migration notes are updated.
- The user can inspect a concrete result and decide the next integration step.

### Definition of ready to release

Ready for review is not sufficient. The applicable CI, integration, security, data, operational, and product-acceptance gates must also be satisfied. A known failed acceptance criterion, data-integrity defect, or material security issue blocks this status. If the user changes scope or accepts a specific risk within permitted policy, record that decision and reassess the claim against the revised contract.

