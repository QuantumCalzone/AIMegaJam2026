// T98: removes the thin wire frames that the edit model drew where the cast sheet's red blocks had been, in
// round 4's take 1. Near each block's edges, a pixel that differs from the pixels 3 px to either side while
// those two match each other is a thin line, and takes their average (horizontally for the side edges,
// vertically for the top and bottom edges). Run from the repo root:
//   swift Docs/Art/Set/house/delines.swift Docs/Art/Set/house/r4/edit_1.png Docs/Art/Set/house.png
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count == 3 else { fatalError("usage: delines.swift <in.png> <out.png>") }
guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: args[1]) as CFURL, nil),
      let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("can't read \(args[1])") }
let W = img.width, H = img.height
var px = [UInt8](repeating: 0, count: W * H * 4)
let ctx = CGContext(data: &px, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))

let blocks = [(429, 243, 491, 357), (538, 243, 601, 334), (636, 243, 710, 337), (741, 243, 815, 336), (848, 243, 922, 339)]
let pad = 14, off = 3
func rgb(_ x: Int, _ y: Int) -> [Double] { let i = (y * W + x) * 4; return [Double(px[i]), Double(px[i + 1]), Double(px[i + 2])] }
func dist(_ a: [Double], _ b: [Double]) -> Double { abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) }
var changed = 0
// Two passes, so a 2 px line that the first pass only halves is caught by the second.
for _ in 0..<2 {
    for (x0, y0, x1, y1) in blocks {
        for y in (y0 - pad)...(y1 + pad) {
            for x in (x0 - pad)...(x1 + pad) {
                let nearSide = abs(x - x0) <= pad || abs(x - x1) <= pad
                let nearTopBottom = abs(y - y0) <= pad || abs(y - y1) <= pad
                var fixes: [[Double]] = []
                if nearSide { let l = rgb(x - off, y), r = rgb(x + off, y); if dist(l, r) < 30 { fixes.append(zip(l, r).map { ($0 + $1) / 2 }) } }
                if nearTopBottom { let u = rgb(x, y - off), d = rgb(x, y + off); if dist(u, d) < 30 { fixes.append(zip(u, d).map { ($0 + $1) / 2 }) } }
                let c = rgb(x, y)
                for f in fixes where dist(c, f) > 36 {
                    let i = (y * W + x) * 4
                    px[i] = UInt8(f[0]); px[i + 1] = UInt8(f[1]); px[i + 2] = UInt8(f[2])
                    changed += 1
                    break
                }
            }
        }
    }
}
let out = ctx.makeImage()!
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: args[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, out, nil)
CGImageDestinationFinalize(dst)
print("saved \(args[2]), \(changed) pixels changed")
