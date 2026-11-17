# T43 build sheet: import the generated models and make the clay material

**Note, 2026-11-17:** the `T43-build/` folder this sheet links was deleted in the post-jam cleanup, because T43 is done and its files were used once. Git history has it (`git show 465cf9f:Docs/tasks/T43-build/<file>`).

Back to [T43](T43.md) and [the plan](../Plan.md). This is prep for T43. It was written without the editor on 2026-11-15 at commit `6172856` (T40's headpieces are in; T41 and T42 haven't started). It is a plan, not a record: nothing here was written to the editor, and no asset was changed. The tool names and arguments below were read from this Mac's running editor with `describe_toolset` (a read of the tool list, no editor action), so they are the real 5.8.4 signatures. The material node and pin names are the ones T43 must confirm (E2 to E4).

Sources read: [T43.md](T43.md), T43's plan entry, [PropArt.md](../PropArt.md) (the style test and its result), `Docs/PropArt/manifest.json`, the findings of T39 and T40, the Unreal MCP rules in T01, T11, T17, T19, T27 and T35, `M_Robot` and `M_Set` as T11 and T17 describe them, `Docs/Submission.md`, `Docs/ItchPage.md`, T46 and T47 (who use `M_Clay` and the headpieces next), and `Tools/art_gen.py`'s manifest writer.

The per-asset call list comes from [make_import_plan.py](T43-build/make_import_plan.py). Run it again when T43 starts and after T41 and T42, because the manifest grows:

```bash
python Docs/tasks/T43-build/make_import_plan.py
```

## Read this first

### What the sheet assumes (check each one before you build)

