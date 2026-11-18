// Renders an OBJ (Z up) offscreen: turntable.png (4 views in a row) and thumbnail.png (the first view).
// usage: swift render.swift model.obj turntable.png thumbnail.png [yawOffsetDegrees]
import AppKit
import SceneKit
import ModelIO
import SceneKit.ModelIO

let args = CommandLine.arguments
let objURL = URL(fileURLWithPath: args[1])
let yaw0 = args.count > 4 ? CGFloat(Double(args[4])!) * .pi / 180 : 0
let asset = MDLAsset(url: objURL)
asset.loadTextures()
let scene = SCNScene()
let holder = SCNNode()
let model = SCNNode(mdlObject: asset.object(at: 0))
for i in 1..<asset.count { model.addChildNode(SCNNode(mdlObject: asset.object(at: i))) }
model.enumerateHierarchy { n, _ in
    n.geometry?.materials.forEach { m in
        m.lightingModel = .lambert
        m.isDoubleSided = true
    }
}
holder.addChildNode(model)
model.eulerAngles = SCNVector3(-CGFloat.pi / 2, 0, 0)  // Z up -> Y up
scene.rootNode.addChildNode(holder)
let (mn, mx) = holder.boundingBox
let center = SCNVector3((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, (mn.z + mx.z) / 2)
let radius = max(mx.x - mn.x, mx.y - mn.y, mx.z - mn.z) * 0.95
model.position = SCNVector3(-center.x, -center.y, -center.z)

let amb = SCNNode(); amb.light = SCNLight(); amb.light!.type = .ambient; amb.light!.intensity = 450
scene.rootNode.addChildNode(amb)
let key = SCNNode(); key.light = SCNLight(); key.light!.type = .directional; key.light!.intensity = 700
key.eulerAngles = SCNVector3(-0.7, 0.5, 0)
scene.rootNode.addChildNode(key)
scene.background.contents = NSColor(calibratedWhite: 0.82, alpha: 1)

let cam = SCNNode(); cam.camera = SCNCamera()
cam.camera!.usesOrthographicProjection = true
cam.camera!.orthographicScale = Double(radius) * 0.62
cam.camera!.zNear = 0.01; cam.camera!.zFar = 100
scene.rootNode.addChildNode(cam)

let size = 512
let renderer = SCNRenderer(device: MTLCreateSystemDefaultDevice(), options: nil)
renderer.scene = scene
renderer.pointOfView = cam
var images: [NSImage] = []
for i in 0..<4 {
    let a = yaw0 + CGFloat(i) * .pi / 2
    let d = Double(radius) * 3
    let el = 0.35
    cam.position = SCNVector3(CGFloat(d * cos(el)) * sin(a), CGFloat(d * sin(el)), CGFloat(d * cos(el)) * cos(a))
    cam.look(at: SCNVector3(0, 0, 0))
    images.append(renderer.snapshot(atTime: 0, with: CGSize(width: size, height: size), antialiasingMode: .multisampling4X))
}
func save(_ img: NSImage, _ path: String) {
    let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
    try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: path))
}
let strip = NSImage(size: NSSize(width: size * 4, height: size))
strip.lockFocus()
for (i, im) in images.enumerated() { im.draw(in: NSRect(x: i * size, y: 0, width: size, height: size)) }
strip.unlockFocus()
save(strip, args[2])
save(images[0], args[3])
