"""Read, edit and write binary FBX 7.x (stdlib only). Keeps every node and property type; arrays are
re-written zlib-compressed. Edits used by T105:
  seal  in.fbx out.fbx cx cz r [y_front]   smooth (Laplacian) the front-facing vertices inside a disc in the
                                            x/z plane, to erase a stamped relief
  tray  in.fbx out.fbx tex_in.png tex_out.png gray_rgb  add a flat round tray under the model, its UVs in an
                                            empty 16x16 texel block of the diffuse map painted gray
  tex   in.fbx out.fbx name.png new.png     replace an embedded texture (Video Content) by file name
"""
import io, math, struct, sys, zlib
from collections import defaultdict

ORIG = {}
ARR = {"f": "f", "d": "d", "l": "q", "i": "i", "b": "?"}
SIMPLE = {"Y": "<h", "C": "<?", "I": "<i", "F": "<f", "D": "<d", "L": "<q"}


class Node:
    def __init__(self, name, props, kids):
        self.name, self.props, self.kids = name, props, kids  # props: list of (type, value)

    def child(self, name):
        return next((k for k in self.kids if k.name == name), None)

    def find(self, name):
        if self.name == name:
            yield self
        for k in self.kids:
            yield from k.find(name)


def read(path):
    data = open(path, "rb").read()
    ver = struct.unpack_from("<I", data, 23)[0]
    wide = ver >= 7500

    def prop(p):
        t = chr(data[p]); p += 1
        if t in SIMPLE:
            v = struct.unpack_from(SIMPLE[t], data, p)[0]
            if t == "C":
                v = data[p:p + 1]  # keep the stored byte ('T'/'F' or 0/1) as it was
            return (t, v), p + struct.calcsize(SIMPLE[t])
        if t in ARR:
            n, enc, clen = struct.unpack_from("<III", data, p); p += 12
            stored = data[p - 12:p + clen]
            raw = data[p:p + clen]; p += clen
            if enc == 1:
                raw = zlib.decompress(raw)
            vals = list(struct.unpack("<%d%s" % (n, ARR[t]), raw))
            ORIG[id(vals)] = (stored, zlib.crc32(raw), n)
            return (t, vals), p
        if t in "SR":
            n = struct.unpack_from("<I", data, p)[0]; p += 4
            return (t, data[p:p + n]), p + n
        raise ValueError(t)

    def node(p):
        if wide:
            end, nprops, _ = struct.unpack_from("<QQQ", data, p); p += 24
        else:
            end, nprops, _ = struct.unpack_from("<III", data, p); p += 12
        if end == 0:
            return None, p
        nl = data[p]; p += 1
        name = data[p:p + nl].decode(); p += nl
        props = []
        for _ in range(nprops):
            v, p = prop(p)
            props.append(v)
        kids = []
        while p < end:
            k, p = node(p)
            if k is None:
                break
            kids.append(k)
        return Node(name, props, kids), end

    roots, pos = [], 27
    while pos < len(data) - 13:
        n, pos = node(pos)
        if n is None:
            pos += 1  # the null record's name-length byte
            break
        roots.append(n)
    footer = data[pos:]
    return data[:27], ver, roots, footer


def write(path, head, ver, roots, footer):
    wide = ver >= 7500
    null = b"\0" * (25 if wide else 13)

    def enc_prop(t, v):
        if t == "C":
            return t.encode() + (v if isinstance(v, bytes) else bytes([1 if v else 0]))
        if t in SIMPLE:
            return t.encode() + struct.pack(SIMPLE[t], v)
        if t in ARR:
            raw = struct.pack("<%d%s" % (len(v), ARR[t]), *v)
            o = ORIG.get(id(v))
            if o and o[2] == len(v) and o[1] == zlib.crc32(raw):
                return t.encode() + o[0]
            comp = zlib.compress(raw)
            return t.encode() + struct.pack("<III", len(v), 1, len(comp)) + comp
        return t.encode() + struct.pack("<I", len(v)) + v

    def enc_node(n, offset):
        pb = b"".join(enc_prop(t, v) for t, v in n.props)
        nm = n.name.encode()
        hdr = (24 if wide else 12) + 1 + len(nm)
        body = io.BytesIO()
        cur = offset + hdr + len(pb)
        for k in n.kids:
            kb = enc_node(k, cur)
            body.write(kb); cur += len(kb)
        if n.kids or not n.props:
            body.write(null); cur += len(null)
        end = cur
        h = struct.pack("<QQQ" if wide else "<III", end, len(n.props), len(pb))
        return h + bytes([len(nm)]) + nm + pb + body.getvalue()

    out = io.BytesIO(); out.write(head)
    cur = len(head)
    for r in roots:
        b = enc_node(r, cur); out.write(b); cur += len(b)
    out.write(null)
    out.write(footer)  # Rodin's footer, verbatim (id, padding, version, magic)
    open(path, "wb").write(out.getvalue())


