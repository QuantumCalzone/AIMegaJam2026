// Rough layout for the itch cover: the five robots from Docs/BotArt/cast.png on one canvas, You in front at
// the centre, the four AIs flanking, the top third clear for the title. Leonardo's edit model then repaints
// this collage as one scene (see Docs/ItchMedia/README.md). Run from the repo root:
//   swift Docs/ItchMedia/cover_art/layout.swift Docs/BotArt/cast.png Docs/ItchMedia/cover_art/layout.png
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count == 3 else { fatalError("usage: layout.swift <cast.png> <out.png>") }

func load(_ path: String) -> CGImage {
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("can't read \(path)") }
    return img
}

func save(_ img: CGImage, _ path: String) {
    let url = URL(fileURLWithPath: path) as CFURL
    guard let dst = CGImageDestinationCreateWithURL(url, UTType.png.identifier as CFString, 1, nil) else { fatalError() }
    CGImageDestinationAddImage(dst, img, nil)
    CGImageDestinationFinalize(dst)
}

let cast = load(args[1])
let panelW = cast.width / 5          // 700: the lineup is five 700 x 1152 panels side by side
let panelH = cast.height             // 1152
let W = 1152, H = 896                // one of the edit model's own sizes, 1.29 : 1 (the cover is 1.26 : 1)

let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
// Work in top-left coordinates, like the numbers below.
ctx.translateBy(x: 0, y: CGFloat(H))
ctx.scaleBy(x: 1, y: -1)
ctx.interpolationQuality = .high

func drawFlipped(_ img: CGImage, in r: CGRect) {
    ctx.saveGState()
    ctx.translateBy(x: r.minX, y: r.maxY)
    ctx.scaleBy(x: 1, y: -1)
    ctx.draw(img, in: CGRect(x: 0, y: 0, width: r.width, height: r.height))
    ctx.restoreGState()
}

// Background: a curtain-and-floor strip from Meta's panel (its left 100 px, clear of the robot), tiled across.
let strip = cast.cropping(to: CGRect(x: panelW, y: 0, width: 100, height: panelH))!
let sy = CGFloat(H) / CGFloat(panelH)
var x: CGFloat = 0
while x < CGFloat(W) {
    drawFlipped(strip, in: CGRect(x: x, y: 0, width: 100 * sy, height: CGFloat(H)))
    x += 100 * sy
}

// A soft-edged mask (white paints, black hides), so the panels' own curtains fade into the background.
func mask(width: Int, height: Int) -> CGImage {
    var px = [UInt8](repeating: 0, count: width * height)
    let fw = Double(width) * 0.24, fh = Double(height) * 0.16
    for y in 0..<height {
        let dy = max(0, min(1, Double(y) / fh))                // row 0 is the top edge
        for x in 0..<width {
            let dx = max(0, min(1, min(Double(x), Double(width - 1 - x)) / fw))
            let a = dx * dy
            px[y * width + x] = UInt8(255 * a * a * (3 - 2 * a))   // smoothstep
        }
    }
    let provider = CGDataProvider(data: Data(px) as CFData)!
    return CGImage(width: width, height: height, bitsPerComponent: 8, bitsPerPixel: 8, bytesPerRow: width,
                   space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGBitmapInfo(rawValue: 0),
                   provider: provider, decode: nil, shouldInterpolate: true, intent: .defaultIntent)!
}

// Each robot: its panel, the canvas x of its centre, its scale, and the canvas y of its feet.
// In every panel the robot stands near x 357; the feet (or OpenAI's ring) are at these panel rows.
struct Bot { let panel: Int; let cx: CGFloat; let s: CGFloat; let feetY: CGFloat; let feetRow: CGFloat }
let bots = [  // drawn back to front
    Bot(panel: 0, cx: 128, s: 0.48, feetY: 838, feetRow: 1075),   // OpenAI
    Bot(panel: 4, cx: 1000, s: 0.48, feetY: 838, feetRow: 1047),  // SpaceXAI
    Bot(panel: 1, cx: 335, s: 0.52, feetY: 852, feetRow: 1088),   // Meta
    Bot(panel: 3, cx: 815, s: 0.52, feetY: 852, feetRow: 1068),   // Anthropic
    Bot(panel: 2, cx: 576, s: 0.62, feetY: 874, feetRow: 1034),   // You
]
let softMask = mask(width: panelW, height: panelH)
for b in bots {
    let crop = cast.cropping(to: CGRect(x: b.panel * panelW, y: 0, width: panelW, height: panelH))!
    let w = CGFloat(panelW) * b.s, h = CGFloat(panelH) * b.s
    let r = CGRect(x: b.cx - 357 * b.s, y: b.feetY - b.feetRow * b.s, width: w, height: h)
    ctx.saveGState()
    ctx.translateBy(x: r.minX, y: r.maxY)
    ctx.scaleBy(x: 1, y: -1)
    let local = CGRect(x: 0, y: 0, width: r.width, height: r.height)
    ctx.clip(to: local, mask: softMask)
    ctx.draw(crop, in: local)
    ctx.restoreGState()
}

save(ctx.makeImage()!, args[2])
print("wrote \(args[2]) (\(W) x \(H))")
