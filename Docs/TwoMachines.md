# Two machines at once: a dispatcher on each

How to work on the jam from two machines at the same time, for example the Mac and the Windows PC. We first did this on 2026-11-15. Either machine can take either role, so the same steps work from both.

[LaunchAgents.md](LaunchAgents.md) holds the dispatcher's own instructions. This file says how the two machines fit together, what we learned, and the text to paste.

## When this applies

This setup is not always in use. It is active when you say so, or when a machine's repo folder has a dispatcher's ledger, `Agents/status/dispatcher.md`. Only then do the split and the dispatcher rules apply. When it is not active, a session takes the first free task in the plan's order, whatever machine a task's entry names; the claims and locks work as always.

A dispatcher deletes its ledger when you stop (see "Set it up"), so that later sessions on that machine don't take the setup as active.

## The parts

| Part | What it does | Where it lives |
|---|---|---|
| The split | Says which machine may take which task, so that the machines don't race for an asset. | This file, and each dispatcher's ledger. |
| A dispatcher session, one per machine | Keeps the ledger, talks to the other machine's dispatcher, tells you what waits on you. It starts task sessions only when you type to it. | A Claude session on the repo folder. Its ledger is `Agents/status/dispatcher.md`, which git ignores. |
| Claims and locks | The only thing both machines see at once. A claim is an LFS lock on `Docs/claims/Txx`. | GitHub, through `git lfs locks`. |

## The split

Most editor tasks change `BP_Show.uasset` or `WBP_Stage.uasset`, and only one session on either machine can hold those. So:

- **The chain machine** keeps the in-show editor chain: it takes only tasks whose Touches line names `BP_Show.uasset` or `WBP_Stage.uasset`.
- **The other machine** takes the rest, in the plan's order: editor tasks on other assets, and tasks that need no editor (data files, docs, generated art, the relay).

Pick the chain machine once: the one that holds an asset of the chain now, or else the one with the faster editor. On 2026-11-15 the PC was the chain machine and the Mac was the other machine.

**Tasks that fall between.** A task that names neither `BP_Show` nor `WBP_Stage`, but shares another asset with the chain (`BP_Robot`, `WBP_MoneyBurn`, `BPC_LLMClient`, `BPC_LinePlayer`, `WBP_ChatLine`), belongs to the other machine. On 2026-11-15 these were T36 and T46. Start such a task when the chain doesn't hold its assets, or move it to the chain machine.

## Set it up

Do this on each machine:

1. `git pull` on `dev`, then open the Unreal Editor on the project, so that Unreal MCP is up.
2. In the Claude desktop app's Code tab, start a session on the repo folder itself, with no worktree, on Fable 5.2. Turn on Remote Control in it, so that the two dispatchers can see and message each other. Paste the dispatcher message below.
3. Before you leave: keep the machine plugged in and awake with the lid open, and leave the Claude app and the editor open.
4. Write down your answer for every open task that needs one before it can work (its Needs line says "my answer" or "my OK"), in the task's file.

To stop: tell each dispatcher that you are stopping ([LaunchAgents.md](LaunchAgents.md), step 4). Once its sessions are done, the dispatcher deletes its ledger, `Agents/status/dispatcher.md`. Without a ledger, the setup is not active on that machine (see "When this applies").

## What we learned

- **A dispatcher can't start a session by itself.** The app allows a start only on a message that you type in the desktop app. It refuses a start on a turn that a session's note or the other dispatcher's message woke, and while you work over Remote Control. On those turns the dispatcher can only post a card for you to click, or tell you.
- **Rejected pushes are normal,** because both machines push to one branch. A session may run `git pull --rebase` and push again when `git status` shows no uncommitted work from another session. Never `--autostash`, never a force-push.
- **`Docs/Plan.md` conflicts often.** Every task commit changes the "Next up" line. When both machines finish close together, the second one's rebase stops there, and that session waits for you. The fix is to keep both sides' lines. Whether a session may do that by itself is not decided yet.
- **The usage limit stops every session at once,** on both machines. A stopped session keeps its claim and its status file. After the limit resets, message the session to go on, or archive it and release its claim so that another session can take the task.
- **A paid step needs a cap.** Each art task names its Meshy credits. Give the running session the balance it should find, and tell it to stop if the balance is lower.

## Text to paste

### The dispatcher message

Fill in the two machine names and pick one of the two last sentences:

```text
Be this machine's dispatcher. Follow the Prompt section of Docs/LaunchAgents.md, and read Docs/TwoMachines.md first.

This machine is <the Mac | the PC>. A second dispatcher runs at the same time on <the other machine>, with its own editor and its own sessions. Both machines use the same branch and the same GitHub account, so check the claims before every start, and keep a machine for every open task in your ledger.

<This machine is the chain machine: it keeps the BP_Show / WBP_Stage chain. | This machine is the other machine: it takes editor tasks on other assets, tasks that need no editor, and prep pieces the chain machine hasn't started.>
```
