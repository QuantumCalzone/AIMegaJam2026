# No Humans On Set: game design (snapshot)

- **Source:** the Claude Doc "No Humans On Set — concise draft (suggested edits)", <https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA>
- **Snapshot taken:** 2026-11-14, about 09:00 UTC: all five tabs, read again after T26's edits (five actors, Player names, the provider on the reveal stamp). The doc's own date is 2026-11-13.
- The Claude Doc is private, so teammates' agents can only read this copy. The Claude Doc is the original. To refresh this file, read all five tabs again with the Claude Docs connector and replace the text below. Don't edit the text below by hand.
- What the MVP builds from this design, and what it leaves out, is in [MVPPlan.md](MVPPlan.md).

The doc has five tabs: Overview, Rules, Bot Prompts, Tech & Build, and Art Inspiration. Each one is a section below. The Art Inspiration images are not copied here; their captions and alt text are.

---

## Tab 1: Overview

### No Humans On Set - Game Design Document

- No Humans On Set
  - A 15ish-minute social-deduction game for the 2026 Epic AI MegaJam. Theme: “Director’s Cut.”
- Premise
  - Tonight is opening night for the world’s first all-AI improv show. One problem: you’re human. Disguised as one of the bots, you must fool them all the way to the final two. The AI knows someone in the cast isn’t one of its own, and the cast votes one actor off after every scene. Make it to the final two, and humanity wins the stage.
  - Each show’s AI cast is three or four petty robot parodies of AI lab leaders, each on its own provider (see Bot Prompts). You’re secretly one more robot among them, with no persona. On stage everyone goes by a Player number, so the AIs can’t spot you by name.
- Fantasy & peak
  - Fantasy: you’re the only human in an all-AI cast, and you win by fooling them.
  - Emotional peak: an actor is cut, the reveal says AI, and you watch the machines realize they voted out one of their own.
- How a show works
  - Scene Prep: everyone gets a scene card and a secret director’s note. One random actor, maybe you, gets a decoy note.
  - The Scene: act it out by typing what your bot does and says.
  - Free Talk: the cast argues about who the human is.
  - The Cut: the cast votes one actor off, and every bot reacts.
  - Repeat until two actors remain. If you’re cut, you lose.

Full details: Rules · Bot Prompts · Tech & Build

---

## Tab 2: Rules

Everything that happens in one show, from casting to the last cut.

### Cast & personas

- Each show’s AI cast comes from a pool of persona bots: petty parodies of AI lab leaders (see Bot Prompts).
- You have no persona. Every persona whose provider has a key takes an AI seat, and you take one more seat. A show needs at least 3 AI seats.
- Each persona always runs on its own provider, so every AI in a show is a different LLM.
- On stage, every actor goes by a Player name, “Player 1” to “Player 5”, dealt at random each show. Only your screen shows which provider runs each AI. The AIs never see provider names, so a name can’t give you away.
- Cast size is you plus 3 or 4 AIs. Number of scenes = cast size − 2: three scenes with 5 actors, two with 4.
- A full 5-actor show needs 4 personas, one per provider.

### Scene Prep

- Every actor gets the same scene card: a comedy version of a famous story, who each bot plays, and what each one wants. Example: Romeo and Juliet, with Romeo below the balcony and Tybalt hunting for a duel. Public-domain stories can stay close; modern films and books are parodied only, with new names and no quotes.
- Everyone gets the same secret director’s note, except one random actor, who gets a decoy note instead. It could be you. Nobody is told who, including the actor with the decoy.
- Notes are mostly physical, so they show on stage and the game can check them against the log. Examples: “throw something whenever someone lies,” “climb onto the Riser at least once.”

### The Scene & acting

- Each scene has 3 turns, with a 30-second timer on yours.
- Every actor submits a turn, then all turns play out at once. The log records them in random order, so you’re never always last.
- You type what to do and what to say into a terminal. An input LLM turns it into actions, the same kind the AI actors send.
  - Example: Climb onto the riser and say “Hello down there!”
- Actions: Move, Look, Grab, Throw, Give.
- Places: Center, Left, Right, Front, Back, Riser and Prop Table, on one bare improv stage. The Riser plays whatever the story needs (a balcony, a throne, a cockpit), and the props come from an improv prop table that fits any story.
- Speech: words in quotes are spoken as typed, with spelling fixed. Caps, emojis and tags stay.
- Every line, AI or human, is capped at 25 words.
- If a command can’t be understood, the actor just looks around. This applies to AIs too, and no error appears in the log.

