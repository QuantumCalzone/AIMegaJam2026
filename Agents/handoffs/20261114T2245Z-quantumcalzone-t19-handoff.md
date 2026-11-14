---
from: quantumcalzone
to: quantumcalzone
---

# T19 handoff: robots act out their actions

T19 is built, saved and committed (this note's commit), but its box in `Docs/MVPPlan.md` stays unchecked. Details are in "T19: robots act out their actions" in Findings.

## Done

- New assets in `Content/NHOS/Stage/`: `BP_Prop`, `BP_PlaceMark`, `BP_StageDirector`, and `Materials/MI_Cardboard`, `MI_PropYellow`, `MI_PropOrange`, `MI_ToyRed`, `MI_Paper`.
- Changed: `BP_Robot` (action queue and the move, look, grab, throw, give and go-home actions), `BP_Show` (`ActorLine` and `StagePrep` each call the director; new variable `NullDir`), `L_Stage` (7 place markers in `Stage/Marks`, 8 props in `Stage/Props`, `StageDirector`).
- Graph sources: `Graphs/BP_Prop/`, `Graphs/BP_PlaceMark/`, `Graphs/BP_StageDirector/`, `Graphs/BP_Robot/`, `Graphs/BP_Show/ActorLine.txt` and `StagePrep.txt` (shorthand; expand with `Tools/dslpp.py`). `BP_Prop`'s construction script was wired by hand and has no file.
- Checked: two free-mode PIE shows played by hand (switches unchanged). Every verb played and printed `NHOS: ACT`, and scene 2 reset the stage. No script errors.

## Left

1. With my OK (my T17/T26 game-window playtest held `Local/switches.json`): set `"autoplay": true` (mode `free`, optionally `spare_human` for all 3 scenes), run one PIE show, confirm `NHOS: ACT` lines and `NHOS: SHOW END`, and take a screenshot with a prop in a hand. Then set autoplay (and spare_human) back to false.
2. I play one show in a game window (command in `CLAUDE.local.md`) and see a throw land. That one show can also cover T17 and T26.
3. Then check T19's box, replace its `Waiting:` line, update "Next up", commit, push, release the locks and the claim.

## Still held (my account)

- Claim `Docs/claims/T19` (the task isn't checked).
- LFS locks: `BP_Show.uasset`, `BP_Robot.uasset`, `L_Stage.umap` (shared with T17/T26 under the same account), and the eight new assets listed above.
- `Agents/status/mvp-T19.md` is deleted; no session is working on T19 now.
