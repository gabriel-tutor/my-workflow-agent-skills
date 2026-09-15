---
name: grill
description: Use before building a feature or changing behavior, when a plan or design needs stress-testing, or when another skill says to call grilling
---

# Grill

This is Matt Pocock's grilling, presented one clickable question at a time.

## Method

1. Invoke Matt Pocock's `grilling` skill with the Skill tool, and follow its method exactly:
   - Keep the design tree and its frontier.
   - Find facts yourself, dispatching a subagent when needed.
   - Put every decision to the user.
   - Keep going until the frontier is empty and the user confirms you share an understanding. Nothing gets built before that confirmation.

   If `grilling` isn't available, tell the user Matt Pocock's skills aren't installed, and stop.
2. In a git repo, also invoke `domain-modeling`, and update `CONTEXT.md` and the ADRs as decisions land.

## Presentation

This replaces grilling's round format. Each of your turns has exactly two parts, in this order:

1. **Facts:** the facts from the code or docs that this question depends on, in a few lines. If it helps, add how many decisions remain after this one, as a number ("3 more decisions after this one").
2. **One question:** ask it with the AskUserQuestion tool, offering 2–4 options. Put your recommended answer first and end its label with "(Recommended)". Free-text answers arrive through "Other". If AskUserQuestion isn't available, write the same question in text: the question, its options as a short list, and your recommendation. Then end your turn.

The rest of the frontier stays in your design tree until its turn; the count in the facts is all the user sees of it. Take each question from the frontier in dependency order. A decision the code or an earlier answer already settles is not a question; the fact goes in the facts section, and the frontier moves on. For anything that will be built, one frontier question is which seams the tests go at, because Matt Pocock's `tdd` tests only at agreed seams.

## Coverage

Before you call the frontier empty, check the design tree against the design lens in `references/design-lens.md` (next to this file). Any axis that applies to this change and is still unsettled is a branch you missed: add it to the frontier. Axes that don't apply are skipped silently. The lens scales with the change, as it says.

## Done

The grill is done when the frontier is empty, the lens has been checked, every branch has been visited, and the user has confirmed the shared understanding. Then offer the next step from the bootstrap's routing, such as `tdd`, `matt-pocock-workflow:implement` or `matt-pocock-workflow:to-spec`, and wait for a yes.
