// T98's house collage: the house-camera capture in the design doc (stage.jpg, 2026-11-15) on the edit model's
// 16:9 canvas (1344 x 768), with the five robots from Docs/BotArt/cast.png pasted over the old pill robots at
// their places, in seat order. Leonardo's edit model then repaints it as one clay house. Run from the repo root:
//   swift Docs/Art/Set/house/collage.swift Docs/Design/images/ArtInspiration/stage.jpg Docs/BotArt/cast.png Docs/Art/Set/house/collage.png
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count == 4 else { fatalError("usage: collage.swift <stage.jpg> <cast.png> <out.png>") }

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

let stage = load(args[1]), cast = load(args[2])
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

// The capture, stretched to the canvas (1920 x 1080 -> 1344 x 768, 1.6% taller).
drawFlipped(stage, in: CGRect(x: 0, y: 0, width: W, height: H))

// Soft-edged mask (black paints), so each crop's own curtain fades into the stage.
func mask(width: Int, height: Int) -> CGImage {
    var px = [UInt8](repeating: 0, count: width * height)
    let fw = Double(width) * 0.16, fh = Double(height) * 0.06
    for y in 0..<height {
        let dy = max(0, min(1, min(Double(y), Double(height - 1 - y)) / fh))
        for x in 0..<width {
            let dx = max(0, min(1, min(Double(x), Double(width - 1 - x)) / fw))
            px[y * width + x] = UInt8(255 - 255 * dx * dy)   // an image mask paints where it is black
        }
    }
    let provider = CGDataProvider(data: Data(px) as CFData)!
    return CGImage(maskWidth: width, height: height, bitsPerComponent: 8, bitsPerPixel: 8, bytesPerRow: width,
                   provider: provider, decode: nil, shouldInterpolate: true)!
}

// Each robot's box in cast.png (x, y, w, h), with OpenAI's halo and floor ring left out, and where its feet
// go on the canvas: the old robot's center x, its feet's y, and its height on screen in px.
struct Bot { let crop: CGRect; let cx: CGFloat; let feet: CGFloat; let h: CGFloat }
let bots = [
    Bot(crop: CGRect(x: 120, y: 255, width: 435, height: 780), cx: 455, feet: 362, h: 118),    // OpenAI
    Bot(crop: CGRect(x: 2195, y: 200, width: 490, height: 875), cx: 566, feet: 357, h: 122),   // Anthropic
    Bot(crop: CGRect(x: 1440, y: 110, width: 595, height: 935), cx: 671, feet: 355, h: 128),   // You
    Bot(crop: CGRect(x: 2835, y: 240, width: 640, height: 805), cx: 776, feet: 357, h: 116),   // SpaceXAI
    Bot(crop: CGRect(x: 795, y: 140, width: 485, height: 960), cx: 888, feet: 362, h: 128),    // Meta
]
for b in bots {
    let part = cast.cropping(to: b.crop)!
    let s = b.h / b.crop.height
    let w = b.crop.width * s
    let r = CGRect(x: b.cx - w / 2, y: b.feet - b.h, width: w, height: b.h)
    drawFlipped(part, in: r, mask: mask(width: Int(b.crop.width), height: Int(b.crop.height)))
}

save(ctx.makeImage()!, args[3])
print("saved \(args[3])")
