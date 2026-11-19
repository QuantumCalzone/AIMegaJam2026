"""T106 step 4: BP_AudienceBot rebuilt on the generated model.
Root at the bot's feet. New `Body` = SM_AudienceBot (scale 0.842, yaw 270 so the model's front
faces the actor's +X, pivot 80.1 above the feet). The engine shapes it replaces go. The screen is
painted flush on the model (no recess, measured from the GLB), so `Visor` goes too and the eyes sit
on the screen's surface. `Hat` gets the new top hat by default (the house script sets each bot's).
The opera glasses move with the eyes. Run s01 (snapshot) BEFORE this: it records the old bots."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, t106lib
importlib.reload(t106lib)
from t106lib import *

PARENT = 'DefaultSceneRoot'   # name of the root scene component (from s01's bot_template); None = the first scene component
DELETE = ['CapLow', 'BodyLow', 'Seam', 'Head', 'FootL', 'FootR', 'Body', 'Visor']
BODY = {'loc': (0, 0, 80.1), 'yaw': 270.0, 'scale': 0.842}
# In the 160 cm frame, feet at 0, front +X (measured from the GLB: the screen's surface is
# x 35.5 to 36.2 at y ±13, z 120 to 125; the screen spans z 106 to 140, 63 wide).
EYE = {'x': 35.0, 'y': 13.0, 'z': 123.0, 'scale': (0.05, 0.10, 0.10)}
HAT = {'mesh': SET + '/SM_Aud_TopHat', 'loc': (0, 0, 174.0), 'yaw': 270.0, 'scale': 0.517}


def go():
    bp = unreal.load_asset(SET + '/BP_AudienceBot')
    sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    L = unreal.SubobjectDataBlueprintFunctionLibrary
    handles = sds.k2_gather_subobject_data_for_blueprint(bp)
    byname, root = {}, handles[0]   # the first handle is the actor's own (T103 used it as the context)
    for h in handles:
        o = L.get_object(L.get_data(h))
        if o is not None:
            byname[o.get_name().replace('_GEN_VARIABLE', '')] = (h, o)
    before = sorted(byname)
    old_eyes = {n: byname[n][1].get_editor_property('relative_location') for n in ('EyeL', 'EyeR') if n in byname}
    gone = [byname[n][0] for n in DELETE if n in byname]
    if gone:
        sds.delete_subobjects(root, gone, bp)
    # new Body
    par = None
    for hh in sds.k2_gather_subobject_data_for_blueprint(bp):
        o = L.get_object(L.get_data(hh))
        if isinstance(o, unreal.SceneComponent) and (PARENT is None or o.get_name().replace('_GEN_VARIABLE', '') == PARENT):
            par = hh
            break
    h, why = sds.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=par, new_class=unreal.StaticMeshComponent, blueprint_context=bp))
    if not L.is_handle_valid(h):
        raise RuntimeError('add Body failed: %s' % why)
    sds.rename_subobject(h, unreal.Text('Body'))
    body = L.get_object(L.get_data(h))
    body.set_editor_property('static_mesh', unreal.load_asset(SET + '/SM_AudienceBot'))
    body.set_editor_property('relative_location', unreal.Vector(*BODY['loc']))
    body.set_editor_property('relative_rotation', unreal.Rotator(roll=0, pitch=0, yaw=BODY['yaw']))
    s = BODY['scale']
    body.set_editor_property('relative_scale3d', unreal.Vector(s, s, s))
    no_collision(body)
    # eyes, glasses, hat
    handles = sds.k2_gather_subobject_data_for_blueprint(bp)
    cur = {}
    for hh in handles:
        o = L.get_object(L.get_data(hh))
        if o is not None:
            cur[o.get_name().replace('_GEN_VARIABLE', '')] = o
    new_eyes = {}
    for n, sign in (('EyeL', -1), ('EyeR', 1)):
        if n not in cur:
            continue
        # keep each eye on the side it was on
        if n in old_eyes and old_eyes[n].y != 0:
            sign = 1 if old_eyes[n].y > 0 else -1
        p = unreal.Vector(EYE['x'], sign * EYE['y'], EYE['z'])
        cur[n].set_editor_property('relative_location', p)
        cur[n].set_editor_property('relative_scale3d', unreal.Vector(*EYE['scale']))
        new_eyes[n] = p
    # the opera glasses sit 10 in front of their eye (as on T49's bot). (Moving them by the eye's change
    # read 0: get_editor_property returned the live vector, already moved.)
    for g, e in (('GlassL', 'EyeL'), ('GlassR', 'EyeR')):
        if g in cur and e in new_eyes:
            p = new_eyes[e]
            cur[g].set_editor_property('relative_location', unreal.Vector(p.x + 10.0, p.y, p.z))
    if 'Hat' in cur:
        hat = cur['Hat']
        hat.set_editor_property('static_mesh', unreal.load_asset(HAT['mesh']))
        hat.set_editor_property('relative_location', unreal.Vector(*HAT['loc']))
        hat.set_editor_property('relative_rotation', unreal.Rotator(roll=0, pitch=0, yaw=HAT['yaw']))
        hs = HAT['scale']
        hat.set_editor_property('relative_scale3d', unreal.Vector(hs, hs, hs))
        hat.set_material(0, unreal.load_asset(MATS + '/MI_Aud_TopHat'))
    for o in cur.values():
        if isinstance(o, unreal.PrimitiveComponent):
            no_collision(o)
    unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    EAL.save_asset(SET + '/BP_AudienceBot', only_if_is_dirty=False)
    after = {n: {'loc': v3(o.get_editor_property('relative_location')), 'scale': v3(o.get_editor_property('relative_scale3d'), 3),
                 'mesh': (o.static_mesh.get_path_name() if isinstance(o, unreal.StaticMeshComponent) and o.static_mesh else None)}
             for n, o in cur.items() if isinstance(o, unreal.SceneComponent)}
    return {'before': before, 'deleted': [n for n in DELETE if n in byname], 'after': after}


run('s04_audbot', go)
