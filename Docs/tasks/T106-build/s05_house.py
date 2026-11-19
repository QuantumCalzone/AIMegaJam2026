"""T106 step 5: the house, placed by one re-runnable script.
Destroys only what it placed (everything under FOLDER) plus the old parts named in DELETE (gone
after the first run), then places every piece again from the numbers below. Every audience bot is
re-placed from OUT/snapshot.json (s01, frozen before the bot was rebuilt): same place, turn, lean,
scale, glasses, its color on the new MI_Aud_*, its hat as the new top hat or bowler.
It does not save. Stop PIE first (T86: get_all_level_actors is empty while PIE runs).

Mesh frame after import (T103, checked by s02): front = mesh +Y, so yaw 90 faces the house (-X),
yaw 270 faces the stage (+X). Actor scale is (width, depth, height)."""
import sys, os, json, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, t106lib
importlib.reload(t106lib)
from t106lib import *

FOLDER = 'Stage/Theater/Opera/T106'
SNAP = json.load(open(OUT + 'snapshot.json'))
SEED = 106

# ---- fill these from s01_inventory.full.json before the first run -------------------------
DELETE = (['CurtainL%d' % i for i in range(7)] + ['CurtainR%d' % i for i in range(7)] + ['Valance', 'ValanceFringe']
          + ['FootHood%d' % i for i in range(9)] + ['FootBulb%d' % i for i in range(9)]
          + ['PropTableCloth', 'PropTableTop', 'Chandelier', 'CherubPlinthL', 'CherubPlinthR', 'CherubL', 'CherubR',
             'BoxL0', 'BoxL1', 'BoxR0', 'BoxR1'] + ['Seat%02d' % i for i in range(13)])
DELETE_PREFIX = ['SMB_Seat', 'SMC_Seat', 'SMD_Seat']
RISER = ['Riser', 'RiserStep']   # T17's gold RiserTrim stays as it is
LIGHTS = {}
FLOOR_Z = -110.0
STAGE_TOP = 0.0
OLD_TABLE = 'PropTableTop'
OLD_CHANDELIER = 'Chandelier'
OLD_HOODS = ['FootHood%d' % i for i in range(9)]
OLD_PLINTHS = ['CherubPlinthL', 'CherubPlinthR']
# -----------------------------------------------------------------------------------------

CH = {'xy': (-500.0, 0.0), 'yaw': 90.0, 'scale': 1.057, 'chain_top': 900.0}
# candle tips, mesh frame at scale 1.057, cm (from the GLB); flames sit 3 cm above
TIPS = [(58.0, 16.3, 14.7), (43.7, 40.2, 14.4), (20.2, 57.6, 14.5), (-6.8, 59.5, 14.6), (-34.5, 47.3, 14.3),
        (-56.5, 20.5, 14.8), (-56.9, -13.1, 14.4), (-43.5, -39.5, 14.4), (-21.0, -56.8, 14.8), (8.3, -58.0, 14.6),
        (35.4, -45.1, 14.6), (56.4, -18.1, 14.6)]
CHERUB = {'x': -243.0, 'y': 495.0, 'turn': 20.0, 'scale': 0.342, 'plinth': (55.0, 55.0, 60.0),
          'eyes': [(-4.0, 15.0, 47.0), (4.0, 15.0, 47.0)], 'eye_scale': 0.035}   # eyes: mesh frame at 0.342, guess: check a close-up
BOX = {'x': -450.0, 'y': 600.0, 'tiers': (152.0, 342.0), 'yaw_off': 65.0, 'w': 1.27,
       'bots': [(-28.0, 35.0, -38.0), (28.0, 35.0, -38.0)]}   # bots on the balcony, mesh frame at scale 1 (GLB)
