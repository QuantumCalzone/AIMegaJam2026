// patch.swift: pastes a rectangle of PATCH over BASE with a feathered edge. Both images are drawn at BASE's size.
// Usage: patch BASE PATCH OUT x0 y0 x1 y1 feather   (pixels, origin top left)
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers
let a = CommandLine.arguments
func load(_ p: String) -> CGImage { CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: p) as CFURL, nil)!, 0, nil)! }
let base = load(a[1]), patch = load(a[2])
let x0 = Double(a[4])!, y0 = Double(a[5])!, x1 = Double(a[6])!, y1 = Double(a[7])!, f = Double(a[8])!
let W = base.width, H = base.height
let cs = CGColorSpace(name: CGColorSpace.sRGB)!
func raster(_ img: CGImage) -> [UInt8] {
  var buf = [UInt8](repeating: 0, count: W * H * 4)
  let c = CGContext(data: &buf, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
  c.interpolationQuality = .high
  c.draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))
  return buf
}
var b = raster(base); let p = raster(patch)
for y in 0..<H { for x in 0..<W {
  let dx = min(Double(x) - x0, x1 - Double(x)), dy = min(Double(y) - y0, y1 - Double(y))
  let m = max(0, min(1, min(dx, dy) / f))
  if m <= 0 { continue }
  let i = (y * W + x) * 4
  for k in 0..<4 { b[i+k] = UInt8(Double(b[i+k]) * (1 - m) + Double(p[i+k]) * m) }
}}
let c = CGContext(data: &b, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[3]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, c.makeImage()!, nil); CGImageDestinationFinalize(d)
