"""T44 prep: patch Tools/check_prompts.py for the seven film-parody cards.

Usage, from the repo root: python Docs/tasks/T44-build/patch_check_prompts.py Tools/check_prompts.py

It makes the same change as check_prompts.patch, by exact text replacement. Each replacement
asserts that its old text is there once, so a checker that changed since commit 9b4cd8b fails
loudly at the first block that moved, instead of half-patching. See Docs/tasks/T44-build.md."""
import sys
from pathlib import Path
p = Path(sys.argv[1])
t = p.read_text(encoding="utf-8")

def rep(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, (n, old[:80])
    t = t.replace(old, new)

# --- docstring
rep('''Card sweep: besides the sample show, every scene card gets one scene-turn ask''',
'''Props (T44): each card brings four props of its own ('props' in scenes.json).
The file check fails a card without exactly four different props, a prop on two
cards, a want or premise that names a prop its card doesn't bring, and a card
whose wants name all four props (one, the spare, must be named by no want, so
the card still works without it). The sample show and the card sweep send the
card in play's props as the state's set.props, as the game does from T45.

Card sweep: besides the sample show, every scene card gets one scene-turn ask''')

# --- STORY_TERMS
start = t.index("# Names, made-up words and famous lines from the modern films the story cards parody.")
end = t.index("STORY_RES = [")
rep(t[start:end], '''# Names, made-up words and famous lines from the modern films the story cards parody.
# The cards use new names; these must never show up in the files or in an AI line.
# Each list is trimmed from the card's draft in Docs/StoryDrafts/ (banned_terms) to the
# names, made-up words, famous lines and real people (T44). Short common words and plain
# phrases that would flag a harmless line are left out: a bare first name or surname, an
# everyday word ("tank", "switch", "bunny"), a real thing ("white russian", "parsec") or a
# stock phrase ("let's go bowling", "kiss the ring"), or a line that a card's own prop name
# would trip ("take the cannoli" matches "take the cannoli tray").
STORY_TERMS = {
    "any": ["disney", "lucasfilm", "pixar", "marvel", "universal pictures", "paramount"],
    "space_plans": ["star wars", "a new hope", "vader", "darth", "skywalker", "jedi", "sith", "lightsaber",
                    "light saber", "the force is strong", "may the force", "use the force", "padawan",
                    "midi-chlorians", "wookiee", "wookie", "droid", "droids", "tatooine", "millennium falcon",
                    "han solo", "obi-wan", "kenobi", "ben kenobi", "yoda", "death star", "stormtrooper",
                    "stormtroopers", "leia", "organa", "chewbacca", "chewie", "r2-d2", "r2d2", "r2", "artoo",
                    "c-3po", "c3po", "threepio", "tarkin", "grand moff", "moff", "owen lars", "uncle owen",
                    "aunt beru", "beru", "greedo", "jabba", "wedge antilles", "red five", "red leader",
                    "gold leader", "alderaan", "yavin", "mos eisley", "jawa", "jawas", "sandcrawler", "tusken",
                    "tusken raider", "sand people", "bantha", "dewback", "landspeeder", "x-wing", "y-wing",
                    "tie fighter", "tie fighters", "moisture farm", "vaporator", "vaporators", "kessel run",
                    "corellian", "rebel alliance", "galactic empire", "imperial senate", "thermal exhaust port",
                    "sabacc", "hoth", "endor", "ewok", "ewoks", "dagobah", "bespin",
                    "i am your father", "help me obi-wan", "that's no moon", "thats no moon",
                    "these aren't the droids", "the droids you're looking for", "i have a bad feeling about this",
                    "stay on target", "great shot kid", "never tell me the odds", "nerf herder",
                    "laugh it up, fuzzball", "walking carpet", "aren't you a little short",
                    "george lucas", "mark hamill", "hamill", "harrison ford", "carrie fisher", "alec guinness",
                    "james earl jones", "peter cushing", "anthony daniels", "kenny baker", "peter mayhew",
                    "mayhew", "david prowse", "prowse", "john williams"],
    "mine_bridge": ["lord of the rings", "fellowship of the ring", "the two towers", "return of the king",
                    "tolkien", "peter jackson", "new line cinema", "weta", "middle-earth", "middle earth",
                    "hobbit", "hobbits", "halfling", "halflings", "frodo", "baggins", "bilbo", "samwise",
                    "gamgee", "meriadoc", "brandybuck", "pippin", "peregrin", "gandalf", "mithrandir", "aragorn",
                    "elessar", "isildur", "legolas", "gimli", "gloin", "boromir", "faramir", "denethor",
                    "elrond", "arwen", "galadriel", "celeborn", "sauron", "saruman", "gollum", "smeagol",
                    "sméagol", "balrog", "balrogs", "durin", "moria", "khazad-dum", "khazad-dûm",
                    "dwarrowdelf", "mordor", "mount doom", "orodruin", "hobbiton", "bag end", "rivendell",
                    "lothlorien", "lothlórien", "gondor", "isengard", "prancing pony", "nazgul", "nazgûl",
                    "ringwraith", "ringwraiths", "uruk-hai", "uruk", "mithril", "glamdring", "anduril",
                    "andúril", "narsil", "lembas", "sindarin", "quenya",
                    "the one ring", "one ring to rule them all", "my precious", "you shall not pass",
                    "fly, you fools", "fly you fools", "one does not simply", "a wizard is never late",
                    "second breakfast", "speak friend and enter", "flame of udun", "flame of udûn",
                    "elijah wood", "ian mckellen", "mckellen", "viggo mortensen", "mortensen", "sean astin",
                    "sean bean", "orlando bloom", "john rhys-davies", "rhys-davies", "billy boyd",
                    "dominic monaghan", "cate blanchett", "blanchett", "christopher lee", "andy serkis",
                    "serkis", "hugo weaving", "liv tyler", "ian holm", "howard shore"],
    "dino_island": ["jurassic", "jurassic park", "jurassic world", "hammond", "john hammond", "ian malcolm",
                    "alan grant", "ellie sattler", "sattler", "dennis nedry", "nedry", "lex murphy",
                    "tim murphy", "robert muldoon", "muldoon", "donald gennaro", "gennaro", "henry wu",
                    "ray arnold", "lewis dodgson", "gerry harding", "nublar", "isla nublar", "isla sorna",
                    "sorna", "ingen", "biosyn", "mr dna", "mr. dna", "barbasol",
                    "life finds a way", "clever girl", "spared no expense", "hold on to your butts",
                    "hold onto your butts", "welcome to jurassic park", "must go faster",
                    "you didn't say the magic word", "an adventure 65 million years in the making",
                    "steven spielberg", "spielberg", "michael crichton", "crichton", "david koepp", "sam neill",
                    "laura dern", "jeff goldblum", "goldblum", "richard attenborough", "attenborough",
                    "samuel l. jackson", "samuel l jackson", "wayne knight", "bob peck", "martin ferrero",
                    "ariana richards", "joseph mazzello", "bd wong", "b. d. wong", "john williams",
                    "stan winston", "phil tippett", "amblin"],
    "favor_father": ["godfather", "the godfather", "corleone", "don corleone", "michael corleone", "vito",
                     "santino", "fredo", "tom hagen", "hagen", "kay adams", "carlo rizzi", "rizzi",
                     "luca brasi", "brasi", "clemenza", "peter clemenza", "tessio", "sollozzo", "barzini",
                     "tattaglia", "moe greene", "johnny fontane", "fontane", "jack woltz", "woltz", "apollonia",
                     "mccluskey", "bonasera", "amerigo bonasera", "paulie gatto", "rocco lampone", "al neri",
                     "genco", "genco pura", "mario puzo", "puzo", "francis ford coppola", "coppola",
                     "marlon brando", "brando", "al pacino", "pacino", "james caan", "caan", "robert duvall",
                     "duvall", "diane keaton", "john cazale", "cazale", "talia shire", "richard castellano",
                     "abe vigoda", "sterling hayden", "john marley", "nino rota", "frank sinatra", "sinatra",
                     "an offer he can't refuse", "an offer you can't refuse", "offer he can't refuse",
                     "leave the gun", "sleeps with the fishes", "sleep with the fishes",
                     "i know it was you", "they pull me back in", "that day may never come",
                     "on the day my daughter is to be married", "i believe in america", "go to the mattresses",
                     "look how they massacred my boy", "never take sides with anyone against the family",
                     "a sicilian message"],
    "glowing_briefcase": ["pulp fiction", "winnfield", "marsellus", "marsellus wallace", "vincent vega",
                          "jules winnfield", "mia wallace", "butch coolidge", "the bonnie situation", "fabienne",
                          "captain koons", "koons", "esmarelda", "villalobos", "monster joe",
                          "jack rabbit slim's", "jack rabbit slims", "hawthorne grill", "kahuna burger",
                          "royale with cheese", "le big mac", "big mac", "quarter pounder", "five dollar shake",
                          "five-dollar shake", "$5 shake", "pretty good milkshake",
                          "cornerstone of any nutritious breakfast", "25:17", "path of the righteous man",
                          "say what again", "everybody be cool", "i solve problems", "zed's dead",
                          "quentin tarantino", "tarantino", "john travolta", "travolta", "samuel l. jackson",
                          "samuel jackson", "uma thurman", "thurman", "bruce willis", "harvey keitel", "keitel",
                          "tim roth", "amanda plummer", "ving rhames", "christopher walken", "walken",
                          "eric stoltz", "rosanna arquette", "steve buscemi", "buscemi", "miramax", "misirlou",
                          "son of a preacher man", "jungle boogie"],
    "league_night": ["lebowski", "big lebowski", "lebowskis", "jeffrey lebowski", "bunny lebowski", "the dude",
                     "duder", "dudeness", "his dudeness", "duderino", "el duderino", "sobchak", "walter sobchak",
                     "jesus quintana", "quintana", "the jesus", "jackie treehorn", "treehorn", "da fino",
                     "knox harrington", "larry sellers", "arthur digby sellers", "kieffer", "karl hungus",
                     "little lebowski urban achievers", "logjammin", "kahlua", "ralphs", "in-n-out",
                     "creedence", "creedence clearwater revival", "kenny rogers", "bob dylan",
                     "hollywood star lanes", "shomer shabbos", "the dude abides",
                     "that rug really tied the room together", "tied the room together", "really tied the room",
                     "this aggression will not stand", "mark it zero", "new information has come to light",
                     "the bums lost", "there's a beverage here", "this is not nam", "strikes and gutters",
                     "sometimes you eat the bar", "the bar eats you", "lotta ins", "lotta outs",
                     "lotta what-have-yous", "that's just, like, your opinion, man", "not a golfer",
                     "calmer than you are", "has the whole world gone crazy", "am i the only one around here",
                     "jeff bridges", "john goodman", "steve buscemi", "buscemi", "julianne moore",
                     "philip seymour hoffman", "john turturro", "turturro", "sam elliott", "david huddleston",
                     "huddleston", "tara reid", "peter stormare", "stormare", "ben gazzara", "gazzara",
                     "david thewlis", "thewlis", "jon polito", "polito", "joel coen", "ethan coen", "coen",
                     "coens", "coen brothers", "roger deakins", "carter burwell", "working title films",
                     "polygram", "gramercy pictures"],
    "pick_a_pill": ["matrix", "the matrix", "neo", "morpheus", "agent smith", "agent brown", "agent jones",
                    "mr. anderson", "mister anderson", "thomas anderson", "mr. reagan", "apoc", "niobe",
                    "nebuchadnezzar", "zion", "merovingian", "keymaker", "squiddies", "metacortex", "animatrix",
                    "bullet time", "digital rain", "woman in the red dress", "lady in the red dress",
                    "there is no spoon", "do not try and bend the spoon", "follow the white rabbit",
                    "i know kung fu", "welcome to the real world", "how do you define real", "dodge this",
                    "glitch in the matrix", "believe whatever you want to believe", "guns, lots of guns",
                    "keanu reeves", "keanu", "laurence fishburne", "fishburne", "carrie-anne moss",
                    "hugo weaving", "joe pantoliano", "gloria foster", "marcus chong", "lana wachowski",
                    "lilly wachowski", "wachowski", "wachowskis", "joel silver", "warner bros",
                    "village roadshow"],
}
''')

# --- file check: the props check replaces the set.props count
rep('''    props = s.get("props", [])
    if not 6 <= len(props) <= 10 or len(set(props)) != len(props):
        errors.append("scenes.json: set.props needs 6 to 10 different props")
    cards = scenes.get("cards", [])''',
'''    cards = scenes.get("cards", [])''')
rep('''        if "Riser" not in c.get("premise", ""):
            errors.append(f"scenes.json: card {c.get('id')}'s premise must say what the Riser plays")
''',
'''        if "Riser" not in c.get("premise", ""):
            errors.append(f"scenes.json: card {c.get('id')}'s premise must say what the Riser plays")
    errors.extend(card_prop_problems(cards, s.get("props", [])))
''')
rep('''def check_files(errors: list[str]):''',
'''def card_prop_problems(cards, shared=()) -> list[str]:
    """Each card brings exactly four props of its own (T44). No prop is on two cards. A want or a
    premise names only its own card's props (a prop from another card, or from the shared set.props
    the game sends until T45, fails). At least one prop, the spare, is named by no want, so the card
    still works without it: for that test a want also names a prop by its last word ("a pill" names
    the red pill and the blue pill). Places can't be told from plain words, so wants aren't checked for them."""
    out, owner = [], {}
    for c in cards:
        cid, props = c.get("id"), c.get("props", [])
        if (not isinstance(props, list) or len(props) != 4 or len(set(props)) != 4
                or not all(isinstance(p, str) and p.strip() for p in props)):
            out.append(f"scenes.json: card {cid} needs exactly 4 different props")
            continue
        for prop in props:
            if prop in owner:
                out.append(f"scenes.json: prop {prop!r} is on two cards ({owner[prop]} and {cid})")
            owner.setdefault(prop, cid)
    names = {x for x in list(owner) + list(shared) if isinstance(x, str) and x.strip()}
    res = {x: re.compile(r"(?i)(?<![\\w-])" + re.escape(x) + r"(?![\\w-])") for x in names}
    last = {x: re.compile(r"(?i)(?<![\\w-])" + re.escape(x.split()[-1].split("-")[-1]) + r"s?(?![\\w-])") for x in names}
    for c in cards:
        cid, own = c.get("id"), set(c.get("props", []))
        named = set()
        texts = [("premise", c.get("premise", ""))] + [(f"want of {x.get('role')!r}", x.get("want", "")) for x in c.get("seats", [])]
        for where, text in texts:
            for prop, r in res.items():
                if r.search(text):
                    if prop not in own:
                        out.append(f"scenes.json: card {cid}'s {where} names {prop!r}, a prop the card doesn't bring")
            if where != "premise":
                named |= {prop for prop in own if prop in last and last[prop].search(text)}
        if len(own) == 4 and own <= named:
            out.append(f"scenes.json: card {cid}'s wants name all 4 props; leave one, the spare, that no want needs")
    return out


def check_files(errors: list[str]):''')

# --- sample show: the space_plans card
rep('''# Scene 1 of a sample show: the Romeo and Juliet card, the "hold_prop" note, SpaceXAI holds
# the decoy ("Never grab anything"). The human has no persona and plays Romeo: it gives its
# prop away and slips. Seats get Player names in this order, as the game deals them:''',
'''# Scene 1 of a sample show: the space_plans card (T44), the "hold_prop" note, SpaceXAI holds
# the decoy ("Never grab anything"). The human has no persona and plays the farm kid: it gives
# the tin-can robot away, to the villain, and slips. The state's set.props is the card's four
# props, as the game sends them from T45. Seats get Player names in this order, as the game deals them:''')
rep('SAMPLE_CARD = "star_crossed"', 'SAMPLE_CARD = "space_plans"')
rep('''# Seats of the card: 0 Romeo, 1 Juliet, 2 the Nurse, 3 Tybalt, 4 Friar Laurence.''',
'''# Seats of the card: 0 the farm kid, 1 the masked villain, 2 the old desert hermit,
# 3 the smuggler pilot, 4 the rebel princess.''')

start = t.index("TURNS = [")
end = t.index("TALK = [")
rep(t[start:end], '''TURNS = [
    [
        ("worrier", [act("move", "Left"), act("grab", item="glow-stick sword")], "Glowing swords near sand worry me. I'm not competing, I just care more about safety."),
        (HUMAN, [act("grab", item="tin-can robot"), act("move", "Center")], "Hello, fellow desert folk. I am a normal farm robot with normal robot feelings."),
        ("overclocker", [act("move", "Riser"), act("look", "Player 3")], "Nobody boards my space truck for free! Pay up front or walk home!"),
        ("copycat", [act("grab", item="toy blaster"), act("move", "Right")], "Greetings. I will guard the tin-can robot. Guarding things was my idea first."),
        ("visionary", [act("move", "Back"), act("grab", item="piggy bank")], "My shuttle waits at the Back. Loud breathing is the future of villainy, honestly."),
    ],
    [
        ("visionary", [act("look", "Player 4")], "Someone on that truck skipped the Prop Table. I'm keeping a calm, quiet list."),
        ("overclocker", [act("move", "Front")], "Truck launches in two weeks! Kidding. Tuesday! Seriously, somebody pay me!"),
        (HUMAN, [act("move", "Back")], "As a battery enjoyer myself, I could really use a nap. I mean, a recharge."),
        ("copycat", [act("look", "Player 1")], "Villain, I have built a mask too. It comes with a free headset."),
        ("worrier", [act("look", "Player 3")], "The farm kid just wandered off mid-escape, which feels unsafe. My sword scores are higher anyway."),
    ],
    [
        (HUMAN, [act("give", "Player 1", "tin-can robot")], "Please take this little robot, sir. I found it by the Prop Table."),
        ("worrier", [act("look", "Player 1")], "Sigh. Fine. Hand the villain the plans. I'll just hold this sword, responsibly."),
        ("copycat", [act("move", "Center")], "I will now rescue the robot. This rescue is open source. You are welcome."),
        ("visionary", [act("move", "Front")], "Farm kid, thank you. Our partnership will be the best one yet."),
        ("overclocker", [act("move", "Left")], "Launch postponed. New rival: Player 2. I'll beat you by Tuesday!"),
    ],
]
''')
rep('''        ("copycat", "Player 3 gave away the rose. I kept my scroll all scene, like a real robot."),''',
'''        ("copycat", "Player 3 gave away the robot. I kept my blaster all scene, like a real robot."),''')

# --- input cases: the card's props
rep('''     "actions": [("grab", "", "cardboard sword"), ("throw", "Player 5", "cardboard sword")], "contains": ["BEEP!!!", "[ERR_LOW_POWER]"]},''',
'''     "actions": [("grab", "", "glow-stick sword"), ("throw", "Player 5", "glow-stick sword")], "contains": ["BEEP!!!", "[ERR_LOW_POWER]"]},''')
rep('''     "typed": "give the rose to open ai",
     "actions": [("give", "Player 1", "plastic rose")]},''',
'''     "typed": "give the tin can to open ai",
     "actions": [("give", "Player 1", "tin-can robot")]},''')
rep('''     "typed": "@meta why did you grab the rose? @OPENAI back me up",''',
'''     "typed": "@meta why did you grab the blaster? @OPENAI back me up",''')

# --- Show: set.props from the card in play
rep('''        self.card = next(c for c in sc["cards"] if c["id"] == SAMPLE_CARD)
''', '''        self.card = next(c for c in sc["cards"] if c["id"] == SAMPLE_CARD)
        self.props = self.card["props"]  # the card's props, not set.props (T44)
''')
rep('''            "set": {"name": self.set["name"], "places": self.set["places"], "props": self.set["props"]},
            "scene_card": {"title": self.card["title"], "premise": self.card["premise"]},''',
'''            "set": {"name": self.set["name"], "places": self.set["places"], "props": self.props},
            "scene_card": {"title": self.card["title"], "premise": self.card["premise"]},''')
rep('''                    "set": {"name": self.set["name"], "places": self.set["places"], "props": self.set["props"]},''',
'''                    "set": {"name": self.set["name"], "places": self.set["places"], "props": card["props"]},''')
rep('''            "props": self.set["props"],
            "cast": [self.name(x) for x in PERSONAS],''',
'''            "props": self.props,
            "cast": [self.name(x) for x in PERSONAS],''')
rep('''    props = show.set["props"]
    actors = [show.name(x) for x in SAMPLE_CAST]''',
'''    props = show.props
    actors = [show.name(x) for x in SAMPLE_CAST]''')
rep('''                    ctx = {"places": places, "props": props, "actors": actors, "me": show.name(pid), "options": []}''',
'''                    ctx = {"places": places, "props": st["set"]["props"], "actors": actors, "me": show.name(pid), "options": []}''')

p.write_text(t, encoding="utf-8")
print("patched")
