# AIMegaJam2026

Our entry for the [2026 Epic AI MegaJam](https://itch.io/jam/2026-epic-ai-megajam). It's an Unreal Engine 5.8 project with Blueprints only, so there's no C++ to compile.

## What you need

- **Unreal Engine 5.8.4** from the Epic Games launcher, on Windows or macOS. Everyone must use the same version, because assets saved in a newer engine won't open in an older one.
- **Git with [Git LFS](https://git-lfs.com).** Install Git LFS *before* you clone. Unreal assets are stored in LFS.
- **macOS:** Epic lists macOS Sonoma 14.5 as the minimum for UE 5.8. Epic doesn't list macOS 27 yet; forum reports say 5.8.4 is the first 5.8 release that packages Mac builds on it. You only need Xcode to package a macOS build, not to work on the game.
- **Optional:** [Claude Code](https://claude.com/claude-code), in the desktop app or in a terminal.

## Get the project

```bash
git lfs install
```

```bash
git clone https://github.com/QuantumCalzone/AIMegaJam2026.git
```

If `.uasset` files are only a few hundred bytes after cloning, LFS wasn't set up. Run `git lfs install`, then `git lfs pull` in the repo folder.

## Open the project

- **Windows:** double-click `AIMegaJam2026.uproject`.
- **macOS:** launch Unreal Engine 5.8 from the Epic Games launcher. In the project browser, click **Browse** and pick `AIMegaJam2026.uproject`.

The first time it opens, the editor warns that some plugins are experimental (Unreal MCP). That's expected.

If git shows `AIMegaJam2026.uproject` as changed after you open it, and the only change is the `EngineAssociation` line, revert that line. Don't commit it. It should stay `"5.8"`.

## Use Claude Code with the editor (Unreal MCP)

The project turns on Unreal MCP. While the editor is open, it runs a local MCP server at `http://127.0.0.1:8000/mcp`, and `.mcp.json` points Claude Code at it. Claude can then build Blueprints, place actors, make materials and more, right in the editor.

1. Open the project in the editor.
2. Start Claude Code in the repo folder. In the desktop app, pick this folder. In a terminal, run `claude` from it.
3. Approve the `unreal-mcp` server when Claude Code asks. To skip that prompt from now on, add `"enabledMcpjsonServers": ["unreal-mcp"]` to your own `.claude/settings.local.json`. Git ignores that file.
4. If you restart the editor, reconnect `unreal-mcp` from `/mcp`.

If something else on your machine already uses port 8000, change the port in **Edit > Editor Preferences > Agentic Workflows > Model Context Protocol**. Then update the URL in your local `.mcp.json`, and don't commit that change.

[CLAUDE.md](CLAUDE.md) has the project details Claude Code reads: engine paths, commands, rendering settings and the jam rules.

## Working together

- **Binary assets can't be merged.** Two people editing the same Blueprint, level or asset means one person's work is lost. Agree on who edits what, and pull before you start.
- **Outside assets** (Fab and others) must be listed in the jam submission. Note the source and license when you add one.
- **Git LFS storage and bandwidth** count against the GitHub account's limits. Avoid committing large source files you don't need.

## Build the game

- **Windows builds must be packaged on Windows.** In the editor, use **Platforms > Windows > Package Project**. For the command-line version, see [CLAUDE.md](CLAUDE.md).
- A Mac can package a macOS build (this needs Xcode), but not a Windows one.

## Jam rules in short

- The theme is **"Director's Cut"**.
- Building runs Nov 12–15, 2026. The **deadline is Nov 15, 5:59 PM PST**, and late entries are disqualified.
- No game work before Nov 12. Anything made before the jam (prompts, scripts, assets) must be declared, including this repo's setup files.
- Teams can have up to 5 people. Any AI tools are allowed.
- Each team member must be 18 or older and have an active Epic Games account. The submission form asks for the email linked to that account.
- Partners email their codes to people who joined the jam on itch.io. Some codes have claim deadlines, so check the jam page.
- Full rules: the [itch.io jam page](https://itch.io/jam/2026-epic-ai-megajam) and the Official Rules linked there.
