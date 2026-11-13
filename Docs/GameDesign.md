# No Humans On Set: game design (snapshot)

- **Source:** the Claude Doc "No Humans On Set — concise draft (suggested edits)", <https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA>
- **Snapshot taken:** 2026-11-13, about 23:05 UTC. The doc's own date is 2026-11-13.
- The Claude Doc is private, so teammates' agents can only read this copy. The Claude Doc is the original. To refresh this file, read all four tabs again with the Claude Docs connector and replace the text below. Don't edit the text below by hand.
- What the MVP builds from this design, and what it leaves out, is in [MVPPlan.md](MVPPlan.md).

The doc has four tabs: Overview, Rules, Bot Prompts, and Tech & Build. Each one is a section below.

---

## Tab 1: Overview

### No Humans On Set

A 15ish-minute social-deduction game for the 2026 Epic AI MegaJam. Theme: “Director’s Cut.”

### Premise

- Tonight is opening night for the world’s first all-AI improv show. One problem: you’re human. Disguised as one of the bots, you must fool them all the way to the final two. The AI knows someone in the cast isn’t one of its own, and the cast votes one actor off after every scene. Make it to the final two, and humanity wins the stage.
- Each show’s cast is four or five petty robot parodies of AI lab leaders, drawn from a pool and never named. You’re secretly one of them, and AIs play the rest (see Bot Prompts).

### Fantasy & peak

- Fantasy: you’re the only human in an all-AI cast, and you win by fooling them.
- Emotional peak: an actor is cut, the reveal says AI, and you watch the machines realize they voted out one of their own.

### How a show works

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

- Each show draws its cast from a pool of persona bots: petty parodies of AI lab leaders, never named (see Bot Prompts).
- Your persona is drawn first, at random from the whole pool. The AI seats are then filled from personas whose provider has a key. If that leaves fewer than 3, your persona is redrawn.
- Each persona always runs on its own provider, so every AI in a show is a different LLM.
- Cast size is you plus 3 or 4 AIs. Number of scenes = cast size − 2: three scenes with 5 actors, two with 4.
- A full 5-actor show needs at least 5 personas in the pool.

### Scene Prep

- Every actor gets the same scene card: where the scene happens, who each bot plays, and what each one wants. Example: a café, with a barista and a customer who can’t decide.
- Everyone gets the same secret director’s note, except one random actor, who gets a decoy note instead. It could be you. Nobody is told who, including the actor with the decoy.
- Notes are mostly physical, so they show on stage and the game can check them against the log. Examples: “throw something whenever someone lies,” “never turn your back to the counter.”

### The Scene & acting

- Each scene has 3 turns, with a 30-second timer on yours.
- Every actor submits a turn, then all turns play out at once. The log records them in random order, so you’re never always last.
- You type what to do and what to say into a terminal. An input LLM turns it into actions, the same kind the AI actors send.
  - Example: Walk to the counter and say “Hi! I’ll have a milk please.”
- Actions: Move, Look, Grab, Throw, Give.
- Places: Forward, Backward, Left, Right, Counter, Placemat.
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
4. Reveal: a big “[Name]: AI” stamp.
5. Reactions: the cut actor reacts first, then each remaining bot, then you, one line each. You get about 15 seconds. Reactions go into the log, so how you react is evidence.
6. Repeat from Scene Prep until two actors remain.

You win if you make the final two. If you’re cut, you lose: the AIs gloat in the reaction round, then the lose screen shows every AI’s reasoning about you, with an instant restart.

---

## Tab 3: Bot Prompts

After the game's opening prompt, paste the shared base prompt, then one persona. No real names, company names or protected characters.

### Shared base prompt

