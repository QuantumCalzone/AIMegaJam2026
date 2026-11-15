# Prop art

How each generated 3D asset is made: its reference image, its Meshy settings and its import. The files live in `Docs/PropArt/`, one folder per asset. `.gitattributes` already sends `*.png` and `*.fbx` to LFS.

**Status:** the style test passed on 2026-11-15 (see "Test result" at the end). The plan's asset tasks make the rest the same way with `Tools/art_gen.py`. The art direction (stop-motion clay), the 13 headpieces and the props of each story are in the design doc: the "Art Inspiration" tab and the "Stories" tab. The story drafts behind them are in `Docs/StoryDrafts/`.

## Making a batch (T39)

Every asset is an entry in [PropArt/manifest.json](PropArt/manifest.json): 13 headpieces, 28 props (6 spares, `core: false`) and 3 set pieces, each with its prompt, Meshy model, texture, polycount and size. `Tools/art_gen.py` reads it and writes each asset's status back into it as soon as it has it: `images` (the Leonardo generation), `pick`, `ref`, `task` (the Meshy task), `credits` and `fbx`. Every step skips an asset that already has it, so a run that stops can simply be run again.

```bash
python Tools/art_gen.py status --kind headpiece
python Tools/art_gen.py batch-images --kind headpiece
python Tools/art_gen.py sheet --kind headpiece --candidates
python Tools/art_gen.py pick hood 2
python Tools/art_gen.py batch-meshes --kind headpiece --max-credits 260
python Tools/art_gen.py sheet --kind headpiece
```

1. `batch-images` makes 4 Leonardo candidates per asset, three assets at a time, into `Local/art/props/<id>/` (not git). The log goes to `Docs/PropArt/<id>/leonardo.json`.
2. `sheet --candidates` saves `Local/art/sheet_<kind>_candidates.html` with each asset's four candidates, numbered. Look at them (or read the PNGs) and `pick` the clearest outline: the whole object in frame, nothing touching it, a three-quarter view. `pick --force` re-picks an asset that already has a model and clears it, so the next `batch-meshes` makes it again.
3. `batch-meshes` checks the balance, then runs Meshy image to 3D for every asset with a `ref` and no `fbx`, up to 8 at once. It never starts a task that would take the run past `--max-credits` (estimates: `meshy-7.1` 20, `meshy-6-lite` 5, plus 10 with a texture) and prints the balance before and after. The FBX, its thumbnail and `meshy_image.json` go to `Docs/PropArt/<id>/`.
4. `sheet` saves `Local/art/sheet_<kind>.html` with every thumbnail, for one look at a whole kind.

Two runs on different kinds can go at once: each status write reloads the manifest first. Commit one task's manifest changes at a time.

## The look to match

Stop-motion clay: matte modeling clay, chunky rounded forms, faint thumbprints and tool marks, saturated but slightly chalky colors. The house camera sees a prop at about 30 px tall, so a bold outline and one or two strong colors matter more than detail. The stage isn't clay yet, so there is no style reference image: the prompt carries the look.

## Style test: the plush horse head

Why this one: it's the crime-family story's signature prop, engine shapes can't make it, and it's soft and organic, which shows best whether Meshy's output reads as clay.

### 1. Reference image (Leonardo)

1. Start a new image generation: 1:1, the highest resolution your plan allows, 4 images. No style reference.
2. Prompt:

   ```text
   A plush toy horse head made of modeling clay, in a stop-motion claymation style: a chunky, rounded, cuddly brown horse head with a cream muzzle, a short black yarn mane, two round button eyes and a soft stitched seam, cut off neatly at the neck like a stuffed toy. Matte clay surface with faint thumbprints, saturated slightly chalky colors, soft even lighting. Three-quarter view from slightly above, the whole object centered and in frame, plain light gray background.
   ```

3. Negative prompt:

   ```text
   blood, gore, realistic horse, fur texture, text, letters, logo, watermark, people, hands, robots, multiple objects, cropped, cut off, busy background, strong shadows, photorealistic, glossy plastic
   ```

4. Pick the image with the clearest outline: the whole head in frame, ears and muzzle visible, nothing touching it.
5. Save it as `Docs/PropArt/plush_horse_head/ref.png`. Write down the model name and the seed.

### 2. Model (Meshy)

