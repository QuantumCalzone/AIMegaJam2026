# T92 build sheet: the Mac upload

Back to [T92](T92.md) and [the plan](../Plan.md). A prep session wrote this on the Mac on 2026-11-19, before T91 started. It read the code and ran only commands that read. It did not package a build, make a worktree, run butler, open the editor or change any code. The line numbers are those at `72c00ed`. T91 will move them, so find each line by its code, not its number.

## In short

Fix these before the first run on the Mac. Each one has its own section below.

1. **No butler on this Mac.** The itch data folder has an empty `broth/butler/versions/`, and the itch app is not installed for this user. T92 needs your OK to download butler 15.32.0 for darwin-arm64 from broth. It is a 9.6 MiB zip.
2. **Log in with butler before the first dry run.** `deploy_itch.py` runs `butler status` in a dry run too, as soon as it finds butler. T89 found that a `butler status` with no saved sign-in starts butler's browser login by itself.
3. **The menu can't pass `NHOS_DEPLOY`.** The menu's Terminal window runs a fresh login shell, not the editor's environment. Add a Mac default for the deploy worktree to `deploy_itch.py`.
4. **`stop_leftovers` never matches on the Mac.** `ps -o comm=` gives a column cut to 16 characters, and the engine path has a space in it.
5. **An ad hoc re-sign must keep the entitlements.** A plain `codesign --force --deep --sign -` removes the app's sandbox entitlements.
6. **The `codesign --verify --deep --strict` gate goes after the secrets check.** With that order, a key planted for Done-when 2 still stops the run at the secrets check.
7. **Disk: 20 GiB free (98% used).** A first package and the step 5 tests need about 10 to 14 GiB. Free some space first, so that 30 GiB or more is free.

## What this Mac has today

All found with commands that only read, on 2026-11-19.