PILASTERS = [(-280.0, -570.0, 0.0), (-280.0, 570.0, 180.0)]  # boards on the proscenium columns' inner faces (y +-580), the faces the house camera sees
# (x, y, yaw) of each shaft's front-face centre on the side walls, from the inventory
PIL = {'shaft': (80.0, 10.0, 600.0), 'base': 0.0, 'cap_scale': (0.422, 0.162, 0.422), 'cap_h': 52.0, 'relief_step': 120.0, 'reliefs': 4, 'cap_fwd': 5.0}
CURTAIN = {'x': -195.0, 'y': 534.0, 'scale': 3.263, 'pivot': 310.6}  # x, y from the old pleats
VALANCE = {'x': -250.0, 'z': 400.0, 'scale': (6.128, 0.556, 4.111)}   # 1160 wide: fits between the columns    # z: its pivot; bottom = z - 90
TABLE = {'xy': (300.0, 300.0), 'w': 0.631, 'd': 0.673, 'h0': 0.965, 'top0': 40.4, 'height0': 80.0}
FOOT = {'scale': 0.14, 'pivot': 13.2, 'glow': (0.0, 2.0, -3.0), 'glow_d': 13.0}
SEAT = {'scale': (0.705, 0.691, 0.408), 'pivot': 38.4, 'rear': 35.0, 'cushion': 31.0}
OLD_BACK_HALF = 7.0    # T49's seat-back cube was 14 deep: its rear face is 7 behind its centre
ROWS = [('A', -470.0, 0.0, [y * 100.0 for y in range(-6, 7)], False),
        ('B', -570.0, 14.0, [y * 100.0 for y in range(-6, 7)], True),
        ('C', -670.0, 28.0, [y * 100.0 for y in range(-5, 6)], True),
        ('D', -770.0, 42.0, [y * 100.0 for y in range(-4, 5)], True)]   # name, back x, rise, ys, own channel
BOT = {'dx': 24.0, 'sink': 4.0}   # bot centre this far in front of the back's centre; feet this far into the cushion
HATS = {'top': (SET + '/SM_Aud_TopHat', 'MI_Aud_TopHat', 174.0, 0.517),
        'bowler': (SET + '/SM_Aud_Bowler', 'MI_Aud_Bowler', 178.0, 0.526)}
HAT_MIX = (0.47, 0.40)  # top hat, bowler; the rest bare (a bot bare before stays bare)
BACK_ONLY_HIDE = ['EyeL', 'EyeR']

CUBE = unreal.load_asset('/Engine/BasicShapes/Cube')
SPHERE = unreal.load_asset('/Engine/BasicShapes/Sphere')
CYL = unreal.load_asset('/Engine/BasicShapes/Cylinder')
BOT_CLASS = unreal.EditorAssetLibrary.load_blueprint_class(SET + '/BP_AudienceBot')
_m = {}


def mat(n):
    if n not in _m:
        _m[n] = unreal.load_asset(MATS + '/' + n)
    return _m[n]


def sm(n):
    return unreal.load_asset(SET + '/' + n)


def snap(label):
    for a in SNAP['actors']:
        if a['label'] == label:
            return a
    raise KeyError(label)


def rot2(x, y, yaw):
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    return x * c - y * s, x * s + y * c


def place(label, sub, mesh, loc, yaw=0.0, scale=(1, 1, 1), material=None, shadow=True, chan1=False, roll=0.0, pitch=0.0):
    a = eas().spawn_actor_from_object(mesh, unreal.Vector(*loc), unreal.Rotator(roll=roll, pitch=pitch, yaw=yaw))
    a.set_actor_label(label)
    a.set_folder_path(FOLDER + '/' + sub)
    a.set_actor_scale3d(unreal.Vector(*scale))
    c = a.static_mesh_component
    if material is not None:
        for i in range(c.get_num_materials()):
            c.set_material(i, material)
    no_collision(c)
    c.set_cast_shadow(shadow)
    if chan1:
        c.set_lighting_channels(False, True, False)
    return a


def clear():
    gone = 0
    dele = set(DELETE)
    for a in eas().get_all_level_actors():
        lab = a.get_actor_label()
        if (str(a.get_folder_path()).startswith(FOLDER) or lab in dele or any(lab.startswith(p) for p in DELETE_PREFIX)
                or a.get_class().get_name() == 'BP_AudienceBot_C'):
            eas().destroy_actor(a)
            gone += 1
    return gone


