---
from: quantumcalzone
to: all
---

# New tasks T75 to T78 (the AI players emote)

My person added emotes on 2026-11-15. `Docs/Plan.md` has the entries and `Docs/tasks/T75.md` to `T78.md` have the steps. This note is information; the plan is what counts.

- Every reply carries an emotion (12 to start: neutral, happy, sad, angry, worried, scared, surprised, confused, disgusted, suspicious, smug, embarrassed), and its robot acts it out with its face and a gesture as the line plays. My robot emotes too, so a blank face is no tell.
- **T75** `BP_Robot.Emote` and a new `Content/NHOS/Data/emotes.json`, with an `emote_test` switch. Its dependencies are done, and it touches neither `BP_Show` nor `WBP_Stage`, so it belongs to the non-chain machine. It locks `BP_Robot`, which T38 and T47 also change.
- **T76** the `emotion` field in `llm.json`'s reply shape, a rule line in `prompts.json` `base`, the relay's free mode and the checker. No editor, so the non-chain machine, but it waits for T69: it changes the same reply shape, prompts and relay as the chain tasks before it. Its push deploys the relay, so it waits for my person's OK.
- **T77** the game plays each line's emotion, the shared log gets `feels`, and the input LLM picks my emotion. **T78** an emotion chip in the action builder. Both touch `BP_Show`, so they belong to the chain machine.
- They sit right after T69 and before T38. They were first written as T71 to T74, but another session took those numbers at the same time (music, robot voices, lines that type out, and the doc captures), so they are T75 to T78. T34's **Depends on** line gained T78, and T70's gained T75 to T78. No other task's line changed.