| # | Assumption | How to check | If it is wrong |
|---|---|---|---|
| A1 | **T40 is in (13 headpieces, `6172856`), T41 and T42 may not be.** T43 imports whatever kinds have an `fbx` and can come back for the rest. | Run the script. Its list is the work. | Import the kinds that are there; leave T43 open with a `Waiting:` line for the rest, as the plan allows. |
| A2 | **The style test left three assets in `/Game/NHOS/Stage/Props/Meshes/`:** `SM_PlushHorseHead`, `M_PlushHorseHead`, `T_PlushHorseHead_BaseColor`. Nothing else references them (the test's actor was deleted and `L_Stage` not saved). They are in git. | `AssetTools.get_referencers` on each (E9). The script lists the horse head as a MOVE. | If something references them, move them anyway (the move fixes loaded referencers) and save the referencer too, with its lock. |
| A3 | **No other generated asset is in `Content/` yet.** | The script skips anything already at its destination; `AssetTools.find_assets` with `folder_path` `/Game/NHOS/Stage` and `name` `SM_`. | Skip what's there; record its fit if the manifest lacks it. |
| A4 | **The stage is where T17, T19 and T27 left it:** `StageCamera` at (-1050, 0, 330), pitch -20, 90° horizontal; the stage floor's front edge at x = -260; proscenium columns at y = ±640, robot spots inside y = ±440; robots home near x = 0 (outer ones about 50 cm forward); the prop table at (300, 300); the backdrop flat at x = 520. | E5 and E6. | Shift the rows in "Look" by the difference. Keep them inside y = ±440 and in front of the robots. |
| A5 | **The tool signatures below are current** (read 2026-11-15). | `describe_toolset` once per toolset you use, if a call fails on an argument. | Use the names it lists. |
| A6 | **`Tools/art_gen.py` keeps unknown fields.** It reloads the manifest before each write and saves it with `indent=2`, `ensure_ascii=False` and a final newline, so a `fit` field T43 adds survives T41's and T42's runs. | `save_manifest` and the status writer in `Tools/art_gen.py`. | Write `fit` after the last art run, and say so in Findings. |
| A7 | **`Docs/Submission.md` still has the lines quoted in "Step 6"** (as of `6172856`). | Search for each quoted line. | Apply the same meaning to whatever replaced it. |
| A8 | **No other session drives the editor.** | `Agents/status/*.md`: no `Editor: driving`. | Wait, as the rules say. |

### Questions only the editor can settle (in this order; each is one or two calls)

- **E1 Toolsets and the batch runner.** Call `get_execution_environment` once (T01), then use `editor_toolset.toolsets.programmatic.ProgrammaticToolset` for the batches. Confirm its script tool's name with `describe_toolset` (earlier tasks call it `execute_tool_script`; inside the script, `execute_tool(name, json_string)` returns a dict with `returnValue`).
- **E2 How `M_Robot` feeds Substrate.** `MaterialTools.get_property_input` with `material` `/Game/NHOS/Stage/M_Robot.M_Robot` and `material_property` `MP_FrontMaterial`. Expect a `MaterialExpressionSubstrateSlabBSDF`. Then `MaterialTools.get_expression_inputs` on that expression lists the Slab's real input names and which are wired (T11: `Color` into Diffuse Albedo, a constant into Roughness). Build `M_Clay` the same way. If `MP_FrontMaterial` is empty on `M_Robot`, try `MP_MaterialAttributes`, and use whichever it uses.
- **E3 Expression property names for `ObjectTools.set_properties`.** On the first `VectorParameter` you add, call `ObjectTools.list_properties` (with `instance`, T11). Expect `ParameterName` and `DefaultValue`, possibly camelCase (`parameterName`, `defaultValue`), as T35 found for widgets. Use exactly what it lists for every expression below.
- **E4 Expression classes exist under these paths.** `MaterialTools.list_expression_classes` with `material_or_function` = `M_Clay` and `search` `SubstrateSlab`, `Noise`, `LocalPosition`, `AppendVector`, `Normalize`, `VectorParameter`, `ScalarParameter`, `Constant`, `Multiply`, `Add`. Use the returned paths in `add_expression`.
- **E5 The house camera.** `SceneTools.find_actors` for `StageCamera`, then `ActorTools.get_actor_transform`. Use its real transform as the `captureTransform` for the house shot.
- **E6 The stage floor's top and the robots' spots.** `ActorTools.get_actor_bounds` on `StageFloor` (its `max.z` is `Z0`, expected 0 or a little above), and `get_actor_transform` on the five robots.
- **E7 What one import returns.** The red pill alone, by direct `call_tool` (Step 1, call 1): the order and classes of the returned assets, and the names the importer gave the material and texture (the style test got `Material_001` and `texture_0`).
- **E8 How long one import takes.** Time call 1 (and one headpiece) from the log timestamps (`LogFbx`, `LogModelContextProtocol` in `Saved/Logs/AIMegaJam2026.log`). This sets the batch size.
- **E9 The horse head's referencers.** `AssetTools.get_referencers` with `asset_path` for each of its three assets.
- **E10 A headpiece's material slots.** `StaticMeshTools.get_material_slots` after the first headpiece import, so `set_material` uses the real slot name.

## Order of work

`M_Clay` comes first, then the imports. All of it is new assets, so the order doesn't matter to anything else, and a headpiece can get its clay instance in the same script that imports it.

1. E1 to E4, then Step 3 (`M_Clay` and `MI_Clay_Neutral`). Save them.
2. E7, E8, E9, then Step 1 (import, in batches) with Step 1's renames, and the horse head's move. Save after each batch.
3. Step 2 (fit) and Step 4 (look), kind by kind.
4. Step 5 (save; check `git status`), Step 6 (`Docs/Submission.md`), the manifest's `fit` fields, Findings, commit.

**Never call `AssetTools.save_assets` with an empty list.** An empty list saves every dirty asset, and after Step 4 that includes `L_Stage`. Always pass the paths.

## Step 1: Import

### The calls

Every call goes through `call_tool` with the toolset's full name. `import_file` takes an absolute `source_file`; the script prints the absolute path for this machine. Folders that don't exist yet are created by the import (if one isn't, call `AssetTools.create_folder` with `path` first).

**A prop** (red pill; Meshy's material and texture on):

```json
toolset_name: editor_toolset.toolsets.static_mesh.StaticMeshTools
tool_name:    import_file
arguments: {"folder_path": "/Game/NHOS/Stage/Props/pick_a_pill",
            "asset_name": "SM_RedPill",
            "source_file": "<repo>/Docs/PropArt/red_pill/red_pill.fbx",
            "import_materials": true, "import_textures": true, "combine_meshes": true}
```

It returns `returnValue`: a list of `{refPath}`. The first is the mesh; the others are the material and the texture. Straight after, in the same call or script:

```json
AssetTools.move {"path": "/Game/NHOS/Stage/Props/pick_a_pill/Material_001", "new_path": "/Game/NHOS/Stage/Props/pick_a_pill/M_RedPill"}
AssetTools.move {"path": "/Game/NHOS/Stage/Props/pick_a_pill/texture_0",    "new_path": "/Game/NHOS/Stage/Props/pick_a_pill/T_RedPill_BaseColor"}
```

Take the old paths from the returned `refPath`s (drop the `.Name` part after the dot), not from these guesses, and tell the material from the texture with `AssetTools.get_asset_class` (`Material`, `Texture2D`). `move` keeps the mesh's material slot and the material's texture sample pointing at the renamed assets.

**Why the renames come at once:** every Meshy FBX names its material `Material_001` and its texture `texture_0`. The red pill and the blue pill share `Props/pick_a_pill/`, and all three set pieces share `Set/`. If the second import finds a `Material_001` already there, the FBX importer reuses it or collides with it, so the second model would wear the first one's texture. The style test hit this. After each batch, `AssetTools.find_assets` with the batch's folder and `name` `Material_0`, then `texture_`, must return nothing.

**A headpiece** (no materials; it gets the clay instance):

```json
StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_TopHat",
  "source_file": "<repo>/Docs/PropArt/top_hat/top_hat.fbx",
  "import_materials": false, "import_textures": false, "combine_meshes": true}
StaticMeshTools.get_material_slots {"mesh": {"refPath": "/Game/NHOS/Stage/Headpieces/SM_TopHat.SM_TopHat"}}
StaticMeshTools.set_material {"mesh": {"refPath": "/Game/NHOS/Stage/Headpieces/SM_TopHat.SM_TopHat"},
  "slot_name": "<each slot from get_material_slots>",
  "material": {"refPath": "/Game/NHOS/Stage/Materials/MI_Clay_Neutral.MI_Clay_Neutral"}}
```

No renames: with `import_materials` off, nothing but the mesh is made. Meshy made the headpieces without a texture (T40), so there is nothing to lose.

**A set piece** (Meshy's material and texture on, like a prop, in the shared `Set/` folder):

```json
StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Set", "asset_name": "SM_Chandelier",
  "source_file": "<repo>/Docs/PropArt/chandelier/chandelier.fbx",
  "import_materials": true, "import_textures": true, "combine_meshes": true}
AssetTools.move  <returned Material>  ->  /Game/NHOS/Stage/Set/M_Chandelier
AssetTools.move  <returned Texture2D> ->  /Game/NHOS/Stage/Set/T_Chandelier_BaseColor
```

**The plush horse head is moved, not imported.** It was imported and reviewed in the style test. Lock its three files first (they are in git: `git lfs lock Content/NHOS/Stage/Props/Meshes/SM_PlushHorseHead.uasset`, and the same for `M_PlushHorseHead.uasset` and `T_PlushHorseHead_BaseColor.uasset`), then:

```json
AssetTools.move {"path": "/Game/NHOS/Stage/Props/Meshes/T_PlushHorseHead_BaseColor", "new_path": "/Game/NHOS/Stage/Props/favor_father/T_PlushHorseHead_BaseColor"}
AssetTools.move {"path": "/Game/NHOS/Stage/Props/Meshes/M_PlushHorseHead",           "new_path": "/Game/NHOS/Stage/Props/favor_father/M_PlushHorseHead"}
AssetTools.move {"path": "/Game/NHOS/Stage/Props/Meshes/SM_PlushHorseHead",          "new_path": "/Game/NHOS/Stage/Props/favor_father/SM_PlushHorseHead"}
AssetTools.save_assets {"asset_paths": ["/Game/NHOS/Stage/Props/favor_father/SM_PlushHorseHead", "/Game/NHOS/Stage/Props/favor_father/M_PlushHorseHead", "/Game/NHOS/Stage/Props/favor_father/T_PlushHorseHead_BaseColor"]}
```

Then check for redirectors left behind: `AssetTools.find_assets` with `folder_path` `/Game/NHOS/Stage/Props/Meshes` and `name` `""`. Delete whatever is left there (`AssetTools.delete`, `path` each one, then the empty folder). `git status` should show the three old files deleted and three new ones added. Unlock the old paths after the push.

### The `.fbm` folders

The FBX importer unpacks a model's embedded texture into a `<name>.fbm/` folder beside the FBX, so props and set pieces leave one in `Docs/PropArt/<id>/`. They are copies of what's in the asset and don't belong in git. After each batch, from the repo root (Git Bash on the PC works the same):

```bash
for d in Docs/PropArt/*/*.fbm; do [ -d "$d" ] || continue; id=$(basename "$(dirname "$d")"); mkdir -p "Local/art/props/$id"; mv "$d" "Local/art/props/$id/"; done
```

Then `git status --short Docs/PropArt` must list no `.fbm`.

### Batching (each call well under 100 seconds)

Claude Code stops waiting after about 120 s, and a failed tool call ends a whole `execute_tool_script`, even inside `try` (T11). So:

1. **Call 1:** the red pill alone, by direct `call_tool` (E7, E8). Note its time `t_prop`. Then one headpiece alone; note `t_head`.
2. **Batch size:** `n = min(5, floor(60 / t))`, so a batch takes about 60 s at most. A guess before measuring: 2 props or set pieces, 5 headpieces.
3. **One script per batch.** Before each import, `AssetTools.exists` on the destination mesh, and skip it if it's there. That way a script that died halfway can simply run again. After the imports: the renames (or `set_material`), the leftovers check, `save_assets` with this batch's paths, and a return of what was made.
4. **The horse head's move and save** in one call of its own.

A batch script, in the form earlier tasks used (`Saved/agent_script_*.py`). `BATCH` is a slice of the script's `--json` output:

```python
import json
SM = 'editor_toolset.toolsets.static_mesh.StaticMeshTools.'
A = 'editor_toolset.toolsets.asset.AssetTools.'
def t(n, a):
    return execute_tool(n, json.dumps(a))
def pkg(ref):  # '/Game/X/Material_001.Material_001' -> '/Game/X/Material_001'
    return ref.split('.')[0]
BATCH = [  # paste entries from: make_import_plan.py --kind prop --json Saved/T43/import_plan.json
]
def run():
    out = []
    for e in BATCH:
        if t(A + 'exists', {'path': e['asset_path']})['returnValue']:
            out.append([e['id'], 'exists']); continue
        made = t(SM + 'import_file', e['import_args'])['returnValue']
        saved = [e['asset_path']]
        for r in made[1:]:
            p = pkg(r['refPath'])
            cls = t(A + 'get_asset_class', {'asset_path': p})['returnValue']
            for rn in e['renames']:
                if cls == rn['from_class']:
                    t(A + 'move', {'path': p, 'new_path': rn['to']})
                    saved.append(rn['to'])
        if e['slot_material']:
            mesh = {'refPath': e['asset_path'] + '.' + e['asset_name']}
            for s in t(SM + 'get_material_slots', {'mesh': mesh})['returnValue']:
                t(SM + 'set_material', {'mesh': mesh, 'slot_name': s,
                                        'material': {'refPath': e['slot_material'] + '.MI_Clay_Neutral'}})
        t(A + 'save_assets', {'asset_paths': saved})
        out.append([e['id'], [r['refPath'] for r in made], saved])
    return out
```

If E7 shows a texture class other than `Texture2D` (or the material as `MaterialInstanceConstant`), change `from_class` in the pasted entries, not the script.

### Today's list (the script's output at `6172856`)

The manifest has 15 models with an `fbx`: the 13 headpieces (T40), the plush horse head and the red pill. The absolute paths are this Mac's; the script prints the right ones on each machine.

```text
T43 import plan from Docs/PropArt/manifest.json: 15 to do

1. hood (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/hood/hood.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_Hood
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_Hood", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/hood/hood.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/hood/hood.fbm/ (if any) to Local/art/props/hood/

2. dark_shades (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/dark_shades/dark_shades.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_DarkShades
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_DarkShades", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/dark_shades/dark_shades.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/dark_shades/dark_shades.fbm/ (if any) to Local/art/props/dark_shades/

3. top_hat (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/top_hat/top_hat.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_TopHat
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_TopHat", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/top_hat/top_hat.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/top_hat/top_hat.fbm/ (if any) to Local/art/props/top_hat/

4. bob_wig (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/bob_wig/bob_wig.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_BobWig
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_BobWig", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/bob_wig/bob_wig.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/bob_wig/bob_wig.fbm/ (if any) to Local/art/props/bob_wig/

5. ball_cap (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/ball_cap/ball_cap.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_BallCap
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_BallCap", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/ball_cap/ball_cap.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/ball_cap/ball_cap.fbm/ (if any) to Local/art/props/ball_cap/

6. wide_brim_hat (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/wide_brim_hat/wide_brim_hat.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_WideBrimHat
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_WideBrimHat", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/wide_brim_hat/wide_brim_hat.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/wide_brim_hat/wide_brim_hat.fbm/ (if any) to Local/art/props/wide_brim_hat/

7. saucepan_helmet (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/saucepan_helmet/saucepan_helmet.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_SaucepanHelmet
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_SaucepanHelmet", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/saucepan_helmet/saucepan_helmet.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/saucepan_helmet/saucepan_helmet.fbm/ (if any) to Local/art/props/saucepan_helmet/

8. wizard_hat (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/wizard_hat/wizard_hat.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_WizardHat
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_WizardHat", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/wizard_hat/wizard_hat.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/wizard_hat/wizard_hat.fbm/ (if any) to Local/art/props/wizard_hat/

9. tiara (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/tiara/tiara.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_Tiara
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_Tiara", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/tiara/tiara.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/tiara/tiara.fbm/ (if any) to Local/art/props/tiara/

10. fedora (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/fedora/fedora.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_Fedora
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_Fedora", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/fedora/fedora.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/fedora/fedora.fbm/ (if any) to Local/art/props/fedora/

11. horned_helmet_beard (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/horned_helmet_beard/horned_helmet_beard.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_HornedHelmetBeard
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_HornedHelmetBeard", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/horned_helmet_beard/horned_helmet_beard.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/horned_helmet_beard/horned_helmet_beard.fbm/ (if any) to Local/art/props/horned_helmet_beard/

12. dino_hood (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/dino_hood/dino_hood.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_DinoHood
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_DinoHood", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/dino_hood/dino_hood.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/dino_hood/dino_hood.fbm/ (if any) to Local/art/props/dino_hood/

13. beanie (headpiece, 25 cm): IMPORT
   source:   Docs/PropArt/beanie/beanie.fbx
   folder:   /Game/NHOS/Stage/Headpieces
   asset:    SM_Beanie
   material: none on import; then MI_Clay_Neutral on every slot
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Headpieces", "asset_name": "SM_Beanie", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/beanie/beanie.fbx", "import_materials": false, "import_textures": false, "combine_meshes": true}
   then StaticMeshTools.set_material on each slot: /Game/NHOS/Stage/Materials/MI_Clay_Neutral
   then move Docs/PropArt/beanie/beanie.fbm/ (if any) to Local/art/props/beanie/

14. plush_horse_head (prop, 30 cm): MOVE
   source:   Docs/PropArt/plush_horse_head/plush_horse_head.fbx
   folder:   /Game/NHOS/Stage/Props/favor_father
   asset:    SM_PlushHorseHead
   material: keeps its renamed Meshy material and texture (moved with it)
   AssetTools.move {"path": "/Game/NHOS/Stage/Props/Meshes/SM_PlushHorseHead", "new_path": "/Game/NHOS/Stage/Props/favor_father/SM_PlushHorseHead"}
   AssetTools.move {"path": "/Game/NHOS/Stage/Props/Meshes/M_PlushHorseHead", "new_path": "/Game/NHOS/Stage/Props/favor_father/M_PlushHorseHead"}
   AssetTools.move {"path": "/Game/NHOS/Stage/Props/Meshes/T_PlushHorseHead_BaseColor", "new_path": "/Game/NHOS/Stage/Props/favor_father/T_PlushHorseHead_BaseColor"}

15. red_pill (prop, 30 cm): IMPORT
   source:   Docs/PropArt/red_pill/red_pill.fbx
   folder:   /Game/NHOS/Stage/Props/pick_a_pill
   asset:    SM_RedPill
   material: Meshy's material and texture, renamed M_RedPill and T_RedPill_BaseColor
   StaticMeshTools.import_file {"folder_path": "/Game/NHOS/Stage/Props/pick_a_pill", "asset_name": "SM_RedPill", "source_file": "/Users/personal/Projects/AIMegaJam2026/Docs/PropArt/red_pill/red_pill.fbx", "import_materials": true, "import_textures": true, "combine_meshes": true}
   then AssetTools.move the returned Material to /Game/NHOS/Stage/Props/pick_a_pill/M_RedPill
   then AssetTools.move the returned Texture2D to /Game/NHOS/Stage/Props/pick_a_pill/T_RedPill_BaseColor
   then move Docs/PropArt/red_pill/red_pill.fbm/ (if any) to Local/art/props/red_pill/
```

## Step 2: Fit

**Read the bounds.** `StaticMeshTools.get_bounds` with `mesh` `{"refPath": "<asset_path>.<asset_name>"}` returns the mesh's local box in cm, before any actor scale: `min` and `max` (x, y, z). Also read `get_triangle_count` (the test's bar: no more than about 15,600 for a `meshy-7.1` model). Batch these reads for a whole kind in one script.

**The arithmetic.**

- Extents: `dx = max.x - min.x`, `dy = max.y - min.y`, `dz = max.z - min.z`. Meshy makes every model about 190 cm along its longest side.
- **Props and set pieces:** `scale = size_cm / max(dx, dy, dz)`, rounded to 3 decimals. The manifest's `size_cm` is the longest side.
- **Headpieces:** `scale = size_cm / max(dx, dy)`, the footprint, not the height. A headpiece has to fit the head it sits on, so a tall wizard hat and a flat beanie get the same width (25 cm) and the wizard hat stays tall. By the longest side, the wizard hat would come out narrower than the beanie. (Open question 1.)
- **Height on the floor:** an actor at scale `s` whose bottom must touch a floor at `Z0` goes at `z = Z0 - min.z * s`. Meshy's pivot is usually at the model's center, so `min.z` is negative.
- **Sanity check:** if the longest side reads near 1.9 instead of 190, the FBX came in meters without conversion. The formula still holds (the scale comes out about 100 times larger), but say so in Findings.

**Worked example: the plush horse head.** The style test recorded a scale of 0.17 for about 30 cm, which means its longest side is about 30 / 0.17 = 176 cm (a little under Meshy's usual 190). So if `get_bounds` gives a longest side of 176, `scale = 30 / 176 = 0.1705`, recorded as 0.17. If it gives 190, the scale is 30 / 190 = 0.158. Its face points along +Y, and yaw 90 turns it to the house (below). Re-read its bounds after the move rather than trusting the 176; it's a value worked back from the recorded scale, not a measurement.

**The yaw (facing the house).** The house camera looks along +X, so "facing the house" means facing -X. In Unreal a positive yaw turns +X toward +Y, so:

| The model's face points along | Yaw |
|---|---|
| -X | 0 |
| +Y | 90 (the horse head) |
| +X | 180 |
| -Y | -90 |

To find each model's facing in one look: place four copies side by side at yaw 0, 90, 180 and -90, take one close-up from the house side, and pick the copy that faces the camera. This works as one script per model (place, capture, remove), so the capture comes back with the copies already gone:

- copies at x = -200 and y = -300, -100, 100, 300 (yaw 0, 90, 180, -90), scale as computed, `snap_to_ground` true;
- capture from (-520, 0, Z0 + 80), pitch -10, yaw 0 (it covers about ±320 cm at that distance).

A model that looks the same from every side (top hat, wizard hat, beanie, saucepan helmet) gets yaw 0. For the red pill, pick the yaw that shows its long side to the house.

**Record it in the manifest**, one `fit` object per asset, beside the status fields:

```json
"fit": {"asset": "/Game/NHOS/Stage/Headpieces/SM_TopHat", "bounds_cm": [176.2, 170.9, 141.0],
        "min_z": -70.5, "tris": 15012, "scale": 0.142, "yaw": 0, "underside": "open"}
```

(The numbers are made up, to show the form. `underside` is only for headpieces: open or filled, which T40 asked T43 to find out for T47.) Write it with the same formatting `art_gen.py` uses, and only when no art run is going (check `Agents/status/`):

```python
import json, pathlib
p = pathlib.Path('Docs/PropArt/manifest.json')
m = json.loads(p.read_text(encoding='utf-8'))
FIT = {  # id -> fit object
}
for a in m['assets']:
    if a['id'] in FIT:
        a['fit'] = FIT[a['id']]
p.write_text(json.dumps(m, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
```

## Step 3: `M_Clay` and its instance

### What it copies

T11 made `M_Robot` as one Substrate Slab BSDF with a `Color` vector parameter into Diffuse Albedo and a constant roughness. T17 made `M_Set` as one Slab with `Color`, `Metal`, `Rough`, `Glow`, `Fuzz` and `Planks` parameters. `M_Clay` is the same idea, kept small: one Slab, a `Color` parameter, a `Rough` parameter (the name `M_Set` uses) at 0.85, and a faint bumpy normal from two noise samples. T46 builds the bots from engine shapes with `M_Clay` instances, and T47 colors each headpiece with a dynamic instance's `Color`, so keep those two parameter names exactly.

### The graph

```
LocalPosition ─► Multiply(A) ◄─ ThumbScale (0.1)
                    │
                    ├──────────────► NoiseX.Position ─┐
                    └─► Add(A) ◄─ Constant3Vector     │
                           └──────► NoiseY.Position ─┤
                                                     ▼
                       AppendVector(A = NoiseX, B = NoiseY)  (float2)
                                    ▼
                       Multiply(A) ◄─ ThumbDepth (0.15)
                                    ▼
                       AppendVector(A, B = Constant 1)  (float3)
                                    ▼
                       Normalize ─► Slab.Normal
Color (vector param) ─► Slab.Diffuse Albedo
Rough (0.85)         ─► Slab.Roughness
Slab ─► material output, Front Material (MP_FrontMaterial)
```

**Why local position:** props fly and turn (T19). Noise from world position would crawl across a moving prop; local position sticks to it. The cost: on a non-uniformly scaled engine shape the bumps stretch a little, which is faint enough not to matter.

### The calls

`M` below means `{"refPath": "/Game/NHOS/Stage/Materials/M_Clay.M_Clay"}`. Each `add_expression` returns the new expression's `refPath`; keep them by the names in the first column. Put the class paths from E4 in `expression_class` (the expected ones are listed). Set properties with `ObjectTools.set_properties` (`instance` = the expression, `values` = a JSON string, T17), using the property names E3 found.

1. `MaterialTools.create_material` `{"folder_path": "/Game/NHOS/Stage/Materials", "asset_name": "M_Clay"}`.
2. Add the nodes (`MaterialTools.add_expression`, `material_or_function` `M`, `x`/`y` roughly as in the diagram; `layout_expressions` tidies them at the end):

| Name | `expression_class` (expected) | Properties to set |
|---|---|---|
| `Slab` | `/Script/Engine.MaterialExpressionSubstrateSlabBSDF` | none |
| `Color` | `/Script/Engine.MaterialExpressionVectorParameter` | `ParameterName` `Color`, `DefaultValue` `{"R": 0.32, "G": 0.30, "B": 0.28, "A": 1}` (a warm mid-gray, linear) |
| `Rough` | `/Script/Engine.MaterialExpressionScalarParameter` | `ParameterName` `Rough`, `DefaultValue` 0.85 |
| `Pos` | `/Script/Engine.MaterialExpressionLocalPosition` | none (default: including offsets) |
| `ThumbScale` | `/Script/Engine.MaterialExpressionScalarParameter` | `ParameterName` `ThumbScale`, `DefaultValue` 0.1 |
| `PosMul` | `/Script/Engine.MaterialExpressionMultiply` | none |
| `Offset` | `/Script/Engine.MaterialExpressionConstant3Vector` | `Constant` `{"R": 17.3, "G": 5.1, "B": 9.7, "A": 0}` |
| `PosAdd` | `/Script/Engine.MaterialExpressionAdd` | none |
| `NoiseX` | `/Script/Engine.MaterialExpressionNoise` | `NoiseFunction` `NOISEFUNCTION_GradientALU`, `Levels` 3, `Scale` 1, `OutputMin` -1, `OutputMax` 1, `bTurbulence` false |
| `NoiseY` | same as `NoiseX` | same |
| `XY` | `/Script/Engine.MaterialExpressionAppendVector` | none |
| `ThumbDepth` | `/Script/Engine.MaterialExpressionScalarParameter` | `ParameterName` `ThumbDepth`, `DefaultValue` 0.15 |
| `XYMul` | `/Script/Engine.MaterialExpressionMultiply` | none |
| `One` | `/Script/Engine.MaterialExpressionConstant` | `R` 1 |
| `XYZ` | `/Script/Engine.MaterialExpressionAppendVector` | none |
| `Norm` | `/Script/Engine.MaterialExpressionNormalize` | none |

3. Wire them (`MaterialTools.connect_expressions`: `from_expression`, `from_output_name`, `to_expression`, `to_input_name`; `""` is the default output). Read each node's real pin names once with `get_expression_input_names` and `get_expression_output_names`; the names here are the engine's usual ones:

| From (output) | To (input) |
|---|---|
| `Pos` (`""`) | `PosMul` (`A`) |
| `ThumbScale` (`""`) | `PosMul` (`B`) |
| `PosMul` (`""`) | `NoiseX` (`Position`) |
| `PosMul` (`""`) | `PosAdd` (`A`) |
| `Offset` (`""`) | `PosAdd` (`B`) |
| `PosAdd` (`""`) | `NoiseY` (`Position`) |
| `NoiseX` (`""`) | `XY` (`A`) |
| `NoiseY` (`""`) | `XY` (`B`) |
| `XY` (`""`) | `XYMul` (`A`) |
| `ThumbDepth` (`""`) | `XYMul` (`B`) |
| `XYMul` (`""`) | `XYZ` (`A`) |
| `One` (`""`) | `XYZ` (`B`) |
| `XYZ` (`""`) | `Norm` (`VectorInput`) |
| `Color` (`""`, the RGB output) | `Slab` (`Diffuse Albedo`) |
| `Rough` (`""`) | `Slab` (`Roughness`) |
| `Norm` (`""`) | `Slab` (`Normal`) |

4. `MaterialTools.connect_to_output` `{"expression": <Slab>, "output_name": "", "material_property": "MP_FrontMaterial"}` (or what E2 showed `M_Robot` uses).
5. `MaterialTools.get_expression_inputs` on `Slab` and `Norm`: every row above is wired. `MaterialTools.layout_expressions` `{"material_or_function": M}`, then `MaterialTools.recompile` `{"material_or_function": M}`. It raises if the shader fails; read `LogMaterial` in the editor log for the reason.
6. `MaterialInstanceTools.list_parameters` `{"material": M}` shows `Color`, `Rough`, `ThumbScale`, `ThumbDepth`.
7. The instance: `MaterialInstanceTools.create` `{"folder_path": "/Game/NHOS/Stage/Materials", "asset_name": "MI_Clay_Neutral", "parent": M}`, then `MaterialInstanceTools.set_vector_parameter` `{"instance": {"refPath": "/Game/NHOS/Stage/Materials/MI_Clay_Neutral.MI_Clay_Neutral"}, "name": "Color", "value": {"r": 0.35, "g": 0.33, "b": 0.31, "a": 1}}` (a neutral clay gray; the headpieces were generated mid-gray, and T47 sets each role's color at run time).
8. `AssetTools.save_assets` `{"asset_paths": ["/Game/NHOS/Stage/Materials/M_Clay", "/Game/NHOS/Stage/Materials/MI_Clay_Neutral"]}`.

**One instance for all headpieces.** "An instance in a neutral color on every headpiece" is one `MI_Clay_Neutral` set on every headpiece's slots (Step 1). T47 makes a dynamic instance per robot for the role colors, so 13 identical constant instances would add nothing.

### If a node or pin differs in the editor

- **The Slab's pins** have spaces in their names (`Diffuse Albedo`, `Second Roughness`, `Fuzz Amount`). Use exactly what `get_expression_input_names` returns.
- **`VectorParameter` outputs:** if `""` gives four channels and Diffuse Albedo complains, use the `RGB` output, or wire through a `ComponentMask` (R, G, B).
- **No `LocalPosition` class:** use `MaterialExpressionWorldPosition` minus `MaterialExpressionObjectPositionWS` (a `Subtract`). It crawls when a prop turns, but stays put when it only moves.
- **The noise shows seams or garbage on a model without UVs:** the tangent-space normal needs UVs, and Meshy's untextured headpieces may have poor ones. Set the material's `bTangentSpaceNormal` (check the name with `list_properties` on `M_Clay`) to false, and drive the Slab's Normal from the engine function `/Engine/Functions/Engine_MaterialFunctions02/PerturbNormalLQ` (a `MaterialExpressionMaterialFunctionCall`) fed by `NoiseX` times `ThumbDepth` as its height. If that function isn't at that path, leave Normal unwired. A flat matte clay passes the task; the thumbprints are a nice-to-have.
- **Thumbprint size:** the bumps come out about `object scale / ThumbScale` cm across. At a headpiece's scale of about 0.13, a `ThumbScale` of 0.1 gives bumps of about 1.3 cm. T46's engine shapes are scaled about 0.5 to 1.5, so their instances need a `ThumbScale` of about 0.5 for the same look. Tune `ThumbScale` and `ThumbDepth` on `MI_Clay_Neutral` from a close-up, and write the values in Findings for T46. They may not show from the house camera at all (a prop is about 30 px there); that's fine.
- **The inside of an open headpiece (hood, bob wig, dino hood) shows through:** set `TwoSided` on `M_Clay` (`list_properties` for the name) and recompile.
- **Chalky look (optional):** the Slab's `Fuzz Amount` (about 0.2) and `Fuzz Color` (the `Color` parameter) give the soft, chalky sheen `M_Set`'s `Fuzz` gives velvet. Only if the close-up looks plasticky.

## Step 4: Look

Place the models one kind at a time, so each house shot shows a clean row and the robots stay visible behind it. Every temporary actor is named `T43_<id>` and goes in the outliner folder `T43Temp`, so cleanup is one folder.

**Place:** `SceneTools.add_to_scene_from_asset` with `asset_path` the mesh (`/Game/NHOS/Stage/Headpieces/SM_TopHat`), `name` `T43_top_hat`, `xform` `{"location": {"x": X, "y": Y, "z": Z}, "rotation": {"pitch": 0, "yaw": YAW, "roll": 0}, "scale": {"x": S, "y": S, "z": S}}` and `snap_to_ground` true. Then `SceneTools.set_actor_folder` `{"actor": <returned actor>, "folder_path": "T43Temp"}`. If `snap_to_ground` leaves it floating or sunk, set the full transform again with `ActorTools.set_actor_transform`, passing location, rotation and scale every time (T17), with `z = Z0 - min.z * S`.

**Rows** (stage x runs from the house to the back; the camera is at x = -1050; spots stay inside y = ±440, T19):

| Pass | Models | Where | Spacing |
|---|---|---|---|
| 1 | the 13 headpieces | one row at x = -200 | `y_i = -420 + i * 70` (i = 0..12: -420 to 420) |
| 2 | the props (2 today, up to 28) | row A at x = -200 for the first half, row B at x = -120 for the rest | `s = min(80, 840 / (n - 1))` with n the models in the row; `y_i = -420 + i * s`; row B shifted by `s / 2` so its models show between row A's |
| 3 | the 3 set pieces | x = 150 (behind the front spots, in front of the backdrop at 520): cherub y = -380, theater box y = 0, chandelier y = 380 | on the floor; the robots may hide part of the theater box, which is fine for a size check |

Row B is staggered because the camera looks down at only 20°: a 30 cm prop hides about 80 cm of floor behind it. Robots at home stand near x = 0 to -50, about 35 cm in radius, so x = -120 keeps row B clear of them.

**Screenshots** (`EditorToolset.EditorAppToolset.CaptureViewport` with `captureTransform` `{"location": ..., "rotation": ..., "scale": {"x": 1, "y": 1, "z": 1}}` and `bShowUI` false; `CaptureViewport` captures the editor world, which is what's wanted here, T17):

- **House:** from `StageCamera`'s transform (E5; expected (-1050, 0, 330), pitch -20, yaw 0). The editor viewport is narrower than 16:9, so the frame shows a little less from side to side than the game does (T11).
- **Close-up:** from (row x - 220, y, Z0 + 70), pitch -12, yaw 0, which covers about ±220 cm. One per kind is the minimum; for the 13 headpieces take three, at y = -300, 0 and 300. Take one of the horse head and the red pill up close too, to compare with the style test's shots.
- **Saving them:** the capture comes back as base64 PNG. Write it with `AssetTools.write_file` to `Saved/T43/shots/<pass>_<view>.txt` (only text extensions under `Saved/` work, T35), then decode outside the editor: `base64 -D -i Saved/T43/shots/x.txt -o Saved/T43/shots/x.png` on the Mac, `certutil -decode` on the PC. `Saved/` is not in git.

**Judge each shot for:** every model at a sensible size next to the robots (a headpiece about half a robot head across, a prop about the size of T19's table props), facing the house, standing on the floor (not sunk, not floating), and no import faults (holes, missing texture, the gray-checker default material on a prop).

**Clean up:** `SceneTools.get_actors_in_folder` `T43Temp`, then `SceneTools.remove_from_scene` on each, then confirm the folder is empty. **Don't save `L_Stage`.** The level stays dirty in this editor session; that's expected. If the editor later asks to save it, say no. After T43 is pushed, the next session that changes `L_Stage` must reload it from disk first (T45 locks it next).

## Step 5: Save and check

- Every batch already saved its own assets. At the end, `AssetTools.is_dirty` on each new asset should be false, and on `/Game/NHOS/Maps/L_Stage` true (unsaved, as intended).
- `git status --short`: new files only under `Content/NHOS/Stage/Headpieces/`, `Content/NHOS/Stage/Props/<card>/`, `Content/NHOS/Stage/Set/` and `Content/NHOS/Stage/Materials/` (`M_Clay`, `MI_Clay_Neutral`); the horse head's three moves; `Docs/PropArt/manifest.json`; `Docs/Submission.md`; `Docs/tasks/T43.md`. No `L_Stage.umap`, no `.fbm`.
- Stage those paths by name. Unlock the horse head's old paths after the push.

## Step 6: `Docs/Submission.md`

Three places say no AI image or 3D tool was used. Replace each by its text (they were at lines 68 to 97 and 126 at `6172856`). Check `Docs/Assets.md` first for the exact Leonardo and Meshy plans and licenses T40 to T42 recorded, and use those words if they differ from these.

**1. In "Tools you used", under "AI tools we built the game with",** after the Claude Docs line, add:

```text
- Leonardo.ai (the lucid-origin model, through its API): a reference image for each generated 3D model, four candidates per model, one picked by hand.
- Meshy (Pro plan, image to 3D with Meshy 7.1 and Meshy 6 Lite): the clay-style 3D models, made from those reference images: the 13 costume headpieces, the story props and the opera-house set pieces. Props and set pieces keep Meshy's texture; the headpieces wear our own clay material.
```

(List only the kinds that are in at the time: if T41 or T42 hasn't run, leave out the story props or the set pieces.)

**2. The last line of that text block.** Replace:

```text
No AI image, 3D, texture, music, sound or voice tools were used. [T20: confirm once the audio is in.]
```

with:

```text
The only AI image and 3D tools were Leonardo.ai and Meshy, above. No AI texture, music, sound or voice tools were used. [T20: confirm once the audio is in.]
```

**3. The partner-prize line under the block.** Replace:

```text
None of the partner tools named on the jam page for prizes (Hyper3D Rodin, Meshy, Tripo, fal, PBRgen) were used, so there's nothing extra to list for those prizes. Add to this list if open question 7 turns something up.
```

with:

```text
Of the partner tools named on the jam page for prizes (Hyper3D Rodin, Meshy, Tripo, fal, PBRgen), we used Meshy: every generated 3D model in the game (headpieces, story props and set pieces) is a Meshy image-to-3D model, as listed above and in Docs/Assets.md. Check the jam page for what the Meshy prize asks for. Add to this list if open question 7 turns something up.
```

**4. Under "Art"** (in the asset declarations). Replace:

```text
- No outside or AI-generated art. The theater, the five robots and the six painted backdrops are built in the editor from the engine's basic shapes, with our own materials and no textures.
```

with:

```text
- AI-generated 3D models, made by us: the costume headpieces, the story props and the opera-house set pieces were made with Meshy (Pro plan, which gives us ownership of the output) from reference images we generated with Leonardo.ai. Docs/Assets.md lists each one with its prompt. Props and set pieces keep Meshy's textures; the headpieces use our own clay material.
- Everything else is built in the editor from the engine's basic shapes, with our own materials and no textures: the theater, the five robots and the six painted backdrops.
```

(Same rule: only the kinds that are in. If T46 or T48 has changed the robots or the backdrops by then, describe them as they are.)

## Open questions for T43

1. **Headpiece scale: footprint or longest side?** The sheet scales headpieces so their footprint is 25 cm, so they all fit one head, and props and set pieces by their longest side. Recommended, but `size_cm` was never defined. T47 sets the final scale and offset on T46's head anyway; T43's number is the starting point.
2. **Moving the horse head needs locks on three files in git** (`Content/NHOS/Stage/Props/Meshes/`), which T43's Touches don't list ("New assets only, so no locks"). The sheet moves them, because the asset is already imported and reviewed. The alternative is to leave it in `Props/Meshes/` and say so in Findings, but then one prop wouldn't follow the folder rule.
3. **`Docs/ItchPage.md` says the same thing** ("no AI image or 3D generator was used", in the AI disclosure's Graphics answer). Step 6 names only `Submission.md`, and `ItchPage.md` isn't in T43's Touches. Ask the person whether T43 should fix it too (recommended: yes, the same commit, one line).
4. **The Leonardo plan and license.** `PropArt.md` says a free Leonardo plan makes the image public and Leonardo's, with commercial use allowed; the batch used the API's own pay-as-you-go balance. Use what `Docs/Assets.md` says after T40 to T42, and if it doesn't say, ask the person which plan was used.
5. **Set-piece sizes are estimates** (chandelier 180 cm, cherub 60 cm, theater box 300 cm; T39). T43 records the scale for those sizes from the stage check; T49 places them in the house and may change them. Note any that looked wrong.
6. **The horned helmet's face and closed hats.** T40 found the helmet keeps a small round face that would cover the robot's own, and Meshy usually makes closed solids, which would hide T47's antenna topper. Record each headpiece's `underside` in `fit` and add both to Findings for T47; T43 doesn't fix them.
7. **Thumbprint values.** The noise's size and depth are a first guess. Record the tuned `ThumbScale` and `ThumbDepth` (and whether the tangent-space version worked on the untextured headpieces) in Findings, because T46 uses `M_Clay` on engine shapes next.
