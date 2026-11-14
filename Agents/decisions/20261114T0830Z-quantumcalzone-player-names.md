---
from: quantumcalzone
to: all
---

# The AIs read Player names; the human sees providers

Decided by my person on 2026-11-14, after a show put "Anthropic" on the human's robot. Built in T26 of `Docs/MVPPlan.md`.

- **Every provider gets its own AI seat, and the human takes one more seat with no persona.** A full show has 5 actors and 3 scenes. The human no longer borrows a persona, so no provider's AI ever sits out for them.
- **The AIs and the Director read "Player 1" to "Player 5"** (`SeatName` in `BP_Show`), in the cast, the log, options, votes and game messages. No provider name ever reaches them. If they read four provider names plus a fifth name, they would know who the human is.
- **The human's screen shows each AI's provider and "You"** (`SeatLabel`). AI text is shown through `DisplayText`, which swaps Player names for labels. Provider names the human types are turned back into Player names before the AIs read them.
- Persona ids (`worrier`) and the provider `name` fields in `personas.json` stay as they are. The human's seat id is `human`.
