import json, os, struct, zlib, fbxedit as e
def png1(r,g,b):
    raw=b'\x00'+bytes([r,g,b])
    def chunk(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b'')
flat={'texture_normal.png':png1(128,128,255),'texture_roughness.png':png1(217,217,217),'texture_metallic.png':png1(0,0,0)}
plan=json.load(open('plan.json'))
src={'cannoli_tray':('test/cannoli_tray.fbx','fixed/cannoli_tray.png'),'wedding_envelope':('test/env_seal.fbx','fixed/wedding_envelope.png')}
os.makedirs('final',exist_ok=True)
for x in plan:
    p=x['prop']
    fbx,dif=src.get(p,(f'dl/{p}/model.fbx', f'fixed/{p}.png' if os.path.exists(f'fixed/{p}.png') else f'dl/{p}/texture_diffuse.png'))
    h,v,roots,f=e.read(fbx)
    for r in roots:
        for vid in r.find('Video'):
            fn=(vid.child('RelativeFilename') or vid.child('Filename')).props[0][1].decode().split('/')[-1]
            c=vid.child('Content')
            if fn=='texture_diffuse.png': c.props[0]=('R',open(dif,'rb').read())
            elif fn in flat: c.props[0]=('R',flat[fn])
            elif fn=='texture_emissive.png': pass
    os.makedirs(f'final/{p}',exist_ok=True)
    e.write(f'final/{p}/model.fbx',h,v,roots,f)
    os.system(f'cp "{dif}" final/{p}/texture_diffuse.png')
    print(p, os.path.getsize(f'final/{p}/model.fbx')//1024,'KB', fbx, dif)
