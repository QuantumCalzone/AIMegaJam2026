"""T86: a full house. Places more rows of stalls and audience bots in L_Stage.

Run it in the editor with L_Stage open, from the console box:
    py "<repo>/Docs/tasks/T86-build/stalls_more.py"

It is re-runnable: it first destroys every actor under FOLDER (and only
those), then places everything again from the numbers below, with a fixed
random seed, so each run gives the same house. T49's own pieces under
Stage/Theater/Opera/Stalls and .../Audience are never touched; the bots this
script adds to T49's row (row A) live under FOLDER too.

It does not save. Save the level yourself (and nothing else) when it looks right.
"""
import random
import unreal

FOLDER = "Stage/Theater/Opera/StallsMore"
SEED = 86

FLOOR_Z = -110.0          # top of HouseFloor
SEAT_SCALE = (0.14, 0.82, 0.75)   # T49's seat back on the 100 cm engine cube
SEAT_H = 75.0
BOT_DX = 18.0             # a bot sits this far in front of (stage side of) its seat back
BOT_DZ = 26.0             # its root above the row's floor (T49: -84 on a -110 floor)

# Rows from the stage toward the house camera. x is the seat back's center.
# Each row behind T49's is raised (a raked house), on a dark deck, so the
# rows hide the floor between them from the camera's steep angle.
ROWS = [
    # name, x, rise, seat ys
    ("B", -570.0, 14.0, [y * 100.0 for y in range(-6, 7)]),   # 13 seats
    ("C", -670.0, 28.0, [y * 100.0 for y in range(-5, 6)]),   # 11 seats
    ("D", -770.0, 42.0, [y * 100.0 for y in range(-4, 5)]),   # 9 seats
]
FILL = 0.8                # share of new seats with a bot
ROW_A = ("A", -470.0, 0.0)  # T49's row: its empty seats that get a bot
ROW_A_NEW = [-400.0, -100.0, 200.0, 400.0]

COLORS = ["MI_Clay_AudRose", "MI_Clay_AudPlum", "MI_Clay_AudMustard",
          "MI_Clay_AudBrick", "MI_Clay_AudLilac"]

# Headpieces from costumes.json, refit from the robots' head to the bot's:
# the bot's Hat sits at z 185, scale 0.42 for the top hat, where a robot's is
# z 19.7, scale 0.3787, so K = 0.42 / 0.3787 and the socket is at z 163.
K = 0.42 / 0.3787
SOCKET_Z = 163.0
HATS = {
    # id: (mesh, scale, x, y, z, yaw, weight, color)
    "top_hat":       ("SM_TopHat",      0.3787,   0.0, 0.0, 19.7, 270, 50, "MI_Clay_Charcoal"),
    "fedora":        ("SM_Fedora",      0.4505,   0.0, 0.0,  9.8, 270, 12, "MI_Clay_Black"),
    "wide_brim_hat": ("SM_WideBrimHat", 0.4732,   0.0, 0.0,  7.8, 270,  8, "MI_Clay_Charcoal"),
    "beanie":        ("SM_Beanie",      0.4182,   0.0, 0.0, 23.8, 270, 10, "MI_Clay_Knit"),
    "ball_cap_back": ("SM_BallCap",     0.6021, -20.0, 0.0, 12.9,  90,  6, "MI_Clay_Denim"),
    "none":          (None,             0.0,      0.0, 0.0,  0.0,   0, 14, None),
}
GLASSES = 0.2             # share of bots with opera glasses up
LEAN = 0.2                # share of bots leaning toward a neighbor
LEAN_DEG = 8.0
YAW_DEG = 15.0
SCALE_MIN, SCALE_MAX = 0.37, 0.43
# Shadows on rows B to D (T86 step 5). Off: only the shadowless glow lights
# them, so their shadows showed nothing and cost about 1 ms of GPU time.
# The bots added to T49's row keep their shadows, like their neighbors.
CAST_SHADOWS = False

# Light. FrontWash's beam falls on the rows near the camera and made them
# brighter than T49's row. So rows B to D use lighting channel 1 only: no
# stage light reaches them. A faint glow on channel 1 alone, from the stage
# side, rims their domes and hat brims. It lights nothing on channel 0, so it
# can't reach the stage, the robots or T49's pieces. It casts no shadow.
OWN_CHANNEL = True

