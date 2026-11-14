# Outside assets (jam submission: list every one)

| Asset | Source | License | Where |
|---|---|---|---|
| Slackey-Regular.ttf (UI headers) | Google Fonts | SIL OFL 1.1 (`Art/Fonts/Slackey-LICENSE.txt`) | `Art/Fonts/`, imported to `/Game/UI/Fonts/FF_Slackey` |
| Englebert-Regular.ttf (UI body) | Google Fonts | SIL OFL 1.1 (`Art/Fonts/Englebert-OFL.txt`) | `Art/Fonts/`, imported to `/Game/UI/Fonts/FF_Englebert` |
| UE4 Mannequin mesh + Third Person animations (placeholder actors until generated characters replace them) | Epic Games, UE 5.8 `Templates/TemplateResources/Standard/Mannequin` | Epic Content License (free for use in UE projects) | `Content/Character/`, `Content/Animations/` |
| Character and prop concept art | Flux.1 schnell (fp8) run locally in ComfyUI via `Tools/ArtGen` | Apache-2.0 model; outputs owned by the user | `Art/Generated/` |
| 3D models (planned) | Meshy, Hyper3D Rodin, Tripo via ComfyUI partner nodes (`Tools/ArtGen`) | Per provider terms and plan | `Art/Generated/<set>/<item>/models/` |
| Voice lines (planned) | ElevenLabs (Voice Design + text to speech) via `Tools/VoiceGen`, text from `Tools/barks/DT_Barks.csv` | ElevenLabs plan terms | `Art/Voice/`, `/Game/Audio/VO/` |
