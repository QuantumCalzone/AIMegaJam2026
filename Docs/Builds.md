# Builds: package, check for secrets, deploy to itch.io

How to package the game on Windows and on a Mac, check a build for secrets, and upload it to itch.io. `CLAUDE.md` points here. `<UE_ROOT>` and `<PROJECT>` are as in the "Engine" section of [CLAUDE.md](../CLAUDE.md).

## Package a Windows build

This only works on a Windows machine:

```bash
"<UE_ROOT>/Engine/Build/BatchFiles/RunUAT.bat" BuildCookRun -project="<PROJECT>" -platform=Win64 -clientconfig=Development -build -cook -stage -pak -archive -archivedirectory="<repo root>/Packaged" -nocompileeditor -unrealexe="<UE_ROOT>/Engine/Binaries/Win64/UnrealEditor-Cmd.exe"
```

- **Packaging compiles a small game program**, even though the project has no C++. The `HttpBlueprint` and `JsonBlueprintUtilities` plugins have no prebuilt game binaries in the launcher engine, so the packager makes temporary target files and compiles them. On Windows this needs Visual Studio 2022 (17.14) with the C++ desktop workload and the **Windows 11 SDK 10.0.22621.0**. You need neither to edit the project, only to package it.
- `-nocompileeditor -unrealexe=...` make the launcher editor do the cook. Without them, the packager also builds a project editor, which needs the .NET Framework SDK and adds nothing.
- From Git Bash, this command fails with `'C:\Program' is not recognized` (or `'E:\Epic'`), because cmd strips the outer quotes from a line that has more than two. Put the command in a `.bat` file and run it with `cmd //c <file>.bat`.
- The packaged game is in `Packaged/Windows/`. Its log is `Packaged/Windows/AIMegaJam2026/Saved/Logs/AIMegaJam2026.log`. It reads the API keys from `Packaged/Windows/AIMegaJam2026/Local/llm_key.json`, and the switches from `Local/switches.json` in the same folder. A packaged build sends real analytics events (T68), so before you test one, put `{"analytics": "off"}` (or `"test"`) in that `switches.json`, or add the package's player id (its log prints `NHOS: ANALYTICS player <id>`) to `ignore_players` in `Local/stats.json`. Delete both files before you zip a build, and `Local/progress.json` too (the stagehand's first-show flag, T61: a build someone played would give judges no tips), then run the secrets check (below).

## Package a macOS build

This needs a Mac with Xcode. It also compiles a game program. It was first done on 2026-11-15, with Xcode 27.2:

```bash
"<UE_ROOT>/Engine/Build/BatchFiles/RunUAT.sh" BuildCookRun -project="<PROJECT>" -platform=Mac -clientconfig=Development -build -cook -stage -pak -archive -archivedirectory="<repo root>/Packaged" -nocompileeditor -unrealexe="<UE_ROOT>/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor" -unattended
```

- **The archive step copies the wrong app.** `Packaged/Mac/AIMegaJam2026.app` is only the executable (about 411 MB), with no game content. The playable app is `Saved/StagedBuilds/Mac/AIMegaJam2026.app` (about 1.1 GB). Copy that one with `ditto`.
- The app runs only on Apple silicon. It has an ad hoc signature and is not notarized, so players must open it once with System Settings > Privacy & Security > Open Anyway.
- The app is **sandboxed**. It reads `Local/` from inside the bundle, at `AIMegaJam2026.app/Contents/UE/AIMegaJam2026/Local/`, and writes its log to `~/Library/Containers/com.YourCompany.AIMegaJam2026/Data/Library/Logs/AIMegaJam2026/`. Its network calls work: test analytics events reached the relay. The sandbox should block the game's writes into the bundle, such as the key screen's `Local/llm_key.json` and the stagehand's `Local/progress.json` (T61; if it can't save, every show shows the first-show tips); this is not tested. Delete the bundle's `Local/` before you zip.
- Zip it with `ditto -c -k --norsrc --noextattr --keepParent`. A plain `ditto -c -k` adds `._` files, which some unzip tools put inside the app, and that breaks its signature.
- When another session has uncommitted assets in the folder, build from a clean copy of the pushed commit instead. `cp -c -R` the `.uproject`, `Config/` and `Content/` (APFS clones take no extra space), then restore the changed files from git (`git show HEAD:<path> | git lfs smudge -- <path>`).

