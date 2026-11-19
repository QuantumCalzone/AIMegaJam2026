"""T106 step 2: import the 12 approved GLBs into /Game/NHOS/Stage/Set (T103's way: AssetImportTask
through Interchange, into a temp folder, then renamed). Keeps BaseColor and Normal, deletes the
importer's materials and the metallic-roughness map, turns Nanite off, removes collision, sets the
texture settings, and reports each mesh's bounds against the size it should have at scale 1.
Expected frame (T103 decision 1): x100, +Z up, the model's front (glTF +Z) on mesh +Y, glTF X on mesh X.
Set ONLY to a list of piece folders to (re)import just those."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, t106lib
importlib.reload(t106lib)
from t106lib import *

# piece folder -> asset name, max texture size (0 = keep 2048)
PIECES = {
    'chandelier_model':   ('Set_Chandelier', 0),
    'cherub_robot_model': ('Set_Cherub', 0),
    'wall_pilaster':      ('Set_PilasterCapital', 0),
    'theater_box':        ('Set_TheaterBox', 0),
    'side_curtain':       ('Set_SideCurtain', 0),
    'valance':            ('Set_Valance', 0),
    'prop_table':         ('Set_PropTable', 1024),
    'stalls_seat':        ('Set_StallsSeat', 1024),
    'footlight':          ('Set_Footlight', 1024),
    'audience_bot':       ('AudienceBot', 0),
    'top_hat':            ('Aud_TopHat', 1024),
    'bowler_hat':         ('Aud_Bowler', 1024),
}
ONLY = None


def no_nanite(mesh):
    ns = mesh.get_editor_property('nanite_settings')
    ns.set_editor_property('enabled', False)
    try:
        unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem).set_nanite_settings(mesh, ns, True)
    except Exception:
        mesh.set_editor_property('nanite_settings', ns)


def strip_collision(mesh):
    sme = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
    try:
        sme.remove_collisions(mesh)
    except Exception:
        pass
    bs = mesh.get_editor_property('body_setup')
    if bs:
        try:
            bs.set_editor_property('collision_trace_flag', unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AS_COMPLEX)
        except Exception:
            pass


def tex_settings(t, kind, max_size):
    if kind == 'Normal':
        t.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_NORMALMAP)
        t.set_editor_property('srgb', False)
        t.set_editor_property('flip_green_channel', True)
    else:
        t.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_DEFAULT)
        t.set_editor_property('srgb', True)
    if max_size:
        t.set_editor_property('max_texture_size', max_size)


def import_piece(folder, name, max_size):
    tmp = SET + '/_imp/' + folder
    t = unreal.AssetImportTask()
    t.filename = ART + folder + '/model.glb'
    t.destination_path = tmp
    t.automated = True
    t.save = False
    t.replace_existing = True
    AT.import_asset_tasks([t])
    objs = [str(p).split('.')[0] for p in t.get_editor_property('imported_object_paths')]
    res = {'objs': objs}
    meshes, tex, other = [], {}, []
    for o in objs:
        a = unreal.load_asset(o)
        if isinstance(a, unreal.StaticMesh):
            meshes.append(o)
        elif isinstance(a, unreal.Texture2D):
            n = o.rsplit('/', 1)[1].lower()
            k = 'Normal' if 'normal' in n else ('BaseColor' if ('diffuse' in n or 'base' in n) else 'MR')
            tex[k] = o
        else:
            other.append(o)
    if len(meshes) != 1:
        raise RuntimeError('%s: %d meshes imported (%s)' % (folder, len(meshes), meshes))
    # keep the importer's normal-map flags as found, for the record (open question 8)
    if 'Normal' in tex:
        nt = unreal.load_asset(tex['Normal'])
        res['normal_as_imported'] = {'flip_green': nt.get_editor_property('flip_green_channel'),
                                     'srgb': nt.get_editor_property('srgb'),
                                     'compression': str(nt.get_editor_property('compression_settings'))}
    kept = {}
    for k in ('BaseColor', 'Normal'):
        if k in tex:
            dst = '%s/T_%s_%s' % (SET, name, k)
            if EAL.does_asset_exist(dst):
                EAL.delete_asset(dst)
            EAL.rename_asset(tex[k], dst)
            tx = unreal.load_asset(dst)
            tex_settings(tx, k, max_size)
            kept[k] = dst
    dstm = '%s/SM_%s' % (SET, name)
    if EAL.does_asset_exist(dstm):
        EAL.delete_asset(dstm)
    EAL.rename_asset(meshes[0], dstm)
    m = unreal.load_asset(dstm)
    no_nanite(m)
    strip_collision(m)
    # the importer's materials and the MR map go; the slots get M_SetModel instances in step 3
    for o in other + ([tex['MR']] if 'MR' in tex else []):
        try:
            EAL.delete_asset(o)
        except Exception as e:
            res.setdefault('delete_failed', []).append(o + ': ' + str(e))
    b = m.get_bounding_box()
    res.update({'mesh': dstm, 'tex': kept, 'tris': m.get_num_triangles(0), 'slots': len(m.static_materials),
                'nanite': m.get_editor_property('nanite_settings').get_editor_property('enabled'),
                'bmin': v3(b.min), 'bmax': v3(b.max)})
    for a in [dstm] + list(kept.values()):
        EAL.save_asset(a, only_if_is_dirty=False)
    return res


def orientation_check():
    """Chandelier candle tip at glTF-derived (58.0, 16.3, 14.7)/1.057 (mesh frame, cm, scale 1):
    compare the nearest vertex distance to it and to its X-mirror. The smaller one says how X maps."""
    m = unreal.load_asset(SET + '/SM_Set_Chandelier')
    try:
        sec = unreal.ProceduralMeshLibrary.get_section_from_static_mesh(m, 0, 0)
        verts = sec[0]
    except Exception as e:
        return 'no vertex read: ' + str(e)
    p = unreal.Vector(58.0 / 1.057, 16.3 / 1.057, 14.7 / 1.057)
    q = unreal.Vector(-p.x, p.y, p.z)
    r = unreal.Vector(p.x, -p.y, p.z)
    d = lambda a: round(min((v - a).length() for v in verts), 2)
    return {'as_expected': d(p), 'x_mirrored': d(q), 'y_mirrored': d(r), 'nverts': len(verts)}


def go():
    out = {}
    for folder, (name, mx) in PIECES.items():
        if ONLY and folder not in ONLY:
            continue
        out[folder] = import_piece(folder, name, mx)
    if EAL.does_directory_exist(SET + '/_imp'):
        EAL.delete_directory(SET + '/_imp')
    out['_orientation'] = orientation_check()
    return out


run('s02_import', go)
