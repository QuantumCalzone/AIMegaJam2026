"""Binary FBX -> OBJ (positions, UVs) plus mesh stats. Stdlib only.
usage: fbx2obj.py model.fbx out.obj texture.png stats.json"""
import json, struct, sys, zlib
from collections import defaultdict


def read_fbx(path):
    data = open(path, "rb").read()
    assert data[:20] == b"Kaydara FBX Binary  ", "not a binary FBX"
    ver = struct.unpack_from("<I", data, 23)[0]
    wide = ver >= 7500
    pos = 27

    def prop(p):
        t = chr(data[p]); p += 1
        simple = {"Y": "<h", "C": "<?", "I": "<i", "F": "<f", "D": "<d", "L": "<q"}
        if t in simple:
            v = struct.unpack_from(simple[t], data, p)[0]
            return v, p + struct.calcsize(simple[t])
        if t in "fdlib":
            n, enc, clen = struct.unpack_from("<III", data, p); p += 12
            raw = data[p:p + clen]; p += clen
            if enc == 1:
                raw = zlib.decompress(raw)
            fmt = {"f": "f", "d": "d", "l": "q", "i": "i", "b": "?"}[t]
            return list(struct.unpack("<%d%s" % (n, fmt), raw)), p
        if t in "SR":
            n = struct.unpack_from("<I", data, p)[0]; p += 4
            v = data[p:p + n]; p += n
            return (v.decode("utf-8", "replace") if t == "S" else v), p
        raise ValueError("prop type %r" % t)

    def node(p):
        if wide:
            end, nprops, plen = struct.unpack_from("<QQQ", data, p); p += 24
        else:
            end, nprops, plen = struct.unpack_from("<III", data, p); p += 12
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
        return {"name": name, "props": props, "kids": kids}, end

    roots = []
    while pos < len(data) - 13:
        n, pos = node(pos)
        if n is None:
            break
        roots.append(n)
    return roots


def find_all(nodes, name):
    for n in nodes:
        if n["name"] == name:
            yield n
        yield from find_all(n["kids"], name)


def child(n, name):
    for k in n["kids"]:
        if k["name"] == name:
            return k
    return None


def main(fbx, out_obj, tex, stats_path):
    roots = read_fbx(fbx)
    up = None
    for p in find_all(roots, "P"):
        if p["props"] and p["props"][0] in ("UpAxis", "UnitScaleFactor"):
            up = up or {}
            up[p["props"][0]] = p["props"][-1]
    lines = ["mtllib model.mtl", "usemtl m"]
    vbase = tbase = 0
    tris = 0
    allv = []
    edges = defaultdict(int)
    meshes = 0
    for g in find_all(roots, "Geometry"):
        vn = child(g, "Vertices")
        if vn is None:
            continue
        meshes += 1
        V = vn["props"][0]
        P = child(g, "PolygonVertexIndex")["props"][0]
        verts = [tuple(V[i:i + 3]) for i in range(0, len(V), 3)]
        allv += verts
        uvn = child(g, "LayerElementUV")
        UV, UVI, mapping = [], None, "ByPolygonVertex"
        if uvn is not None:
            UV = child(uvn, "UV")["props"][0]
            ui = child(uvn, "UVIndex")
            UVI = ui["props"][0] if ui else None
            mapping = child(uvn, "MappingInformationType")["props"][0]
        for v in verts:
            lines.append("v %.6f %.6f %.6f" % v)
        for i in range(0, len(UV), 2):
            lines.append("vt %.6f %.6f" % (UV[i], UV[i + 1]))
        poly, pvi = [], 0
        for idx in P:
            end = idx < 0
            vi = ~idx if end else idx
            if UVI is not None:
                ti = UVI[pvi]
            elif mapping == "ByPolygonVertex":
                ti = pvi
            else:
                ti = vi
            poly.append((vi, ti))
            pvi += 1
            if end:
                for j in range(1, len(poly) - 1):
                    a, b, c = poly[0], poly[j], poly[j + 1]
                    lines.append("f " + " ".join("%d/%d" % (x[0] + 1 + vbase, x[1] + 1 + tbase) for x in (a, b, c)))
                    tris += 1
                for j in range(len(poly)):
                    e = tuple(sorted((poly[j][0] + vbase, poly[(j + 1) % len(poly)][0] + vbase)))
                    edges[e] += 1
                poly = []
        vbase += len(verts)
        tbase += len(UV) // 2
    open(out_obj, "w").write("\n".join(lines) + "\n")
    open(out_obj.rsplit("/", 1)[0] + "/model.mtl", "w").write("newmtl m\nKd 1 1 1\nmap_Kd %s\n" % tex)
    mn = [min(v[i] for v in allv) for i in range(3)]
    mx = [max(v[i] for v in allv) for i in range(3)]
    # pieces by union-find over edges
    parent = list(range(len(allv)))

    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        ra, rb = f(a), f(b)
        if ra != rb:
            parent[ra] = rb
    roots_ = defaultdict(int)
    for i in range(len(allv)):
        roots_[f(i)] += 1
    st = {"meshes": meshes, "triangles": tris, "vertices": len(allv),
          "bbox_min": [round(x, 3) for x in mn], "bbox_max": [round(x, 3) for x in mx],
          "pieces": len(roots_), "piece_vertex_counts": sorted(roots_.values(), reverse=True)[:8],
          "open_edges": sum(1 for c in edges.values() if c == 1), "fbx_settings": up}
    json.dump(st, open(stats_path, "w"), indent=1)
    print(json.dumps(st))


if __name__ == "__main__":
    main(*sys.argv[1:5])
