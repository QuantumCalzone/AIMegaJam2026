// mb.swift (T99): makes the money burn's textures from the picked Leonardo images, with no outside art.
//   mb bill   SRC.png OUT.png FONT.ttf x0 y0 axis y1 rx ry   the bill, its left half mirrored about the medallion, 256x128, "100" on the rosettes
//   mb char   BILL.png OUT.png                the same bill charred to ash (same outline)
//   mb flames SRC.png SHEET.png EMBER.png     8 flames keyed off the dark background into one row of 128x128 frames; the ember from a tip
//   mb badge  BILLSRC.png OUT.png FONT.ttf HEX LETTER    a 128x128 clay disc in HEX with the letter pressed in
import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

struct Img { var w: Int; var h: Int; var p: [Float]   // RGBA, straight alpha, 0...1, row 0 = top
  init(_ w: Int, _ h: Int) { self.w = w; self.h = h; p = [Float](repeating: 0, count: w * h * 4) }
  func px(_ x: Int, _ y: Int) -> (Float, Float, Float, Float) { let i = (y * w + x) * 4; return (p[i], p[i+1], p[i+2], p[i+3]) }
  mutating func set(_ x: Int, _ y: Int, _ c: (Float, Float, Float, Float)) { let i = (y * w + x) * 4; p[i] = c.0; p[i+1] = c.1; p[i+2] = c.2; p[i+3] = c.3 }
}
let cs = CGColorSpace(name: CGColorSpace.sRGB)!
func ctx(_ w: Int, _ h: Int) -> CGContext { CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)! }
func fromCtx(_ c: CGContext) -> Img {
  var o = Img(c.width, c.height); let d = c.data!.bindMemory(to: UInt8.self, capacity: c.width * c.height * 4)
  for i in 0..<(c.width * c.height) { let a = Float(d[i*4+3]) / 255
    for k in 0..<3 { o.p[i*4+k] = a > 0 ? min(1, Float(d[i*4+k]) / 255 / a) : 0 }; o.p[i*4+3] = a }
  return o
}
func cg(_ m: Img) -> CGImage { let c = ctx(m.w, m.h); let d = c.data!.bindMemory(to: UInt8.self, capacity: m.w * m.h * 4)
  for i in 0..<(m.w * m.h) { let a = max(0, min(1, m.p[i*4+3]))
    for k in 0..<3 { d[i*4+k] = UInt8(max(0, min(1, m.p[i*4+k])) * a * 255 + 0.5) }; d[i*4+3] = UInt8(a * 255 + 0.5) }
  return c.makeImage()! }
func load(_ path: String) -> Img { let im = CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil)!, 0, nil)!
  let c = ctx(im.width, im.height); c.draw(im, in: CGRect(x: 0, y: 0, width: im.width, height: im.height)); return fromCtx(c) }
func save(_ m: Img, _ path: String) { let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
  CGImageDestinationAddImage(d, cg(m), nil); CGImageDestinationFinalize(d) }
// Crops (x0,y0,w,h in top-left pixels) and scales into a w2 x h2 image placed at (ox,oy) on a canvas cw x ch. flip mirrors it.
func place(_ m: Img, crop: CGRect, into cw: Int, _ ch: Int, at r: CGRect, flip: Bool = false) -> Img {
  let c = ctx(cw, ch); c.interpolationQuality = .high
  let sub = cg(m).cropping(to: crop)!
  // CG draws with y up: convert the top-left rect r to bottom-left.
  var dr = CGRect(x: r.minX, y: CGFloat(ch) - r.maxY, width: r.width, height: r.height)
  if flip { c.translateBy(x: CGFloat(cw), y: 0); c.scaleBy(x: -1, y: 1); dr.origin.x = CGFloat(cw) - r.maxX }
  c.draw(sub, in: dr); return fromCtx(c) }
func lum(_ c: (Float, Float, Float, Float)) -> Float { 0.2126 * c.0 + 0.7152 * c.1 + 0.0722 * c.2 }
func hex(_ s: String) -> (Float, Float, Float) { let v = UInt32(s.replacingOccurrences(of: "#", with: ""), radix: 16)!
  return (Float((v >> 16) & 255) / 255, Float((v >> 8) & 255) / 255, Float(v & 255) / 255) }
