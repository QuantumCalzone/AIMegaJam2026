// overlay.swift: OUT W H BGHEX then groups of: file x y w h [cropX cropY cropW cropH] separated by "+" (top-left coords)
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers
let a = CommandLine.arguments
let W = Int(a[2])!, H = Int(a[3])!, bg = UInt32(a[4], radix: 16)!
let c = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
c.setFillColor(red: CGFloat((bg >> 16) & 255) / 255, green: CGFloat((bg >> 8) & 255) / 255, blue: CGFloat(bg & 255) / 255, alpha: 1)
c.fill(CGRect(x: 0, y: 0, width: W, height: H)); c.interpolationQuality = .high
var items = [[String]](); var cur = [String]()
for s in a[5...] { if s == "+" { items.append(cur); cur = [] } else { cur.append(s) } }; if !cur.isEmpty { items.append(cur) }
for it in items {
  var img = CGImageSourceCreateImageAtIndex(CGImageSourceCreateWithURL(URL(fileURLWithPath: it[0]) as CFURL, nil)!, 0, nil)!
  let v = it[1...].map { CGFloat(Double($0)!) }
  if v.count >= 8 { img = img.cropping(to: CGRect(x: v[4], y: v[5], width: v[6], height: v[7]))! }
  c.draw(img, in: CGRect(x: v[0], y: CGFloat(H) - v[1] - v[3], width: v[2], height: v[3]))
}
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, c.makeImage()!, nil); CGImageDestinationFinalize(d)
