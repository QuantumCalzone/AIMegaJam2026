"""T106 step 1 (read only): what L_Stage holds before the rebuild.
Writes OUT/s01_inventory.json and, the first time only, a frozen copy OUT/snapshot.json that
the house script rebuilds the audience from (every bot's place, turn, lean, scale, color, hat,
glasses). Never re-freeze it after the house script has run: set FREEZE=True only on purpose."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, t106lib
importlib.reload(t106lib)
from t106lib import *

FREEZE = not os.path.exists(OUT + 'snapshot.json')


def mesh_info(c):
    d = {'name': c.get_name(), 'class': c.get_class().get_name(),
         'rel_loc': v3(c.get_editor_property('relative_location')),
         'rel_rot': r3(c.get_editor_property('relative_rotation')),
         'rel_scale': v3(c.get_editor_property('relative_scale3d'), 3),
         'visible': c.is_visible()}
    if isinstance(c, unreal.StaticMeshComponent):
        m = c.static_mesh
        d['mesh'] = m.get_path_name() if m else None
        d['mats'] = [(x.get_path_name() if x else None) for x in c.get_materials()]
        d['shadow'] = c.cast_shadow
        lc = c.get_editor_property('lighting_channels')
        d['chan'] = [lc.channel0, lc.channel1, lc.channel2]
        try:
            o, e = c.bounds.origin, c.bounds.box_extent
            d['wb'] = [round(o.z - e.z, 1), round(o.z + e.z, 1)]
        except Exception:
            pass
    return d


def actor_info(a):
    o, e = a.get_actor_bounds(False)
    d = {'label': a.get_actor_label(), 'name': a.get_name(), 'class': a.get_class().get_name(),
         'folder': str(a.get_folder_path()), 'loc': v3(a.get_actor_location()),
         'rot': r3(a.get_actor_rotation()), 'scale': v3(a.get_actor_scale3d(), 3),
         'bmin': v3(o - e), 'bmax': v3(o + e), 'hidden': a.is_hidden_ed()}
    comps = a.get_components_by_class(unreal.StaticMeshComponent)
    if len(comps) == 1:
        d.update({k: v for k, v in mesh_info(comps[0]).items() if k in ('mesh', 'mats', 'shadow', 'chan')})
    elif comps:
        d['comps'] = [mesh_info(c) for c in comps]
    for cls in (unreal.LightComponent,):
        for lc in a.get_components_by_class(cls):
            d['light'] = {'class': lc.get_class().get_name(), 'intensity': lc.intensity,
                          'color': [round(lc.light_color.r), round(lc.light_color.g), round(lc.light_color.b)],
                          'shadows': lc.cast_shadows}
            try:
                d['light']['radius'] = lc.attenuation_radius
                d['light']['cones'] = [lc.inner_cone_angle, lc.outer_cone_angle]
            except Exception:
                pass
    cam = a.get_component_by_class(unreal.CameraComponent)
    if cam:
        d['fov'] = cam.field_of_view
    return d


def bot_record(a, info):
    """What the house script needs to put a new bot where this one is."""
    by = {c['name']: c for c in info.get('comps', [])}
    color = None
    for n in ('Head', 'Body', 'Seam'):
        if n in by and by[n].get('mats'):
            color = by[n]['mats'][0].rsplit('.', 1)[-1]
            break
    hat = by.get('Hat', {})
    hat_mesh = hat.get('mesh').rsplit('.', 1)[-1] if hat.get('mesh') and hat.get('visible') else None
    lows = [c['wb'][0] for n, c in by.items() if 'wb' in c and n not in ('Hat', 'GlassL', 'GlassR') and c.get('visible')]
    feet = min(lows) if lows else None
    # lows of hidden parts too (rows B-D hide the feet): from the template feet offset, filled below
    allows = [c['wb'][0] for n, c in by.items() if 'wb' in c and n in ('FootL', 'FootR')]
    return {'label': info['label'], 'folder': info['folder'], 'loc': info['loc'], 'rot': info['rot'],
            'scale': info['scale'], 'color': color, 'hat': hat_mesh,
            'glasses': bool(by.get('GlassL', {}).get('visible')),
            'feet_z': min(allows) if allows else feet,
            'hidden_parts': [n for n, c in by.items() if not c.get('visible')],
            'chan': by.get('Body', by.get('Head', {})).get('chan'),
            'shadow': by.get('Body', by.get('Head', {})).get('shadow')}


def params(path):
    m = unreal.load_asset(path)
    if m is None:
        return None
    d = {'class': m.get_class().get_name()}
    if isinstance(m, unreal.MaterialInstanceConstant):
        d['parent'] = m.parent.get_path_name() if m.parent else None
        d['scalars'] = {str(p.parameter_info.name): round(p.parameter_value, 4) for p in m.scalar_parameter_values}
        d['vectors'] = {str(p.parameter_info.name): [round(p.parameter_value.r, 4), round(p.parameter_value.g, 4), round(p.parameter_value.b, 4)] for p in m.vector_parameter_values}
        d['textures'] = {str(p.parameter_info.name): (p.parameter_value.get_path_name() if p.parameter_value else None) for p in m.texture_parameter_values}
    else:
        d['scalars'] = [str(x) for x in MEL.get_scalar_parameter_names(m)]
        d['vectors'] = [str(x) for x in MEL.get_vector_parameter_names(m)]
        d['textures'] = [str(x) for x in MEL.get_texture_parameter_names(m)]
        d['statics'] = [str(x) for x in MEL.get_static_switch_parameter_names(m)]
    return d


def refs(path):
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    pkg = path.split('.')[0]
    o = unreal.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True,
                                              include_searchable_names=False, include_soft_management_references=False,
                                              include_hard_management_references=False)
    return [str(x) for x in (ar.get_referencers(pkg, o) or [])]


def go():
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    res = {'map': world.get_path_name(), 'actors': [], 'bots': [], 'folders': {}}
    for a in eas().get_all_level_actors():
        info = actor_info(a)
        f = info['folder']
        res['folders'][f] = res['folders'].get(f, 0) + 1
        if info['class'] == 'BP_AudienceBot_C':
            info['comps'] = [mesh_info(c) for c in a.get_components_by_class(unreal.StaticMeshComponent)]
            res['bots'].append(bot_record(a, info))
            continue
        res['actors'].append(info)
    # the audience bot's template
    bp = unreal.load_asset(SET + '/BP_AudienceBot')
    sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    tmpl = []
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        o = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
        if isinstance(o, unreal.SceneComponent):
            tmpl.append(mesh_info(o))
    res['bot_template'] = tmpl
    # materials and their referencers
    mats = ['MI_Theater_' + n for n in ('Velvet', 'Gold', 'WoodDark', 'Wood', 'Cloth', 'Black', 'Gunmetal')]
    res['theater_mi'] = {n: params(MATS + '/' + n) for n in mats}
    res['masters'] = {p: params(p) for p in ('/Game/NHOS/Stage/M_Set', MATS + '/M_Clay', MATS + '/M_CastModel')}
    res['glows'] = {n: params(MATS + '/' + n) for n in ('MI_FootGlow', 'MI_FireGlow', 'MI_Aud_Screen', 'MI_Aud_Eye')}
    check = [SET + '/' + n for n in ('SM_Chandelier', 'SM_Cherub', 'SM_TheaterBox', 'M_Chandelier', 'M_Cherub', 'M_TheaterBox',
                                     'T_Chandelier_BaseColor', 'T_Cherub_BaseColor', 'T_TheaterBox_BaseColor')]
    check += [MATS + '/' + n for n in ('MI_Clay_AudRose', 'MI_Clay_AudPlum', 'MI_Clay_AudMustard', 'MI_Clay_AudBrick', 'MI_Clay_AudLilac',
                                       'MI_Clay_Charcoal', 'MI_Clay_Black', 'MI_Clay_Knit', 'MI_Clay_Denim', 'MI_Theater_Gunmetal')]
    res['referencers'] = {p.rsplit('/', 1)[1]: refs(p) for p in check}
    if FREEZE:
        json.dump({'bots': res['bots'], 'bot_template': tmpl,
                   'actors': [a for a in res['actors'] if a['folder'].startswith('Stage')]},
                  open(OUT + 'snapshot.json', 'w'), indent=1)
    res['froze_snapshot'] = FREEZE
    json.dump(res, open(OUT + 's01_inventory.full.json', 'w'), indent=1, default=str)
    return {'actors': len(res['actors']), 'bots': len(res['bots']), 'folders': res['folders'], 'froze': FREEZE}


run('s01_inventory', go)
