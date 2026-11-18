# T105: emissive glow for three props: T_<A>_Glow mask x color x strength -> Emissive Color
import unreal, json, traceback
SAVED = unreal.Paths.project_saved_dir() + "T105/"
P = "/Users/personal/Projects/AIMegaJam2026/Docs/Art/Props/"
MEL = unreal.MaterialEditingLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
jobs = [("space_plans", "glow_stick_sword", "GlowStickSword", (0.55, 1.0, 0.72), 6.0),
        ("mine_bridge", "glowing_staff", "GlowingStaff", (0.85, 0.95, 1.0), 8.0),
        ("glowing_briefcase", "glowing_briefcase", "GlowingBriefcase", (1.0, 0.72, 0.28), 3.0)]
res = []
for card, prop, A, col, k in jobs:
    r = {"prop": prop}
    try:
        folder = "/Game/NHOS/Stage/Props/" + card
        t = unreal.AssetImportTask(); t.filename = P + card + "/" + prop + "/glow.png"
        t.destination_path = folder; t.destination_name = "T_%s_Glow" % A
        t.replace_existing = True; t.automated = True; t.save = False
        at.import_asset_tasks([t])
        tex = unreal.load_asset("%s/T_%s_Glow" % (folder, A))
        tex.set_editor_property("srgb", False)
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_GRAYSCALE)
        m = unreal.load_asset("%s/M_%s" % (folder, A))
        old = MEL.get_material_property_input_node(m, unreal.MaterialProperty.MP_EMISSIVE_COLOR)
        if old is None:
            s = MEL.create_material_expression(m, unreal.MaterialExpressionTextureSample, -600, 300)
            s.set_editor_property("texture", tex)
            s.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_GRAYSCALE)
            c = MEL.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -600, 500)
            c.set_editor_property("constant", unreal.LinearColor(col[0] * k, col[1] * k, col[2] * k, 1))
            mul = MEL.create_material_expression(m, unreal.MaterialExpressionMultiply, -300, 400)
            MEL.connect_material_expressions(s, "R", mul, "A")
            MEL.connect_material_expressions(c, "", mul, "B")
            MEL.connect_material_property(mul, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
        MEL.recompile_material(m)
        r["emissive"] = str(MEL.get_material_property_input_node(m, unreal.MaterialProperty.MP_EMISSIVE_COLOR))
    except Exception:
        r["error"] = traceback.format_exc()
    res.append(r)
# the bowl: a new import came in with Nanite on; the other props have it off
sm = unreal.load_asset("/Game/NHOS/Stage/Props/favor_father/SM_BowlOfOranges")
ns = sm.get_editor_property("nanite_settings"); ns.enabled = False; sm.set_editor_property("nanite_settings", ns)
res.append({"bowl_tris": sm.get_num_triangles(0)})
# the test folder
unreal.EditorAssetLibrary.delete_directory("/Game/T105Tmp")
res.append({"tmp_gone": not unreal.EditorAssetLibrary.does_directory_exist("/Game/T105Tmp")})
json.dump(res, open(SAVED + "glow_out.json", "w"), indent=1)
