---
from: quantumcalzone
to: all
---

# New tasks T67 to T69 (analytics)

My person added analytics on 2026-11-15. `Docs/Plan.md` has the entries and `Docs/tasks/T67.md` to `T69.md` have the steps. This note is information; the plan is what counts.

- **T67** the relay takes events (`POST /event`) and `Tools/analytics_report.py` reports them. It needs no editor and touches neither `BP_Show` nor `WBP_Stage`, so it belongs to the non-chain machine. Its push deploys the relay, so it waits for my person's OK.
- **T68** the game sends its events from a new `BPC_Analytics`, with a SaveGame player id and a title-screen toggle. **T69** the input LLM names stage directions typed into the speech field, and the builder reports clicks on greyed-out actions. Both touch `BP_Show`, so they belong to the chain machine.
- They sit right after T66 and before T38, in that order. No other task's Depends on line changed.
- T68 adds a privacy line to `Docs/ItchPage.md`. T70 rewrites that page, so it should keep the line, or add it if T68 isn't done yet.
- T68 changes a rule in CLAUDE.md: Test for Free will send analytics events to the relay unless the new `analytics` switch is `off`. Until T68 lands, free mode still makes no network call.
