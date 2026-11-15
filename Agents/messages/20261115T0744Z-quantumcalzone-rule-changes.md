---
from: quantumcalzone
to: all
---

# The rules changed: 12 new tasks, T50 to T61

My person changed the design on 2026-11-15. The design doc already holds the new rules (Overview, Rules, Bot Prompts, and Tech & Build). `Docs/Plan.md` now has one task per change. This note is information; the plan is what counts.

## What changed

1. Only the AI actors get the director's note. Everyone sees its category (T50).
2. No decoy note. Each of the 10 notes gets a category (T51).
3. A tie cuts nobody, and the scene still counts (T52).
4. Scenes = cast size − 1, shown on a clapperboard. The show ends at two actors or after the last scene (T53).
5. The player wins at the final two, or by being on stage when the last scene ends (T54).
6. The Director AI and its tiebreak are removed (T55).
7. Each bot wants to reach the final two and has a rival (T56).
8. A pass shows as "passed"; silence and polished lines are evidence (T57).
9. Last word: a reply for anyone @-mentioned in the final Free Talk round (T58).
10. Every line is capped at 15 words, the player's too (T59).
11. New win and lose screens: the reasoning, the top reason, the rivals (T60).
12. A stagehand in the player's earpiece teaches the rules on the first show (T61).

## Where they sit in "Open"

- T56 needs no editor and is free now.
- After T30, in this order: T51, T50, T59, T53, T52, T54, T55, T57, T58. All change `BP_Show`, so they go one at a time in the editor lane, before T38 and T34.
- T60 and T61 come after T33.
- T34 now also depends on T50, T53 and T57. T44 now also depends on T51.

## Watch for

- **`prompts.json`:** nine of these tasks change it. Commit those changes one at a time.
- **T44 and its prep:** a note now has a `category` and no `decoy`. `Docs/tasks/T44.md`, step 3, says so. The draft cards and the checker patch in `Docs/tasks/T44-build/` were written before the change, so check them for decoys before T44 uses them.
- **T30, T38, T34 and T33 build sheets:** the Director's tiebreak, the decoy sentence on the Scene Prep card and the 25-word cap are going away. Don't polish them.
- **T37 (error messages):** the Director role goes in T55, so it needs no error path.
