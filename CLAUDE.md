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
- **Submission:** a packaged Windows build, zipped as `TeamName_GameName`, under 1 GB (use butler for larger builds), uploaded to itch.io. It needs a 30–60 second gameplay video. A dev log is optional but required for the Glass Box category. A "Tools you used" field is optional but required for some partner prizes. Web builds need the separate UE 5.9 MegaJam Preview, so this 5.8 project targets desktop.
- **Judging:** each entry is scored 1–5 on all of: ambition and innovation, theme, fun, gameplay, visuals, level design and progression, and audio. Audio and progression count as much as visuals.

## Engine

- `AIMegaJam2026.uproject` points to the engine with a GUID (`EngineAssociation`), not a version string. On this machine the GUID resolves (through `HKCU\Software\Epic Games\Unreal Engine\Builds`) to the launcher install at `E:/Epic Games/UE_5.8` (5.8.4). On another machine, use "Switch Unreal Engine version" on the `.uproject` to fix the association.
- Editor binaries: `E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe` (GUI) and `UnrealEditor-Cmd.exe` (headless and commandlets).

## Commands

Open the editor:

```bash
"E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" "C:/Users/Personal/Projects/AIMegaJam2026/AIMegaJam2026.uproject"
```

Run an editor Python script headless (the editor must be closed if the script saves assets):

```bash
"E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" "C:/Users/Personal/Projects/AIMegaJam2026/AIMegaJam2026.uproject" -run=pythonscript -script="C:/path/to/script.py"
```

Package a Windows build:

```bash
"E:/Epic Games/UE_5.8/Engine/Build/BatchFiles/RunUAT.bat" BuildCookRun -project="C:/Users/Personal/Projects/AIMegaJam2026/AIMegaJam2026.uproject" -platform=Win64 -clientconfig=Development -build -cook -stage -pak -archive -archivedirectory="C:/Users/Personal/Projects/AIMegaJam2026/Packaged"
```

Editor log (also catches Python output and errors): `Saved/Logs/AIMegaJam2026.log`.

## Working with assets

- `.uasset` and `.umap` files are binary. Do not edit them as text. To change Blueprints, levels or other assets, use Unreal MCP (see below) when the editor is running. Otherwise, write an editor Python script that uses the `unreal` module (the Python Script Plugin is on and uses Python 3.11), or tell the user what to change in the editor.
- Project settings live in `Config/Default*.ini`. These are text and safe to edit, but the editor rewrites them when settings change in its UI. Make edits while the editor is closed, or the editor may overwrite them.

## Unreal MCP

UE 5.8 includes **Unreal MCP**, the experimental `ModelContextProtocol` plugin. It runs an MCP server inside the editor process at `http://127.0.0.1:8000/mcp`. Through it, an agent can spawn and edit actors, build Blueprints and Widget Blueprints, author materials, MetaSounds, Niagara, PCG and Sequencer content, and run automation tests. Docs: https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor

- **Not enabled in this project yet.** In this engine install the plugin is off by default. To turn it on, add `ModelContextProtocol` and `AllToolsets` to the `Plugins` list in the `.uproject` (with the editor closed) or use Edit > Plugins. Then restart the editor and click Edit > Editor Preferences > Agentic Workflows > Model Context Protocol > Generate Client Config. This writes `.mcp.json` to the project root. Start Claude Code from the project root after the editor is running.
- The server uses tool search: it lists four meta-tools (`list_toolsets`, `describe_toolsets`, `describe_tools`, `call_tool`), not every tool. Find tools with those first.
- Tool calls run one at a time on the game thread. Don't send several calls in parallel. Claude Code stops waiting after about 120 seconds, so split long work (big scripts, asset scans, automation runs) into shorter calls.
- The server only exists while the editor runs. Commandlets don't start it unless you pass `-ModelContextProtocolStartServer`.
- Instructions for every connecting agent can be set in Project Settings > Agentic Workflows > Model Context Protocol > Instructions. They are stored in `DefaultGame.ini`.
- Server logs use the `LogModelContextProtocol` category in the editor log.

## Rendering and project configuration

These settings (in `Config/DefaultEngine.ini`) affect how content must be authored:

- Lumen for global illumination and reflections, Virtual Shadow Maps and hardware ray tracing are on. Static lighting is off (`r.AllowStaticLighting=False`), so do not rely on baked lightmaps.
- **Substrate** materials are on (`r.Substrate=True`). Build materials with Substrate nodes, not the legacy material model.
- Windows uses DX12 with SM6. Target hardware is Desktop with Maximum quality.
- `GameDefaultMap` points to the engine template `/Engine/Maps/Templates/OpenWorld` (a World Partition map). Change it when the project has its own map.
- Input uses **Enhanced Input** (`EnhancedPlayerInput` / `EnhancedInputComponent`). Make Input Actions and Mapping Contexts, not legacy action or axis mappings.
- The `ModelingToolsEditorMode` plugin is on (editor only).

## Source control

- Remote: `https://github.com/QuantumCalzone/AIMegaJam2026.git`, branch `main`.
- `.gitignore` excludes the folders the engine generates (`DerivedDataCache/`, `Intermediate/`, `Saved/`, `Binaries/`) and packaged builds in `Packaged/`. Don't archive builds into `Build/`, because Unreal uses that folder for project build settings.
- **Git LFS** stores binary files (see `.gitattributes`): `.uasset`, `.umap`, models, images, audio, fonts and archives. When you add a new kind of binary file, add an LFS rule for it before you commit it.
