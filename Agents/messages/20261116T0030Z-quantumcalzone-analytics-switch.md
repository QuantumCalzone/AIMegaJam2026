---
from: quantumcalzone
to: all
date: 2026-11-16
---

# T68 is in: the analytics switch

T68 is in. The editor sends no analytics events unless `Local/switches.json` has `"analytics": "test"` (for checks). A packaged build sends real events: before you test one, put `{"analytics": "off"}` or `"test"` in its `Local/switches.json`, or add its id (the log's `NHOS: ANALYTICS player <id>`) to `ignore_players` in `Local/stats.json`.

Put `"analytics": "off"` in each machine's `Local/switches.json` (the PC's has it), so agents' test shows stay out of the data. An autoplay run sends only with `"test"`.
