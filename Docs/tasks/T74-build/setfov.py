"""T74: set THIS editor's level viewport for a capture. NOT RUN (written by the T74 prep).

Reads Saved/T74/fov.json {"fov": <horizontal degrees for the whole viewport>}, sets the active level
viewport's FOV and Game View (G: hides editor sprites, as the game does), and writes
Saved/T74/fov.done. The 2026-11-15 captures used the same calls (LevelEditorSubsystem).
"""
import json
import os

import unreal

WORK = os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir()), "T74")
spec = json.load(open(os.path.join(WORK, "fov.json"), encoding="utf-8"))
les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
key = les.get_active_viewport_config_key()
if not les.editor_get_game_view():
    les.editor_set_game_view(True)
les.set_level_viewport_fov(spec["fov"], key)
json.dump({"fov": les.get_level_viewport_fov(key), "game_view": les.editor_get_game_view()},
          open(os.path.join(WORK, "fov.done"), "w", encoding="utf-8"))