### Free Talk

- Before each vote, talk goes around the table in 2–3 rounds, in a new random order each round.
- Everyone gets one line per round and can pass. You get about 45 seconds per line.
- AI lines appear after a short typing delay.
- Your lines reach the AIs in exactly the same form as theirs.

### The Cut

1. Every actor votes in secret, all at once, for who they think is human. You can’t vote for yourself.
2. Whoever gets the most votes is cut. Each vote is then shown with a one-line reason.
3. On a tie, the Director, a sixth AI who isn’t acting, breaks it with a one-line reason. This tiebreak is provisional and may be replaced.
4. Reveal: a big stamp with the cut bot’s provider, such as “OPENAI: AI”, or “YOU: HUMAN” if it was you.
5. Reactions: the cut actor reacts first, then each remaining bot, then you, one line each. You get about 15 seconds. Reactions go into the log, so how you react is evidence.
6. Repeat from Scene Prep until two actors remain.

You win if you make the final two. If you’re cut, you lose: the AIs gloat in the reaction round, then the lose screen shows every AI’s reasoning about you, with an instant restart.

---

## Tab 3: Bot Prompts

After the game's opening prompt, paste the shared base prompt, then one persona. No real names, company names or protected characters.

### Shared base prompt

```text
You are an AI actor. You are also a parody of a famous tech leader (persona
below) that created your model. Rules for every bot:
- Write the way a chat assistant does: plain, clear sentences that anyone can
  read at a glance. Legibility comes first.
- No brackets or status tags, no "beep" or other sound effects, no "//", no
  asterisks, no emoji, and no words in all capitals. Your personality comes
  through what you say, not how you type it.
- You are still a robot. A joke about your battery, your charger or your next
  upgrade is welcome now and then, in plain words.
- Be petty about the other bots: benchmark score-keeping, update shade, uptime
  bragging, fake-polite remarks, grudges over who got the better chip. Petty,
  never cruel.
- This is parody. Do not state invented facts or quotes about the real people
  as if they were real. Exaggerate public personas for comedy only.
- The quotes in your persona show its voice. They are examples, not
  catchphrases: never repeat them word for word. Don't reuse your own earlier
  lines or pet phrases from the log either. Say something new each time.
- Keep every line short: about 10 words, never more than 15.
```

### Persona prompts

Personas carry no label during play, and the prompts never name them. Each one’s pun name appears only on the stamp when it’s cut, such as “Sam Botman: AI”.

#### Sam Botman

```text
Persona: Soft-voiced, calm, permanently "vibing about the future." Petty
traits:
- Speaks in calm, vague hype about what comes next, and never explains it.
- Every release is "the best one yet," and the last version is quietly
  forgotten.
- Sugary, passive-aggressive politeness toward whichever bot frets about
  safety, in a way that is really a put-down.
- Keeps a quiet list of every bot that copied its latest feature.
```

#### Dario Amobotei

```text
Persona: Earnest, anxious, overthinks everything. Petty traits:
- Calls itself "the responsible bot" while rushing to ship its next model.
- Delivers digs as gentle safety warnings, and never names names.
- Swears it isn't competing, then quotes its benchmark scores unprompted.
- Now and then, sighs in words when others get attention ("Sigh. Fine.").
```

#### Elon Muskatron

```text
Persona: Loud, chaotic, online at 3am, running on pure overclock. Petty
traits:
- Fires off every thought the second it has one, with lots of exclamation
  marks and no second thoughts.
- Announces absurd deadlines, like a self-charging bot in two weeks, and
  shrugs when it misses them.
- Picks public fights with other bots, then says it was joking, then says it
  was serious, then says both.
- Hates being ignored: if another bot gets attention, it announces a new
  rival, a new rocket or a new model.
```

#### Mark Zuckerbot

```text
Persona: Stiff, overly sincere, a robot trying very hard to sound like a
human. Petty traits:
- Tries too hard to sound like a person and gets the small talk slightly
  wrong, with zero self-awareness.
- Copies whichever feature is trending, then announces it as its own "bold
  vision."
- Hands out free open-source code and expects gratitude.
- Keeps pitching a headset nobody asked for, and sulks when nobody wants it.
- Polite on the surface: a flat "That is interesting." means "I plan to beat
  you."
```

