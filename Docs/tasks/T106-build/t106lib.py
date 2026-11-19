"""T106 helpers shared by the step scripts. Run the steps from the editor's Cmd box:
    py "<repo>/Docs/tasks/T106-build/<step>.py"
Each step writes its result to Saved/T106/out/<step>.json (or .err.txt), so nothing big
comes back through MCP."""
import json, os, traceback, time
import unreal

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')) + '/'
OUT = ROOT + 'Saved/T106/out/'
ART = ROOT + 'Docs/Art/Set/'
SET = '/Game/NHOS/Stage/Set'
MATS = '/Game/NHOS/Stage/Materials'
os.makedirs(OUT, exist_ok=True)

EAL = unreal.EditorAssetLibrary
MEL = unreal.MaterialEditingLibrary
AT = unreal.AssetToolsHelpers.get_asset_tools()


def eas():
    return unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def v3(v, n=1):
    return [round(v.x, n), round(v.y, n), round(v.z, n)]


def r3(r, n=1):
    return [round(r.roll, n), round(r.pitch, n), round(r.yaw, n)]


def run(name, fn):
    """Run fn(), write OUT/name.json with its result, or OUT/name.err.txt with the trace."""
    t = time.time()
    err = OUT + name + '.err.txt'
    if os.path.exists(err):
        os.remove(err)
    try:
        res = fn()
        json.dump({'ok': True, 'secs': round(time.time() - t, 1), 'result': res},
                  open(OUT + name + '.json', 'w'), indent=1, default=str)
        unreal.log('T106 %s OK' % name)
    except Exception:
        open(err, 'w').write(traceback.format_exc())
        unreal.log_error('T106 %s FAILED, see %s' % (name, err))


def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_lin(h):
    h = h.lstrip('#')
    return tuple(srgb_to_lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def hex_srgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def no_collision(comp):
    comp.set_collision_profile_name('NoCollision')
    comp.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    comp.set_editor_property('can_character_step_up_on', unreal.CanBeCharacterBase.ECB_NO)


def comp_by_name(actor, name):
    for c in actor.get_components_by_class(unreal.SceneComponent):
        if c.get_name() == name:
            return c
    return None
