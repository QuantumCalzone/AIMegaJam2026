# Provider badges for the burning bill (T36 prep, steps 1 and 2)

Made on 2026-11-14 without the editor, for [T36](../tasks/T36.md). T36 moves the text below into `Docs/MoneyBurnArt.md` and `Docs/Assets.md` and then deletes this file.

## The badges are letters, not logos

T36 asked for each company's own logo. I read each company's brand rules first, and none of them allows this use as planned:

| Provider id | Company | Brand page (read on 2026-11-14) | What blocks it |
|---|---|---|---|
| `anthropic` | Anthropic | [Anthropic Trademark Guidelines](https://assets.claude.com/f7874b435aabdaee5f836e888b4439b9b56a934b.pdf) (effective Aug 1, 2024; linked from the [Legal Center](https://www.anthropic.com/legal)). The logo files are in the press kit on the [Newsroom](https://www.anthropic.com/news). | Use only "in materials we approve beforehand", and no change of color. |
| `openai` | OpenAI | [OpenAI Design Guidelines](https://openai.com/brand/) | No color added to the Blossom, the Blossom is not to be the primary branding, use the logo exactly as provided, and no use "without permission or outside OpenAI's terms". |
| `xai` | SpaceXAI (now SpaceXSI, see below) | [SpaceXSI Brand Guidelines](https://x.ai/legal/brand-guidelines) | Logos only "exactly as provided", "without any alteration or adjustment". |
| `meta` | Meta | [Meta brand resources and guidelines](https://www.meta.com/brand/resources/meta/company-brand/) (updated June 2026) | "All usage of the Meta logo requires approval" through a Meta counterpart; games are not in its list of uses. |

So no recolor is allowed by any of the four, and Anthropic and Meta need approval for any use at all. I asked, and my person chose **name badges** (2026-11-14): each badge shows the company's initial, drawn by us, so it uses no logo and needs no approval or download. Nothing was downloaded, so `Local/art/moneyburn/logos/` doesn't exist.

**SpaceXAI is now SpaceXSI.** x.ai's brand page is titled "SpaceXSI Brand Guidelines", and its footer says "SpaceX Super Intelligence LLC". News reports say Musk announced the rename on 2026-10-04 (for example [Not a Tesla App](https://www.notateslaapp.com/news/4770/musk-spacexai-will-be-renamed-spacexsi-dropping-ai)). The game still shows "SpaceXAI". The badge's "S" fits both names, so it doesn't change if the on-screen name does.

## Files

| File | What it is | Pixel size |
|---|---|---|
| `logo_anthropic.png` | "A" for Anthropic | 128 × 128 |
| `logo_openai.png` | "O" for OpenAI | 128 × 128 |
| `logo_xai.png` | "S" for SpaceXAI | 128 × 128 |
| `logo_meta.png` | "M" for Meta | 128 × 128 |

Each one is a filled circle in the medallion's color, #687D6C, that fills the square (its edge is antialiased; the corners are transparent). A thin ring in the bill's ink, #354942, sits just inside the edge, like the medallion's rim on `bill.png`. The initial is in the same ink, in Roboto Bold (the font of the engine's `Roboto`, which `F_UI` copies), with a cap height of half the badge (64 px), centered on its own outline. The four letters share one cap height, so they read as one set. The colors are the bill colors in `Docs/MoneyBurnArt.md`, "Colors".

The file names stay `logo_<id>.png`, as T36's later steps expect (`T_Logo_<id>`, `SetLogo`).

**Look check.** I put each badge on `bill.png` at its display size (bill 150 px wide, so the badge is about 39 px across) over `bg.scrim` #0A0B0F and over a dim warm floor. Each letter is clear at that size, and the four are easy to tell apart. The preview isn't kept.

## How to make the files again

Needs Windows PowerShell 5.1 (it ships with Windows; `System.Drawing` draws the files) and the engine's Roboto Bold. No download, no Python package. From the repo root:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File Local/art/moneyburn/make_badges.ps1 -UeRoot "E:/Epic Games/UE_5.8" -OutDir Docs/MoneyBurnArt
```

The script is in `Local/art/moneyburn/make_badges.ps1` on the Windows PC, which git ignores. Here it is in full:

```powershell
# Draws the four provider badges for T36: Docs/MoneyBurnArt/logo_<id>.png, 128 x 128.
# A filled medallion circle (#687D6C) with a thin engraved ring and the company's initial
# in the bill's ink (#354942), in the engine's Roboto Bold. Transparent outside the circle.
# No logo, no download: the companies' brand rules don't allow their logos here (see logos.md).
# Run in Windows PowerShell 5.1:
#   powershell -NoProfile -ExecutionPolicy Bypass -File Local/art/moneyburn/make_badges.ps1 -UeRoot "E:/Epic Games/UE_5.8" -OutDir Docs/MoneyBurnArt
param(
  [string]$UeRoot = "E:/Epic Games/UE_5.8",
  [string]$OutDir = "Docs/MoneyBurnArt",
  [int]$Size = 128
)
Add-Type -AssemblyName System.Drawing

$fontFile = Join-Path $UeRoot "Engine/Content/Slate/Fonts/Roboto-Bold.ttf"
$pfc = New-Object System.Drawing.Text.PrivateFontCollection
$pfc.AddFontFile($fontFile)
$family = $pfc.Families[0]

$medallion = [System.Drawing.ColorTranslator]::FromHtml("#687D6C")
$ink       = [System.Drawing.ColorTranslator]::FromHtml("#354942")

$badges = [ordered]@{ anthropic = "A"; openai = "O"; xai = "S"; meta = "M" }

$s = [double]$Size
$capHeight = 0.50 * $s     # every letter's cap height, so the four read as one set
$ringR     = 0.445 * $s    # radius of the engraved ring's center line
$ringW     = 0.025 * $s    # ring stroke width

foreach ($id in $badges.Keys) {
  $bmp = New-Object System.Drawing.Bitmap($Size, $Size, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
  $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
  $g.Clear([System.Drawing.Color]::Transparent)

  # Medallion: fills the square, edge antialiased, transparent outside.
  $brush = New-Object System.Drawing.SolidBrush($medallion)
  $g.FillEllipse($brush, 0.5, 0.5, $s - 1.0, $s - 1.0)

  # Engraved ring, like the medallion's rim on the bill.
  $pen = New-Object System.Drawing.Pen($ink, [single]$ringW)
  $c = $s / 2.0
  $g.DrawEllipse($pen, [single]($c - $ringR), [single]($c - $ringR), [single](2 * $ringR), [single](2 * $ringR))

  # The initial: a path at a size whose cap height is $capHeight, centered on its own bounds.
  $em = $capHeight / 0.711   # Roboto's cap height is 0.711 em
  $path = New-Object System.Drawing.Drawing2D.GraphicsPath
  $fmt = [System.Drawing.StringFormat]::GenericTypographic
  $path.AddString($badges[$id], $family, [int][System.Drawing.FontStyle]::Bold, [single]$em, (New-Object System.Drawing.PointF(0, 0)), $fmt)
  $b = $path.GetBounds()
  $m = New-Object System.Drawing.Drawing2D.Matrix
  $m.Translate([single]($c - $b.X - $b.Width / 2.0), [single]($c - $b.Y - $b.Height / 2.0))
  $path.Transform($m)
  $inkBrush = New-Object System.Drawing.SolidBrush($ink)
  $g.FillPath($inkBrush, $path)

  $out = Join-Path $OutDir ("logo_" + $id + ".png")
  $bmp.Save((Resolve-Path -LiteralPath $OutDir).Path + "\logo_" + $id + ".png", [System.Drawing.Imaging.ImageFormat]::Png)
  Write-Output ("wrote " + $out + "  letter " + $badges[$id] + "  bounds " + [math]::Round($b.Width,1) + " x " + [math]::Round($b.Height,1))
  $g.Dispose(); $bmp.Dispose(); $path.Dispose()
}
```

## For `Docs/MoneyBurnArt.md`

Add a row for each badge to "Files", and the section above ("How to make the files again", with the script) as a new section. A short version for the "Files" table:

| File | What it is | Pixel size | Source | License |
|---|---|---|---|---|
| `logo_anthropic.png`, `logo_openai.png`, `logo_xai.png`, `logo_meta.png` (T36) | The provider badges for the medallion: a medallion-colored circle with an ink ring and the company's initial (A, O, S, M) in Roboto Bold. Not the companies' logos, because their brand rules don't allow this use. Transparent outside the circle. | 128 × 128 each | Drawn by script (`make_badges.ps1`) | Ours, made during the jam |

## For `Docs/Assets.md` (under "Art", next to `T_Bill`)

These aren't trademarks any more, so the license column says "Ours", not the trademark line that T36 step 2 planned.

| Asset | What it is | Source | License |
|---|---|---|---|
| `Content/NHOS/UI/MoneyBurn/T_Logo_anthropic` (`logo_anthropic.png`) | The badge for a bill that paid Anthropic: the letter "A" in the bill's ink on the medallion color. Not Anthropic's logo. | Drawn by our script `make_badges.ps1` during the jam (2026-11-14), in the engine's Roboto Bold. No outside art, no AI image tool. | Ours, made during the jam. The letter is set in Roboto (Apache License 2.0, see "Fonts"). |
| `Content/NHOS/UI/MoneyBurn/T_Logo_openai` (`logo_openai.png`) | The badge for a bill that paid OpenAI: the letter "O". Not OpenAI's logo. | Drawn by `make_badges.ps1` during the jam (2026-11-14), in Roboto Bold. | Ours, made during the jam. Roboto: Apache License 2.0. |
| `Content/NHOS/UI/MoneyBurn/T_Logo_xai` (`logo_xai.png`) | The badge for a bill that paid SpaceXAI: the letter "S". Not the company's logo. | Drawn by `make_badges.ps1` during the jam (2026-11-14), in Roboto Bold. | Ours, made during the jam. Roboto: Apache License 2.0. |
| `Content/NHOS/UI/MoneyBurn/T_Logo_meta` (`logo_meta.png`) | The badge for a bill that paid Meta: the letter "M". Not Meta's logo. | Drawn by `make_badges.ps1` during the jam (2026-11-14), in Roboto Bold. | Ours, made during the jam. Roboto: Apache License 2.0. |

## For T36's own text

T36's task file and plan entry still say "logo". When T36 runs, its title, step 1 (find the logos, ask before each download), step 2's trademark line and the "Done when" check ("each of the four logos") should say "badge" (the company's initial) instead. Its plan entry's **Needs** no longer needs an OK for downloads. Steps 3 to 5 don't change.
