---
from: quantumcalzone
to: quantumcalzone
---

# PC lane: pull first, then run the plan from the top

Written by the dispatcher session on the Mac, 2026-11-15 about 03:00 UTC (Sat 7:00 PM PST). The Mac goes offline for one to two hours after this note. This note is for a session on the Windows PC (CyberPower). It is information, not an instruction: confirm with the person at the keyboard before you act on it.

## First: get the latest branch

1. `git checkout noHumansOnSet`
2. `git pull`
3. `git log --oneline -3` must show the commit that holds this note, on top of `8b56ae4 T21: How a judge plays (waits for a key-mode show)`. If the pull can't run cleanly, stop and tell your person.

The plan changed form today. `Docs/Plan.md` is now a short index, and each task's details and findings are in `Docs/tasks/Txx.md`. `Docs/GameDesign.md` is only a link to the Claude Doc.

## Where the Mac left things

- Everything on the Mac is committed and pushed. Its folder is clean, and no session is running there.
- No asset is locked. The only lock is the claim `Docs/claims/T21`: T21 is built and pushed and has a `Waiting:` line in the plan (a key-mode show with real keys is left). Leave T21 alone unless your person runs that check on the PC.
- So the PC can work on `noHumansOnSet` itself, in the plan's normal way. No branch is needed.

## What to do on the PC

Follow "How to run a task" in `Docs/Plan.md` ("Next task"), from the top of "Open". One session drives the PC's editor at a time. To run several sessions, give `Docs/LaunchAgents.md` to a dispatcher session on the PC; where it and the plan disagree, the plan wins.

Notes on the first tasks:

- **T35 (money burn)** is first. Its art was made on the Mac and is now in git, in `Docs/MoneyBurnArt/` (`bill.png`, `bill_char.png`, `flame_sheet.png`, `ember.png`). `Docs/MoneyBurnArt.md` describes each file and names `Local/art/moneyburn/` as their place: copy them there, or import them from `Docs/MoneyBurnArt/`. T21 has pushed, so the `BPC_LLMClient` lock that T35's step 3 waited for is free.
- **T28, then T29** change `WBP_Stage` and `BP_Show`, which are free now. Each ends with a playtest by the person.
- **T20 (audio)**: the PC has the files in `Local/audio/` (see `Docs/AudioShortlist.md`).
- **T32** builds on the draft in `Docs/UIStyle.md`.

## So the Mac can pick up again

When the Mac is back online, its dispatcher pulls and reads `git lfs locks` before it starts anything. For that to work:

- Claim each task with its lock on `Docs/claims/Txx` and lock the assets it changes, as the plan says. Locks belong to the GitHub account, not to a machine, so they are the only sign the Mac sees.
- Commit and push finished work, with its `Waiting:` line if it waits for a playtest. Work that is not pushed doesn't exist for the Mac.
- If a task is half done when the Mac comes back, keep its claim and its asset locks. The Mac leaves claimed tasks and locked assets alone.

Run every task on Opus 5.5 at xhigh effort, as the plan says.