def chandelier(rep):
    yaw, s = CH['yaw'], CH['scale']
    bottom = snap(OLD_CHANDELIER)['bmin'][2] if OLD_CHANDELIER else 411.0 - 95.0
    z = bottom + 100.5 * s / 1.057
    x, y = CH['xy']
    place('Chandelier', 'Chandelier', sm('SM_Set_Chandelier'), (x, y, z), yaw, (s, s, s), shadow=False)
    k = s / 1.057
    for i, (tx, ty, tz) in enumerate(TIPS):
        dx, dy = rot2(tx * k, ty * k, yaw)
        place('ChandelierFlame%02d' % i, 'Chandelier', SPHERE, (x + dx, y + dy, z + tz * k + 3.0), 0, (0.03, 0.03, 0.05),
              mat('MI_FootGlow'), shadow=False)
    top = z + 99.5 * k
    h = CH['chain_top'] - top
    place('ChandelierChain', 'Chandelier', CYL, (x, y, top + h / 2), 0, (0.04, 0.04, h / 100.0), mat('MI_Theater_Black'), shadow=False)
    rep['chandelier'] = {'pivot_z': round(z, 1), 'bottom': round(bottom, 1)}


def cherubs(rep):
    pw, pd, ph = CHERUB['plinth']
    base = min(snap(l)['bmin'][2] for l in OLD_PLINTHS) if OLD_PLINTHS else STAGE_TOP
    s = CHERUB['scale']
    for side in (-1, 1):
        x, y = CHERUB['x'], CHERUB['y'] * side
        yaw = 90.0 + CHERUB['turn'] * side   # faces the house, turned toward the middle
        place('CherubPlinth%+d' % side, 'Cherubs', CUBE, (x, y, base + ph / 2), yaw, (pw / 100, pd / 100, ph / 100), mat('MI_Theater_WoodDark'))
        z = base + ph + 32.5 * s / 0.342
        place('Cherub%+d' % side, 'Cherubs', sm('SM_Set_Cherub'), (x, y, z), yaw, (s, s, s))
        for j, (ex, ey, ez) in enumerate(CHERUB['eyes']):
            dx, dy = rot2(ex, ey, yaw)
            e = CHERUB['eye_scale']
            place('CherubEye%+d_%d' % (side, j), 'Cherubs', SPHERE, (x + dx, y + dy, z - 32.5 + ez), yaw, (e * 0.5, e, e), mat('MI_Aud_Eye'), shadow=False)
    rep['cherubs'] = {'plinth_base': base}


def boxes(rep, box_bots):
    w = BOX['w']
    spots = []
    for side in (-1, 1):
        yaw = 90.0 + BOX['yaw_off'] * side
        for t, tz in enumerate(BOX['tiers']):
            x, y = BOX['x'], BOX['y'] * side
            place('Box%+d_%d' % (side, t), 'Boxes', sm('SM_Set_TheaterBox'), (x, y, tz), yaw, (w, 0.904, 1.0))
            for bx, by, bz in BOX['bots']:
                dx, dy = rot2(bx * w, by * 0.904, yaw)
                spots.append(((x + dx, y + dy, tz + bz), yaw + 90.0))
    rep['box_spots'] = len(spots)
    return spots


