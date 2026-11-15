"""Build Docs/tasks/T45-build/props.json (the draft of Content/NHOS/Data/props.json).

Reads the cards' props from a scenes.json (default: the T44 draft; pass the real
Content/NHOS/Data/scenes.json once T44 has landed) and each model's fit from
Docs/PropArt/manifest.json. Run from the repo root:

    python Docs/tasks/T45-build/make_props.py [path/to/scenes.json] [out.json]

It fails (assert) if a card prop has no manifest entry, so a renamed prop shows up.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
scenes_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "Docs/tasks/T44-build/scenes.json"
out_path = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "Docs/tasks/T45-build/props.json"

# Longest side in cm on stage, per prop (T43's finding: 30 cm for every prop read wrong for
# rings, pills, watches, swords and staffs). Robots are 150 cm tall with hands at about 75 cm.
SIZE_CM = {
    "tin-can robot": 45, "glow-stick sword": 70, "toy blaster": 32, "piggy bank": 32,
    "cursed ring": 12, "glowing staff": 90, "water bucket": 35, "frying pan": 42,
    "dino egg": 32, "meaty drumstick": 32, "safety waiver": 30, "dino plush": 36,
    "plush horse head": 40, "cannoli tray": 42, "wedding envelope": 26, "bowl of oranges": 30,
    "glowing briefcase": 45, "gold pocket watch": 14, "giant milkshake": 45, "giant cheeseburger": 40,
    "rolled-up rug": 80, "bowling ball": 26, "ransom bag": 36, "milk carton": 26,
    "red pill": 12, "blue pill": 12, "ringing phone": 26, "bent spoon": 20,
}

# A prop with no model yet: an engine shape in an old T19 prop material (T45 step 1).
# Engine basic shapes are 100 cm across with the pivot at the center.
FALLBACK = {
    "bowl of oranges": {"mesh": "/Engine/BasicShapes/Sphere.Sphere",
                        "material": "/Game/NHOS/Stage/Materials/MI_PropOrange.MI_PropOrange",
                        "note": "no model yet (T43 skipped it: core false); one big clay orange"},
}
DEFAULT_FALLBACK = {"mesh": "/Engine/BasicShapes/Cube.Cube",
                    "material": "/Game/NHOS/Stage/Materials/MI_Cardboard.MI_Cardboard"}

manifest = {a["id"]: a for a in json.loads((ROOT / "Docs/PropArt/manifest.json").read_text())["assets"]}
scenes = json.loads(scenes_path.read_text())

props, missing, cards = {}, [], {}
for card in scenes["cards"]:
    cards[card["id"]] = list(card["props"])
    for name in card["props"]:
        mid = name.replace("-", "_").replace(" ", "_")
        a = manifest.get(mid)
        assert a is not None, f"{name!r} ({mid}) has no entry in Docs/PropArt/manifest.json"
        assert a.get("story") == card["id"], f"{name!r} is on {card['id']} but the manifest says {a.get('story')}"
        size = SIZE_CM.get(name, 30)
        fit = a.get("fit")
        if fit and fit.get("asset"):
            pkg = fit["asset"]
            assert (ROOT / ("Content" + pkg[len("/Game"):] + ".uasset")).exists(), f"{pkg} is not on disk"
            b = fit["bounds_cm"]
            scale = round(size / max(b), 4)
            h = b[2] * scale
            props[name] = {
                "card": card["id"],
                "mesh": f"{pkg}.{pkg.rsplit('/', 1)[1]}",
                "scale": scale,
                "yaw": fit["yaw"],
                "z": round(-fit["min_z"] * scale, 1),
                "grip_z": round(-h / 2, 1),
                "wear": "hand",
                "size_cm": size,
            }
        else:
            fb = FALLBACK.get(name, DEFAULT_FALLBACK)
            scale = round(size / 100.0, 4)
            props[name] = {
                "card": card["id"],
                "mesh": fb["mesh"],
                "material": fb["material"],
                "scale": scale,
                "yaw": 0,
                "z": round(50.0 * scale, 1),
                "grip_z": round(-50.0 * scale, 1),
                "wear": "hand",
                "size_cm": size,
            }
            missing.append({"name": name, "card": card["id"], "manifest_id": mid,
                            "why": fb.get("note", "no model yet")})

out = {
    "_readme": [
        "Each card prop's look on the Prop Table (T45). Keyed by the prop's name exactly as scenes.json spells it.",
        "mesh: the static mesh's object path, loaded by BP_Prop.SetProp as a soft reference at Scene Prep. material: only for a prop with no model yet (it goes on slot 0); a model keeps its own M_<Name> material (SetProp clears slot 0's override).",
        "scale: uniform scale of the Model component (size_cm / the model's longest side in Docs/PropArt/manifest.json). yaw: the Model's relative yaw (90 turns every Meshy model to the house). z: the Model's relative height, which puts the model's bottom on the actor's origin.",
        "grip_z: the actor's height offset from the hand when held, so the hand holds the middle of the prop (BP_Prop.GripLoc z). wear: hand, head or back (BP_Robot.Receive's slots).",
        "The game never sends this file to the AIs. The state's set.props is the card's own props list from scenes.json.",
        "Docs/tasks/T45-build/make_props.py builds this file from scenes.json and the manifest; size_cm is its only hand-set value.",
    ],
    "props": props,
    "missing_models": missing,
}
out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
print(f"{len(props)} props on {len(cards)} cards, {len(missing)} without a model -> {out_path}")
