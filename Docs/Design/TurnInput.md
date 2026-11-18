# Turn Input

Each scene turn, you click to build one action and type one optional line, then press **Action!** to send both. Clicking handles everything physical: actions, props, places and targets. Typing handles only what your character says.

## Layout

The turn panel sits at the bottom of the screen. From top to bottom: a preview line in terminal style that updates as you build, the action builder, and the speech field with its Face chip, word counter, Action! button and turn timer.

```text
> throw rose at @Meta: "Oops, my servo slipped."

[Move] [Look] [Grab] [Throw] [Give] [Look around] [No action]
   rose · teacup · umbrella       (targets for the picked action)

[Face: Auto]  Say something (optional)...   12/15   [Action!]   0:21
```

## Building an action

- Pick one action button. Only its valid targets appear as chips:
  - Move: a place (Center, Left, Right, Front, Back, Riser, Prop Table)
  - Look: an actor, a prop or a place
  - Grab: a prop nobody is holding, while you hold fewer than two
  - Throw: a prop you’re holding, then a target (an actor or a place)
  - Give: a prop you’re holding, then an actor whose hands aren’t full
  - Look around and No action: no targets
- The builder offers only moves the game would accept from an AI, checked by the same rules as the AIs’ tool calls. Holding nothing greys out Throw and Give, with the tip “Grab something first.” Holding two greys out Grab, with the tip “Your hands are full.”
- Look around and No action are in the AIs’ action set too, so both sides choose from the same seven.
- Props come from the current scene card.
- Picking a different action clears its targets. Clicking a picked chip again deselects it.
- The default is No action, so a speech-only turn is always valid. One action per turn.

## Saying a line

- Keyboard focus stays in the speech field all turn. Clicking the builder never takes it, so you can type while you click.
- The line is optional, with a hard cap of 15 words. The counter turns red at 15 and blocks more words.
- Typing @ opens a list of actors by the names on your screen, such as @Meta. The mention goes in as one unit (one Backspace removes it), shows as a chip in the preview line and reaches the AIs as that actor’s Player name (@Player 2).
- The speech field never controls actions. Typing “I throw the rose” only says those words.
- The Face chip, left of the speech field, picks the face your robot shows with this line: Auto (the game reads it from your words) or one of the emotions. It goes back to Auto at each of your turns, and a pick shows on a pass or a silent turn too.

## Sending the turn

- Press Action! or Enter. No action with an empty line is allowed: you just stand there.
- When the 30-second timer runs out, the turn sends itself:
  - A finished action goes as built.
  - An unfinished action (picked, but its targets incomplete) becomes “looks around”, the same fallback a bot gets when its command fails.
  - Whatever is typed goes as is.

## What happens after

- The action goes straight into the shared log as a structured action, in exactly the AIs’ tool-call format, with no LLM in between.
- The line goes through the input LLM for spelling fixes only, never for wording or tone. If that call fails or is slow, the line goes as typed, so a turn never stalls.
- The log shows every actor’s turn the same way: a short narration of the action, then the quoted line, such as: Player 3 throws the rose at Player 2. “Oops, my servo slipped.” Your screen shows Player names as the names you know.

## Other phases

- Free Talk: no builder and no timer. The speech field, Action! and a Pass button.
- Last word and reactions after the Cut: no builder. The speech field, Action! and Pass, with 15 seconds each. When time runs out, what you typed is sent; an empty field is a pass.
- The Face chip shows in Free Talk, the last word and the reactions too, and hides in the vote.

## Scope

- For the jam: action buttons, target chips, the speech field with its counter and @ mentions, the preview line, Action!, and the timeout rules.
- Later: clicking props, places or actors on the stage to fill the picked target, and number keys 1–7 to pick actions.
