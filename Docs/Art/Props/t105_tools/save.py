import json, os, subprocess, shutil
P="/Users/personal/Projects/AIMegaJam2026/Docs/Art/Props"
plan=json.load(open('plan.json')); ids=json.load(open('ids.json'))
notes={
 'cannoli_tray':"Rodin left out the gray tray in all three takes (image, image with the tray named first, text only). Take 1 is kept; T105's fbxedit.py added a flat round tray under it (48 segments, 480 triangles) whose UVs sit in an empty corner of the diffuse map, painted pale silver-gray (168,168,162). My person chose this.",
 'wedding_envelope':"Take 1 is kept (take 2 kept the seal mark and lost the clean shape). The stamped mark was relief in the mesh and paint in the texture: fbxedit.py smoothed the seal's front vertices (171 vertices, 40 Laplacian passes) and fixtex.swift filled the seal disc in the diffuse map with its rim's median color. My person chose this.",
 'plush_horse_head':"Take 1 (11c4a17b-...) came back broken: 10,016 scattered sliver triangles with a total area of 0.006. Take 2 is the model.",
 'ringing_phone':"The curly cord stayed in both takes (the image wins over the prompt). Take 2 is kept: one closed piece, where take 1's cord was 19 loose pieces. My person chose to keep the cord.",
 'bowling_ball':"The model came back pale lavender with no swirls. fixtex.swift recolored the diffuse map to deep plum (hue 305, value x0.6). My person chose this fix over a redo.",
 'rolled_up_rug':"The diamonds came back bright mustard-orange (now Meta's seat color). fixtex.swift shifted the orange pixels to dark old gold (hue 37, saturation 0.74, value x0.72). My person chose this fix.",
 'glowing_staff':"Rodin also made an emissive map that covers only the crystal; it is the glow mask (glow.png).",
 'glow_stick_sword':"glow.png masks the mint blade (fixtex.swift glow, hue 95-175) for the emissive material.",
 'glowing_briefcase':"glow.png masks the gold lining (fixtex.swift glow, hue 28-58); it also catches the two small gold latch plates. The god rays are an engine light, not in the model.",
 'tin_can_robot':"Texture de-light on: the can came out near white rather than silver-gray. My person approved it as it is.",
}
for x in plan:
    p,c=x['prop'],x['card']; d=f'final/{p}'
    subprocess.run(['python3','fbx2obj.py',f'{d}/model.fbx',f'{d}/model.obj',os.path.abspath(f'{d}/texture_diffuse.png'),f'{d}/mesh_stats.json'],check=True,capture_output=True)
    subprocess.run(['./render',f'{d}/model.obj',f'{d}/turntable.png',f'{d}/thumbnail.png'],check=True)
    subprocess.run(['sips','-s','format','jpeg','-s','formatOptions','82','--resampleWidth','1600',f'{d}/turntable.png','--out',f'{d}/turntable.jpg'],check=True,capture_output=True)
    subprocess.run(['sips','--resampleWidth','384',f'{d}/thumbnail.png'],check=True,capture_output=True)
    dst=f'{P}/{c}/{p}'
    shutil.copy(f'{d}/model.fbx',f'{dst}/model.fbx')
    shutil.copy(f'{d}/thumbnail.png',f'{dst}/model_thumb.png')
    shutil.copy(f'{d}/turntable.jpg',f'{dst}/model_turntable.jpg')
    st=json.load(open(f'{d}/mesh_stats.json'))
    i=ids[p]
    log={"prop":x['name'],"card":c,"task":"T105","made":"2026-11-18",
         "service":"Hyper3D Rodin (hyper3d.ai), Business plan, through the hyper3d MCP server",
         "tool":"rodin_generate","tier":"Gen-2.5-Medium","mesh_mode":"Raw","geometry_file_format":"fbx",
         "quality_override":x['quality_override'],
         "texture_delight":x['texture_delight'] if p not in ('cannoli_tray',) else True,
         "reference":"model_view.png","upload_id":i['upload_id'],
         "generation_id":i['generation_id'] if p not in ('cannoli_tray','wedding_envelope','ringing_phone') else None,
         "prompt":x['prompt'],
         "takes":(i.get('history',[])+[i['generation_id']]),
         "size_cm":x['size_cm'],
         "mesh":st,
         "files":{"model.fbx":"Rodin's base_basic_pbr.fbx; its embedded diffuse map is the final one, and its normal, roughness and metallic maps are flat 1-pixel images (flat normal, roughness 0.85, not metallic), so the clay stays matte",
                  "model_thumb.png":"front view (T105's SceneKit renderer)","model_turntable.jpg":"four sides"},
         "credits":"Rodin reports no cost per call; about 0.5 credit a generation (T81's measurement). T105's total is in Docs/tasks/T105.md."}
    used={'cannoli_tray':0,'wedding_envelope':0,'ringing_phone':1}
    if p in used: log['generation_id']=log['takes'][used[p]]
    if p=='cannoli_tray': log['texture_delight']=True; log['note_prompts']="takes 2 and 3 named the tray first; take 3 had no reference image"
    if p in notes: log['note']=notes[p]
    if os.path.exists(f'fixed/{p}_glow.png'): shutil.copy(f'fixed/{p}_glow.png',f'{dst}/glow.png'); log['files']['glow.png']="emissive mask, white = glows"
    if p=='glowing_staff':
        subprocess.run(['sips','-s','format','png',f'dl/{p}/texture_emissive.png','--out',f'{dst}/glow.png'],check=True,capture_output=True); log['files']['glow.png']="Rodin's emissive map: the crystal glows"
    json.dump(log,open(f'{dst}/model_log.json','w'),indent=1)
    print(p, st['triangles'], st['pieces'])
