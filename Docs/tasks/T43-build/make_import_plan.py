#!/usr/bin/env python3
"""Print T43's import plan: one entry per generated model still to import.

Reads Docs/PropArt/manifest.json (Python 3.10+, no packages) and lists, in
import order (manifest order: headpieces, then props grouped by card, then set
pieces), every asset that has an `fbx` and no StaticMesh at its destination
yet. For each one it prints the source FBX, the destination folder, the asset
name, the kind and the material choice, plus the exact arguments for
StaticMeshTools.import_file and the renames that must follow it.

An asset whose SM_<Name> already exists somewhere else under
Content/NHOS/Stage/ (the style test's SM_PlushHorseHead in Props/Meshes/) is
listed as a MOVE, not an import: T43 moves the reviewed asset and its material
and texture instead of importing it a second time.

Usage (from the repo root or anywhere):
    python Docs/tasks/T43-build/make_import_plan.py
    python Docs/tasks/T43-build/make_import_plan.py --kind headpiece
    python Docs/tasks/T43-build/make_import_plan.py --json Saved/T43/import_plan.json
    python Docs/tasks/T43-build/make_import_plan.py --manifest <other manifest.json>

--json writes the same plan as a JSON list. Put it under Saved/ so an Unreal
MCP ProgrammaticToolset script can read it with AssetTools.read_file (the
sandbox has no open(); T17).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CONTENT = REPO / "Content"
STAGE = CONTENT / "NHOS" / "Stage"

# Where each kind goes. Props go one folder per card (the manifest's `story`).
DEST = {
    "headpiece": "/Game/NHOS/Stage/Headpieces",
    "prop": "/Game/NHOS/Stage/Props/{story}",
    "set": "/Game/NHOS/Stage/Set",
}
CLAY_INSTANCE = "/Game/NHOS/Stage/Materials/MI_Clay_Neutral"


def pascal(asset_id: str) -> str:
    """plush_horse_head -> PlushHorseHead (the style test's naming)."""
    return "".join(part[:1].upper() + part[1:] for part in asset_id.split("_") if part)


def game_to_disk(game_path: str) -> Path:
    """/Game/NHOS/Stage/Set/SM_X -> <repo>/Content/NHOS/Stage/Set/SM_X.uasset"""
    assert game_path.startswith("/Game/")
    return CONTENT / (game_path[len("/Game/"):] + ".uasset")


def disk_to_game(path: Path) -> str:
    rel = path.relative_to(CONTENT).with_suffix("")
    return "/Game/" + rel.as_posix()


def fbx_problem(fbx: Path) -> str | None:
    """None if the FBX looks real; else why not (missing, or an LFS pointer)."""
    if not fbx.is_file():
        return "missing on disk"
    with fbx.open("rb") as f:
        head = f.read(64)
    if head.startswith(b"version https://git-lfs"):
        return "is an LFS pointer (run git lfs pull)"
    return None


def plan(manifest: dict, kinds: set[str] | None) -> tuple[list[dict], list[str]]:
    entries: list[dict] = []
    notes: list[str] = []
    for a in manifest["assets"]:
        kind = a["kind"]
        if kinds and kind not in kinds:
            continue
        if not a.get("fbx"):
            continue
        name = pascal(a["id"])
        sm = f"SM_{name}"
        if kind == "prop":
            if not a.get("story"):
                notes.append(f"{a['id']}: prop without a story, skipped")
                continue
            folder = DEST["prop"].format(story=a["story"])
        else:
            folder = DEST[kind]
        dest_asset = f"{folder}/{sm}"
        if game_to_disk(dest_asset).is_file():
            notes.append(f"{a['id']}: {dest_asset} already exists, skipped")
            continue

        source = (REPO / a["fbx"]).resolve()
        problem = fbx_problem(source)
        if problem:
            notes.append(f"{a['id']}: {a['fbx']} {problem}, skipped")
            continue

        with_materials = kind != "headpiece"
        with_textures = with_materials and bool(a.get("texture"))
        renames = []
        if with_materials:
            renames.append({"from_class": "Material", "to": f"{folder}/M_{name}"})
        if with_textures:
            renames.append({"from_class": "Texture2D", "to": f"{folder}/T_{name}_BaseColor"})

        if with_materials:
            material = ("Meshy's material and texture, renamed "
                        f"M_{name} and T_{name}_BaseColor" if with_textures
                        else f"Meshy's material (no texture), renamed M_{name}")
        else:
            material = f"none on import; then {CLAY_INSTANCE.rsplit('/', 1)[1]} on every slot"

        entry = {
            "id": a["id"],
            "kind": kind,
            "action": "import",
            "source": a["fbx"],
            "source_abs": str(source),
            "folder": folder,
            "asset_name": sm,
            "asset_path": dest_asset,
            "material": material,
            "size_cm": a.get("size_cm"),
            "import_args": {
                "folder_path": folder,
                "asset_name": sm,
                "source_file": str(source),
                "import_materials": with_materials,
                "import_textures": with_textures,
                "combine_meshes": True,
            },
            "renames": renames,
            "slot_material": None if with_materials else CLAY_INSTANCE,
            "fbm": str(source.with_suffix(".fbm").relative_to(REPO)),
            "fbm_to": f"Local/art/props/{a['id']}/",
        }

        # The same mesh somewhere else under Stage/ (the style test's copy)?
        elsewhere = sorted(p for p in STAGE.rglob(f"{sm}.uasset"))
        if elsewhere:
            old = disk_to_game(elsewhere[0])
            old_folder = old.rsplit("/", 1)[0]
            moves = [{"from": old, "to": dest_asset}]
            for prefix, suffix in (("M_", ""), ("T_", "_BaseColor")):
                sib = elsewhere[0].with_name(f"{prefix}{name}{suffix}.uasset")
                if sib.is_file():
                    moves.append({"from": f"{old_folder}/{sib.stem}", "to": f"{folder}/{sib.stem}"})
            entry.update(action="move", moves=moves, import_args=None, renames=[])
            entry["material"] = "keeps its renamed Meshy material and texture (moved with it)"
        entries.append(entry)
    return entries, notes


def show(entries: list[dict], notes: list[str], manifest_label: str) -> None:
    print(f"T43 import plan from {manifest_label}: {len(entries)} to do")
    for i, e in enumerate(entries, 1):
        print()
        print(f"{i}. {e['id']} ({e['kind']}, {e['size_cm']} cm): {e['action'].upper()}")
        print(f"   source:   {e['source']}")
        print(f"   folder:   {e['folder']}")
        print(f"   asset:    {e['asset_name']}")
        print(f"   material: {e['material']}")
        if e["action"] == "move":
            for m in e["moves"]:
                print(f"   AssetTools.move {json.dumps({'path': m['from'], 'new_path': m['to']})}")
            continue
        print(f"   StaticMeshTools.import_file {json.dumps(e['import_args'])}")
        for r in e["renames"]:
            print(f"   then AssetTools.move the returned {r['from_class']} to {r['to']}")
        if e["slot_material"]:
            print(f"   then StaticMeshTools.set_material on each slot: {e['slot_material']}")
        print(f"   then move {e['fbm']}/ (if any) to {e['fbm_to']}")
    if notes:
        print()
        print("Skipped:")
        for n in notes:
            print(f"- {n}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--manifest", type=Path, default=REPO / "Docs/PropArt/manifest.json")
    ap.add_argument("--kind", action="append", choices=sorted(DEST),
                    help="only this kind (repeatable)")
    ap.add_argument("--json", type=Path, help="also write the plan as JSON to this path")
    args = ap.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    entries, notes = plan(manifest, set(args.kind) if args.kind else None)
    try:
        label = args.manifest.resolve().relative_to(REPO).as_posix()
    except ValueError:
        label = str(args.manifest)
    show(entries, notes, label)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(entries, indent=1) + "\n", encoding="utf-8")
        print(f"\nwrote {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