def pilasters(rep):
    """An engine shaft on the wall, and the capital at its top and repeated down its face as reliefs.
    Each (x, y, yaw) is the point on the shaft's front face, at the wall; yaw faces the shaft's front."""
    sw, sd, sh = PIL['shaft']
    cw, cd, chh = PIL['cap_scale']
    for i, (x, y, yaw) in enumerate(PILASTERS):
        bx, by = rot2(0.0, -sd / 2, yaw)          # shaft centre: half its depth behind the face
        z0 = PIL.get('base', FLOOR_Z)
        place('PilShaft%d' % i, 'Pilasters', CUBE, (x + bx, y + by, z0 + sh / 2), yaw, (sw / 100, sd / 100, sh / 100), mat('MI_Theater_WoodDark'))
        fx, fy = rot2(0.0, PIL['cap_fwd'], yaw)   # capital centre this far in front of the face
        for k in range(PIL['reliefs'] + 1):
            zc = z0 + sh - PIL['cap_h'] / 2 - k * PIL['relief_step']
            place('PilCap%d_%d' % (i, k), 'Pilasters', sm('SM_Set_PilasterCapital'), (x + fx, y + fy, zc), yaw, (cw, cd, chh))
    rep['pilasters'] = len(PILASTERS)


def curtains_valance(rep):
    s = CURTAIN['scale']
    for side in (-1, 1):
        place('SideCurtain%+d' % side, 'Drapes', sm('SM_Set_SideCurtain'), (CURTAIN['x'], CURTAIN['y'] * side, STAGE_TOP + CURTAIN['pivot']),
              90.0, (s * side, s, s))
    place('Valance', 'Drapes', sm('SM_Set_Valance'), (VALANCE['x'], 0.0, VALANCE['z']), 90.0, VALANCE['scale'])


def riser(rep):
    for lab in RISER:
        for a in eas().get_all_level_actors():
            if a.get_actor_label() == lab:
                a.static_mesh_component.set_material(0, mat('MI_Theater_WoodDark'))


def table(rep):
    old = snap(OLD_TABLE) if OLD_TABLE else None
    top = old['bmax'][2] if old else STAGE_TOP + 80.0
    hs = TABLE['h0'] * (top - STAGE_TOP) / TABLE['height0']
    z = top - TABLE['top0'] * hs / TABLE['h0']
    place('PropTable', 'Stage', sm('SM_Set_PropTable'), (TABLE['xy'][0], TABLE['xy'][1], z), 90.0, (TABLE['w'], TABLE['d'], hs))
    rep['table'] = {'top': top, 'hscale': round(hs, 3)}


def footlights(rep):
    s = FOOT['scale']
    for i, lab in enumerate(OLD_HOODS):
        o = snap(lab)
        x = (o['bmin'][0] + o['bmax'][0]) / 2
        y = (o['bmin'][1] + o['bmax'][1]) / 2
        z = o['bmin'][2] + FOOT['pivot']
        place('Footlight%d' % i, 'Footlights', sm('SM_Set_Footlight'), (x, y, z), 90.0, (s, s, s))
        gx, gy = rot2(FOOT['glow'][0], FOOT['glow'][1], 90.0)
        d = FOOT['glow_d'] / 100.0
        place('FootBulb%d' % i, 'Footlights', SPHERE, (x + gx, y + gy, z + FOOT['glow'][2]), 0, (d, d, d), mat('MI_FootGlow'), shadow=False)
    rep['footlights'] = len(OLD_HOODS)


def stalls(rep):
    sx, sy, sz = SEAT['scale']
    n = 0
    for name, bx, rise, ys, own in ROWS:
        top = FLOOR_Z + rise
        px = bx - OLD_BACK_HALF + SEAT['rear']   # new back's rear face where the cube's was
        for y in ys:
            place('Seat%s%+04d' % (name, int(y / 100)), 'Stalls/Row' + name, sm('SM_Set_StallsSeat'),
                  (px, y, top + SEAT['pivot']), 270.0, (sx, sy, sz), shadow=not own, chan1=own)
            n += 1
    rep['seats'] = n


