"""T99 round 1: four backdrop candidates per card. Runs Tools/art_gen.py image, seven in parallel."""
import subprocess, sys, concurrent.futures
STYLE = ("Stop-motion claymation style: hand-sculpted from matte modeling clay with faint thumbprints, soft rounded "
         "chunky forms, bold simple shapes and a clean readable silhouette, saturated slightly chalky colors, from the "
         "same world as a gold, crimson and cream 19th-century clay opera house. ")
COMP = (" A painted theater backdrop flat in shallow clay relief, wide 2:1 panoramic, seen straight on. Composition: "
        "the most interesting scenery sits in the upper left, the upper right and the middle band; the top center is "
        "calm and simple; the bottom third is a plain, simple, uncluttered floor or ground with no objects. Soft even "
        "frontal light with no strong light direction and no hard cast shadows; warm colors a little softer than the "
        "actors who will stand in front of it. No characters, no people, no robots, no animals, no text, no letters, "
        "no numbers, no signs, no logos.")
NEG = ("text, letters, words, numbers, signs, logo, watermark, brand mark, people, characters, person, robot, animals, "
       "creatures, realistic human face, hair, fur, thin wires, glossy plastic, chrome, photorealistic, ink outlines, "
       "flat 2D illustration, scary, gore, theater curtains, stage, proscenium, audience, frame, border, blurry")
SCENES = {
 "desert_planet": "A sandy orange desert at dusk under two glowing suns low on the horizon, one big and golden, one smaller and coral pink. Rolling dunes of chunky sculpted clay. On the left, a small rusty dome-shaped clay hut with a round wooden door. On the right, a battered, patched, boxy space truck with dents, rivets, a round cockpit window and stubby tail fins, resting on short landing legs. High in the lavender and dusty pink sky, a big pale gray moon with a tiny door and two little square windows, looking suspicious.",
 "dwarf_mine": "A vast abandoned underground dwarf mine: rows of tall chunky carved stone pillars fading into dusty darkness, a deep chasm across the middle spanned by one thick arched stone bridge, a warm tangerine glow rising from far below the bridge, a few wall torches, old wooden mine carts and abandoned pickaxes on the rocky ledges. Slate blue and deep plum shadows with glowing orange highlights, bright enough to read on a stage.",
 "jungle_park": "A steamy tropical island jungle: big rounded ferns and fat palm trees in deep green and teal; a sagging electric fence of thick ropes on chunky wooden posts, one post snapped; a tilted blank yellow warning sign showing only a simple three-toed footprint symbol; a trail of giant three-toed footprints pressed into brown mud; soft white puffs of mist; a small orange and brown volcano puffing one round smoke cloud on the far horizon; a warm late-afternoon sky in peach and turquoise.",
 "garden_wedding": "A sunny garden wedding party: a big red-and-white striped party tent, strings of round paper lanterns, a long banquet table with a white tablecloth and a tall tiered white wedding cake, potted lemon trees with fat yellow lemons, a pink stucco villa with green shutters and a terracotta roof, rolling green hills and puffy clay clouds in a bright blue sky.",
 "retro_diner": "A cozy retro roadside diner interior at night: a long clay counter with round cherry-red stools on the left, glass pie domes on the counter, a black-and-white checkered floor, turquoise and cream walls, plump red booths on the right, a big round wall clock with no numbers, a rounded jukebox glowing warm amber, wide windows showing a deep blue night sky with a fat clay moon.",
 "bowling_lanes": "A retro 1960s bowling alley on league night: honey-colored wooden lanes stretching back in forced perspective, neat triangles of chunky white bowling pins with red stripes at the end of each lane, a rounded ball return holding colorful clay bowling balls, a curved space-age ceiling dotted with starburst lamps, teal and tangerine geometric wall panels, a row of blank pale-blue scoring screens.",
 "midnight_cubicles": "A gloomy office floor after midnight: rows of low gray cubicle walls, chunky beige boxy computer monitors on desks, each screen glowing with soft green streaks trickling down like rain, one buzzing fluorescent ceiling light, a tall back window with blue rain streaks and a dark skyline of simple blocky buildings, a water cooler and a potted plant at the sides, deep teal and gray shadows with sickly green glow accents.",
}
def run(i):
    p = STYLE + SCENES[i] + COMP
    r = subprocess.run([sys.executable, "Tools/art_gen.py", "image", "--out", f"Local/art/T99/backdrops/{i}",
                        "--prompt", p, "--negative", NEG, "--width", "2048", "--height", "1024", "--count", "4"],
                       capture_output=True, text=True)
    return i, r.returncode, (r.stdout + r.stderr).strip()[-300:]
ids = sys.argv[1:] or list(SCENES)
with concurrent.futures.ThreadPoolExecutor(7) as ex:
    for i, code, out in ex.map(run, ids):
        print(i, code, out, flush=True)