func smooth(_ a: Float, _ b: Float, _ x: Float) -> Float { let t = max(0, min(1, (x - a) / (b - a))); return t * t * (3 - 2 * t) }
// Antialiased coverage of a rounded rectangle (top-left coords).
func rrect(_ x: Float, _ y: Float, _ r: CGRect, _ rad: Float) -> Float {
  let cx = Float(r.midX), cy = Float(r.midY), hw = Float(r.width) / 2 - rad, hh = Float(r.height) / 2 - rad
  let qx = max(abs(x - cx) - hw, 0), qy = max(abs(y - cy) - hh, 0)
  let d = (qx * qx + qy * qy).squareRoot() - rad + min(max(abs(x - cx) - hw, abs(y - cy) - hh), 0)
  return max(0, min(1, 0.5 - d)) }
// Renders text into an alpha mask (row 0 = top), its cap box centered on (cx, cy).
func textMask(_ w: Int, _ h: Int, _ s: String, font: String, capPx: CGFloat, cx: CGFloat, cy: CGFloat) -> [Float] {
  let desc = CTFontManagerCreateFontDescriptorsFromURL(URL(fileURLWithPath: font) as CFURL) as! [CTFontDescriptor]
  let f0 = CTFontCreateWithFontDescriptor(desc[0], 100, nil); let size = 100 * capPx / CTFontGetCapHeight(f0)
  let f = CTFontCreateWithFontDescriptor(desc[0], size, nil)
  let attrs = [kCTFontAttributeName: f, kCTForegroundColorAttributeName: CGColor(red: 1, green: 1, blue: 1, alpha: 1)] as CFDictionary
  let line = CTLineCreateWithAttributedString(CFAttributedStringCreate(nil, s as CFString, attrs))
  let b = CTLineGetBoundsWithOptions(line, .useGlyphPathBounds)
  let c = ctx(w, h); c.setShouldAntialias(true)
  c.textPosition = CGPoint(x: cx - b.midX, y: (CGFloat(h) - cy) - CTFontGetCapHeight(f) / 2)
  CTLineDraw(line, c); let m = fromCtx(c)
  return (0..<(w * h)).map { m.p[$0 * 4 + 3] } }

