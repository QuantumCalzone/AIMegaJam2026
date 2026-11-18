// grid out.png cols cellW cellH cropTop file... (each image crops cropTop px of title bar, scaled to the cell)
import AppKit
let a = CommandLine.arguments
let cols = Int(a[2])!, cw = CGFloat(Double(a[3])!), ch = CGFloat(Double(a[4])!), top = CGFloat(Double(a[5])!)
let files = Array(a[6...]); let rows = (files.count + cols - 1) / cols
let img = NSImage(size: NSSize(width: cw * CGFloat(cols), height: ch * CGFloat(rows)))
img.lockFocus()
NSColor.black.setFill(); NSRect(x: 0, y: 0, width: img.size.width, height: img.size.height).fill()
for (i, f) in files.enumerated() {
    guard let im = NSImage(contentsOfFile: f) else { continue }
    let r = i / cols, c = i % cols
    let src = NSRect(x: 0, y: 0, width: im.size.width, height: im.size.height - top * im.size.height / 968)
    im.draw(in: NSRect(x: CGFloat(c) * cw, y: img.size.height - CGFloat(r + 1) * ch, width: cw, height: ch), from: src, operation: .sourceOver, fraction: 1)
    let lab = (f as NSString).lastPathComponent.replacingOccurrences(of: "png_", with: "").replacingOccurrences(of: ".png", with: "")
    (lab as NSString).draw(at: NSPoint(x: CGFloat(c) * cw + 8, y: img.size.height - CGFloat(r) * ch - 26), withAttributes: [.font: NSFont.boldSystemFont(ofSize: 18), .foregroundColor: NSColor.yellow, .backgroundColor: NSColor.black])
}
img.unlockFocus()
let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
try! rep.representation(using: .jpeg, properties: [.compressionFactor: 0.85])!.write(to: URL(fileURLWithPath: a[1]))
