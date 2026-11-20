#!/usr/bin/env python3
"""Package the last release (main's tip) and push it to the game's itch.io page with butler.

Usage (Python 3.10+, no packages needed). It packages for the machine it runs on: a Windows build
on Windows, a Mac build on a Mac.

    python Tools/deploy_itch.py --dry-run                 # package origin/main, check it, push nothing
    python Tools/deploy_itch.py                           # the same, then push it
    python Tools/deploy_itch.py --commit origin/dev --dry-run   # try dev's tip before a release
    python Tools/deploy_itch.py --commit <sha>            # a given commit (a real push of anything
                                                          # but main's tip ships an unreleased build)
    python Tools/deploy_itch.py --hidden                  # the first push to a channel: makes it, hidden
    python Tools/deploy_itch.py --build <folder> --dry-run   # check (and push) a build already made

main is the production branch: it holds the last release, and a release is a merge of dev into
main on the person's word (see "Releases" in CLAUDE.md). So what goes up by default is always a
release. In the editor, Tools > itch.io runs this script (Content/Python/nhos_itch_deploy.py). See
"Deploys to itch.io" in Docs/Builds.md.

| Platform | Channel | Folder inside the download   | Built with                         |
|----------|---------|------------------------------|------------------------------------|
| Windows  | windows | NoHumansOnSet_Windows/       | RunUAT.bat (VS 2022, Win 11 SDK)   |
| Mac      | mac     | NoHumansOnSet_Mac/ (the .app)| RunUAT.sh (Xcode)                  |

What it does, in order:

1. Moves the deploy worktree (--deploy or NHOS_DEPLOY; on the PC by default
   C:/Users/Personal/Projects/NHOS_deploy), a detached git worktree of the repo folder, to the
   commit: git fetch (main and dev), git checkout --detach, git lfs pull. It never builds in the repo folder,
   where sessions have uncommitted work. The worktree shares the repo folder's .git/lfs, so a run
   downloads only new LFS objects.
2. Packages it with the "Package a Windows build" or "Package a macOS build" command from
   Docs/Builds.md, into <deploy worktree>/Packaged/deploy/<short sha>/. On Windows the command goes in
   a .bat run with cmd /c. On a Mac it takes the staged app from Saved/StagedBuilds/Mac/ (the
   archive step copies only the executable) and copies it with ditto.
3. Puts the build in NoHumansOnSet_<Windows|Mac>/ and deletes every .pdb and any Local/ or Saved/
   folder in it (in the Mac app, Contents/UE/AIMegaJam2026/Local/).
4. Runs Tools/check_build_secrets.py on it with --local <repo folder>/Local (the deploy worktree
   has no Local/, and nothing is ever copied out of it). Anything but exit code 0 stops the run,
   and so does a check that found no key files to look for.
5. Reads the page's channels back with butler status. A channel that isn't on the page yet would
   become a new file, visible at once, so only a push with --hidden may make one; the editor's
   menu never does. butler pushes only to its own channels, so it can't touch a file that went up
   through the web form (the jam's file). Then it pushes:
   butler push <build> quantumcalzone/no-humans-on-set:<channel>
       --userversion <commit date>-<short sha> --if-changed

butler signs in with the butler_creds file that `butler login` saved (or BUTLER_API_KEY, when that
variable is set). This script never reads or prints a key.

Exit code: 0 pushed (or, with --dry-run, ready to push), 1 failed or stopped.
"""

from __future__ import annotations

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = "AIMegaJam2026"
RELEASE_BRANCH = "main"  # the production branch: the last release, built by default
WORK_BRANCH = "dev"  # where all work happens; fetched too, so --commit origin/dev is up to date
DEFAULT_COMMIT = f"origin/{RELEASE_BRANCH}"
GAME = "quantumcalzone/no-humans-on-set"