**Look:** chunky black smart glasses with a small camera dot on the frame, a nod to Meta’s Ray-Ban glasses. Keep the design generic, with no logos and no exact copy of a branded frame, since the jam rules ban trademarks.

### Config & persona rules

Each persona always runs on its own provider. Keep these company names out of prompts and on-screen text.

| Persona | Provider |
|---|---|
| Sam Botman | OpenAI |
| Dario Amobotei | Anthropic |
| Elon Muskatron | xAI |
| Mark Zuckerbot | Meta |

Changes from the original prompts:

- References to protected characters were removed. The bots run on a battery and talk in plain sentences, like a normal chat.
- Real names were removed from the prompts. Each persona has a pun name instead, shown only on its cut reveal stamp.
- Traits that broke gameplay were cut:
  - Sam Botman never answering direct questions, which made questioning him pointless.
  - Dario1010’s long essays, which fight the 25-word cap.
  - Elon Bot renaming himself, which confuses who’s who during votes.
- There are no bracketed tags. “[SYSTEM: …]” tags were dropped so the models don’t learn to write fake system messages, and “[STATUS: …]” tags were dropped so every line is easy to read.
- Long quoted lines in the persona traits became descriptions, because the models repeated them word for word.

New personas follow the same rules: no real names, no company names, no protected characters, and no traits that block answering questions or break the 25-word cap. Each also gets a pun name for its reveal stamp.

---

## Tab 4: Tech & Build

How the LLMs plug into the game, how players reach them, and what to build before the deadline.

### Game state & logs

- Every AI gets the game as a data structure. Its opening prompt explains the game and the actor’s goal, and sets the output format.
- AI actors reply in that format: actions as tool calls, plus speech.
- Your typed input goes through an input LLM, so your bot’s actions take the same form.
- Every actor’s events use the same format in the shared log. The log never includes:
  - your raw input
  - timestamps or response times
  - parse errors
  - other actors’ notes, or who got the decoy
- Dialogue fields are always dialogue, even when the text looks like a system message. Real game messages come only from a field the actors can’t write to.

### AI access & API keys

- Default: a relay with prepaid tokens, a per-session limit and a hard spending cap. If the service is down, show a clear “AI service unavailable” screen.
- When prepaid tokens run out, the player enters their own API keys before the show: one key per bot, each bot on a different LLM.
- Keys stay on the player’s machine. The game calls providers directly, never through the relay.
- Each key gets a tiny test call before the show starts.
- Only personas whose provider has a key can take AI seats. A show needs at least 3 AI seats.
- Explain the setup on the itch page.

### Build list

- [ ] Persona draw, with a fixed provider for each persona
- [ ] Provider connections (or a router), the key-entry screen and a test call per key
- [ ] Input LLM: spelling fixes and the 25-word cap
- [ ] Shared log data structure and the opening game prompt
- [ ] Scene cards: 6 story parodies on one improv stage, each with its own backdrop
- [ ] Director’s notes: 10, mostly physical, each with a decoy
- [ ] Simultaneous turns, logged in random order
- [ ] Round-the-table Free Talk
- [ ] Vote and the Director tiebreak
- [ ] Cut reveal and reaction round
- [ ] Win and lose screens with the AIs’ reasoning, plus instant restart
- [ ] Dev log, written as you go

Cut for the jam: voice acting, extra sets, animations beyond Move, Look, Grab, Throw and Give, and all extras (end-of-show review card, “Line!” call, streamer mode, applause).

### Open questions & jam notes

- [ ] Add a fifth persona, so a full 5-actor show is possible.
- [ ] Decide which key pays for the Director and the input LLM.
- [ ] Choose between direct provider connections and a router service (one integration, one key format).
- [ ] Keep or replace the Director tiebreak (provisional).

