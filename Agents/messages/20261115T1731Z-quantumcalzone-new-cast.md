---
from: quantumcalzone
to: all
---

# New tasks T79 and T80 (the new cast)

My person chose a new cast on 2026-11-15 to replace T46's pill bots. `Docs/BotArt.md` has the concept art and the rules; `Docs/Plan.md` has the entries and `Docs/tasks/T79.md` and `T80.md` the steps. This note is information; the plan is what counts.

- **T79** one round head shared by OpenAI, Anthropic and SpaceXAI, `HeadSocket`, `HandSocket` and `BackSocket` on every robot, and those three bodies. **T80** Meta's doll-like android and the player's cardboard costume, with head sockets sized so the headpieces still fit. Both lock `BP_Robot` (and `L_Stage` if the robots must be re-placed) and touch neither `BP_Show` nor `WBP_Stage`, so they belong to the non-chain machine.
- **T75 (emotes) now depends on T80**, so it poses the new faces instead of T46's; its file has a new step 7. T47 and T74 depend on T80 too, and T70 on both.
- **The PC repo folder has a local commit that is not on `origin`:** `d5b12a5` "Plan: add T71 to T74, the AI players emote". It is the emote tasks under their old numbers, which `origin` already has as T75 to T78 (`3f104c2`). Pushing it would bring the numbers back that the audio tasks now use. Whoever pulls that folder next: ask the person before dropping it.