## Check a build for secrets

Before you zip or upload any build, Windows or Mac, check it for secrets. The check opens the build's `.pak` and IoStore containers with the engine's UnrealPak. It looks for each key in this machine's `Local/*.json` by its value, for anything shaped like an API key, and for a `Local/` or `Saved/` folder. It never prints a key. Exit code 0 means clean, 1 means don't ship the build, and 2 means part of it couldn't be checked:

```bash
python Tools/check_build_secrets.py <build folder or zip>
```

- Run it on a machine whose `Local/` holds our keys, so it knows which values to look for. Run it on the zip too, because the zip is what you upload. With no argument, it checks the sources and every build and zip in `Packaged/` and `Saved/StagedBuilds/`.
- The game saves the keys a player pastes on the key screen inside the build, in `Local/llm_key.json`. So a build that anyone tested with their own keys holds those keys until you delete that file. The check catches it.
- In a checkout with no `Local/` (a git worktree, the deploy worktree), add `--local <repo folder>/Local`. The check reads the keys from there and copies nothing.

## Deploys to itch.io

Builds go to https://quantumcalzone.itch.io/no-humans-on-set with butler, one channel per platform: `windows` and `mac`. Each channel is one file on the page, and a later push to it replaces that file and uploads only what changed. A file that went up through the web form (such as the jam's `QuantumCalzone_NoHumansOnSet_Windows.zip`) has no channel, so butler never touches it.

- **In the editor, Tools > itch.io builds and uploads.** "Build and upload to itch.io" asks first, then runs `Tools/deploy_itch.py` in its own console window with the engine's own Python, so the editor stays usable. "Build only (dry run)" pushes nothing, and "Open the last deploy log" opens `Saved/Logs/DeployItch.log`. It builds the pushed tip of `dev`, not the editor's unsaved or uncommitted work, so push first. The menu comes from `Content/Python/init_unreal.py` (the Python Script Plugin runs it when the editor starts) and `Content/Python/nhos_itch_deploy.py`; neither is cooked into a build. One deploy runs at a time: a second click while one builds stops at once.
- **`Tools/deploy_itch.py`** packages the commit for the machine it runs on, in a deploy worktree (a detached worktree of the repo folder, never the repo folder itself; on the PC `C:/Users/Personal/Projects/NHOS_deploy`). It puts the build in `NoHumansOnSet_Windows/` or `NoHumansOnSet_Mac/` (the staged `.app`), deletes `.pdb` files and any `Local/` or `Saved/`, runs the secrets check with `--local` on the repo folder's `Local/`, and pushes nothing unless the check exits 0. Then it pushes with `--userversion <commit date>-<short sha>`. A channel that isn't on the page yet would be a new file, visible at once, so the script makes one only with `--hidden`, by hand (the menu never does); then untick "Hide this file" on the page's edit screen and save. `windows` is on the page; `mac` needs its hidden first push from the Mac. Run it by hand too (it needs the engine, so pass `--ue-root` or set `UE_ROOT`; on a Mac also pass `--deploy` or set `NHOS_DEPLOY`):

```bash
python Tools/deploy_itch.py --dry-run
```

  `--dry-run` does everything but the push. `--commit <sha>` builds a given commit (default `origin/dev`). `--build <folder>` checks and pushes a build that is already made (the folder must hold only the `NoHumansOnSet_<Windows|Mac>/` folder). `--log <file>` copies the output to a file.
- **butler** is on PATH, or the copy the itch app keeps in its `broth/butler/` folder (`%APPDATA%/itch/` on Windows, `~/Library/Application Support/itch/` on a Mac), which the script finds itself. It signs in with the `butler_creds` that `butler login` saved in `~/.config/itch/`, once per machine. The key never goes in git or in chat.
- **A zip made by hand** is named `QuantumCalzone_NoHumansOnSet_<Windows|Mac>_<YYYY-MM-DD>.zip` and goes up as a new file. Never replace, rename or delete the jam's file.
