// T95 lineup collage: the five approved characters side by side, scaled so each stands the same height
// (head top to feet), feet on one line. "feather" blends each panel's edges into its neighbours (the input for
// the repaint edit); "panels" keeps hard, separate panels. Run from the repo root:
//   swift Docs/Art/Cast/lineup.swift <out.png> <W> <H> <feetY> <charH> feather|panels  path:top:bottom:cx ...
// top, bottom and cx are the character's head top, feet bottom and centre x, in the source image's pixels.
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let a = Array(CommandLine.arguments.dropFirst())
let W = Int(a[1])!, H = Int(a[2])!, feetY = Double(a[3])!, charH = Double(a[4])!, feather = a[5] == "feather"
let chars = a[6...].map { s -> (CGImage, Double, Double, Double) in
    let p = s.split(separator: ":").map(String.init)
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: p[0]) as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("can't read \(p[0])") }
    return (img, Double(p[1])!, Double(p[2])!, Double(p[3])!)
}
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.interpolationQuality = .high
ctx.setFillColor(CGColor(red: 0.12, green: 0.1, blue: 0.1, alpha: 1))
ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
do {   // a plain stage behind the panels: crimson curtain over wooden planks, for the repaint to unify
    ctx.setFillColor(CGColor(red: 0.42, green: 0.06, blue: 0.07, alpha: 1))
    ctx.fill(CGRect(x: 0, y: Double(H) - feetY + 60, width: Double(W), height: feetY - 60))
    ctx.setFillColor(CGColor(red: 0.50, green: 0.30, blue: 0.16, alpha: 1))
    ctx.fill(CGRect(x: 0, y: 0, width: Double(W), height: Double(H) - feetY + 60))
}
let n = Double(chars.count), panel = Double(W) / n, gap = feather ? 0.0 : 8.0

// A horizontal soft mask: opaque in the middle, fading out over `f` of each side.
func hmask(_ w: Int, _ f: Double) -> CGImage {
    var px = [UInt8](repeating: 0, count: w)
    for x in 0..<w { px[x] = UInt8(255 * max(0, min(1, min(Double(x), Double(w - 1 - x)) / (Double(w) * f)))) }
    let prov = CGDataProvider(data: Data(px) as CFData)!   // a gray image, not an image mask: white paints
    return CGImage(width: w, height: 1, bitsPerComponent: 8, bitsPerPixel: 8, bytesPerRow: w,
                   space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGBitmapInfo(rawValue: 0), provider: prov,
                   decode: nil, shouldInterpolate: true, intent: .defaultIntent)!
}
for (i, (img, top, bottom, cx)) in chars.enumerated() {
    let s = charH / (bottom - top)
    let iw = Double(img.width) * s, ih = Double(img.height) * s
    let centre = panel * (Double(i) + 0.5)
    // top-left coordinates of the scaled image, then flipped into CG's bottom-left space
    let x0 = centre - cx * s, yTop = feetY - bottom * s
    let rect = CGRect(x: x0, y: Double(H) - (yTop + ih), width: iw, height: ih)
    let clipW = feather ? panel * 1.5 : panel - gap
    let clip = CGRect(x: centre - clipW / 2, y: 0, width: clipW, height: Double(H))
    ctx.saveGState()
    if feather { ctx.clip(to: clip, mask: hmask(Int(clipW), 0.22)) } else { ctx.clip(to: clip) }
    ctx.draw(img, in: rect)
    // Where the source doesn't reach the canvas edge, stretch its top and bottom strips (curtain folds and
    // planks run straight, so they continue cleanly).
    let strip = 24
    if rect.maxY < Double(H), let top = img.cropping(to: CGRect(x: 0, y: 0, width: img.width, height: strip)) {
        ctx.draw(top, in: CGRect(x: rect.minX, y: rect.maxY - 1, width: iw, height: Double(H) - rect.maxY + 1))
    }
    if rect.minY > 0, let bot = img.cropping(to: CGRect(x: 0, y: img.height - strip, width: img.width, height: strip)) {
        ctx.draw(bot, in: CGRect(x: rect.minX, y: 0, width: iw, height: rect.minY + 1))
    }
    ctx.restoreGState()
}
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[0]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
