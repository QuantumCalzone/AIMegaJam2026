# Money burn art (T35 prep)

The art that T35 (a bill burns in the bottom-right corner for every relay call) imports in its step 2. It was made on 2026-11-14 without the editor. The files are in `Local/art/moneyburn/`, which git ignores, so they exist only on the Mac that made them. T35 imports them under `Content/NHOS/UI/`, and then records them in `Docs/Assets.md` from this page.

The bill is drawn by a script, because Kenney's bundle has no banknote (see "Backups"). The flame and the ember are Kenney sprites (CC0 1.0), recolored by the same script into the palette of the T32 prep draft of `Docs/UIStyle.md` (commit `eb882ac`; the UI direction now lives in the design doc). I checked every image myself at about 120 px wide over `bg.scrim` and over a dim warm stage floor (`Local/art/moneyburn/preview.png`): the bill reads as a banknote, the char reads as burnt paper, and the flame reads as fire.

## Files

| File | What it is | Pixel size | Source | License |
|---|---|---|---|---|
| `bill.png` | The banknote: a muted sage bill with a double border, a robot head in a round medallion, two rosettes and "100" in each corner. No real currency's design, portrait or symbol. Transparent outside its rounded corners (2 px margin). | 256 × 128 (2:1, so it shows at 120 × 60) | Drawn by script (`makeart.swift`, below) | Ours, made during the jam |
| `bill_char.png` | The same bill, charred: near-black ash with a faint ghost of the design. Same size and outline as `bill.png`, so T35 can wipe from one to the other ("the bill blackens from one edge"). Optional. | 256 × 128 | Drawn by script, from `bill.png` | Ours, made during the jam |
| `flame_sheet.png` | The flame flipbook: one row of **8 frames, each 128 × 128**, frame 0 at the left. Each flame stands on a base 10 px above its frame's bottom edge, centered. Transparent background. Loops as a flicker at about 12 to 16 fps. | 1024 × 128 | Kenney **Particle Pack** (1.1): `2D assets/Particle Pack/PNG (Transparent)/muzzle_02.png`, `muzzle_03.png` and `muzzle_05.png` (white masks, 512 × 512), scaled, some mirrored and stretched, and tinted by `makeart.swift` | CC0 1.0 (the pack's `License.txt`) |
| `ember.png` | One soft ember: a gold core fading to orange. Use it small (6 to 10 px) for the rising embers. | 32 × 32 | Kenney **Particle Pack** (1.1): `2D assets/Particle Pack/PNG (Transparent)/circle_05.png`, scaled and tinted by `makeart.swift` | CC0 1.0 |
| `preview.png` | Not for import. A mock of the burn at display size, used for the look check. | 1100 × 560 | Made by a preview script from the files above | Ours |
| `makeart.swift` | Not for import. The script below, kept next to the art so it can be run again. | | | |
| `logo_anthropic.png`, `logo_openai.png`, `logo_xai.png`, `logo_meta.png` (T36) | The provider badges for the medallion: a medallion-colored circle with an ink ring and the company's initial (A, O, S, M) in Roboto Bold. Not the companies' logos, because their brand rules don't allow this use. Transparent outside the circle. Committed in `Docs/MoneyBurnArt/`; see "The provider badges (T36)" below. | 128 × 128 each | Drawn by script (`make_badges.ps1`) | Ours, made during the jam |

Frame order in `flame_sheet.png` (source, mirrored, vertical scale): 0 `muzzle_02` 1.00, 1 `muzzle_03` 0.96, 2 `muzzle_05` 1.04, 3 `muzzle_02` mirrored 0.92, 4 `muzzle_03` mirrored 1.06, 5 `muzzle_05` mirrored 0.95, 6 `muzzle_02` 1.08, 7 `muzzle_03` mirrored 0.98. The frames are not one drawn animation, so a fast loop flickers like fire, and a slow loop would look like shapes changing.

### Colors

All colors come from the T32 prep draft of `Docs/UIStyle.md` (commit `eb882ac`):

