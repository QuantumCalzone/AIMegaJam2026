"""T74: dress L_Stage for one card in THIS editor, without saving. NOT RUN (written by the T74 prep).

Run it in the T74 editor's console box (`py "<absolute path to this file>"`); t74.py does that for you.
It reads Saved/T74/spec.json, which t74.py writes:
    {"card": "space_plans", "seats": {...fallback seats, see t74.py...}, "world": "editor" (or "pie")}
and writes Saved/T74/dress.json when it ends (t74.py waits for that file). It never saves an asset.

What it does, in this order (each step says whether it needs PIE; none should):
  1. The backdrop: sets the Backdrop actor's PreviewBackdrop (which reruns its construction script,
     and that calls ShowBackdrop), then calls BP_Backdrop.ShowBackdrop(id) itself.  [editor world]
  2. The props: the card's four props on the four BP_Prop actors, in the order ResetStage would
     use (GetAllActorsOfClass): PropName, then BP_Prop.SetProp(name). A fifth prop actor (none
     since T45) gets "" and hides.                                                 [editor world]
     BP_StageDirector.ResetStage is NOT called: it reads the card from BP_Show's CardArr, which is
     only loaded at BeginPlay, so outside PIE it would leave the old props (Graphs/BP_StageDirector/
     CardFromShow.txt). SetProp is what ResetStage calls for each prop.
  3. The costumes: one of the card's seats on each robot, by T47's BP_Robot.SetHeadpiece(Id, Color).
     SetHeadpiece makes its Hat component at run time (Add Component by Class); this is the one
     call that might not work in the editor world. dress.json says, per robot, whether a visible
     Hat came out of it.                                                            [editor world, RE-CHECK]
  4. The labels: hides each robot's Label text ("ROBOT" in the editor), and every component the
     game hides anyway (hidden in game: billboards, place-mark sprites), so the editor frame
     matches the game's.                                                            [editor world]
  5. Reports the StageCamera's transform and FOV, and each robot's place, facing and visible top,
     for t74.py's cameras.
Steps 1 to 3 never touch a robot's properties after step 3, because a construction-script rerun
on a robot (a property change) would rebuild it without its hat and label state.
"""
import json
import os
import re
import traceback

import unreal

SAVED = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir())
WORK = os.path.join(SAVED, "T74")
CONTENT = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_content_dir())
SCENES = os.path.join(CONTENT, "NHOS", "Data", "scenes.json")

# Seat order of the robots (BP_Robot.SetPersona's ids): OpenAI, Anthropic, SpaceXAI, Meta, You.
SEAT_ORDER = ["visionary", "worrier", "overclocker", "copycat", "human"]
PROVIDER = {"visionary": "OpenAI", "worrier": "Anthropic", "overclocker": "SpaceXAI", "copycat": "Meta", "human": "You"}

out = {"ok": False, "steps": [], "errors": []}


def note(msg):
    out["steps"].append(msg)
    unreal.log("T74: " + msg)


def snake(name):
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name).lower()


def setp(obj, name, value):
    """set_editor_property by the Blueprint name, then by its snake_case Python name."""
    for n in (name, snake(name)):
        try:
            obj.set_editor_property(n, value)
            return n
        except Exception:
            pass
    raise RuntimeError("no property %s on %s" % (name, obj.get_name()))


def getp(obj, name, default=None):
    for n in (name, snake(name)):
        try:
            return obj.get_editor_property(n)
        except Exception:
            pass
    return default


def seat_map(seats):
    """Which card seat each robot plays, in SEAT_ORDER: the card's own order, except that the dark
    shades never go to Meta (it already wears black glasses) or to You (the box): they swap with
    Anthropic, whose gold glasses the shades then hide. (T74 prep decision; change it here.)"""
    order = list(range(len(seats)))
    for i in (3, 4):
        if i < len(order) and seats[order[i]].get("headpiece") == "dark_shades":
            order[1], order[i] = order[i], order[1]
    return order