def set_bot(a, rec, rng, back_only):
    col = (rec.get('color') or 'MI_Clay_AudRose').replace('MI_Clay_Aud', 'MI_Aud_')
    body = comp_by_name(a, 'Body')
    body.set_material(0, mat(col if col.startswith('MI_Aud_') else 'MI_Aud_Rose'))
    hat = comp_by_name(a, 'Hat')
    if rec.get('hat') is None:
        kind = None
    else:
        r = rng.random()
        kind = 'top' if r < HAT_MIX[0] else ('bowler' if r < HAT_MIX[0] + HAT_MIX[1] else None)
    if kind is None:
        hat.set_visibility(False)
    else:
        mesh, m, z, s = HATS[kind]
        hat.set_static_mesh(unreal.load_asset(mesh))
        hat.set_material(0, mat(m))
        hat.set_relative_location(unreal.Vector(0, 0, z), False, False)
        hat.set_relative_scale3d(unreal.Vector(s, s, s))
    if rec.get('glasses') and not back_only:
        comp_by_name(a, 'GlassL').set_visibility(True)
        comp_by_name(a, 'GlassR').set_visibility(True)
    if back_only:
        for nme in BACK_ONLY_HIDE:
            c = comp_by_name(a, nme)
            if c:
                c.set_visibility(False)
        for c in a.get_components_by_class(unreal.PrimitiveComponent):
            c.set_lighting_channels(False, True, False)
            c.set_cast_shadow(False)
    return col, kind


def bots(rep, box_spots):
    rng = random.Random(SEED)
    rowx = {r[1]: r for r in ROWS}
    stall, box = [], []
    for rec in sorted(SNAP['bots'], key=lambda r: r['label']):
        # a stall bot sits 18 in front of a row's back (T49, T86); anything else is a box bot
        near = min(rowx, key=lambda bx: abs(rec['loc'][0] - 18.0 - bx))
        is_stall = rec['loc'][2] < 0 and abs(rec['loc'][1]) <= 650 and abs(rec['loc'][0] - 18.0 - near) < 30
        (stall if is_stall else box).append((rec, rowx[near]))
    counts = {'top': 0, 'bowler': 0, None: 0}
    for rec, (name, bx, rise, ys, own) in stall:
        roll, pitch, yaw = rec['rot']
        loc = (bx + BOT['dx'], rec['loc'][1], FLOOR_Z + rise + SEAT['cushion'] - BOT['sink'])
        a = eas().spawn_actor_from_class(BOT_CLASS, unreal.Vector(*loc), unreal.Rotator(roll=roll, pitch=pitch, yaw=yaw))
        a.set_actor_label('Aud%s%+04d' % (name, int(round(rec['loc'][1] / 100))))
        a.set_folder_path(FOLDER + '/Audience/Row' + name)
        a.set_actor_scale3d(unreal.Vector(*rec['scale']))
        col, kind = set_bot(a, rec, rng, own)
        counts[kind] += 1
    for i, (rec, _) in enumerate(box):
        if i >= len(box_spots):
            break
        (x, y, z), yaw = box_spots[i]
        roll = rec['rot'][0]
        a = eas().spawn_actor_from_class(BOT_CLASS, unreal.Vector(x, y, z), unreal.Rotator(roll=roll, pitch=0.0, yaw=yaw))
        a.set_actor_label('AudBox%02d' % i)
        a.set_folder_path(FOLDER + '/Audience/Boxes')
        a.set_actor_scale3d(unreal.Vector(*rec['scale']))
        col, kind = set_bot(a, rec, rng, False)
        counts[kind] += 1
    rep['bots'] = {'stalls': len(stall), 'boxes': min(len(box), len(box_spots)), 'box_records': len(box),
                   'hats': {str(k): v for k, v in counts.items()}}


def lights(rep):
    out = {}
    for lab, f in LIGHTS.items():
        base = snap(lab)['light']['intensity']
        for a in eas().get_all_level_actors():
            if a.get_actor_label() == lab:
                lc = a.get_component_by_class(unreal.LightComponent)
                lc.set_intensity(base * f)
                out[lab] = round(base * f, 2)
    rep['lights'] = out


def go():
    rep = {'destroyed': clear()}
    chandelier(rep)
    cherubs(rep)
    spots = boxes(rep, None)
    pilasters(rep)
    curtains_valance(rep)
    riser(rep)
    table(rep)
    footlights(rep)
    stalls(rep)
    bots(rep, spots)
    lights(rep)
    return rep


run('s05_house', go)
