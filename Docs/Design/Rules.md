# Rules

Everything that happens in one show, from casting to the last cut.

## Cast & personas

- Each show’s AI cast comes from a pool of persona bots: petty parodies of AI lab leaders (see Bot Prompts).
- You have no persona. Every persona whose provider has a key takes an AI seat, and you take one more seat. A show needs at least 3 AI seats.
- Each persona always runs on its own provider, so every AI in a show is a different LLM.
- On stage, every actor goes by a Player name, “Player 1” to “Player 5”, dealt at random each show. Only your screen shows which provider runs each AI. The AIs never see provider names, so a name can’t give you away.
- Cast size is you plus 3 or 4 AIs. Number of scenes = cast size − 1: four scenes with 5 actors, three with 4. That includes one spare scene, which a tie uses up.
- A full 5-actor show needs 4 personas, one per provider.
- Each AI wants two things: to find the human, and to reach the final two itself. Each also has a rival bot it would like to see cut, and when torn between two suspects it leans toward its rival (see Bot Prompts). The rivals are revealed at the end.

## Scene Prep

- Every actor gets the same scene card: a comedy version of a famous story, who each bot plays, and what each one wants. Example: a desert farm kid hiding a tin-can robot from a villain who breathes very loudly. Modern films are parodied only, with new names and no quotes.
- Only the AI actors get the secret director’s note. You don’t, and you know it. Your card shows a clue to it instead: its category in scene 1, such as Props, then a new kind of clue each scene, such as only its vowels or a riddle from the director. No kind of clue comes twice in a show.
- The AIs know you lack the note and see exactly which clue you got. They follow it subtly so you can’t simply copy them, never say it aloud during the scene, and treat anyone who only matches the clue, or copies a turn late, as a suspect.
- The twelve kinds of clue: the category, the vowels only, the consonants only, the first letters, the words scrambled, Pig Latin, the key word hidden, only the key word, emoji, the opposite rule, a riddle from the director, and the note autocorrected.
- Notes are mostly physical, so they show on stage and the game can check them against the log. Examples: “throw something whenever someone lies,” “climb onto the Riser at least once.”
- Scene Prep is a pause. The scene and the stage’s places and props show in a panel in the middle of your screen, with Start the scene under them. Your card on the right shows your role and your want, the note’s clue, and the cast with their roles and wants. The scene starts when you press Start the scene.

## The Scene & acting

- During the scene, your screen shows only your own card: your role, your want and the note’s clue.
- Each scene has 3 turns, with a 30-second timer on yours.
- You act blind on turn 1. After that, read the AIs’ moves and work out the note. Acting early risks guessing wrong; waiting risks copying late.
- Every actor submits a turn, then all turns play out at once. The log records them in random order, so you’re never always last.
- Each turn you click to build one action and type one optional line, then press Action! to send both (see [Turn Input](TurnInput.md)). Your action reaches the log in the same form the AI actors send.
  - Example: Click Move, then Riser, and type “Hello down there!”
- Actions: Move, Look, Grab, Throw, Give, Look around and No action. The AIs and you choose from the same set, by the same rules: one action a turn; Grab takes a prop nobody holds; Throw and Give need a prop you hold; Look can take an actor, a prop or a place; Move goes only to a place, and a throw at a place puts the prop down there. Nobody holds more than two props. The AIs see who holds what.
- Places: Center, Left, Right, Front, Back, Riser and Prop Table, on one clay opera-house stage. The Riser plays whatever the story needs (a balcony, a throne, a cockpit), and each story card brings its own props to the Prop Table.
- Speech: whatever you type in the speech field is spoken as is, with spelling fixed. Caps, emojis and tags stay.
- Mentions: type @ in the speech field and pick a name you see, like @Meta, to speak to one actor. The AIs read it as that actor’s Player name (@Player 2), and they use the same form to speak to someone. Your screen shows every Player name as the name you know.
- Every line, AI or human, is capped at 15 words.
- If an AI’s command can’t be understood or breaks a rule, that actor just looks around, and no error appears in the log. Your builder can’t send an invalid action, but an unfinished one becomes “looks around” when the timer runs out.

## Free Talk

- Before each vote, talk goes around the table in 2–3 rounds, in a new random order each round.
- Everyone gets one line per round and can pass. Your line has no timer.
- Passes are visible: “passed” shows next to anyone who passes. The AIs treat silence, and lines that sound too polished, as evidence.
- AI lines appear after a short typing delay.
- Your lines reach the AIs in exactly the same form as theirs.
- The scene is over, so actors may name the director’s note when they accuse someone. They hold you only to what your clue could tell you.
- Last word: anyone @-mentioned in the final round gets one reply before the vote. You get 15 seconds for yours.

