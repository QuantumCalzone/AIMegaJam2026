// The itch cover: crops the repainted art to 1.26 : 1, shades the top, and sets the name in the game's display
// style (UIStyle: Gold #F2C14E letters with an InkSolid #161225 outline) in Roboto Black, the engine's own font.
// Writes the full-size master; sips makes the 630 x 500 cover from it (see Docs/ItchMedia/README.md).
// Run from the repo root:
//   swift Docs/ItchMedia/cover_art/title.swift <art.png> <Roboto-Black.ttf> <out.png> [cropX]
import CoreGraphics
import CoreText
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count >= 4 else { fatalError("usage: title.swift <art.png> <font.ttf> <out.png> [cropX]") }

func load(_ path: String) -> CGImage {
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("can't read \(path)") }
    return img
}

func rgb(_ hex: UInt32, _ a: CGFloat = 1) -> CGColor {
    CGColor(srgbRed: CGFloat((hex >> 16) & 255) / 255, green: CGFloat((hex >> 8) & 255) / 255,
            blue: CGFloat(hex & 255) / 255, alpha: a)
}

let art = load(args[1])
let H = art.height                                   // 896
let W = Int((Double(H) * 630.0 / 500.0).rounded())   // 1129: itch's cover shape, 630 x 500
let cropX = args.count > 4 ? Int(args[4])! : (art.width - W) / 2
let crop = art.cropping(to: CGRect(x: cropX, y: 0, width: W, height: H))!

let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
// CoreGraphics is y-up here: y = H is the top edge.
ctx.draw(crop, in: CGRect(x: 0, y: 0, width: W, height: H))

// Shade the top 40% with ink, strongest at the top edge, so the name stands off the bright spotlight.
let shade = CGGradient(colorsSpace: CGColorSpace(name: CGColorSpace.sRGB)!,
                       colors: [rgb(0x161225, 0.55), rgb(0x161225, 0)] as CFArray, locations: [0, 1])!
ctx.drawLinearGradient(shade, start: CGPoint(x: 0, y: H), end: CGPoint(x: 0, y: Double(H) * 0.60), options: [])

// The font, from the file (the engine's Roboto, Apache 2.0).
let provider = CGDataProvider(url: URL(fileURLWithPath: args[2]) as CFURL)!
let cgFont = CGFont(provider)!

// One line of text as a path, centred on x = W/2 with its baseline at `baseline` (y-up), letter-spaced.
func textPath(_ s: String, size: CGFloat, baseline: CGFloat, tracking: CGFloat) -> CGPath {
    let font = CTFontCreateWithGraphicsFont(cgFont, size, nil, nil)
    let attr = NSAttributedString(string: s, attributes: [
        NSAttributedString.Key(kCTFontAttributeName as String): font,
        NSAttributedString.Key(kCTKernAttributeName as String): size * tracking])
    let line = CTLineCreateWithAttributedString(attr)
    let width = CTLineGetTypographicBounds(line, nil, nil, nil) - Double(size * tracking)  // no trailing space
    let path = CGMutablePath()
    let x0 = (CGFloat(W) - CGFloat(width)) / 2
    for run in CTLineGetGlyphRuns(line) as! [CTRun] {
        let n = CTRunGetGlyphCount(run)
        var glyphs = [CGGlyph](repeating: 0, count: n)
        var pos = [CGPoint](repeating: .zero, count: n)
        CTRunGetGlyphs(run, CFRange(location: 0, length: n), &glyphs)
        CTRunGetPositions(run, CFRange(location: 0, length: n), &pos)
        for i in 0..<n {
            guard let g = CTFontCreatePathForGlyph(font, glyphs[i], nil) else { continue }
            path.addPath(g, transform: CGAffineTransform(translationX: x0 + pos[i].x, y: baseline))
        }
    }
    return path
}

// Two lines: NO HUMANS / ON SET, in the top 31% of the frame (the antenna starts at about 33%).
let size1: CGFloat = 150, size2: CGFloat = 150
let cap = size1 * 0.711                                  // Roboto's cap height
let top: CGFloat = 34                                    // px from the top edge to the first line's caps
let gap: CGFloat = 26
let base1 = CGFloat(H) - top - cap
let base2 = base1 - gap - size2 * 0.711
let title = CGMutablePath()
title.addPath(textPath("NO HUMANS", size: size1, baseline: base1, tracking: 0.02))
title.addPath(textPath("ON SET", size: size2, baseline: base2, tracking: 0.08))

// A soft drop shadow, then a thick ink outline, then the gold fill (light at the top, deeper at the base).
ctx.saveGState()
ctx.setShadow(offset: CGSize(width: 0, height: -8), blur: 18, color: rgb(0x000000, 0.7))
ctx.addPath(title)
ctx.setLineWidth(18)
ctx.setLineJoin(.round)
ctx.setStrokeColor(rgb(0x161225))
ctx.strokePath()
ctx.restoreGState()

ctx.addPath(title)
ctx.setLineWidth(18)
ctx.setLineJoin(.round)
ctx.setStrokeColor(rgb(0x161225))
ctx.strokePath()

func goldFill(_ path: CGPath, top: CGFloat, bottom: CGFloat) {
    ctx.saveGState()
    ctx.addPath(path)
    ctx.clip()
    let g = CGGradient(colorsSpace: CGColorSpace(name: CGColorSpace.sRGB)!,
                       colors: [rgb(0xFFE7A0), rgb(0xF2C14E), rgb(0xD39A2E)] as CFArray,
                       locations: [0, 0.5, 1])!
    ctx.drawLinearGradient(g, start: CGPoint(x: 0, y: top), end: CGPoint(x: 0, y: bottom), options: [])
    ctx.restoreGState()
}
goldFill(textPath("NO HUMANS", size: size1, baseline: base1, tracking: 0.02), top: base1 + cap, bottom: base1)
goldFill(textPath("ON SET", size: size2, baseline: base2, tracking: 0.08), top: base2 + size2 * 0.711, bottom: base2)

let url = URL(fileURLWithPath: args[3]) as CFURL
let dst = CGImageDestinationCreateWithURL(url, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
print("wrote \(args[3]) (\(W) x \(H), crop x \(cropX))")