def geom(roots):
    for r in roots:
        for g in r.find("Geometry"):
            if g.child("Vertices"):
                return g


def polys(pvi):
    out, cur = [], []
    for i, idx in enumerate(pvi):
        cur.append((~idx if idx < 0 else idx, i))
        if idx < 0:
            out.append(cur); cur = []
    return out


def cmd_seal(a):
    head, ver, roots, footer = read(a[0])
    cx, cz, r = map(float, a[2:5])
    g = geom(roots)
    V = g.child("Vertices").props[0][1]
    n = len(V) // 3
    P = polys(g.child("PolygonVertexIndex").props[0][1])
    nb = defaultdict(set)
    for poly in P:
        ids = [v for v, _ in poly]
        for i in range(len(ids)):
            nb[ids[i]].add(ids[i - 1]); nb[ids[i]].add(ids[(i + 1) % len(ids)])
    # front-facing = the nearest surface along -y inside the disc: keep vertices within 0.04 of the min y per cell
    inside = [i for i in range(n) if math.hypot(V[3 * i] - cx, V[3 * i + 2] - cz) < r]
    ymin = min(V[3 * i + 1] for i in inside)
    sel = [i for i in inside if V[3 * i + 1] < ymin + float(a[5] if len(a) > 5 else 0.05)]
    sset = set(sel)
    for _ in range(40):
        newv = {}
        for i in sel:
            ns = [j for j in nb[i]]
            w = 1 - min(1, math.hypot(V[3 * i] - cx, V[3 * i + 2] - cz) / r) ** 4  # fade at the rim
            for c in range(3):
                avg = sum(V[3 * j + c] for j in ns) / len(ns)
                newv[(i, c)] = V[3 * i + c] + (avg - V[3 * i + c]) * 0.6 * w
        for (i, c), val in newv.items():
            V[3 * i + c] = val
    # drop the baked normals' detail: Unreal recomputes them when the import asks; keep arrays valid
    print("smoothed", len(sel), "vertices; front y", round(ymin, 3))
    write(a[1], head, ver, roots, footer)


def cmd_tex(a):
    head, ver, roots, footer = read(a[0])
    name, new = a[2], open(a[3], "rb").read()
    hits = 0
    for r in roots:
        for v in r.find("Video"):
            fn = v.child("RelativeFilename") or v.child("Filename")
            if fn and fn.props[0][1].decode().endswith(name):
                c = v.child("Content")
                c.props[0] = ("R", new); hits += 1
    print("replaced", hits, "embedded", name)
    write(a[1], head, ver, roots, footer)


