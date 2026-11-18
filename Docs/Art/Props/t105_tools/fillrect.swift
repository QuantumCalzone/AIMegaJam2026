// fillrect in.png out.png x y size r,g,b  (x,y top-left in pixels)
import AppKit
let a = CommandLine.arguments
let src = NSBitmapImageRep(data: try! Data(contentsOf: URL(fileURLWithPath: a[1])))!
let w = src.pixelsWide, h = src.pixelsHigh
let out = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: w * 4, bitsPerPixel: 32)!
let x0 = Int(a[3])!, y0 = Int(a[4])!, sz = Int(a[5])!
let c = a[6].split(separator: ",").map { Int($0)! }
for y in 0..<h { for x in 0..<w {
    var p = [Int](repeating: 0, count: 4)
    if x >= x0 && x < x0 + sz && y >= y0 && y < y0 + sz {
        // faint clay noise so the tray isn't a dead flat color
        let n = Int((sin(Double(x) * 1.7) * cos(Double(y) * 2.3)) * 5)
        p = [c[0] + n, c[1] + n, c[2] + n, 255]
    } else { src.getPixel(&p, atX: x, y: y); p[3] = 255 }
    out.setPixel(&p, atX: x, y: y)
} }
try! out.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2]))
