#!/usr/bin/env python3
"""Package a commit of noHumansOnSet and push it to the itch.io page as the post-jam Windows file.

Usage (Python 3.10+, no packages needed; Windows only, since it packages a Windows build):

    python Tools/deploy_itch.py --dry-run                 # package origin/noHumansOnSet, check it, push nothing
    python Tools/deploy_itch.py                           # the same, then push it
    python Tools/deploy_itch.py --commit <sha>            # a given commit (the workflow passes its own)
    python Tools/deploy_itch.py --hidden                  # the first push only: a new channel, hidden
    python Tools/deploy_itch.py --build <folder> --dry-run   # check (and push) a build already made

The GitHub Actions workflow .github/workflows/itch-windows.yml runs this on each push that changes
the game. See "Deploys to itch.io" in CLAUDE.md.

What it does, in order:

1. Moves the deploy worktree (default C:/Users/Personal/Projects/NHOS_deploy, a detached git
   worktree of the repo folder) to the commit: git fetch, git checkout --detach, git lfs pull.
   It never builds in the repo folder, where sessions have uncommitted work. The worktree shares
   the repo folder's .git/lfs, so a run downloads only new LFS objects.
2. Packages it with the "Package a Windows build" command from CLAUDE.md, written to a .bat and
   run with cmd /c, into <deploy worktree>/Packaged/deploy/<short sha>/.
3. Renames the build's Windows/ folder to NoHumansOnSet_PostJam_Windows, so the folder inside the
   download says post-jam too, and deletes every .pdb and any Local/ or Saved/ folder in it.
4. Runs Tools/check_build_secrets.py on it with --local <repo folder>/Local (the deploy worktree
   has no Local/, and nothing is ever copied out of it). Anything but exit code 0 stops the run,
   and so does a check that found no key files to look for.
5. Reads the page's channels back with butler status, checks the channel is windows-postjam (never
   the jam's file, which went up through the web form and has no channel), and pushes:
   butler push <build> quantumcalzone/no-humans-on-set:windows-postjam
       --userversion postjam-<commit date>-<short sha> --if-changed

butler signs in with BUTLER_API_KEY when that variable is set (the workflow's Actions secret), or
else with the butler_creds file that `butler login` saved. This script never reads or prints a key.

Exit code: 0 pushed (or, with --dry-run, ready to push), 1 failed or stopped.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = "AIMegaJam2026"
BRANCH = "noHumansOnSet"

GAME = "quantumcalzone/no-humans-on-set"
CHANNEL = "windows-postjam"
TOP_FOLDER = "NoHumansOnSet_PostJam_Windows"

DEFAULT_DEPLOY = Path("C:/Users/Personal/Projects/NHOS_deploy")
UE_ROOTS = [Path("C:/Program Files/Epic Games/UE_5.8")]

# Processes a cancelled run can leave behind in the deploy worktree. They hold files open there,
# so the next run's checkout would fail. Only ones whose command line names the worktree are
# stopped.
LEFTOVER_NAMES = ["UnrealEditor-Cmd.exe", "UnrealEditor.exe", "UnrealPak.exe", "UnrealBuildTool.exe",
                  "AutomationTool.exe", "ShaderCompileWorker.exe", "dotnet.exe", "cmd.exe",
                  "cl.exe", "link.exe"]


def say(text: str) -> None:
    print(f"[deploy] {text}", flush=True)


def fail(text: str) -> int:
    print(f"[deploy] STOP: {text}", flush=True)
    return 1


def run(cmd: list[str], cwd: Path | None = None, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    shown = " ".join(f'"{c}"' if " " in c else c for c in cmd)
    say(f"$ {shown}")
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=capture)
    if check and proc.returncode != 0:
        if capture:
            print(proc.stdout + proc.stderr, flush=True)
        raise RuntimeError(f"{cmd[0]} ended with exit code {proc.returncode}")
    return proc


def git(*args: str, cwd: Path, capture: bool = True) -> str:
    proc = run(["git", *args], cwd=cwd, capture=capture)
    return proc.stdout.strip() if capture else ""


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


def find_ue_root(arg: str | None) -> Path | None:
    roots = []
    if arg:
        roots.append(Path(arg))
    if os.environ.get("UE_ROOT"):
        roots.append(Path(os.environ["UE_ROOT"]))
    roots += UE_ROOTS
    for r in roots:
        if (r / "Engine/Build/BatchFiles/RunUAT.bat").is_file():
            return r
    return None


def find_butler(arg: str | None) -> Path | None:
    """--butler, BUTLER, butler on PATH, or the copy the itch app keeps in %APPDATA%/itch/broth."""
    if arg:
        return Path(arg) if Path(arg).is_file() else None
    if os.environ.get("BUTLER") and Path(os.environ["BUTLER"]).is_file():
        return Path(os.environ["BUTLER"])
    on_path = shutil.which("butler")
    if on_path:
        return Path(on_path)
    broth = Path(os.environ.get("APPDATA", "")) / "itch/broth/butler"
    chosen = broth / ".chosen-version"
    if chosen.is_file():
        exe = broth / "versions" / chosen.read_text().strip() / "butler.exe"
        if exe.is_file():
            return exe
    return None


# ---------------------------------------------------------------- the deploy worktree

def stop_leftovers(deploy: Path) -> None:
    if os.name != "nt":
        return
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
    for line in out.splitlines():
        say(line)
    if out:
        time.sleep(3)


def prepare_worktree(repo: Path, deploy: Path, commit: str) -> str:
    """Moves the deploy worktree to the commit and returns the full sha."""
    git("fetch", "origin", BRANCH, cwd=repo, capture=False)
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


def package(deploy: Path, ue_root: Path, run_dir: Path) -> Path:
    """Packages the deploy worktree into run_dir and returns the build's Windows/ folder."""
    uproject = deploy / f"{PROJECT}.uproject"
    runuat = ue_root / "Engine/Build/BatchFiles/RunUAT.bat"
    cmdexe = ue_root / "Engine/Binaries/Win64/UnrealEditor-Cmd.exe"
    win = lambda p: str(p).replace("/", "\\")
    bat = run_dir.with_suffix(".bat")
    bat.write_text(
        "@echo off\r\n"
        f'call "{win(runuat)}" BuildCookRun -project="{win(uproject)}" -platform=Win64 '
        f"-clientconfig=Development -build -cook -stage -pak -archive "
        f'-archivedirectory="{win(run_dir)}" -nocompileeditor -unrealexe="{win(cmdexe)}" -unattended\r\n'
        "exit /b %ERRORLEVEL%\r\n", encoding="ascii")
    run(["cmd", "/c", win(bat)], cwd=deploy)
    built = run_dir / "Windows"
    if not (built / f"{PROJECT}.exe").is_file():
        raise RuntimeError(f"the package step ended but {built / (PROJECT + '.exe')} is missing")
    return built


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


