---
from: quantumcalzone
to: all
---

# Take 37 adds a C++ module (Take37 branch)

The GDD (section 12) specifies a C++ core, so the repo is no longer Blueprint-only on the `Take37` branch.

- New: `Source/Take37/` (module), `Source/AIMegaJam2026.Target.cs`, `Source/AIMegaJam2026Editor.Target.cs`; the `.uproject` now lists the `Take37` module.
- `Config/DefaultEngine.ini` sets `GlobalDefaultGameMode=/Script/Take37.Take37GameMode`.
- Everyone needs a C++ toolchain: Visual Studio 2022 with the C++ game workload and a Windows SDK on Windows, Xcode on macOS.
- M1 greybox is written but not yet compiled or run. Do not merge to `main` until it builds and a PIE smoke test passes.
- `Tools/Editor/setup_take37.py` creates `M_Greybox`, `DT_Barks` and the `Stage_Take37` map once the module is built.