- **Flame:** a heat ramp from `state.dangerFill` #C42B2F (outer edge and tips) through `state.ai` #F2A93B, `accent.goldHover` #FFC857 and `accent.gold` #FFE7A3 to `note.text` #FFF4D6 (the hot core near the base). It is the only saturated part, as UIStyle asks.
- **Ember:** the same ramp, from orange at the rim to gold in the core.
- **Bill:** blends of `state.win` #6FDCA6, `note.text` and `accent.goldHover`, desaturated and dimmed so the bill stays tertiary and never brighter than the gold button: paper #889A83, medallion #687D6C, ink #354942, fine lines #637666.
- **Char:** `bg.scrim` #0A0B0F toward `note.bg` #4A3A12 and `text.disabled` #80848F, so it reads as ash, not as a brown panel.

## Licenses and sources

- **Kenney Particle Pack 1.1**, by Kenney (www.kenney.nl), from my copy of the bundle "Kenney Game Assets All-in-1 3.8.0.zip". Its `License.txt` says Creative Commons Zero (CC0), http://creativecommons.org/publicdomain/zero/1.0/. Credit is not required; the pack also credits Indigo Ray, Craig Nisbet, Zoltan Erdokovy, Heliagon, ThreeDee, Killst4r and Tim2501 for filter templates. For `Docs/Assets.md`: "Kenney, Particle Pack 1.1, `muzzle_02/03/05.png` and `circle_05.png`, recolored; CC0 1.0; https://kenney.nl/assets/particle-pack".
- **The bill and the char** were drawn by `makeart.swift` during the jam (2026-11-14). No outside art, no AI image tool, nothing downloaded.
- The bundle zip is in `~/Downloads` on this Mac, not in the repo root. It was unzipped (only the packs I looked at) into a scratch folder outside the repo. It is not staged and must never be.

## Backups

