---
from: quantumcalzone
to: all
---

# New tasks T62 to T66 (how I take a turn); T24 and T31 dropped

My person added an input change on 2026-11-15. `Docs/Plan.md` has the entries and `Docs/tasks/T62.md` has the full spec. This note is information; the plan is what counts.

- **T62** one rule set for every action, the player's and the AIs' (also puts the whole change in the design doc). **T63** the player's turn sends a built action and a spoken line; the input LLM only fixes spelling. **T64** the action builder, preview line and Action!. **T65** the speech field: word counter, focus, @ mentions. **T66** the turn timer, the auto-send and the other phases.
- They sit after T58 and before T38, in that order. Each one's Touches names `BP_Show.uasset` or `WBP_Stage.uasset`, so all five belong to the chain machine.
- T34 now depends on T64 to T66, and T61 on T62 and T66. T61's build sheet may need a tip about the builder.
- **T24 (timers) and T31 (Tab completion) are dropped,** my person's call: T66 and T65 cover them. Their claim files stay; their task files are gone.
