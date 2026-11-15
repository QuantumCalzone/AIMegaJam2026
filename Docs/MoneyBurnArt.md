# Money burn art (T35 prep)

The art that T35 (a bill burns in the bottom-right corner for every relay call) imports in its step 2. It was made on 2026-11-14 without the editor. The files are in `Local/art/moneyburn/`, which git ignores, so they exist only on the Mac that made them. T35 imports them under `Content/NHOS/UI/`, and then records them in `Docs/Assets.md` from this page.

The bill is drawn by a script, because Kenney's bundle has no banknote (see "Backups"). The flame and the ember are Kenney sprites (CC0 1.0), recolored by the same script into the palette in `Docs/UIStyle.md`. I checked every image myself at about 120 px wide over `bg.scrim` and over a dim warm stage floor (`Local/art/moneyburn/preview.png`): the bill reads as a banknote, the char reads as burnt paper, and the flame reads as fire.

## Files

| File | What it is | Pixel size | Source | License |
|---|---|---|---|---|
| `bill.png` | The banknote: a muted sage bill with a double border, a robot head in a round medallion, two rosettes and "100" in each corner. No real currency's design, portrait or symbol. Transparent outside its rounded corners (2 px margin). | 256 × 128 (2:1, so it shows at 120 × 60) | Drawn by script (`makeart.swift`, below) | Ours, made during the jam |
| `bill_char.png` | The same bill, charred: near-black ash with a faint ghost of the design. Same size and outline as `bill.png`, so T35 can wipe from one to the other ("the bill blackens from one edge"). Optional. | 256 × 128 | Drawn by script, from `bill.png` | Ours, made during the jam |
| `flame_sheet.png` | The flame flipbook: one row of **8 frames, each 128 × 128**, frame 0 at the left. Each flame stands on a base 10 px above its frame's bottom edge, centered. Transparent background. Loops as a flicker at about 12 to 16 fps. | 1024 × 128 | Kenney **Particle Pack** (1.1): `2D assets/Particle Pack/PNG (Transparent)/muzzle_02.png`, `muzzle_03.png` and `muzzle_05.png` (white masks, 512 × 512), scaled, some mirrored and stretched, and tinted by `makeart.swift` | CC0 1.0 (the pack's `License.txt`) |
| `ember.png` | One soft ember: a gold core fading to orange. Use it small (6 to 10 px) for the rising embers. | 32 × 32 | Kenney **Particle Pack** (1.1): `2D assets/Particle Pack/PNG (Transparent)/circle_05.png`, scaled and tinted by `makeart.swift` | CC0 1.0 |
| `preview.png` | Not for import. A mock of the burn at display size, used for the look check. | 1100 × 560 | Made by a preview script from the files above | Ours |
| `makeart.swift` | Not for import. The script below, kept next to the art so it can be run again. | | | |

Frame order in `flame_sheet.png` (source, mirrored, vertical scale): 0 `muzzle_02` 1.00, 1 `muzzle_03` 0.96, 2 `muzzle_05` 1.04, 3 `muzzle_02` mirrored 0.92, 4 `muzzle_03` mirrored 1.06, 5 `muzzle_05` mirrored 0.95, 6 `muzzle_02` 1.08, 7 `muzzle_03` mirrored 0.98. The frames are not one drawn animation, so a fast loop flickers like fire, and a slow loop would look like shapes changing.

### Colors

All colors come from `Docs/UIStyle.md`:

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
// (Kenney Particle Pack circle_05.png tinted). Colors come from Docs/UIStyle.md.
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

// UIStyle.md palette entries used here.
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
