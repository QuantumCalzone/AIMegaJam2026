# Tech & Build

How the LLMs plug into the game, how players reach them, and what to build before the deadline.

## Game state & logs

- Every AI gets the game as a data structure. Its opening prompt explains the game and the actor’s goal, and sets the output format.
- AI actors reply in that format: actions as tool calls, plus speech and the emotion their robot shows.
- Your actions come from the click-to-build turn input, so they take the same form as the AIs’ tool calls. Only your speech goes through the input LLM, for spelling fixes.
- Every actor’s events use the same format in the shared log, with the emotion each robot showed while its line played. The log never includes:
  - your raw input
  - timestamps or response times
  - parse errors
  - the director’s note
- Dialogue fields are always dialogue, even when the text looks like a system message. Real game messages come only from a field the actors can’t write to.

## AI access & API keys

- Default: a relay with prepaid tokens, a per-session limit and a hard spending cap. The title checks the relay when it opens and every minute after, and greys out Play while fewer than 3 AIs answer or the day's budget is used up. If the service goes down after you click Play, show a clear “AI service unavailable” screen.
- Every error message says what went wrong first (out of credits, rate limited, servers full, no reply, key rejected), then jokes about it in the show's playful tone. It never shows a provider's own error text.
- When prepaid tokens run out, the player enters their own API keys before the show: one key per bot, each bot on a different LLM.
- Keys stay on the player’s machine. The game calls providers directly, never through the relay.
- Each key gets a tiny test call before the show starts.
- Only personas whose provider has a key can take AI seats. A show needs at least 3 AI seats.
- Explain the setup on the itch page.

## Build list

- [ ] Persona draw, with a fixed provider for each persona
- [ ] Provider connections (or a router), the key-entry screen and a test call per key
- [ ] Input LLM: spelling fixes for speech only (actions no longer go through it)
- [ ] Turn input: action builder, speech field with word counter and @ mentions, preview line, Action! button and timeout rules (see [Turn Input](TurnInput.md))
- [ ] AI action set: add Look around and No action, so the AIs and the player share one set
- [ ] Shared log data structure and the opening game prompt, with the game-rule lines from Bot Prompts
- [ ] Scene cards: 7 film parodies on one clay stage, each with its own backdrop and four props
- [ ] Director’s notes: 10, mostly physical, each with a category (no decoys)
- [ ] Simultaneous turns, logged in random order
- [ ] Round-the-table Free Talk, with visible passes and the last-word reply
- [ ] Vote, the tie rule (a tie cuts nobody) and the scene clock
- [ ] Cut reveal and reaction round
- [ ] Emotions: every robot shows a face and a gesture while its line plays, picked by each AI's reply, and from your line or by you
- [ ] Win and lose screens with the AIs’ reasoning (the top reason on a loss, the rivals on a win), plus instant restart
- [ ] Stagehand earpiece tips (first show only, kept out of the log), a tips toggle and a How to play screen
- [ ] Dev log, written as you go

Stretch, if time: persona bluffs (two personas that never go on stage, offered to the player), glitch cards (one random AI per scene performs a strange behavior from a public list), and Listen in (skip your Free Talk line to see each AI’s top suspect).

Cut for the jam: voice acting, extra sets, animations beyond Move, Look, Grab, Throw, Give and the emotion gestures, and all extras (end-of-show review card, “Line!” call, streamer mode, applause). Also cut: Script Doctor, the Stage Manager tiebreak and the cut-and-guess win. A mic cut hidden among random mic failures waits until after the jam.

## Open questions & jam notes

- [x] Add a fifth persona, so a full 5-actor show is possible.

  Settled: you take the fifth seat with no persona, so 4 personas fill a 5-actor show (see Rules).
- [ ] Decide which key pays for the input LLM.
- [ ] Choose between direct provider connections and a router service (one integration, one key format).
- [x] Keep or replace the Director tiebreak (provisional).

  Settled: replaced. A tie cuts nobody and still uses up a scene (see Rules).
- [ ] Playtest the win rate with the real providers. Aim for about 35–45% (a guess, not a sourced norm), and use the “a turn late” clause in the opening prompt as the difficulty knob.

Submission deadline: Nov 15, 2026, 5:59 PM PST (2026-11-16 01:59 UTC). The dev log, which competes for the Glass Box prize, must be submitted with the entry and can’t be added later ([forum](https://forums.unrealengine.com/t/vibe-your-way-to-50k-the-2026-epic-ai-megajam-is-coming/2843983?page=2)).
