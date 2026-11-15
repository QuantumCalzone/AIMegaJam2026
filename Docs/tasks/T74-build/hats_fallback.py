"""T74 fallback A: put the headpieces on by hand in the editor world, if BP_Robot.SetHeadpiece can't
(dress.json says hat_ok false). NOT RUN (written by the T74 prep).

Run it right after dress.py, in the same T74 editor: `py "<absolute path to this file>"`. It reads
Saved/T74/dress.json (which robot plays which seat) and Content/NHOS/Data/costumes.json (T47's fits),
and for each robot spawns a StaticMeshActor with the headpiece, attached to the robot's HeadSocket the
way T80-build part 5 tried hats, with T47's relative fit and color. It also does what SetHeadpiece
does around the hat: hides the robot's own glasses under the dark shades, and lifts the antenna stalk
and the toppers so they poke out of the hat (T47-build part 2e's lift). It writes Saved/T74/hats.json.
Nothing is saved; the spawned actors are labeled T74Hat_<persona> and go when the editor closes.
"""
import json
import os
import traceback

import unreal

SAVED = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir())
WORK = os.path.join(SAVED, "T74")
CONTENT = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_content_dir())
out = {"hats": [], "errors": []}


def comp(actor, name):
    for c in actor.get_components_by_class(unreal.SceneComponent):
        if c.get_name() == name:
            return c
    return None


def rel(c, loc):
    c.set_editor_property("relative_location", loc)


def main():
    d = json.load(open(os.path.join(WORK, "dress.json"), encoding="utf-8"))
    heads = json.load(open(os.path.join(CONTENT, "NHOS", "Data", "costumes.json"), encoding="utf-8"))["headpieces"]
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = eas.get_all_level_actors()
    for a in actors:
        if a.get_actor_label().startswith("T74Hat_"):
            eas.destroy_actor(a)
    bots = {}
    for b in actors:
        if b.get_class().get_name() == "BP_Robot_C":
            try:
                bots[str(b.get_editor_property("PersonaId"))] = b
            except Exception:
                bots[str(b.get_editor_property("persona_id"))] = b
    for c in d["cast"]:
        b, h = bots.get(c["persona"]), heads.get(c["headpiece"])
        if not b or not h:
            out["errors"].append("no robot or headpiece for %s" % c)
            continue
        fit = dict(h)
        fit.update((h.get("on") or {}).get(c["persona"], {}))
        sock = comp(b, "HeadSocket")
        hidden_hat = comp(b, "Hat")  # what SetHeadpiece made, if anything: hide it
        if hidden_hat:
            hidden_hat.set_visibility(False, False)
        mesh = unreal.load_asset(h["mesh"].split(".")[0])
        hat = eas.spawn_actor_from_class(unreal.StaticMeshActor, sock.get_world_location())
        hat.set_actor_label("T74Hat_" + c["persona"])
        smc = hat.static_mesh_component
        smc.set_mobility(unreal.ComponentMobility.MOVABLE)
        smc.set_static_mesh(mesh)
        smc.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        keep = unreal.AttachmentRule.KEEP_RELATIVE
        hat.attach_to_component(sock, "", keep, keep, keep, False)
        smc.set_editor_property("relative_location", unreal.Vector(fit["x"], fit["y"], fit["z"]))
        smc.set_editor_property("relative_rotation", unreal.Rotator(roll=0.0, pitch=0.0, yaw=fit["yaw"]))
        smc.set_editor_property("relative_scale3d", unreal.Vector(fit["scale"], fit["scale"], fit["scale"]))
        hx = c["color"].lstrip("#")
        col = unreal.Color(r=int(hx[0:2], 16), g=int(hx[2:4], 16), b=int(hx[4:6], 16), a=255)
        mid = smc.create_dynamic_material_instance(0)
        mid.set_vector_parameter_value("Color", unreal.MathLibrary.conv_color_to_linear_color(col))
        # The shades hide the robot's own glasses (T47 ShowGlasses; T79 and T80 tag them "glasses").
        for x in b.get_components_by_class(unreal.StaticMeshComponent):
            tags = [str(t) for t in x.get_editor_property("component_tags")]
            if "glasses" in tags:
                x.set_visibility(c["headpiece"] != "dark_shades" and c["persona"] in tags, False)
        # The lift: the stalk's base 4 cm under the hat's top (T47-build 2e), Nub and every "acc" part
        # at z 165 or more rise with it. Their places now are bare-headed (SetHeadpiece failed early).
        nub = comp(b, "Nub")
        lift = 0.0
        if fit["top"] > 0 and nub:
            sl, ss = sock.get_editor_property("relative_location"), sock.get_editor_property("relative_scale3d")
            lift = max(0.0, sl.z + ss.z * fit["top"] + 8.0 - nub.get_editor_property("relative_location").z)
        if lift > 0:
            parts = [nub] + [x for x in b.get_components_by_class(unreal.StaticMeshComponent)
                             if "acc" in [str(t) for t in x.get_editor_property("component_tags")]
                             and x.get_editor_property("relative_location").z >= 165.0 and x != nub]
            for x in parts:
                l = x.get_editor_property("relative_location")
                rel(x, unreal.Vector(l.x, l.y, l.z + lift))
        out["hats"].append({"persona": c["persona"], "headpiece": c["headpiece"], "color": c["color"], "lift": lift})


try:
    main()
except Exception:
    out["errors"].append(traceback.format_exc())
json.dump(out, open(os.path.join(WORK, "hats.json"), "w", encoding="utf-8"), indent=1)
