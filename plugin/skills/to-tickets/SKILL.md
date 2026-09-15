---
name: to-tickets
description: Use when a spec exists and needs splitting into tickets
---

# To tickets

This skill runs Matt Pocock's `to-tickets`, which only the user can invoke directly.

1. **Load it.** Read Matt Pocock's `to-tickets/SKILL.md` from the directory the session bootstrap names. If the bootstrap says his skills were not found, or the file is missing, tell the user Matt Pocock's skills aren't installed, and stop.
2. **Follow it exactly,** with one addition. Every ticket gets a **How to verify** line after its acceptance criteria: the command, or the short manual steps, that prove those criteria are met (`npm test -- coupons`, or "run `npm start`, add two items, apply SAVE10, the total drops 10%"). Reuse the repo's real scripts; if the repo has no test or run command yet, say so in the line instead of inventing one.
3. **Next.** Offer `matt-pocock-workflow:implement` for the first ticket whose blockers are done, and wait for a yes.
