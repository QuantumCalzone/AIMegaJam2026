// T96: canvases for the costume edits. Run from the repo root:
//   swift Docs/Art/Costumes/canvas.swift pad <in.png> <out.png> <W> <H>
//       Scales the source to width W, puts it at the bottom, and fills the headroom above by stretching its
//       top 24 px (the lineup's curtain folds run straight up, so they continue cleanly).
//   swift Docs/Art/Costumes/canvas.swift tile <out.png> <W> <H> <img|-> [<img|-> ...]
//       Equal panels side by side on plain light gray (#D9D9D9), each image scaled to fit its panel and
//       centred; "-" leaves a panel empty. Gives every image in an edit the same shape (T94's lesson).
//   swift Docs/Art/Costumes/canvas.swift sheet <out.png> <panelW> <panelH> <label> <img> [<label> <img> ...]
//       A fit sheet: the panels side by side on dark plum, each image scaled to fit, its label above it.
//   swift Docs/Art/Costumes/canvas.swift grid <out.png> <cols> <cellW> <cellH> <label> <img> [...]
//       Labeled cells in rows of <cols>, filled row by row, each image scaled to fit its cell.
//   swift Docs/Art/Costumes/canvas.swift crop <in.png> <out.png> <x> <y> <w> <h>
//       A crop in top-left pixel coordinates (sips -c ignores its offset and crops from the centre).
import CoreGraphics
import CoreText
import Foundation
import ImageIO
import UniformTypeIdentifiers

let a = Array(CommandLine.arguments.dropFirst())
func load(_ p: String) -> CGImage {
    guard let s = CGImageSourceCreateWithURL(URL(fileURLWithPath: p) as CFURL, nil),
          let i = CGImageSourceCreateImageAtIndex(s, 0, nil) else { fatalError("can't read \(p)") }
    return i
}
func canvas(_ w: Int, _ h: Int) -> CGContext {
    let c = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
                      space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    c.interpolationQuality = .high
    c.setFillColor(CGColor(red: 0.85, green: 0.85, blue: 0.85, alpha: 1))
    c.fill(CGRect(x: 0, y: 0, width: w, height: h))
    return c
}
func save(_ c: CGContext, _ p: String) {
    let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: p) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(d, c.makeImage()!, nil)
    CGImageDestinationFinalize(d)
}
switch a[0] {
case "pad":
    let img = load(a[1]), W = Int(a[3])!, H = Int(a[4])!
    let c = canvas(W, H)
    let s = Double(W) / Double(img.width), ih = Double(img.height) * s
    c.draw(img, in: CGRect(x: 0, y: 0, width: Double(W), height: ih))
    if let top = img.cropping(to: CGRect(x: 0, y: 0, width: img.width, height: 24)) {
        c.draw(top, in: CGRect(x: 0, y: ih - 1, width: Double(W), height: Double(H) - ih + 1))
    }
    save(c, a[2])
case "tile":
    let W = Int(a[2])!, H = Int(a[3])!, paths = Array(a[4...])
    let c = canvas(W, H), pw = Double(W) / Double(paths.count)
    for (i, p) in paths.enumerated() where p != "-" {
        let img = load(p)
        let s = min(pw / Double(img.width), Double(H) / Double(img.height))
        let w = Double(img.width) * s, h = Double(img.height) * s
        c.draw(img, in: CGRect(x: pw * Double(i) + (pw - w) / 2, y: (Double(H) - h) / 2, width: w, height: h))
    }
    save(c, a[1])
case "sheet":
    let pw = Int(a[2])!, ph = Int(a[3])!, rest = Array(a[4...]), n = rest.count / 2, pad = 12, head = 44
    let W = n * pw + (n + 1) * pad, H = head + ph + 2 * pad
    let c = canvas(W, H)
    c.setFillColor(CGColor(red: 0.13, green: 0.10, blue: 0.11, alpha: 1))
    c.fill(CGRect(x: 0, y: 0, width: W, height: H))
    for i in 0..<n {
        let x = pad + i * (pw + pad)
        let font = CTFontCreateWithName("Helvetica-Bold" as CFString, 24, nil)
        let attrs: [NSAttributedString.Key: Any] = [
            NSAttributedString.Key(kCTFontAttributeName as String): font,
            NSAttributedString.Key(kCTForegroundColorAttributeName as String): CGColor(red: 0.94, green: 0.89, blue: 0.77, alpha: 1)]
        let line = CTLineCreateWithAttributedString(NSAttributedString(string: rest[2 * i], attributes: attrs))
        let tw = CTLineGetTypographicBounds(line, nil, nil, nil)
        c.textPosition = CGPoint(x: Double(x) + (Double(pw) - tw) / 2, y: Double(H - pad - 30))
        CTLineDraw(line, c)
        let img = load(rest[2 * i + 1])
        let s = min(Double(pw) / Double(img.width), Double(ph) / Double(img.height))
        let w = Double(img.width) * s, h = Double(img.height) * s
        c.draw(img, in: CGRect(x: Double(x) + (Double(pw) - w) / 2, y: Double(pad) + (Double(ph) - h) / 2, width: w, height: h))
    }
    save(c, a[1])
case "grid":
    let cols = Int(a[2])!, cw = Int(a[3])!, chh = Int(a[4])!, rest = Array(a[5...]), n = rest.count / 2
    let pad = 12, head = 34, rows = (n + cols - 1) / cols
    let W = cols * cw + (cols + 1) * pad, H = rows * (head + chh) + (rows + 1) * pad
    let c = canvas(W, H)
    c.setFillColor(CGColor(red: 0.13, green: 0.10, blue: 0.11, alpha: 1))
    c.fill(CGRect(x: 0, y: 0, width: W, height: H))
    for i in 0..<n {
        let x = pad + (i % cols) * (cw + pad), top = pad + (i / cols) * (head + chh + pad)
        let font = CTFontCreateWithName("Helvetica-Bold" as CFString, 22, nil)
        let attrs: [NSAttributedString.Key: Any] = [
            NSAttributedString.Key(kCTFontAttributeName as String): font,
            NSAttributedString.Key(kCTForegroundColorAttributeName as String): CGColor(red: 0.94, green: 0.89, blue: 0.77, alpha: 1)]
        let line = CTLineCreateWithAttributedString(NSAttributedString(string: rest[2 * i], attributes: attrs))
        c.textPosition = CGPoint(x: Double(x + 4), y: Double(H - top - 26))
        CTLineDraw(line, c)
        let img = load(rest[2 * i + 1])
        let s = min(Double(cw) / Double(img.width), Double(chh) / Double(img.height))
        let w = Double(img.width) * s, h = Double(img.height) * s
        c.draw(img, in: CGRect(x: Double(x) + (Double(cw) - w) / 2, y: Double(H - top - head - chh) + (Double(chh) - h) / 2, width: w, height: h))
    }
    save(c, a[1])
case "crop":
    let img = load(a[1])
    let r = CGRect(x: Int(a[3])!, y: Int(a[4])!, width: Int(a[5])!, height: Int(a[6])!)
    let part = img.cropping(to: r)!   // CGImage cropping uses top-left coordinates
    let c = canvas(part.width, part.height)
    c.draw(part, in: CGRect(x: 0, y: 0, width: part.width, height: part.height))
    save(c, a[2])
default: fatalError("pad, tile, sheet, grid or crop")
}
