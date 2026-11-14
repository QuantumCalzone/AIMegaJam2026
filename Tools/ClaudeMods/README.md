# Claude Code mods

Mods for Claude Code that help us run this project. A mod changes Claude Code's own interface. These don't touch the game and aren't part of the build.

Mods are an early-access feature of Claude Code. These were made with Claude Code 2.1.325.

## task-list

A pane beside the chat that shows the tasks in [Docs/Plan.md](../../Docs/Plan.md):

- **Done:** one collapsed line. Click it to see the tasks, crossed out.
- **In progress:** an unchecked task with a `Waiting:` or `Blocked:` line in the plan, a status file in `Agents/status/`, a claim lock on `Docs/claims/Txx`, or a session running in the desktop app. Each shows why (waits on you, blocked, running, claimed), the line it waits on, and the Code sessions whose title or name has its number (`T18: ...`, `t18-...`). Click a task or a session to open that session.
- **Not started:** each with "ready" or the unfinished tasks it waits for.

Tasks keep the plan's order, which is its priority order. A task added later shows where it sits in the plan, not where its number would put it.

The pane finds a task only under `## Tasks` in the plan, as a line that starts `- [ ] **Txx Title**` or `- [x] **Txx Title**`. "Changing the plan" in the plan describes that form. A task's status file is `Agents/status/task-Txx.md`; the older name, `mvp-Txx.md`, still counts.

It reads everything again every 20 seconds, and the claim locks every 2 minutes, because `git lfs locks` asks GitHub. `/task-list` opens the pane again after you close it.

Start the session in the repo folder: the mod reads the plan from the session's project folder. Sessions and status files are this computer's own. The plan and the claims are the same on every computer.

### Set it up

Use one of these. Both load the mod from this folder, so a `git pull` brings its changes.

**A. Load the folder in every session.** Add this to the `env` block of your own `~/.claude/settings.json` (not the project's settings), with the absolute path of this checkout, then start a new session:

```json
{
  "env": {
    "CLAUDE_CODE_PLUGIN_DIRS": "C:/path/to/AIMegaJam2026/Tools/ClaudeMods/task-list"
  }
}
```

If `CLAUDE_CODE_PLUGIN_DIRS` already names a folder, add this one after it in the same value, separated by `;` on Windows or `:` on macOS.

A session picks up changes when it starts. To have a running desktop session reload the mod when its files change, also set `"CLAUDE_CODE_PLUGIN_DIR_WATCH": "1"` there.

**B. Install it from this folder.** In a terminal:

```bash
claude plugin marketplace add "C:/path/to/AIMegaJam2026/Tools/ClaudeMods"
```

```bash
claude plugin install task-list@nhos-mods
```

It is read from this folder, not from a copy, so after a `git pull` run `/reload-plugins` in a session to load the new version.

### Change it

The code is `task-list/hooks/register.tsx`. The test is `task-list/hooks/task-list.test.tsx`; run it, and check the mod, with:

```bash
claude plugin test Tools/ClaudeMods/task-list
```

```bash
claude plugin validate Tools/ClaudeMods/task-list
```

When Claude Code loads the mod, it writes the API types to `task-list/.claude-plugin/types/`, with a `.gitignore` that keeps them out of git.

### Where it opens a session

A click first asks the desktop app to show the session in this window (`ccd_window` `open_session_in`). The app allows that only for sessions this session started, so for any other session the mod opens the session's `claude://` link with the operating system (`start` on Windows, `open` on macOS), which brings it up in the app. In a terminal session without the desktop app, the pane shows the tasks and says the sessions are unavailable.