PLATFORMS = {
    "windows": {"channel": "windows", "folder": "NoHumansOnSet_Windows", "main": f"{PROJECT}.exe"},
    "mac": {"channel": "mac", "folder": "NoHumansOnSet_Mac", "main": f"{PROJECT}.app"},
}

DEFAULT_DEPLOY = {"windows": Path("C:/Users/Personal/Projects/NHOS_deploy")}
UE_ROOTS = {
    "windows": [Path("C:/Program Files/Epic Games/UE_5.8")],
    "mac": [Path("/Users/Shared/Epic Games/UE_5.8")],
}

# Processes a cancelled run can leave behind in the deploy worktree. They hold files open there,
# so the next run's checkout would fail. Only ones whose command line names the worktree are
# stopped.
LEFTOVER_NAMES = ["UnrealEditor-Cmd.exe", "UnrealEditor.exe", "UnrealPak.exe", "UnrealBuildTool.exe",
                  "AutomationTool.exe", "ShaderCompileWorker.exe", "dotnet.exe", "cmd.exe",
                  "cl.exe", "link.exe"]
LEFTOVER_NAMES_MAC = ["UnrealEditor", "UnrealPak", "dotnet", "ShaderCompileWorker", "xcodebuild", "clang"]


def say(text: str) -> None:
    print(f"[deploy] {text}", flush=True)


def fail(text: str) -> int:
    print(f"[deploy] STOP: {text}", flush=True)
    return 1


def run(cmd: list[str], cwd: Path | None = None, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    shown = " ".join(f'"{c}"' if " " in c else c for c in cmd)
    say(f"$ {shown}")
    if capture:
        proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    else:
        # Streamed through print, so --log gets the packager's and butler's output too.
        with subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, errors="replace") as child:
            for line in child.stdout:
                print(line, end="", flush=True)
        proc = subprocess.CompletedProcess(cmd, child.returncode)
    if check and proc.returncode != 0:
        if capture:
            print(proc.stdout + proc.stderr, flush=True)
        raise RuntimeError(f"{cmd[0]} ended with exit code {proc.returncode}")
    return proc


def git(*args: str, cwd: Path, capture: bool = True) -> str:
    proc = run(["git", *args], cwd=cwd, capture=capture)
    return proc.stdout.strip() if capture else ""


class _Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, text):
        for s in self.streams:
            s.write(text)
            s.flush()

    def flush(self):
        for s in self.streams:
            s.flush()


def tee_to(log: Path) -> None:
    """Copies this run's own output to the log (child processes' output goes through print below)."""
    log.parent.mkdir(parents=True, exist_ok=True)
    fh = log.open("w", encoding="utf-8")
    sys.stdout = _Tee(sys.__stdout__, fh)
    sys.stderr = _Tee(sys.__stderr__, fh)


def take_lock(deploy: Path):
    """One run at a time per deploy worktree: a second click while a build runs stops at once."""
    lock = deploy.parent / (deploy.name + ".lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        try:
            pid = int(lock.read_text().strip() or 0)
        except (OSError, ValueError):
            pid = 0
        if pid and _alive(pid):
            raise RuntimeError(f"another deploy is running (process {pid}); wait for it to finish")
        lock.unlink(missing_ok=True)  # left by a run that was closed
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(fd, str(os.getpid()).encode())
    os.close(fd)
    import atexit
    atexit.register(lambda: lock.unlink(missing_ok=True))


def _alive(pid: int) -> bool:
    if os.name == "nt":
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def this_platform() -> str | None:
    system = platform.system()
    return {"Windows": "windows", "Darwin": "mac"}.get(system)


# ---------------------------------------------------------------- finding things

def find_repo(arg: str | None) -> Path:
    """The repo folder: --repo, NHOS_REPO, or the main worktree of the checkout this script is in."""
    if arg:
        return Path(arg).resolve()
    if os.environ.get("NHOS_REPO"):
        return Path(os.environ["NHOS_REPO"]).resolve()
    common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                            cwd=HERE, capture_output=True, text=True).stdout.strip()
    return Path(common).parent.resolve()


