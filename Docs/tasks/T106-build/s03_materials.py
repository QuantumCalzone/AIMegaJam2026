"""T106 step 3: the surfaces.
1. T49's MI_Theater_* instances (on M_Set) updated in place to T98's swatches.
2. A new master M_SetModel (Substrate slab): the model's BaseColor with a palette shift that
   moves up to four key colors onto their swatches, keeping the painted detail; its normal map;
   one roughness; no metal.
3. Its instances: MI_Set_<piece> and the audience's MI_Aud_<Color>, MI_Aud_TopHat, MI_Aud_Bowler,
   each put on its mesh's slots.
The palette shift works in sRGB: keys and targets are stored as sRGB values in the vector
parameters (not linear), and the Custom node converts the texture to sRGB and back."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, t106lib
importlib.reload(t106lib)
from t106lib import *

M_SET = '/Game/NHOS/Stage/M_Set'
REBUILD_MASTER = False   # True deletes and rebuilds M_SetModel (its instances keep their parent path)

# 1. T98's swatches on T49's instances. Colors are linear (the M_Set parameters are linear).
THEATER = {
    'MI_Theater_Velvet':   {'Color': '#9E1B22', 'Rough': 0.8, 'Fuzz': 0.3, 'Metal': 0.0},
    'MI_Theater_Gold':     {'Color': '#D9B24E', 'Rough': 0.55, 'Metal': 0.0, 'ThumbDepth': 0.2, 'ThumbScale': 0.08},
    'MI_Theater_WoodDark': {'Color': '#5A3A22', 'Rough': 0.8, 'Metal': 0.0, 'ThumbDepth': 0.15},
    'MI_Theater_Wood':     {'Color': '#A87E4F', 'Rough': 0.75, 'Metal': 0.0},
    'MI_Theater_Cloth':    {'Color': '#F0E3C4', 'Rough': 0.85, 'Metal': 0.0},
    'MI_Theater_Black':    {'Color': '#17110F', 'Rough': 0.9, 'Metal': 0.0},
}

GOLD, CREAM, WOOD, VELVET = '#D9B24E', '#F0E3C4', '#5A3A22', '#9E1B22'
# 3. instance -> (mesh, rough, [(key, to), ...]) ; keys are sRGB hex measured on the diffuse maps
MODELS = {
    'MI_Set_Chandelier':      ('SM_Set_Chandelier', 0.6, [('#C38444', GOLD), ('#E9D5B0', CREAM)]),
    'MI_Set_Cherub':          ('SM_Set_Cherub', 0.6, [('#CF9B5F', GOLD)]),
    'MI_Set_PilasterCapital': ('SM_Set_PilasterCapital', 0.6, [('#D08A5C', GOLD), ('#B7633E', WOOD)]),
    'MI_Set_TheaterBox':      ('SM_Set_TheaterBox', 0.8, [('#B47E44', WOOD), ('#851C18', VELVET), ('#D5AC73', GOLD), ('#AC4635', VELVET)]),
    'MI_Set_SideCurtain':     ('SM_Set_SideCurtain', 0.8, [('#720F14', VELVET), ('#D79A46', GOLD)]),
    'MI_Set_Valance':         ('SM_Set_Valance', 0.8, [('#871E20', VELVET), ('#F2B85E', GOLD)]),
    'MI_Set_PropTable':       ('SM_Set_PropTable', 0.85, [('#D6C7A8', CREAM)]),
    'MI_Set_StallsSeat':      ('SM_Set_StallsSeat', 0.8, [('#CC414B', VELVET), ('#84523E', WOOD), ('#D69764', GOLD)]),
    'MI_Set_Footlight':       ('SM_Set_Footlight', 0.7, [('#C9945B', GOLD), ('#F4E7C9', CREAM), ('#4C372E', WOOD)]),
    'MI_Aud_TopHat':          ('SM_Aud_TopHat', 0.85, [('#444547', '#17110F'), ('#DF0704', '#7A1E22')]),
    'MI_Aud_Bowler':          ('SM_Aud_Bowler', 0.85, [('#444547', '#17110F'), ('#9F4B3C', '#7A1E22')]),
}
AUD_COLORS = {'Rose': '#C98B8B', 'Plum': '#7E5A7A', 'Mustard': '#C9A43F', 'Brick': '#A65A3E', 'Lilac': '#A89BC9'}
AUD_KEYS = ('#B86752', '#9B4C35', '#E5C8A4')   # body, its shadowed side, the cream belly and pods

WIDTH = 0.25
CODE = """float3 b = pow(saturate(Base.rgb), 1.0/2.2);
float w2 = max(Width*Width, 1e-4);
float3 o = b;
float3 d;
d = b - KeyA.rgb; o += exp(-dot(d,d)/w2) * (ToA.rgb - KeyA.rgb);
d = b - KeyB.rgb; o += exp(-dot(d,d)/w2) * (ToB.rgb - KeyB.rgb);
d = b - KeyC.rgb; o += exp(-dot(d,d)/w2) * (ToC.rgb - KeyC.rgb);
d = b - KeyD.rgb; o += exp(-dot(d,d)/w2) * (ToD.rgb - KeyD.rgb);
return pow(saturate(o), 2.2);"""
SLOTS = ['KeyA', 'ToA', 'KeyB', 'ToB', 'KeyC', 'ToC', 'KeyD', 'ToD']


def pin(names, *want):
    """Find a slab input whose name contains every word in want (case-insensitive)."""
    for n in names:
        s = str(n).lower()
        if all(w in s for w in want):
            return str(n)
    raise RuntimeError('no slab input with %s in %s' % (want, names))


def build_master():
    path = MATS + '/M_SetModel'
    if EAL.does_asset_exist(path):
        if not REBUILD_MASTER:
            return {'master': 'kept'}
        EAL.delete_asset(path)
    m = AT.create_asset('M_SetModel', MATS, unreal.Material, unreal.MaterialFactoryNew())
    E = lambda cls, x, y: MEL.create_material_expression(m, cls, x, y)
    base = E(unreal.MaterialExpressionTextureSampleParameter2D, -1400, -300)
    base.set_editor_property('parameter_name', 'BaseTex')
    base.set_editor_property('texture', unreal.load_asset(SET + '/T_Set_Chandelier_BaseColor'))
    base.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
    nrm = E(unreal.MaterialExpressionTextureSampleParameter2D, -1400, 300)
    nrm.set_editor_property('parameter_name', 'NormalTex')
    nrm.set_editor_property('texture', unreal.load_asset(SET + '/T_Set_Chandelier_Normal'))
    nrm.set_editor_property('sampler_type', unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
    namt = E(unreal.MaterialExpressionScalarParameter, -1100, 500)
    namt.set_editor_property('parameter_name', 'NormalAmount')
    namt.set_editor_property('default_value', 1.0)
    flat = E(unreal.MaterialExpressionConstant3Vector, -1100, 200)
    flat.set_editor_property('constant', unreal.LinearColor(0, 0, 1, 1))
    lerp = E(unreal.MaterialExpressionLinearInterpolate, -800, 300)
    MEL.connect_material_expressions(flat, '', lerp, 'A')
    MEL.connect_material_expressions(nrm, 'RGB', lerp, 'B')
    MEL.connect_material_expressions(namt, '', lerp, 'Alpha')

    cus = E(unreal.MaterialExpressionCustom, -700, -300)
    cus.set_editor_property('description', 'PaletteShift')
    cus.set_editor_property('code', CODE)
    cus.set_editor_property('output_type', unreal.CustomMaterialOutputType.CMOT_FLOAT3)
    ins = []
    for n in ['Base'] + SLOTS + ['Width']:
        ci = unreal.CustomInput()
        ci.set_editor_property('input_name', n)
        ins.append(ci)
    cus.set_editor_property('inputs', ins)
    MEL.connect_material_expressions(base, 'RGB', cus, 'Base')
    for i, n in enumerate(SLOTS):
        p = E(unreal.MaterialExpressionVectorParameter, -1100, -900 + i * 70)
        p.set_editor_property('parameter_name', n)
        p.set_editor_property('default_value', unreal.LinearColor(0, 0, 0, 1))
        MEL.connect_material_expressions(p, '', cus, n)
    w = E(unreal.MaterialExpressionScalarParameter, -1100, -320)
    w.set_editor_property('parameter_name', 'Width')
    w.set_editor_property('default_value', WIDTH)
    MEL.connect_material_expressions(w, '', cus, 'Width')

    rough = E(unreal.MaterialExpressionScalarParameter, -700, 100)
    rough.set_editor_property('parameter_name', 'Rough')
    rough.set_editor_property('default_value', 0.8)

    slab = E(unreal.MaterialExpressionSubstrateSlabBSDF, -300, 0)
    names = MEL.get_material_expression_input_names(slab)
    MEL.connect_material_expressions(cus, '', slab, pin(names, 'albedo'))
    rn = [str(x) for x in names if 'rough' in str(x).lower() and 'second' not in str(x).lower() and 'fuzz' not in str(x).lower()]
    MEL.connect_material_expressions(rough, '', slab, rn[0])
    MEL.connect_material_expressions(lerp, '', slab, [str(x) for x in names if str(x).lower() == 'normal'][0])
    MEL.connect_material_property(slab, '', unreal.MaterialProperty.MP_FRONT_MATERIAL)
    MEL.recompile_material(m)
    EAL.save_asset(path, only_if_is_dirty=False)
    return {'master': 'built', 'slab_inputs': [str(x) for x in names]}


def shade(hx):
    """The body color's shadowed side, darker by the same ratio as the texture's own shade."""
    k, d, h = hex_srgb(AUD_KEYS[0]), hex_srgb(AUD_KEYS[1]), hex_srgb(hx)
    return '#%02X%02X%02X' % tuple(int(round(min(1.0, h[i] * d[i] / k[i]) * 255)) for i in range(3))


def set_vec(mi, name, hexs):
    c = hex_srgb(hexs)
    MEL.set_material_instance_vector_parameter_value(mi, name, unreal.LinearColor(c[0], c[1], c[2], 1.0))


def make_mi(name, mesh, rough, keys, tex_prefix):
    path = MATS + '/' + name
    mi = unreal.load_asset(path) if EAL.does_asset_exist(path) else \
        AT.create_asset(name, MATS, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    MEL.set_material_instance_parent(mi, unreal.load_asset(MATS + '/M_SetModel'))
    MEL.set_material_instance_texture_parameter_value(mi, 'BaseTex', unreal.load_asset(SET + '/T_%s_BaseColor' % tex_prefix))
    MEL.set_material_instance_texture_parameter_value(mi, 'NormalTex', unreal.load_asset(SET + '/T_%s_Normal' % tex_prefix))
    MEL.set_material_instance_scalar_parameter_value(mi, 'Rough', rough)
    MEL.set_material_instance_scalar_parameter_value(mi, 'Width', WIDTH)
    letters = 'ABCD'
    for i in range(4):
        k, t = keys[i] if i < len(keys) else ('#000000', '#000000')
        set_vec(mi, 'Key' + letters[i], k)
        set_vec(mi, 'To' + letters[i], t)
    MEL.update_material_instance(mi)
    EAL.save_asset(path, only_if_is_dirty=False)
    if mesh:
        sm = unreal.load_asset(SET + '/' + mesh)
        for i in range(len(sm.static_materials)):
            sm.set_material(i, mi)
        EAL.save_asset(SET + '/' + mesh, only_if_is_dirty=False)
    return path


def go():
    res = {'theater': {}}
    for name, ps in THEATER.items():
        mi = unreal.load_asset(MATS + '/' + name)
        before = {str(p.parameter_info.name): round(p.parameter_value, 3) for p in mi.scalar_parameter_values}
        for k, v in ps.items():
            if k == 'Color':
                c = hex_lin(v)
                MEL.set_material_instance_vector_parameter_value(mi, 'Color', unreal.LinearColor(c[0], c[1], c[2], 1.0))
            else:
                MEL.set_material_instance_scalar_parameter_value(mi, k, float(v))
        MEL.update_material_instance(mi)
        EAL.save_asset(MATS + '/' + name, only_if_is_dirty=False)
        res['theater'][name] = before
    res.update(build_master())
    res['instances'] = []
    for name, (mesh, rough, keys) in MODELS.items():
        res['instances'].append(make_mi(name, mesh, rough, keys, mesh[3:]))
    for col, hx in AUD_COLORS.items():
        keys = [(AUD_KEYS[0], hx), (AUD_KEYS[1], shade(hx)), (AUD_KEYS[2], CREAM)]
        res['instances'].append(make_mi('MI_Aud_' + col, 'SM_AudienceBot' if col == 'Rose' else None, 0.8, keys, 'AudienceBot'))
    return res


run('s03_materials', go)
