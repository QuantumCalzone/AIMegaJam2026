import json, os
P = "/Users/personal/Projects/AIMegaJam2026/Docs/Art/Props"
pr = json.load(open(f"{P}/prompts.json"))
override = {
 "tin_can_robot": "A little toy robot built from a dented tin can: a fat cylindrical can body in matte silver-gray clay (not shiny metal) with one big round dent and a few dark rust-brown patches, two big round bolt eyes, a small funnel hat on top, two short chunky bent arms and two stubby wheel feet. Cute and homemade.",
 "glowing_briefcase": "A slim, flat attache case in matte black clay lying flat on the ground and opened wide: the thin lid swings up almost upright, joined to the base along the back edge, and the front of the base faces the viewer with a chunky handle in the middle and two old-gold latches. The shallow inside is lined in warm gold clay. No light rays.",
 "wedding_envelope": "A fat cream wedding-card envelope, plump as if stuffed full, its flap sealed with a big round plain dark red wax seal with no marks on it, and tied with a thick crimson ribbon in a big bow.",
 "rolled_up_rug": "A rolled-up rug: a long, thick cylinder of rug rolled tight, deep red with a big simple dark old-gold diamond pattern, tied with two thick cream cords, with a rounded spiral showing at each end.",
 "ransom_bag": "A lumpy, bulging tan canvas money sack tied at the top with a thick rope, with a few plain flat green paper bills sticking out of the top. No writing and no symbols.",
 "red_pill": "A single big, chunky medicine capsule pill lying on its side: a smooth rounded capsule, one half deep cherry red and the other half cream.",
 "blue_pill": "A single big, chunky medicine capsule pill lying on its side: a smooth rounded capsule, one half deep navy blue and the other half cream.",
 "ringing_phone": "An old rotary desk telephone in charcoal black with a big cream dial with round finger holes, its chunky handset knocked crooked on the cradle, one end tilted up. No cord.",
 "bent_spoon": "A big, chunky spoon in pale silver-gray matte clay, its neck bent 30 degrees just below the round bowl; it rests on its bowl with the straight handle tilted up. One spoon, in one piece.",
 "giant_milkshake": "A tall, chunky diner milkshake glass made of solid opaque pale cream clay (not see-through), filled with a pink shake, topped with a big swirl of whipped cream, one round red cherry and a thick red-and-white striped straw.",
}
tail = " Hand-sculpted matte modeling clay, stop-motion claymation style, chunky rounded forms. One single closed object, no base, no text, no logos."
small = {"red_pill", "blue_pill", "cursed_ring", "bent_spoon", "safety_waiver", "wedding_envelope", "gold_pocket_watch"}
delight = {"tin_can_robot", "gold_pocket_watch", "cursed_ring", "cannoli_tray", "bent_spoon", "frying_pan"}
plan = []
for card, props in pr["cards"].items():
    for pid, v in props.items():
        img = f"{P}/{card}/{pid}/model_view.png"
        plan.append({"card": card, "prop": pid, "name": v["name"], "size_cm": v["size_cm"], "image": img,
                     "bytes": os.path.getsize(img),
                     "prompt": override.get(pid, v["subject"]) + tail,
                     "quality_override": 8000 if pid in small else 15000,
                     "texture_delight": pid in delight})
json.dump(plan, open("plan.json", "w"), indent=1)
for x in plan: print(x["prop"], len(x["prompt"]), x["quality_override"], x["texture_delight"])
