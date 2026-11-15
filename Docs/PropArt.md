# Prop art

How each generated 3D asset is made: its reference image, its Meshy settings and its import. The files live in `Docs/PropArt/`, one folder per asset. `.gitattributes` already sends `*.png` and `*.fbx` to LFS.

**Status:** style test, one asset. If it passes, a plan task makes the rest the same way. The art direction (stop-motion clay), the 13 headpieces and the props of each story are in the design doc: the "Art Inspiration" tab and the "Stories" tab. The story drafts behind them are in `Docs/StoryDrafts/`.

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

## Recording each asset

- Add a row to [Assets.md](Assets.md): the asset, "Meshy (Pro plan), image to 3D from a Leonardo.ai image", the prompt, and the license ("Ours: made on a paid Meshy plan, which gives ownership").
- On a free Leonardo plan, the reference image is public and Leonardo owns it, with a license that allows commercial use. The model is Meshy's output.
