// fixtex.swift <mode> in.png out.png [args]
//  plum:   recolor a lavender ball to deep plum (keeps value variation)
//  rug:    shift orange/mustard pixels (hue 20-60, sat > .35) to dark old gold
//  seal cx cy r: fill a disc with the median color of its rim ring, soft edge (removes a stamped mark)
//  glow hueLo hueHi satMin valMin: write a white-on-black mask of pixels in that hue range (degrees)
import AppKit

let a = CommandLine.arguments
let mode = a[1]
let src = NSBitmapImageRep(data: try! Data(contentsOf: URL(fileURLWithPath: a[2])))!
let w = src.pixelsWide, h = src.pixelsHigh
let out = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h, bitsPerSample: 8, samplesPerPixel: 4,
                           hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: w * 4, bitsPerPixel: 32)!
func get(_ x: Int, _ y: Int) -> (Double, Double, Double) {
    var p = [Int](repeating: 0, count: 4)
    src.getPixel(&p, atX: x, y: y)
    return (Double(p[0]) / 255, Double(p[1]) / 255, Double(p[2]) / 255)
}
func put(_ x: Int, _ y: Int, _ c: (Double, Double, Double)) {
    var p = [Int(max(0, min(1, c.0)) * 255), Int(max(0, min(1, c.1)) * 255), Int(max(0, min(1, c.2)) * 255), 255]
    out.setPixel(&p, atX: x, y: y)
}
func hsv(_ c: (Double, Double, Double)) -> (Double, Double, Double) {
    let mx = max(c.0, c.1, c.2), mn = min(c.0, c.1, c.2), d = mx - mn
    var hh = 0.0
    if d > 0 {
        if mx == c.0 { hh = 60 * ((c.1 - c.2) / d).truncatingRemainder(dividingBy: 6) }
        else if mx == c.1 { hh = 60 * ((c.2 - c.0) / d + 2) }
        else { hh = 60 * ((c.0 - c.1) / d + 4) }
    }
    if hh < 0 { hh += 360 }
    return (hh, mx == 0 ? 0 : d / mx, mx)
}
func rgb(_ hh: Double, _ s: Double, _ v: Double) -> (Double, Double, Double) {
    let c = v * s, x = c * (1 - abs((hh / 60).truncatingRemainder(dividingBy: 2) - 1)), m = v - c
    let (r, g, b): (Double, Double, Double)
    switch hh { case 0..<60: (r, g, b) = (c, x, 0); case 60..<120: (r, g, b) = (x, c, 0); case 120..<180: (r, g, b) = (0, c, x)
    case 180..<240: (r, g, b) = (0, x, c); case 240..<300: (r, g, b) = (x, 0, c); default: (r, g, b) = (c, 0, x) }
    return (r + m, g + m, b + m)
}
var changed = 0
switch mode {
case "plum":
    for y in 0..<h { for x in 0..<w {
        let c = get(x, y); let (hh, s, v) = hsv(c)
        if s > 0.12 && hh > 240 && hh < 330 { put(x, y, rgb(305, min(0.6, s * 1.1 + 0.08), v * 0.6)); changed += 1 } else { put(x, y, c) }
    } }
case "rug":
    for y in 0..<h { for x in 0..<w {
        let c = get(x, y); let (hh, s, v) = hsv(c)
        if hh >= 20 && hh <= 60 && s > 0.35 && v > 0.35 { put(x, y, rgb(37, 0.74, v * 0.72)); changed += 1 } else { put(x, y, c) }
    } }
case "seal":
    let cx = Double(a[4])!, cy = Double(a[5])!, r = Double(a[6])!
    var ring: [(Double, Double, Double)] = []
    for y in 0..<h { for x in 0..<w {
        let d = hypot(Double(x) - cx, Double(y) - cy)
        if d > r * 0.9 && d < r { ring.append(get(x, y)) }
    } }
    func med(_ k: KeyPath<(Double, Double, Double), Double>) -> Double { let s = ring.map { $0[keyPath: k] }.sorted(); return s[s.count / 2] }
    let m = (med(\.0), med(\.1), med(\.2))
    for y in 0..<h { for x in 0..<w {
        let c = get(x, y); let d = hypot(Double(x) - cx, Double(y) - cy)
        if d < r {
            let t = d < r * 0.85 ? 1.0 : (r - d) / (r * 0.15)
            // a soft dome: a little lighter at the top-left, as the clay catches light
            let shade = 1.0 + 0.08 * (1 - d / r)
            let f = (m.0 * shade, m.1 * shade, m.2 * shade)
            put(x, y, (c.0 + (f.0 - c.0) * t, c.1 + (f.1 - c.1) * t, c.2 + (f.2 - c.2) * t)); changed += 1
        } else { put(x, y, c) }
    } }
case "glow":
    let lo = Double(a[4])!, hi = Double(a[5])!, smin = Double(a[6])!, vmin = Double(a[7])!
    for y in 0..<h { for x in 0..<w {
        let (hh, s, v) = hsv(get(x, y))
        let inRange = lo <= hi ? (hh >= lo && hh <= hi) : (hh >= lo || hh <= hi)
        if inRange && s >= smin && v >= vmin { put(x, y, (1, 1, 1)); changed += 1 } else { put(x, y, (0, 0, 0)) }
    } }
default: fatalError("mode")
}
try! out.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[3]))
print("\(mode): \(changed) of \(w * h) pixels")
