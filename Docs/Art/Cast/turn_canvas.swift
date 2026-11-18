// T95 turnaround input: a 1344 x 768 light gray canvas (one of the edit model's own sizes) with the approved
// concept on the left half and the right half empty, for one edit that draws the front view on the left and the
// side view on the right. Run from the repo root:
//   swift Docs/Art/Cast/turn_canvas.swift <approved.png> <out.png>
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let a = Array(CommandLine.arguments.dropFirst())
guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[0]) as CFURL, nil),
      let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("can't read \(a[0])") }
let W = 1344, H = 768
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.interpolationQuality = .high
ctx.setFillColor(CGColor(red: 0.85, green: 0.85, blue: 0.85, alpha: 1))
ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
let h = Double(H), w = Double(img.width) * h / Double(img.height)
ctx.draw(img, in: CGRect(x: Double(W) / 4 - w / 2, y: 0, width: w, height: h))
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
