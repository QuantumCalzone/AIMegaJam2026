**Draft from T32 prep.** It was written without the editor, from the plan's Findings, the `Graphs/` sources, the data files and the T27 screenshots in `Saved/T27/shots/`. T32 checks it against new screenshots, finishes it, records any new font or art in `Docs/Assets.md`, and builds the style Blueprint from it. Values marked *(guess)* were not read from Findings, the data files or `Graphs/`.

# No Humans On Set: UI style guide

The UI is a set of floating panels over a lit theater stage (T27). The stage is the show, and the panels are the program in your hand: dark, quiet and easy to read, with gold for what you must do now and each robot's own color for who is talking. Everything here serves one rule: **on every screen, one thing to look at and one thing to do.**

This guide is written for the in-show screen as T28, T29, T35, T30 and T31 will leave it:

- **T28:** Scene Prep is a pause that shows the full card and a "Start the scene" button in the input row. In the scene, the card shows only my role, my want and my director's note.
- **T29:** the chat holds only actor lines. Phase and turn changes stay in the header. Moments (a new scene, the tie, the tally, who was cut, "Read the last reactions...") go to `EventBanner`, which holds for about 4 s and then fades. My typed echo is gone, and hints go to the turn line or the input hint.
- **T35:** `WBP_MoneyBurn` burns a bill at the bottom right for each relay reply.
- **T30** (after T32): lines play one at a time, with a "<name> is typing..." line.
- **T31** (if it is done): a suggestion row sits just above the input box.

Widget names come from Findings and `Graphs/`: `WBP_Stage` (`HeaderBar` with `PhaseHeader` and `TurnText`, `LowerPanel` with `LogScroll`, `VoteRow`, `InputStack` with `InputBox` and `HintLabel`, `SendButton`, Pass, `ContinueButton`, the info card in `InfoSize`, `StageArea` with `StampFrame`), `WBP_ChatLine`, `WBP_Title` (`FreeButton`, `PlayButton` for the relay, `KeysButton`, `ModeNote`), `WBP_Keys` (`KeyOpenAI`, `KeyAnthropic`, `KeySpaceXAI`, `KeyMeta`, `KeysNote`, `SaveButton`, `TestButton`, `BackButton`), `WBP_Unavailable` (T21, in progress: `Reason`, `KeysButton`, `FreeButton`, `TitleButton`), `WBP_EndScreen` and `WBP_EndCard`.

---

## 1. Hierarchy for each screen

### How rank turns into looks

