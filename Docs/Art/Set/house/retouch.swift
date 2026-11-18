// T98: paints out the red blocks that the cast sheet's curtain left behind each robot in the picked house
// concept. Inside each block's box, every strongly crimson pixel is replaced, row by row, by a blend of the
// pixels just left and right of the box (the backdrop above the horizon, the floor below it). The orange
// robot is not crimson enough to match; my scarf and the red telephone on the table are left out by hand.
// Run from the repo root:
//   swift Docs/Art/Set/house/retouch.swift Docs/Art/Set/house/r1c_cream/edit_1.png Docs/Art/Set/house/r1_pick_retouched.png
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count == 3 else { fatalError("usage: retouch.swift <in.png> <out.png>") }
guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: args[1]) as CFURL, nil),
      let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("can't read \(args[1])") }
let W = img.width, H = img.height
var px = [UInt8](repeating: 0, count: W * H * 4)
let ctx = CGContext(data: &px, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))   // row 0 of px is the top row

// Block boxes (x0, y0, x1, y1), top-left pixel coordinates on the 1344 x 768 pick.
let blocks = [(429, 243, 491, 357), (538, 243, 601, 334), (636, 243, 710, 337), (741, 243, 815, 336), (848, 243, 922, 339)]
let keep = [(658, 281, 692, 320), (815, 270, 850, 310)]   // my scarf; the red telephone
func kept(_ x: Int, _ y: Int) -> Bool { keep.contains { x >= $0.0 && x <= $0.2 && y >= $0.1 && y <= $0.3 } }
func at(_ x: Int, _ y: Int) -> (Double, Double, Double) {
    var r = 0.0, g = 0.0, b = 0.0
    for dx in -1...1 { let i = (y * W + min(W - 1, max(0, x + dx))) * 4; r += Double(px[i]); g += Double(px[i + 1]); b += Double(px[i + 2]) }
    return (r / 3, g / 3, b / 3)
}
var changed = 0
for (x0, y0, x1, y1) in blocks {
    for y in y0...y1 {
        let l = at(x0 - 3, y), r = at(x1 + 3, y)
        for x in x0...x1 where !kept(x, y) {
            let i = (y * W + x) * 4
            let R = Double(px[i]), G = Double(px[i + 1]), B = Double(px[i + 2])
            // The box's edge rows and columns take softer reds (the block's anti-aliased outline); the orange
            // robot's box (the second) needs a stricter ratio inside, so its shaded edges stay orange.
            let edge = min(x - x0, x1 - x, y - y0, y1 - y) < 4
            let ratio = edge ? 1.6 : (x0 == 538 ? 3.0 : 2.4)
            guard R > 55, R > ratio * G, R > (edge ? 1.4 : 2.0) * B else { continue }
            let t = Double(x - x0) / Double(x1 - x0)
            px[i] = UInt8(l.0 + (r.0 - l.0) * t); px[i + 1] = UInt8(l.1 + (r.1 - l.1) * t); px[i + 2] = UInt8(l.2 + (r.2 - l.2) * t)
            changed += 1
        }
    }
}
let out = ctx.makeImage()!
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: args[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, out, nil)
CGImageDestinationFinalize(dst)
print("saved \(args[2]), \(changed) pixels changed")