def check_layout(push_root: Path) -> Path:
    entries = sorted(p.name for p in push_root.iterdir())
    if entries != [TOP_FOLDER]:
        raise RuntimeError(f"{push_root} must hold only {TOP_FOLDER}/, but holds: {', '.join(entries) or 'nothing'}")
    top = push_root / TOP_FOLDER
    if not (top / f"{PROJECT}.exe").is_file():
        raise RuntimeError(f"{top} has no {PROJECT}.exe")
    return top


def secrets_check(repo_tools: Path, push_root: Path, local: Path, ue_root: Path | None) -> int:
    cmd = [sys.executable, str(repo_tools / "check_build_secrets.py"), str(push_root), "--local", str(local)]
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
    ap.add_argument("--commit", default=f"origin/{BRANCH}", help=f"the commit to build (default: origin/{BRANCH})")
    ap.add_argument("--build", help="a push root that already holds a NoHumansOnSet_PostJam_Windows/ build: "
                                    "skip the checkout and the packaging")
    ap.add_argument("--dry-run", action="store_true", help="do everything but the push")
    ap.add_argument("--hidden", action="store_true", help="push to a new channel as hidden (the first push only)")
    ap.add_argument("--repo", help="the repo folder (default: NHOS_REPO, or the main worktree of this checkout)")
    ap.add_argument("--deploy", default=os.environ.get("NHOS_DEPLOY", str(DEFAULT_DEPLOY)),
                    help=f"the deploy worktree (default: NHOS_DEPLOY or {DEFAULT_DEPLOY})")
    ap.add_argument("--ue-root", help="the engine folder (default: UE_ROOT, or the launcher's UE_5.8)")
    ap.add_argument("--butler", help="butler.exe (default: BUTLER, PATH, or the itch app's copy)")
    args = ap.parse_args()

    assert "postjam" in CHANNEL and "PostJam" in TOP_FOLDER
    if os.name != "nt" and not args.build:
        return fail("packaging a Windows build needs Windows")

    repo = find_repo(args.repo)
    local = repo / "Local"
    if not local.is_dir():
        return fail(f"{local} is missing: the secrets check needs our keys from the repo folder's Local/")
    deploy = Path(args.deploy).resolve()
    if deploy == repo or repo in deploy.parents:
        return fail(f"the deploy worktree {deploy} must be outside the repo folder {repo}")
    ue_root = find_ue_root(args.ue_root)
    butler = find_butler(args.butler)
    if butler is None and not args.dry_run:
        return fail("butler not found (pass --butler or put it on PATH)")
    say(f"repo folder {repo}")

    try:
        if args.build:
            push_root = Path(args.build).resolve()
            sha = None
            if args.commit != f"origin/{BRANCH}":
                sha = git("rev-parse", "--verify", f"{args.commit}^{{commit}}", cwd=repo)
        else:
            if ue_root is None:
                return fail("the engine was not found (pass --ue-root or set UE_ROOT)")
            sha = prepare_worktree(repo, deploy, args.commit)
            say(f"building {sha[:7]} in {deploy}")
            deploy_dir = deploy / "Packaged" / "deploy"
            # Only the newest run's build is kept.
            if deploy_dir.is_dir():
                for old in deploy_dir.iterdir():
                    shutil.rmtree(old) if old.is_dir() else old.unlink()
            push_root = deploy_dir / sha[:7]
            push_root.mkdir(parents=True)
            built = package(deploy, ue_root, push_root)
            built.rename(push_root / TOP_FOLDER)
        top = check_layout(push_root)
        strip_build(top)
    except (RuntimeError, OSError, subprocess.SubprocessError) as e:
        return fail(str(e))

    code = secrets_check(HERE, push_root, local, ue_root)
    if code != 0:
        return fail(f"the secrets check ended with exit code {code}; nothing was pushed")
    say("the secrets check is clean")

    if sha:
        when = git("show", "-s", "--format=%cI", sha, cwd=repo)
        day = datetime.fromisoformat(when).astimezone(timezone.utc).strftime("%Y-%m-%d")
        version = f"postjam-{day}-{sha[:7]}"
    else:
        version = f"postjam-{datetime.now(timezone.utc):%Y-%m-%d}-manual"

    cmd = [str(butler) if butler else "butler", "push", str(push_root), f"{GAME}:{CHANNEL}",
           "--userversion", version, "--if-changed"]
    if butler:
        found = channels(butler)
        if found is None:
            return fail("butler could not read the page's channels back")
        say(f"channels on the page: {', '.join(found) or 'none'} (the jam's file has no channel)")
        if args.hidden and CHANNEL in found:
            return fail(f"--hidden works only on a new channel, and {CHANNEL} exists")
    if args.hidden:
        cmd.append("--hidden")
    if args.dry_run:
        say("dry run: would push with " + " ".join(cmd))
        say(f"the build is in {push_root}")
        return 0
    try:
        run(cmd, capture=False)
    except RuntimeError as e:
        return fail(str(e))
    say(f"pushed {version} to {GAME}:{CHANNEL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
