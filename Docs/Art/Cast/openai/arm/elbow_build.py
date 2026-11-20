"""OpenAI's elbows (2026-11-20): split the rigid knit sleeve in two and give BP_Robot an elbow on each arm.

Why: OpenAI's fold (its "hands pressed together" at rest, T79) swung each straight sleeve 70 degrees forward,
so the arms jutted at the camera and the hands never met. With an elbow, the fold bends the forearms forward
and in, and the mittens meet thumbs up in front of the chest, as in openai/approved.png.

How it was run (2026-11-20): first in a second editor from a worktree, unsaved, to check it; then in the main
editor, which is the only one that can save BP_Robot (a second editor can't save an asset another editor has
loaded). In the main editor: BlueprintTools.add_variable FoldElbowPitch and FoldElbowYaw (float); this file in
the Cmd box (py "<this file>"); write_graph_dsl SetPersona and EventGraph from Graphs/BP_Robot/ (expanded with
Tools/dslpp.py); compile_blueprint; then save SM_OpenAI_UpperArm, SM_OpenAI_Forearm and BP_Robot, and nothing else.

What it does:
1. SM_OpenAI_UpperArm and SM_OpenAI_Forearm, next to SM_OpenAI_Arm: copies of it, cut at the elbow, mesh z 17
   (the sleeve runs from z 95 at the shoulder to the cuff at about z -50; the mitten is below). The upper arm
   keeps every polygon whose centre is above z 14, the forearm every polygon below z 29. Each cut end hides
   inside the other piece, and both keep SM_OpenAI_Arm's frame, so they line up with no offset when straight.
2. BP_Robot:
   - OArmXL/OArmXR show the upper arm. Each turns 90 degrees about its own long axis, about the joint point
     (mesh (-4, 2, 79.5)), so the mitten's thumb points forward and the palm faces in. Before, the thumbs
     pointed out to the sides, and the folded mittens looked like finger guns.
   - ElbowL/ElbowR, Scene components on ArmPivotL/ArmPivotR. SetPersona puts OpenAI's at mesh (-5, 4, 17) on the
     arm (pivot frame (0.03, -+3.53, -15.66)) and every other robot's at the pivot.
   - OForeXL/OForeXR, the forearms, on the elbows, with OArmXL/OArmXR's tags and settings.
   - HandSocketL/HandSocket move onto ElbowL/ElbowR, so a held prop rides the forearm. EventGraph keeps each
     socket at its shoulder's rotation, so a held prop stays upright.
   The fold's angles are variables (FoldElbowPitch, FoldElbowYaw), which the graphs read: SetPersona and
   EventGraph, written from Graphs/BP_Robot/ with BlueprintTools.write_graph_dsl after this script.
"""
import json
import unreal

OUT = None  # a path to write a JSON report to, or None

ARM = "/Game/NHOS/Stage/Cast/openai/SM_OpenAI_Arm"
DIR = "/Game/NHOS/Stage/Cast/openai"
BP = "/Game/NHOS/Stage/BP_Robot"
ELBOW_Z, UPPER_BELOW, FORE_ABOVE = 17.0, 3.0, 12.0
TWIST = 90.0
JOINT = unreal.Vector(-4.0, 2.0, 79.5)    # T109's joint point: the sleeve's centre 4 cm (15.5 mesh) under its top
ELBOW = unreal.Vector(-5.0, 4.0, ELBOW_Z)  # the sleeve's centre at the elbow
# T109's arm components (location, rotation as Rotator(roll, pitch, yaw), scale); the right arm is the left mirrored.
T109 = {"L": (unreal.Vector(-0.23, -6.09, -19.54), unreal.Rotator(0.0, 14.0, -90.0), unreal.Vector(0.258, 0.258, 0.258)),
        "R": (unreal.Vector(-0.23, 6.09, -19.54), unreal.Rotator(0.0, -14.0, -90.0), unreal.Vector(-0.258, 0.258, 0.258))}
COPY = ["component_tags", "override_materials", "cast_shadow", "visible", "hidden_in_game", "mobility",
        "generate_overlap_events", "can_character_step_up_on", "body_instance"]

report = {}
eal = unreal.EditorAssetLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()