def main():
    spec = json.load(open(os.path.join(WORK, "spec.json"), encoding="utf-8"))
    card_id = spec["card"]
    scenes = json.load(open(SCENES, encoding="utf-8"))
    card = next(c for c in scenes["cards"] if c["id"] == card_id)
    seats = card["seats"]
    # T47 writes headpiece and color into each seat. If a seat lacks them, use spec["seats"]
    # (t74.py fills it from Docs/tasks/T47-build/scenes_seats.json) and say so.
    fb = {s["role"]: s for s in spec.get("seats", {}).get(card_id, [])}
    for s in seats:
        if not s.get("headpiece") or not s.get("color"):
            f = fb.get(s["role"], {})
            s["headpiece"], s["color"] = f.get("headpiece", ""), f.get("color", "")
            out["errors"].append("scenes.json seat %r has no headpiece/color; used T47-build's %s %s" % (s["role"], s["headpiece"], s["color"]))

    # "world": "pie" dresses the running PIE world instead (fallback B in the sheet): the same calls on
    # the PIE actors, no property sets (a PIE actor's construction script must not rerun).
    pie = spec.get("world") == "pie"
    ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    world = ues.get_game_world() if pie else ues.get_editor_world()
    if world is None:
        raise RuntimeError("no PIE world: start PIE first" if pie else "no editor world")
    if pie:
        actors = list(unreal.GameplayStatics.get_all_actors_of_class(world, unreal.Actor))
    else:
        actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
    out["world"] = "pie" if pie else "editor"

    def setp_world(obj, name, value):
        if not pie:
            setp(obj, name, value)

    def by_class(cname):
        return [a for a in actors if a.get_class().get_name() == cname]

    # 1. The backdrop
    bid = card["backdrop"]["id"]
    for bd in by_class("BP_Backdrop_C"):
        try:
            setp_world(bd, "PreviewBackdrop", bid)
        except Exception as e:
            out["errors"].append("PreviewBackdrop: %s" % e)
        bd.call_method("ShowBackdrop", (bid,))
        note("backdrop %s on %s" % (bid, bd.get_actor_label()))

    # 2. The props, in GetAllActorsOfClass order (what BP_StageDirector.Init and ResetStage use)
    prop_cls = unreal.EditorAssetLibrary.load_blueprint_class("/Game/NHOS/Stage/BP_Prop")
    props = list(unreal.GameplayStatics.get_all_actors_of_class(world, prop_cls))
    names = card["props"]
    out["props"] = []
    for i, p in enumerate(props):
        name = names[i] if i < len(names) else ""
        try:
            setp_world(p, "PropName", name)
        except Exception as e:
            out["errors"].append("PropName on %s: %s" % (p.get_actor_label(), e))
        p.call_method("SetProp", (name,))
        l = p.get_actor_location()
        out["props"].append([p.get_actor_label(), name, [round(l.x), round(l.y), round(l.z)]])
    note("props %s on %d actors" % (names, len(props)))
    if len(props) < len(names):
        out["errors"].append("only %d prop actors for %d props" % (len(props), len(names)))

    # 3. The costumes
    bots = {}
    for b in by_class("BP_Robot_C"):
        pid = getp(b, "PersonaId") or getp(b, "PreviewPersona") or ""
        bots[str(pid)] = b
    missing = [p for p in SEAT_ORDER if p not in bots]
    if missing:
        out["errors"].append("no robot with persona %s (found %s)" % (missing, sorted(bots)))
    order = seat_map(seats)
    out["cast"] = []
    for i, pid in enumerate(SEAT_ORDER):
        b = bots.get(pid)
        if not b or i >= len(order):
            continue
        s = seats[order[i]]
        b.call_method("SetHeadpiece", (s["headpiece"], s["color"]))
        hat = getp(b, "Hat")
        hat_ok = bool(hat) and hat.is_visible() and bool(getp(hat, "StaticMesh"))
        out["cast"].append({"persona": pid, "provider": PROVIDER[pid], "label": b.get_actor_label(),
                            "role": s["role"], "headpiece": s["headpiece"], "color": s["color"], "hat_ok": hat_ok})
        if not hat_ok:
            out["errors"].append("%s: SetHeadpiece(%s) left no visible Hat in the %s world" % (PROVIDER[pid], s["headpiece"], out["world"]))
    note("costumes on %d robots" % len(out["cast"]))

    # 4. The labels, and everything the game hides anyway
    hidden = 0
    for a in actors:
        is_bot = a.get_class().get_name() == "BP_Robot_C"
        for c in a.get_components_by_class(unreal.PrimitiveComponent):
            hide = bool(getp(c, "hidden_in_game", False))
            if is_bot and isinstance(c, unreal.TextRenderComponent):
                hide = True  # the Label ("ROBOT" in the editor) and T57's "(passed)" line on it
            if hide and c.is_visible():
                c.set_visibility(False, False)
                hidden += 1
    note("hid %d components (robot labels and hidden-in-game parts)" % hidden)

    # 5. What t74.py needs for its cameras
    cams = [a for a in actors if a.get_actor_label() == "StageCamera"]
    if cams:
        cc = cams[0].get_component_by_class(unreal.CameraComponent)
        l, r = cc.get_world_location(), cc.get_world_rotation()
        out["camera"] = {"loc": [l.x, l.y, l.z], "rot": [r.pitch, r.yaw, r.roll], "fov": cc.get_editor_property("field_of_view")}
    else:
        out["errors"].append("no StageCamera; t74.py uses (-1050, 0, 330), pitch -20, FOV 90")
    out["robots"] = []
    for pid in SEAT_ORDER:
        b = bots.get(pid)
        if not b:
            continue
        loc, yaw = b.get_actor_location(), b.get_actor_rotation().yaw
        fwd, right = b.get_actor_forward_vector(), b.get_actor_right_vector()
        top, half = 0.0, 0.0
        for c in b.get_components_by_class(unreal.PrimitiveComponent):
            if isinstance(c, unreal.TextRenderComponent) or not c.is_visible():
                continue
            o, e, _r = unreal.SystemLibrary.get_component_bounds(c)
            top = max(top, o.z + e.z)
            d = o - loc
            half = max(half, abs(d.x * right.x + d.y * right.y) + max(e.x, e.y))
        out["robots"].append({"persona": pid, "provider": PROVIDER[pid], "label": b.get_actor_label(),
                              "loc": [loc.x, loc.y, loc.z], "yaw": yaw, "fwd": [fwd.x, fwd.y], "top": top, "half_width": half})
    out["card"] = card_id
    out["ok"] = not out["errors"]


try:
    main()
except Exception:
    out["errors"].append(traceback.format_exc())
json.dump(out, open(os.path.join(WORK, "dress.json"), "w", encoding="utf-8"), indent=1)
