"""T44 prep: build the new scenes.json from the old one and the card objects in Docs/StoryDrafts/.

Usage, from the repo root, on the OLD scenes.json (it reads the _readme, set and notes from it):
    python Docs/tasks/T44-build/make_scenes.py . Content/NHOS/Data/scenes.json
On the scenes.json of commit 6ada2ab (T51: every note holds only id, category and note) it writes
the file Docs/tasks/T44-build/scenes.json holds. See Docs/tasks/T44-build.md."""
import json, sys
from pathlib import Path
repo = Path(sys.argv[1]); out = Path(sys.argv[2])
old = json.loads((repo / "Content/NHOS/Data/scenes.json").read_text(encoding="utf-8"))
ORDER = ["star_wars", "fellowship", "jurassic_park", "godfather", "pulp_fiction", "big_lebowski", "matrix"]
cards = [json.loads((repo / f"Docs/StoryDrafts/{n}.json").read_text(encoding="utf-8"))["card"] for n in ORDER]

# Fix 1 (T44 step 2): the simulation card's spare. Keep all four props (T39's art list keeps 28),
# and take the bent spoon out of the fortune-teller's want, so the spoon is a spare no want needs.
m = next(c for c in cards if c["id"] == "pick_a_pill")
ft = next(s for s in m["seats"] if s["role"] == "A fortune-teller baking cookies")
assert ft["want"] == "Stir your cookie dough with the bent spoon at the Back, then give the spoon to whoever you predict will pick the wrong pill."
ft["want"] = "Stir your cookie dough at the Back, then give a pill to whoever you predict will pick the wrong one."

readme = old["_readme"][:]
readme[1] = ("set: one stage for every story. 'places' are the only places an action may name, and the game turns any other name into 'looks around'. "
             "The places stand in for whatever a story needs, and each card's premise says what the Riser plays. The 'what' text of a place is public, like the rest of the set and the card. "
             "Keep the names short: the input LLM and the robots' actions (T19) use them. "
             "'props' is the shared list the game still sends as the state's set.props until T45 puts each card's own props on the Prop Table; T45 removes it.")
readme[2] = (readme[2].replace("The game sends actors only the card's title and premise, plus each seat's role and want.",
             "'props' is the four props the card brings to the Prop Table. A want names only its own card's props and the places, and at least one prop, the spare, is named by no want, so the card still works if the spare is dropped. "
             "The game sends actors only the card's title and premise, plus each seat's role and want (and, from T45, the card's props as set.props)."))
assert "'props' is the four props" in readme[2]
readme[4] = readme[4].replace("and each one must work in every story.", "and each one must work in every story, with any card's four props.")
assert "four props" in readme[4]

# T44 step 3: say_chicken names a prop no card has now. Its replacement works with any card and keeps
# say_chicken's category, Speech. A note holds only id, category and note (T51).
notes = []
for n in old["notes"]:
    assert set(n) == {"id", "category", "note"}, f"note {n.get('id')} is not in T51's form (id, category, note)"
    if n["id"] == "say_chicken":
        n = {"id": "favorite_prop", "category": "Speech", "note": "Mention your favorite prop every time you speak."}
    notes.append(n)
assert any(n["id"] == "favorite_prop" for n in notes), "no say_chicken note to replace"

def j(v): return json.dumps(v, ensure_ascii=False)
L = ["{", '\t"_readme": [']
L += [f"\t\t{j(r)}," for r in readme]; L[-1] = L[-1][:-1]
L += ["\t],", '\t"set": {', f'\t\t"id": {j(old["set"]["id"])},', f'\t\t"name": {j(old["set"]["name"])},', '\t\t"places": [']
L += [f'\t\t\t{{ "name": {j(p["name"])}, "what": {j(p["what"])} }},' for p in old["set"]["places"]]; L[-1] = L[-1][:-1]
L += ["\t\t],", f'\t\t"props": {j(old["set"]["props"])}'.replace('", "', '", "'), "\t},", '\t"cards": [']
for i, c in enumerate(cards):
    L += ["\t\t{", f'\t\t\t"id": {j(c["id"])},', f'\t\t\t"title": {j(c["title"])},', f'\t\t\t"premise": {j(c["premise"])},',
          f'\t\t\t"backdrop": {{ "id": {j(c["backdrop"]["id"])}, "what": {j(c["backdrop"]["what"])} }},',
          f'\t\t\t"props": {j(c["props"])},', '\t\t\t"seats": [']
    L += [f'\t\t\t\t{{ "role": {j(s["role"])}, "want": {j(s["want"])} }},' for s in c["seats"]]; L[-1] = L[-1][:-1]
    L += ["\t\t\t]", "\t\t}" + ("," if i < len(cards) - 1 else "")]
L += ["\t],", '\t"notes": [']
L += [f'\t\t{{ "id": {j(n["id"])}, "category": {j(n["category"])}, "note": {j(n["note"])} }},' for n in notes]; L[-1] = L[-1][:-1]
L += ["\t]", "}", ""]
out.write_text("\n".join(L), encoding="utf-8")
json.loads(out.read_text(encoding="utf-8"))
assert all(set(n) == {"id", "category", "note"} for n in json.loads(out.read_text(encoding="utf-8"))["notes"])
print("wrote", out)