# Rows B to D are seen only from behind, over a seat back, so a bot's face,
# feet and lower body never show. Hiding them takes about two thirds of the
# draws away (step 5). Opera glasses face the stage too, so only row A has them.
BACK_ONLY_HIDE = ["CapLow", "BodyLow", "Seam", "Visor", "EyeL", "EyeR", "FootL", "FootR"]
GLOW = {"loc": (-380.0, 0.0, 180.0), "rot": (-40.0, 180.0, 0.0),  # pitch, yaw, roll
        "intensity": 250.0, "radius": 1300.0, "inner": 50.0, "outer": 80.0,
        "color": (255, 214, 170)}

MAT = "/Game/NHOS/Stage/Materials/"
CUBE = unreal.load_asset("/Engine/BasicShapes/Cube")
VELVET = unreal.load_asset(MAT + "MI_Theater_Velvet")
DECK_MAT = unreal.load_asset(MAT + "MI_Theater_Black")
BOT_CLASS = unreal.EditorAssetLibrary.load_blueprint_class("/Game/NHOS/Stage/Set/BP_AudienceBot")

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
rng = random.Random(SEED)
_mats = {}


def mat(name):
    if name not in _mats:
        _mats[name] = unreal.load_asset(MAT + name)
    return _mats[name]


def clear():
    gone = 0
    for a in eas.get_all_level_actors():
        if str(a.get_folder_path()).startswith(FOLDER):
            eas.destroy_actor(a)
            gone += 1
    return gone


def no_collision(comp):
    comp.set_collision_profile_name("NoCollision")
    comp.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    comp.set_editor_property("can_character_step_up_on", unreal.CanBeCharacterBase.ECB_NO)


def cube(label, folder, loc, scale, material):
    a = eas.spawn_actor_from_object(CUBE, unreal.Vector(*loc), unreal.Rotator(0, 0, 0))
    a.set_actor_label(label)
    a.set_folder_path(folder)
    a.set_actor_scale3d(unreal.Vector(*scale))
    c = a.static_mesh_component
    c.set_material(0, material)
    no_collision(c)
    c.set_cast_shadow(CAST_SHADOWS)
    return a


def comp(actor, name):
    for c in actor.get_components_by_class(unreal.StaticMeshComponent):
        if c.get_name() == name:
            return c
    return None


def pick_hat():
    total = sum(h[6] for h in HATS.values())
    r = rng.uniform(0, total)
    for hid, h in HATS.items():
        r -= h[6]
        if r <= 0:
            return hid
    return "top_hat"


def bot_color(actor):
    c = comp(actor, "Head")
    m = c.get_material(0) if c else None
    return m.get_name() if m else None


def place_bot(label, folder, x, y, floor_top, color, lean_sign, back_only=False):
    yaw = rng.uniform(-YAW_DEG, YAW_DEG)
    roll = lean_sign * rng.uniform(LEAN_DEG * 0.6, LEAN_DEG) if lean_sign else 0.0
    loc = unreal.Vector(x, y + rng.uniform(-4, 4), floor_top + BOT_DZ)
    a = eas.spawn_actor_from_class(BOT_CLASS, loc, unreal.Rotator(roll=roll, pitch=0.0, yaw=yaw))
    a.set_actor_label(label)
    a.set_folder_path(folder)
    s = rng.uniform(SCALE_MIN, SCALE_MAX)
    a.set_actor_scale3d(unreal.Vector(s, s, s))
    for n in ("Seam", "Body", "Head"):
        comp(a, n).set_material(0, mat(color))
    hid = pick_hat()
    hat = comp(a, "Hat")
    mesh, hs, hx, hy, hz, hyaw, _, hcol = HATS[hid]
    if mesh is None:
        hat.set_visibility(False)
    else:
        hat.set_static_mesh(unreal.load_asset("/Game/NHOS/Stage/Headpieces/" + mesh))
        hat.set_relative_location(unreal.Vector(hx * K, hy * K, SOCKET_Z + hz * K), False, False)
        hat.set_relative_rotation(unreal.Rotator(0.0, 0.0, float(hyaw)), False, False)
        hat.set_relative_scale3d(unreal.Vector(hs * K, hs * K, hs * K))
        hat.set_material(0, mat(hcol))
    glasses = rng.random() < GLASSES
    if back_only:
        for n in BACK_ONLY_HIDE:
            comp(a, n).set_visibility(False)
    elif glasses:
        comp(a, "GlassL").set_visibility(True)
        comp(a, "GlassR").set_visibility(True)
    return a, hid


