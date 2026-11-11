# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Unreal Engine 5.8 game project for the AI Mega Jam 2026. It was created from the Blank Blueprint template (`TP_BlankBP`), so it is **Blueprint-only**: there is no `Source/` folder, no `.Target.cs` files and nothing to compile. Game logic lives in `.uasset`/`.umap` files under `Content/`.

## Game jam rules (2026 Epic AI MegaJam)

Source: the jam's itch.io page (https://itch.io/jam/2026-epic-ai-megajam). The Official Rules PDF linked there is the final authority.

- **Dates:** The theme is revealed at the kickoff livestream on Nov 11, 2026, 11 AM PST. Building runs from Nov 12, 12:00 AM EST, to the **deadline on Nov 15, 5:59 PM PST (8:59 PM EST)**. Late entries are disqualified.
- **No game work before Nov 12.** Any prompts, scripts or assets made before the jam must be declared in the submission. This includes this repo's setup files (CLAUDE.md, `.gitignore`, `.gitattributes`).
- **AI:** Any AI tools are allowed, with no limit on agents.
- **Outside assets** (Fab and others) are allowed if the license permits. Every one must be listed in the submission, so record each asset's source and license when you add it.
- **Team:** solo, or up to 5 people.
- **Eligibility:** each entrant must be 18 or older and have an active Epic Games account. The submission form asks for each member's name and the email linked to their Epic account.
- **Partner codes:** partners email their codes to people who joined the jam on itch.io. Some codes have claim deadlines (the jam page lists Anthropic as Nov 12–27 and Meshy as by Nov 17). Check the jam page for the others.
- **Build configuration:** the jam page lists the platforms as "Windows 10 or 11, macOS, Android, or iOS (development build)". It is not clear if that note is for all platforms or only for iOS. The package commands below use `-clientconfig=Development`. Read the Official Rules before you change to Shipping.
- **Submission:** a packaged build (Windows 10 or 11, macOS, Android or iOS; this project targets Windows), zipped as `TeamName_GameName`, under 1 GB (use butler for larger builds), uploaded to itch.io. It needs a 30–60 second gameplay video. A dev log is optional but required for the Glass Box category. A "Tools you used" field is optional but required for some partner prizes. Web builds need the separate UE 5.9 MegaJam Preview, so this 5.8 project targets desktop.
- **Judging:** each entry is scored 1–5 on all of: ambition and innovation, theme, fun, gameplay, visuals, level design and progression, and audio. Audio and progression count as much as visuals.

## Engine

Contributors work on Windows and macOS. Everyone must use **UE 5.8.4**, because assets saved in a newer engine version won't open in an older one. 5.8.4 is also the first 5.8 release reported to package Mac builds on macOS 27.

- `EngineAssociation` in the `.uproject` is `"5.8"`, which matches an Epic launcher install of 5.8 on either platform. If opening the project rewrites it (to a `{GUID}` or anything else), revert that line and never commit it.
- Engine root, written `<UE_ROOT>` below:
  - Windows launcher default: `C:/Program Files/Epic Games/UE_5.8`
  - macOS launcher default: `/Users/Shared/Epic Games/UE_5.8`
  - A custom install location may also be listed in your own `CLAUDE.local.md`. Git ignores that file; use it for notes about your own machine.
- Editor binary:
  - Windows: `<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor.exe` (GUI) and `UnrealEditor-Cmd.exe` (headless and commandlets).
  - macOS: `<UE_ROOT>/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor`, for both GUI and commandlets.
- `<PROJECT>` below is the absolute path to `AIMegaJam2026.uproject` in the repo root. On Windows, give the engine a Windows-style path (`C:/...`), not a Git Bash path (`/c/...`).

## Commands

Open the editor (Windows shown; on macOS use the macOS editor binary):

```bash
"<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor.exe" "<PROJECT>"
```

Run an editor Python script headless (the editor must be closed if the script saves assets). On macOS, use the macOS editor binary in place of `UnrealEditor-Cmd.exe`:

```bash
"<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "<PROJECT>" -run=pythonscript -script="<absolute path to script.py>"
```

Package a Windows build. This only works on a Windows machine:

```bash
"<UE_ROOT>/Engine/Build/BatchFiles/RunUAT.bat" BuildCookRun -project="<PROJECT>" -platform=Win64 -clientconfig=Development -build -cook -stage -pak -archive -archivedirectory="<repo root>/Packaged"
```

Package a macOS build. This needs a Mac with Xcode:

```bash
"<UE_ROOT>/Engine/Build/BatchFiles/RunUAT.sh" BuildCookRun -project="<PROJECT>" -platform=Mac -clientconfig=Development -build -cook -stage -pak -archive -archivedirectory="<repo root>/Packaged"
```

