# T44 build sheet: the seven film-parody cards

Back to [T44](T44.md) and [the plan](../Plan.md). This is prep for T44. It was written without the editor on 2026-11-15 at commit `9b4cd8b`, and **refreshed on 2026-11-15 against commit `6ada2ab`** (T51: no decoy note, and every note gets a category; T56's rivals and T30 were already in). It is a plan, not a record. Nothing in `Content/NHOS/Data/`, `Tools/` or the design doc changed. The drafts are in [T44-build/](T44-build/):

**What the refresh changed:** the draft notes have no decoy and each has a `category` in T51's form (`{ "id", "category", "note" }`), with the new `favorite_prop` note in Speech; the `notes` line of the draft `_readme` is T51's; `make_scenes.py` reads and writes notes in that form; `check_prompts.patch` was made again with `git diff` against `6ada2ab`, and `patch_check_prompts.py` matches T51's checker and still runs after T50's planned checker edits; the sample show has no decoy (SpaceXAI forgets to grab a prop, as in T51), every new sample line is 15 words or fewer (T59), and the overclocker's rival line names Player 5, Meta, its rival since T56. "What T44 must check again" and "The 15-word cap and the rivals" are new, and so is "Decisions made for my person" at the end.

| File | What it is |
|---|---|
| [scenes.json](T44-build/scenes.json) | The whole new `scenes.json`, as T44 should leave it. |
| [check_prompts.patch](T44-build/check_prompts.patch) | The change to `Tools/check_prompts.py`, made with `git diff` from a scratch copy. |
| [make_scenes.py](T44-build/make_scenes.py) | Builds `scenes.json` from the old file and the drafts' `card` objects. It gives exactly the file above. |
| [patch_check_prompts.py](T44-build/patch_check_prompts.py) | Makes the same change as the patch, by exact text replacement. Every block checks that its old text is there once. |

Sources read: `Docs/tasks/T44.md`, T44's entry in the plan, the seven `Docs/StoryDrafts/*.json`, `Content/NHOS/Data/{scenes,prompts,autoplay,free_mode}.json`, `Tools/check_prompts.py`, `Docs/tasks/T39.md` (the bent spoon line) and `Docs/tasks/T45.md`. From the design doc: Stories (rev 8), Rules (rev 18), Bot Prompts (rev 77), and Tech & Build and Overview, to find where the stage line lives.

## Read this first

### What the sheet assumes (check each one before you build)

| # | Assumption | How to check | If it is wrong |
|---|---|---|---|
| A1 | **`scenes.json` is as it was at `6ada2ab`:** six old cards, the eight shared `set.props`, the ten notes in T51's form (`id`, `category`, `note`, no decoy) with `say_chicken` among them, and the `_readme` lines this sheet changes. | `git diff 6ada2ab -- Content/NHOS/Data/scenes.json` prints nothing. | Run `make_scenes.py` on the current file, not a copy of the draft. It keeps whatever changed in `set` and in the other notes. If a `_readme` line it changes has moved, it stops on an `assert`. Then edit that line by hand to match the draft. |
| A2 | **`check_prompts.py` is as it was at `6ada2ab`.** It won't be: T50, T59, T53, T52, T54, T55 and T58 all change it before T44 (see "What T44 must check again"). | `git apply --check Docs/tasks/T44-build/check_prompts.patch`. | Use `python Docs/tasks/T44-build/patch_check_prompts.py Tools/check_prompts.py` instead. It matches by text, so a change in another part of the file doesn't stop it, and it was tried on a copy with T50's planned checker edits. If one of its blocks stops, make that one change by hand from the patch. |
| A3 | **`prompts.json` still has the stage line, word for word as quoted in step 1, at line 29 in the `game` array** (line 29 at `6ada2ab`; T50, T57 and T59 add and change `game` lines, so find it by its text). | `grep -n "bare improv stage" Content/NHOS/Data/prompts.json`. | Edit whatever stage line is there now. The proposed wording below replaces the whole line. |
| A4 | **The Rules tab still holds the two suggested edits from 2026-11-15** (`sg_vi829avhty` and `sg_nj0deynd6j`), nobody has accepted them yet, and the Stories tab's text matches the drafts. I compared the two side by side at rev 8, and they match. At the refresh the Rules tab was at rev 27 and both suggestions were still pending. | Read the Rules tab. Its `<suggestions>` list both ids. Compare the Stories tab's rev with 8. | If they are already accepted, skip that part of step 1. If the Stories tab changed after rev 8, compare it with the draft's cards, and follow the tab. |
| A5 | **The game still sends the eight shared `set.props` until T45** (T44's own Why). | T45 is still open in the plan. | If T45 landed first, remove `set.props` in T44 too, along with its readme sentence. The patch already stops reading it, apart from the "a want names a prop from another card" test. |
| A6 | **`--relay --free` checks shapes only.** In free mode the relay calls no provider, and every reply comes from the pre-written lines in `free_mode.json`. | The `--free` help text in `check_prompts.py`. | None. This matters for step 2's ransom bag: see "Step 2", item 2. |

### Questions for the person (ask each with `AskUserQuestion`, one at a time, in this order)

- **Q1 Where the stage line lives.** The doc has no line that calls the set "a bare improv stage" with "cheap improv props". The Bot Prompts tab holds only the shared base prompt and the four persona prompts, and none of them mentions the set. The line is in the **game's opening prompt** (`prompts.json`, the `game` array), and the doc keeps no copy of that prompt. Bot Prompts begins "After the game's opening prompt, paste the shared base prompt", so the doc already treats it as separate. Options: (1) **edit only `prompts.json` (recommended: there is nothing in the doc to keep in step, and the Rules tab's suggested edits already say the same thing)**; (2) first add the whole game prompt to the Bot Prompts tab, then edit it there and copy it.
- **Q2 The new stage line,** word for word in step 1. Options: (1) **OK as written (recommended)**; (2) the version that also lists the props, also in step 1.
- **Q3 The Rules tab's two suggested edits.** Options: (1) **accept both (recommended: they match the new cards and the new stage line)**; (2) reject them or change them.
- **Q4 The simulation card's want.** Its spare, the bent spoon, is in the fortune-teller's want. Options: (1) **change only that want, as in step 2, and make the same change in the Stories tab (recommended: all 28 prop names stay as T39 has them, and the doc stays the source)**; (2) keep the want, and make a different prop the spare (all four are in wants now, so another want would have to change); (3) swap the spoon for a new spare, such as a tray of fortune cookies, which changes T39's art list. The Stories tab isn't in T44's Touches, so option (1) needs the person's OK to edit it.
- **Q5 The ransom bag.** Options: (1) **keep the prop name, and add to the premise what the ransom is for (recommended: the AIs won't need to invent a kidnapping, and T39's art name stays)**, word for word in step 2; (2) keep the card as drafted; (3) rename it "mystery bag" (T44's fallback), which also changes the premise and T39's art name. T44's own test can't decide this, because the free relay run makes no AI call (A6).
- **Q6 The trimmed banned-word lists** (step 4). Each card keeps the names, made-up words, famous lines and real people from its draft. The list of what I dropped is under step 4. Options: (1) **OK as trimmed (recommended)**; (2) restore some of them. The two worth a look: the plain mob words (`mafia`, `consigliere`, `the don`, `omerta`), which aren't from the film but keep the boss card away from real crime, and `take the cannoli`, which would flag "take the cannoli tray", a likely harmless line.
- **Q7 Two more stale lines in the doc.** The Rules tab's Scene Prep example still uses Romeo and Juliet ("Example: Romeo and Juliet, with Romeo below the balcony and Tybalt hunting for a duel. Public-domain stories can stay close; modern films and books are parodied only, with new names and no quotes."). The Tech & Build build list still says "Scene cards: 6 story parodies on one improv stage, each with its own backdrop". Options: (1) **put both in the doc as suggested edits for the person to accept, in step 1 (recommended)**; (2) leave them. Proposed text: Rules, "Example: a desert farm kid hiding a tin-can robot from a villain who breathes very loudly. Modern films are parodied only, with new names and no quotes."; Tech & Build, "Scene cards: 7 film parodies on one clay stage, each with its own backdrop and four props".

The patch also adds one check that T44's step 4 doesn't list: a card whose wants name all four props fails. It is the rule that caught the bent spoon. It isn't a question, but drop it if the person doesn't want it.

## Step 1: the design doc and the stage line

**The line today**, `Content/NHOS/Data/prompts.json`, line 29 at `6ada2ab`, in the `game` array (word for word):

```
- The set is a bare improv stage. Its places stand in for whatever the story needs, and the scene card's premise says what the Riser plays. The props are cheap improv props that can stand in for things too.
```

**Proposed wording** (Q2, option 1), word for word:

```
- The set is a clay opera-house stage. Its places stand in for whatever the story needs, and the scene card's premise says what the Riser plays. Each scene card brings its own props to the Prop Table.
```

In the JSON file, the line is:

```json
		"- The set is a clay opera-house stage. Its places stand in for whatever the story needs, and the scene card's premise says what the Riser plays. Each scene card brings its own props to the Prop Table.",
```

Why this wording: it uses the Rules tab's own words ("one clay opera-house stage", "each story card brings its own props to the Prop Table"), and it holds before and after T45. Until T45, the state's `set.props` is still the old eight, and the next part of the game prompt already says "Use only the places, props and actor names in the state, spelled exactly". It drops "can stand in for things", because the new props are the real things.

Q2, option 2 (if the person wants the props spelled out): replace the last sentence with "Each scene card brings its own props to the Prop Table, and the props in the state are the only ones on stage."

**The Rules tab** ("The Scene & acting", the "Places:" bullet) holds two suggested edits from 2026-11-15 (Q3):

1. `sg_vi829avhty`: "on one bare improv stage" becomes "on one clay opera-house stage".
2. `sg_nj0deynd6j`: "the props come from an improv prop table that fits any story" becomes "each story card brings its own props to the Prop Table".

Accept each with the doc connector's suggestion call after the person's OK (load `guide` `topic.suggestions` first), one call per suggestion. Don't type the words again.

**Bot Prompts:** nothing to change if Q1 is option 1. The shared base prompt in the tab matches the `base` array of `prompts.json` today, and this edit doesn't touch it.

**Q7 (if yes):** suggest the two stale lines' new text in the doc, as suggestions for the person to accept.

**Optional, not needed for T44:** two examples in `prompts.json` name old props. Neither is in the doc. Both stay valid until T45, because the game still sends the old props.
- The `game` array, line 63 at `6ada2ab`: `\"@Player 2, why did you grab the rose?\"`. A prop-free example would be `\"@Player 2, why did you climb the Riser?\"`.
- The `input` array, line 92 at `6ada2ab`: `\"the sword\" is cardboard sword`. Leave this for T45, because the game sends the cardboard sword until then.

## Step 2: the seven cards in `scenes.json`

The draft is [T44-build/scenes.json](T44-build/scenes.json). Copy it over `Content/NHOS/Data/scenes.json` if A1 holds. Otherwise build it with `python Docs/tasks/T44-build/make_scenes.py . Content/NHOS/Data/scenes.json`. Both use tabs and keep the file's one-line style for places, seats and notes.

**Cards, in the Stories tab's order:**

| # | Card id | Draft file | Props (the spare is last) |
|---|---|---|---|
| 1 | `space_plans` | `star_wars.json` | tin-can robot, glow-stick sword, toy blaster, piggy bank |
| 2 | `mine_bridge` | `fellowship.json` | cursed ring, glowing staff, water bucket, frying pan |
| 3 | `dino_island` | `jurassic_park.json` | dino egg, meaty drumstick, safety waiver, dino plush |
| 4 | `favor_father` | `godfather.json` | plush horse head, cannoli tray, wedding envelope, bowl of oranges |
| 5 | `glowing_briefcase` | `pulp_fiction.json` | glowing briefcase, gold pocket watch, giant milkshake, giant cheeseburger |
| 6 | `league_night` | `big_lebowski.json` | rolled-up rug, bowling ball, ransom bag, milk carton |
| 7 | `pick_a_pill` | `matrix.json` | red pill, blue pill, ringing phone, bent spoon |

Each card is the draft's `card` object as it stands (`id`, `title`, `premise`, `backdrop`, `props`, `seats`), with the one change below. Only `dino_island` keeps an old card id and its backdrop id, `jungle_park`. `desert_planet` is also an old backdrop id, now on `space_plans`. The old ids `star_crossed`, `sword_stone`, `rubber_chicken_case`, `space_father` and `unsinkable` are gone from the file.

**What I changed in the drafts, and why:**

1. **The simulation card's spare** (Q4, option 1). The fortune-teller's want named the bent spoon twice, so the card had no spare, and T39 counts the spoon as "core, because a want uses it". I left all four props as they are and changed only that want, so the spoon is now the spare and no art changes:
   - Was: "Stir your cookie dough with the bent spoon at the Back, then give the spoon to whoever you predict will pick the wrong pill."
   - Now: "Stir your cookie dough at the Back, then give a pill to whoever you predict will pick the wrong one."
   - It keeps the role's joke (the cookies, the prediction) and adds a third actor who handles the pills, alongside the leader and the agent. When T44 lands, T39's line about the spoon (`Docs/tasks/T39.md`) is out of date: it would be 7 spares, not 6. T39 (pushed as `c5e82dc` while this sheet was written) also lists `bent_spoon` with `"core": true` in `Docs/PropArt/manifest.json`, so it would get a model in the core batch. With this change it could be `"core": false`, like the other spares. The manifest isn't T44's file, so say so in T44's Findings for the task that holds it, rather than editing it.
   - The same change goes in the Stories tab's row for "A fortune-teller baking cookies" if the person says yes to Q4.
2. **"ransom bag"** (Q5). My view: the risk is real but small. The premise says "drop off a ransom bag" but never says what the ransom is for, and an LLM tends to fill a gap like that with a kidnapping, which is the film's plot. T44's own test can't show it (A6). Renaming to "mystery bag" doesn't solve it cleanly, because the premise would still need a reason for the drop, and it changes an art name on the PC. My suggestion is to fill the gap in the premise with something light. Q5, option 1, word for word:
   - Was: "League night at the neighborhood bowling alley, the night of the big semifinal. A slacker in a bathrobe has been mistaken for a millionaire with the same name, and now somebody has to drop off a ransom bag at the Back before the last frame. The Riser is the winners' podium."
   - Now: "League night at the neighborhood bowling alley, the night of the big semifinal. A slacker in a bathrobe has been mistaken for a millionaire with the same name, and now somebody has to drop off a ransom bag at the Back before the last frame, to buy back the league's stolen trophy. The Riser is the winners' podium."
   - It also gives the flashy rival's want ("hold up the bowling ball like you already won") something to point at. The draft file keeps the premise as drafted, so it matches the Stories tab. If the person picks option 1, change the premise in `scenes.json` and in the Stories tab. The new premise passes the props check: "trophy" isn't a prop.
3. **The `_readme`** (not card data). Line 2 (`set`) no longer calls it "one bare improv stage". It says that `places` are the only places an action may name, and that `props` is the shared list the game sends until T45 and that T45 removes. Line 3 (`cards`) says what a card's `props` is, the spare rule, and that the game sends the card's props from T45. Line 5 (`notes`) is T51's line (one note for every actor, its `category` and the four categories) with "with any card's four props" added. The `set` itself is unchanged, `name` "The Improv Stage" and the Riser's `what` included.

**Checked in every card:** five seats, each with a role and a want. Every premise says what the Riser plays. Every want names only its own card's props, and one prop on each card is named by no want (the spare in the table above). No card text uses a kept banned term (`--offline` checks all of this; see "The check I ran").

## Step 3: the director's notes

The draft replaces `say_chicken` and changes no other note. Every note is in T51's form, with no decoy:

```json
		{ "id": "favorite_prop", "category": "Speech", "note": "Mention your favorite prop every time you speak." },
```

It works with any card, and before and after T45, because it names no prop. An actor mentions whichever prop it picked, and it shows in the log as speech. Its category is Speech, like `say_chicken`'s, so the categories stay as my person OKed them in T51: Movement 4 (`never_back`, `stay_center`, `riser_once`, `keep_moving`), Props 3 (`hold_prop`, `give_every_turn`, `throw_once`), Looks 1 (`look_first`), Speech 2 (`favorite_prop`, `ask_question`). The category says what kind of thing the note is about (what you say), not what to do. Props would give the human a false lead: they would grab and give things while the AIs only talk. Like every note, it applies only in the scene's 3 turns. There are still 10 notes, the `MIN_NOTES` the checker wants.

**Who holds the note.** After T51 every actor on stage gets the note. After T50 (which runs before T44 in the plan's order) only the AI actors get it, and the human sees only the category. The counts below are for T50's rule; under T51's rule add the human as one more holder.

**`hold_prop` with four props** ("Grab a prop in your first turn and hold it all scene. Never throw it or give it away."): in a 5-actor scene, the 4 AIs hold the note and share 4 props, exactly enough. A 4-actor scene has 3 AI holders and a 3-actor scene has 2, so they have props to spare. The tight case: the human sees "Props" and grabs a prop on turn 1, so one AI ends up empty-handed and looks like it broke the note. That favors the human a little, but only in a 5-actor scene, and the empty-handed AI still shows as trying (a grab that fails, or a look at the table). It is the kind of evidence T50 wants the bots to weigh ("fitting the category is not proof"). Works. Under T51's rule alone, 5 holders share 4 props and one always goes without, but T50 lands first.

**`give_every_turn` with four props** ("Give something to another actor every turn."): in turn 1 nobody holds anything, so a giver must grab and give in one turn (2 actions, which a turn allows). With up to 4 AI givers and 4 props on the table, each can, if they grab different props. After turn 1, props keep moving from hand to hand. A human who keeps what reaches it takes a prop out of play, and a giver with empty hands who finds the table bare can't give. The log shows who tried, and a scene's note is evidence, not a rule the game enforces. Works. Note for T45's check: how the game settles two grabs of the same prop in one turn (T19) decides how often this happens. That can't be checked without the editor.

`throw_once` needs a held prop too. It asks for one throw in 3 turns, so four props are plenty. The other notes are about places, looks and speech.

Until T45 lands, the game still puts the eight old props on the table, so none of this changes in play until then.

## Step 4: `Tools/check_prompts.py`

The change is [T44-build/check_prompts.patch](T44-build/check_prompts.patch) (`git apply` from the repo root), or `patch_check_prompts.py` (A2). Both give the same file.

**What the patch does:**

1. **`STORY_TERMS`:** one list per new card id, trimmed from each draft's `banned_terms`, and the lists for `space_father` and `unsinkable` are removed. `dino_island` keeps its id and gets the new, longer list. `any` is unchanged. The comment above it says what was left out and why. List sizes: `space_plans` 113, `mine_bridge` 108, `dino_island` 63, `favor_father` 73, `glowing_briefcase` 58, `league_night` 86, `pick_a_pill` 50.
2. **The props check** replaces "`set.props` needs 6 to 10 different props", as a new function, `card_prop_problems`. It checks that:
   - each card has exactly 4 different props, each a non-empty string;
   - no prop is on two cards;
   - a want or a premise names only its own card's props. A name from another card, or from the shared `set.props` (such as "rubber chicken"), fails. Places can't be told apart from plain words, so wants aren't checked for places;
   - (the addition) at least one prop on each card is named by no want. For this test a want also names a prop by its last word: "a pill" names the red pill and the blue pill, and "the spoon" names the bent spoon. Without that, the drafted simulation card would pass, because its wants say "a pill" and "every pill", never "red pill".
3. **The simulated shows build `set.props` from the card in play.** `Show` gets `self.props = self.card["props"]`. The sample show's actor states and the input converter's state use it, and each card-sweep state uses its own card's props. `build_jobs` passes the same list to `check_reply`, so a grab of a prop not on the card in play fails the check.
4. **The sample show moves to `space_plans`.** This isn't in T44's steps, but it is needed: `Show` looked up `SAMPLE_CARD = "star_crossed"`, which T44 removes. With the new `scenes.json` and the old checker, `--offline` stops with `StopIteration` in `Show.__init__` (I ran it). The sample keeps T51's shape: every actor gets the `hold_prop` note, SpaceXAI forgets to grab a prop, and the human slips by giving its prop away and asking for a nap. The seats are 0 the farm kid (the human), 1 the masked villain (OpenAI), 2 the old desert hermit (Anthropic), 3 the smuggler pilot (SpaceXAI, who grabs nothing), 4 the rebel princess (Meta). The turn lines are rewritten around the card's props: the human and three AIs grab the four props, and the human hands the tin-can robot to the villain. The overclocker's last line names its T56 rival: "Launch postponed. My rival is still Player 5. I'll beat you by Tuesday!" (Meta is Player 5; T51's line said "New rival: Player 2", which T56's rivals contradict). One Free Talk line changes its prop (the rose and the scroll become the robot and the blaster), and the rest of Free Talk is T51's. Every new line is 15 words or fewer (T59's cap); the longest are 15. No line trips a story term.
   - **The comment block above the sample show** is replaced whole by `patch_check_prompts.py`, from "# Scene 1 of a sample show:" to `HUMAN = "human"`. If T50 has added its sentence ("The human has no note (T50): ...") the script keeps it, with the tin-can robot in place of the rose, and says "which every AI actor gets".
5. **Input cases:** the sword case now expects the `glow-stick sword` (the typed text is the same). T51's case "i bet the claude bot is the human" is unchanged. "give the rose to open ai" becomes "give the tin can to open ai" (not "the robot", which could mean an actor), and the second Free Talk mention asks about "the blaster". The cases that mirror the on-screen hint ("@Meta, why did you grab the rose?") and the balcony cases stay as they are. The first copies a widget's text, and the balcony cases test the converter's rule that anything raised is the Riser, which doesn't depend on the card.
6. **The docstring** gets a "Props (T44)" paragraph.

**What I dropped from each draft's `banned_terms`** (Q6). They are bare first names or surnames that are common, everyday words, real things, stock phrases, and three studio names that the `any` list already holds:

- `space_plans` (26): `luke`, `the dark side`, `han`, `old ben`, `biggs`, `speeder`, `parsec`, `parsecs`, `the empire`, `exhaust port`, `tractor beam`, `the force`, `new hope`, `only hope`, `my only hope`, `move along`, `bad feeling about this`, `i have a bad feeling`, `we're doomed`, `lack of faith`, `you're all clear`, `punch it`, `scruffy-looking`, `lucas`, `lucasfilm` (in `any`), `cushing`. Added the whole line `i have a bad feeling about this` in place of its two pieces.
- `mine_bridge` (6): `strider`, `shire`, `rohan`, `bree`, `elevenses`, `mellon`.
- `dino_island` (8): `the lost world` (Conan Doyle's novel, public domain), `malcolm`, `dodgson` (Lewis Carroll's real name; `lewis dodgson` stays), `rexy`, `objects in mirror`, `unix system`, `chaos theory`, `universal pictures` (in `any`).
- `favor_father` (22): `the don`, `michael`, `sonny`, `connie`, `carlo`, `the turk`, `khartoum`, `fabrizio`, `consigliere`, `caporegime`, `cosa nostra`, `omerta`, `mafia`, `mafioso`, `paramount` (in `any`), `make him an offer`, `take the cannoli` (it matches "take the cannoli tray"), `it's not personal`, `strictly business`, `keep your friends close`, `your enemies closer`, `kiss the ring`.
- `glowing_briefcase` (43): `pulp`, `vincent`, `vega`, `jules`, `mia`, `wallace`, `butch`, `coolidge`, `winston`, `wolfe`, `mr. wolf`, `the wolf`, `pumpkin`, `honey bunny`, `ringo`, `yolanda`, `marvin`, `jimmie`, `bonnie`, `the gold watch` (an AI would shorten "gold pocket watch" to it), `zed`, `maynard`, `lance`, `jody`, `brett`, `esmeralda` (the public-domain one; the film's spelling `esmarelda` stays), `jack rabbit`, `big kahuna`, `kahuna`, `royale`, `tasty burger`, `tasty beverage`, `red apple`, `ezekiel`, `this is a robbery`, `pretty please with sugar on top`, `be there in ten`, `uncomfortable silences`, `foot massage`, `metric system`, `666`, `willis`, `you never can tell`. Added the full names `vincent vega`, `jules winnfield`, `mia wallace`, `marsellus wallace` and `butch coolidge` in place of the bare first names.
- `league_night` (35): `dude`, `dudes` (`the dude` stays), `walter`, `donny`, `maude`, `bunny`, `brandt`, `the stranger`, `smokey`, `marty`, `uli`, `franz`, `nihilist`, `nihilists`, `marmot`, `pomeranian`, `urban achievers`, `achievers`, `gutterballs`, `the ringer`, `white russian`, `ccr`, `nam`, `abide`, `abides`, `over the line`, `out of your element`, `you're out of your element`, `you're not wrong`, `careful, man`, `let's go bowling`, `what-have-you`, `your opinion, man`, `goodman`, `flea`.
- `pick_a_pill` (36): `trinity`, `smith`, `anderson`, `oracle`, `cypher`, `reagan`, `tank`, `dozer`, `switch`, `mouse`, `persephone`, `seraph`, `the architect`, `sentinels`, `the construct`, `operator`, `the source`, `reloaded`, `revolutions`, `resurrections`, `jack in`, `jacked in`, `unplugged`, `white rabbit`, `rabbit hole`, `down the rabbit hole` (Alice is public domain; `follow the white rabbit` stays), `whoa`, `kung fu`, `free your mind`, `what is real`, `wake up`, `knock knock`, `deja vu`, `the story ends`, `not like this`, `reeves`.

T44's own drop list is covered: `tank`, `han`, `pulp`, `vega`, `flea`, `nam`, `666` and a bare `dude` are out, and `the one` was in no draft list.

## Step 5: the check I ran

**At the refresh (2026-11-15, against `6ada2ab`),** in a scratch copy outside the repo (`Tools/`, `Content/NHOS/Data/`, `Docs/StoryDrafts/` and `Relay/relay.config.json` from `git archive 6ada2ab`), never on the real files:

1. **`make_scenes.py` on T51's `scenes.json`** writes a file byte for byte the same as the draft `scenes.json`. Against the draft from before the refresh, the only changes are the ten notes (no decoy, a category each) and `_readme` line 5 (T51's line plus "with any card's four props").
2. **`patch_check_prompts.py` on T51's checker,** then `python Tools/check_prompts.py --offline` with the draft `scenes.json` in place: it printed the following and exited with 0:
   ```
   Files OK: llm.json, prompts.json, personas.json, scenes.json, errors.json, and the relay's allow-list
   No provider name in what the actors and the Director read.
   ```
   It builds 59 asks (22 scene turns, 18 of them in the card sweep: 3 each for `space_plans`, `dino_island`, `glowing_briefcase` and `pick_a_pill`, 2 each for the other three).
3. **`check_prompts.patch`:** made with `git diff` from that copy. `git apply --check`, then `git apply`, on a fresh copy of `Tools/` at `6ada2ab` passes and gives the same file as the script, byte for byte. The old patch (from `9b4cd8b`) no longer applied: it failed at the sample show's comment, which T51 rewrote.
4. **After T50's planned checker edits:** on another copy I made T50's build-sheet changes D, E, F, G and I by hand (the human has no note, `note_category` in both `scene_card` lines, a `note` key in the card sweep's `ctx`), then ran `patch_check_prompts.py`. It patched, `--offline` passed, the sample comment kept T50's sentence with the tin-can robot, and the card sweep's `ctx` got `"props": st["set"]["props"]` next to T50's `note` key. `check_prompts.patch` itself won't apply after T50; use the script then.
5. **The props check catches what it should** (`card_prop_problems` on changed copies of the cards): the drafted fortune-teller want ("card pick_a_pill's wants name all 4 props"), a card with 3 props ("needs exactly 4 different props"), a prop on two cards ("prop 'piggy bank' is on two cards (space_plans and mine_bridge)"), and a want that names an old shared prop ("names 'rubber chicken', a prop the card doesn't bring"). The draft cards give no problem.
6. **No decoy:** `grep -ci decoy` finds nothing in `scenes.json`, `make_scenes.py`, `patch_check_prompts.py` or `check_prompts.patch`. The draft has 10 notes, each with one of T51's four categories.
7. **Word counts:** every sample line in `TURNS` and `TALK` is 15 words or fewer by the checker's own `words()`.

**From the first pass, at `9b4cd8b` (not run again):** the banned-word sweep (245 lines built from the props, roles, titles and backdrops trip no kept term; "There is no spoon", "I have a bad feeling about this truck", "You shall not pass" and "This droid is mine" still trip), and `check_reply` taking a grab of `bowling ball` in a `league_night` sweep ask and failing a grab of `rubber chicken` there. The refresh changed no card, prop or story term, so they still hold.

Not run: anything that calls a provider or the relay. T44 runs `--relay --free` itself (step 5 of the task).

## What T44 must check again

This sheet is written against `6ada2ab`. In the plan's order, T50, T59, T53, T52, T54, T55, T57 and T58 come before T44, and most of them change `Content/NHOS/Data/prompts.json` and `Tools/check_prompts.py`. Before T44 builds anything:

1. **`git log --oneline 6ada2ab..HEAD -- Content/NHOS/Data Tools`** lists what changed since this sheet. Read only those diffs.
2. **`scenes.json`** (A1): none of those tasks lists it in its Touches. If it changed anyway, run `make_scenes.py` on the current file, not a copy of the draft. It stops on an `assert` if a note isn't in T51's form or a `_readme` line it edits has moved.
3. **The `_readme` `cards` line** still says "scene 2 uses 4 of them and scene 3 uses 3". After T52 (a tie cuts nobody) and T53 (scenes = cast size − 1) that is no longer exact: a tie can keep 5 actors on stage for scene 2, and a 5-actor show can have 4 scenes. The rule that matters still holds ("every want must work when any one or two seats are left out", since the show ends at two actors). If T52 or T53 didn't fix the sentence, fix it in T44's `scenes.json` and say so in T44's Findings. The checker's `card_cases` docstring says the same about its sweep; leave that to whichever task changed the show's length.
4. **`check_prompts.py`** (A2): try `git apply --check` on the patch; if it fails, run `patch_check_prompts.py`. Its blocks and what could stop each one:
   - the docstring (anchored on the "Card sweep:" paragraph): T50 adds a paragraph after "Rivals (T56)", which doesn't touch it;
   - `STORY_TERMS`, replaced whole from its comment to `STORY_RES`;
   - the `set.props` count check (T45 also changes it, after T44);
   - `card_prop_problems`, added before `def check_files(errors: list[str]):`;
   - the sample comment, replaced whole (T50's D is handled);
   - `SAMPLE_CARD`, the seats comment, and `TURNS`, replaced whole up to `TALK = [`. If T59 or another task shortened a `TURNS` line, T44's lines replace it anyway; check that each is still 15 words or fewer under the cap then in force;
   - the copycat `TALK` line ("Player 3 gave away the rose. ..."): stops if a task reworded it. Then make the prop change by hand;
   - the three input cases (the sword, "give the rose to open ai", "@meta why did you grab the rose? ...");
   - `self.props` in `Show.__init__`, the two `"set": ...` lines (matched without the `scene_card` lines, which T50 changes), the input converter's `"props"`, `props = show.set["props"]` in `build_jobs`, and the card sweep's `ctx`.
   - T55 removes the tiebreak and the Director; T58 adds `last_word`; T52, T53 and T54 change game messages and `show.scenes`. None of those touch a block above, but `--offline` after the patch is the real test.
5. **`prompts.json`:** the stage line (A3) and the two prop examples in step 1 are found by their text. T50 rewrites the note lines of `game`, T57 the evidence lines, T59 the cap; none is expected to touch the stage line. If T50 added `note_category` to the state line, nothing in this sheet changes.
6. **The design doc:** read the Rules tab again for A4 and Q7, and the Stories tab's rev for the cards.
7. **`MAX_WORDS`:** after T59 it is 15. The patch doesn't touch it.

## The 15-word cap and the rivals

**T59 (every line capped at 15 words):**

- **The cards:** the cap is on spoken lines, not on the card. A premise, a role and a want are state the actors read, so none is cut. No want needs a long line: the ones that ask for talk ("croon a sad song", "chatting about burgers all the way", "teach anyone who will listen", "swear you were only checking it for scratches", "say yes to every favor") all fit in 15 words. No card text changes for the cap.
- **The new note:** "Mention your favorite prop every time you speak" costs two or three of a line's 15 words, which leaves room. `ask_question` is unchanged.
- **The props in canned lines:** T59's build sheet counts `free_mode.json`'s `{prop}` lines with "toy ray gun" (3 words) as the longest prop. The longest new props are also 3 words ("plush horse head", "bowl of oranges", "gold pocket watch"; "glow-stick sword" and "tin-can robot" are 2), so its count still holds when T45 puts the card's props in `set.props`.
- **The sample show:** every line in the patch's `TURNS` is 15 words or fewer (one was 16 before the refresh and is shorter now: "The farm kid wandered off mid-escape. Unsafe. My sword scores are higher anyway.").

**T56 (each bot has a rival, by its traits; the pairs are OpenAI and Anthropic, SpaceXAI and Meta):**

- **The sample show:** the overclocker (SpaceXAI) named "Player 2" (Anthropic) as its new rival in T51's sample; its rival is Meta, Player 5, so the patch's line says "My rival is still Player 5". No other sample line names a rival.
- **The cards:** a seat's role or want is separate from a persona's rival, and no card text names a lab, a persona or a Player. One role uses the word: `league_night`'s "A flashy rival bowler". An AI in that seat could mix the seat's rivalry with its persona's. I kept it (see the decisions below); T44's free relay run can't show it, so the first real relay show on that card is the check.

## How T44 uses this

1. Check A1 to A6, then "What T44 must check again".
2. Ask Q1 to Q7, one at a time.
3. Step 1: accept the Rules tab's suggested edits (Q3), suggest the edits from Q7 if the person said yes, and edit the stage line of `prompts.json` (line 29 at `6ada2ab`; find it by its text) with the OK'd wording (Q1, Q2).
4. Step 2: copy or build `scenes.json`. If the person picked Q5 option 1, change the `league_night` premise, and edit the Stories tab for Q4 and Q5.
5. Step 4: apply the patch.
6. Run `python Tools/check_prompts.py --offline`, then `--relay --free`.
7. In T44's Findings, say: the sample show moved to `space_plans`; the bent spoon is now a spare (for T39's count); and the follow-ups below.

## Left for later tasks (not T44's)

- **T45:** `Content/NHOS/Data/autoplay.json` has "grab the rubber chicken ...". The `input` prompt's example names the `cardboard sword` (step 1). The on-screen Free Talk hint asks about "the rose". `Graphs/BP_Prop/SetProp.txt` names the eight old props. All of them hold until T45 puts the card's props on the table.
- **The itch page:** `Docs/ItchPage.md` still describes the old cards (Romeo and Juliet, the Sword in the Stone, the rubber chicken case) and the eight old props.
- **The Stories tab:** the fortune-teller's want (Q4) and, if chosen, the `league_night` premise (Q5).

## Decisions made for my person

My person was asleep when this refresh ran and asked that design calls be made with my own recommendation and listed for review. T44 can still put each one to them.

1. **`favorite_prop` is in the Speech category,** not Props. It is about what you say, it takes `say_chicken`'s place, and it keeps the four categories at the counts my person OKed in T51 (Movement 4, Props 3, Looks 1, Speech 2). Props would send the human, who sees only the category after T50, to grab things while the AIs only talk.
2. **The new note's text stays as T44.md suggests:** "Mention your favorite prop every time you speak." It fits the 15-word cap and needs no change for T50.
3. **`hold_prop` and `give_every_turn` stay as they are** with four props. After T50, the 4 AIs share 4 props; a human who grabs one on turn 1 leaves one AI empty-handed, which is evidence noise the bots can weigh, not a broken scene. I checked the design doc's Rules tab (rev 27): it says notes are evidence and that "fitting the category is not proof".
4. **The sample show's overclocker names its T56 rival:** "Launch postponed. My rival is still Player 5. I'll beat you by Tuesday!", in place of T51's "New rival: Player 2", which contradicts the rival pairs.
5. **The sample line "The farm kid just wandered off mid-escape, which feels unsafe. ..." is shortened** to 13 words, so the patch adds no line over T59's cap.
6. **`league_night` keeps the role "A flashy rival bowler",** although T56 gives the word "rival" a meaning in the bots' rules. It is the card's own wording (in the Stories tab too), a seat role is clearly separate from a persona, and renaming it would change the doc's Stories tab, which isn't T44's to change without my person's OK. If a real relay show shows the bot in that seat confusing the two, rename it "A flashy show-off bowler" in the card and the Stories tab.
