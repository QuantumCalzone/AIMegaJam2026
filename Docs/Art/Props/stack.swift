// T97: stacks images of the same width top to bottom (the seven card strips into the design doc's props picture).
//   swift Docs/Art/Props/stack.swift <out.png> <img> <img> ...
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let args = Array(CommandLine.arguments.dropFirst())
let imgs = args.dropFirst().map { p -> CGImage in
    let s = CGImageSourceCreateWithURL(URL(fileURLWithPath: p) as CFURL, nil)!
    return CGImageSourceCreateImageAtIndex(s, 0, nil)!
}
let W = imgs.map(\.width).max()!, H = imgs.map(\.height).reduce(0, +)
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
var top = 0
for img in imgs {
    ctx.draw(img, in: CGRect(x: 0, y: H - top - img.height, width: img.width, height: img.height))
    top += img.height
}
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: args[0]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
print("saved \(args[0]) (\(W) x \(H))")