Editor log (also catches Python output and errors): `Saved/Logs/AIMegaJam2026.log`.

## Working with assets

- `.uasset` and `.umap` files are binary. Do not edit them as text. To change Blueprints, levels or other assets, use Unreal MCP (see below) when the editor is running. Otherwise, write an editor Python script that uses the `unreal` module (the Python Script Plugin is on and uses Python 3.11), or tell the user what to change in the editor.
- Project settings live in `Config/Default*.ini`. These are text and safe to edit, but the editor rewrites them when settings change in its UI. Make edits while the editor is closed, or the editor may overwrite them.

## Unreal MCP

UE 5.8 includes **Unreal MCP**, the experimental `ModelContextProtocol` plugin. It runs an MCP server inside the editor process at `http://127.0.0.1:8000/mcp`. Through it, an agent can spawn and edit actors, build Blueprints and Widget Blueprints, author materials, MetaSounds, Niagara, PCG and Sequencer content, and run automation tests. Docs: https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor

- **How it's set up here** (UE 5.8.4 has both the plugin and auto-start off by default, unlike the docs):
  - `ModelContextProtocol` and `AllToolsets` are enabled in the `.uproject`, limited to the Editor target, so packaged builds don't include the server.
  - Auto-start is on through `Config/DefaultEditorPerProjectUserSettings.ini` (`bAutoStartServer=True`), so the server starts whenever the editor opens.
  - `AllToolsets` pulls in Game Features, which needs the `GameFeatureData` entry under `AssetManagerSettings` in `DefaultGame.ini`. Without that entry, the editor reports load errors at startup.
  - `.mcp.json` in the project root (written by `ModelContextProtocol.GenerateClientConfig ClaudeCode`) points Claude Code at the server as `unreal-mcp`.
- **Connecting:** open the editor first, then start Claude Code from the project root. A session that started before the editor won't see the server until it reconnects. Each person approves `unreal-mcp` once, or adds `"enabledMcpjsonServers": ["unreal-mcp"]` to their own `.claude/settings.local.json` (git ignores that file).
- The server uses tool search. In 5.8.4 it lists three meta-tools, not the four in the docs: `list_toolsets`, `describe_toolset` and `call_tool`. In Claude Code they appear as `mcp__unreal-mcp__<name>`. Start with `list_toolsets`, then `describe_toolset` to get a toolset's tools, then `call_tool` to run one. Every editor action, read or write, goes through `call_tool`.
- If the editor restarts during a session, the connection drops. Reconnect `unreal-mcp` from `/mcp`.
- Tool calls run one at a time on the game thread. Don't send several calls in parallel. Claude Code stops waiting after about 120 seconds, so split long work (big scripts, asset scans, automation runs) into shorter calls.
- The server only exists while the editor runs. Commandlets don't start it unless you pass `-ModelContextProtocolStartServer`.
- Instructions for every connecting agent can be set in Project Settings > Agentic Workflows > Model Context Protocol > Instructions. They are stored in `DefaultGame.ini`.
- Server logs use the `LogModelContextProtocol` category in the editor log.

## Rendering and project configuration

These settings (in `Config/DefaultEngine.ini`) affect how content must be authored:

- Lumen for global illumination and reflections, Virtual Shadow Maps and hardware ray tracing are on. Static lighting is off (`r.AllowStaticLighting=False`), so do not rely on baked lightmaps.
- **Substrate** materials are on (`r.Substrate=True`). Build materials with Substrate nodes, not the legacy material model.
- Windows uses DX12 with SM6, and macOS uses Metal SM6. Target hardware is Desktop with Maximum quality.
- `GameDefaultMap` points to the engine template `/Engine/Maps/Templates/OpenWorld` (a World Partition map). Change it when the project has its own map.
- Input uses **Enhanced Input** (`EnhancedPlayerInput` / `EnhancedInputComponent`). Make Input Actions and Mapping Contexts, not legacy action or axis mappings.
- The `ModelingToolsEditorMode` plugin is on (editor only).

## Source control

- Remote: `https://github.com/QuantumCalzone/AIMegaJam2026.git`, branch `main`.
- `.gitignore` excludes the folders the engine generates (`DerivedDataCache/`, `Intermediate/`, `Saved/`, `Binaries/`) and packaged builds in `Packaged/`. Don't archive builds into `Build/`, because Unreal uses that folder for project build settings.
- **Git LFS** stores binary files (see `.gitattributes`): `.uasset`, `.umap`, models, images, audio, fonts and archives. When you add a new kind of binary file, add an LFS rule for it before you commit it.
- Binary assets can't be merged. Before changing a Blueprint, level or other asset, pull first. If someone else may be editing the same asset, check with the user.
- `README.md` holds the setup steps for human contributors. Keep it in step with this file when setup changes.