def own_channel(actor):
    for c in actor.get_components_by_class(unreal.PrimitiveComponent):
        c.set_lighting_channels(False, True, False)
        if not CAST_SHADOWS:
            c.set_cast_shadow(False)


def place_glow():
    g = GLOW
    a = eas.spawn_actor_from_class(unreal.SpotLight, unreal.Vector(*g["loc"]),
                                   unreal.Rotator(roll=g["rot"][2], pitch=g["rot"][0], yaw=g["rot"][1]))
    a.set_actor_label("SM_HouseGlow")
    a.set_folder_path(FOLDER + "/Light")
    c = a.get_component_by_class(unreal.SpotLightComponent)
    c.set_editor_property("intensity_units", unreal.LightUnits.CANDELAS)
    c.set_intensity(g["intensity"])
    c.set_attenuation_radius(g["radius"])
    c.set_inner_cone_angle(g["inner"])
    c.set_outer_cone_angle(g["outer"])
    c.set_light_color(unreal.LinearColor(g["color"][0] / 255.0, g["color"][1] / 255.0, g["color"][2] / 255.0, 1.0))
    c.set_cast_shadows(False)
    c.set_editor_property("lighting_channels", unreal.LightingChannels(channel0=False, channel1=True, channel2=False))
    return a


def choose_color(avoid):
    options = [c for c in COLORS if c not in avoid]
    return rng.choice(options or COLORS)


def run():
    gone = clear()
    report = {"destroyed": gone, "rows": {}}

    # Colors already seated, by (row, y), so neighbors never match.
    seated = {}
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("AudStall"):
            seated[("A", round(a.get_actor_location().y))] = bot_color(a)

    # Row A: fill some of T49's empty seats.
    name, bx, rise = ROW_A
    folder = FOLDER + "/RowA"
    for y in ROW_A_NEW:
        avoid = {seated.get((name, round(y - 100))), seated.get((name, round(y + 100)))}
        col = choose_color(avoid)
        lean = 0
        if rng.random() < LEAN:
            lean = rng.choice([-1, 1])
        place_bot("SMA_Aud%+04d" % int(y / 100), folder, bx + BOT_DX, y, FLOOR_Z + rise, col, lean)
        seated[(name, round(y))] = col
    report["rows"]["A"] = {"bots_added": len(ROW_A_NEW)}

    prev = "A"
    for name, bx, rise, ys in ROWS:
        folder = FOLDER + "/Row" + name
        top = FLOOR_Z + rise
        # Deck under the raised row: from 30 behind the seat back to 70 in front.
        span = (max(ys) - min(ys)) + 82.0 + 60.0
        deck_h = rise + 2.0
        deck = cube("SM%s_Deck" % name, folder, (bx + 20.0, 0.0, FLOOR_Z - 2.0 + deck_h / 2.0),
             (1.0, span / 100.0, deck_h / 100.0), DECK_MAT)
        if OWN_CHANNEL:
            own_channel(deck)
        # Seats, then bots: about FILL of them, never three empty in a row.
        filled = [rng.random() < FILL for _ in ys]
        for i in range(2, len(ys)):
            if not filled[i] and not filled[i - 1] and not filled[i - 2]:
                filled[i - 1] = True
        n_bots = 0
        for i, y in enumerate(ys):
            seat = cube("SM%s_Seat%+04d" % (name, int(y / 100)), folder, (bx, y, top + SEAT_H / 2.0), SEAT_SCALE, VELVET)
            if OWN_CHANNEL:
                own_channel(seat)
            if not filled[i]:
                continue
            avoid = {seated.get((name, round(y - 100))), seated.get((prev, round(y)))}
            col = choose_color(avoid)
            lean = 0
            if rng.random() < LEAN:
                left = filled[i - 1] if i > 0 else False
                right = filled[i + 1] if i + 1 < len(ys) else False
                sides = [s for s, ok in ((-1, left), (1, right)) if ok]
                lean = rng.choice(sides) if sides else 0
            bot, hid = place_bot("SM%s_Aud%+04d" % (name, int(y / 100)), folder, bx + BOT_DX, y, top, col, lean, back_only=True)
            if OWN_CHANNEL:
                own_channel(bot)
            seated[(name, round(y))] = col
            n_bots += 1
        report["rows"][name] = {"seats": len(ys), "bots": n_bots}
        prev = name
    if OWN_CHANNEL:
        place_glow()
    unreal.log("T86 STALLSMORE " + str(report))
    return report


run()