def find_ue_root(arg: str | None, plat: str) -> Path | None:
    roots = []
    if arg:
        roots.append(Path(arg))
    if os.environ.get("UE_ROOT"):
        roots.append(Path(os.environ["UE_ROOT"]))
    roots += UE_ROOTS[plat]
    script = "RunUAT.bat" if plat == "windows" else "RunUAT.sh"
    for r in roots:
        if (r / "Engine/Build/BatchFiles" / script).is_file():
            return r
    return None


def find_butler(arg: str | None) -> Path | None:
    """--butler, BUTLER, butler on PATH, or the copy the itch app keeps in its broth folder."""
    if arg:
        return Path(arg) if Path(arg).is_file() else None
    if os.environ.get("BUTLER") and Path(os.environ["BUTLER"]).is_file():
        return Path(os.environ["BUTLER"])
    on_path = shutil.which("butler")
    if on_path:
        return Path(on_path)
    if os.name == "nt":
        broth, exe_name = Path(os.environ.get("APPDATA", "")) / "itch/broth/butler", "butler.exe"
    else:
        broth, exe_name = Path.home() / "Library/Application Support/itch/broth/butler", "butler"
    chosen = broth / ".chosen-version"
    if chosen.is_file():
        exe = broth / "versions" / chosen.read_text().strip() / exe_name
        if exe.is_file():
            return exe
    return None


# ---------------------------------------------------------------- the deploy worktree

def stop_leftovers(deploy: Path) -> None:
    if os.name == "nt":
        names = ",".join(f"'{n}'" for n in LEFTOVER_NAMES)
        path = str(deploy).replace("/", "\\").replace("'", "''")
        ps = ("$p = '" + path + "'; $me = " + str(os.getpid()) + "; "
              "Get-CimInstance Win32_Process | Where-Object { @(" + names + ") -contains $_.Name -and "
              "$_.ProcessId -ne $me -and $_.CommandLine -and "
              "($_.CommandLine.Replace('/', '\\')).IndexOf($p, [StringComparison]::OrdinalIgnoreCase) -ge 0 } | "
              "ForEach-Object { Write-Output (\"stopping leftover \" + $_.Name + \" \" + $_.ProcessId); "
              "Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }")
        out = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                             capture_output=True, text=True).stdout.strip()
    else:
        out_lines = []
        ps = subprocess.run(["ps", "-axo", "pid=,comm=,args="], capture_output=True, text=True).stdout
        for line in ps.splitlines():
            parts = line.split(None, 2)
            if len(parts) < 3 or int(parts[0]) == os.getpid():
                continue
            if Path(parts[1]).name in LEFTOVER_NAMES_MAC and str(deploy) in parts[2]:
                out_lines.append(f"stopping leftover {Path(parts[1]).name} {parts[0]}")
                subprocess.run(["kill", "-9", parts[0]], capture_output=True)
        out = "\n".join(out_lines)
    for line in out.splitlines():
        say(line)
    if out:
        time.sleep(3)


