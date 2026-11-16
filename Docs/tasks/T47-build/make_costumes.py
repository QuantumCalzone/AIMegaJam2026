"""Build the T47 costume drafts. Run from the repo root:

    python Docs/tasks/T47-build/make_costumes.py [path/to/scenes.json]

Writes, next to this script:
  costumes.json      the draft of Content/NHOS/Data/costumes.json: each headpiece's mesh and its
                     fit on the robot's HeadSocket, computed from Docs/PropArt/manifest.json
                     (fit.bounds_cm) and T79's shared round head (see HEAD below).
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

# T79's shared round head (OpenAI, Anthropic, SpaceXAI), in Rig space (cm), from T79-build.md part 2:
# an ellipsoid with radii 33 (deep, x), 35 (wide, y), 31 (tall, z) around z 127, so it runs from z 96
# to 158. HeadSocket sits on its top, at (0, 0, 158), scale 1. The screen (Visor) shows from about
# z 118 to 147 at the middle; the eyes' centers are at z 135 (12 cm tall, so z 129 to 141), the brows
# at z 144 to 145, the mouth at z 123 (it stretches to 118.5 to 127.5). The ear pods stand out to
# y +-38 at z 118 to 138. Anthropic's glasses stand out to x 35.8 and the eyes to x 38. The antenna
# stalk (Nub) runs from z 156 to 180, as on T46.
# Rule for every piece but the shades: nothing covers the eyes (front edge above z 141) or the mouth;
# a wig's bangs may cover the brows (Docs/BotArt.md: "the mouth always shows").
HEAD_TOP = 158.0
EYE_FRONT_X = 40.0  # the shades' front: in front of Anthropic's glasses (x 35.8) and the eyes (x 38)

# The fit of each headpiece, set by hand from the manifest's bounds (the shapes inside the boxes
# were not seen). width: the model's width across the face in cm (raw X, since every Meshy model faces
# raw +Y); bottom: where its lowest point sits, in Rig z on the round head (it is written out relative
# to HeadSocket); x: toward the face (+) or the back (-); y: to the robot's left (+) or right (-);
# lifts: whether the stalk and the toppers rise so they poke out of its top. look: why a close-up must
# check it first (T47-build.md part 5c); None if the numbers follow plainly from the head.
FIT = {
    #                  width  bottom    x     y     lifts  look
    "top_hat":         (72,  150.0,   0.0,  0.0,  True,  None),  # filled underside: rests on the crown, brim 5 cm over the brows
    "wide_brim_hat":   (90,  150.0,   0.0,  0.0,  True,  None),
    "fedora":          (80,  150.0,   0.0,  0.0,  True,  None),
    "wizard_hat":      (80,  150.0,   0.0,  0.0,  True,  None),
    "ball_cap":        (74,  143.0,  20.0,  0.0,  True,  "raised 8 cm: on T46's head its bill sat at z 135, which is now the eye line"),
    "beanie":          (68,  142.0,   0.0,  0.0,  True,  "raised 12 cm off the eyes and narrowed from 76 to 68, so it doesn't stand 74 cm over the head"),
    "tiara":           (56,  146.0,   0.0,  0.0,  False, "raised 6 cm off the eyes and narrowed to the head's width there (55 cm); a front-only arc would need x about 22"),
    "saucepan_helmet": (89,  145.0,   0.0, 17.7,  True,  "the pot (54 cm of the 89; the raw pot is 115 of 190.2) rests where the head is 54 cm across, its front rim at z 145; y moves the pot, not the handle, over the head: if the pot sits off to one side, negate y"),
    "bob_wig":         (84,   92.0,  -4.0,  0.0,  True,  "the fringe should end over the brows (about z 145) and the sides may show the ear pods"),
    "hood":            (110,  52.0,  -4.0,  0.0,  True,  "the face opening must frame the screen (z 118 to 147)"),
    "dino_hood":       (84,  113.0,  10.0,  0.0,  True,  "the snout and the open jaw must leave the eyes and the mouth showing"),
    "horned_helmet_beard": (85, 88.0, 4.0,  0.0,  True,  "raised 20 cm with the face: the helmet's rim above the eyes (z 141), the beard below the mouth (z 118)"),
    "dark_shades":     (72,  124.0,  None,  0.0,  False, "on the eyes (z 129 to 141) and clear of the mouth (z 124 and down); the temples rest on the ear pods; SpaceXAI's nose comes out under them"),
}
FRONT_YAW = 270  # turns a Meshy model (face at raw +Y) to the robot's face at Rig +X

# Per-persona overrides, for a head whose HeadSocket alone doesn't make a piece fit (T80's Meta and my
# box head). Each entry: {persona id: {any of scale, x, y, z, top}}, in HeadSocket space, replacing the
# headpiece's own value on that robot. Empty until T80's findings or T47's close-ups say otherwise.
ON = {
    # "dark_shades": {"copycat": {"z": -20.0}},
    # T83: my Hyper3D box head is shallower (front at x 23.4, not 28) and its eye slots sit lower (z 134.7,
    # not 138), so the shades come 4 cm back and 4.5 cm down on my box to cover the slots.
    "dark_shades": {"human": {"x": -4.4, "z": -24.6}},
}
PERSONAS = {"visionary", "worrier", "overclocker", "copycat", "human"}

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
heads, looks = {}, {}
for hid, (width, bottom, x, y, lifts, look) in FIT.items():
    a = manifest[hid]
    assert a["kind"] == "headpiece", hid
    fit = a["fit"]
    pkg = fit["asset"]
    assert (ROOT / ("Content" + pkg[len("/Game"):] + ".uasset")).exists(), pkg
    bx, by, bz = fit["bounds_cm"]
    s = width / bx
    h, depth = bz * s, by * s
    if x is None:  # sits on the face: its front at EYE_FRONT_X
        x = EYE_FRONT_X - depth / 2
    top = bottom + h
    heads[hid] = {
        "mesh": f"{pkg}.{pkg.rsplit('/', 1)[1]}",
        "scale": round(s, 4),
        "x": round(x, 1),
        "y": round(y, 1),
        "z": round(bottom - fit["min_z"] * s - HEAD_TOP, 1),  # the mesh pivot is its center: z = bottom + h/2, from HeadSocket
        "yaw": FRONT_YAW,
        "top": round(top - HEAD_TOP, 1) if lifts else 0.0,
        "size_cm": [round(width), round(depth), round(h)],
    }
    if look:
        looks[hid] = look
# The eldest son's cap, backwards: the same model turned round, its bill over the back.
heads["ball_cap_back"] = dict(heads["ball_cap"], yaw=(FRONT_YAW + 180) % 360, x=-heads["ball_cap"]["x"])
looks["ball_cap_back"] = looks["ball_cap"]
for hid, per in ON.items():
    assert hid in heads and set(per) <= PERSONAS, (hid, per)
    assert all(set(v) <= {"scale", "x", "y", "z", "top"} for v in per.values()), per
    heads[hid]["on"] = per

costumes = {
    "_readme": [
        "The headpieces the robots wear (T47). Each seat in scenes.json names one by its id ('headpiece') and gives its color ('color', sRGB hex).",
        "mesh: the static mesh's object path, loaded by BP_Robot.SetHeadpiece as a soft reference. Every headpiece model has MI_Clay_Neutral on its slots, and SetHeadpiece sets its Color.",
        "scale, x, y, z, yaw: the Hat component's relative transform under the robot's HeadSocket (cm, degrees), sized for the shared round head (T79). The face is +X; yaw 270 turns a model's face to it. T80 placed and scaled Meta's and my box's HeadSocket so the same numbers fit there.",
        "top: the headpiece's top above HeadSocket, in cm. The antenna stalk, the toppers and the name label rise so they poke out of it. 0 leaves them where they are (the tiara and the shades).",
        "on: optional, {persona id: {any of scale, x, y, z, top}}, which replaces those numbers on that robot only, for a head the socket alone doesn't fit.",
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
print(f"to look at first in the editor: {', '.join(sorted(looks))}")

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
