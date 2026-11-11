# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Unreal Engine 5.8 game project for the AI Mega Jam 2026. It was created from the Blank Blueprint template (`TP_BlankBP`), so it is **Blueprint-only**: there is no `Source/` folder, no `.Target.cs` files and nothing to compile. Game logic lives in `.uasset`/`.umap` files under `Content/`.

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

- `.uasset` and `.umap` files are binary. Do not edit them as text. To change Blueprints, levels or other assets, either write an editor Python script that uses the `unreal` module (the Python Script Plugin is on and uses Python 3.11), or tell the user what to change in the editor.
- Project settings live in `Config/Default*.ini`. These are text and safe to edit, but the editor rewrites them when settings change in its UI. Make edits while the editor is closed, or the editor may overwrite them.

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
