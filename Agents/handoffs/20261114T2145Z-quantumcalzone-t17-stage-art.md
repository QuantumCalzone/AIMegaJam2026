---
from: quantumcalzone
to: quantumcalzone
---

# T17 stage art: waiting only on the personality verdict

- **Done and pushed:** commit 4b605a8 "T17: Stage art and personality (verdict pending)". The improv theater in `L_Stage` (camera, lights and the `StagePost` exposure volume included), persona robot looks and motion in `BP_Robot`, `BP_Backdrop` with six backdrops, `M_Set`, `M_Backdrop`, 41 instances in `Content/NHOS/Stage/Materials/`, and the `BP_Show` hooks (`StagePrep`, `PersonaColor`, `StageSetup`, `StageCut`, one `StagePrep` call at the top of `ShowPrep`). "T17: stage art results" in `Docs/MVPPlan.md` Findings has the details and the Unreal MCP rules found. The DSL sources are in `Saved/T17/src/` (not in git).
- **Checked:** two free-mode autoplay shows in PIE reached `NHOS: SHOW END` (one win, one loss), with `STAGE robots=5`, four different backdrops and no failed calls. Screenshots are in `Saved/T17/shots/` (not in git).
- **Waiting:** my verdict that the stage has personality (T17's Done-when). Not seen yet: the AIs' cheer when the human is caught.
- **To close T17:** once I say it has personality, check T17's box in `Docs/MVPPlan.md`, swap its `Waiting:` line for a `Result:` line, update "Next up", add a DevLog line, commit as `T17: ...`, push, then `git lfs unlock Docs/claims/T17`. If I ask for changes instead, they go in `BP_Robot`, `BP_Backdrop` or `L_Stage`. T19 now holds those locks, so coordinate with it.
- **Claim and locks:** I keep `Docs/claims/T17`, because the plan keeps a claim until its task's box is checked. I released `BP_Backdrop.uasset` and `M_Robot.uasset`. `BP_Show`, `BP_Robot` and `L_Stage` stay locked under the same account, and T19 has taken them over.