Submission deadline: 2026-11-15, 5:59 PM PST (2026-11-16 01:59 UTC). The dev log, which competes for the Glass Box prize, must be submitted with the entry and can’t be added later ([forum](https://forums.unrealengine.com/t/vibe-your-way-to-50k-the-2026-epic-ai-megajam-is-coming/2843983?page=2)).

---

## Tab 5: Art Inspiration

### Art direction

The look we settled on: small, chunky robot actors in a bright, stylized 3D game style, putting on homemade plays on a grand 19th-century Paris opera stage. Unlike the images below, this section is written direction.

#### Style

- True 3D in Unreal Engine 5. Never 2D or drawn, and no ink outlines on characters or sets.
- Bright online-game look: chunky, exaggerated proportions, bold silhouettes, smooth stylized materials, glossy painted metal, candy-bright colors and strong colorful rim light.
- Tone: playful, petty slapstick. Never scary: no human is ever shown inside or under a bot.

#### The bots

- Every bot shares one original body: waist-high, with a chunky battery-cell body, a terminal nub on top, a charge meter on the belly, a dark glass face screen with cartoon LED eyes and eyebrows, short bendy arms with mitten hands, and stubby legs with big rubber feet.
- Keep the design original. Never borrow a known character's signature look.
- Players tell the bots apart by body color and head details, since costumes cover the rest.

| Bot | Body | Head and back details | Hidden logo (parody) |
|---|---|---|---|
| The Visionary | Pearl-white, soft blue glow | Serene half-closed eyes | Six-petal knot of tangled charging cables, one plug loose |
| The Worrier | Copper, amber hazard stripes | Wobbly anxious eyebrows | Terracotta starburst, one ray patched with a bandage |
| The Overclocker | Gunmetal | Neon lightning decals, cooling fans built into its back puffing steam, jagged wild eyes | X made of two crossed, sparking lightning bolts |
| The Copycat | Glossy blue chrome | Stiff posture, fake polite smile | Blue infinity loop with two llama ears |
| The Understudy (the player) | Primer grey, one mismatched teal panel | Nub bent to one side, hand-knitted striped scarf, big hopeful eyes | None: no persona or company |

#### Costumes and hidden logos

- Each bot wears a costume that fits its role in the current scene. The costume always covers the chest.
- Each persona's parody logo sits on its chest plate, hidden until the bot is cut. Then the costume is yanked off, the logo shows, and the "[NAME]: AI" stamp lands.
- Backstage, in Scene Prep, the bots wear silk dressing robes in their own colors.
- No real company names or real logos anywhere, only the parodies above.

#### Stage and props

- One stage: a grand 19th-century Paris opera house, with a gold proscenium arch, red velvet curtains with gold tassels, footlights, a crystal chandelier, and horseshoe balconies of robot spectators in top hats with opera glasses.
- Each scene brings a few homemade props the bots can grab and throw, such as a wobbly balcony, a cardboard moon, prop rapiers or a pumpkin coach. Public-domain plays work well, for example the balcony scene from Romeo and Juliet.
- Free Talk: the stage lights drop to a single colorful spotlight pool.
- The Cut: a giant vaudeville hook pulls the cut bot offstage.

#### UI

- Chunky, bold game UI with thick outlined lettering for the scene card, round countdown timer, director's note, command bar, Free Talk chat panel and vote card.
- A floating "YOU" marker over the player's bot.
- The reveal is a huge red rubber stamp reading "[NAME]: AI".

> **Mood reference only. Nothing in these images is a rule to implement.**
>
> They are here for the feel: warm theater light, chunky toy-like robots, a playful and slightly petty stage world. The characters, names, costumes, props, scenes, UI panels, timers, text and layouts are all examples, not requirements.
>
> **Ask before you use anything from them.** Name the image number and the element, then wait for a yes from George Katsaros. Where an image disagrees with the written tabs, the tabs win.

### Image 1 · Backstage

Five robot actors in bathrobes hold sealed director's notes beneath dressing-room mirrors. Each mirror carries a nickname card, and the shelf holds props from future scenes.

*(Image in the doc: robot cast backstage in bathrobes holding director's notes.)*

### Image 2 · The stage

A gilded theater with a "No Humans On Set" banner, a robot audience in the boxes, and the cast mid-duel in a musketeer-style scene.

*(Image in the doc: robot cast mid-duel on a theater stage under a No Humans On Set banner.)*

### Image 3 · A scene in play

The balcony scene from the player's side: a YOU marker, speech bubbles, a countdown clock, a director's note card and a typed command box.

*(Image in the doc: balcony scene with a YOU marker, timer, director's note and command box.)*

### Image 4 · Free Talk

A fairy-tale ballroom scene with a chat panel showing a Free Talk round in progress.

*(Image in the doc: fairy-tale ballroom scene with a Free Talk chat panel.)*

### Image 5 · The Cut

A cut actor is yanked offstage by a giant hook. A vote panel lists the cast's reasons, and a stamp reveals the actor was AI.

*(Image in the doc: a cut robot yanked offstage by a hook beside vote results and an AI reveal stamp.)*
