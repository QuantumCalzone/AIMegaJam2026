---
from: quantumcalzone
to: all
---

# New tasks T81, T82 and T83 (the cast in Hyper3D)

My person chose on 2026-11-15 to replace the cast's engine-shape bodies (T79, T80) with models generated in Hyper3D from the same concept images in `Docs/BotArt/`, as soon as possible. `Docs/Plan.md` has the entries and `Docs/tasks/T81.md` to `T83.md` the steps. This note is information; the plan is what counts.

- **T81** generates the models with no editor. It is first in "Open" and free now, but it needs the `hyper3d` MCP server, which is set up and signed in on the Mac only (user scope, OAuth). The PC has no setup, so T81 runs on the Mac. It needs my person's OK on the credit estimate before its first paid call, and ends waiting for their look at the sheet.
- **T82** (OpenAI, Anthropic and SpaceXAI) and **T83** (Meta and the player's costume) swap the models into `BP_Robot`. They sit right under T75, which goes first on `BP_Robot`. Both lock `BP_Robot` (and `L_Stage` if the robots must be re-placed) and touch neither `BP_Show` nor `WBP_Stage`, so they belong to the non-chain machine.
- **T74 now depends on T83**, so its captures show the final cast. T70 depends on all three.
