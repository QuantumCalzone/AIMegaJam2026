"""Imports the UI fonts as FontFace assets. Font import needs the Slate UI, so the commandlet cannot do it.

Run with the full editor (it quits itself when done):
  UnrealEditor.exe <PROJECT> -ExecutePythonScript="<this file>" -unattended -nosplash
"""
import os
import unreal

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
eal = unreal.EditorAssetLibrary

for name, ttf in (("FF_Slackey", "Slackey-Regular.ttf"), ("FF_Englebert", "Englebert-Regular.ttf")):
    if eal.does_asset_exist("/Game/UI/Fonts/" + name):
        unreal.log(name + " exists, skipping")
        continue
    task = unreal.AssetImportTask()
    task.filename = os.path.join(REPO, "Art", "Fonts", ttf)
    task.destination_path = "/Game/UI/Fonts"
    task.destination_name = name
    task.factory = unreal.FontFileImportFactory()
    task.automated = True
    task.save = True
    task.replace_existing = True
    asset_tools.import_asset_tasks([task])
    unreal.log("Imported " + name)

unreal.SystemLibrary.execute_console_command(None, "QUIT_EDITOR")
