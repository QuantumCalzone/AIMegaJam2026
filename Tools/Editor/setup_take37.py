"""One-time editor setup for the Take 37 prototype.

Creates:
  /Game/Materials/M_Greybox   - Color / Emissive / Roughness / Metallic parameters (rebuilt on every run)
  /Game/Data/DT_Barks         - imported from Tools/barks/DT_Barks.csv with row struct FBarkRow
  /Game/Maps/Stage_Take37     - empty level; ATake37GameMode builds the stage at runtime

Fonts need the full editor: run Tools/Editor/import_fonts.py separately (see its header).

Run headless with the editor CLOSED, after the Take37 module is compiled:
  UnrealEditor-Cmd.exe <PROJECT> -run=pythonscript -script="<this file>"

Then set Project Settings > Maps & Modes > Default Maps to /Game/Maps/Stage_Take37.
Safe to re-run: existing assets are left alone (delete them first to regenerate).
"""
import os
import unreal

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV = os.path.join(REPO, "Tools", "barks", "DT_Barks.csv")

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
eal = unreal.EditorAssetLibrary


def make_material():
    """M_Greybox: Color (vector), Emissive (scalar multiplier of Color), Roughness, Metallic. Always rebuilt."""
    path = "/Game/Materials/M_Greybox"
    if eal.does_asset_exist(path):
        eal.delete_asset(path)
    mat = asset_tools.create_asset("M_Greybox", "/Game/Materials", unreal.Material, unreal.MaterialFactoryNew())
    mat.set_editor_property("used_with_skeletal_mesh", True)
    mel = unreal.MaterialEditingLibrary

    def node(cls, x, y):
        return mel.create_material_expression(mat, cls, x, y)

    color = node(unreal.MaterialExpressionVectorParameter, -700, 0)
    color.set_editor_property("parameter_name", "Color")
    color.set_editor_property("default_value", unreal.LinearColor(0.6, 0.6, 0.6, 1.0))

    emissive = node(unreal.MaterialExpressionScalarParameter, -700, 300)
    emissive.set_editor_property("parameter_name", "Emissive")
    emissive.set_editor_property("default_value", 0.0)

    rough = node(unreal.MaterialExpressionScalarParameter, -700, 450)
    rough.set_editor_property("parameter_name", "Roughness")
    rough.set_editor_property("default_value", 0.55)

    metal = node(unreal.MaterialExpressionScalarParameter, -700, 600)
    metal.set_editor_property("parameter_name", "Metallic")
    metal.set_editor_property("default_value", 0.0)

    mul = node(unreal.MaterialExpressionMultiply, -400, 150)
    mel.connect_material_expressions(color, "", mul, "A")
    mel.connect_material_expressions(emissive, "", mul, "B")

    mel.connect_material_property(color, "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(mul, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    mel.connect_material_property(rough, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.connect_material_property(metal, "", unreal.MaterialProperty.MP_METALLIC)
    mel.recompile_material(mat)
    eal.save_loaded_asset(mat)
    unreal.log("Created M_Greybox")


def import_barks():
    path = "/Game/Data/DT_Barks"
    if eal.does_asset_exist(path):
        unreal.log("DT_Barks exists, skipping")
        return
    struct = unreal.load_object(None, "/Script/Take37.BarkRow")
    if struct is None:
        unreal.log_error("FBarkRow not found. Is the Take37 module compiled?")
        return
    factory = unreal.CSVImportFactory()
    factory.automated_import_settings.import_row_struct = struct
    factory.automated_import_settings.import_type = unreal.CSVImportType.ECSV_DATA_TABLE
    task = unreal.AssetImportTask()
    task.filename = CSV
    task.destination_path = "/Game/Data"
    task.destination_name = "DT_Barks"
    task.factory = factory
    task.automated = True
    task.save = True
    task.replace_existing = True
    asset_tools.import_asset_tasks([task])
    unreal.log("Imported DT_Barks from " + CSV)


def make_map():
    path = "/Game/Maps/Stage_Take37"
    if eal.does_asset_exist(path):
        unreal.log("Stage_Take37 exists, skipping")
        return
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if les.new_level(path):
        les.save_current_level()
        unreal.log("Created " + path)
    else:
        unreal.log_error("Could not create " + path + ". Create an empty level by hand and save it there.")


make_material()
import_barks()
make_map()
