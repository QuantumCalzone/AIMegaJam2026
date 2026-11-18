// T98: paints out the antenna that the edit left on the front view of the audience robot (s4_audience_fix,
// edit_1, robot 1). Inside the antenna's box, above the dome, every reddish pixel takes the gray of the
// background 14 px to its left. Run from the repo root:
//   swift Docs/Art/Set/pieces/noantenna.swift Docs/Art/Set/pieces/s4_audience_fix/edit_1.png Docs/Art/Set/pieces/s4_audience_fix/edit_1_noantenna.png
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
let img = CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil)!, 0, nil)!
let W = img.width, H = img.height
var px = [UInt8](repeating: 0, count: W * H * 4)
let ctx = CGContext(data: &px, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))
var n = 0
for y in 252...289 {
    for x in 136...166 {
        let i = (y * W + x) * 4
        if Int(px[i]) > Int(px[i + 1]) + 12 {
            let j = (y * W + x - 14 - (x - 136)) * 4   // a background pixel left of the box, same row
            px[i] = px[j]; px[i + 1] = px[j + 1]; px[i + 2] = px[j + 2]; n += 1
        }
    }
}
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
print("saved \(a[2]), \(n) pixels changed")
