"""Build the T47 costume drafts. Run from the repo root:

    python Docs/tasks/T47-build/make_costumes.py [path/to/scenes.json]

Writes, next to this script:
  costumes.json      the draft of Content/NHOS/Data/costumes.json: each headpiece's mesh and its
                     fit on the robot's head, computed from Docs/PropArt/manifest.json (fit.bounds_cm)
                     and T46's head (a 70 cm pill whose dome tops out at z 158 in Rig).
  scenes_seats.json  every card's seats with the headpiece and color T47 adds, in scenes.json order.
It then checks the roles in a scenes.json (default Content/NHOS/Data/scenes.json) against SEATS.
With a second path it writes that scenes.json with headpiece and color added to every seat and one
sentence added to the _readme's cards line (T47 step 1). It edits the text, so the file keeps its
hand formatting. T47 runs it in place:

    python Docs/tasks/T47-build/make_costumes.py Content/NHOS/Data/scenes.json Content/NHOS/Data/scenes.json

It stops on an assert if a card, a role or a manifest entry has moved.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
scenes_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "Content/NHOS/Data/scenes.json"
out_scenes = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None

# T46's head, in Rig space (cm): the top cap is a sphere of radius 35 centered at z 123,
# so the dome tops out at z 158. The face (the screen) is at +X; the back slot is at X -38.
# The antenna stalk (Nub) runs from z 156 to 180 and the toppers sit above it.
DOME_TOP = 158.0
STALK_BASE = 156.0

# The fit of each headpiece, set by hand from the manifest's bounds (the models' shapes were not
# looked at from below; see T43's "underside"). width_cm is the model's width across the face
# (raw X, since every Meshy model faces raw +Y); bottom_z is where its lowest point sits in Rig;
# x moves it toward the face (+) or the back (-). lift: how far the stalk and toppers rise so they
# poke out of the top (0 for pieces that leave the dome's top open).
FIT = {
    #                  width  bottom   x     lift?
    "hood":            (98,   98.0,  -6.0,  True),   # baggy; its opening faces the house, rim below the screen's top corners
    "dark_shades":     (74,  102.0,  None,  False),  # on the eyes (eye line about z 116: check EyeL); front at x 36
    "top_hat":         (72,  150.0,   0.0,  True),
    "bob_wig":         (84,   92.0,  -4.0,  True),   # open underside (T43); the fringe may reach the screen's top
    "ball_cap":        (74,  135.0,  20.0,  True),   # the bill reaches forward over the screen
    "wide_brim_hat":   (90,  150.0,   0.0,  True),
    "saucepan_helmet": (126, 128.0,   0.0,  True),   # width includes the handle (raw X 190 vs pot 115)
    "wizard_hat":      (80,  150.0,   0.0,  True),
    "tiara":           (64,  140.0,   0.0,  False),  # a circlet around the dome; the stalk shows through its middle
    "fedora":          (80,  150.0,   0.0,  True),
    "horned_helmet_beard": (85, 68.0, 4.0,  True),   # the beard hangs over the screen's lower half (T43); check the eyes
    "dino_hood":       (84,  100.0,  10.0,  True),   # the snout reaches forward over the screen
    "beanie":          (76,  130.0,   0.0,  True),
}
FRONT_YAW = 270  # turns a Meshy model (face at raw +Y) to the robot's face at Rig +X
EYE_FRONT_X = 36.0

# Each role's headpiece and color, from the design doc's Stories tab (rev 9) and Art Inspiration
# Costumes (rev 29). The doc names colors in words; these hex values are this sheet's picks (sRGB).
# Secondary details (trim, bands, the beard) are dropped: each headpiece takes one color.
SEATS = {
    "space_plans": [
        ("A farm kid", "wide_brim_hat", "#E3C770", "sandy straw yellow"),
        ("A masked villain", "saucepan_helmet", "#222226", "black"),
        ("An old desert hermit", "hood", "#7A5232", "earthy brown"),
        ("A smuggler pilot", "dark_shades", "#1A1A1E", "black lenses"),
        ("A rebel princess", "tiara", "#D9DEE6", "silver and white"),
    ],
    "mine_bridge": [
        ("A barefoot homebody", "bob_wig", "#8B4A26", "chestnut brown"),
        ("A bossy old wizard", "wizard_hat", "#8C8A86", "dusty grey"),
        ("A brooding ranger", "hood", "#5E7A3A", "moss green"),
        ("A loud, proud dwarf", "horned_helmet_beard", "#6B6F75", "iron grey (ginger beard dropped)"),
        ("A vain elf", "tiara", "#C9CED6", "pale silver"),
    ],
    "dino_island": [
        ("The billionaire park owner", "top_hat", "#F0E6CC", "cream white"),
        ("A dinosaur expert", "wide_brim_hat", "#7A7A3A", "olive green"),
        ("A runaway dinosaur with tiny arms", "dino_hood", "#5DA642", "grass green"),
        ("A kid on the tour", "ball_cap", "#C8202E", "cherry red"),
        ("The park's nervous lawyer", "dark_shades", "#1A1A1E", "black"),
    ],
    "favor_father": [
        ("The family boss, father of the bride", "fedora", "#2A2A2E", "charcoal black (red band dropped)"),
        ("The hot-headed eldest son", "ball_cap_back", "#E0482E", "tomato red, worn backwards"),
        ("The reluctant youngest son", "hood", "#6B6B30", "olive green"),
        ("The family adviser", "dark_shades", "#1A1A1E", "black"),
        ("A washed-up crooner", "top_hat", "#8A3FB8", "glittery purple"),
    ],
    "glowing_briefcase": [
        ("A chatty errand man in a black suit", "dark_shades", "#121216", "glossy black"),
        ("A nosy errand man in a black suit", "fedora", "#4A4A4E", "dark gray (black band dropped)"),
        ("The boss's bored wife", "bob_wig", "#141416", "jet black"),
        ("A runaway boxer who refused to lose", "hood", "#B8262A", "red (gold trim dropped)"),
        ("A smooth fixer in a tuxedo", "top_hat", "#1C1C20", "black (white band dropped)"),
    ],
    "league_night": [
        ("A laid-back slacker in a bathrobe", "hood", "#D9C9A3", "oatmeal beige"),
        ("A hot-headed teammate who knows every rule", "saucepan_helmet", "#6E7438", "olive green"),
        ("A quiet bowler nobody listens to", "ball_cap", "#9CCCEB", "pale sky blue"),
        ("A flashy rival bowler", "top_hat", "#F0459A", "hot pink"),
        ("An avant-garde artist", "bob_wig", "#1F4FC8", "cobalt blue"),
    ],
    "pick_a_pill": [
        ("A sleepy office worker", "beanie", "#6E7F92", "dull office gray-blue"),
        ("A grand leader in a long coat", "wide_brim_hat", "#6E1E2A", "deep maroon"),
        ("A rebel in black leather", "bob_wig", "#18181C", "glossy black"),
        ("A stern agent in a dark suit", "dark_shades", "#1A1A1E", "black"),
        ("A fortune-teller baking cookies", "wizard_hat", "#B9A3DE", "soft lavender"),
    ],
}

manifest = {a["id"]: a for a in json.loads((ROOT / "Docs/PropArt/manifest.json").read_text())["assets"]}
heads = {}
for hid, (width, bottom, x, lifts) in FIT.items():
    a = manifest[hid]
    assert a["kind"] == "headpiece", hid
    fit = a["fit"]
    pkg = fit["asset"]
    assert (ROOT / ("Content" + pkg[len("/Game"):] + ".uasset")).exists(), pkg
    bx, by, bz = fit["bounds_cm"]
    s = width / bx
    h, depth = bz * s, by * s
    if x is None:  # sits on the face: its front at the screen
        x = EYE_FRONT_X - depth / 2
    top = bottom + h
    heads[hid] = {
        "mesh": f"{pkg}.{pkg.rsplit('/', 1)[1]}",
        "scale": round(s, 4),
        "x": round(x, 1),
        "z": round(bottom - fit["min_z"] * s, 1),  # the mesh pivot is its center, so z = bottom + h/2
        "yaw": FRONT_YAW,
        "lift": round(max(0.0, top - DOME_TOP - 2.0), 1) if lifts else 0.0,
        "size_cm": [round(width), round(depth), round(h)],
    }
# The eldest son's cap, backwards: the same model turned round, its bill over the back.
heads["ball_cap_back"] = dict(heads["ball_cap"], yaw=(FRONT_YAW + 180) % 360, x=-heads["ball_cap"]["x"])

costumes = {
    "_readme": [
        "The headpieces the robots wear (T47). Each seat in scenes.json names one by its id ('headpiece') and gives its color ('color', sRGB hex).",
        "mesh: the static mesh's object path, loaded by BP_Robot.SetHeadpiece as a soft reference. Every headpiece model has MI_Clay_Neutral on its slots, and SetHeadpiece sets its Color.",
        "scale, x, z, yaw: the Headpiece component's relative transform under the robot's Rig (cm, degrees). The face is +X; yaw 270 turns a model's face to it. z puts the model's lowest point where it sits on the head.",
        "lift: how far the antenna stalk and the persona's topper rise while the headpiece is on, so they poke out of its top. 0 leaves them where they are.",
        "size_cm: width, depth and height on the head, for reading only. ball_cap_back is ball_cap worn backwards (the same model).",
        "The game never sends this file or a seat's headpiece and color to the AIs. Docs/tasks/T47-build/make_costumes.py builds it from Docs/PropArt/manifest.json.",
    ],
    "headpieces": heads,
}
(HERE / "costumes.json").write_text(json.dumps(costumes, indent=2, ensure_ascii=False) + "\n")

seats_out = {cid: [{"role": r, "headpiece": hp, "color": c, "doc_color": w} for r, hp, c, w in rows] for cid, rows in SEATS.items()}
(HERE / "scenes_seats.json").write_text(json.dumps(seats_out, indent=2, ensure_ascii=False) + "\n")

used = {hp for rows in SEATS.values() for _, hp, _, _ in rows}
assert used <= set(heads), used - set(heads)
meshes = {heads[h]["mesh"] for h in used}
print(f"{len(heads)} headpiece ids ({len(meshes)} models in use), {sum(map(len, SEATS.values()))} seats on {len(SEATS)} cards")
unused = set(FIT) - {h.replace('_back', '') for h in used}
assert not unused, f"headpieces no seat wears: {unused}"

README_ADD = (" Each seat's 'headpiece' (an id in costumes.json) and 'color' (sRGB hex) dress the robot that plays it (T47);"
              " the game never sends them to the AIs.")

if scenes_path.exists():
    # Edit the text, not the parsed JSON: scenes.json is hand-formatted (one line per seat).
    import re
    text = scenes_path.read_text()
    sc = json.loads(text)
    assert [c["id"] for c in sc["cards"]] == list(SEATS), "the cards moved"
    for c in sc["cards"]:
        roles = [s["role"] for s in c["seats"]]
        assert roles == [r for r, *_ in SEATS[c["id"]]], f"{c['id']}: the roles moved: {roles}"
    for cid, rows in SEATS.items():
        for role, hp, col, _ in rows:
            # Matches the seat with or without an earlier run's headpiece and color, so a re-run
            # after a change to SEATS rewrites them in place.
            pat = re.compile(r'(\{ "role": ' + re.escape(json.dumps(role, ensure_ascii=False))
                             + r', "want": "(?:[^"\\]|\\.)*")(?:, "headpiece": "[^"]*", "color": "[^"]*")?( \})')
            text, n = pat.subn(lambda m: f'{m.group(1)}, "headpiece": "{hp}", "color": "{col}"{m.group(2)}', text)
            assert n == 1, f"{cid}: seat {role!r} found {n} times in the one-line form"
    lines = text.split("\n")
    k = [i for i, l in enumerate(lines) if l.startswith('\t\t"cards:')]
    assert len(k) == 1 and lines[k[0]].endswith('",'), "the _readme cards line moved"
    if README_ADD not in lines[k[0]]:
        lines[k[0]] = lines[k[0]][:-2] + README_ADD + '",'
    text = "\n".join(lines)
    out = json.loads(text)
    assert all(s.get("headpiece") in heads and s.get("color") for c in out["cards"] for s in c["seats"])
    if out_scenes:
        out_scenes.write_text(text)
        print(f"scenes.json with costumes -> {out_scenes}")
    else:
        print(f"{scenes_path}: every role matches; pass an output path to write the costumes into it")