let a = CommandLine.arguments
switch a[1] {
case "bill":
  // args: SRC OUT FONT x0 y0 axis y1 [rosetteX rosetteY], source pixels. The left half (x0...axis) is mirrored about the
  // medallion's axis, so the medallion lands at the bill's exact center, where the widget draws the badge.
  let src = load(a[2]); let x0 = Int(a[5])!, y0 = Int(a[6])!, ax = Int(a[7])!, y1 = Int(a[8])!
  let hw = ax - x0, hh = y1 - y0
  var sym = Img(2 * hw, hh)
  for y in 0..<hh { for x in 0..<hw { let c = src.px(x0 + x, y0 + y); sym.set(x, y, c); sym.set(2 * hw - 1 - x, y, c) } }
  let box = CGRect(x: 2, y: 2, width: 252, height: 124)
  var o = place(sym, crop: CGRect(x: 0, y: 0, width: sym.w, height: sym.h), into: 256, 128, at: box)
  if a.count > 10 && a[4] != "-" {
    let rx = 2 + CGFloat(Int(a[9])! - x0) / CGFloat(sym.w) * 252, ry = 2 + CGFloat(Int(a[10])! - y0) / CGFloat(sym.h) * 124
    let ink = hex("#2E3A2C")
    for cx in [rx, 256 - rx] {
      let m = textMask(256, 128, "100", font: a[4], capPx: 11, cx: cx, cy: ry)
      for y in 0..<128 { for x in 0..<256 { let t = m[y * 256 + x]; let hi = (y > 0 && x > 0) ? m[(y - 1) * 256 + x - 1] : 0
        var c = o.px(x, y)
        let lip = max(0, hi - t) * 0.5   // a light lip below right, so the number reads as pressed into the clay
        c.0 += (min(1, c.0 * 1.2) - c.0) * lip; c.1 += (min(1, c.1 * 1.2) - c.1) * lip; c.2 += (min(1, c.2 * 1.2) - c.2) * lip
        c.0 += (ink.0 - c.0) * t * 0.9; c.1 += (ink.1 - c.1) * t * 0.9; c.2 += (ink.2 - c.2) * t * 0.9; o.set(x, y, c) } } }
  }
  for y in 0..<128 { for x in 0..<256 { var c = o.px(x, y); c.3 = rrect(Float(x) + 0.5, Float(y) + 0.5, box, 7); o.set(x, y, c) } }
  save(o, a[3])
case "char":
  var o = load(a[2]); var mean: Float = 0, n: Float = 0
  for y in 0..<o.h { for x in 0..<o.w { let c = o.px(x, y); if c.3 > 0.5 { mean += lum(c); n += 1 } } }; mean /= n
  let ash = hex("#16110F"), warm = hex("#4A3A2A")
  for y in 0..<o.h { for x in 0..<o.w { let c = o.px(x, y); let d = (lum(c) - mean) * 0.55
    o.set(x, y, (ash.0 + warm.0 * 0.25 + d, ash.1 + warm.1 * 0.25 + d, ash.2 + warm.2 * 0.25 + d * 0.9, c.3)) } }
  save(o, a[3])
case "flames":
  let src = load(a[2])
  var bgL: Float = 0; for y in 4..<28 { for x in 4..<28 { bgL += lum(src.px(x, y)) } }; bgL /= 576
  var al = Img(src.w, src.h)   // keyed copy
  for y in 0..<src.h { for x in 0..<src.w { let c = src.px(x, y)
    let chroma = max(c.0, c.1, c.2) - min(c.0, c.1, c.2), m = max(chroma * 1.4, (lum(c) - bgL) * 1.3)
    let t = smooth(0.10, 0.24, m)
    // take the dark background back out of the edge colors
    let k: Float = t > 0.01 ? 1 / max(t, 0.35) : 0
    al.set(x, y, (min(1, bgL + (c.0 - bgL) * k), min(1, bgL + (c.1 - bgL) * k), min(1, bgL + (c.2 - bgL) * k), t)) } }
  func groups(_ proj: [Int], _ minRun: Int) -> [(Int, Int)] { var g = [(Int, Int)](); var s = -1
    for (i, v) in proj.enumerated() { if v > 0 && s < 0 { s = i } else if v == 0 && s >= 0 { if i - s >= minRun { g.append((s, i)) }; s = -1 } }
    if s >= 0 { g.append((s, proj.count)) }; return g }
  var colP = [Int](repeating: 0, count: src.w), rowP = [Int](repeating: 0, count: src.h)
  for y in 0..<src.h { for x in 0..<src.w where al.p[(y * src.w + x) * 4 + 3] > 0.5 { colP[x] += 1; rowP[y] += 1 } }
  let cg4 = groups(colP.map { $0 > 2 ? 1 : 0 }, 40), rg2 = groups(rowP.map { $0 > 2 ? 1 : 0 }, 40)
  print("flame columns:", cg4, "rows:", rg2)
  var boxes = [CGRect]()
  for r in rg2 { for c in cg4 { boxes.append(CGRect(x: c.0 - 3, y: r.0 - 3, width: c.1 - c.0 + 6, height: r.1 - r.0 + 6)) } }
  // frame plan: (flame index, mirrored, height scale, width scale), alternating the rows so the color flickers too
  let plan: [(Int, Bool, CGFloat, CGFloat)] = [(0, false, 1.00, 1.00), (5, true, 0.94, 1.04), (2, false, 1.06, 0.96), (4, true, 0.96, 1.02),
                                               (1, false, 1.03, 0.98), (7, true, 0.91, 1.05), (3, false, 1.08, 0.95), (6, true, 0.98, 1.00)]
  var sheet = Img(1024, 128)
  for (f, (i, flip, hs, ws)) in plan.enumerated() { let b = boxes[i]
    let H = 104 * hs, W = H * b.width / b.height * ws
    let fr = place(al, crop: b, into: 128, 128, at: CGRect(x: (128 - W) / 2, y: 118 - H, width: W, height: H), flip: flip)
    for y in 0..<128 { for x in 0..<128 { sheet.set(f * 128 + x, y, fr.px(x, y)) } } }
  save(sheet, a[3])
  // the ember: the small loose tip in the first flame's box (the smallest blob of a fair size)
  let b = boxes[0]; let bx = Int(b.minX), by = Int(b.minY), bw = Int(b.width), bh = Int(b.height)
  var lab = [Int](repeating: 0, count: bw * bh); var comps = [(Int, Int, Int, Int, Int)]()   // area, minx, miny, maxx, maxy
  for sy in 0..<bh { for sx in 0..<bw where lab[sy * bw + sx] == 0 && al.p[((by + sy) * src.w + bx + sx) * 4 + 3] > 0.5 {
    var st = [(sx, sy)]; lab[sy * bw + sx] = comps.count + 1; var c = (0, sx, sy, sx, sy)
    while let (x, y) = st.popLast() { c.0 += 1; c.1 = min(c.1, x); c.2 = min(c.2, y); c.3 = max(c.3, x); c.4 = max(c.4, y)
      for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)] { let nx = x + dx, ny = y + dy
        if nx >= 0 && ny >= 0 && nx < bw && ny < bh && lab[ny * bw + nx] == 0 && al.p[((by + ny) * src.w + bx + nx) * 4 + 3] > 0.5 {
          lab[ny * bw + nx] = comps.count + 1; st.append((nx, ny)) } } }
    comps.append(c) } }
  let tips = comps.filter { $0.0 > 60 }.sorted { $0.0 < $1.0 }
  print("blobs in flame 1 (area):", comps.map { $0.0 }.filter { $0 > 20 })
  if tips.count > 1, let t = tips.first { let pad = 4
    let r = CGRect(x: bx + t.1 - pad, y: by + t.2 - pad, width: t.3 - t.1 + 2 * pad, height: t.4 - t.2 + 2 * pad)
    let s = 24 / max(r.width, r.height)
    let e = place(al, crop: r, into: 32, 32, at: CGRect(x: (32 - r.width * s) / 2, y: (32 - r.height * s) / 2, width: r.width * s, height: r.height * s))
    save(e, a[4]) } else { print("no separate tip found; no ember written") }
