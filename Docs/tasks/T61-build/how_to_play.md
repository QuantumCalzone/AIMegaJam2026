# How to play: the six bullets (draft)

**DRAFT, waiting for my person's OK.** T61's step 6 shows these to my person before its commit, and only the text they OK goes into `WBP_HowToPlay`. A Mac prep session wrote them on 2026-11-15 from the design doc's Rules tab (rev 27), for the rules as the open tasks leave them: T52 (a tie cuts nobody), T53 (the scene clock), T54 (two ways to win), T55 (no Director AI), T57 ("passed"), T58 (the last word) and T59 (the 15-word cap).

## The bullets

The screen's title is **How to play**. Each bullet starts with a bold lead, like the itch page's "How a show works".

1. **You're the human.** Four AI actors and you, each a robot named "Player 1" to "Player 5". Only your screen shows which lab runs each AI.
2. **Scene Prep.** Everyone gets the same scene card. The AIs also get a secret director's note. You only see its category, and they know it.
3. **The scene.** Three turns. Type what your robot does and says. On turn 1 you act blind; then work out the note, but copy too late and they'll notice.
4. **Free Talk.** A few rounds, one line each. You can pass, but "passed" shows and silence is evidence, and so is a line that sounds too polished. Get @-mentioned in the last round and you get one reply.
5. **The Cut.** Everyone votes in secret for the human. Most votes is cut, and the stamp shows who it really was. A tie cuts nobody but still uses up the scene.
6. **How it ends.** The clapperboard counts the scenes. Make the final two, or still be on stage when the last scene ends, and you win. Get cut and you lose.

Every bullet is 38 words or fewer, its bold lead included. The longest is bullet 4.

## Where each bullet comes from

All from the Rules tab. Nothing here is in the repo's other files word for word.

| # | Rules tab section | The rule |
|---|---|---|
| 1 | Cast & personas | You have no persona; a cast is you plus 3 or 4 AIs, each on its own provider; every actor goes by a Player name; only your screen shows the providers. Written for a full cast of five, since that is the usual show. |
| 2 | Scene Prep | The same card for everyone; only the AI actors get the note; the card shows its category; the AIs know you lack it (T50, T51). |
| 3 | The Scene & acting | 3 turns; you type what to do and say; you act blind on turn 1; acting early risks guessing wrong, waiting risks copying late. |
| 4 | Free Talk | 2 to 3 rounds, one line per round, a pass allowed; "passed" shows (T57); silence and lines that sound too polished are evidence (T57); a last word for anyone @-mentioned in the final round (T58). |
| 5 | The Cut, steps 1 to 4 | A secret vote; the most votes is cut; the reveal stamp; a tie cuts nobody and still counts against the clock (T52); no one outside the cast breaks it (T55, so the Director is not named). |
| 6 | The Cut, step 6, and the paragraph after it | The clapperboard (T53); you win by making the final two or by still being on stage when the last scene ends (T54); if you're cut, you lose. |

## Left out on purpose

- **The 15-word cap (T59).** The stagehand's style tip says it, and the game cuts every line at 15 words anyway. If my person wants it here, the shortest fit is a second sentence in bullet 3: "Every line is capped at 15 words."
- **The 30-second timer.** The Rules tab gives my turn a 30-second timer, but T24 (timers) is optional and not built, and `Docs/ItchPage.md` says there are no timers. If T24 is done before T61, add "You have 30 seconds." to bullet 3.
- **The reactions** (the Cut, step 5) and **the rivals** (Cast & personas). Neither changes what I do to win. The rivals show on the win screen (T60).
- **The controls** (@-mentions, actions, places). The input row's hints and the itch page's Controls section cover them.