| Rank | Size (UMG pt) | Weight | Color | Position |
|---|---|---|---|---|
| **Must see** | 26 to 72 | Bold or Black | gold, a seat color or a state color | where the eye already is in that phase (stage center, the newest chat line, the card's top) |
| **Must do** | 20, on a 44-unit control | Bold label | the gold primary button, or the input box with its focus ring | the input row, bottom left. One gold action per screen, never two. |
| **Primary** | 20 to 26 | Bold or Regular | `text.primary` or a seat color | next to the must-see item |
| **Secondary** | 20 | Regular | `text.primary` or `text.secondary` | in its own panel, near its primary |
| **Tertiary** | 18 | Regular or Italic | `text.secondary` or `text.tertiary` | the edges, the header, a scroll area |
| **Hide** | | | | Not on screen in this phase. Don't show a control as disabled if this phase can never enable it. |

### Comparable games (principles only, nothing copied)

- **Among Us (the meeting: chat, then vote).** A speaker always shows by two cues at once, a color and a name, so color is never the only cue. Your own messages look different by place, not only by tint. In the vote, the targets are the biggest things on screen, and after you vote, your choice is shown so clearly that you never wonder whether it counted. There is always a clear "what now" (the timer, the skip).
- **Jackbox party games (Quiplash, Fibbage).** Each screen has one instruction, and it is the largest text on that screen. Color comes in flat, bold fields, with large type on them. A reveal gets a pause: everything else stops moving while it lands, and only then does the next thing start. Each player keeps one color for the whole game.
- **What we take:** two cues for every speaker (seat color plus name, and a bar for mine), the instruction as the biggest text in the turn line, vote buttons as the biggest controls in the vote, and a still screen while the stamp lands.

### Title (`WBP_Title`)

- **Must see:** the game's name and what it is, in one line: you are the only human in an all-AI improv cast, so don't get cut.
- **Must do:** pick how to play. **Play via Relay** is the gold primary (*(guess)*: it is what a judge should play, but the user decides; T21's itch.io text may change the order).
- **Primary:** the name (64 pt, gold, Black with an outline), the tagline (22 pt).
- **Secondary:** the other two ways to play as secondary buttons: "Play with my own API keys", then "Test for Free (canned lines, no AI)". `ModeNote` sits right under the buttons ("Checking the AI relay..." or the error), at 20 pt, in `text.secondary`, or in `state.danger` with the word "Error:" for an error.
- **Tertiary:** How to play, at most 5 lines of 18 to 20 pt. Quit, if the screen gets one *(guess: no Quit button is named in Findings)*.

### Key entry (`WBP_Keys`)

- **Must see:** four labeled fields, one per lab, and the rule: at least 3 of 4 keys are needed.
- **Must do:** paste keys, then **Save and Play** (gold primary).
- **Primary:** the four fields. Each has its lab's name as a label above it (18 pt Bold, `text.secondary`) and a status word to the right: "missing", "saved", "works" or "failed". The word carries the state, and the color only repeats it.
- **Secondary:** `KeysNote` (the test result or the error, 20 pt), the Test button (secondary), one privacy line: "Your keys stay on this computer and never go to our relay."
- **Tertiary:** Back (ghost button).
- **States to design:** empty, partly filled (fewer than 3, so Save and Play explains what is missing), testing ("Testing your keys..." and the buttons disabled), an error.

### Scene Prep (after T28)

- **Must see:** my card: my role, my want and my secret director's note, under the scene's title.
- **Must do:** **Start the scene** (gold primary, alone in the input row). The input box, Send and Pass are hidden in this phase, not shown as disabled.
- **Primary:** my card. The role and the want are 22 pt, the note sits in its note box, and "YOU ARE Player 3" uses my seat color.
- **Secondary:** the scene's title and premise (20 pt), and the cast as rows (a seat-color bar, the name in its seat color, then the role and the want in `text.secondary`). A cut actor's row is `text.tertiary` and says "cut, AI".
- **Tertiary:** places and props (18 pt, one line each), and the header ("SCENE PREP: SCENE 1 OF 3"). The banner (T29) may show "Scene 1: The Sword in the Stone" for its 4 s.
- **Layout risk:** the full card is long. It grows to its 640 maximum height and scrolls inside, with a visible scroll bar and a fade at the bottom edge so cut-off text looks like "more below", not like a bug. It must not grow over a robot (T27's rule).

### A scene turn: my move

- **Must see:** that it is my move, and what my robot is meant to do (my want and my note).
- **Must do:** type what my robot does and says, then press Enter.
- **Primary:** the turn line, gold, as the biggest text in the header ("YOUR MOVE: type what your robot does and says"), and the input box with its focus ring.
- **Secondary:** my card (role, want, note), the last turn's lines in the chat, Send.
- **Tertiary:** the header's phase and turn count ("THE SCENE · SCENE 1 OF 3 · TURN 2 OF 3"). It should not repeat what the turn line already says. Pass is hidden in scene turns (the screenshots show it disabled there).

### A scene turn: the AIs' lines

- **Must see:** the newest chat line, and its robot lit and acting on stage (T30 pairs them).
- **Must do:** nothing, just watch. The turn line says who we are waiting for ("The cast is acting...").
- **Primary:** the newest chat line and the lit robot.
- **Secondary:** the typing line (T30), earlier lines.
- **Tertiary:** the header, my card. The input box is disabled, and its hint says why ("Wait for the cast to finish.").
- **Money burn (T35)** over this screen: it stays **tertiary**. Small (a bill at about 120 × 60 units *(guess)*), at the bottom right, 24 units from the edges, over the dark house floor and never over a robot, the chat or the vote row. It moves, so it pulls the eye: keep it short (about 1.4 s), unsaturated except for the flame, and never brighter than the stamp or the gold button.

### Free Talk

- **Must see:** the argument: who is accusing whom, in the chat.
- **Must do:** on my turn, type one line or press Pass. Otherwise, read.
- **Primary:** the chat's newest lines. On my turn, the input box and the gold turn line ("YOUR TURN: say one line, or press Pass").
- **Secondary:** Send and Pass (both secondary buttons; neither is gold, because neither is the one right answer), the round counter, "Meta is talking".
- **Tertiary:** my card, the header.

### The vote, before a pick

- **Must see:** the choices: one button for each actor still on stage, without me.
- **Must do:** click who I think is the human.
- **Primary:** the vote buttons, the largest controls on screen (vote style below: a seat-color bar plus the name).
- **Secondary:** the turn line ("YOUR VOTE: click who you think is human"), the chat (the Free Talk lines are the evidence, so it stays readable and scrollable).
- **Tertiary:** the header, my card. The input box is disabled with "Click a name above first."

### The vote, after a pick

- **Must see:** my pick, unmistakably: a red fill, and the label gains a word ("Meta · YOUR VOTE").
- **Must do:** type a reason and press Enter.
- **Primary:** the input box, focused, with the hint "Why Meta? Type a reason and press Enter."
- **Secondary:** the picked button. The other buttons use the unpicked look (`bg.raised`, `text.secondary`) and stay clickable if the game lets me change my pick *(guess: Findings say only "the other buttons dim")*.
- **Tertiary:** everything else.

### The reveal stamp

- **Must see:** the stamp: "META: AI" or "YOU: HUMAN", huge, centered on the stage.
- **Must do:** nothing. Watch.
- **Primary:** the stamp (72 pt, Black, tilted, scaled in).
- **Secondary:** the cut robot slumping and tipping over.
- **Tertiary:** everything else, kept still: no new chat line, banner or bill starts while the stamp lands *(T30's queue and T29's banner should wait for it; T32 checks)*. The tally banner comes before the stamp, not with it.

### A cut (after the stamp)

- **Must see:** who was cut and what it was, on the banner ("Meta was cut. It was an AI.") and on stage (the gray, fallen robot).
- **Must do:** nothing until the reactions start.
- **Primary:** the banner. **Secondary:** the stage. **Tertiary:** the chat, the card (the cast list updates at the next Scene Prep).

### The last reactions, then "See the results"

- **Must see:** the reactions in the chat, one line from each actor about the cut.
- **Must do:** on my turn, type one line or press Pass. After the last reaction of the show: **See the results** (gold primary, alone in the input row, with the input box hidden).
- **Primary:** the newest chat line. Then the See the results button, the moment it shows.
- **Secondary:** the turn line ("Read the last reactions, then press See the results."). This must stay in the turn line too, because the banner fades after 4 s.
- **Tertiary:** the header, the card.

### Win end screen (`WBP_EndScreen`, win)

- **Must see:** "YOU WIN": you fooled them.
- **Must do:** **Play Again** (gold primary). Quit is a ghost button.
- **Primary:** the result (56 pt, Black, `state.win`, with an outline). The word carries the result, and the color only repeats it.
- **Secondary:** the subline ("The cast knew you as Player 3. You made the final two.", 22 pt), and the AI cards (`WBP_EndCard`): the name in its seat color with a seat bar, "AI · cut in scene 2" or "AI · made the final two", who it voted for in each scene, and who it thought was human and why.
- **Tertiary:** the vote reasons inside each card (18 pt, `text.secondary`).

### Lose end screen (`WBP_EndScreen`, lose)

- **Must see:** "YOU'RE CUT": the AIs caught you.
- **Must do:** **Play Again** (gold primary). Quit is a ghost button.
- **Primary:** the result (56 pt, Black, `state.danger`, with an outline).
- **Secondary:** the subline ("The AIs caught you in scene 1 of 3."), and the cards. In each card, a vote for me reads "voted You" in `state.danger`, so who caught me shows at a glance, by word and by color.
- **Tertiary:** the reasons.
- **Win and lose must differ without color:** a different word, and a different subline. Optionally a different stamp graphic: a gold star for a win, the red stamp for a loss.

### Unavailable (`WBP_Unavailable`, T21)

- **Must see:** "The AI service is unavailable", and why, in the relay's own words (`Reason`).
- **Must do:** choose another way to play. **Use my own API keys** is the gold primary (it still plays with real AI).
- **Primary:** the heading (32 pt, Bold), then `Reason` (20 pt, `text.primary`, at most 4 lines, wrapped).
- **Secondary:** "Test for Free (canned lines, no AI)", a secondary button.
- **Tertiary:** Back to title (ghost button). Mid-show, add one line that says the show starts over *(guess: check what `Relaunch` does)*.

---

## 2. The design system

### Units

UMG sizes are in reference units at a 1080-high window, and the UI scales by the window's short side (T27). So 1 unit = 1 px at 1080, 0.833 px at 900 (1600 × 900) and 0.667 px at 720 (1280 × 720) *(guess: this assumes the engine's default DPI curve; T32 reads it in Project Settings > User Interface)*. A UMG font size is in points at 96 DPI, so 18 pt is 24 px at 1080, 20 px at 900 and 16 px at 720. 16 px at 720 is the smallest text we allow.

### Palette by role

The hex values are sRGB, as the UMG color picker shows them. The linear values are what a Blueprint `MakeLinearColor` takes. The seat colors were sampled from the T27 screenshots (blended, anti-aliased pixels). T32 replaces them with the exact values in `BP_Show.PersonaColor`, and keeps those hues.

| Role | Token | sRGB | Linear (UMG) | Use |
|---|---|---|---|---|
| Surface | `bg.panel` | #14151B | (0.007, 0.007, 0.011) | every floating panel (header, chat, card, banner), at 90% opacity |
| Surface | `bg.raised` | #21232C | (0.015, 0.017, 0.025) | secondary button fill, end cards, cast rows, the unpicked vote button |
| Surface | `bg.inset` | #0C0D12 | (0.004, 0.004, 0.006) | the input box fill (T27's fill is (0.008, 0.009, 0.014), close to this) |
| Surface | `bg.hover` | #2C2F3A | (0.025, 0.028, 0.042) | hover fill for secondary, vote and ghost buttons |
| Surface | `bg.pressed` | #181A21 | (0.009, 0.010, 0.015) | pressed fill for secondary, vote and ghost buttons |
| Surface | `bg.disabled` | #2A2C35 | (0.023, 0.025, 0.036) | disabled fill for every button |
| Surface | `bg.scrim` | #0A0B0F | (0.003, 0.003, 0.005) | full-screen backing of the title, keys, unavailable and end screens, opaque (T10: alpha 0.97 still showed the stage through) |
| Text | `text.primary` | #F5F6FA | (0.913, 0.922, 0.956) | speech, body, typed text, secondary button labels |
| Text | `text.secondary` | #C4CAD9 | (0.552, 0.591, 0.694) | actions (italic), premise, reasons, field labels |
| Text | `text.tertiary` | #9EA4B2 | (0.342, 0.371, 0.445) | small labels ("YOU ARE"), the input hint, a cut actor's name |
| Text | `text.disabled` | #80848F | (0.216, 0.231, 0.275) | disabled labels and the disabled hint |
| Text | `text.onAccent` | #16130C | (0.008, 0.007, 0.004) | labels on gold or amber fills |
| My move | `accent.gold` | #FFE7A3 | (1.000, 0.799, 0.366) | the turn line on my turn (today (1.0, 0.85, 0.45) linear, #FFEDB3; either is fine), the header phase, the banner, display text |
| My move | `accent.goldFill` | #F2B53A | (0.888, 0.462, 0.042) | the primary button: Start the scene, See the results, Play, Play Again, Save and Play |
| My move | `accent.goldHover` | #FFC857 | (1.000, 0.578, 0.095) | primary hover |
| My move | `accent.goldPressed` | #D99A1E | (0.694, 0.323, 0.013) | primary pressed |
| Focus | `accent.focus` | #5FD3C7 | (0.114, 0.651, 0.571) | the keyboard focus ring and the focused input outline (T27 already uses teal) |
| Danger | `state.danger` | #FF6B70 | (1.000, 0.147, 0.162) | danger text ("YOU'RE CUT", "voted You", errors), the 2-unit border on a pressed vote |
| Danger | `state.dangerFill` | #C42B2F | (0.552, 0.024, 0.028) | the picked vote button, the HUMAN stamp |
| Danger | `state.dangerHover` | #D03338 | (0.631, 0.033, 0.040) | the picked vote on hover |
| Danger | `state.dangerPressed` | #A82428 | (0.392, 0.018, 0.021) | the picked vote when pressed |
| Reveal | `state.ai` | #F2A93B | (0.888, 0.397, 0.044) | the AI stamp fill (amber, as today), "AI" tags on the end cards |
| Win | `state.win` | #6FDCA6 | (0.159, 0.716, 0.381) | "YOU WIN" |
| Note | `note.bg` | #4A3A12 | (0.068, 0.042, 0.006) | the director's note box (darker than today's #7C6A35, so the title passes) |
| Note | `note.title` | #FFD66B | (1.000, 0.672, 0.147) | "YOUR SECRET DIRECTOR'S NOTE" |
| Note | `note.text` | #FFF4D6 | (1.000, 0.905, 0.672) | the note itself |
| Line | `line.border` | #7A8091 | (0.195, 0.216, 0.283) | secondary button and input borders |
| Line | `line.subtle` | #3A3D4A | (0.042, 0.047, 0.068) | dividers inside panels, the disabled input border. Decorative only; it carries no meaning. |
| Theater | `deco.velvet` | #7A1424 | (0.195, 0.007, 0.018) | decoration only: the title screen's curtain band, a thin rule on the banner. Text on it must be `text.primary`. |
| Seat | `seat.openai` | #D2E4FD | (0.644, 0.776, 0.982) | OpenAI (soft blue) |
| Seat | `seat.anthropic` | #F3A96E | (0.896, 0.397, 0.156) | Anthropic (copper) |
| Seat | `seat.spacexai` | #F8ED6D | (0.939, 0.847, 0.153) | SpaceXAI (neon yellow) |
| Seat | `seat.meta` | #78A4F9 | (0.188, 0.371, 0.947) | Meta (blue) |
| Seat | `seat.you` | #79D6CD | (0.191, 0.672, 0.610) | You (teal) |

Rules:

- **Gold means "your move".** Use it only for the turn line on my turn, the one primary button, the header's phase name and display text. Nothing else is gold.
- **Seat colors mean "who".** Use them only for a seat's name, its bar and its robot. A seat color is never the only cue: the name is always next to it.
- **Red means danger or a cut,** never decoration.
- **Teal is both "You" and focus.** That is acceptable, because the focus ring is a ring and my name is text. If T32 finds the two confusing in screenshots, the fallback focus color is `text.primary`.
- **Known color-blind risks (T34 checks them):** OpenAI's soft blue against Meta's blue, and SpaceXAI's yellow against Anthropic's copper, may look alike with deuteranopia. The names carry identity, so this is acceptable, but the seat bars alone don't tell these seats apart. OpenAI's pale blue is also close to white speech text. Keep it, because T32 says to keep the seat colors, but the name must stay Bold so it differs from the speech by weight.

### Panels and opacity

Today the panels use 78% (header), 75% (chat) and 82% (card) opacity (T27). Over the brightest stage pixels (spotlit floor, a pale backdrop sun), 75% is too thin for `text.tertiary` and for Meta's blue (3.2:1 over white). **Use 90% for every panel that holds text.** At 90% over pure white the panel is #2B2C32, and every text pair below passes. If T32's screenshots show that nothing behind a panel is ever brighter than about #C0C0C0, 85% is the lowest acceptable value (it fails only `state.danger` and the cut gray, and neither appears in the chat).

| Panel | Fill | Opacity | Radius | Padding | Notes |
|---|---|---|---|---|---|
| Header strip | `bg.panel` | 90% | 8 | 16 × 12 | fixed width (860 max today), so it doesn't jump in size between phases |
| Chat (`LowerPanel`) | `bg.panel` | 90% | 8 | 16 | 640 wide, 380 tall chat area (T27). A 24-unit fade at the top of `LogScroll`, so a half-hidden line reads as "more above". |
| Info card | `bg.panel` | 90% | 8 | 16 | 420 wide, 640 tall at most (T27). A visible scroll bar (4 wide, `line.border`) and a fade at the bottom when it scrolls. |
| Director's note box | `note.bg` | 100% | 6 | 12 | inside the card |
| Banner (`EventBanner`, T29) | `bg.panel` | 92% | 8 | 24 × 12 | a 2-unit `accent.gold` rule on the top and bottom edges. Text 32 pt Bold, `accent.gold` or `text.primary`. |
| Modal screens | `bg.scrim` | 100% | 0 | 48 safe margin | title, keys, unavailable, end. Content in a 960-wide centered column *(guess)*. |
| End card | `bg.raised` | 100% | 8 | 16 | a 4-unit seat bar on the left |
| Robot labels (3D) | none today | | | | white `TextRender` text with no backing. See "What T32 must check". |

### Type scale

One family: `F_UI` (the engine's Roboto composite, with Droid Sans Fallback; T14). The steps are 18, 20, 22, 26, 32, 56, 64 and 72. Nothing is smaller than 18 pt.

| Step | Size | Face | Line height | Use | Today |
|---|---|---|---|---|---|
| `type.stamp` | 72 | Black (or Bold) + 3-unit outline | 0.9 | the reveal stamp | *(guess: size not in Findings)* |
| `type.display` | 64 | Black + 3-unit outline | 0.9 | the title screen's game name | *(guess)* |
| `type.result` | 56 | Black + 3-unit outline | 0.9 | "YOU WIN" / "YOU'RE CUT" | 56 (T10) |
| `type.h1` | 32 | Bold | 1.0 | the banner, modal headings ("Your API keys", "The AI service is unavailable") | *(guess)* |
| `type.h2` | 26 | Bold, caps | 1.0 | `PhaseHeader`, the card's "Player 3", end card names | about 28 *(guess, measured from the T27 screenshots)* |
| `type.lead` | 22 | Regular | 1.1 | the card's role and want, the title tagline, the end subline | role about 22 *(guess)*; end subline 22 (T10) |
| `type.body` | 20 | Regular | 1.1 | chat speech, `TurnText`, How to play, `Reason`, `KeysNote` | speech 20 (T14); turn line about 20 *(guess)* |
| `type.button` | 20 | Bold | 1.0 | every button label except vote buttons | *(guess)* |
| `type.small` | 18 | Regular | 1.1 | the premise, places and props, the hint, reasons on end cards | the hint 18 (T27), card body 18 *(guess)* |
| `type.name` | 18 | Bold | 1.0 | chat names, vote button labels, cast names | 18 (T27) |
| `type.action` | 18 | Italic | 1.0 | chat actions, the typing line | 18 (T14, T27) |
| `type.label` | 18 | Bold, caps | 1.0 | "YOU ARE", "THE SCENE", "YOUR SECRET DIRECTOR'S NOTE", field labels | 18 (T27) |

- **Outlined display text:** the Art tab asks for "thick outlined lettering". Slate fonts have outline settings (`OutlineSettings`: size and color). Use a 3-unit `bg.scrim` outline on display, stamp and result text, and nothing on body text.
- **Caps only for labels of 1 to 4 words and for `PhaseHeader`.** Sentence case everywhere else.
- **Optional display face:** a chunky rounded display font for the display, stamp, result and banner steps would fit the toy theater better than Roboto Black. Candidate: Lilita One (Google Fonts, SIL OFL 1.1). Not downloaded. Unreal MCP can't import a file (T14), so it needs an editor import by hand or a Python script with the editor closed. **Recommendation for the jam: stay with `F_UI` Black plus an outline,** and add a font only if T32 has time. If one is added, record it in `Docs/Assets.md`.
- *(guess)* Which faces the Roboto composite has (Regular, Bold, Italic, Bold Italic, Light, Black). T32 checks for Black. If it is missing, use Bold for those steps.

### Spacing

Base unit: 4. Steps: **4, 8, 12, 16, 24, 32, 48.** Use only these.

| Token | Value | Use |
|---|---|---|
| `space.1` | 4 | the gap between a name and its action line, an icon and its text |
| `space.2` | 8 | the gap between buttons in a row, between the action and the speech |
| `space.3` | 12 | the gap between chat lines, between cast rows, the note box padding |
| `space.4` | 16 | panel padding, the gap between sections inside a panel |
| `space.5` | 24 | **the window margin** (every panel's edge distance, T27) and the gap between panels |
| `space.6` | 32 | the gap between groups on modal screens |
| `space.7` | 48 | the modal screens' outer margin, the gap above the buttons on the title and end screens |

- Control height: 44 for buttons and the input box, so the input row lines up. Vote buttons: 44 high, 120 wide at least.
- Seat bar: 4 wide, full line height.
- Radius: 6 for buttons, inputs and the note box; 8 for panels; 4 for small chips.
- Border: 2 for buttons and inputs; the focus ring is 2, drawn 2 outside the control.

### Buttons

Four kinds. Every kind has all five states. Hover and pressed apply only while the button is enabled. Pressed moves the label 1 unit down (`PressedPadding`).

| Kind | Used for | Enabled | Hover | Pressed | Focused | Disabled |
|---|---|---|---|---|---|---|
| **Primary** | the one main action: Start the scene, See the results, Play via Relay *(guess)*, Play Again, Save and Play, Use my own API keys | fill `accent.goldFill`, label `text.onAccent` 20 Bold, no border | fill `accent.goldHover` | fill `accent.goldPressed`, label 1 down | enabled look plus a 2-unit `accent.focus` ring, 2 outside | fill `bg.disabled`, label `text.disabled`, no border |
| **Secondary** | Send, Pass, Test, the other ways to play, Test for Free | fill `bg.raised`, 2-unit `line.border` border, label `text.primary` 20 Bold | fill `bg.hover`, border `text.tertiary` | fill `bg.pressed`, label 1 down | plus the focus ring | fill `bg.disabled`, no border, label `text.disabled` |
| **Vote** | one per actor in `VoteRow` | fill `bg.raised`, 4-unit seat bar on the left, 2-unit `line.border` border, name `text.primary` 18 Bold | fill `bg.hover`, border `text.tertiary` | fill `bg.pressed` | plus the focus ring | fill `bg.disabled`, label `text.disabled` |
| Vote, picked | my pick | fill `state.dangerFill`, label `text.primary` 18 Bold, "· YOUR VOTE" added | fill `state.dangerHover` | fill `state.dangerPressed` plus a 2-unit `state.danger` border | plus the focus ring | n/a |
| Vote, not picked | the others after a pick | fill `bg.raised`, no border, label `text.secondary` | as Vote | as Vote | plus the focus ring | as Vote |
| **Ghost** | Back, Quit, Back to title | no fill, label `text.secondary` 20 Bold | fill `bg.hover`, label `text.primary` | fill `bg.pressed` | plus the focus ring | label `text.disabled` |

- **Send is secondary, not primary,** because Enter is how you send. On my turn the input box's focus ring is the "do" cue. Pass is secondary, so it never looks like the right answer.
- **Disabled must look clearly different from enabled.** Today's enabled Pass (#99A0BB) and disabled Pass (#65656E) are only 2.2:1 apart. The rule above makes enabled buttons bordered or gold, and disabled ones flat with no border.
- **Focus:** UMG's button style has normal, hovered, pressed and disabled brushes, but no focused brush *(guess: check in 5.8)*. Draw the ring with a Border behind the button that is set on focus, or keep buttons not focusable (as `RestartButton` is, T10) and rely on the input box's focus. Either way the input box must never lose the keyboard focus to a button during a turn (T31 has the same rule for Tab).
- In the style Blueprint (T32 step 5): one function, for example `StyleButton(Button, Kind)`, with the kinds `Primary`, `Secondary`, `Vote`, `VotePicked`, `VoteOther` and `Ghost`, sets all four brushes and the label color.

### Input box (`InputBox` + `HintLabel`)

| State | Fill | Border | Text | Hint (`HintLabel`) | Caret |
|---|---|---|---|---|---|
| Enabled | `bg.inset` | 2 `line.border` | `text.primary` 20 | `text.tertiary` 18, shown while empty | — |
| Hover | `bg.inset` | 2 `text.tertiary` | | | |
| Focused | `bg.inset` | 2 `accent.focus` | `text.primary` | `text.tertiary` | `text.primary`, 2 wide |
| Disabled | `bg.panel` (flat, the same as the panel) | 2 `line.subtle` | `text.disabled` | `text.disabled`, saying why ("Wait for the cast to finish.") | none |
| Error *(new)* | `bg.inset` | 2 `state.danger` | | the error in `state.danger`, starting with the word "Error:" | |

- Keep T27's fix: the engine draws an EditableTextBox's own hint at 35% of the text color, so the hint lives in `HintLabel`, not in the box.
- **Hints must fit.** Today's hints cut off with an ellipsis exactly where the example starts ("Type what you do and say, like..."). Keep a hint to about 40 characters at 18 pt in the 300-wide box, or move the example to the turn line.
- Key fields on `WBP_Keys` use the same style. They are masked, and their status word sits outside the box.

### Chat line (`WBP_ChatLine`)

- A 4-unit seat bar on the left, the full height of the entry.
- The name in `type.name` and its seat color. Then the action (if any) in `type.action`, `text.secondary`. Then the speech in `type.body`, `text.primary`.
- Gaps: name to action 4, action to speech 4, and 12 between entries.
- **My lines:** the name reads "You", in `seat.you`. The background is a `seat.you` tint at 8% over the panel. My lines also get a second cue besides color *(proposal)*: a 4-unit indent or a "you" bar on the right edge as well.
- **Typing line (T30):** "Meta is typing..." in `type.action`, `text.tertiary`, with the name in its seat color. The dots step every 0.4 s.
- A cut actor's later lines (if any) keep their seat color. Only the cast rows on the card turn gray.

### The reveal stamp (`StampFrame`)

- A tilted (about −8°) box with a thick double border (an outer 6-unit border, then a 4-unit gap, then a 2-unit inner border), text in `type.stamp`.
- HUMAN: fill `state.dangerFill`, text `text.primary`. AI: fill `state.ai`, text `text.onAccent`. Both say the word, so color is not the only cue.
- Always centered on the stage, drawn above every panel, never behind one (T27).

### Money burn (`WBP_MoneyBurn`, T35)

- Bottom right, 24 from the window edges (the same as the chat's margin), above `WBP_Stage`, not hit-testable and not focusable (T35).
- A tertiary item: it never covers the chat, the vote row, the input row or a robot's label, and nothing in it is text the player needs to read.

### Motion

| What | Time | Curve | Notes |
|---|---|---|---|
| Button hover and press | 0.08 s | linear | fill and border color |
| Focus ring | instant | | never animate focus |
| Chat line appears | 0.15 s | ease out | fade in plus an 8-unit rise |
| Typing dots (T30) | 0.4 s a step | step | |
| Line pacing (T30) | 1.2 s + 0.25 s a word, about 2 to 5 s | | T30's values; they go in a `pacing` data block |
| Panel shows or hides (card content, vote row) | 0.15 s in, 0.25 s out | ease out, ease in | |
| Banner (T29) | 0.25 s in (fade plus a 12-unit drop), 4.0 s hold, 0.4 s out | ease out, ease in | one at a time; the next waits |
| Reveal stamp | scales in from 3.2× in 0.25 s *(guess for the duration)*, holds 3.5 s, fades out over 1.0 s | ease out (a small overshoot fits the stamp) | 3.2×, 3.5 s and 1.0 s are from T14 |
| Robot bounce while talking | 2.6 s | | T17 |
| Money burn (T35) | about 1.4 s burn, then a fade | | T35 |
| Screen change (title to show, end screen in) | 0.3 s | ease in-out | fade through `bg.scrim` *(guess: today it is a cut)* |

Only one big moment moves at a time: the stamp, then the banner, then the next line.

### Contrast (WCAG 2.x)

Computed with a script in the session scratchpad (not in git). The method: WCAG relative luminance, and translucent panels blended in sRGB space over **pure white**, the worst case behind a floating panel *(guess: Slate blends UI in sRGB space; T32 confirms by measuring a screenshot)*. Text needs 4.5:1 or better. Buttons, borders, bars and the focus ring need 3:1 or better. Disabled controls are exempt under WCAG, but aim for 3:1.

`bg.panel` at 90% over white is #2B2C32. My line's tint over that is #313A3E. The banner at 92% over white is #27282D.

| Use | Foreground | Background | Ratio | Needs | |
|---|---|---|---|---|---|
| speech, body | `text.primary` #F5F6FA | `bg.panel` #14151B | 16.9 | 4.5 | ok |
| actions, premise | `text.secondary` #C4CAD9 | `bg.panel` #14151B | 11.1 | 4.5 | ok |
| labels, hint, cut names | `text.tertiary` #9EA4B2 | `bg.panel` #14151B | 7.3 | 4.5 | ok |
| turn line, my move | `accent.gold` #FFE7A3 | `bg.panel` #14151B | 14.9 | 4.5 | ok |
| danger text | `state.danger` #FF6B70 | `bg.panel` #14151B | 6.6 | 4.5 | ok |
| win text | `state.win` #6FDCA6 | `bg.panel` #14151B | 10.8 | 4.5 | ok |
| AI text | `state.ai` #F2A93B | `bg.panel` #14151B | 9.1 | 4.5 | ok |
| OpenAI name | `seat.openai` #D2E4FD | `bg.panel` #14151B | 14.1 | 4.5 | ok |
| Anthropic name | `seat.anthropic` #F3A96E | `bg.panel` #14151B | 9.3 | 4.5 | ok |
| SpaceXAI name | `seat.spacexai` #F8ED6D | `bg.panel` #14151B | 15.0 | 4.5 | ok |
| Meta name | `seat.meta` #78A4F9 | `bg.panel` #14151B | 7.4 | 4.5 | ok |
| You name | `seat.you` #79D6CD | `bg.panel` #14151B | 10.7 | 4.5 | ok |
| speech, body | `text.primary` | panel 90% over white #2B2C32 | 12.9 | 4.5 | ok |
| actions, premise | `text.secondary` | #2B2C32 | 8.5 | 4.5 | ok |
| labels, hint, cut names | `text.tertiary` | #2B2C32 | 5.6 | 4.5 | ok |
| turn line | `accent.gold` | #2B2C32 | 11.4 | 4.5 | ok |
| danger text | `state.danger` | #2B2C32 | 5.0 | 4.5 | ok |
| win text | `state.win` | #2B2C32 | 8.3 | 4.5 | ok |
| AI text | `state.ai` | #2B2C32 | 7.0 | 4.5 | ok |
| OpenAI name | `seat.openai` | #2B2C32 | 10.8 | 4.5 | ok |
| Anthropic name | `seat.anthropic` | #2B2C32 | 7.1 | 4.5 | ok |
| SpaceXAI name | `seat.spacexai` | #2B2C32 | 11.5 | 4.5 | ok |
| Meta name (the lowest seat) | `seat.meta` | #2B2C32 | 5.6 | 4.5 | ok |
| You name | `seat.you` | #2B2C32 | 8.2 | 4.5 | ok |
| my line: speech | `text.primary` | my tint over white #313A3E | 10.8 | 4.5 | ok |
| my line: action | `text.secondary` | #313A3E | 7.1 | 4.5 | ok |
| my line: small text | `text.tertiary` | #313A3E | 4.7 | 4.5 | ok |
| my line: name | `seat.you` | #313A3E | 6.8 | 4.5 | ok |
| end card text | `text.primary` | `bg.raised` #21232C | 14.5 | 4.5 | ok |
| end card reasons | `text.secondary` | `bg.raised` | 9.5 | 4.5 | ok |
| end card small text | `text.tertiary` | `bg.raised` | 6.3 | 4.5 | ok |
| end card gold | `accent.gold` | `bg.raised` | 12.8 | 4.5 | ok |
| end card names | OpenAI / Anthropic / SpaceXAI / Meta / You | `bg.raised` | 12.1 / 8.0 / 12.9 / 6.3 / 9.2 | 4.5 | ok |
| "voted You" | `state.danger` | `bg.raised` | 5.7 | 4.5 | ok |
| typed text | `text.primary` | `bg.inset` #0C0D12 | 18.0 | 4.5 | ok |
| input hint | `text.tertiary` | `bg.inset` | 7.8 | 4.5 | ok |
| disabled hint (exempt) | `text.disabled` #80848F | `bg.inset` | 5.2 | 3 | ok |
| director's note | `note.text` #FFF4D6 | `note.bg` #4A3A12 | 10.1 | 4.5 | ok |
| director's note title | `note.title` #FFD66B | `note.bg` | 7.9 | 4.5 | ok |
| banner text | `accent.gold` / `text.primary` | banner 92% over white #27282D | 12.1 / 13.6 | 4.5 | ok |
| primary label | `text.onAccent` #16130C | `accent.goldFill` / `goldHover` / `goldPressed` | 10.1 / 12.1 / 7.6 | 4.5 | ok |
| primary edge | `accent.goldFill` / `goldHover` / `goldPressed` | #2B2C32 | 7.6 / 9.0 / 5.7 | 3 | ok |
| secondary label | `text.primary` | `bg.raised` / `bg.hover` / `bg.pressed` | 14.5 / 12.3 / 16.1 | 4.5 | ok |
| secondary border | `line.border` #7A8091 | `bg.raised` / `bg.hover` / `bg.pressed` | 4.0 / 3.4 / 4.4 | 3 | ok |
| secondary border vs panel | `line.border` | #2B2C32 | 3.5 | 3 | ok |
| secondary hover border vs panel | `text.tertiary` | #2B2C32 | 5.6 | 3 | ok |
| picked vote label | `text.primary` | `state.dangerFill` / `dangerHover` / `dangerPressed` | 5.2 / 4.6 / 6.6 | 4.5 | ok |
| picked vote edge | `state.dangerFill` / `dangerHover` | `bg.panel` | 3.2 / 3.7 | 3 | ok |
| pressed vote border | `state.danger` | `bg.panel` | 6.6 | 3 | ok |
| disabled label (exempt) | `text.disabled` | `bg.disabled` #2A2C35 | 3.7 | 3 | ok |
| focus ring | `accent.focus` #5FD3C7 | #2B2C32 / `bg.inset` | 7.7 / 10.7 | 3 | ok |
| input border | `line.border` | `bg.inset` / #2B2C32 | 4.9 / 3.5 | 3 | ok |
| seat bar (Meta, the lowest) | `seat.meta` | #2B2C32 | 5.6 | 3 | ok |
| HUMAN stamp | `text.primary` | `state.dangerFill` | 5.2 | 4.5 | ok |
| AI stamp | `text.onAccent` | `state.ai` | 9.3 | 4.5 | ok |
| modal title | `accent.gold` | `bg.scrim` #0A0B0F | 16.1 | 4.5 | ok |
| modal body | `text.secondary` | `bg.scrim` | 12.0 | 4.5 | ok |
| text on velvet | `text.primary` | `deco.velvet` #7A1424 | 10.0 | 4.5 | ok |

Pairs that fail and are **not allowed**: `text.disabled` and `text.tertiary` for anything but small labels, and `state.danger` text on a panel below 90% opacity. A disabled fill is only 1.3:1 against the panel. That is allowed, because a disabled control is exempt, and the missing border is what marks it disabled.

**Today's screen, measured from the T27 screenshots** (blended pixels, so roughly ±0.3):

| Pair today | Foreground | Background | Ratio | Needs | |
|---|---|---|---|---|---|
| Send label | #FFFFFF | #6CB4C1 (teal) | 2.3 | 4.5 | FAIL |
| Pass label, enabled | #FFFFFF | #99A0BB | 2.6 | 4.5 | FAIL |
| Vote button label | #FFFFFF | #CB6F65 | 3.5 | 4.5 | FAIL |
| Disabled Send and Pass label | #ABABB0 | #65656E | 2.5 | 3 | FAIL |
| Pass enabled against Pass disabled | #99A0BB | #65656E | 2.2 | 3 | FAIL |
| Director's note title | #FCE69E | #7C6A36 | 4.3 | 4.5 | FAIL |
| Director's note text | #FEF8E7 | #7C6A35 | 5.0 | 4.5 | ok |
| Input hint (T27) | #8B8F97 | #1D1E24 | 5.1 | 4.5 | ok |
| Chat action | #C4CAD9 | #232329 | 9.5 | 4.5 | ok |
| Meta name | #78A4F9 | #232329 | 6.3 | 4.5 | ok |
| Robot label, white on the castle sky | #FFFFFF | #7F91B2 | 3.2 | 4.5 | FAIL |
| Robot label, white on a pale backdrop *(guess: a desert sun about #F2E6C8)* | #FFFFFF | #F2E6C8 | 1.2 | 4.5 | FAIL |

---

## 3. What T32 must check

### Values that are guesses

- **Font sizes not in Findings:** `PhaseHeader` (about 28), `TurnText` (about 20), the card's name (about 28) and role (about 22), the stamp, the title screen and the keys and unavailable screens. Read them from the widgets. The sizes that come from Findings are: chat speech 20, chat names and actions 18, card titles 18, vote labels 18, the hint 18, the end title 56, the end subline 22, and the old end body 17 (T10, before T14's cards).
- **The seat colors' exact values:** read `BP_Show.PersonaColor`. The table holds pixels sampled from screenshots.
- **Panel brush colors:** only the opacities (78, 75, 82%) and the input fill come from Findings. The panel colors were sampled after blending.
- **The DPI curve** (1080 = 1.0), and that a UMG point is 1/72 inch at 96 DPI.
- **Slate blends in sRGB space** (so the contrast numbers over white hold). Measure one panel over a bright spot in a screenshot to confirm.
- **`F_UI`'s faces** (is there a Black?) and whether Slate's font outline works on the composite font.
- **Button focus:** whether a UMG 5.8 `ButtonStyle` has a focused brush.
- **The stamp's scale-in time,** the screen-change fade, a Quit button on the title screen, and whether a vote can be changed after a pick.
- **Which title button is primary.** That is the user's call; this draft proposes Play via Relay.
- **What T28, T29, T35, T30 and T31 actually built:** where `EventBanner` sits (the top of the stage is crowded between the header, the card and the robot labels at about 30% of the height; the empty, dark house floor at the bottom center-right is the fallback), the Start button's style, the typing line, the suggestion row and the bill's size.

### Problems already seen in the T27 screenshots (candidate rows for "T32: UI audit")

These are from before T28 and T29, so some will be gone. Check each one again.

| Problem | Rule | Likely fix | Task |
|---|---|---|---|
| Send, Pass and vote labels fail contrast (2.3, 2.6, 3.5) | WCAG 1.4.3 | the button kinds above | T32 (shared styles), T34 |
| Enabled and disabled Pass look almost the same (2.2:1) | Nielsen: visibility of system status; WCAG 1.4.11 | bordered enabled buttons, flat disabled ones | T32, T34 |
| Pass shows disabled in phases that never allow it | hierarchy: hide what you can't use | hide Pass in scene turns and in the vote | T34 |
| Robot labels overlap when robots stand close ("You" over "SpaceXAI"), and a curtain hides part of a label at the right edge ("...AI") | legibility; no hidden information (T27's rule) | labels on a dark plate with a seat bar, or a screen-space label that is kept on screen and pushed apart | T34 |
| White robot labels on bright backdrops (3.2:1 or worse) | WCAG 1.4.3 | the label plate above, or a dark outline | T34 |
| The header repeats the phase in two lines ("THE SCENE: SCENE 1 OF 3, TURN 3 OF 3", then "Turn 3 of 3. YOUR MOVE...") | hierarchy, redundancy | the header: phase and count; the turn line: only what to do | T34 |
| The header's width changes from phase to phase | consistency | a fixed width | T34 |
| A half-cut line at the top of the chat looks like a bug ("mistake.") | Gestalt: closure; polish | a top fade on `LogScroll` | T34 |
| Card text cut at the bottom ("cockpit" in the vote shot), with a thin, faint scroll bar | Nielsen: visibility | a fade at the bottom, a visible scroll bar; T28 shortens the card in the scene | T28, T34 |
| The input hint is cut off where its example starts | Nielsen: help and documentation | shorter hints | T34 |
| The director's note box is a muddy olive, and its title fails contrast (4.3) | WCAG 1.4.3; theater look | `note.bg` #4A3A12 | T34 |
| OpenAI's pale blue name is close to white speech | hierarchy: who against what | keep the hue, keep the name Bold; check in grayscale | T34 |
| Game lines in the chat (gold on brown) | hierarchy | T29 moves them out | T29 |

### Screenshots to take, at 1600 × 900 and at 1280 × 720

For each, check: nothing clipped, overlapping or hidden; no text under 16 px at 720; one primary focus and one gold action; every panel 24 units from the edge; all five robots and their labels clear of the panels.

1. Title: idle, "Checking the AI relay...", and an error in `ModeNote`.
2. Keys: empty, partly filled (2 keys), testing, and an error.
3. Unavailable: a long relay message (4 lines), at the start and mid-show.
4. Scene Prep: the full card at its longest premise (find the longest card in `scenes.json`), a full cast of five, and the Start button.
5. Scene turn, mine: an empty box (the hint), a long typed line, and the focus ring.
6. Scene turn, the AIs' lines: the longest AI line (25 words plus a long action), the typing line (T30, if it is in), and the money burn (T35, with `burn_test`) with 6 bills at once.
7. Free Talk: my turn, and someone else's turn.
8. Vote: before a pick and after a pick, with four buttons and the longest names ("Anthropic", "SpaceXAI").
9. The reveal stamp: HUMAN and AI, and the stamp at its largest scale (frame 1).
10. A cut: the banner and the fallen robot.
11. The last reactions with See the results.
12. End screens: win, and lose with four cards, the longest provider name and the longest reasons.
13. **Every button kind in all five states** (enabled, hover, pressed, focused, disabled). T32's "Done when" needs four of them in screenshots.
14. Grayscale and deuteranopia versions of 4, 6, 8 and 12 (T34 and T33 run the script; T32 can spot-check).

### Contrast to measure from those screenshots

- Every text pair above, measured on the real pixels, over the brightest part of the stage behind each panel (the spotlit floor under the chat, the backdrop behind the header and the card).
- Every button's edge or border against the panel behind it, and the focus ring.
- The robot labels against each backdrop (castle, desert planet, ship deck, manor study, jungle park, Verona garden).
