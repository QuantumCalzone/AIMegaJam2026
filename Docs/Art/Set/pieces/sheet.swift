// T98: lays the piece views out on one review sheet, in the order given, 5 to a row, each fitted into a
// 320 x 320 cell. Run from the repo root:
//   swift Docs/Art/Set/pieces/sheet.swift Docs/Art/Set/pieces/sheet.png <view.png> ...
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let a = Array(CommandLine.arguments.dropFirst())
let out = a[0], files = Array(a.dropFirst())
let cell = 320, cols = 5, rows = (files.count + cols - 1) / cols
let W = cell * cols, H = cell * rows
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.setFillColor(CGColor(red: 0.75, green: 0.75, blue: 0.76, alpha: 1)); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
ctx.interpolationQuality = .high
for (k, f) in files.enumerated() {
    let img = CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: f) as CFURL, nil)!, 0, nil)!
    let s = min(Double(cell - 16) / Double(img.width), Double(cell - 16) / Double(img.height))
    let w = Double(img.width) * s, h = Double(img.height) * s
    let cx = Double((k % cols) * cell) + Double(cell) / 2, cy = Double(H - (k / cols) * cell) - Double(cell) / 2
    ctx.draw(img, in: CGRect(x: cx - w / 2, y: cy - h / 2, width: w, height: h))
}
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
print("saved \(out)")
