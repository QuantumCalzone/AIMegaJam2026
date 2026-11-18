// T108's swatch sheet: Meta's mustard candidates beside the other seats, the UI's gold, Anthropic's orange
// and the audience's mustard, as chat lines, name tags and clay bodies on the stage.
// Run from the repo root:  swift Docs/Art/Seat/swatch.swift <out.png> NAME=#RRGGBB [NAME=#RRGGBB ...]
import CoreGraphics
import CoreText
import Foundation
import ImageIO
import UniformTypeIdentifiers

func hex(_ s: String) -> CGColor {
    let v = Int(s.replacingOccurrences(of: "#", with: ""), radix: 16)!
    return CGColor(srgbRed: CGFloat((v >> 16) & 255) / 255, green: CGFloat((v >> 8) & 255) / 255,
                   blue: CGFloat(v & 255) / 255, alpha: 1)
}
func scale(_ c: CGColor, _ k: CGFloat, toward w: CGFloat = 0) -> CGColor {
    let p = c.components!
    return CGColor(srgbRed: min(1, p[0] * k + w), green: min(1, p[1] * k + w), blue: min(1, p[2] * k + w), alpha: 1)
}

let args = Array(CommandLine.arguments.dropFirst())
guard args.count >= 2 else { fatalError("usage: swatch.swift <out.png> NAME=#RRGGBB ...") }
let cands = args[1...].map { a -> (String, String) in let p = a.components(separatedBy: "="); return (p[0], p[1]) }

let ink = hex("#161225"), white = hex("#FFFFFF"), quiet = hex("#C9C3DA"), gold = hex("#F2C14E")
let oldGold = hex("#A9873A"), setGold = hex("#D9B24E"), paper = hex("#F5E9CF"), paperText = hex("#2B1D12")
let wood = hex("#5A3A22"), planks = hex("#A87E4F"), audMustard = hex("#C9A43F"), curtain = hex("#9E1B22")
let seats: [(String, String)] = [("OpenAI", "#A8CCFF"), ("Anthropic", "#E8894A"), ("SpaceXAI", "#D8F04A"), ("Meta", ""), ("You", "#3FD0C9")]

let colW = 600, gap = 24, H = 1060
let W = gap + cands.count * (colW + gap)
let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                    space: CGColorSpace(name: CGColorSpace.sRGB)!, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
// Flip so y grows downward; text is drawn with its own flip.
ctx.translateBy(x: 0, y: CGFloat(H)); ctx.scaleBy(x: 1, y: -1)
ctx.setFillColor(hex("#0B0912")); ctx.fill(CGRect(x: 0, y: 0, width: W, height: H))

func text(_ s: String, _ x: CGFloat, _ y: CGFloat, _ size: CGFloat, _ c: CGColor, bold: Bool = false) -> CGFloat {
    let f = CTFontCreateWithName((bold ? "Helvetica-Bold" : "Helvetica") as CFString, size, nil)
    let a = NSAttributedString(string: s, attributes: [kCTFontAttributeName as NSAttributedString.Key: f,
                                                       kCTForegroundColorAttributeName as NSAttributedString.Key: c])
    let line = CTLineCreateWithAttributedString(a)
    ctx.saveGState(); ctx.translateBy(x: x, y: y); ctx.scaleBy(x: 1, y: -1)
    ctx.textPosition = .zero; CTLineDraw(line, ctx); ctx.restoreGState()
    return CGFloat(CTLineGetTypographicBounds(line, nil, nil, nil))
}
func rrect(_ r: CGRect, _ rad: CGFloat, fill: CGColor, stroke: CGColor? = nil, lw: CGFloat = 0) {
    let p = CGPath(roundedRect: r, cornerWidth: rad, cornerHeight: rad, transform: nil)
    ctx.addPath(p); ctx.setFillColor(fill); ctx.fillPath()
    if let s = stroke { ctx.addPath(p); ctx.setStrokeColor(s); ctx.setLineWidth(lw); ctx.strokePath() }
}
// A clay body: a lit egg with a warm key light from the upper left.
func clay(_ cx: CGFloat, _ cy: CGFloat, _ rw: CGFloat, _ rh: CGFloat, _ c: CGColor) {
    ctx.saveGState()
    ctx.addEllipse(in: CGRect(x: cx - rw, y: cy - rh, width: 2 * rw, height: 2 * rh)); ctx.clip()
    let g = CGGradient(colorsSpace: CGColorSpace(name: CGColorSpace.sRGB), colors: [scale(c, 1.08, toward: 0.06), c, scale(c, 0.62), scale(c, 0.42)] as CFArray, locations: [0, 0.35, 0.8, 1])!
    ctx.drawRadialGradient(g, startCenter: CGPoint(x: cx - rw * 0.35, y: cy - rh * 0.4), startRadius: 0,
                           endCenter: CGPoint(x: cx, y: cy), endRadius: max(rw, rh) * 1.15, options: [.drawsAfterEndLocation])
    ctx.restoreGState()
}

