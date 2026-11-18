// T95: a free, local recolor of one hue band (SpaceXAI's olive to its seat lime), with no generation pass.
// Pixels whose hue is near `hue` and whose saturation is above `minSat` get their value scaled by `gain`, their
// saturation set toward `sat`, and their hue moved to `toHue`, with a soft falloff at the band's edges, so shading
// and thumbprints stay. Run from the repo root:
//   swift Docs/Art/Cast/recolor.swift <in.png> <out.png> <hue> <width> <minSat> <toHue> <sat> <gain>
//   swift Docs/Art/Cast/recolor.swift <in.png> sample x,y x,y ...      (prints RGB and HSV at points)
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let a = Array(CommandLine.arguments.dropFirst())
guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: a[0]) as CFURL, nil),
      let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("can't read \(a[0])") }
let W = img.width, H = img.height
var px = [UInt8](repeating: 0, count: W * H * 4)
let ctx = CGContext(data: &px, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W * 4,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))

func hsv(_ r: Double, _ g: Double, _ b: Double) -> (Double, Double, Double) {
    let mx = max(r, g, b), mn = min(r, g, b), d = mx - mn
    var h = 0.0
    if d > 0 {
        if mx == r { h = 60 * ((g - b) / d).truncatingRemainder(dividingBy: 6) }
        else if mx == g { h = 60 * ((b - r) / d + 2) }
        else { h = 60 * ((r - g) / d + 4) }
    }
    if h < 0 { h += 360 }
    return (h, mx == 0 ? 0 : d / mx, mx)
}
func rgb(_ h: Double, _ s: Double, _ v: Double) -> (Double, Double, Double) {
    let c = v * s, x = c * (1 - abs((h / 60).truncatingRemainder(dividingBy: 2) - 1)), m = v - c
    let (r, g, b): (Double, Double, Double) = h < 60 ? (c, x, 0) : h < 120 ? (x, c, 0) : h < 180 ? (0, c, x) :
        h < 240 ? (0, x, c) : h < 300 ? (x, 0, c) : (c, 0, x)
    return (r + m, g + m, b + m)
}

if a[1] == "sample" {
    for p in a[2...] {
        let xy = p.split(separator: ",").map { Int($0)! }
        let i = (xy[1] * W + xy[0]) * 4   // CG rows run top to bottom in memory
        let (r, g, b) = (Double(px[i]) / 255, Double(px[i + 1]) / 255, Double(px[i + 2]) / 255)
        let (h, s, v) = hsv(r, g, b)
        print(p, px[i], px[i + 1], px[i + 2], String(format: "h %.0f s %.2f v %.2f", h, s, v))
    }
    exit(0)
}
let hue = Double(a[2])!, width = Double(a[3])!, minSat = Double(a[4])!, toHue = Double(a[5])!, sat = Double(a[6])!, gain = Double(a[7])!
for i in stride(from: 0, to: px.count, by: 4) {
    let (r, g, b) = (Double(px[i]) / 255, Double(px[i + 1]) / 255, Double(px[i + 2]) / 255)
    let (h, s, v) = hsv(r, g, b)
    let dh = abs(h - hue)
    let wh = max(0, min(1, (width - dh) / (width * 0.35)))        // 1 inside the band, fades over its outer 35%
    let ws = max(0, min(1, (s - minSat) / 0.12))                  // fades in above minSat
    let w = wh * ws
    if w <= 0 { continue }
    let nh = h + (toHue - h) * w, ns = s + (sat - s) * w * 0.8, nv = min(1, v * (1 + (gain - 1) * w))
    let (nr, ng, nb) = rgb(nh, ns, nv)
    px[i] = UInt8(max(0, min(255, nr * 255))); px[i + 1] = UInt8(max(0, min(255, ng * 255))); px[i + 2] = UInt8(max(0, min(255, nb * 255)))
}
let out = ctx.makeImage()!
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[1]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, out, nil)
CGImageDestinationFinalize(dst)
