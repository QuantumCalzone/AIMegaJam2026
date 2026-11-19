// grid.swift: tiles images into a labeled grid PNG. Usage: grid OUT COLS CELLW CELLH BG(hex) file...
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers
import CoreText
let a = CommandLine.arguments
let out = a[1], cols = Int(a[2])!, cw = Int(a[3])!, ch = Int(a[4])!
let bgHex = UInt32(a[5], radix: 16)!
let files = Array(a[6...])
let rows = (files.count + cols - 1) / cols
let pad = 8, W = cols * (cw + pad) + pad, H = rows * (ch + pad) + pad
let cs = CGColorSpace(name: CGColorSpace.sRGB)!
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.setFillColor(red: CGFloat((bgHex >> 16) & 255)/255, green: CGFloat((bgHex >> 8) & 255)/255, blue: CGFloat(bgHex & 255)/255, alpha: 1)
ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))
ctx.interpolationQuality = .high
for (i, f) in files.enumerated() {
  guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: f) as CFURL, nil), let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { continue }
  let c = i % cols, r = i / cols
  let x = pad + c * (cw + pad), y = H - (pad + (r + 1) * (ch + pad)) + pad
  let s = min(CGFloat(cw) / CGFloat(img.width), CGFloat(ch) / CGFloat(img.height))
  let dw = CGFloat(img.width) * s, dh = CGFloat(img.height) * s
  ctx.draw(img, in: CGRect(x: CGFloat(x) + (CGFloat(cw) - dw)/2, y: CGFloat(y) + (CGFloat(ch) - dh)/2, width: dw, height: dh))
  let label = "\(i + 1)" as CFString
  let font = CTFontCreateWithName("Helvetica-Bold" as CFString, 28, nil)
  let attrs = [kCTFontAttributeName: font, kCTForegroundColorAttributeName: CGColor(red: 1, green: 1, blue: 1, alpha: 1)] as CFDictionary
  let line = CTLineCreateWithAttributedString(CFAttributedStringCreate(nil, label, attrs))
  ctx.setFillColor(red: 0, green: 0, blue: 0, alpha: 0.7)
  ctx.fill(CGRect(x: x + 6, y: y + ch - 40, width: 34, height: 34))
  ctx.textPosition = CGPoint(x: x + 14, y: y + ch - 33)
  CTLineDraw(line, ctx)
}
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: out) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dest)