## The Cut

1. Every actor votes in secret, all at once, for who they think is human. You can’t vote for yourself.
2. Whoever gets the most votes is cut. Each vote is then shown with a one-line reason.
3. On a tie, nobody is cut, and the scene still counts against the clock. No one outside the cast ever breaks a tie.
4. Reveal: a big stamp with the cut bot’s provider, such as “OPENAI: AI”, or “YOU: HUMAN” if it was you.
5. Reactions: the cut actor reacts first, then each remaining bot, then you, one line each. You get 15 seconds; when time runs out, what you typed is sent, and an empty field is a pass. Reactions go into the log, so how you react is evidence.
6. Repeat from Scene Prep until two actors remain or the last scene ends. A clapperboard on screen shows the count, such as SCENE 2 / 4.

You win if you make the final two, or if you’re still on stage when the last scene ends. Then every AI, cut or still on stage, reacts to the reveal in one line: the cut robots get back up, still gray, and your robot cheers. The win screen shows every AI’s reasoning, then reveals their rivals. If you’re cut, you lose: the AIs gloat in the reaction round, then the lose screen shows every AI’s reasoning about you, names the reason that got the most votes, and offers an instant restart.

## Emotions

- Every robot shows an emotion while its line plays: a face and a small gesture, such as happy, angry, worried, confused, suspicious or smug, or a calm neutral face.
- Each AI picks its emotion with every reply, a pass included. It's the emotion it acts, not always what it feels: a bot may keep a calm face while it accuses someone, or fake confusion when it's under suspicion.
- Everyone on stage sees every face. The AIs can't see the stage, so the shared log tells them what each face showed, and a face can be evidence.
- Your robot shows emotions too, or one blank face would give you away. The game picks yours from your line, unless you pick it yourself before you send.
- Emotions never show up in the words: no tags or stage directions in any line.

## Onboarding

The first show is the tutorial. Each rule appears once, at the moment it first matters, as one line from a character in the world.

### The Stagehand

- A friendly AI stagehand backstage, the one AI in the building on your side, whispers tips through your earpiece. Its portrait shows beside each tip.
- It explains the category hint inside the fiction: “I could only sneak you the category.”
- Its lines are static text in their own color, on a channel only the player sees. They never enter the shared log.

### What the player sees, and when

| Moment | On screen | Earpiece line (first show only) |
| --- | --- | --- |
| Before the show | Three lines: you’re the only human; each scene the cast cuts whoever seems human; survive to the final two or the last scene | “Don’t act like a robot. Act bored of being one.” |
| Scene Prep | Scene card: story, your role, your want, **Clue: Category**, **Props**, **Note: ██████ (bots only)**. From scene 2, a new kind of clue, such as **Clue: Vowels only**, **\_e\_e\_ \_o\_e \_o \_\_e \_a\_\_.** | “I could only get you the category this time. They have the full note, and they know you don’t. Watch turn 1.” |
| Scene, turn 1 | Action builder, speech field and timer | “Act now and risk guessing wrong, or wait and risk copying late. They notice both.” |
| Free Talk | “Passed” next to anyone who passes | “One line a round. You can pass, but they notice silence. Get @’d in the last round and you get a reply.” |
| The Cut | Vote, reveal, reactions | “Most votes is cut. A tie cuts nobody but burns a scene.” |
| Always | Clapperboard in the corner: **SCENE 2 / 4** | None |
| Lose screen | “YOU: HUMAN”, then each AI’s reason | Names the reason with the most votes: “They caught you copying late.” |
| Win screen | Each AI’s reasoning, then their rivals revealed | “You fooled them. Every one of them.” |

### Supporting pieces

- First-show tips also cover style, one idea per line across the first scene: plain sentences, no caps or emoji, 15 words max, don’t go silent, and don’t over-polish.
- Tips show only on the first show. Later shows keep the scene card, the clapperboard and the “passed” markers. A settings toggle brings the tips back.
- A How to play button opens the full rules in six bullets. It’s never forced.
- The lose screen does the most teaching. Naming the top reason turns a loss into a lesson, and the instant restart lets the player use it right away.
- The itch page carries the same three opening lines, since judges read it first.