def prepare_worktree(repo: Path, deploy: Path, commit: str) -> str:
    """Moves the deploy worktree to the commit and returns the full sha."""
    git("fetch", "origin", RELEASE_BRANCH, WORK_BRANCH, cwd=repo, capture=False)
    sha = git("rev-parse", "--verify", f"{commit}^{{commit}}", cwd=repo)
    if not (deploy / ".git").exists():
        if deploy.exists() and any(deploy.iterdir()):
            raise RuntimeError(f"{deploy} exists and is not a git worktree; move it away first")
        say(f"making the deploy worktree {deploy}")
        git("worktree", "add", "--detach", str(deploy), sha, cwd=repo, capture=False)
    else:
        stop_leftovers(deploy)
        # Tracked changes and untracked files that git doesn't ignore go; the engine's ignored
        # folders (DerivedDataCache, Intermediate, Saved) stay, so the next cook is faster.
        git("reset", "--hard", "--quiet", cwd=deploy, capture=False)
        git("clean", "-fdq", cwd=deploy, capture=False)
        git("checkout", "--detach", "--force", "--quiet", sha, cwd=deploy, capture=False)
    git("lfs", "pull", cwd=deploy, capture=False)
    head = git("rev-parse", "HEAD", cwd=deploy)
    if head != sha:
        raise RuntimeError(f"the deploy worktree is at {head}, not {sha}")
    if git("status", "--porcelain", "--untracked-files=no", cwd=deploy):
        raise RuntimeError("the deploy worktree has changes after the checkout")
    if (deploy / "Local").exists():
        raise RuntimeError(f"{deploy / 'Local'} exists; the deploy worktree must have no Local/ folder")
    return sha


def package_windows(deploy: Path, ue_root: Path, run_dir: Path, top: Path) -> None:
    uproject = deploy / f"{PROJECT}.uproject"
    runuat = ue_root / "Engine/Build/BatchFiles/RunUAT.bat"
    cmdexe = ue_root / "Engine/Binaries/Win64/UnrealEditor-Cmd.exe"
    win = lambda p: str(p).replace("/", "\\")
    archive = run_dir / "archive"
    bat = run_dir / "package.bat"
    bat.write_text(
        "@echo off\r\n"
        f'call "{win(runuat)}" BuildCookRun -project="{win(uproject)}" -platform=Win64 '
        f"-clientconfig=Development -build -cook -stage -pak -archive "
        f'-archivedirectory="{win(archive)}" -nocompileeditor -unrealexe="{win(cmdexe)}" -unattended\r\n'
        "exit /b %ERRORLEVEL%\r\n", encoding="ascii")
    run(["cmd", "/c", win(bat)], cwd=deploy)
    built = archive / "Windows"
    if not (built / f"{PROJECT}.exe").is_file():
        raise RuntimeError(f"the package step ended but {built / (PROJECT + '.exe')} is missing")
    built.rename(top)


def package_mac(deploy: Path, ue_root: Path, run_dir: Path, top: Path) -> None:
    uproject = deploy / f"{PROJECT}.uproject"
    runuat = ue_root / "Engine/Build/BatchFiles/RunUAT.sh"
    editor = ue_root / "Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"
    staged = deploy / "Saved/StagedBuilds/Mac" / f"{PROJECT}.app"
    if staged.exists():
        shutil.rmtree(staged)
    run([str(runuat), "BuildCookRun", f"-project={uproject}", "-platform=Mac", "-clientconfig=Development",
         "-build", "-cook", "-stage", "-pak", "-archive", f"-archivedirectory={run_dir / 'archive'}",
         "-nocompileeditor", f"-unrealexe={editor}", "-unattended"], cwd=deploy)
    # The archive step copies only the executable; the playable app is the staged one.
    if not (staged / "Contents").is_dir():
        raise RuntimeError(f"the package step ended but {staged} is missing")
    top.mkdir()
    run(["ditto", str(staged), str(top / f"{PROJECT}.app")])


def strip_build(top: Path) -> None:
    removed = 0
    for dirpath, dirnames, filenames in os.walk(top, topdown=True):
        for d in list(dirnames):
            if d.lower() in ("local", "saved"):
                shutil.rmtree(Path(dirpath) / d)
                dirnames.remove(d)
                say(f"deleted {Path(dirpath, d).relative_to(top.parent).as_posix()}/")
        for f in filenames:
            if f.lower().endswith(".pdb"):
                (Path(dirpath) / f).unlink()
                removed += 1
    say(f"deleted {removed} .pdb file(s)")


