"""T99: reimports the approved 2D art over its textures, so every reference stays. Run inside the editor: type
py "<absolute path to this file>" into the console box. It writes Saved/T99/import.json. Each texture keeps its settings (sRGB, compression, mips, group), because the import replaces the
source data only. Pass a group name in GROUPS to do part of it; it saves what it imported and prints one line each."""
import json
import unreal

ROOT = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
ART = ROOT + "Docs/Art/2D/"
JOBS = {
    "backdrops": [(ART + "backdrops/%s.png" % i, "/Game/NHOS/Stage/Backdrops", "T_Backdrop_" + i)
                  for i in ("desert_planet", "dwarf_mine", "jungle_park", "garden_wedding", "retro_diner",
                            "bowling_lanes", "midnight_cubicles")],
    "stagehand": [(ART + "stagehand/portrait_256.png", "/Game/NHOS/UI/Stagehand", "T_Stagehand_Portrait")],
    "moneyburn": [(ART + "moneyburn/" + f, "/Game/NHOS/UI/MoneyBurn", t) for f, t in (
        ("bill.png", "T_Bill"), ("bill_char.png", "T_BillChar"), ("flame_sheet.png", "T_FlameSheet"),
        ("ember.png", "T_Ember"), ("logo_anthropic.png", "T_Logo_anthropic"), ("logo_openai.png", "T_Logo_openai"),
        ("logo_xai.png", "T_Logo_xai"), ("logo_meta.png", "T_Logo_meta"))],
}
GROUPS = globals().get("GROUPS") or list(JOBS)


def settings(t):
    return (t.get_editor_property("srgb"), str(t.get_editor_property("compression_settings")),
            str(t.get_editor_property("mip_gen_settings")), str(t.get_editor_property("lod_group")),
            t.blueprint_get_size_x(), t.blueprint_get_size_y())


tasks, before = [], {}
for g in GROUPS:
    for src, folder, name in JOBS[g]:
        path = folder + "/" + name
        old = unreal.EditorAssetLibrary.load_asset(path)
        if not old:
            raise RuntimeError("missing texture " + path)
        before[path] = settings(old)
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", src)
        t.set_editor_property("destination_path", folder)
        t.set_editor_property("destination_name", name)
        t.set_editor_property("replace_existing", True)
        t.set_editor_property("replace_existing_settings", False)
        t.set_editor_property("automated", True)
        t.set_editor_property("save", True)
        tasks.append((path, t))
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t for _, t in tasks])
out = []
for path, _ in tasks:
    now = settings(unreal.EditorAssetLibrary.load_asset(path))
    unreal.EditorAssetLibrary.save_asset(path, only_if_is_dirty=False)
    ok = now[:4] == before[path][:4]
    out.append({"asset": path, "ok": ok, "before": list(before[path]), "after": list(now)})
    unreal.log("T99 import %s %s %s -> %s" % (path, "OK" if ok else "SETTINGS CHANGED", before[path], now))
json.dump(out, open(ROOT + "Saved/T99/import.json", "w"), indent=1)
