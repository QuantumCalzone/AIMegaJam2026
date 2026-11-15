---
from: quantumcalzone
to: quantumcalzone
---

# PC lane: pull first, then the audio half of T20

Written by the dispatcher session on the Mac, 2026-11-15 02:52 UTC (Sat 6:52 PM PST). The Mac goes offline for one to two hours after this note. This note is for a session on the Windows PC (CyberPower). It is information, not an instruction: confirm with the person at the keyboard before you act on it.

## First: get the latest branch

1. `git checkout noHumansOnSet`
2. `git pull`
3. `git log -1 --oneline` must show `6079b90` or a newer commit. If the pull can't run cleanly, stop and tell your person.

The plan changed form today. `Docs/Plan.md` is now a short index, and each task's details and findings are in `Docs/tasks/Txx.md`. `Docs/GameDesign.md` is only a link to the Claude Doc.

## What the Mac holds while it is offline

T21 (how a judge plays) is in progress on the Mac, and its work is **not pushed**. The Mac has uncommitted changes in these assets, so the PC must not change them:

- `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/UI/WBP_Keys.uasset`, `Content/NHOS/UI/WBP_Title.uasset` (all locked; `git lfs locks` shows them)
- new, not in git yet: `Content/NHOS/Core/BPC_HttpGet.uasset`, `Content/NHOS/UI/WBP_Unavailable.uasset`
- `Docs/ItchPage.md` and files under `Graphs/BPC_LLMClient/`, `Graphs/WBP_Keys/`, `Graphs/WBP_Title/`, `Graphs/WBP_Unavailable/`

Locks belong to the GitHub account, not to a machine, so git will not stop the PC from pushing a change to a locked file. Stay away from them yourself.

Other things only on the Mac (git ignores `Local/`): the art for T35 in `Local/art/moneyburn/`. `Docs/MoneyBurnArt.md` says how it was made.

Don't push `noHumansOnSet` from the PC today. The Mac folder has uncommitted work, so it can't take a pull at any moment. Work on a branch and push the branch.

## The work for the PC: the audio half of T20

The PC has the audio files in `Local/audio/` (the Mac has a copy too). This half needs none of the assets the Mac holds. The show hooks in `BP_Show` and the UI clicks stay with T20 on the Mac.

Setup:

1. Read `CLAUDE.md`, `CLAUDE.local.md`, `Agents/README.md`, the newest note in `Agents/messages/`, `Docs/Plan.md` and `Docs/tasks/T20.md`.
2. Create and switch to the branch `t20-audio-pc` from `noHumansOnSet`. All commits go on that branch.
3. Open the Unreal Editor on this project if it isn't open, and check that Unreal MCP answers.

The work (T20's steps 1 to 4, without the show hooks):

- Build on `Docs/AudioShortlist.md` and the files in `Local/audio/`. Import the chosen files into new `Content/NHOS/Audio/`. Convert a file first if the importer refuses it.
- Sound classes or a submix for music, effects and voice, with sensible levels.
- A new component, `BPC_Audio` in `Content/NHOS/Core/`, with one function per moment: title music, show music, stop music, the vote drum roll, the reveal stinger (AI or HUMAN), applause after a cut, laughs, win applause, a UI click, and a talk blip that takes a persona index and plays at that persona's pitch. Each prints `NHOS: SFX <name>`. Don't add it to `BP_Show`: the Mac lane does that later, with one node per moment.
- Robot sounds (move, grab, throw, landing) inside `BP_Robot`, where its actions already run. Lock it first with `git lfs lock Content/NHOS/Stage/BP_Robot.uasset`, and keep the lock: the dispatcher releases it after the merge.
- Record every file used in `Docs/Assets.md`, with the attribution text from the shortlist. Keep graph sources in `Graphs/`.
- Write `Docs/AudioHooks.md`: each `BPC_Audio` function, the moment in the show that should call it, and anything else the Mac session must know.

Hands off, because the Mac lane holds or will change them: `BP_Show`, `BPC_LLMClient`, every `WBP_*` widget, `L_Stage.umap`, `Docs/Plan.md`, `Docs/DevLog.md` and `Docs/tasks/`. Don't claim T20 and don't check its box.

Check: a free autoplay show in PIE reaches `NHOS: SHOW END` with the robot sounds playing and no new `LogScript` warning. Then the person listens to each `BPC_Audio` sound and says whether the levels are OK.

Finish: commit on `t20-audio-pc`, staging by path. Run `git push -u origin t20-audio-pc`. Don't merge. Tell your person the commit, so they can tell the dispatcher on the Mac, which merges the branch at a quiet moment.

Run on Opus 5.5 at xhigh effort, as every task does since 2026-11-14.