1. **Image to 3D**, with `ref.png`.
2. Model **Meshy 7.1** (20 credits), not Ultra 2K (25 credits), which is the paid plans' default.
3. **Texture on** (+10 credits). The test compares Meshy's texture with our own flat clay color.
4. **Symmetry on**, if Meshy offers it.
5. When it finishes, **Remesh** (free) to about 5,000 triangles.
6. Download **FBX** into `Docs/PropArt/plush_horse_head/`, named `plush_horse_head.fbx`. If the download is a `.zip` with texture images beside the FBX, unzip it all there. Not GLB: the import tool takes only FBX and OBJ.

One try costs about 30 credits. Two or three tries are fine.

### 3. Import and look (an agent, through Unreal MCP)

1. `StaticMeshTools.import_file` into `/Game/NHOS/Stage/Props/Meshes/` as `SM_PlushHorseHead`, with `import_materials` and `import_textures` on. Call it with `toolset_name` `editor_toolset.toolsets.static_mesh.StaticMeshTools` and `tool_name` `import_file` (no prefix). It uses the FBX importer, so it takes `.fbx` and `.obj` and refuses `.glb`. A test OBJ imported at the right size (checked 2026-11-15).
2. Read the triangle count and the bounds, and scale it to about 30 cm, the size of today's props.
3. Make a first `M_Clay` (Substrate, matte, roughness about 0.85, a `Color` parameter, a faint noise in the normal for thumbprints) in `/Game/NHOS/Stage/Materials/`. It's new, so nothing needs a lock.
4. Place a temporary actor on the prop table. Take two screenshots, one from the house camera and one close up, with Meshy's texture. Then put an `M_Clay` instance on it and take them again.
5. Delete the temporary actor. Don't save `L_Stage`.

### Pass if

- From the house camera it reads as a plush horse head, and close up it reads as clay, with either Meshy's texture or `M_Clay`.
- It imports with no errors, at about 5,000 triangles or fewer.

If it fails, try once with Meshy's text-to-3D, or fall back to engine shapes with `M_Clay`.

## Test result (2026-11-15)

**Passed, by image to 3D.** `SM_PlushHorseHead` reads as a plush clay horse head close up, with the stitching, the white blaze, the button eyes, the smile and the yarn mane of its reference. From the house camera it reads as a brown horse head on the prop table. Next to today's glossy shape-built props it looks richer, so the clay restyle of the stage will close the gap.

- **Image to 3D beat text to 3D.** Both cost 30 credits on Meshy 7.1 with a 2K texture. Text to 3D ignored "head only" and made a whole pony; image to 3D followed the picture. So the batch makes a Leonardo image first.
- **Leonardo:** `lucid-origin` through the v2 API, 4 candidates, about 1 minute. Candidate 2, a three-quarter view with a neck stump, was the clear pick; the three front views were flatter. The v2 reply had no `apiCreditCost`. The API has its own pay-as-you-go balance, apart from the web plan: with none, it answers HTTP 402 "Insufficient tokens".
- **Meshy:** image to 3D at `target_polycount` 15000 took about a minute. At 5,000 triangles (the text-to-3D try) the clay shows facets; at about 15,600 it stays smooth.
- **Meshy's texture is the look.** It already reads as clay and carries the details (seams, buttons, blaze) that a flat clay color would lose, so `M_Clay` was not made. Props keep Meshy's texture; a flat clay material is for things built from engine shapes, and for headpieces, which each come in several colors.
- **Import:** `StaticMeshTools.import_file` took the FBX with its embedded texture and made `Material_001` and `texture_0`. Rename them at once (`M_<Asset>`, `T_<Asset>_BaseColor`), or the next import collides. The importer also leaves a `<name>.fbm/` folder beside the FBX; it belongs in `Local/art/props/`, not git.
- **Size and facing:** Meshy scales every model to about 1.9 m, so the horse head needs a scale of 0.17 for about 30 cm. Its face points along +Y: yaw 90 turns it to the house.
- **Credits:** 60 of 1,100 for the test (two models). 1,040 left.
- **Kept in git:** `ref.png`, the FBX, the thumbnails and the three JSON logs. The other candidates, the GLBs and the texture maps are in `Local/art/props/plush_horse_head/`.

## Recording each asset

- Add a row to [Assets.md](Assets.md): the asset, "Meshy (Pro plan), image to 3D from a Leonardo.ai image", the prompt, and the license ("Ours: made on a paid Meshy plan, which gives ownership").
- On a free Leonardo plan, the reference image is public and Leonardo owns it, with a license that allows commercial use. The model is Meshy's output.
