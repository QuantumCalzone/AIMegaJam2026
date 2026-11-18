# T105 PIE check (PIE world only, nothing saved): pause the show, dress the four props with one card's
# names (SetProp) at the table slots, put one prop in a robot's HandSocket as TickFly leaves it, and move the
# house camera for close shots ("table", "hold") or put it back ("house").
import unreal, json, os, traceback
SAVED = unreal.Paths.project_saved_dir() + "T105/"
cfg = json.load(open(SAVED + "dress.json"))
PJ = json.load(open(unreal.Paths.project_content_dir() + "NHOS/Data/props.json"))["props"]
out = {}
try:
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
    unreal.GameplayStatics.set_game_paused(world, False)
    unreal.GameplayStatics.set_global_time_dilation(world, 0.0005)
    pc = unreal.load_class(None, "/Game/NHOS/Stage/BP_Prop.BP_Prop_C")
    rc = unreal.load_class(None, "/Game/NHOS/Stage/BP_Robot.BP_Robot_C")
    props = sorted(unreal.GameplayStatics.get_all_actors_of_class(world, pc), key=lambda a: a.get_name())
    robots = sorted(unreal.GameplayStatics.get_all_actors_of_class(world, rc), key=lambda a: a.get_name())
    out["robots"] = [(a.get_name(), [round(v) for v in (a.get_actor_location().x, a.get_actor_location().y)]) for a in robots]
    if cfg.get("hide_ui", True):
        sc = unreal.load_class(None, "/Game/NHOS/Core/BP_Show.BP_Show_C")
        for sh in unreal.GameplayStatics.get_all_actors_of_class(world, sc):
            st = sh.get_editor_property("Stage")
            if st:
                st.set_visibility(unreal.SlateVisibility.HIDDEN)
    if cfg.get("names"):
        for a, n in zip(props, cfg["names"]):
            a.detach_from_actor(unreal.DetachmentRule.KEEP_WORLD, unreal.DetachmentRule.KEEP_WORLD, unreal.DetachmentRule.KEEP_WORLD)
            a.set_actor_location_and_rotation(a.get_editor_property("HomeLoc"), a.get_editor_property("HomeRot"), False, True)
            a.call_method("SetProp", (n,))
        out["set"] = [(a.get_name(), str(a.get_editor_property("PropName"))) for a in props]
    if cfg.get("hold"):
        h = cfg["hold"]
        prop = next(a for a in props if str(a.get_editor_property("PropName")) == h["prop"])
        bot = robots[h["robot"]]
        hand = bot.get_editor_property("HandSocket")
        prop.attach_to_component(hand, "", unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)
        prop.set_actor_relative_location(unreal.Vector(0, 0, PJ[h["prop"]]["grip_z"]), False, True)
        prop.set_actor_relative_rotation(unreal.Rotator(0, 0, 0), False, True)
        out["held"] = (bot.get_name(), h["prop"])
    if cfg.get("cam"):
        hid = []
        for b in robots:
            l = b.get_actor_location()
            near = cfg["cam"] == "table" and ((l.x - 300) ** 2 + (l.y - 305) ** 2) ** 0.5 < 260
            if cfg["cam"] == "hold":
                near = b != robots[cfg["hold"]["robot"]]
            b.set_actor_hidden_in_game(near)
            if near: hid.append(b.get_name())
        out["hidden"] = hid
        pcon = unreal.GameplayStatics.get_player_controller(world, 0)
        vt = pcon.get_view_target()
        home = SAVED + "house_xf.json"
        comps = vt.get_components_by_class(unreal.CameraComponent)
        if not os.path.exists(home):
            l, r = vt.get_actor_location(), vt.get_actor_rotation()
            json.dump([l.x, l.y, l.z, r.pitch, r.yaw, r.roll, comps[0].field_of_view if comps else 90], open(home, "w"))
        hx = json.load(open(home))
        comps = vt.get_components_by_class(unreal.CameraComponent)
        if cfg["cam"] == "house":
            vt.set_actor_location_and_rotation(unreal.Vector(hx[0], hx[1], hx[2]), unreal.Rotator(roll=hx[5], pitch=hx[3], yaw=hx[4]), False, True)
            for c in comps: c.set_field_of_view(hx[6])
        else:
            if cfg["cam"] == "table":
                tgt = unreal.Vector(300, 305, 95); eye = unreal.Vector(70, 250, 190)
            else:
                bot = robots[cfg["hold"]["robot"]]
                bl = bot.get_actor_location()
                tgt = unreal.Vector(bl.x, bl.y, bl.z + 85); eye = unreal.Vector(bl.x - 430, bl.y - 60, bl.z + 130)
            rot = unreal.MathLibrary.find_look_at_rotation(eye, tgt)
            vt.set_actor_location_and_rotation(eye, rot, False, True)
            for c in comps: c.set_field_of_view(40.0)
        out["cam"] = cfg["cam"]
except Exception:
    out["error"] = traceback.format_exc()
json.dump(out, open(SAVED + "dress_out.json", "w"), indent=1)
