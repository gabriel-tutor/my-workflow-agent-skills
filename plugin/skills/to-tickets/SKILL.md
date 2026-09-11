---
name: to-tickets
description: Use when a spec exists and needs splitting into tickets
---

# To tickets

This skill runs Matt Pocock's `to-tickets`, which only the user can invoke directly.

1. **Load it.** Read Matt Pocock's `to-tickets/SKILL.md` from the directory the session bootstrap names. If the bootstrap says his skills were not found, or the file is missing, tell the user Matt Pocock's skills aren't installed, and stop.
2. **Follow it exactly.** Its quiz on the proposed breakdown is the gate: iterate until the user approves the breakdown. Before it publishes, confirm where the tickets will go, and wait for a yes.
3. **Next.** Offer `matt-pocock-workflow:implement` for the first ticket whose blockers are done, and wait for a yes. Between tickets, suggest `/clear`.
