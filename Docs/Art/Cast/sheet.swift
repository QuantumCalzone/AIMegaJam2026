// Contact sheet for T95's rounds: the images side by side, each numbered, scaled to one height.
// Run from the repo root:  swift Docs/Art/Cast/sheet.swift <out.png> <height> <img1> <img2> ...
// A label may be given as path=LABEL (otherwise the images are numbered 1, 2, 3 ...).
import CoreGraphics
import CoreText
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = Array(CommandLine.arguments.dropFirst())
guard args.count >= 3, let H = Int(args[1]) else { fatalError("usage: sheet.swift <out.png> <height> <img> ...") }
let items: [(CGImage, String)] = args[2...].enumerated().map { i, a in
    let parts = a.components(separatedBy: "=")
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: parts[0]) as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("can't read \(parts[0])") }
    return (img, parts.count > 1 ? parts[1] : "\(i + 1)")
}
let gap = 12, label = 44
let widths = items.map { Int(Double($0.0.width) * Double(H) / Double($0.0.height)) }
let W = widths.reduce(0, +) + gap * (items.count + 1), TH = H + label + gap
let ctx = CGContext(data: nil, width: W, height: TH, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.interpolationQuality = .high
ctx.setFillColor(CGColor(red: 0.12, green: 0.1, blue: 0.1, alpha: 1))
ctx.fill(CGRect(x: 0, y: 0, width: W, height: TH))
let font = CTFontCreateWithName("Helvetica-Bold" as CFString, 30, nil)
var x = gap
for (i, (img, text)) in items.enumerated() {
    ctx.draw(img, in: CGRect(x: x, y: gap, width: widths[i], height: H))
    let s = NSAttributedString(string: text, attributes: [kCTFontAttributeName as NSAttributedString.Key: font,
        kCTForegroundColorAttributeName as NSAttributedString.Key: CGColor(red: 1, green: 1, blue: 1, alpha: 1)])
    let line = CTLineCreateWithAttributedString(s)
    let tw = CTLineGetTypographicBounds(line, nil, nil, nil)
    ctx.textPosition = CGPoint(x: Double(x) + (Double(widths[i]) - tw) / 2, y: Double(gap + H + 10))
    CTLineDraw(line, ctx)
    x += widths[i] + gap
}
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: args[0]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
