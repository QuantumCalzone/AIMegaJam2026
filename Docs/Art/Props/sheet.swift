// T97: a contact sheet of one card's prop candidates, one column per prop, one row per candidate, each
// labeled, so the card's props read as a set. Run from the repo root:
//   swift Docs/Art/Props/sheet.swift <out.png> <rows> <label> <img> [<img> ...] <label> <img> ...
// Each column is a label followed by exactly <rows> image paths ("-" leaves a cell empty).
import CoreGraphics
import CoreText
import Foundation
import ImageIO
import UniformTypeIdentifiers

var args = Array(CommandLine.arguments.dropFirst())
guard args.count >= 3, let rows = Int(args[1]) else { fatalError("usage: sheet.swift <out.png> <rows> <label> <img>...") }
let out = args[0]
args = Array(args.dropFirst(2))
var cols: [(String, [String])] = []
while !args.isEmpty {
    guard args.count >= rows + 1 else { fatalError("each column needs a label and \(rows) images") }
    cols.append((args[0], Array(args[1...rows])))
    args = Array(args.dropFirst(rows + 1))
}

func load(_ path: String) -> CGImage? {
    guard path != "-", let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil) else { return nil }
    return CGImageSourceCreateImageAtIndex(src, 0, nil)
}

let cell = 420, pad = 16, head = 56, tag = rows > 1 ? 30 : 0   // candidate numbers only when there is a choice
let W = cols.count * cell + (cols.count + 1) * pad
let H = head + rows * (cell + tag) + (rows + 1) * pad
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.setFillColor(CGColor(red: 0.13, green: 0.10, blue: 0.11, alpha: 1))
ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))

// CoreGraphics puts y = 0 at the bottom; these helpers take top-left coordinates.
func text(_ s: String, x: Int, top: Int, size: CGFloat, width: Int) {
    let font = CTFontCreateWithName("Helvetica-Bold" as CFString, size, nil)
    let attrs: [NSAttributedString.Key: Any] = [
        NSAttributedString.Key(kCTFontAttributeName as String): font,
        NSAttributedString.Key(kCTForegroundColorAttributeName as String): CGColor(red: 0.94, green: 0.89, blue: 0.77, alpha: 1)]
    let line = CTLineCreateWithAttributedString(NSAttributedString(string: s, attributes: attrs))
    let w = CTLineGetTypographicBounds(line, nil, nil, nil)
    ctx.textPosition = CGPoint(x: CGFloat(x) + (CGFloat(width) - CGFloat(w)) / 2, y: CGFloat(H - top) - size)
    CTLineDraw(line, ctx)
}

for (c, (label, paths)) in cols.enumerated() {
    let x = pad + c * (cell + pad)
    text(label, x: x, top: pad + 6, size: 26, width: cell)
    for (r, path) in paths.enumerated() {
        let top = head + pad + r * (cell + tag + pad)
        if let img = load(path) {
            ctx.interpolationQuality = .high
            ctx.draw(img, in: CGRect(x: x, y: H - top - cell, width: cell, height: cell))
        }
        if rows > 1 { text("\(r + 1)", x: x, top: top + cell + 2, size: 22, width: cell) }
    }
}

let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
print("saved \(out) (\(W) x \(H))")