case "badge":
  let src = load(a[2]); let col = hex(a[5]); let ink = hex("#2B1D12")
  // clay grain: the high-pass luminance of a plain patch of the bill's paper
  let patch = place(src, crop: CGRect(x: Int(a.count > 7 ? Int(a[7])! : 330), y: Int(a.count > 8 ? Int(a[8])! : 600), width: 160, height: 160), into: 128, 128, at: CGRect(x: 0, y: 0, width: 128, height: 128))
  var L = [Float](repeating: 0, count: 128 * 128); for i in 0..<(128 * 128) { L[i] = lum(patch.px(i % 128, i / 128)) }
  var B = L; let r = 5
  for y in 0..<128 { for x in 0..<128 { var s: Float = 0, n: Float = 0
    for dy in -r...r { for dx in -r...r { let xx = min(127, max(0, x + dx)), yy = min(127, max(0, y + dy)); s += L[yy * 128 + xx]; n += 1 } }
    B[y * 128 + x] = s / n } }
  let m = textMask(128, 128, a[6], font: a[4], capPx: 60, cx: 64, cy: 64)
  var o = Img(128, 128); let R: Float = 63
  for y in 0..<128 { for x in 0..<128 {
    let dx = Float(x) + 0.5 - 64, dy = Float(y) + 0.5 - 64, d = (dx * dx + dy * dy).squareRoot(), rr = d / R
    var s: Float = 1 - 0.10 * (dx + dy) / R                       // light from the upper left
    if rr > 0.86 && rr < 0.98 { let t = (rr - 0.86) / 0.12; s += (t < 0.5 ? 0.12 : -0.22) * sin(t * .pi) * 1.0 }   // raised rim
    if rr > 0.80 && rr <= 0.86 { s -= 0.10 * sin((rr - 0.80) / 0.06 * .pi) }                                      // groove inside the rim
    let g = (L[y * 128 + x] - B[y * 128 + x]) * 1.6
    var c = (col.0 * s + g, col.1 * s + g, col.2 * s + g)
    let hi = y > 0 && x > 0 ? m[(y - 1) * 128 + (x - 1)] : 0       // pressed-in letter: a light lip below right
    let t = m[y * 128 + x]
    c.0 += (min(1, col.0 * 1.25) - c.0) * max(0, hi - t) * 0.8; c.1 += (min(1, col.1 * 1.25) - c.1) * max(0, hi - t) * 0.8; c.2 += (min(1, col.2 * 1.25) - c.2) * max(0, hi - t) * 0.8
    c.0 += (ink.0 - c.0) * t * 0.92; c.1 += (ink.1 - c.1) * t * 0.92; c.2 += (ink.2 - c.2) * t * 0.92
    o.set(x, y, (c.0, c.1, c.2, max(0, min(1, R - d + 0.5)))) } }
  save(o, a[3])
default: print("unknown command")
}
