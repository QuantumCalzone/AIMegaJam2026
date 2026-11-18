// sheet.swift out.png title "label|view.png|turntable.png" ...  -> one row per prop: view, then the 4 turntable views
import AppKit
let a = CommandLine.arguments
let cell: CGFloat = 300, labelH: CGFloat = 34, titleH: CGFloat = 50
let rows = Array(a[3...])
let W = cell * 5, H = titleH + CGFloat(rows.count) * (cell + labelH)
let img = NSImage(size: NSSize(width: W, height: H))
img.lockFocus()
NSColor(calibratedRed: 0.16, green: 0.13, blue: 0.14, alpha: 1).setFill(); NSRect(x: 0, y: 0, width: W, height: H).fill()
let attrs: [NSAttributedString.Key: Any] = [.font: NSFont.boldSystemFont(ofSize: 22), .foregroundColor: NSColor(calibratedRed: 1, green: 0.95, blue: 0.85, alpha: 1)]
(a[2] as NSString).draw(at: NSPoint(x: 14, y: H - titleH + 12), withAttributes: attrs)
for (i, r) in rows.enumerated() {
    let p = r.split(separator: "|").map(String.init)
    let top = H - titleH - CGFloat(i) * (cell + labelH)
    (p[0] as NSString).draw(at: NSPoint(x: 14, y: top - labelH + 6), withAttributes: attrs)
    let y = top - labelH - cell
    if let v = NSImage(contentsOfFile: p[1]) { v.draw(in: NSRect(x: 0, y: y, width: cell, height: cell)) }
    if let t = NSImage(contentsOfFile: p[2]) {
        let s = t.size.height
        for k in 0..<4 {
            t.draw(in: NSRect(x: cell * CGFloat(k + 1), y: y, width: cell, height: cell), from: NSRect(x: CGFloat(k) * s, y: 0, width: s, height: s), operation: .sourceOver, fraction: 1)
        }
    }
}
img.unlockFocus()
let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[1]))
