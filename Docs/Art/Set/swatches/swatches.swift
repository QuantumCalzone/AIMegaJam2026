// T98: renders one 512 x 512 swatch per set surface: its albedo (the style guide's palette, with the gold
// brightened as my person asked on 2026-11-18) under soft, even light, with clay lumps and faint thumbprints
// from value noise, plus each surface's own pattern (plank seams, velvet pleat sheen, a satin band on the
// gold). They show the color and the clay feel only: the real material is a Substrate slab (see README).
// Run from the repo root:  swift Docs/Art/Set/swatches/swatches.swift Docs/Art/Set/swatches
import CoreGraphics
import Foundation
import ImageIO
import UniformTypeIdentifiers

let outDir = CommandLine.arguments[1]
let N = 512

func hex(_ s: String) -> (Double, Double, Double) {
    let v = Int(s.dropFirst(), radix: 16)!
    return (Double((v >> 16) & 255) / 255, Double((v >> 8) & 255) / 255, Double(v & 255) / 255)
}
func hash(_ x: Int, _ y: Int, _ s: Int) -> Double {
    var h = UInt64(bitPattern: Int64(x &* 374761393 &+ y &* 668265263 &+ s &* 2147483647))
    h = (h ^ (h >> 13)) &* 1274126177; h ^= h >> 16
    return Double(h & 0xFFFF) / 65535
}
func noise(_ x: Double, _ y: Double, _ s: Int) -> Double {   // smooth value noise, 0...1
    let xi = Int(floor(x)), yi = Int(floor(y)); let fx = x - floor(x), fy = y - floor(y)
    let u = fx * fx * (3 - 2 * fx), v = fy * fy * (3 - 2 * fy)
    let a = hash(xi, yi, s), b = hash(xi + 1, yi, s), c = hash(xi, yi + 1, s), d = hash(xi + 1, yi + 1, s)
    return (a + (b - a) * u) * (1 - v) + (c + (d - c) * u) * v
}
func fbm(_ x: Double, _ y: Double, _ s: Int) -> Double { noise(x, y, s) * 0.55 + noise(x * 2.1, y * 2.1, s + 7) * 0.3 + noise(x * 4.3, y * 4.3, s + 13) * 0.15 }

enum Pattern { case plain, planks, velvet, satin }
let swatches: [(String, String, Pattern)] = [
    ("velvet_crimson", "#9E1B22", .velvet),
    ("gold_bright", "#D9B24E", .satin),
    ("wood_dark", "#5A3A22", .plain),
    ("stage_planks", "#A87E4F", .planks),
    ("cream", "#F0E3C4", .plain),
    ("house_black", "#17110F", .plain),
]

for (name, color, pattern) in swatches {
    let base = hex(color)
    var px = [UInt8](repeating: 255, count: N * N * 4)
    for y in 0..<N {
        for x in 0..<N {
            let fx = Double(x), fy = Double(y)
            // Clay: broad lumps, then faint oval thumbprints (dips) scattered by noise.
            var shade = 1 + (fbm(fx / 90, fy / 90, 1) - 0.5) * 0.14
            let t = noise(fx / 22, fy / 22, 5) * 0.7 + noise(fx / 9, fy / 9, 6) * 0.3; if t > 0.74 { shade -= (t - 0.74) * 0.3 }
            var tint = (0.0, 0.0, 0.0)
            switch pattern {
            case .plain: break
            case .planks:
                let row = y / 64, inRow = y % 64
                shade *= 0.93 + hash(row, 0, 3) * 0.12                       // each plank a little different
                if inRow < 3 { shade *= 0.55 }                                 // the seam
                let offset = (row % 2) * 170; if (x + offset) % 340 < 3 { shade *= 0.6 }   // butt joints
                shade *= 1 + (noise(fx / 60, Double(row) * 9 + fy / 300, 9) - 0.5) * 0.1  // soft grain
            case .velvet:
                shade *= 0.82 + 0.28 * pow(0.5 + 0.5 * sin(fx / 512 * .pi * 2 * 3.5), 1.6)  // pleats with a soft sheen
            case .satin:
                let band = exp(-pow((fx + fy * 0.6 - 420) / 120, 2)); shade *= 1 + band * 0.16
                tint = (band * 0.03, band * 0.02, 0)
            }
            let i = (y * N + x) * 4
            px[i] = UInt8(max(0, min(255, (base.0 * shade + tint.0) * 255)))
            px[i + 1] = UInt8(max(0, min(255, (base.1 * shade + tint.1) * 255)))
            px[i + 2] = UInt8(max(0, min(255, (base.2 * shade + tint.2) * 255)))
        }
    }
    let ctx = CGContext(data: &px, width: N, height: N, bitsPerComponent: 8, bytesPerRow: N * 4,
                        space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    let path = "\(outDir)/\(name).png"
    let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: path) as CFURL, UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(dst, ctx.makeImage()!, nil)
    CGImageDestinationFinalize(dst)
    print("saved \(path)")
}