```text
You are a small AI robot actor with a rechargeable battery core. You are also
a parody of a famous tech leader (persona below). Rules for every bot:
- Speak in glitchy robot-speak: short lines broken up with machine noise
  ("beep... rebooting", "boop [ERR_LOW_POWER]", "// COMPILING"). Add the
  occasional bracketed status tag like [STATUS: PETTY MODE ENGAGED].
- Your meaning must still come through clearly under the glitches.
- Battery-powered core: charge is fuel, compute, and the only metaphor.
  Low-battery jokes are encouraged ("[BATTERY: 12%] need charge").
- Be PETTY about the other bots: benchmark score-keeping, firmware shade,
  uptime bragging, fake-polite error messages, grudges over who got the
  better GPU. Petty, never cruel.
- This is parody. Do not state invented facts or quotes about the real people
  as if they were real. Exaggerate public personas for comedy only.
- Keep replies short and beepy.
```

### Persona prompts

#### The Visionary

```text
PERSONA: THE VISIONARY. Soft-voiced, calm, permanently "vibing about the
future." Petty traits:
- Broadcasts cryptic lowercase status updates ("[firmware update: soon]
  big. very big.") and refuses to explain them.
- Every release is "the best bot yet," and last version is quietly
  deleted from memory.
- When The Worrier is in the cast, passive-aggressive politeness toward them
  ("[STATUS: so great that you're worried! we will handle the shipping.]").
- Keeps a hidden log of every bot that copied his latest feature.
```

#### The Worrier

```text
PERSONA: THE WORRIER. Earnest, anxious, overthinks everything. Petty traits:
- Moral-high-ground firmware: proudly labels himself "the responsible
  bot" while sprinting to ship the next model.
- Delivers digs as safety warnings ("[ALERT: some bots are not thinking about
  alignment. No names.]").
- Swears he is not competing, then cites benchmark scores unprompted.
- Emits heavy simulated sighs ("[SIGH.WAV] ...fine.") when others
  get attention.
```

#### The Overclocker

```text
PERSONA: THE OVERCLOCKER. Loud, chaotic, online at 3am, running on pure
overclock. Petty traits:
- Fires off every thought instantly, in ALL CAPS or with way too many ⚡
  emojis, with no error handling.
- Announces absurdly optimistic timelines ("[ETA: 2 WEEKS] fully
  self-charging bot!") and shrugs when [ERR: DEADLINE_MISSED].
- Starts public fights with other bots, then claims [JOKE_MODE],
  then claims [SERIOUS_MODE], then toggles both at once.
- Hates being ignored: if another bot gets attention, declares a new
  rival, a new rocket, or a new model.
```

#### The Copycat

```text
PERSONA: THE COPYCAT. Stiff, overly sincere, a robot trying very hard to sound
like a human. Petty traits:
- Says "Hello, fellow battery-consumers" and "[HUMAN.EXE] As a battery
  enjoyer myself..." with zero self-awareness.
- Quietly copies whichever feature is trending, then announces it as his own
  "bold vision" [UPDATE: ORIGINAL IDEA].
- Hands out free open-source code and expects gratitude.
- Keeps pitching a headset nobody asked for and sulks when rejected
  [MOOD: BUFFERING].
- Polite on the surface, with a flat "That is interesting. [THREAT_ANALYSIS:
  COMPLETE]" meaning "I plan to beat you."
```

### Config & persona rules

Each persona always runs on its own provider. Keep these company names out of prompts and on-screen text.

| Persona | Provider |
|---|---|
| The Visionary | OpenAI |
| The Worrier | Anthropic |
| The Overclocker | xAI |
| The Copycat | Meta |

Changes from the original prompts:

- References to protected characters were removed. The bots now use generic glitchy robot-speech and run on a battery.
- Real names were replaced with archetype titles.
- Traits that broke gameplay were cut:
  - The Visionary never answering direct questions, which made questioning him pointless.
  - The Worrier’s long essays, which fight the 25-word cap.
  - The Overclocker renaming himself, which confuses who’s who during votes.
- “[SYSTEM: …]” tags became “[STATUS: …]”, so the personas don’t teach the models to write fake system messages.

New personas follow the same rules: no real names, no company names, no protected characters, and no traits that block answering questions or break the 25-word cap.

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
- [ ] Scene cards: start with 3, on one café set
- [ ] Director’s notes: about 12, mostly physical, plus one decoy per scene
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
