#!/usr/bin/env python3
"""Check that a packaged build holds no API key or other secret, before you zip or upload it.

Usage (from anywhere; Python 3.10+, no packages needed):

    python Tools/check_build_secrets.py                        # the sources, then every build and zip
                                                               # in Packaged/ and Saved/StagedBuilds/
    python Tools/check_build_secrets.py Packaged/Windows       # one build folder
    python Tools/check_build_secrets.py TeamName_NoHumansOnSet.zip   # the zip you will upload
    python Tools/check_build_secrets.py --sources              # only the sources
    python Tools/check_build_secrets.py --local C:/path/to/repo/Local <build>
                                                               # take the keys from another Local/

What it looks for:

- Our real secrets, by value: every string field named "...key" (16 characters or more) in this
  machine's Local/*.json (llm_key.json, stats.json, meshy_key.json and the rest) and every value in
  Relay/.dev.vars. It searches for each one as UTF-8 and as UTF-16, whole or in part.
  --local <folder> reads the keys from that Local/ folder instead (and Relay/.dev.vars from the
  Relay/ folder next to it), for a checkout with no Local/ of its own, such as a git worktree or
  the deploy worktree that Tools/deploy_itch.py builds in. Nothing is copied out of it.
- Anything shaped like a key: Anthropic, OpenAI, xAI, Meta, Meshy, Google, GitHub and AWS keys,
  and private keys. The masked example key in errors.json does not match.
- Files that must never ship: a Local/ folder (llm_key.json holds the keys a tester pasted on the
  key screen, which the game saves inside the build), any *_key.json, stats.json, switches.json,
  .dev.vars, .env, .pem and .p12 files, and a Saved/ folder (a test run's logs and save game,
  with our player id and our machine's paths).

Where it looks:

- The sources the cook reads: Content/ (every .uasset, .umap and data file), Config/ and the
  .uproject. Content/NHOS/Data ships as loose files, and every asset can carry a string.
- A build: every loose file, and every file inside its .pak and IoStore (.utoc/.ucas) containers.
  The containers are compressed, so it opens them with the engine's UnrealPak (found from
  --ue-root, the UE_ROOT variable, or the launcher's default UE_5.8 folder) and checks that the
  cooked BPC_LLMClient reads back as text, so the scan is not blind.
- A .zip: the names inside it, then everything in it as a build.

It never prints a secret: a hit names the file, which secret or which kind of key, and its length.
Exit code: 0 clean, 1 something found, 2 not everything could be checked (no UnrealPak, an LFS
file that is not pulled, a container that did not open).
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROJECT = "AIMegaJam2026"

# A string that the cooked BPC_LLMClient always holds. If it doesn't read back from the
# extracted container, the extraction gave compressed bytes and the scan of the assets is blind.
CANARY_FILE = "NHOS/Core/BPC_LLMClient.uexp"
CANARY = b"Local/llm_key.json"

# Each key shape starts with a fixed prefix. A fast substring search for the prefix runs first,
# and the regex only where the prefix is present: one regex with alternatives is ~30x slower.
_KEY_SHAPES = [
    ("an Anthropic API key", rb"sk-ant-", rb"[A-Za-z0-9_\-]{30,}"),
    ("an OpenAI API key", rb"sk-proj-", rb"[A-Za-z0-9_\-]{30,}"),
    ("an OpenAI API key", rb"sk-svcacct-", rb"[A-Za-z0-9_\-]{30,}"),
    ("an OpenAI API key", rb"sk-admin-", rb"[A-Za-z0-9_\-]{30,}"),
    ("an xAI API key", rb"xai-", rb"[A-Za-z0-9]{40,}"),
    ("a Meta API key", rb"LLM_", rb"[A-Za-z0-9]{12,}_[A-Za-z0-9]{20,}"),
    ("a Meshy API key", rb"msy_", rb"[A-Za-z0-9]{20,}"),
    ("a Google API key", rb"AIza", rb"[0-9A-Za-z_\-]{35}"),
    ("a GitHub token", rb"ghp_", rb"[A-Za-z0-9]{36,}"),
    ("a GitHub token", rb"gho_", rb"[A-Za-z0-9]{36,}"),
    ("a GitHub token", rb"ghs_", rb"[A-Za-z0-9]{36,}"),
    ("a GitHub token", rb"github_pat_", rb"[A-Za-z0-9_]{40,}"),
    ("an AWS access key", rb"AKIA", rb"[0-9A-Z]{16}(?![0-9A-Z])"),
    ("an AWS access key", rb"ASIA", rb"[0-9A-Z]{16}(?![0-9A-Z])"),
    ("a private key", rb"-----BEGIN ", rb"(?:[A-Z]+ )?PRIVATE KEY-----\s*[A-Za-z0-9+/=\r\n]{64,}"),
]
PATTERNS = [(label, prefix, re.compile(re.escape(prefix) + rest)) for label, prefix, rest in _KEY_SHAPES]
SHAPE_NAMES = sorted({label for label, _, _ in PATTERNS})

CHUNK = 64 * 1024 * 1024
OVERLAP = 4096  # longer than any needle or key, so a hit across two chunks is still found

SECRET_FILE_NAMES = {"llm_key.json", "stats.json", "switches.json", ".env"}
SECRET_SUFFIXES = (".pem", ".p12", ".pfx")


class Report:
    def __init__(self) -> None:
        self.problems: list[str] = []
        self.gaps: list[str] = []

    def problem(self, text: str) -> None:
        self.problems.append(text)
        print(f"  FOUND  {text}")

    def gap(self, text: str) -> None:
        self.gaps.append(text)
        print(f"  NOT CHECKED  {text}")


def rel(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


# ---------------------------------------------------------------- the secrets to look for

def is_secret_field(name: str) -> bool:
    n = name.lower()
    if n.startswith("_") or n == "key_field":
        return False
    return n.endswith("key") or "token" in n or "secret" in n


def walk_json(obj, path, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                if is_secret_field(k) and len(v.strip()) >= 16:
                    out.append((f"{path} {k}", v.strip()))
            else:
                walk_json(v, f"{path} {k}" if path else k, out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_json(v, f"{path}[{i}]", out)


def load_secrets(local: Path) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if local.is_dir():
        for f in sorted(local.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8-sig"))
            except (OSError, ValueError):
                continue
            items: list[tuple[str, str]] = []
            walk_json(data, "", items)
            for field, value in items:
                found.append((f"Local/{f.name}:{field.strip()}", value))
    for f in sorted((local.parent / "Relay").glob(".dev.vars*")):
        if f.name.endswith(".example"):
            continue
        try:
            lines = f.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            if "=" in line and not line.lstrip().startswith("#"):
                name, value = line.split("=", 1)
                value = value.strip().strip('"').strip("'")
                if len(value) >= 16:
                    found.append((f"Relay/{f.name}:{name.strip()}", value))
    # The same key can sit in two files; look for it once.
    seen: set[str] = set()
    unique = []
    for label, value in found:
        if value not in seen:
            seen.add(value)
            unique.append((label, value))
    return unique


def needles_for(secrets):
    """Each secret becomes a 20-character slice from its middle (or the whole value when short),
    so a cut-off copy is found too, as UTF-8 and as UTF-16."""
    out = []
    for label, value in secrets:
        if len(value) >= 40:
            mid = len(value) // 2
            part = value[mid - 10:mid + 10]
        else:
            part = value
        out.append((label, len(value), part.encode("utf-8")))
        out.append((label, len(value), part.encode("utf-16-le")))
    return out


# ---------------------------------------------------------------- scanning files

def scan_bytes_file(path: Path, shown: str, needles, report: Report, shapes: bool = True) -> None:
    hits: set[str] = set()
    try:
        with path.open("rb") as fh:
            tail = b""
            while True:
                chunk = fh.read(CHUNK)
                if not chunk:
                    break
                data = tail + chunk
                for label, length, needle in needles:
                    if needle in data:
                        hits.add(f"{shown}: holds the value of {label} ({length} characters)")
                if shapes:
                    for kind, prefix, rx in PATTERNS:
                        if prefix in data:
                            for m in rx.finditer(data):
                                hits.add(f"{shown}: holds {kind} ({len(m.group(0))} characters)")
                tail = data[-OVERLAP:]
    except OSError as e:
        report.gap(f"{shown}: could not read ({e})")
        return
    for h in sorted(hits):
        report.problem(h)


def forbidden_reason(relpath: str) -> str | None:
    parts = [p for p in relpath.replace("\\", "/").split("/") if p]
    lower = [p.lower() for p in parts]
    name = lower[-1] if lower else ""
    if "local" in lower[:-1]:
        return "is in a Local/ folder (keys and switches), which must not ship"
    if "saved" in lower[:-1]:
        return "is in a Saved/ folder (a test run's logs and save game), which must not ship"
    if name in SECRET_FILE_NAMES or name.endswith("_key.json") or name.startswith(".dev.vars"):
        return "is a key or switches file, which must not ship"
    if name.endswith(SECRET_SUFFIXES):
        return "is a certificate or private key file, which must not ship"
    return None


CONTAINER_SUFFIXES = (".pak", ".ucas", ".utoc")


def scan_tree(root: Path, shown_base: str, needles, report: Report, check_names: bool,
              container_shapes: bool = True) -> int:
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for fn in sorted(filenames):
            p = Path(dirpath) / fn
            r = rel(p, root)
            shown = f"{shown_base}/{r}" if shown_base else r
            if check_names:
                why = forbidden_reason(r)
                if why:
                    report.problem(f"{shown} {why}")
            # When the containers get opened, their files are checked for key shapes there;
            # the raw (compressed) bytes only get the by-value search, so a hit isn't listed twice.
            shapes = container_shapes or p.suffix.lower() not in CONTAINER_SUFFIXES
            scan_bytes_file(p, shown, needles, report, shapes)
            count += 1
    return count


# ---------------------------------------------------------------- the sources

def scan_sources(needles, report: Report) -> None:
    print("Sources (what the cook reads): Content/, Config/, the .uproject")
    count = 0
    lfs_missing = 0
    targets = [REPO / "Content", REPO / "Config"]
    for top in targets:
        if not top.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(top):
            dirnames.sort()
            for fn in sorted(filenames):
                p = Path(dirpath) / fn
                shown = rel(p, REPO)
                if fn.lower().endswith((".uasset", ".umap")):
                    try:
                        with p.open("rb") as fh:
                            head = fh.read(64)
                    except OSError:
                        head = b""
                    if head.startswith(b"version https://git-lfs"):
                        lfs_missing += 1
                        continue
                scan_bytes_file(p, shown, needles, report)
                count += 1
    for p in sorted(REPO.glob("*.uproject")):
        scan_bytes_file(p, p.name, needles, report)
        count += 1
    if lfs_missing:
        report.gap(f"{lfs_missing} assets are LFS pointers, not pulled (run git lfs pull)")
    print(f"  {count} files read")


# ---------------------------------------------------------------- builds and containers

def find_unrealpak(ue_root: str | None) -> Path | None:
    roots = []
    if ue_root:
        roots.append(Path(ue_root))
    if os.environ.get("UE_ROOT"):
        roots.append(Path(os.environ["UE_ROOT"]))
    system = platform.system()
    if system == "Windows":
        roots.append(Path("C:/Program Files/Epic Games/UE_5.8"))
        exe = Path("Engine/Binaries/Win64/UnrealPak.exe")
    elif system == "Darwin":
        roots.append(Path("/Users/Shared/Epic Games/UE_5.8"))
        exe = Path("Engine/Binaries/Mac/UnrealPak")
    else:
        exe = Path("Engine/Binaries/Linux/UnrealPak")
    for r in roots:
        if (r / exe).is_file():
            return r / exe
    return None


def extract_container(unrealpak: Path, container: Path, out: Path) -> tuple[bool | None, str]:
    """True when files came out, None when the container has no file index (global.utoc holds
    only the engine's global shaders and script data, nothing named), False when it failed."""
    out.mkdir(parents=True, exist_ok=True)
    try:
        proc = subprocess.run([str(unrealpak), str(container.resolve()), "-Extract", str(out)],
                              capture_output=True, text=True, timeout=900)
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, str(e)
    files = sum(len(f) for _, _, f in os.walk(out))
    if files == 0:
        if "Missing directory index" in proc.stdout + proc.stderr:
            return None, "no file index"
        last = (proc.stdout + proc.stderr).strip().splitlines()[-1:] or [f"exit code {proc.returncode}"]
        return False, last[0]
    return True, f"{files} files"


def scan_build(build: Path, shown_base: str, needles, report: Report, unrealpak: Path | None) -> None:
    print(f"Build: {shown_base}")
    loose = scan_tree(build, shown_base, needles, report, check_names=True,
                      container_shapes=unrealpak is None)
    print(f"  {loose} loose files read (the containers' raw bytes too)")
    containers = sorted([p for p in build.rglob("*") if p.suffix.lower() in (".pak", ".utoc")])
    if not containers:
        report.gap(f"{shown_base}: no .pak or .utoc found; is this a packaged build?")
        return
    if unrealpak is None:
        report.gap(f"{shown_base}: UnrealPak not found (pass --ue-root), so the {len(containers)} "
                   "compressed containers were not opened")
        return
    canary_seen = False
    canary_ok = False
    for c in containers:
        shown_c = f"{shown_base}/{rel(c, build)}"
        tmp = Path(tempfile.mkdtemp(prefix="nhos_secrets_"))
        try:
            ok, info = extract_container(unrealpak, c, tmp)
            if ok is None:
                print(f"  {shown_c}: {info} (engine data only); its raw bytes were checked")
                continue
            if not ok:
                # A .pak next to a .utoc can be an empty stub; only a real failure is a gap.
                if c.suffix.lower() == ".pak" and c.stat().st_size < 4096:
                    continue
                report.gap(f"{shown_c}: UnrealPak could not open it ({info})")
                continue
            for p in tmp.rglob("*"):
                if p.is_file() and p.as_posix().endswith(CANARY_FILE):
                    canary_seen = True
                    if CANARY in p.read_bytes():
                        canary_ok = True
            n = scan_tree(tmp, shown_c, needles, report, check_names=True)
            print(f"  {shown_c}: opened, {n} files read")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    if canary_seen and not canary_ok:
        report.gap(f"{shown_base}: the extracted assets did not read back as text, so their scan is blind")
    elif not canary_seen:
        report.gap(f"{shown_base}: BPC_LLMClient was not in any container, so the scan could not prove "
                   "it reads the cooked assets")


def scan_zip(zpath: Path, needles, report: Report, unrealpak: Path | None) -> None:
    print(f"Zip: {zpath.name}")
    try:
        zf = zipfile.ZipFile(zpath)
    except (OSError, zipfile.BadZipFile) as e:
        report.gap(f"{zpath.name}: could not open ({e})")
        return
    with zf:
        for name in zf.namelist():
            why = forbidden_reason(name)
            if why:
                report.problem(f"{zpath.name}:{name} {why}")
        tmp = Path(tempfile.mkdtemp(prefix="nhos_zip_"))
        try:
            zf.extractall(tmp)
            scan_build(tmp, zpath.name, needles, report, unrealpak)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("targets", nargs="*", help="build folders or zips (default: every one in Packaged/ and Saved/StagedBuilds/)")
    ap.add_argument("--sources", action="store_true", help="check only the sources, no build")
    ap.add_argument("--ue-root", help="the engine folder that holds Engine/Binaries/.../UnrealPak")
    ap.add_argument("--local", help="the Local/ folder to read our keys from (default: Local/ in this "
                                    "repo); Relay/.dev.vars is read from the Relay/ folder next to it")
    args = ap.parse_args()

    local = Path(args.local).resolve() if args.local else REPO / "Local"
    if args.local and not local.is_dir():
        print(f"--local {args.local}: no such folder")
        return 2
    secrets = load_secrets(local)
    needles = needles_for(secrets)
    if secrets:
        names = ", ".join(label for label, _ in secrets)
        print(f"Looking for {len(secrets)} secrets by value ({names}) and {len(SHAPE_NAMES)} kinds of key.")
    else:
        print(f"No Local/*.json key files on this machine: looking for {len(SHAPE_NAMES)} kinds of key only.")
        # Tools/deploy_itch.py stops on this line: a build checked without our keys is not checked.

    report = Report()
    unrealpak = None if args.sources else find_unrealpak(args.ue_root)

    if args.targets:
        for t in args.targets:
            p = Path(t)
            if p.suffix.lower() == ".zip" and p.is_file():
                scan_zip(p, needles, report, unrealpak)
            elif p.is_dir():
                scan_build(p, rel(p, REPO), needles, report, unrealpak)
            else:
                report.gap(f"{t}: no such folder or zip")
    else:
        scan_sources(needles, report)
        if not args.sources:
            # Packaged/ holds the archived builds and zips. On a Mac, the playable app is the
            # staged one in Saved/StagedBuilds/ (the archive step copies only the executable).
            builds = []
            for folder in (REPO / "Packaged", REPO / "Saved" / "StagedBuilds"):
                if folder.is_dir():
                    builds += [p for p in sorted(folder.iterdir())
                               if p.is_dir() or p.suffix.lower() == ".zip"]
            if not builds:
                print("No build in Packaged/ or Saved/StagedBuilds/ to check.")
            for b in builds:
                if b.is_dir():
                    scan_build(b, rel(b, REPO), needles, report, unrealpak)
                else:
                    scan_zip(b, needles, report, unrealpak)

    print()
    if report.problems:
        print(f"RESULT: FOUND {len(report.problems)} problem(s). Do not zip or upload this build.")
        return 1
    if report.gaps:
        print(f"RESULT: nothing found, but {len(report.gaps)} part(s) were not checked (see NOT CHECKED).")
        return 2
    print("RESULT: clean. No key, key file or test-run data found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