def make_piece(name, keep):
    path = DIR + "/" + name
    if eal.does_asset_exist(path):
        raise RuntimeError(path + " exists already")
    sm = tools.duplicate_asset(name, DIR, unreal.load_asset(ARM))
    desc = sm.get_static_mesh_description(0)
    total = desc.get_polygon_count()
    drop = []
    for i in range(desc.get_polygon_count()):
        pid = unreal.PolygonID(i)
        if not desc.is_polygon_valid(pid):
            continue
        vs = desc.get_polygon_vertices(pid)
        z = sum(desc.get_vertex_position(v).z for v in vs) / len(vs)
        if not keep(z):
            drop.append(pid)
    for pid in drop:
        desc.delete_polygon(pid)
    sm.build_from_static_mesh_descriptions([desc], False)
    report[name] = {"dropped": len(drop), "kept": total - len(drop)}
    return sm


upper = make_piece("SM_OpenAI_UpperArm", lambda z: z > ELBOW_Z - UPPER_BELOW)
fore = make_piece("SM_OpenAI_Forearm", lambda z: z < ELBOW_Z + FORE_ABOVE)

sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
lib = unreal.SubobjectDataBlueprintFunctionLibrary
bp = unreal.load_asset(BP)


def gather():
    out = {}
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        out[str(lib.get_variable_name(lib.get_data(h)))] = h
    return out


def template(h):
    return lib.get_object_for_blueprint(lib.get_data(h), bp)


def add(name, cls, parent):
    m = gather()
    if name in m:
        raise RuntimeError(name + " exists already")
    res = sds.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=m[parent], new_class=cls, blueprint_context=bp))
    h = res[0] if isinstance(res, tuple) else res
    sds.rename_subobject(h, unreal.Text(name))
    return h


for side in ("L", "R"):
    sgn = 1.0 if side == "L" else -1.0
    loc, rot, sc = T109[side]
    # Spin the mesh TWIST degrees about its own Z first (mirrored on the right), then keep the joint point where it was.
    rot2 = unreal.MathLibrary.compose_rotators(unreal.Rotator(0.0, 0.0, sgn * TWIST), rot)
    loc2 = loc + (unreal.Transform(loc, rot, sc).transform_location(JOINT) - unreal.Transform(loc, rot2, sc).transform_location(JOINT))
    elbow = unreal.Transform(loc2, rot2, sc).transform_location(ELBOW)

    arm_t = template(gather()["OArmX" + side])
    arm_t.set_editor_property("static_mesh", upper)
    arm_t.set_editor_property("relative_location", loc2)
    arm_t.set_editor_property("relative_rotation", rot2)

    add("Elbow" + side, unreal.SceneComponent, "ArmPivot" + side)
    m = gather()
    sock = "HandSocket" if side == "R" else "HandSocketL"
    moved = sds.attach_subobject(m["Elbow" + side], m[sock])

    add("OForeX" + side, unreal.StaticMeshComponent, "Elbow" + side)
    m = gather()
    fore_t = template(m["OForeX" + side])
    for p in COPY:
        try:
            fore_t.set_editor_property(p, arm_t.get_editor_property(p))
        except Exception as e:  # report and go on: none of these is essential
            report.setdefault("copy_errors", []).append("%s: %s" % (p, e))
    fore_t.set_collision_profile_name(arm_t.get_collision_profile_name())
    fore_t.set_editor_property("static_mesh", fore)
    # The elbow sits at the pivot in the Blueprint's defaults; SetPersona moves OpenAI's to `elbow`.
    fore_t.set_editor_property("relative_location", loc2 - elbow)
    fore_t.set_editor_property("relative_rotation", rot2)
    fore_t.set_editor_property("relative_scale3d", sc)

    report[side] = {"arm_loc": [loc2.x, loc2.y, loc2.z], "arm_rot": [rot2.roll, rot2.pitch, rot2.yaw],
                    "elbow": [elbow.x, elbow.y, elbow.z], "socket_moved": bool(moved),
                    "tags": [str(t) for t in arm_t.get_editor_property("component_tags")]}

unreal.BlueprintEditorLibrary.compile_blueprint(bp)
if OUT:
    json.dump(report, open(OUT, "w"), indent=1)
print("OPENAI_ELBOWS", json.dumps(report))
