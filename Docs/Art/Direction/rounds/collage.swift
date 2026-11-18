// Round 1b collage for T94's direction board: the five robots from Docs/BotArt/cast.png pasted over the picked
// board, on a 1344 x 768 canvas (the edit model's own 16:9 size). Leonardo's edit model then repaints it as one
// scene, as the itch cover was made (Docs/ItchMedia/cover_art/layout.swift). Run from the repo root:
//   swift Docs/Art/Direction/rounds/collage.swift Docs/Art/Direction/rounds/r0_board.png Docs/BotArt/cast.png Docs/Art/Direction/rounds/r1b/collage.png
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count == 4 else { fatalError("usage: collage.swift <board.png> <cast.png> <out.png>") }

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

let board = load(args[1]), cast = load(args[2])
let panelW = cast.width / 5, panelH = cast.height   // five 700 x 1152 panels
let W = 1344, H = 768

let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.translateBy(x: 0, y: CGFloat(H))   // top-left coordinates
ctx.scaleBy(x: 1, y: -1)
ctx.interpolationQuality = .high

func drawFlipped(_ img: CGImage, in r: CGRect, mask: CGImage? = nil) {
    ctx.saveGState()
    ctx.translateBy(x: r.minX, y: r.maxY)
    ctx.scaleBy(x: 1, y: -1)
    let local = CGRect(x: 0, y: 0, width: r.width, height: r.height)
    if let m = mask { ctx.clip(to: local, mask: m) }
    ctx.draw(img, in: local)
    ctx.restoreGState()
}

// The board, scaled to the canvas height and centred.
let bs = CGFloat(H) / CGFloat(board.height)
let bw = CGFloat(board.width) * bs
drawFlipped(board, in: CGRect(x: (CGFloat(W) - bw) / 2, y: 0, width: bw, height: CGFloat(H)))

// Soft-edged mask (white paints), so each panel's own curtain fades into the board.
func mask(width: Int, height: Int) -> CGImage {
    var px = [UInt8](repeating: 0, count: width * height)
    let fw = Double(width) * 0.24, fh = Double(height) * 0.12
    for y in 0..<height {
        let dy = max(0, min(1, min(Double(y), Double(height - 1 - y)) / fh))
        for x in 0..<width {
            let dx = max(0, min(1, min(Double(x), Double(width - 1 - x)) / fw))
            let a = dx * dy
            px[y * width + x] = UInt8(255 * a * a * (3 - 2 * a))
        }
    }
    return CGImage(width: width, height: height, bitsPerComponent: 8, bitsPerPixel: 8, bytesPerRow: width,
                   space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGBitmapInfo(rawValue: 0),
                   provider: CGDataProvider(data: Data(px) as CFData)!, decode: nil, shouldInterpolate: true,
                   intent: .defaultIntent)!
}

// Each robot: its panel, canvas x of its centre and the panel row of its feet (from layout.swift).
// Left to right as in cast.png: OpenAI, Meta, You, Anthropic, SpaceXAI. The robot stands near panel x 357.
struct Bot { let panel: Int; let cx: CGFloat; let feetRow: CGFloat }
let bots = [Bot(panel: 0, cx: 290, feetRow: 1075), Bot(panel: 1, cx: 481, feetRow: 1088),
            Bot(panel: 3, cx: 863, feetRow: 1068), Bot(panel: 4, cx: 1054, feetRow: 1047),
            Bot(panel: 2, cx: 672, feetRow: 1034)]   // You drawn last, in front
let s: CGFloat = 0.32, feetY: CGFloat = 548
let softMask = mask(width: panelW, height: panelH)
for b in bots {
    let crop = cast.cropping(to: CGRect(x: b.panel * panelW, y: 0, width: panelW, height: panelH))!
    drawFlipped(crop, in: CGRect(x: b.cx - 357 * s, y: feetY - b.feetRow * s,
                                 width: CGFloat(panelW) * s, height: CGFloat(panelH) * s), mask: softMask)
}
save(ctx.makeImage()!, args[3])
print("wrote \(args[3]) (\(W) x \(H))")