def cmd_tray(a):
    """Adds a tray: a flat cylinder under the model's lowest point, 1.25x the model's x/y extent."""
    head, ver, roots, footer = read(a[0])
    tex_in, tex_out, gray = a[2], a[3], a[4]
    g = geom(roots)
    V = g.child("Vertices").props[0][1]
    pvi = g.child("PolygonVertexIndex").props[0][1]
    ln = g.child("LayerElementNormal"); N = ln.child("Normals").props[0][1]; NI = ln.child("NormalsIndex").props[0][1]
    lu = g.child("LayerElementUV"); UV = lu.child("UV").props[0][1]; UI = lu.child("UVIndex").props[0][1]
    xs, ys, zs = V[0::3], V[1::3], V[2::3]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    rad = max(max(xs) - min(xs), max(ys) - min(ys)) / 2 * float(a[5] if len(a) > 5 else 1.1)
    z0 = min(zs); th = rad * 0.07
    zt, zb = z0 + th * 0.4, z0 - th * 0.6  # the pile sinks a little into the tray
    rim_h, rim_w = th * 0.9, rad * 0.06
    # find an empty 16x16 block on a 2048 map by rasterizing UV triangle bounding boxes on a 128 grid
    occ = [[False] * 128 for _ in range(128)]
    P = polys(pvi)
    for poly in P:
        us = [UV[2 * UI[i]] for _, i in poly]; vs = [UV[2 * UI[i] + 1] for _, i in poly]
        for gx in range(int(min(us) * 128), min(127, int(max(us) * 128)) + 1):
            for gy in range(int(min(vs) * 128), min(127, int(max(vs) * 128)) + 1):
                occ[gy][gx] = True
    cell = next(((gx, gy) for gy in range(128) for gx in range(128) if not occ[gy][gx]
                 and all(not occ[yy][xx] for yy in range(max(0, gy - 1), min(128, gy + 2)) for xx in range(max(0, gx - 1), min(128, gx + 2)))), None)
    assert cell, "no empty texel block"
    u0, v0 = (cell[0] + 0.5) / 128, (cell[1] + 0.5) / 128
    print("tray uv cell", cell, "-> texel", int(u0 * 2048), int((1 - v0) * 2048))
    # geometry: rings (radius, z) from center top to under side
    seg = 48
    prof = [(0, zt), (rad - rim_w, zt), (rad - rim_w * 0.3, zt + rim_h), (rad, zt + rim_h * 0.6), (rad, zb), (rad * 0.9, zb - th * 0.2), (0, zb - th * 0.2)]
    base = len(V) // 3
    ring_ids = []
    for (rr, zz) in prof:
        ids = []
        for s in range(seg if rr > 0 else 1):
            ang = 2 * math.pi * s / seg
            V += [cx + rr * math.cos(ang), cy + rr * math.sin(ang), zz]
            ids.append(base); base += 1
        ring_ids.append(ids)
    uvi = len(UV) // 2; UV += [u0, v0]
    newpolys = []
    for k in range(len(prof) - 1):
        A, B = ring_ids[k], ring_ids[k + 1]
        for s in range(seg):
            a0, a1 = A[s % len(A)], A[(s + 1) % len(A)]
            b0, b1 = B[s % len(B)], B[(s + 1) % len(B)]
            if len(A) == 1:
                newpolys.append([a0, b1, b0])
            elif len(B) == 1:
                newpolys.append([a0, a1, b0])
            else:
                newpolys.append([a0, a1, b1, b0])
    newpolys = [list(reversed(q)) for q in newpolys]
    for poly in newpolys:
        # face normal (flip so it points away from the axis/up or down)
        p = [V[3 * i:3 * i + 3] for i in poly]
        e1 = [p[1][c] - p[0][c] for c in range(3)]; e2 = [p[2][c] - p[0][c] for c in range(3)]
        nrm = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]]
        L = math.sqrt(sum(c * c for c in nrm)) or 1
        nrm = [c / L for c in nrm]
        ni = len(N) // 3; N += nrm
        for j, vi in enumerate(poly):
            pvi.append(~vi if j == len(poly) - 1 else vi)
            NI.append(ni); UI.append(uvi)
    # Edges node is optional; drop it so it can't disagree with the new polygons
    g.kids = [k for k in g.kids if k.name != "Edges"]
    # paint the gray block (with a margin) into the diffuse map
    write(a[1], head, ver, roots, footer)
    import subprocess
    gx0, gy0 = int(u0 * 2048) - 24, int((1 - v0) * 2048) - 24
    subprocess.run([sys.executable, __file__, "_paint", tex_in, tex_out, str(gx0), str(gy0), "48", gray], check=True)


if __name__ == "__main__":
    cmd, a = sys.argv[1], sys.argv[2:]
    if cmd == "_paint":
        # delegate to the Swift fill tool
        import subprocess, os
        here = os.path.dirname(os.path.abspath(__file__))
        subprocess.run([os.path.join(here, "fillrect"), *a], check=True)
    else:
        {"seal": cmd_seal, "tray": cmd_tray, "tex": cmd_tex}[cmd](a)
