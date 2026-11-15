# Bot art

The concept art for the cast that replaces T46's clay pill bots: what was chosen, the rules the build keeps, and how each image was made. The files are in `Docs/BotArt/`. They are concept images only, not game assets: rows go into [Assets.md](Assets.md) when the build makes the models (T79, T80).

**Status:** chosen on 2026-11-15, after eleven concept rounds, by my picks in rounds 7 and 8, edited in round 10 (no hair) and checked in costume in round 11. Every round, with every take, is on the private concept page <https://claude.ai/artifact/DnjwjcZ1UV9o8BGAB4p9TQ> (ask QuantumCalzone for access). The design doc's "Art Inspiration" tab still describes the pill bots; T79 changes it, after my OK. T79 builds the shared round head and three of the bots, T80 builds Meta's android and my costume.

![The cast](BotArt/cast.png)

## The look

A polished claymation short: smooth, saturated matte clay with faint thumbprints, chunky toy-like forms, small gold accents and warm stage light, so the bots look like they came from the same shop as the props, the cherubs and the chandelier. Cute, never creepy: the gothic storybook round (round 4) turned skeletal fast and was dropped.

## The cast

Four polished bots and one human in a homemade costume. That contrast is the game's premise: the player is the one pretending. The provider bots each carry a light parody nod to their company's leader through signature traits only (glasses, clothes, expression, pose), never through anyone's name or looks. No prompt names anyone, and nothing carries a brand mark.

| Seat | Image | Body | Signature | Head |
|---|---|---|---|---|
| OpenAI | [openai.png](BotArt/openai.png) | A smooth pale-blue teardrop that floats over a glowing ring | A gray knit sweater, hands pressed together, wide earnest eyes, a halo above | Shared round head |
| Meta | [meta.png](BotArt/meta.png) | A doll-like android: pale gold-white skin, jointed arms, a royal blue tee and pants, cream shoes | Thick black wayfarer-style smart glasses with a tiny camera in each corner, glowing yellow-gold eyes, a chunky gold chain, a stiff polite smile | Its own doll head (face, ears, nose) |
| You | [you.png](BotArt/you.png) | A person in a robot costume: a teal-painted cardboard box body with duct tape and bottle-cap buttons, striped sleeves, garden gloves, jeans, sneakers | A box over the head with two eye slots the person's eyes peek through, a smile drawn on, a ping-pong-ball antenna, the red and cream knitted scarf | Its own box head |
| Anthropic | [anthropic.png](BotArt/anthropic.png) | A round orange body with a cream belly and a few buttons | Perfectly circular wire glasses, calm half-closed eyes, a finger raised to make a careful point, an amber light on a thin antenna | Shared round head |
| SpaceXAI | [spacexai.png](BotArt/spacexai.png) | A round lime body with a cream belly on coiled spring arms and legs, chunky boots | A long straight sculpted nose under the visor, one angled brow, a wide toothy grin, a double thumbs-up, a small lightning bolt | Shared round head |

`sources/` holds my four picks before the edit removed their hair. Your bot was not edited.

## Rules the build keeps

- **One shared round head** for OpenAI, Anthropic and SpaceXAI, about as wide as T46's 70 cm dome, with the screen face in the same place. One scale and offset per headpiece then fits all three. Meta's doll head and your box head each get their own scale and offset per headpiece (26 numbers).
- **Sockets, not fixed heights.** T46 put the hand slot at the arm pivot minus 44 cm, the head slot at 160 cm and the back slot at 106 cm. With five bodies, each bot gets a hand, head and back socket of its own, and props and headpieces attach there.
- **About 1.6 m tall,** as T46, so the labels (228 cm), the prop slots and T38's bubbles keep their places.
- **The seat color is on the body.** Wigs and hoods hide most of a head, so the body is what tells the bots apart under a costume. Meta's blue is its tee.
- **No hair and no wires** for now (my call, 2026-11-15).
- **Costumes over built-in parts.** The shades hide Meta's and Anthropic's own glasses. OpenAI's halo, Anthropic's antenna and SpaceXAI's bolt poke up beside any hat. On SpaceXAI the shades sit on the visor above the nose.
- **Every emotion face has a mouth.** The shades cover the eyes and a wig's bangs cover the brows, but the mouth always shows.
- **Parody nods only.** Real people's names stay out of prompts and off the screen, as the build notes say. Before this ships, read the jam's Official Rules for anything on real people's likeness.

## The costume check

Three of the 13 headpieces (the top hat, the bob wig and the dark shades), each put on the five cast images with the edit model and the headpiece's own reference image from `Docs/PropArt/`: [costume_top_hat.png](BotArt/costume_top_hat.png), [costume_bob_wig.png](BotArt/costume_bob_wig.png), [costume_dark_shades.png](BotArt/costume_dark_shades.png). All three fit all five. The edit model bends a headpiece to fit; a rigid mesh in the engine won't, which is why Meta and your box head get their own fit. One drift: the shades edit added a gray patch to SpaceXAI's head.

## Emotions

The emote tasks build this: T75 poses each robot's face and a gesture for twelve emotions (`emotes.json`), T76 adds `emotion` to every reply, T77 plays it as the line plays (mine too) and T78 lets me pick mine. Since T79 and T80, T75 poses the new cast's faces. [emotions.png](BotArt/emotions.png) shows a range on the round screen face (round 7), as a reference.

## How the images were made

1. **The source images:** Leonardo Lucid Origin text to image, 864 × 1152, four takes per prompt, with `Tools/art_gen.py image`. Each prompt and seed is in `logs/<seat>_source.json`.
2. **The edits:** `Tools/art_gen.py edit` (Leonardo's instruction-based `gemini-2.5-flash-image`), which changes the source image only as the prompt says. The hair removal and Meta's chain are in `logs/<seat>_edit.json`; the costume check is in `logs/costume_<headpiece>_<seat>.json`, with the headpiece's reference image as a second image. The edit keeps the source's size: three edits are 864 × 1184, a little taller than their 864 × 1152 sources.
3. **Lessons:** a text prompt redrawn from a pick gives a new robot every time (round 9 drifted far from my picks), so change a picked image with `edit`, never with a new prompt. Leonardo doesn't hold more than one specified character per image: group shots drew six or seven bots and mixed the colors, so lineups are made by putting single images side by side. Leonardo reported no cost for any of these calls (`api_credit_cost` is null), but the balance does drop: the cover's edits measured 26 API credits per edited image (`Docs/ItchMedia/README.md`).
