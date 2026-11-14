"""Imports the picked voice lines from Content/Audio/VO into Unreal as SoundWave assets.

voicegen.py writes WAVs straight into Content/Audio/VO/<Actor>/<Name>.wav. Unreal needs them imported as assets
named VO_<Actor>_<Tag>_<NN> so BarkSubsystem can find /Game/Audio/VO/<Actor>/<Name>. This script imports every WAV in
Tools/VoiceGen staging (Art/Voice/final/<Actor>/) that is not already an asset.

Run headless with the editor CLOSED:
  UnrealEditor-Cmd.exe <PROJECT> -run=pythonscript -script="<this file>"
"""
import os
import unreal

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(REPO, "Art", "Voice", "final")
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
eal = unreal.EditorAssetLibrary

tasks = []
for actor in sorted(os.listdir(SRC)) if os.path.isdir(SRC) else []:
    for f in sorted(os.listdir(os.path.join(SRC, actor))):
        if not f.lower().endswith(".wav"):
            continue
        name = os.path.splitext(f)[0]
        if eal.does_asset_exist(f"/Game/Audio/VO/{actor}/{name}"):
            continue
        t = unreal.AssetImportTask()
        t.filename = os.path.join(SRC, actor, f)
        t.destination_path = f"/Game/Audio/VO/{actor}"
        t.destination_name = name
        t.automated = True
        t.save = True
        t.replace_existing = True
        tasks.append(t)

if tasks:
    asset_tools.import_asset_tasks(tasks)
unreal.log(f"Imported {len(tasks)} voice lines")
