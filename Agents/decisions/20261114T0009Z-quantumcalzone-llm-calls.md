---
from: quantumcalzone
to: all
---

# LLM calls: Blueprint-only, and the packager compiles a game program

Decided in T02 of `Docs/MVPPlan.md`. The Claude call works from Blueprint in PIE (T01) and in a packaged Windows Development build (T02): both print `NHOS: SPIKE OK <text>`.

## Blueprint-only, no C++ module

- Every Claude call goes through `Content/NHOS/Core/BPC_LLMClient.uasset`. It uses two engine plugins: `HttpBlueprint` (the `Http Request` node) and `JsonBlueprintUtilities` (`Load Json from File/String`, `Get Field`, `Set Field`, `Get Json String`).
- Don't add a C++ module for LLM calls. Revisit this only if a later task needs something these nodes can't do. The nodes can't read the HTTP status code or response headers, and they can't stream.

## Packaging compiles code anyway

- The two plugins have no prebuilt game binaries in the launcher engine. When it packages, UAT writes temporary `.Target.cs` files and compiles a game executable. That took 35 s on the first build.
- Editing the project needs no compiler. Only the person who packages needs one:
  - **Windows:** Visual Studio 2022 17.14 with the C++ desktop workload, plus the **Windows 11 SDK 10.0.22621.0**. Without the SDK, the build fails at once with `Sdk: not found`.
  - **macOS:** Xcode. Not tried yet.
- The Windows package command in `CLAUDE.md` adds `-nocompileeditor -unrealexe="<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor-Cmd.exe"`. Without these flags, UAT also builds a project editor, which needs the .NET Framework 4.6+ SDK and gains nothing, because the launcher editor already has the plugins.

## Where the API key lives

- In `Local/llm_key.json`, which the game reads at `Get Project Directory` + `Local/llm_key.json`. Copy it from `Docs/llm_key.example.json`. Git ignores `Local/` and `Packaged/`.
  - In the editor, the file is in the repo root: `<repo>/Local/llm_key.json`.
  - In a packaged build, it is in `Packaged/Windows/AIMegaJam2026/Local/llm_key.json`. Packaging doesn't copy it there; copy it yourself to test.
- **Never ship a key.** Before you zip a build, delete `Local/` from it. Judges will need the key-entry screen or the relay from the design doc (see "After the MVP" in the plan).

## Where data files live and how the game reads them

- Runtime data lives in `Content/NHOS/Data/*.json`: settings, prompts, personas and scene cards. The game reads each file at `Get Project Content Directory` + `NHOS/Data/<file>.json` with `Load Json from File`. Long text is stored as arrays of lines.
- `Config/DefaultGame.ini` stages that folder as loose files (`DirectoriesToAlwaysStageAsNonUFS`). In a build they sit next to the pak, at `Packaged/Windows/AIMegaJam2026/Content/NHOS/Data/`, and the same Blueprint path finds them. So you can change a prompt in a packaged build without packaging again.
- A new data file needs no config change, as long as it goes in that folder.

## Also settled in T02

- HTTPS works in the packaged build with the certificates the engine already ships. No extra staging is needed.
- `GameDefaultMap` is `L_Stage`, and `DefaultGame.ini` cooks only `L_Stage`.
- The `GameFeatureData` asset scan in `DefaultGame.ini` is marked `bIsEditorOnly=True`, because packaged builds don't include Game Features.
- Seconds per call, cost per show and build size are recorded in "T02: packaged build results" in `Docs/MVPPlan.md`.