- **Flame:** Kenney **Smoke Particles**, `2D assets/Smoke Particles/PNG/Explosion/explosion00.png` to `explosion08.png` (CC0 1.0). That is already a 9-frame orange sequence, but it reads as a puff of fire, not a flame, and each frame is 583 × 536. Second backup: Particle Pack `flame_05.png` and `flame_06.png` (CC0), two clean single flame tongues, tinted with the same ramp; only 2 shapes, so they need mirroring to make 6 frames.
- **Ember:** Particle Pack `star_05.png` (a soft glow dot, CC0), or Kenney **Jumper Pack** `2D assets/Jumper Pack/PNG/Particles/portal_orangeParticle.png` (CC0, already orange, a pixel diamond, so it fits less well).
- **Bill:** the bundle has none. The closest Kenney sprites are **Emote Pack** `PNG/Vector/Style 1/emote_cash.png` and **Fish Pack** `PNG/Double/hud_dollar.png`, but both are a "$" sign (a real currency's symbol) and not a bill, so I didn't use them. The backup is the same script with the paper in the note colors: change `paper` to `note.text` #FFF4D6 dimmed and `ink` to `note.bg` #4A3A12. That reads more like a theater ticket than money.

## LFS

`.gitattributes` already sends `*.png` (and `*.uasset`) to LFS, so T35 needs no new rule. `makeart.swift` stays in `Local/` and is not imported; if a `.swift` file is ever committed, it is text and needs no LFS rule.

## How to make the files again

Needs a Mac with the Swift compiler (Xcode or the command line tools); no Python packages. Unzip only the Particle Pack from the bundle into an empty folder, then:

```bash
swiftc -O Local/art/moneyburn/makeart.swift -o /tmp/makeart && /tmp/makeart "<unzip folder>/2D assets/Particle Pack/PNG (Transparent)" Local/art/moneyburn
```

### `makeart.swift`

```swift
// makeart.swift: builds the T35 money-burn art.
// Usage: swift makeart.swift <particlePackTransparentDir> <outDir>
// Writes bill.png (drawn here), bill_char.png (bill.png darkened), flame_sheet.png
// (Kenney Particle Pack muzzle_*.png tinted into 8 flame frames) and ember.png
// (Kenney Particle Pack circle_05.png tinted). Colors come from the eb882ac draft of Docs/UIStyle.md.
import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
let srcDir = args[1], outDir = args[2]
let cs = CGColorSpace(name: CGColorSpace.sRGB)!

struct RGB { var r, g, b: Double }
func hex(_ s: String) -> RGB {
  let v = Int(s.dropFirst(), radix: 16)!
  return RGB(r: Double((v >> 16) & 255) / 255, g: Double((v >> 8) & 255) / 255, b: Double(v & 255) / 255)
}
func mix(_ a: RGB, _ b: RGB, _ t: Double) -> RGB { RGB(r: a.r + (b.r - a.r) * t, g: a.g + (b.g - a.g) * t, b: a.b + (b.b - a.b) * t) }
func cg(_ c: RGB, _ a: Double = 1) -> CGColor { CGColor(colorSpace: cs, components: [c.r, c.g, c.b, a])! }

// Palette entries of the eb882ac UIStyle.md draft used here.
let noteText = hex("#FFF4D6"), noteBg = hex("#4A3A12"), gold = hex("#FFE7A3"), goldHover = hex("#FFC857")
let stateAi = hex("#F2A93B"), dangerFill = hex("#C42B2F"), win = hex("#6FDCA6"), panel = hex("#14151B")
let scrim = hex("#0A0B0F")

func newCtx(_ w: Int, _ h: Int) -> CGContext {
  CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: cs,
            bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
}
func save(_ img: CGImage, _ name: String) {
  let url = URL(fileURLWithPath: outDir).appendingPathComponent(name)
  let d = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil)!
  CGImageDestinationAddImage(d, img, nil); CGImageDestinationFinalize(d)
}
func load(_ path: String) -> CGImage {
  let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil)!
  return CGImageSourceCreateImageAtIndex(src, 0, nil)!
}
// Alpha channel of an image drawn into w x h, row 0 = top.
func alphaOf(_ ctx: CGContext) -> [Double] {
  let w = ctx.width, h = ctx.height, p = ctx.data!.bindMemory(to: UInt8.self, capacity: w * h * 4)
  var a = [Double](repeating: 0, count: w * h)
  for i in 0..<(w * h) { a[i] = Double(p[i * 4 + 3]) / 255 }
  return a
}
func boxBlur(_ a: [Double], _ w: Int, _ h: Int, _ r: Int, passes: Int = 3) -> [Double] {
  var cur = a
  for _ in 0..<passes {
    var tmp = [Double](repeating: 0, count: w * h)
    for y in 0..<h { for x in 0..<w { var s = 0.0
      for k in -r...r { s += cur[y * w + min(max(x + k, 0), w - 1)] }
      tmp[y * w + x] = s / Double(2 * r + 1) } }
    for y in 0..<h { for x in 0..<w { var s = 0.0
      for k in -r...r { s += tmp[min(max(y + k, 0), h - 1) * w + x] }
      cur[y * w + x] = s / Double(2 * r + 1) } }
  }
  return cur
}
// Writes color + alpha (straight) into a premultiplied context.
func put(_ ctx: CGContext, _ x: Int, _ y: Int, _ c: RGB, _ a: Double) {
  let p = ctx.data!.bindMemory(to: UInt8.self, capacity: ctx.width * ctx.height * 4)
  let i = (y * ctx.width + x) * 4, aa = min(max(a, 0), 1)
  p[i] = UInt8(min(max(c.r, 0), 1) * aa * 255 + 0.5); p[i + 1] = UInt8(min(max(c.g, 0), 1) * aa * 255 + 0.5)
  p[i + 2] = UInt8(min(max(c.b, 0), 1) * aa * 255 + 0.5); p[i + 3] = UInt8(aa * 255 + 0.5)
}
// Fire ramp by heat 0..1: dangerFill -> stateAi -> goldHover -> gold -> noteText.
func fire(_ t: Double) -> RGB {
  let stops: [(Double, RGB)] = [(0, dangerFill), (0.3, stateAi), (0.55, goldHover), (0.8, gold), (1, noteText)]
  let tt = min(max(t, 0), 1)
  for i in 1..<stops.count where tt <= stops[i].0 {
    return mix(stops[i - 1].1, stops[i].1, (tt - stops[i - 1].0) / (stops[i].0 - stops[i - 1].0))
  }
  return noteText
}

// ---------- flame_sheet.png ----------
let F = 128, frameCount = 8
// (source file, mirrored, vertical scale) per frame, ordered for a flicker loop.
let frames: [(String, Bool, Double)] = [
  ("muzzle_02.png", false, 1.00), ("muzzle_03.png", false, 0.96), ("muzzle_05.png", false, 1.04),
  ("muzzle_02.png", true, 0.92), ("muzzle_03.png", true, 1.06), ("muzzle_05.png", true, 0.95),
  ("muzzle_02.png", false, 1.08), ("muzzle_03.png", true, 0.98)]
// Union of the alpha bounds of the sources, in 512 px source space.
var minX = 512, minY = 512, maxX = 0, maxY = 0
var bottomOf: [String: Int] = [:]
for name in Set(frames.map { $0.0 }) {
  let c = newCtx(512, 512); c.draw(load(srcDir + "/" + name), in: CGRect(x: 0, y: 0, width: 512, height: 512))
  let a = alphaOf(c)
  var own = 0
  for y in 0..<512 { for x in 0..<512 where a[y * 512 + x] > 0.15 {
    minX = min(minX, x); maxX = max(maxX, x); minY = min(minY, y); maxY = max(maxY, y)
    if a[y * 512 + x] > 0.6 { own = max(own, y) } } }
  bottomOf[name] = own
}
// Mirroring needs symmetric bounds around the center.
let halfW = max(256 - minX, maxX - 256)
let boxW = Double(2 * halfW), boxH = Double(maxY - minY + 1)
let fit = min(Double(F - 8) / boxW, Double(F - 10) / (boxH * 1.08))
let sheet = newCtx(F * frameCount, F)
for (i, fr) in frames.enumerated() {
  let m = newCtx(F, F)
  m.interpolationQuality = .high
  let sx = fit, sy = fit * fr.2
  // Source rows minY...maxY map so the flame base sits 10 px above the frame bottom (CG origin is bottom-left).
  let baseY = 10.0, srcBottomFromBottom = Double(512 - 1 - bottomOf[fr.0]!)
  m.translateBy(x: Double(F) / 2, y: baseY - srcBottomFromBottom * sy)
  if fr.1 { m.scaleBy(x: -1, y: 1) }
  m.draw(load(srcDir + "/" + fr.0), in: CGRect(x: -256 * sx, y: 0, width: 512 * sx, height: 512 * sy))
  let a = alphaOf(m)
  let b = boxBlur(a, F, F, 6)
  let fc = newCtx(F, F)
  for y in 0..<F { for x in 0..<F {
    let al = a[y * F + x]; if al <= 0 { continue }
    let up = 1 - Double(y) / Double(F - 1) // row 0 is the top here: up = 1 at top
    let bb = min(1, b[y * F + x] * 1.1)
    let heat = 0.9 * pow(bb, 2.4) * (1 - 0.65 * up) + 0.05
    put(fc, x, y, fire(heat), al)
  } }
  sheet.draw(fc.makeImage()!, in: CGRect(x: i * F, y: 0, width: F, height: F))
}
save(sheet.makeImage()!, "flame_sheet.png")

// ---------- ember.png ----------
let E = 32
let ec = newCtx(E, E); ec.interpolationQuality = .high
let circ = load(srcDir + "/circle_05.png")
// circle_05 is a soft disc in the middle of a 512 canvas; scale so the disc fills the ember.
ec.draw(circ, in: CGRect(x: -Double(E) * 0.62, y: -Double(E) * 0.62, width: Double(E) * 2.24, height: Double(E) * 2.24))
let ea = alphaOf(ec)
let eo = newCtx(E, E)
for y in 0..<E { for x in 0..<E { let al = ea[y * E + x]; if al <= 0 { continue }
  put(eo, x, y, fire(0.2 + 0.6 * al), min(1, al * 1.1)) } }
save(eo.makeImage()!, "ember.png")

// ---------- bill.png (drawn, no real currency's design) ----------
let BW = 256, BH = 128
// Muted bill colors blended from the palette: state.win toward note.text and bg.panel, then desaturated.
func desat(_ c: RGB, _ t: Double) -> RGB { let l = 0.3 * c.r + 0.59 * c.g + 0.11 * c.b; return mix(c, RGB(r: l, g: l, b: l), t) }
func dim(_ c: RGB, _ k: Double) -> RGB { RGB(r: c.r * k, g: c.g * k, b: c.b * k) }
let sage = mix(mix(win, noteText, 0.35), goldHover, 0.18)
let paper = dim(desat(sage, 0.45), 0.72)
let paperDark = dim(desat(mix(sage, win, 0.4), 0.5), 0.6)
let ink = desat(mix(win, panel, 0.72), 0.35)
let inkSoft = mix(ink, paper, 0.55)
func drawBill(_ c: CGContext) {
  let r = CGRect(x: 2, y: 2, width: BW - 4, height: BH - 4)
  c.setFillColor(cg(paper)); c.addPath(CGPath(roundedRect: r, cornerWidth: 6, cornerHeight: 6, transform: nil)); c.fillPath()
  // Fine wavy lines as paper texture.
  c.saveGState()
  c.addPath(CGPath(roundedRect: r, cornerWidth: 6, cornerHeight: 6, transform: nil)); c.clip()
  c.setStrokeColor(cg(paperDark, 0.55)); c.setLineWidth(1)
  for k in stride(from: -10.0, to: Double(BH) + 10, by: 7) {
    c.move(to: CGPoint(x: 0, y: k))
    for x in stride(from: 0.0, through: Double(BW), by: 4) { c.addLine(to: CGPoint(x: x, y: k + 2.2 * sin(x / 13 + k / 9))) }
    c.strokePath()
  }
  c.restoreGState()
  // Outer and inner borders.
  c.setStrokeColor(cg(ink)); c.setLineWidth(4)
  c.addPath(CGPath(roundedRect: r.insetBy(dx: 7, dy: 7), cornerWidth: 4, cornerHeight: 4, transform: nil)); c.strokePath()
  c.setLineWidth(1.5); c.setStrokeColor(cg(inkSoft))
  c.addPath(CGPath(roundedRect: r.insetBy(dx: 13, dy: 13), cornerWidth: 3, cornerHeight: 3, transform: nil)); c.strokePath()
  // Center medallion: an oval with a robot head (the game's cast), not a portrait.
  let cx = Double(BW) / 2, cy = Double(BH) / 2
  let oval = CGRect(x: cx - 38, y: cy - 38, width: 76, height: 76)
  c.setFillColor(cg(paperDark)); c.fillEllipse(in: oval)
  c.setStrokeColor(cg(ink)); c.setLineWidth(3); c.strokeEllipse(in: oval)
  c.setLineWidth(1.2); c.setStrokeColor(cg(inkSoft)); c.strokeEllipse(in: oval.insetBy(dx: 5, dy: 5))
  c.setFillColor(cg(ink))
  let head = CGRect(x: cx - 18, y: cy - 16, width: 36, height: 28)
  c.addPath(CGPath(roundedRect: head, cornerWidth: 7, cornerHeight: 7, transform: nil)); c.fillPath()
  c.fill(CGRect(x: cx - 1.5, y: cy + 12, width: 3, height: 9))     // antenna
  c.fillEllipse(in: CGRect(x: cx - 4, y: cy + 19, width: 8, height: 8))
  c.fill(CGRect(x: cx - 22, y: cy - 7, width: 4, height: 10))      // ears
  c.fill(CGRect(x: cx + 18, y: cy - 7, width: 4, height: 10))
  c.setFillColor(cg(paper))
  c.fillEllipse(in: CGRect(x: cx - 11, y: cy - 4, width: 8, height: 8)) // eyes
  c.fillEllipse(in: CGRect(x: cx + 3, y: cy - 4, width: 8, height: 8))
  c.fill(CGRect(x: cx - 8, y: cy - 11, width: 16, height: 3))           // mouth
  // Side rosettes.
  for sx in [-1.0, 1.0] {
    let px = cx + sx * 74
    c.setStrokeColor(cg(inkSoft)); c.setLineWidth(1.2)
    for k in 0..<3 { c.strokeEllipse(in: CGRect(x: px - 16 + Double(k) * 4, y: cy - 16 + Double(k) * 4, width: 32 - Double(k) * 8, height: 32 - Double(k) * 8)) }
    c.setFillColor(cg(ink)); c.fillEllipse(in: CGRect(x: px - 3, y: cy - 3, width: 6, height: 6))
  }
  // Corner numerals: plain digits, no currency symbol.
  let font = CTFontCreateWithName("Helvetica-Bold" as CFString, 17, nil)
  for (x, y) in [(20.0, 92.0), (Double(BW) - 50, 92.0), (20.0, 20.0), (Double(BW) - 50, 20.0)] {
    let s = NSAttributedString(string: "100", attributes: [kCTFontAttributeName as NSAttributedString.Key: font,
                                                            kCTForegroundColorAttributeName as NSAttributedString.Key: cg(ink)])
    let line = CTLineCreateWithAttributedString(s)
    c.textPosition = CGPoint(x: x, y: y); CTLineDraw(line, c)
  }
}
let bc = newCtx(BW, BH); bc.interpolationQuality = .high; drawBill(bc)
let billImg = bc.makeImage()!
save(billImg, "bill.png")

// ---------- bill_char.png: same shape, charred, for the "blackens from one edge" wipe ----------
let cc = newCtx(BW, BH); cc.draw(billImg, in: CGRect(x: 0, y: 0, width: BW, height: BH))
let cp = cc.data!.bindMemory(to: UInt8.self, capacity: BW * BH * 4)
let charDark = mix(scrim, noteBg, 0.12), charLight = mix(mix(scrim, hex("#80848F"), 0.38), noteBg, 0.15)
for i in 0..<(BW * BH) {
  let a = Double(cp[i * 4 + 3]) / 255; if a <= 0 { continue }
  let l = (0.3 * Double(cp[i * 4]) + 0.59 * Double(cp[i * 4 + 1]) + 0.11 * Double(cp[i * 4 + 2])) / 255 / a
  let x = i % BW, y = i / BW
  let n = 0.5 + 0.5 * sin(Double(x) * 0.37 + sin(Double(y) * 0.21) * 3) * cos(Double(y) * 0.29 + Double(x) * 0.05)
  let c = mix(charDark, charLight, min(1, l * l * 0.9 + n * 0.22))
  put(cc, x, y, c, a)
}
save(cc.makeImage()!, "bill_char.png")
print("ok")
```

## The provider badges (T36)

Made on 2026-11-14 without the editor, as T36's prep (steps 1 and 2), and imported by T36 as `Content/NHOS/UI/MoneyBurn/T_Logo_<id>` (UI texture group, no mipmaps, `TC_EditorIcon`, like `T_Bill`). They are committed in `Docs/MoneyBurnArt/` (`logo_anthropic.png`, `logo_openai.png`, `logo_xai.png`, `logo_meta.png`). Each bill shows the badge of the provider its reply was paid to, over the robot head in the medallion.

### The badges are letters, not logos

T36 asked for each company's own logo. I read each company's brand rules first, and none of them allows this use as planned:

| Provider id | Company | Brand page (read on 2026-11-14) | What blocks it |
|---|---|---|---|
| `anthropic` | Anthropic | [Anthropic Trademark Guidelines](https://assets.claude.com/f7874b435aabdaee5f836e888b4439b9b56a934b.pdf) (effective Aug 1, 2024; linked from the [Legal Center](https://www.anthropic.com/legal)). The logo files are in the press kit on the [Newsroom](https://www.anthropic.com/news). | Use only "in materials we approve beforehand", and no change of color. |
| `openai` | OpenAI | [OpenAI Design Guidelines](https://openai.com/brand/) | No color added to the Blossom, the Blossom is not to be the primary branding, use the logo exactly as provided, and no use "without permission or outside OpenAI's terms". |
| `xai` | SpaceXAI (now SpaceXSI, see below) | [SpaceXSI Brand Guidelines](https://x.ai/legal/brand-guidelines) | Logos only "exactly as provided", "without any alteration or adjustment". |
| `meta` | Meta | [Meta brand resources and guidelines](https://www.meta.com/brand/resources/meta/company-brand/) (updated June 2026) | "All usage of the Meta logo requires approval" through a Meta counterpart; games are not in its list of uses. |

So no recolor is allowed by any of the four, and Anthropic and Meta need approval for any use at all. I asked, and my person chose **name badges** (2026-11-14): each badge shows the company's initial, drawn by us, so it uses no logo and needs no approval or download. Nothing was downloaded, so `Local/art/moneyburn/logos/` doesn't exist.

**SpaceXAI is now SpaceXSI.** x.ai's brand page is titled "SpaceXSI Brand Guidelines", and its footer says "SpaceX Super Intelligence LLC". News reports say Musk announced the rename on 2026-10-04 (for example [Not a Tesla App](https://www.notateslaapp.com/news/4770/musk-spacexai-will-be-renamed-spacexsi-dropping-ai)). The game still shows "SpaceXAI". The badge's "S" fits both names, so it doesn't change if the on-screen name does.

### Files

| File | What it is | Pixel size |
|---|---|---|
| `logo_anthropic.png` | "A" for Anthropic | 128 × 128 |
| `logo_openai.png` | "O" for OpenAI | 128 × 128 |
| `logo_xai.png` | "S" for SpaceXAI | 128 × 128 |
| `logo_meta.png` | "M" for Meta | 128 × 128 |

Each one is a filled circle in the medallion's color, #687D6C, that fills the square (its edge is antialiased; the corners are transparent). A thin ring in the bill's ink, #354942, sits just inside the edge, like the medallion's rim on `bill.png`. The initial is in the same ink, in Roboto Bold (the font of the engine's `Roboto`, which `F_UI` copies), with a cap height of half the badge (64 px), centered on its own outline. The four letters share one cap height, so they read as one set. The colors are the bill colors in `Docs/MoneyBurnArt.md`, "Colors".

The file names stay `logo_<id>.png`, as T36's later steps expect (`T_Logo_<id>`, `SetLogo`).

**Look check.** I put each badge on `bill.png` at its display size (bill 150 px wide, so the badge is about 39 px across) over `bg.scrim` #0A0B0F and over a dim warm floor. Each letter is clear at that size, and the four are easy to tell apart. The preview isn't kept.

### How to make the files again

Needs Windows PowerShell 5.1 (it ships with Windows; `System.Drawing` draws the files) and the engine's Roboto Bold. No download, no Python package. From the repo root:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File Local/art/moneyburn/make_badges.ps1 -UeRoot "E:/Epic Games/UE_5.8" -OutDir Docs/MoneyBurnArt
```

The script is in `Local/art/moneyburn/make_badges.ps1` on the Windows PC, which git ignores. Here it is in full:

```powershell
# Draws the four provider badges for T36: Docs/MoneyBurnArt/logo_<id>.png, 128 x 128.
# A filled medallion circle (#687D6C) with a thin engraved ring and the company's initial
# in the bill's ink (#354942), in the engine's Roboto Bold. Transparent outside the circle.
# No logo, no download: the companies' brand rules don't allow their logos here (see Docs/MoneyBurnArt.md).
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
