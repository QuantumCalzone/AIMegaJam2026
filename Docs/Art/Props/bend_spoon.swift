// T97: bends the spoon by hand, since no Leonardo take drew the bend my person asked for (a spoon bent at the neck,
// just below the bowl). Takes an upright spoon on a plain background, cuts the handle off at the neck and rotates it
// about the neck's centre, then fills the handle's old place with the background. Run from the repo root:
//   swift Docs/Art/Props/bend_spoon.swift <in.png> <out.png> <neck_y> <pivot_x> <degrees>
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
let neckY = Int(a[3])!, pivotX = Double(a[4])!, deg = Double(a[5])!
let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, nil)!
let img = CGImageSourceCreateImageAtIndex(src, 0, nil)!
let W = img.width, H = img.height
var inp = [UInt8](repeating: 0, count: W * H * 4)
let space = CGColorSpace(name: CGColorSpace.sRGB)!
let info = CGImageAlphaInfo.premultipliedLast.rawValue
CGContext(data: &inp, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4, space: space, bitmapInfo: info)!
    .draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))   // row 0 is the top of the image

func px(_ x: Int, _ y: Int, _ c: Int) -> Double { Double(inp[(y * W + x) * 4 + c]) }
// The background is a vertical gradient: per row, the mean of the 40 px at each edge.
var bg = [[Double]](repeating: [0, 0, 0], count: H)
for y in 0..<H { for c in 0..<3 { var s = 0.0; for x in 0..<40 { s += px(x, y, c) + px(W - 1 - x, y, c) }; bg[y][c] = s / 80 } }
func lum(_ x: Int, _ y: Int) -> Double { (px(x, y, 0) + px(x, y, 1) + px(x, y, 2)) / 3 }
func bgl(_ y: Int) -> Double { (bg[y][0] + bg[y][1] + bg[y][2]) / 3 }
// How much a source pixel is spoon: 0 at a difference of 6 from the background, 1 at 16.
func mask(_ x: Int, _ y: Int) -> Double { min(1, max(0, (abs(lum(x, y) - bgl(y)) - 6) / 10)) }

var out = inp
// Fill the handle's old place: in each row above the neck, paint over the spoon by blending the background just left
// and right of it, so the fill matches the background's own shading (it is not even from side to side).
for y in 0..<neckY {
    var minX = -1, maxX = -1
    for x in 0..<W where mask(x, y) > 0 { if minX < 0 { minX = x }; maxX = x }
    guard minX >= 0 else { continue }
    let l = max(0, minX - 8), r = min(W - 1, maxX + 8)
    for x in l...r {
        let f = Double(x - l) / Double(max(1, r - l)), i = (y * W + x) * 4
        for c in 0..<3 { out[i + c] = UInt8(px(l, y, c) * (1 - f) + px(r, y, c) * f) }
    }
}
let overlap = 6 // source rows below the neck that move with the handle, so the joint has no gap
let t = deg * .pi / 180, py = Double(neckY)
for y in 0..<H {
    for x in 0..<W {
        // Inverse rotation: where in the source did this output pixel come from?
        let dx = Double(x) - pivotX, dy = Double(y) - py
        let sx = Int((pivotX + dx * cos(t) + dy * sin(t)).rounded())
        let sy = Int((py - dx * sin(t) + dy * cos(t)).rounded())
        guard sx >= 0, sx < W, sy >= 0, sy < neckY + overlap else { continue }
        let m = mask(sx, sy)
        guard m > 0 else { continue }
        let i = (y * W + x) * 4
        // Carry the spoon's shading as an offset from its own row's background onto this row's background.
        for c in 0..<3 {
            let base = y < neckY ? Double(out[i + c]) : bg[y][c]   // below the neck, the original pixel is spoon, not background
            let v = base + (px(sx, sy, c) - bg[sy][c])
            out[i + c] = UInt8(max(0, min(255, Double(out[i + c]) * (1 - m) + v * m)))
        }
    }
}
// Round off the joint like a bent knuckle: a disc as wide as the neck, centred on the pivot, shaded from the neck's
// own row so its light and dark sides match the spoon.
var nl = -1, nr = -1
for x in 0..<W where mask(x, neckY + 3) > 0.5 { if nl < 0 { nl = x }; nr = x }
let rad = Double(nr - nl) / 2 + 1
for y in max(0, neckY - Int(rad) - 2)...min(H - 1, neckY + Int(rad) + 2) {
    for x in max(0, Int(pivotX - rad) - 2)...min(W - 1, Int(pivotX + rad) + 2) {
        let d = hypot(Double(x) - pivotX, Double(y) - py)
        let m = min(1, max(0, rad - d))   // one pixel of soft edge
        guard m > 0 else { continue }
        let sxn = min(nr, max(nl, Int(pivotX + (Double(x) - pivotX))))
        let i = (y * W + x) * 4
        for c in 0..<3 { out[i + c] = UInt8(Double(out[i + c]) * (1 - m) + px(sxn, neckY + 3, c) * m) }
    }
}
let octx = CGContext(data: &out, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4, space: space, bitmapInfo: info)!
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, octx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
print("saved \(a[2])")