| Item | Found | For T92 |
|---|---|---|
| macOS | 27.2.1 (26B131), arm64, Apple M2 Max, 96 GiB RAM | OK |
| Xcode | Xcode 27.2 (27B52), `xcode-select -p` = `/Applications/Xcode.app/Contents/Developer`, Apple clang 21.0.0, SDK 27.2 | OK. Builds.md's first Mac package used this Xcode. There is no separate command line tools package (no `CLTools_Executables` receipt). Xcode's own tools are enough. |
| Engine | `/Users/Shared/Epic Games/UE_5.8`, `Build.version` 5.8.4 (CL 58902052). `RunUAT.sh`, `Engine/Binaries/Mac/UnrealPak` and the engine's Python 3.11.8 (`Engine/Binaries/ThirdParty/Python3/Mac/bin/python3`) are all there | OK. These are the paths that `deploy_itch.py`, `check_build_secrets.py` and the menu expect. |
| The menu | The editor log of 2026-11-18 reads `NHOS: ITCH MENU added (Tools > itch.io, 3 entries)` | The menu loads on the Mac. No entry has run yet. |
| Editor log | `~/Library/Logs/Unreal Engine/AIMegaJam2026Editor/AIMegaJam2026.log`. The project has no `Saved/Logs/` | The menu's log `Saved/Logs/DeployItch.log` still goes in the project, because `_log_path()` builds the path from the project folder and makes the folder. CLAUDE.md's "Editor log: `Saved/Logs/...`" is true only on Windows (see "Docs", below). |
| butler | Not on PATH. `~/Library/Application Support/itch/broth/butler/versions/` is empty (made 2026-11-15 17:04), with no `.chosen-version`. No `itch.app` for this user (Spotlight finds one only in another account's home) | **Missing.** See "Step 2". |
| butler's sign-in | `~/.config/itch/butler_creds` does not exist (only checked that it exists; not read) | You run `butler login`. |
| Deploy worktree | `git worktree list`: the repo folder (`dev`) and two old app worktrees under `.claude/worktrees/` (`t100-music`, `t90-design-docs`; not ours, leave them alone). No `NHOS_deploy` | `deploy_itch.py` makes it on its first run (`git worktree add --detach`). |
| Free disk | 20 GiB free of 926 GiB (98% used) on `/System/Volumes/Data` | **Tight.** See "Disk". |
| git, git-lfs | git 2.54.0 (Apple Git-157). git-lfs **3.0.2, darwin amd64** (2021, runs under Rosetta), in `/usr/local/bin` | It works in the repo folder today. If `git lfs pull` in the new worktree fails, update git-lfs first. |
| Python | `python` is **not** on PATH. `python3` is 3.13.0 (`/usr/local/bin`). The engine's Python is 3.11.8 | By hand, use `python3` or the engine's Python. Builds.md's `python Tools/deploy_itch.py` fails on this Mac as written. |
| Login shell PATH | `zsh -lic` gives `/usr/local/bin:...`, so the Terminal window finds `git`, `git-lfs` and `python3` | OK for the menu's Terminal window. |
| `Local/` | `art/`, `audio/`, `leonardo_key.json`, `llm_key.json`, `meshy_key.json`, `stability_key.json`, `stats.json`, `switches.json` (names only) | The secrets check finds our keys from `--local <repo>/Local`. |
| Existing Mac builds | None. No `Saved/StagedBuilds/`, `Packaged/` is empty, and Spotlight finds no `AIMegaJam2026.app` | Nothing to test `codesign` or the secrets check on before the first package. |
| Shared DDC | `~/Library/Application Support/Epic/UnrealEngine/Common/DerivedDataCache`, 1.5 GB | The deploy worktree's cook reuses it. |
| Sandbox entitlements | `BaseEngine.ini`: `PremadeMacEntitlements=.../Sandbox.Server.entitlements` (Development), `ShippingSpecificMacEntitlements=.../Sandbox.NoNet.entitlements`. The engine's `Sandbox.Client.entitlements` has `app-sandbox` and `network.client`. The project's `Config/` sets no signing or entitlements | Our Development build gets the engine's premade sandbox entitlements. A re-sign must keep them. |

## The Mac path as the code has it today

What happens when you click Tools > itch.io > "Build only (dry run)" in the Mac editor. **OK** means the line should work as it is. **CHANGE** points to a change in the next section.

### The menu: `Content/Python/nhos_itch_deploy.py`

1. `_project_dir()` (line 27) gives `/Users/personal/Projects/AIMegaJam2026`. **OK.**
2. `_engine_root()` (line 31): the editor log gives `Base Directory: /Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/`, so `engine_dir()` resolves to `.../UE_5.8/Engine/`, and the root is `/Users/Shared/Epic Games/UE_5.8`. **OK** (not checked in the editor).
3. `_engine_python()` (line 41): `Engine/Binaries/ThirdParty/Python3/Mac/bin/python3` exists (3.11.8). **OK.**
4. `launch()` (lines 60 to 62) builds `args = [python, -u, Tools/deploy_itch.py, --repo, <project>, --ue-root, <root>, --log, Saved/Logs/DeployItch.log, (--dry-run)]`. **CHANGE M2** (the deploy worktree: see "How the menu finds the deploy worktree").
5. Lines 71 to 75 write `Saved/DeployItch.command`: `#!/bin/sh`, then `cd ` + `subprocess.list2cmdline([project])`, then the args in single quotes. `list2cmdline` uses Windows quoting (double quotes, backslashes). It works only because the project path has no space, `$` or quote. **CHANGE M1.**
6. Line 76: `open -a Terminal Saved/DeployItch.command`. Terminal runs the file in a **new login shell**, with the user's own environment from `~/.zprofile` and `~/.zshrc`, not the editor's. When the script ends, the window stays open only if the Terminal profile's "When the shell exits" is "Don't close the window" (the default). **OK, check it in the editor** (open question Q7).
7. `open_log()` (line 104): `open <log>` opens it in the default app for `.log` (Console). **OK.**
8. `build_and_upload()` (line 80): the dialog text says "the pushed tip of dev". **T91 changes it** (see "What T91 changes under T92").

### The script: `Tools/deploy_itch.py`

1. `this_platform()` (line 174): `Darwin` gives `mac`. **OK.**
2. `find_repo()` (line 181): the menu passes `--repo`. **OK.**
3. Line 411: `local = repo / "Local"` exists. **OK.**
4. Line 414: `deploy_arg = args.deploy or NHOS_DEPLOY or DEFAULT_DEPLOY.get("mac")`, and `DEFAULT_DEPLOY` (line 73) has only `windows`. So a menu run stops at line 416: "no deploy worktree: pass --deploy or set NHOS_DEPLOY". **CHANGE M3.**
5. `find_ue_root()` (line 192): the menu passes `--ue-root`. The launcher default is also in `UE_ROOTS["mac"]`. **OK.**
6. `find_butler()` (line 206): `--butler`, then `BUTLER`, then PATH, then `~/Library/Application Support/itch/broth/butler/.chosen-version` → `versions/<v>/butler`. Today it finds nothing. A dry run goes on without butler, and a real push stops at line 420. **OK once butler is installed in that layout** (see "Step 2").
7. `take_lock()` (line 143): `/Users/personal/Projects/NHOS_deploy.lock`. `_alive()` uses `os.kill(pid, 0)`. **OK.**
8. `prepare_worktree()` (line 258): `git fetch origin dev` (T91 changes the branch), then `git worktree add --detach` on the first run. On later runs, `stop_leftovers`, `reset --hard`, `clean -fdq`, `checkout --detach --force` and `lfs pull`. **OK, except `stop_leftovers`: CHANGE M4.**
9. `package_mac()` (line 305):
   - Lines 309 to 311 delete an old `Saved/StagedBuilds/Mac/AIMegaJam2026.app` in the deploy worktree. **OK.**
   - Lines 312 to 314: `RunUAT.sh BuildCookRun ... -platform=Mac -clientconfig=Development -build -cook -stage -pak -archive -archivedirectory=<run_dir>/archive -nocompileeditor -unrealexe=<UnrealEditor> -unattended`. This is the same command as "Package a macOS build" in Builds.md. **OK.**
   - Lines 315 to 317 take the staged app, not the archive's. That is **trap 1, handled**. The archive's useless 411 MB app stays in `<run_dir>/archive/`. **CHANGE M5** (delete it).
   - Line 319: `ditto <staged app> <top>/AIMegaJam2026.app` makes a full 1.1 GB copy. **CHANGE M5** (`--clone`).
10. `check_layout()` (line 337): `push/` holds only `NoHumansOnSet_Mac/`, which holds `AIMegaJam2026.app`. **OK.**
11. `strip_build()` (line 322) deletes any `local` or `saved` folder at any depth, so `AIMegaJam2026.app/Contents/UE/AIMegaJam2026/Local/` too. That is **trap 2, handled**. It also deletes `.pdb` files (none on a Mac). Deleting anything inside the `.app` breaks its seal, and nothing signs it again. **CHANGE M6.** Normally nothing is deleted: the deploy worktree has no `Local/` (`prepare_worktree` checks that), and `DefaultGame.ini` stages only `NHOS/Data` as loose files.
12. `secrets_check()` (line 348): `check_build_secrets.py <push> --local <repo>/Local --ue-root <root>` with `Engine/Binaries/Mac/UnrealPak`. **OK on paper.** Open question Q4 lists what only a real build shows.
13. **No `codesign` gate.** **CHANGE M7.**
14. Lines 460 to 463: the version from `git show -s --format=%cI`. **OK.**
15. Lines 467 to 470: `butler push <push> quantumcalzone/no-humans-on-set:mac --userversion <day>-<sha> --if-changed --fix-permissions`. The push holds the folder, not a zip. **Trap 3 is not hit here**, because the script never zips. itch makes the zip that a browser downloads. Whether that zip keeps the signature is step 5 (Q1).
16. Lines 471 to 483: `butler status` reads the channels, **even in a dry run** (see "Step 2"). With `--hidden`, it stops if `mac` exists. Without it, a real push to a missing `mac` stops. **OK.**

### The secrets check: `Tools/check_build_secrets.py`

- `find_unrealpak()` (line 291) finds `Engine/Binaries/Mac/UnrealPak` from `--ue-root`. **OK.**
- `scan_tree()` (line 237) calls `os.walk` without `followlinks`. A symlink to a file is read through the link, and a symlink to a folder is not walked into (its target is inside the bundle anyway). A **broken** symlink gives "could not read" (NOT CHECKED), which ends with exit code 2, and the deploy stops. Q4.
- `forbidden_reason()` (line 216) flags any `.pem`. If the Mac app stages the engine's `cacert.pem` (`Engine/Content/Certificates/ThirdParty/cacert.pem`) as a loose file inside the bundle, the check reports FOUND. The Windows build had none, loose or in the containers, because the Windows check passed. Q4. If it happens, allow exactly that one path in `forbidden_reason()`. That file is not in T92's Touches, so add it there in the same commit.

## The changes T92 should make

### M1: quote the `cd` for sh (`nhos_itch_deploy.py`, line 73)

```python
import shlex
...
        with open(cmd_file, "w") as fh:
            fh.write("#!/bin/sh\ncd " + shlex.quote(project) + "\n"
                     + " ".join(shlex.quote(a) for a in args) + "\n")
```

`shlex.quote` gives the same result as the current hand-made single quotes for the args, and is correct for the `cd` too.

### M2 and M3: the deploy worktree on a Mac (`deploy_itch.py`, line 73; help text, line 393; docstring, line 23; message, line 416)

```python
DEFAULT_DEPLOY = {
    "windows": Path("C:/Users/Personal/Projects/NHOS_deploy"),
    "mac": Path.home() / "Projects" / "NHOS_deploy",   # /Users/personal/Projects/NHOS_deploy, next to the repo folder
}
```

Update the `--deploy` help text ("or on Windows ...") and the docstring's step 1 to name both defaults. Then the menu passes nothing new. See "How the menu finds the deploy worktree" for why `NHOS_DEPLOY` is not enough.

### M4: find leftover processes on a Mac (`deploy_itch.py`, `stop_leftovers`, lines 241 to 251)

Found here with `ps -axo pid=,comm=,args=`: the `comm` column is cut to 16 characters (`/Users/Shared/Ep`), and the engine path has a space in it (`Epic Games`). `line.split(None, 2)` then gives `parts[1] = "/Users/Shared/Ep"` or `"/Users/personal/"`, and its `.name` never equals `UnrealEditor`, `dotnet` and the others. So no leftover is ever stopped. Read the two columns separately, each with unlimited width:

```python
def _mac_processes() -> list[tuple[int, str, str]]:
    """(pid, executable name, full command line) for every process."""
    def column(field: str) -> dict[int, str]:
        out = subprocess.run(["ps", "-axww", "-o", "pid=", "-o", f"{field}="],
                             capture_output=True, text=True).stdout
        rows = {}
        for line in out.splitlines():
            pid, _, rest = line.strip().partition(" ")
            if pid.isdigit():
                rows[int(pid)] = rest.strip()
        return rows
    comm, args = column("comm"), column("args")
    return [(pid, Path(c).name, args.get(pid, "")) for pid, c in comm.items()]
```

In `stop_leftovers`, the `else` branch becomes:

```python
    else:
        out_lines = []
        for pid, name, cmdline in _mac_processes():
            if pid == os.getpid() or name not in LEFTOVER_NAMES_MAC or str(deploy) not in cmdline:
                continue
            out_lines.append(f"stopping leftover {name} {pid}")
            subprocess.run(["kill", "-9", str(pid)], capture_output=True)
        out = "\n".join(out_lines)
```

Checked on this Mac: `ps -axww -o pid= -o comm=` gives the full path (`/Users/Shared/Epic Games/UE_5.8/.../MacOS/UnrealEditor`), and `-o args=` gives the full command line. Also add the compiler's names to `LEFTOVER_NAMES_MAC` (line 85): `"clang++"`, `"ld"`. UnrealBuildTool and AutomationTool run as `dotnet`, which is already in the list. Check this with `ps -axww -o pid= -o comm=` while a package runs.

### M5: the archive's wrong app and the copy (`package_mac`, lines 312 to 319)

```python
    top.mkdir()
    # --clone: an APFS clone, not a second 1.1 GB copy (the deploy worktree and the push folder are on one volume).
    run(["ditto", "--clone", str(staged), str(top / f"{PROJECT}.app")])
    # The archive step's app is only the executable (trap 1); it is never pushed, so free its 411 MB.
    shutil.rmtree(run_dir / "archive", ignore_errors=True)
```

`ditto --clone` is in this Mac's `man ditto` ("Attempt to clone regular files when copying"). A clone holds the same bytes, so the signature is the same. If `ditto --clone` makes the gate fail when a plain `ditto` passes, drop `--clone`.

### M6: sign again only when the bundle changed, and keep the entitlements (`strip_build` and a new `resign_app`)

`strip_build` should say whether it deleted anything inside the `.app`:

```python
def strip_build(top: Path) -> bool:
    """Deletes .pdb files and Local/ or Saved/ folders. Returns True when it changed anything inside a .app."""
    removed = 0
    bundle_changed = False
    for dirpath, dirnames, filenames in os.walk(top, topdown=True):
        in_app = any(p.endswith(".app") for p in Path(dirpath).relative_to(top).parts)
        for d in list(dirnames):
            if d.lower() in ("local", "saved"):
                shutil.rmtree(Path(dirpath) / d)
                dirnames.remove(d)
                bundle_changed |= in_app
                say(f"deleted {Path(dirpath, d).relative_to(top.parent).as_posix()}/")
        for f in filenames:
            if f.lower().endswith(".pdb"):
                (Path(dirpath) / f).unlink()
                removed += 1
                bundle_changed |= in_app
    say(f"deleted {removed} .pdb file(s)")
    return bundle_changed
```

The ad hoc re-sign. A plain `codesign --force --deep --sign -` writes a new signature **with no entitlements**, so the app would lose `com.apple.security.app-sandbox` and run unsandboxed. Its `Local/`, log and save paths would then differ from the build that Builds.md describes. Keep the old signature's metadata, and check that the entitlements are still there:

```python
def entitlements(app: Path) -> str:
    proc = subprocess.run(["codesign", "-d", "--entitlements", "-", "--xml", str(app)],
                          capture_output=True, text=True)
    return proc.stdout.strip()


def resign_app(app: Path) -> None:
    before = entitlements(app)
    run(["codesign", "--force", "--deep", "--sign", "-",
         "--preserve-metadata=identifier,entitlements,requirements,flags,runtime", str(app)])
    after = entitlements(app)
    if before != after:
        raise RuntimeError("the ad hoc re-sign changed the app's entitlements "
                           f"(before {len(before)} bytes, after {len(after)} bytes)")
```

`man codesign` here says that `--preserve-metadata` "is ignored" if the old binary has the linker-signed flag. If UE's own signing step left the main binary linker-signed, the entitlements are lost even with this flag (Q6). The `before != after` test catches that. Then save `before` to a file and sign with `--entitlements <file>` instead.

In `main()`, after `strip_build`:

```python
        changed = strip_build(top)
        if plat == "mac" and changed:
            say("the .app changed, so it is signed again ad hoc")
            resign_app(top / PLATFORMS["mac"]["main"])
```

The same `resign_app` is what Done-when 3 does by hand to the copy after it writes `switches.json` into the bundle.

### M7: the `codesign --verify --deep --strict` gate

```python
def verify_signature(app: Path) -> int:
    proc = run(["codesign", "--verify", "--deep", "--strict", "--verbose=2", str(app)],
               check=False, capture=True)
    print(proc.stdout + proc.stderr, flush=True)   # codesign writes its result to stderr
    return proc.returncode
```

In `main()`, right after the secrets check and before `butler status`:

```python
    code = secrets_check(push_root, local, ue_root)
    if code != 0:
        return fail(f"the secrets check ended with exit code {code}; nothing was pushed")
    say("the secrets check is clean")

    if plat == "mac":
        if verify_signature(top / PLATFORMS["mac"]["main"]) != 0:
            return fail("codesign --verify --deep --strict failed on the app; nothing was pushed")
        say("the app's signature is valid")
```

`top` is set inside the `try` (line 450), so it is defined here. The gate runs in a dry run and with `--build` too, because both reach this point. `codesign` can't check a Mac build on Windows, so the gate is for `plat == "mac"` only. A `--platform mac --build` run on the PC is not a case the script supports anyway.

## Where the gates go, in order

1. Package, then `ditto --clone` the staged app into `push/NoHumansOnSet_Mac/`.
2. `strip_build`. **If it changed the `.app`: `resign_app`**, ad hoc, with the entitlements kept (M6). Only here does the bundle change. Nothing after this point writes into it.
3. **The secrets check** (`--local <repo>/Local`). It comes first, so Done-when 2's planted key stops the run here, as that check expects. Plant the key **outside** the bundle (`push/NoHumansOnSet_Mac/planted.txt`). Then the run stops at the secrets check for the right reason, and the signature has nothing to do with it.
4. **`codesign --verify --deep --strict`** (M7).
5. `butler status`, then the channel guard, then the push (or the dry run's "would push").

If step 5 (Q1) chooses the zip, the zip is made between 4 and 5 with `ditto -c -k --norsrc --noextattr --keepParent` (trap 3). Run the secrets check on the zip too, as Builds.md asks for any zip.

## How the menu finds the deploy worktree, and what the editor's environment sees

- **What the editor's environment sees does not matter.** The menu doesn't start Python itself. It writes `Saved/DeployItch.command` and runs `open -a Terminal` on it. Terminal starts the file in a new login shell (zsh), so `deploy_itch.py` sees the variables from `~/.zprofile` and `~/.zshrc` (and any `launchctl setenv`), and **not** the editor's. A Mac app started from the Dock or the Epic launcher has no shell variables anyway. So setting `NHOS_DEPLOY` for the editor does nothing for the menu.
- **Recommended: a Mac default in `deploy_itch.py` (M3):** `~/Projects/NHOS_deploy`, which is `/Users/personal/Projects/NHOS_deploy`, next to the repo folder as on the PC. The menu works with no setup, and a run by hand needs no `--deploy`.
- Other ways that work, if a different path is wanted: export `NHOS_DEPLOY` in `~/.zprofile` (the Terminal window reads it), or have the menu write `--deploy <path>` into the args. Both are more setup than a default, so use the default.
- **The first run makes the worktree:** `git worktree add --detach /Users/personal/Projects/NHOS_deploy <sha>` from the repo folder, then `git lfs pull` there. It shares the repo folder's `.git/lfs` (3.6 GB). The checkout's LFS files at HEAD are about 2.1 GB, and `lfs pull` copies them into the worktree. T92 doesn't need to make the worktree by hand.

## Step 2: butler on the Mac

- No copy to use: no itch app for this user, and an empty `broth/butler/versions/`.
- **Download, on your OK:** `https://broth.itch.zone/butler/darwin-arm64/LATEST/archive/default`. broth's `LATEST` for `darwin-arm64` is **15.32.0**, the same version as the PC's copy. The zip is **10,041,882 bytes (9.6 MiB)**, read from a 1-byte range request. There is also a `darwin-amd64` channel at 15.32.0. Use arm64.
- **Where to put it, so that the script finds it with no PATH change:** unzip it into `~/Library/Application Support/itch/broth/butler/versions/15.32.0/` and write `15.32.0` to `~/Library/Application Support/itch/broth/butler/.chosen-version`. This is the itch app's layout, and `find_butler()` reads it. Download with `curl` into a new empty folder, and unzip from there. A file that `curl` downloads has no quarantine attribute, so it runs. Check it with `"<that folder>/butler" version` (no sign-in needed).
- **Then you run `butler login`** in Terminal, with the full path to butler. It saves `~/.config/itch/butler_creds`. Do this **before the first dry run**: `deploy_itch.py` runs `butler status` in a dry run as soon as it finds butler, and with no sign-in that starts butler's browser login by itself (T89, part 1). Or install butler only after the first dry run.

## Step 5: which push keeps the signature

From butler's pages (read on 2026-11-19: `pushing.html`, `installing.html`, the itch app's `platforms/macos.html`):

- butler keeps symlinks as symlinks by default (`--dereference` turns that off). The itch app's macOS page says butler "handles symlinks" and fixes permissions on upload.
- **A zip gets unzipped.** butler's pushing page says the push target "can also be a .zip file". Its auto-unzip appendix says that a pushed folder that holds one `.zip` and nothing else is unpacked, and its contents are pushed. This is on by default, and `--no-auto-unzip` turns it off. So "push the ditto zip" uploads the **same files** as "push the folder", unless you add `--no-auto-unzip`. Then the build is one file, a zip.
- The pages say "just push your .app bundle". They say nothing about code signatures, or about the zip that itch makes for a browser download.

So the real choice is between these two:

- **A. The folder, as the script pushes it now** (`--fix-permissions`). itch makes the download zip from the build. The itch app can also install and launch it. Recommended, **if** the downloaded zip keeps symlinks, exec bits and the signature.
- **B. A folder that holds only the `ditto -c -k --norsrc --noextattr --keepParent` zip, pushed with `--no-auto-unzip`.** The build is the zip itself. What a browser then gets is unknown (Q2): the zip as it is, or a zip around the zip. The itch app would get a zip, not an app.

How to test it (it needs real pushes, so it comes after the hidden first push):

1. Push A hidden (that is step 6's first push).
2. Download the file in a browser, signed in, if the owner can download a hidden file (Q3). Otherwise do it after you show the file. Unzip it with Archive Utility (double-click), then check:
   - `codesign --verify --deep --strict --verbose=2 <app>`.
   - `find <app> -type l | wc -l`, the same count as in the pushed build.
   - `ls -l <app>/Contents/MacOS/`: the exec bit is set.
   - `xattr -lr <app> | grep -v quarantine | head`: no detritus that `--strict` would object to.
   - `codesign -d --entitlements - --xml <app>`: still has `app-sandbox`.
3. If A fails, push B to the same channel. `mac` exists then, so no `--hidden`, but the file is still hidden until you show it. Check the same things on what the browser saves.
4. Write down which one kept the signature, and why, in T92's findings and in Builds.md.

## What T91 changes under T92

T91 runs on the PC first and edits the same two files. Pull before T92 starts, and re-read these parts:

- **`deploy_itch.py`:** `BRANCH`, the `--commit` default (`origin/main`), the `git fetch origin <branch>` in `prepare_worktree`, the `args.commit != f"origin/{BRANCH}"` test in the `--build` branch of `main()`, and the docstring. T92's changes (`DEFAULT_DEPLOY`, `stop_leftovers`, `package_mac`, `strip_build`, the new `resign_app` and `verify_signature`, and the gate in `main()`) are in other functions. The one shared spot is `main()`, near the push. Re-read it after T91 before you add the gate.
- **`nhos_itch_deploy.py`:** the upload dialog's text (`main`'s tip) and a new entry such as "Dry run of dev", which passes `--commit origin/dev --dry-run`. On the Mac, every entry goes through `launch()` and the `.command` file, so check the new entry there too. The startup line's "3 entries" will change. The Mac launch code (M1) is in `launch()`. If T91 changes `launch()`'s signature (for example, an `extra_args` parameter), apply M1 to the new code.
- **`Docs/Builds.md` "Deploys to itch.io" and CLAUDE.md's short section:** T91 rewrites them for `main`. T92's doc edits go on top of T91's text.
- **What a dry run builds:** after T91, "Build only (dry run)" builds `main`'s tip, which is the first release after T91's step 7. Done-when 1 still passes with "Dry run of dev". Say in the findings which one ran.

## The checks for "Done when", in order

Before you start:

- **Free disk to 30 GiB or more** (see "Disk"). Not done by Claude: deleting the person's files is the person's call.
- **Your OK to download butler** (above), then **your `butler login`**.
- **The editor.** "Build only (dry run)" runs from the menu, so the editor stays open. It packages in the deploy worktree, which is a separate folder, so the repo folder's open editor is not in the way. T89 did the same on the PC. The session drives the editor only for the menu click, with `Editor: driving` in its status file. The first run, by hand, can run with the editor closed, to keep the first cook fast. It is your call whether to close it.

Then:

1. **The first dry run by hand.** `"/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/ThirdParty/Python3/Mac/bin/python3" Tools/deploy_itch.py --dry-run --ue-root "/Users/Shared/Epic Games/UE_5.8"` (with M1 to M7 made). Run it in the background, because the first package takes 10 minutes or more. Fix what breaks. Expect: `push/NoHumansOnSet_Mac/AIMegaJam2026.app`, the gate's "valid on disk / satisfies its Designated Requirement", and the secrets check's "RESULT: clean" with exit code 0. Needs: nothing from you, once butler is signed in (or not yet installed).
2. **Done-when 1, from the menu.** Tools > itch.io > "Build only (dry run)" in the Mac editor. Terminal opens and runs it, the log lands in `Saved/Logs/DeployItch.log`, and the same three results show. Needs: the editor (one session driving), butler signed in. The click may need screen access, which the person declined in T89. If so, run `nhos_itch_deploy.launch(dry_run=True)` through Unreal MCP's Python. That runs the same code with no click. Say which one ran.
3. **Done-when 2, a planted key.** `ditto --clone <push> <scratch>/copy/push`, then write a fake `sk-ant-` plus 48 letters to `copy/push/NoHumansOnSet_Mac/planted.txt` (outside the `.app`). Run `deploy_itch.py --build <scratch>/copy/push --dry-run`. Expect: FOUND, "STOP: the secrets check ended with exit code 1; nothing was pushed", exit code 1. Delete the copy. Needs: nothing from you.
4. **Step 6, the hidden first push.** `deploy_itch.py --build <the dry run's push> --commit <its sha> --hidden`, as the PC did in T89. Then `butler status` lists `mac` about a minute later. Needs: butler signed in. Your OK is not needed for a hidden push, which T92's steps already call for.
5. **Step 5's test** (above). Needs: a browser download. Signed in as you if hidden files can be downloaded (Q3), or after step 6.
6. **Done-when 3: show the file, on your OK.** Untick "Hide this file" on the edit page and save. You do that, or Claude does it in your Chrome on your word, as in T89. A signed-out visitor sees `no-humans-on-set-mac.zip`. Download it, unzip it with Archive Utility, and run `codesign --verify --deep --strict`. Then the autoplay show:
   - Make a copy of the app.
   - Write `{"analytics": "off", "mode": "free", "autoplay": true}` to the copy's `Contents/UE/AIMegaJam2026/Local/switches.json`.
   - Sign the copy again with the M6 command, `--preserve-metadata` included, and check its entitlements.
   - Open it once. **You click Open Anyway** in System Settings > Privacy & Security. Claude doesn't change security settings.
   - Read `~/Library/Containers/com.YourCompany.AIMegaJam2026/Data/Library/Logs/AIMegaJam2026/AIMegaJam2026.log` for `NHOS: ANALYTICS off` and `NHOS: SHOW END`.
   - Delete the copy and the download.
   Needs: your OK to show the file, and your click on Open Anyway.
7. **Done-when 4, the jam's file.** T89 found that the page has no jam file: its only upload is the `windows` channel's. So check that `butler status` shows the `windows` channel's build and version as before the push, and that the edit page lists only `windows` and `mac`. Needs: nothing, or your eyes on the edit page.
8. **Done-when 5, no key.** `git diff --cached` of T92's commit holds no key (`python3 Tools/check_build_secrets.py --sources` for the sources). Nothing from `Local/` or `butler_creds` is printed or committed.
9. **Step 7, the docs** (below), then the commit.

## Disk

20 GiB free now. A rough count for the first run, from this Mac's numbers:

| Item | Estimate |
|---|---|
| Deploy worktree checkout (LFS files 2.1 GB, plus the rest) | about 2.5 GB |
| `Intermediate/` (the game program's compile), `Saved/Cooked/` | about 2 to 3 GB |
| `Saved/StagedBuilds/Mac/AIMegaJam2026.app` | 1.1 GB |
| The archive's app (deleted with M5) | 0.4 GB while it runs |
| The push copy | 1.1 GB, or almost 0 with `ditto --clone` |
| Shared DDC growth | up to 1 to 2 GB |
| The secrets check's extraction in the temp folder (one container at a time) | up to about 1 GB while it runs |
| Step 5 and Done-when 3: download zip, unzipped app, test copy, planted-key copy | about 3 to 4 GB, deleted afterwards |

That is about 10 to 14 GiB, with almost nothing to spare on 20 GiB. The cook also fails badly when the disk fills. Free enough to have 30 GiB or more before step 1.

## Docs (step 7)

- `Docs/Builds.md`, "Package a macOS build": the menu works on the Mac. The deploy worktree is `~/Projects/NHOS_deploy`. Use `python3` or the engine's Python (`python` isn't on PATH on this Mac). The `codesign` gate. Sign again with `--preserve-metadata=...entitlements...`, never a plain `--sign -`, because that drops the sandbox. The editor's log on a Mac is `~/Library/Logs/Unreal Engine/AIMegaJam2026Editor/AIMegaJam2026.log`.
- `Docs/Builds.md`, "Deploys to itch.io": both default deploy worktrees. butler's place on the Mac (the broth layout). The result of step 5.
- CLAUDE.md's short "Deploys to itch.io", `README.md`, and `Docs/ItchPage.md`'s Uploads row (`no-humans-on-set-mac.zip`).
- Outside T92's Touches, so give it to the person as a follow-up: CLAUDE.md's "Editor log ... `Saved/Logs/AIMegaJam2026.log`" line is true only on Windows.

## Open questions only a real run can answer

- **Q1 (step 5):** does the zip that itch makes for a browser download keep the symlinks, the exec bits and the signature after Archive Utility unzips it? That decides A or B.
- **Q2:** with B (`--no-auto-unzip` and one zip in the build), what does a browser get: the ditto zip as it is, or a zip around it? And does Archive Utility's result pass `codesign --verify --deep --strict`?
- **Q3:** can the owner download a hidden file in a browser before showing it? If not, the signature test comes after you show the file. Then a bad first file could be public for a few minutes. To avoid that, test on another channel first, such as a hidden `mac-test`, and delete it afterwards on your OK.
- **Q4:** what is in the staged app?
  - Symlinks, and are any broken? A broken one makes the secrets check exit 2.
  - A `.dSYM`?
  - A loose `cacert.pem` (flagged FOUND)? Anything else in `forbidden_reason()`?
  - Do the Mac `.utoc` containers open with the Mac UnrealPak, and does the BPC_LLMClient canary read back?
- **Q5:** does the staged app pass `codesign --verify --deep --strict` straight out of staging, before anything touches it? If it doesn't, sign it every time (M6 with `changed` forced true), and find out why.
- **Q6:** does the re-sign with `--preserve-metadata` keep the entitlements, or is the main binary linker-signed, so that the flag is ignored? Check with `codesign -d --entitlements - --xml` before and after.
- **Q7:** the Terminal launch from the editor. Does `open -a Terminal` on the `.command` run without a prompt, and does the window stay open at the end to show the result?
- **Q8:** how long the first Mac package takes, and how much disk it really uses.
- **Q9:** does the itch app (for a player who uses it) find and launch `NoHumansOnSet_Mac/AIMegaJam2026.app`, one folder below the build's root? The browser download is the one that matters for the Done-when, so check it only if there is time.
- **Q10:** does git-lfs 3.0.2 (amd64, under Rosetta) pull into the new worktree with the shared `.git/lfs`? Expected yes. If not, update git-lfs.
- **Q11:** can the sandboxed app write `Local/progress.json` inside the bundle? Builds.md lists this as untested, and a signed bundle makes it more likely to fail. It is not T92's to fix. Note what the Done-when 3 run shows.
