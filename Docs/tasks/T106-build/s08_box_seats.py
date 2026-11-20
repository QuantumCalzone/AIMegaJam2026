"""T114: the box audience sits in real box seats. Run after s05 (which places the boxes and the box bots on the
ledge), from the editor's Cmd box: py "<repo>/Docs/tasks/T106-build/s08_box_seats.py". Re-runnable: it destroys only
its own folder (FOLDER, which s05's clear() also removes) and places everything again from the numbers below. It
moves the eight box bots (AudBox00..07, s05's) but keeps each one's color, hat and glasses. It does not save.

Each box (SM_Set_TheaterBox at s05's BOX numbers) is a niche whose balcony is a flat slab with no rail: its top is
at mesh z -40 and its curved front edge is RIM below (mesh frame at scale 1, from the GLB; T114.md has how). This
script stands a parapet on that edge (a dark wood panel, gold balusters on its face, gold mouldings and a crimson
velvet top rail), puts a chair behind it for each bot, seats each bot in its chair, lowered so the parapet hides
its body below the shoulders, turned toward the stage, and hangs a warm lamp under the box's arch.

Box space below is the box's mesh frame times the box's scale (1.27 wide, 0.904 deep), in cm: x across the box,
y out of its front, z up from its pivot."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, t106lib
importlib.reload(t106lib)
from t106lib import *

FOLDER = 'Stage/Theater/Opera/T106/BoxSeats'
BOXES = ['Box-1_0', 'Box-1_1', 'Box+1_0', 'Box+1_1']   # s05's labels
BOX_SCALE = (1.27, 0.904)
FLOOR = -40.0      # the slab's top, mesh z
# the slab top's front edge, mesh frame at scale 1: (|x|, y)
RIM = [(0.0, 84.6), (10.0, 84.0), (20.0, 80.8), (30.0, 75.6), (40.0, 67.4), (50.0, 54.5), (60.0, 37.0), (70.0, 15.7)]
PATH_X = [-69.0, -62.0, -53.0, -42.0, -29.0, -15.0, 0.0, 15.0, 29.0, 42.0, 53.0, 62.0, 69.0]   # parapet vertices, mesh x
# chunky, not spindly (Docs/Design/ArtInspiration.md): fat turned balusters, each a shaft with a ball on it
PAR = {'inset': 4.0, 'thick': 4.0, 'h': 30.0, 'sink': 2.0,            # panel: front face this far inside the rim
       'rail_r': 5.5, 'rail_up': 3.0,                                # velvet rail: centre this far above the panel top
       'gold_r': 2.2, 'baluster_r': 2.6, 'baluster_step': 12.0, 'baluster_out': 2.6,
       'ball_r': 4.4, 'ball_at': 0.38}                               # the ball: its radius, and its height up the shaft (0..1)
SEATS = [(-30.0, 30.0), (30.0, 30.0)]   # each bot's place in box space (x, y); a bot keeps its side of the box
BOT_SHOW = (27.0, 34.0)   # how much of a bot shows above the rail's top (its head and shoulders), cm: lower, upper tier
#                           (the house camera is level with the upper tier's rail, so a little more shows there)
TARGET = (-200.0, 0.0)   # the bots look here: the front of the stage, centre
TURN_JITTER = [4.0, -5.0, 3.0, -3.0, 5.0, -4.0, -2.0, 4.0]   # degrees, per bot, so they don't turn in step
CHAIR = {'scale': (0.55, 0.5), 'back_top': 47.0, 'behind': 6.0}  # back top this far above the bot's pivot; pivot this far behind the bot
# a warm lamp hanging under each box's arch, so the house sees a lit box with people in it, not a dark hole
LAMP = {'at': (0.0, 24.0, 46.0), 'candela': 5.0, 'radius': 230.0, 'color': (255, 196, 140), 'source_r': 3.0,
        'bulb': 6.0, 'rod_top': 62.0, 'rod_r': 0.5}
SEAT_H0 = 188.6      # SM_Set_StallsSeat's height at scale 1 (pivot at its centre)

CUBE = unreal.load_asset('/Engine/BasicShapes/Cube')
SPHERE = unreal.load_asset('/Engine/BasicShapes/Sphere')
CYL = unreal.load_asset('/Engine/BasicShapes/Cylinder')
_m = {}


def mat(n):
    if n not in _m:
        _m[n] = unreal.load_asset(MATS + '/' + n)
    return _m[n]


def rot2(x, y, yaw):
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    return x * c - y * s, x * s + y * c


def rim_y(ax):
    ax = abs(ax)
    for (x0, y0), (x1, y1) in zip(RIM, RIM[1:]):
        if ax <= x1:
            return y0 + (y1 - y0) * (ax - x0) / (x1 - x0)
    return RIM[-1][1]


def place(label, mesh, loc, yaw=0.0, scale=(1, 1, 1), material=None, shadow=True, pitch=0.0):
    a = eas().spawn_actor_from_object(mesh, unreal.Vector(*loc), unreal.Rotator(roll=0.0, pitch=pitch, yaw=yaw))
    a.set_actor_label(label)
    a.set_folder_path(FOLDER)
    a.set_actor_scale3d(unreal.Vector(*scale))
    c = a.static_mesh_component
    if material is not None:
        for i in range(c.get_num_materials()):
            c.set_material(i, material)
    no_collision(c)
    c.set_cast_shadow(shadow)
    return a


def lamp(box, tag):
    a = eas().spawn_actor_from_class(unreal.PointLight, unreal.Vector(*box.w(*LAMP['at'])), unreal.Rotator(0, 0, 0))
    a.set_actor_label('%s_Lamp' % tag)
    a.set_folder_path(FOLDER)
    lc = a.point_light_component
    lc.set_editor_property('intensity_units', unreal.LightUnits.CANDELAS)
    lc.set_intensity(LAMP['candela'])
    lc.set_attenuation_radius(LAMP['radius'])
    lc.set_light_color(unreal.LinearColor(*[c / 255.0 for c in LAMP['color']], 1.0))
    lc.set_cast_shadows(False)
    lc.set_editor_property('source_radius', LAMP['source_r'])
    x, y, z = LAMP['at']
    b = LAMP['bulb']
    place('%s_LampBulb' % tag, SPHERE, box.w(x, y, z), 0.0, (b / 100, b / 100, b / 100), mat('MI_FootGlow'), shadow=False)
    h = LAMP['rod_top'] - (z + b / 2)
    place('%s_LampRod' % tag, CYL, box.w(x, y, z + b / 2 + h / 2), 0.0, (LAMP['rod_r'] / 50, LAMP['rod_r'] / 50, h / 100),
          mat('MI_Theater_Gold'), shadow=False)


def clear():
    gone = 0
    for a in eas().get_all_level_actors():
        if str(a.get_folder_path()).startswith(FOLDER):
            eas().destroy_actor(a)
            gone += 1
    return gone


class Box:
    def __init__(self, actor):
        self.a = actor
        l = actor.get_actor_location()
        self.loc = (l.x, l.y, l.z)
        self.yaw = actor.get_actor_rotation().yaw

    def w(self, x, y, z):
        """box space -> world"""
        dx, dy = rot2(x, y, self.yaw)
        return (self.loc[0] + dx, self.loc[1] + dy, self.loc[2] + z)

    def local(self, wx, wy):
        """world -> box space (x, y)"""
        return rot2(wx - self.loc[0], wy - self.loc[1], -self.yaw)


def path_points():
    pts = [(x * BOX_SCALE[0], rim_y(x) * BOX_SCALE[1]) for x in PATH_X]
    segn = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        segn.append((-(y1 - y0) / L, (x1 - x0) / L))   # outward: the segment's direction turned +90
    out = []
    for i, (x, y) in enumerate(pts):
        ns = [segn[j] for j in (i - 1, i) if 0 <= j < len(segn)]
        nx, ny = sum(n[0] for n in ns), sum(n[1] for n in ns)
        L = math.hypot(nx, ny)
        out.append((x - nx / L * PAR['inset'], y - ny / L * PAR['inset']))
    return out


def parapet(box, tag, rep):
    P = path_points()
    t, h, z0 = PAR['thick'], PAR['h'], FLOOR - PAR['sink']
    ztop = FLOOR + h
    zr = ztop + PAR['rail_up']
    g = PAR['gold_r']
    r = PAR['rail_r']
    n = 0
    carry = 0.0
    for i, ((x0, y0), (x1, y1)) in enumerate(zip(P, P[1:])):
        L = math.hypot(x1 - x0, y1 - y0)
        dx, dy = (x1 - x0) / L, (y1 - y0) / L
        nx, ny = -dy, dx
        wyaw = math.degrees(math.atan2(dy, dx)) + box.yaw
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        cx, cy = mx - nx * t / 2, my - ny * t / 2   # the panel's centre line
        place('%s_Panel%02d' % (tag, i), CUBE, box.w(cx, cy, (z0 + ztop) / 2), wyaw, ((L + 0.6) / 100, t / 100, (ztop - z0) / 100),
              mat('MI_Theater_WoodDark'))
        place('%s_Rail%02d' % (tag, i), CYL, box.w(cx, cy, zr), wyaw, (r / 50, r / 50, L / 100), mat('MI_Theater_Velvet'), pitch=90.0)
        gx, gy = mx + nx * g * 0.5, my + ny * g * 0.5
        place('%s_Gold%02d' % (tag, i), CYL, box.w(gx, gy, ztop - g), wyaw, (g / 50, g / 50, (L + 0.6) / 100),
              mat('MI_Theater_Gold'), pitch=90.0)
        place('%s_Base%02d' % (tag, i), CYL, box.w(gx, gy, FLOOR + g), wyaw, (g / 50, g / 50, (L + 0.6) / 100),
              mat('MI_Theater_Gold'), pitch=90.0)
        n += 4
        # balusters between the two mouldings, evenly spaced along the whole path
        s = PAR['baluster_step'] - carry
        bz0, bz1 = FLOOR + 2 * g, ztop - 2 * g
        br = PAR['baluster_r']
        while s < L:
            bx = x0 + dx * s + nx * PAR['baluster_out']
            by = y0 + dy * s + ny * PAR['baluster_out']
            place('%s_Bal%02d_%02d' % (tag, i, int(s)), CYL, box.w(bx, by, (bz0 + bz1) / 2), 0.0, (br / 50, br / 50, (bz1 - bz0) / 100),
                  mat('MI_Theater_Gold'), shadow=False)
            k = PAR['ball_r']
            place('%s_BalBall%02d_%02d' % (tag, i, int(s)), SPHERE, box.w(bx, by, bz0 + (bz1 - bz0) * PAR['ball_at']), 0.0,
                  (k / 50, k / 50, k / 50 * 0.85), mat('MI_Theater_Gold'), shadow=False)
            n += 2
            s += PAR['baluster_step']
        carry = L - (s - PAR['baluster_step'])
    for i, (x, y) in enumerate(P):
        # a velvet ball at each joint of the rail and at its two ends, on the panels' centre line
        nb = [P[j] for j in (i - 1, i + 1) if 0 <= j < len(P)]
        ax = sum(q[0] for q in nb) / len(nb) - x
        ay = sum(q[1] for q in nb) / len(nb) - y
        L = math.hypot(ax, ay) or 1.0
        place('%s_RailJoint%02d' % (tag, i), SPHERE, box.w(x + ax / L * t / 2, y + ay / L * t / 2, zr), 0.0, (r / 50, r / 50, r / 50),
              mat('MI_Theater_Velvet'))
        n += 1
    rep['parapet_actors'] = rep.get('parapet_actors', 0) + n
    return zr + r   # the rail's top, box space


def box_bots(boxes):
    """Each box's bots (s05's AudBox actors), matched to the nearest box."""
    out = {b.a.get_actor_label(): [] for b in boxes}
    for a in eas().get_all_level_actors():
        if a.get_actor_label().startswith('AudBox'):
            l = a.get_actor_location()
            best = min(boxes, key=lambda b: (b.loc[0] - l.x) ** 2 + (b.loc[1] - l.y) ** 2 + (b.loc[2] - l.z) ** 2)
            out[best.a.get_actor_label()].append(a)
    return out


def seat(box, tag, bots, rail_top, rep):
    rows = []
    bots = sorted(bots, key=lambda a: box.local(a.get_actor_location().x, a.get_actor_location().y)[0])
    for k, a in enumerate(bots[:len(SEATS)]):
        sx, sy = SEATS[k] if len(bots) > 1 else (0.0, SEATS[0][1])
        wx, wy, _ = box.w(sx, sy, 0.0)
        idx = int(a.get_actor_label()[6:])
        yaw = math.degrees(math.atan2(TARGET[1] - wy, TARGET[0] - wx)) + TURN_JITTER[idx % len(TURN_JITTER)]
        pz = box.loc[2] + rail_top - BOT_SHOW[1 if tag.endswith('_1') else 0]
        a.set_actor_location_and_rotation(unreal.Vector(wx, wy, pz), unreal.Rotator(roll=0.0, pitch=0.0, yaw=yaw), False, False)
        # the chair behind it, facing the same way (the seat model faces +X at yaw 270)
        fx, fy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        hs = (pz + CHAIR['back_top'] - (box.loc[2] + FLOOR)) / SEAT_H0
        cx, cy = wx - fx * CHAIR['behind'], wy - fy * CHAIR['behind']
        place('%s_Chair%d' % (tag, k), unreal.load_asset(SET + '/SM_Set_StallsSeat'), (cx, cy, box.loc[2] + FLOOR + SEAT_H0 * hs / 2),
              yaw + 270.0, (CHAIR['scale'][0], CHAIR['scale'][1], hs))
        rows.append({'bot': a.get_actor_label(), 'loc': [round(wx, 1), round(wy, 1), round(pz, 1)], 'yaw': round(yaw, 1), 'chair_h': round(hs, 3)})
    rep.setdefault('bots', {})[tag] = rows


def go():
    rep = {'destroyed': clear()}
    boxes = []
    for lab in BOXES:
        for a in eas().get_all_level_actors():
            if a.get_actor_label() == lab:
                boxes.append(Box(a))
    rep['boxes'] = len(boxes)
    bots = box_bots(boxes)
    top = None
    for b in boxes:
        tag = b.a.get_actor_label().replace('Box', 'BoxSeat')
        top = parapet(b, tag, rep)
        seat(b, tag, bots[b.a.get_actor_label()], top, rep)
        if LAMP['candela'] > 0:
            lamp(b, tag)
    rep['rail_top_box_z'] = round(top, 1) if top is not None else None
    return rep


run('s08_box_seats', go)
