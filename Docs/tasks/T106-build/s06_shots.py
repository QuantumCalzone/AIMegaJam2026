"""T106 step 6: editor-viewport shots of the house, from the house camera and close up, queued on
Slate ticks (T103/T104's way: take_high_res_screenshot after set_level_viewport_camera_info).
Edit SHOTS (or Saved/T106/out/shots.json if it exists: [[name, [x,y,z], [pitch,yaw], w, h], ...])
then run. PNGs go to Saved/T106/shots/<TAG>/. These are layout checks only: the judged shots are
PIE and the game window (the build notes)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, t106lib
importlib.reload(t106lib)
from t106lib import *

TAG = 'v3'
D = ROOT + 'Saved/T106/shots/' + TAG + '/'
os.makedirs(D, exist_ok=True)
CAM = None
for a in eas().get_all_level_actors():
    if a.get_actor_label() == 'StageCamera':
        CAM = a
cl, cr = CAM.get_actor_location(), CAM.get_actor_rotation()
SHOTS = [
    ('house_1600', [cl.x, cl.y, cl.z], [cr.pitch, cr.yaw], 1600, 900),
    ('house_1440', [cl.x, cl.y, cl.z], [cr.pitch, cr.yaw], 1440, 900),
    ('chandelier', [-900, 0, 380], [5, 0], 1000, 700),
    ('cherub_r', [-450, 380, 80], [-5, 30], 900, 700),
    ('box_r', [-800, 250, 250], [0, 40], 1000, 800),
    ('stalls_back', [-1000, 0, 60], [-15, 0], 1200, 700),
    ('stalls_front', [-300, 0, 40], [-10, 180], 1200, 700),
    ('table', [100, 300, 120], [-15, 0], 900, 700),
]
if os.path.exists(OUT + 'shots.json'):
    SHOTS = json.load(open(OUT + 'shots.json'))
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
Q = []
for name, l, r, w, h in SHOTS:
    Q += [('cam', (unreal.Vector(*l), unreal.Rotator(roll=0, pitch=r[0], yaw=r[1]))), ('wait', 6), ('shot', (name + '.png', w, h)), ('wait', 4)]
st = {'Q': Q, 'w': 0, 'log': []}


def tick(dt):
    if st['w'] > 0:
        st['w'] -= 1
        return
    if not st['Q']:
        unreal.unregister_slate_post_tick_callback(st['h'])
        json.dump(st['log'], open(D + 'index.json', 'w'))
        return
    k, v = st['Q'].pop(0)
    if k == 'wait':
        st['w'] = v
    elif k == 'cam':
        ues.set_level_viewport_camera_info(v[0], v[1])
    elif k == 'shot':
        unreal.AutomationLibrary.take_high_res_screenshot(v[1], v[2], D + v[0])
        st['log'].append(v[0])


st['h'] = unreal.register_slate_post_tick_callback(tick)