for (i, (name, hx)) in cands.enumerated() {
    let x0 = CGFloat(gap + i * (colW + gap)), cw = CGFloat(colW)
    let meta = hex(hx)
    _ = text("\(name)  \(hx)", x0, 44, 30, white, bold: true)

    // The chat panel: ink with an old-gold trim, a gold YOUR MOVE line, five chat lines, a gold Action! button.
    let panel = CGRect(x: x0, y: 64, width: cw, height: 420)
    rrect(panel, 16, fill: ink, stroke: oldGold, lw: 2)
    _ = text("YOUR MOVE", x0 + 16, 100, 22, gold, bold: true)
    _ = text("  pick an action and press Action!", x0 + 152, 100, 18, quiet)
    var y: CGFloat = 126
    let lines = ["We open on a diner at midnight.", "Careful: the milkshake is evidence.", "I SAID THE BURGER IS A SPACESHIP!", "As an assistant, I agree. Strongly.", "Uh, me too. Totally a robot thing."]
    for (j, (seat, sh)) in seats.enumerated() {
        let c = seat == "Meta" ? meta : hex(sh)
        ctx.setFillColor(c); ctx.fill(CGRect(x: x0 + 16, y: y, width: 6, height: 46))
        _ = text(seat, x0 + 32, y + 18, 18, c, bold: true)
        _ = text(lines[j], x0 + 32, y + 40, 17, white)
        y += 58
    }
    rrect(CGRect(x: x0 + cw - 176, y: 64 + 420 - 64, width: 160, height: 48), 12, fill: gold, stroke: scale(gold, 1.0, toward: 0.1), lw: 3)
    _ = text("Action!", x0 + cw - 140, 64 + 420 - 32, 24, ink, bold: true)

    // Name tags (seat fill, ink text) and a ballot ticket on paper.
    y = 508
    var tx = x0
    for (seat, sh) in seats {
        let c = seat == "Meta" ? meta : hex(sh)
        let w: CGFloat = seat.count > 6 ? 116 : 98
        rrect(CGRect(x: tx, y: y, width: w, height: 34), 10, fill: c)
        _ = text(seat, tx + 10, y + 23, 17, ink, bold: true)
        tx += w + 8
    }
    rrect(CGRect(x: x0, y: 556, width: cw, height: 58), 16, fill: paper, stroke: paperText, lw: 3)
    ctx.setFillColor(meta); ctx.fill(CGRect(x: x0 + 16, y: 566, width: 6, height: 38))
    _ = text("CUT Meta?", x0 + 32, 592, 22, paperText, bold: true)
    rrect(CGRect(x: x0 + 220, y: 566, width: 92, height: 38), 10, fill: meta)
    _ = text("Meta", x0 + 240, 592, 18, ink, bold: true)
    rrect(CGRect(x: x0 + cw - 132, y: 566, width: 116, height: 38), 12, fill: gold)
    _ = text("Vote", x0 + cw - 98, 592, 20, ink, bold: true)

    // The stage: gold proscenium trim, curtains, planks, the five clay bodies in seat order, an audience bot in front.
    let st = CGRect(x: x0, y: 636, width: cw, height: 400)
    ctx.setFillColor(wood); ctx.fill(st)
    ctx.setFillColor(curtain); ctx.fill(CGRect(x: x0, y: 636, width: 48, height: 300)); ctx.fill(CGRect(x: x0 + cw - 48, y: 636, width: 48, height: 300))
    ctx.setFillColor(setGold); ctx.fill(CGRect(x: x0, y: 636, width: cw, height: 14))
    ctx.fill(CGRect(x: x0 + 48, y: 650, width: 8, height: 286)); ctx.fill(CGRect(x: x0 + cw - 56, y: 650, width: 8, height: 286))
    ctx.setFillColor(planks); ctx.fill(CGRect(x: x0, y: 860, width: cw, height: 176))
    ctx.setFillColor(scale(planks, 0.8)); for k in 0..<5 { ctx.fill(CGRect(x: x0, y: 860 + CGFloat(k) * 36, width: cw, height: 2)) }
    for (j, (seat, sh)) in seats.enumerated() {
        let c = seat == "Meta" ? meta : hex(sh)
        let cx = x0 + 90 + CGFloat(j) * 105
        clay(cx, 820, 38, 64, c)
        clay(cx, 735, 30, 30, seat == "Meta" ? hex("#C9CCD2") : (seat == "You" ? c : c))
        if seat == "Meta" { // black top band over the mustard: black and mustard
            ctx.saveGState(); ctx.addEllipse(in: CGRect(x: cx - 38, y: 756, width: 76, height: 128)); ctx.clip()
            ctx.setFillColor(hex("#151515")); ctx.fill(CGRect(x: cx - 38, y: 756, width: 76, height: 26)); ctx.restoreGState()
            ctx.setFillColor(setGold); ctx.fill(CGRect(x: cx - 14, y: 768, width: 28, height: 5)) // its gold chain
        }
        _ = text(seat, cx - 34, 912, 14, white, bold: true)
    }
    // Footlight hoods (gold) and an audience bot in mustard in the stalls.
    ctx.setFillColor(setGold); for k in 0..<6 { ctx.fill(CGRect(x: x0 + 40 + CGFloat(k) * 100, y: 940, width: 30, height: 10)) }
    ctx.setFillColor(hex("#17110F")); ctx.fill(CGRect(x: x0, y: 960, width: cw, height: 76))
    clay(x0 + 120, 1010, 30, 34, audMustard); clay(x0 + 120, 965, 22, 20, audMustard)
    clay(x0 + 230, 1010, 30, 34, hex("#7E5A7A")); clay(x0 + 230, 965, 22, 20, hex("#7E5A7A"))
    clay(x0 + 340, 1010, 30, 34, hex("#C98B8B")); clay(x0 + 340, 965, 22, 20, hex("#C98B8B"))
    _ = text("audience mustard #C9A43F", x0 + 380, 1018, 15, quiet)
}
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: args[0]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, ctx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