def check_layout(push_root: Path, plat: str) -> Path:
    folder, main = PLATFORMS[plat]["folder"], PLATFORMS[plat]["main"]
    entries = sorted(p.name for p in push_root.iterdir())
    if entries != [folder]:
        raise RuntimeError(f"{push_root} must hold only {folder}/, but holds: {', '.join(entries) or 'nothing'}")
    top = push_root / folder
    if not (top / main).exists():
        raise RuntimeError(f"{top} has no {main}")
    return top


def secrets_check(push_root: Path, local: Path, ue_root: Path | None) -> int:
    cmd = [sys.executable, str(HERE / "check_build_secrets.py"), str(push_root), "--local", str(local)]
    if ue_root:
        cmd += ["--ue-root", str(ue_root)]
    say("$ " + " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    print(out, flush=True)
    if "No Local/*.json key files" in out:
        say("the check found no key files to look for, so it only looked for key shapes")
        return 1
    return proc.returncode


# ---------------------------------------------------------------- butler

def channels(butler: Path) -> dict[str, str] | None:
    """Reads the page's channels back. Returns {channel: line} or None when butler can't read them."""
    proc = subprocess.run([str(butler), "status", GAME], capture_output=True, text=True,
                          stdin=subprocess.DEVNULL, timeout=120)
    out = proc.stdout + proc.stderr
    if proc.returncode != 0:
        print(out, flush=True)
        return None
    found = {}
    for line in out.splitlines():
        m = re.match(r"\s*\|\s*([A-Za-z0-9._-]+)\s*\|", line)
        if m and m.group(1).upper() != "CHANNEL":
            found[m.group(1)] = line.strip()
    if not found and "No channel" not in out:
        print(out, flush=True)
        return None
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--commit", default=DEFAULT_COMMIT,
                    help=f"the commit to build (default: {DEFAULT_COMMIT}, the last release; "
                         f"origin/{WORK_BRANCH} with --dry-run tries the next one)")
    ap.add_argument("--build", help="a push root that already holds a NoHumansOnSet_<Windows|Mac>/ build: "
                                    "skip the checkout and the packaging")
    ap.add_argument("--platform", choices=sorted(PLATFORMS),
                    help="windows or mac (default: this machine's; another one works only with --build)")
    ap.add_argument("--dry-run", action="store_true", help="do everything but the push")
    ap.add_argument("--hidden", action="store_true", help="push to a new channel as hidden (the first push only)")
    ap.add_argument("--repo", help="the repo folder (default: NHOS_REPO, or the main worktree of this checkout)")
    ap.add_argument("--deploy", help="the deploy worktree (default: NHOS_DEPLOY, or on Windows "
                                     f"{DEFAULT_DEPLOY['windows']})")
    ap.add_argument("--ue-root", help="the engine folder (default: UE_ROOT, or the launcher's UE_5.8)")
    ap.add_argument("--butler", help="butler (default: BUTLER, PATH, or the itch app's copy)")
    ap.add_argument("--log", help="also write everything this run prints to this file")
    args = ap.parse_args()
    if args.log:
        tee_to(Path(args.log))

    here = this_platform()
    plat = args.platform or here
    if plat is None:
        return fail("this machine is neither Windows nor a Mac; pass --platform with --build")
    if plat != here and not args.build:
        return fail(f"a {plat} build is packaged only on that platform (this machine: {here})")
    channel, folder = PLATFORMS[plat]["channel"], PLATFORMS[plat]["folder"]

    repo = find_repo(args.repo)
    local = repo / "Local"
    if not local.is_dir():
        return fail(f"{local} is missing: the secrets check needs our keys from the repo folder's Local/")
    deploy_arg = args.deploy or os.environ.get("NHOS_DEPLOY") or DEFAULT_DEPLOY.get(plat)
    if not deploy_arg and not args.build:
        return fail("no deploy worktree: pass --deploy or set NHOS_DEPLOY")
    ue_root = find_ue_root(args.ue_root, here or plat)
    butler = find_butler(args.butler)
    if butler is None and not args.dry_run:
        return fail("butler not found (pass --butler or put it on PATH)")
    say(f"repo folder {repo}, platform {plat}, channel {channel}")

    try:
        if args.build:
            push_root = Path(args.build).resolve()
            sha = None
            if args.commit != DEFAULT_COMMIT:
                sha = git("rev-parse", "--verify", f"{args.commit}^{{commit}}", cwd=repo)
        else:
            deploy = Path(deploy_arg).resolve()
            if deploy == repo or repo in deploy.parents:
                return fail(f"the deploy worktree {deploy} must be outside the repo folder {repo}")
            if ue_root is None:
                return fail("the engine was not found (pass --ue-root or set UE_ROOT)")
            take_lock(deploy)
            sha = prepare_worktree(repo, deploy, args.commit)
            release = git("rev-parse", "--verify", f"{DEFAULT_COMMIT}^{{commit}}", cwd=repo)
            say(f"building {sha[:7]} in {deploy}"
                + (" (main's tip, the last release)" if sha == release
                   else f" (not main's tip {release[:7]}: not a release)"))
            deploy_dir = deploy / "Packaged" / "deploy"
            # Only the newest run's build is kept.
            if deploy_dir.is_dir():
                for old in deploy_dir.iterdir():
                    shutil.rmtree(old) if old.is_dir() else old.unlink()
            run_dir = deploy_dir / sha[:7]
            push_root = run_dir / "push"
            push_root.mkdir(parents=True)
            if plat == "windows":
                package_windows(deploy, ue_root, run_dir, push_root / folder)
            else:
                package_mac(deploy, ue_root, run_dir, push_root / folder)
        top = check_layout(push_root, plat)
        strip_build(top)
    except (RuntimeError, OSError, subprocess.SubprocessError) as e:
        return fail(str(e))

    code = secrets_check(push_root, local, ue_root)
    if code != 0:
        return fail(f"the secrets check ended with exit code {code}; nothing was pushed")
    say("the secrets check is clean")

    if sha:
        when = git("show", "-s", "--format=%cI", sha, cwd=repo)
        day = datetime.fromisoformat(when).astimezone(timezone.utc).strftime("%Y-%m-%d")
        version = f"{day}-{sha[:7]}"
    else:
        version = f"{datetime.now(timezone.utc):%Y-%m-%d}-manual"

    cmd = [str(butler) if butler else "butler", "push", str(push_root), f"{GAME}:{channel}",
           "--userversion", version, "--if-changed"]
    if plat == "mac":
        cmd.append("--fix-permissions")
    if butler:
        found = channels(butler)
        if found is None:
            return fail("butler could not read the page's channels back")
        say(f"channels on the page: {', '.join(found) or 'none'}")
        if args.hidden and channel in found:
            return fail(f"--hidden works only on a new channel, and {channel} exists")
        # A push to a channel that doesn't exist yet makes a new file on the page, visible at once.
        # Only the hidden first push by hand may do that; the editor's menu never does.
        if not args.hidden and channel not in found:
            if not args.dry_run:
                return fail(f"{channel} is not on the page yet: make the first push by hand with --hidden")
            say(f"note: {channel} is not on the page yet, so a real push would stop here (use --hidden)")
    if args.hidden:
        cmd.append("--hidden")
    if sha and not args.dry_run:
        release = git("rev-parse", "--verify", f"{DEFAULT_COMMIT}^{{commit}}", cwd=repo)
        if sha != release:
            say(f"note: {sha[:7]} is not main's tip ({release[:7]}), so this push ships a build that "
                "is not a release; it was asked for with --commit")
    if args.dry_run:
        say("dry run: would push with " + " ".join(cmd))
        say(f"the build is in {push_root}")
        return 0
    try:
        run(cmd, capture=False)
    except RuntimeError as e:
        return fail(str(e))
    say(f"pushed {version} to {GAME}:{channel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
