# T105: reimport props over the old assets. Reads Saved/T105/job.json: [{prop, card, asset (CamelCase), fbx, tex}]
import unreal, json, traceback
SAVED = unreal.Paths.project_saved_dir() + "T105/"
job = json.load(open(SAVED + "job.json"))
at = unreal.AssetToolsHelpers.get_asset_tools()
reg = unreal.AssetRegistryHelpers.get_asset_registry()
res = []
def run_task(src, folder, name):
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", src)
    t.set_editor_property("destination_path", folder)
    t.set_editor_property("destination_name", name)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("replace_existing_settings", False)
    t.set_editor_property("automated", True)
    t.set_editor_property("save", False)
    at.import_asset_tasks([t])
    return list(t.get_editor_property("imported_object_paths"))
def assets_in(folder):
    return set(str(a.package_name) for a in reg.get_assets_by_path(folder, recursive=False))
for j in job:
    r = {"prop": j["prop"]}
    try:
        folder = "/Game/NHOS/Stage/Props/" + j["card"]
        A = j["asset"]
        before = assets_in(folder)
        # texture first: replace T_<A>_BaseColor in place (M_<A> keeps its sample)
        r["tex"] = run_task(j["tex"], folder, "T_%s_BaseColor" % A)
        mesh_paths = run_task(j["fbx"], folder, "SM_%s" % A)
        r["mesh_import"] = mesh_paths
        after = assets_in(folder)
        new = sorted(after - before)
        r["new_assets"] = new
        sm = unreal.load_asset("%s/SM_%s" % (folder, A))
        mat = unreal.load_asset("%s/M_%s" % (folder, A))
        if mat is None and j.get("create_mat"):
            # a new prop: copy a sibling's material (one texture sample into Base Color) and point it at the new texture
            mat = unreal.EditorAssetLibrary.duplicate_asset(j["create_mat"], "%s/M_%s" % (folder, A))
            tex = unreal.load_asset("%s/T_%s_BaseColor" % (folder, A))
            node = unreal.MaterialEditingLibrary.get_material_property_input_node(mat, unreal.MaterialProperty.MP_BASE_COLOR)
            node.set_editor_property("texture", tex)
            unreal.MaterialEditingLibrary.recompile_material(mat)
            r["created_mat"] = mat.get_path_name()
        n = sm.get_num_sections(0)
        mats = sm.get_editor_property("static_materials")
        r["slots"] = [str(m.get_editor_property("material_slot_name")) for m in mats]
        if mat:
            for i in range(len(mats)):
                sm.set_material(i, mat)
        # delete what the FBX import made besides the mesh (its material and textures), if nothing else uses them
        dels = []
        for p in new:
            if p.endswith("/SM_" + A) or p.endswith("/T_%s_BaseColor" % A):
                continue
            if j.get("keep_new"):
                continue
            dels.append(p)
        for p in dels:
            unreal.EditorAssetLibrary.delete_asset(p)
        r["deleted"] = dels
        b = sm.get_bounding_box()
        r["bounds"] = [[b.min.x, b.min.y, b.min.z], [b.max.x, b.max.y, b.max.z]]
        r["tris"] = sm.get_num_triangles(0)
        r["mat"] = sm.get_material(0).get_path_name() if sm.get_material(0) else None
    except Exception as e:
        r["error"] = traceback.format_exc()
    res.append(r)
json.dump(res, open(SAVED + "imp_out.json", "w"), indent=1)
