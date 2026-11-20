"""Editor Python (run in the editor, through the console box): records the game's own sound in PIE.

    py "<abs>/ue_audio.py" start <out_dir> <name>     starts recording the main submix of the PIE world
    py "<abs>/ue_audio.py" stop  <out_dir> <name>     writes <out_dir>/<name>.wav

Each call writes <out_dir>/<name>.<verb>.json with the wall-clock time (time.time()) at the call, so the
driver (record.py) can lay the sound under the picture: ffmpeg stamps every frame with the same clock.

Why the submix: it holds only this game's sound, with nothing from other apps or other editors, and it
needs no loopback device (this PC has no Stereo Mix). The PIE window's size is set by record.py, through
the editor's PlayIn settings (LevelEditorPlaySettings is not exposed to Python). "au.DisableAppVolume 1" keeps the game audible
(and so recorded) when its window is not in front: the engine's UnfocusedVolumeMultiplier is 0.
"""
import json
import os
import sys
import time

import unreal  # UAudioMixerBlueprintLibrary is unreal.AudioMixerLibrary in Python


def game_world():
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
    if world is None:
        raise RuntimeError("no PIE world: start PIE first")
    return world


def note(out_dir, name, verb, **extra):
    os.makedirs(out_dir, exist_ok=True)
    data = {"verb": verb, "time": time.time(), **extra}
    with open(os.path.join(out_dir, f"{name}.{verb}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f)
    unreal.log(f"T113 AUDIO {verb} {name} {data['time']:.3f}")


def main(argv):
    verb = argv[0]
    out_dir, name = argv[1], argv[2]
    if verb == "start":
        world = game_world()
        unreal.SystemLibrary.execute_console_command(world, "au.DisableAppVolume 1")
        # The engine's red on-screen notes (for example "Video memory has been exhausted" while several
        # editors share the GPU) would land in the shot.
        unreal.SystemLibrary.execute_console_command(world, "DisableAllScreenMessages")
        unreal.AudioMixerLibrary.start_recording_output(world, 600.0)
        note(out_dir, name, "start")
    elif verb == "stop":
        world = game_world()
        t = time.time()
        unreal.AudioMixerLibrary.stop_recording_output(
            world, unreal.AudioRecordingExportType.WAV_FILE, name, out_dir.replace("\\", "/").rstrip("/") + "/")
        note(out_dir, name, "stop", called=t)
    else:
        raise ValueError(f"unknown verb {verb}")


main(sys.argv[1:])
