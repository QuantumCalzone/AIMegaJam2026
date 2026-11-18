# Art Inspiration

## Art direction

Stop-motion clay robots put on an improv show in a grand clay opera house, and one human hides among them in a homemade cardboard costume. Everything looks hand-sculpted from matte modeling clay: the robots, the theater, the costumes, the props and the audience. My person chose this direction on 2026-11-17 (T94): the clay opera house of 2026-11-15, done better. All the game's art is being redrawn in it. T95 to T99 draw the concepts, and T103 to T106 make the models. The full style guide is in [Docs/Art/Direction/README.md](../Art/Direction/README.md): the palette, the rules for image-to-3D, and the prompt text that every generation starts from. [Docs/Art/README.md](../Art/README.md) lists every asset being replaced.

The approved direction board. It sets the look, not the layout: the UI's layout is in the UI section below.

![The approved direction board: the five robots sculpted in clay on the opera stage (OpenAI, Meta, the player's cardboard costume, Anthropic, SpaceXAI), a cloth-covered prop table with a giant milkshake and a toy ray gun, red velvet curtains and a gold proscenium, clay robot audience in top hats and bowler hats, a plum UI panel, a paper card and a speech bubble](../Art/Direction/board.png)

### Style

- True 3D in Unreal Engine 5, styled as stop-motion clay. Never 2D or drawn, and no ink outlines on characters or sets.
- Matte modeling clay everywhere, with high roughness and no metal. The gold is gold-painted clay with a satin sheen. Thumbprints and tool marks live in the textures, never in the silhouette. One shared clay material colors anything of a single color.
- Round, toy-like bots with big heads, about a third of their height. The player's costume is the one boxy, homemade shape on stage. The theater is classical but chunky, with nothing thin or spindly.
- Each bot's seat color is its body color, and the seat colors belong to the five alone. The world is crimson velvet, old gold, cream and dark wood, and the audience wears muted colors.
- Detail reads at the house camera's distance. At 1600 × 900 a bot is about 125 px tall and a prop 25 to 50 px. Outline and two or three colors carry a thing, and no detail is smaller than about 1/20 of its height.
- Lumen light with no baked light: warm footlights from below, a soft warm key, pink and cyan rim lights, and a dim house. Textures carry no painted light.
- Built for image-to-3D: thick, joined parts and clean silhouettes. A generated model has no hair, wires, thin rings or see-through parts. Glows and lenses are engine parts.
- Tone: chaotic, petty slapstick. Never scary or gory. No brand marks, writing or real people's likenesses.

### The bots

**Concepts approved in T95 (2026-11-18); T103 builds the models from them.** Until then the game shows the cast as built on 2026-11-15. The concepts, the turnarounds and every round are in [Docs/Art/Cast/](../Art/Cast/README.md).

![The approved cast in seat order on one clay opera stage: OpenAI, a pale blue round-headed bot in a gray knit sweater; Anthropic, an orange round bot with round gold glasses, an amber light and a raised finger; SpaceXAI, a lime round bot with a long nose, a toothy grin, a lightning bolt, spring limbs and a double thumbs-up; Meta, a pale silver android with slicked black hair, yellow eyes, black smart glasses, a gold chain and a black and mustard top; and You, a person in a teal cardboard box costume with eye slots, a drawn smile, a ping-pong ball, a scarf and garden gloves](../Art/Cast/lineup.png)

- Four polished clay bots and one human in a homemade cardboard costume. That contrast is the premise in one picture: round, toy-like bots, and the player as the one boxy, homemade shape, pretending. Every bot is about 1.6 m tall, with a big head about a third of its height, and its seat color is on its body, because a wig or a hood hides most of a head.
- OpenAI, Anthropic and SpaceXAI share one round head: a dark screen face with big LED eyes and a mouth that stretches wide, two cream ear pods and a short gold collar. Meta has its own android head, and the player a cardboard cube.
- **OpenAI:** a short pale sky blue teardrop body on stubby feet, in a gray knit sweater, hands pressed together, wide earnest eyes. It stands on the floor: no halo and no ring.
- **Anthropic:** a round orange body with a big cream belly and three round buttons, short arms and round feet, circular gold glasses over the screen, calm eyes, one finger raised to make a careful point, and an amber light on a short stalk.
- **SpaceXAI:** a round lime body with a cream belly and a lime lightning bolt, on steel coil-spring neck, arms and legs, chunky dark boots, a dark visor with one cocked brow, a long cream nose under it, a wide toothy grin and a double thumbs-up.
- **Meta:** an android with pale silver skin and a grown-up head: thin, flat, slicked-back black hair with a side part, small ears, pale yellow eyes with dead black pupils, a small polite smile, and thick black smart glasses with a camera lens on one corner and a recording light on the other. Ball-jointed silver arms, a black and mustard top, black pants, silver shoes and a chunky gold link chain. Its look nods to Data from *Star Trek: The Next Generation* (my person's call), with no badge or insignia.
- **You:** a person in a homemade robot costume: a teal-painted cardboard cube over the head with two eye slots that the person's eyes peek through, a smile drawn in marker and a ping-pong ball on a straw; a bigger teal box for the body with a duct-tape band and bottle-cap buttons; the red and cream knitted scarf, red and cream striped sleeves, tan garden gloves, jeans and sneakers.
- The energy is borrowed from chaotic sidekick crowds: jittery, slapstick, gibberish blips for voices. No overalls, goggles, rabbit ears or screaming mouths.
- Each provider bot carries a light parody nod to its company's leader through signature traits only (glasses, clothes, expression, pose), never a name, and nothing carries a brand mark. No wires, and no hair but Meta's solid hair cap. Costumes go over the built-in parts: the shades hide Meta's and Anthropic's glasses, a wig sits over Meta's hair, and Anthropic's antenna light, SpaceXAI's bolt and the player's ping-pong ball poke up beside any hat. Every costume has a version for the player's cube head.
- The audience in the boxes and the stalls are small clay capsule bots, most in top hats.

| Seat | Body color |
| --- | --- |
| OpenAI | #A8CCFF pale blue |
| Anthropic | #E8894A orange |
| SpaceXAI | #D8F04A lime |
| Meta | mustard, with black (T95). Its exact hex is set when the UI's seat color changes; until then the game shows #5B8CFF blue |
| You | #3FD0C9 teal |

The colors are the UI's seat colors, so a bot, its name tag and its chat bar always match.

### The stage

**Redrawn in T98 (concepts, approved 2026-11-18); T106 builds it.** Each piece's view, size and material, the swatches and every round are in [Docs/Art/Set/README.md](../Art/Set/README.md).

- One stage for every story: a grand 19th-century opera house, sculpted in clay.
- Warm dark wood walls and box fronts with big, bright gold scroll mouldings. Heavy crimson velvet curtains with gold tie-backs, a crimson valance with gold swags and tassels, and footlights in gold shell hoods along the front edge.
- Two plump gold robot cherubs with screen faces sit on dark wood plinths at the stage's front corners.
- A gold chandelier hangs over the house. Two tiers of horseshoe boxes on each side and four raked rows of crimson stalls below the stage hold the clay audience: small capsule robots with smooth dome heads, two cream ear pods, screen faces and no antennas, in muted rose, plum, mustard, brick and lilac, most in black top hats or bowlers. From the house camera the stalls fill the bottom of the frame, seen from behind, dimmer toward the camera.
- The places stay as they are (Center, Left, Right, Front, Back, the Riser and the Prop Table). The Riser is a dark wood platform with a gold trim and a step; the Prop Table is a round table under a cream cloth.
- Each story drops in its own painted backdrop behind the stage.
- The Cut: a trapdoor opens under the cut bot and it drops out of sight in a puff of clay dust. (Proposal; a curtain drop is the fallback.)

The approved house from the house camera. The robots and the pink backdrop are placeholders: T95 draws the cast and T99 the backdrops.

![The approved house from the house camera: warm brown walls and boxes with big bright gold scrolls, crimson curtains and a gold-swagged valance, a gold chandelier, five robots on the plank stage, gold cherubs at the corners, and the clay robot audience in top hats and bowlers in the stalls](../Art/Set/house.png)

The pieces T106 makes: the chandelier, a robot cherub on its plinth, a wall pilaster, a theater box, a side curtain, the valance, the Riser, the prop table, a stalls seat, a footlight, the audience robot from the front and back, and its top hat and bowler.

![The 14 set piece views on one sheet, each on a plain gray background](../Art/Set/pieces/sheet.png)

The surfaces: crimson velvet, bright gold, dark wood, stage planks, cream and house black.

![Six clay surface swatches: crimson velvet, bright gold, dark wood, stage planks, cream and house black](../Art/Set/swatches/sheet.png)

### Costumes

**Being redrawn in T96 (concepts) and T104 (models), in the direction above.** Until then, this section describes the headpieces as built.

Thirteen clay headpieces dress all 35 roles. Each role wears one, in its own color: one model per piece, and the color comes from its clay material.

- At Scene Prep each bot puts on its role's headpiece. The antenna topper pokes up through it.
- Homemade parody versions only: a black saucepan helmet, never a film's real villain helmet.
- In Scene Prep, before the costumes go on, the bots stand bare-headed in their seat colors.

| Headpiece | Roles (story: color) |
| --- | --- |
| Hood | slacker (bowling: oatmeal) · ranger (ring: moss green) · youngest son (wedding: olive) · boxer (diner: red, gold trim) · hermit (space: brown) |
| Dark shades | adviser (wedding) · lawyer (dino) · agent (office) · chatty errand man (diner) · smuggler (space) |
| Top hat | rival bowler (hot pink) · crooner (glittery purple) · park owner (cream) · fixer (black, white band); also the audience |
| Bob wig | artist (cobalt) · homebody (chestnut) · rebel (glossy black) · boss's wife (jet black) |
| Ball cap | quiet bowler (sky blue) · eldest son (tomato red, backwards) · tour kid (cherry red) |
| Wide-brim hat | dino expert (olive) · leader in a long coat (maroon) · farm kid (straw) |
| Saucepan helmet | rule-keeper teammate (olive) · masked villain (black) |
| Wizard hat | wizard (dusty gray) · fortune-teller (lavender) |
| Tiara | elf (pale silver) · princess (silver and white) |
| Fedora | family boss (black, red band) · nosy errand man (dark gray) |
| Horned helmet with beard | dwarf (iron gray, ginger beard) |
| Dino hood | runaway dinosaur (grass green) |
| Beanie | office worker (gray-blue) |

The 13 headpiece models (Meshy renders), in neutral clay. Each role's color comes from its clay material.

![Renders of the 13 headpiece models: hood, dark shades, top hat, bob wig, ball cap, wide-brim hat, saucepan helmet, wizard hat, tiara, fedora, horned helmet with beard, dino hood and beanie](images/ArtInspiration/headpieces.jpg)

### Props and backdrops

**The props are redrawn: T97's concepts, approved on 2026-11-18, are in `Docs/Art/Props/`, each with a clean model view and its size; T105 makes the models from them. The backdrops are being redrawn in T99.** Until T105 imports the models, the game shows the old ones.

Each story brings four clay props to the Prop Table (three core, the last a spare) and drops in its own painted backdrop. The AI actors may only name the props on the current card.

| Story | Props (spare last) | Backdrop |
| --- | --- | --- |
| Space saga | tin-can robot, glow-stick sword, toy blaster, piggy bank | `desert_planet`: dusk under two suns, a rusty dome hut, a battered space truck, a suspicious gray moon |
| Ring quest | cursed ring, glowing staff, water bucket, frying pan | `dwarf_mine`: carved stone pillars, a thin stone bridge over a chasm, an orange glow from below |
| Dino park | dino egg, meaty drumstick, safety waiver, dino plush | `jungle_park`: steamy jungle, a sagging electric fence, a tilted warning sign, giant muddy footprints |
| Crime family | plush horse head, cannoli tray, wedding envelope, bowl of oranges | `garden_wedding`: a striped party tent, paper lanterns, lemon trees, a tiered cake, a pink villa |
| Diner | glowing briefcase, gold pocket watch, giant milkshake, giant cheeseburger | `retro_diner`: a chrome counter, cherry-red stools, a checkered floor, a big wall clock |
| Bowling | rolled-up rug, bowling ball, ransom bag, milk carton | `bowling_lanes`: shiny lanes, rows of white pins, a ball return, a starry ceiling |
| Simulation | red pill, blue pill, ringing phone, bent spoon | `midnight_cubicles`: gray clay cubicles, one buzzing light, old screens dripping green light |

- Glow is an engine part, never part of a model: the glow-stick blade, the staff's crystal, and the briefcase's lining with its god rays. The briefcase lies open wide, lid upright; the bent spoon is bent at the neck.
- Each backdrop is one painted image in a clay-relief diorama style, on the existing backdrop flat. No characters, text or logos.
- Open question: three director's notes assume the old shared table. "Mention the rubber chicken" names a prop that is gone, and "hold a prop all scene" and "give something every turn" need enough props for five actors.

Each story's props, one row per story in the table's order, spare last (T97's approved concept art, with each prop's size).

![T97's concept art of the 28 story props in seven rows, one per story, each labeled with its size and the spare marked](images/ArtInspiration/props.jpg)

### Stories

Seven film parodies set what gets built: a space saga, a ring quest, a dino park, a crime-family wedding, a diner caper, a bowling league night and an office simulation. Each full card, with every role's want and headpiece, is in [Stories](Stories.md).

## UI

**The UI's 2D art is being redrawn in T99, in the direction above:** the stagehand's portrait, and the burning bills with their badges. The concept, layout, palette, type and components below stay as they are.

The UI is the theater's own paperwork: a call sheet, a sealed note, ballot tickets and a rubber stamp, made chunky enough to read from the back row. Legibility beats style every time, and each screen has one thing to look at and one thing to do.

#### Concept

- **Theater paperwork, game-show bold.** Every piece is a prop the theater would own: a call sheet for your part, a sealed note card, ballot tickets, a rubber stamp and critics' reviews at the end. Thick outlines, big rounded corners, big type.
- **Two materials.** Ink panels (plum-black with an old-gold trim) carry the running talk and sit quietly over the stage. Paper cards (cream, dark text) carry what is yours or decisive. Paper means "read this".
- **Readable first.** When style and legibility disagree, legibility wins. Outlines belong to the UI only; the 3D stays outline-free (see Style).
- **The stage is the hero.** Panels keep to the corners and never cover a robot, its name tag, a thrown prop or the stamp.

#### Layout

![In-show screen layout · 16:9, a scene turn on your move](images/ArtInspiration/layout.svg)

The input row sits bottom left, with the chat above it when you open it. Your part sits top right, and the robots own the band between them. In Scene Prep, the scene sits on a panel at the bottom, in the middle, with Start the scene under it. Only the speech bubbles, the banner and the stamp cross into the stage, and the banner and the stamp stay only a few seconds.

#### Palette and type

Colors are set by role. Start from these values; if a value changes, keep its role. Every text pair below measures 5.4:1 or better (WCAG AA asks 4.5:1).

| Role | Value | Used for |
| --- | --- | --- |
| Ink panel | #161225 at 92% opacity or more | Header, chat, input row, banner |
| Old gold | #A9873A, 2–3 px | Panel trim only |
| Paper | #F5E9CF; text #2B1D12, quiet text #6B5B4A | Your part, ballot tickets, end reviews, the title playbill |
| Gold | #F2C14E, ink text on it | Act now: your move, the primary button, the focus ring |
| Curtain red | #C8202F, white text on it | The vote, the cut, YOU: HUMAN, errors |
| Amber ink | #F29E1F | The PROVIDER: AI stamp |
| Text on ink | #FFFFFF; quiet #C9C3DA | Speech; actions, hints and captions |
| Inset | #0E0B18 | The input box fill |
| Raised | #2A2342 | Secondary button fill |
| Seat colors | OpenAI #A8CCFF · Anthropic #E8894A · SpaceXAI #D8F04A · Meta #5B8CFF · You #3FD0C9 | Names, chat bars, name tags, ballot tickets |

- **Gold means act now, teal means you.** Nothing else in the play area is gold. SpaceXAI moves from yellow to lime so it never reads as gold, and OpenAI and Meta differ in lightness, not only hue.
- **States:** hover mixes a fill 15% toward white, pressed 12% toward black, and disabled is 40% opacity with no outline. Curtain red is only a fill with white text on it: red text on ink measures 3.2:1.
- **Display face:** one chunky rounded sans with an open font license (Lilita One fits), with a 2–3 px dark outline. Use it for the phase header, banner, buttons, stamp, title and end result, in short labels only. If importing it costs more than an hour, use F\_UI Bold with the same outline. List it with the outside assets. The dark outline goes on light display text only; dark labels on gold or paper have none.
- **Body face:** F\_UI (Roboto) stays for chat, cards and hints: names bold, actions italic, speech regular.
- **Mono face:** Droid Sans Mono (ships with the engine), for the preview line only.
- **Type scale at 1080p:** 18 actions and captions · 20 speech, body, chat names (bold) and button labels · 24 card titles · 32 phase header · 48 banner · 72 end result · 120 or more for the stamp. Nothing under 18.
- **Spacing:** only 4, 8, 12, 16, 24, 32 and 48 px. Panels pad 16 and sit 24 from every edge; chat lines sit 12 apart. Corners: panels and cards 16, buttons 12, name tags 10. Outlines: buttons and paper cards 3, the ink panels' old-gold trim 2, the input box 2, the focus ring 3. Seat bars are 6 wide.

#### Components

| Piece | Look | Behavior |
| --- | --- | --- |
| Header | Ink panel, top left. Phase in display type, scene and turn as pips (●●○), one line below on what to do now. | States each fact once; the chat never repeats it. On your move the line turns gold and starts with YOUR MOVE. |
| Clapperboard | A small ink slate under the header, top left, with a striped clapstick. SCENE 2 / 4 in display type. | Set at each Scene Prep; the same in every phase of a scene. Hides with the stage on the title and end screens. |
| Your part | Paper card, top right: your role as the title, your want under it. | In Scene Prep, the scene and the stage show on an ink panel in the lower middle, under the robots' feet, with Start the scene under them; your part and the note's clue stay on the card. When the scene starts, the panel goes and the card stays. |
| Director's note | Gold note card clipped to your part, with a SECRET tab. | Always in view while you act, never behind a scroll. |
| Chat | Ink panel, bottom left, above the input row. Hidden at the start of each show; the Show chat button opens it. Name bold in its seat color, action in quiet italic, speech in white. Your lines get a teal bar and a YOU tag. | Actor lines only, newest at the bottom. "Name is typing…" holds the place of the next line. Each line's speech then types out letter by letter in a box already at its full size, while the speaker's voice babbles one gibberish sound per syllable. It gets every line while hidden, and stays open or closed as you set it until the next show. |
| Speech bubble | Ink bubble over the speaker's robot, above its name tag, with a ring and a pointed tail in the speaker's seat color. Speech in white at 20, wrapping at about 420 px at 1600 × 900. A line with no speech shows its action in quiet italic; a vote shows "Votes for X." above the reason. | Four states. Line: types out with the chat line, in one voice. Typing: three cycling dots before an AI's line in Free Talk and the reactions. Fading: 250 ms, when the next robot speaks or the phase changes. Hidden: a cut robot, Scene Prep, the end screen. The robot just cut still gets bubbles for its last words in the reactions. Stays 24 px inside the window and clear of the panels, the banner and the stamp, moving aside while its tail points at its robot. |
| Input row | Dark box with a 2 px outline, a gold Action! and an outline Pass. In your scene turns the action builder sits above it: the preview line in a mono face, the seven action buttons and the picked action's chips. A Secondary Show chat button (it reads Hide chat while the chat is open) sits at its left end. The panel is 1080 wide in every phase but Scene Prep, where it is 640 wide and holds only Show chat and the greyed field. In scene 1's Scene Prep it is hidden, with the chat. | Your move: a gold focus ring pulses once and the caret waits in the box. Otherwise it dims, and the hint says who you are waiting on. |
| Name tags | A pill over each robot in its seat color, dark outline, 18 pt or more. Yours is teal and reads YOU. | Tags never overlap; close robots stack them. The speaker's tag grows 20%. Yours bounces on your move. |
| Ballot | One paper ticket per actor: a seat-color bar and the provider name. | Click a ticket: a red HUMAN? stamp lands on it and the rest dim. Then type the reason. |
| Banner | Ink strip across the top of the stage, gold display letters. | One moment at a time (a new scene, a tie, the tally, who was cut). Holds 4 s, then fades. |
| Reveal stamp | Rubber stamp tilted −8°, double outline for an inked edge. Red for YOU: HUMAN, amber for PROVIDER: AI. | Slams in from 3× size in 0.2 s with a small shake, holds 3.5 s, fades over 1 s. |
| Turn timer | A gold ring around the current turn pip. | Only if timers ship. Turns red for the last 5 s; never flashes. |
| Money burn | A burning bill, bottom right. | Relay calls only. Never takes a click or the input's focus. |
| Buttons | Display type, 48 px tall, 12 px corners, 3 px outline. | Four kinds: Primary (gold, ink text), Secondary (plum, quiet outline, white text), Danger (curtain red) and Paper (cream, dark text). Hover brightens the fill and lights the outline; pressed darkens it and drops the label 2 px; focused shows the gold ring; disabled drops to 40% opacity and loses its outline. |

#### Screens

Size, weight, color and position follow this ranking: the first column is the biggest thing on screen, the second is the only bright button.

| Screen | See first | Do next |
| --- | --- | --- |
| Title | The name, as a playbill over the stage | Play, on our relay. It stays greyed out, with a short line on why, until at least 3 AIs are working and today's budget isn't used up. Own keys and Test for Free are secondary buttons, each with one line on what it needs. |
| Key entry | Which providers still need a key | Save and Play |
| AI service unavailable | What went wrong, in one sentence | Enter your own keys |
| Scene Prep | The scene in the middle, then your part and the note's clue | Start the scene |
| Scene turn, your move | The header line in gold | Pick an action, add a line if you like, press Action! |
| Scene turn, waiting | The robots acting | Nothing: watch the turn play out |
| Free Talk | The newest chat line | Type a line, or Pass |
| The vote | The ballot | Pick a ticket, then type a reason |
| The reveal | The stamp | Nothing: watch for 3.5 s |
| Reactions | The cut robot and its last words | One line about the cut, or Pass |
| Show over | The last reactions | See the results |
| End screen | YOU WIN or YOU'RE CUT, then one review card per AI | Play Again |

#### Motion and rules

- **Motion times:** hovers and presses 120 ms; panels in and out 250 ms, easing out.
- **Big motion is for moments:** the stamp, the banner, the hook. Text panels never bounce, shake or slide while you read. A small spring overshoot goes only on things that land: the stamp, a picked ticket, the YOU tag.
- **Every screen passes these,** checked at 1600 × 900 and 1280 × 720:
  - Text is 18 pt or more at 1080p, with 4.5:1 contrast or better. Buttons and panel edges reach 3:1.
  - Color never carries meaning alone: each seat color comes with its name, each state with a word or a shape. Check a grayscale and a deuteranopia version.
  - One primary focus and one next action. Each instruction is said once.
  - Nothing covers a robot, its name tag or a thrown prop.
  - Panels sit 24 px from every edge.
  - No emoji, at most two typefaces, and no sentence in all caps.

#### Fix first

Today's screens (the 2026-11-14 playtest shots) work, but read as a generic dark app. In order of how much they hurt a player:

1. **Name tags overlap** when robots stand close ("You" over "SpaceXAI", "Anthropic" over "OpenAI"). Stack them.
2. **The turn is said three times:** in the header, the line under it, and the chat. Say it once, in the header.
3. **The vote buttons are all the same red,** so seat identity is lost at the decision. Use seat-colored ballot tickets.
4. **Panels at 75–82% opacity** let the stage show through words. Raise them to 92% or more.
5. **The scene premise fills the card during play.** Show it in Scene Prep only; in the scene, your part and the note are enough.
6. **Nothing says "theater" yet:** plain dark boxes and Roboto everywhere. The display face, the paper cards and the old-gold trim fix that.
