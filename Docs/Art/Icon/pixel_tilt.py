"""T115: lays out the picked icon (2 Tilt) as pixel grids for 16, 20 and 24 px.

The vector art (RevealArt.cs) blurs below 32 px, so these sizes get hand-placed pixels.
This script places the big shapes on the grid: the tile, the box tilted at a clean 1:2 step
(about 27 degrees, near the vector's 24), the face, the arm and glove, the scarf. Its output was
pasted into RevealArt.cs's Pix table and then touched up by hand there; RevealArt.cs is the source
of truth, not this script. Letters are the ones RevealArt.FromPix reads:
  . clear  r rim  b tile  K ink  T teal  t lid  H hollow slot  L liner  g glove  c cuff
  s red stripe  w cream stripe  S skin  e skin shade  h hair  W white  P pupil  R tongue  f scarf
Usage: python pixel_tilt.py [16|20|24]
"""
import sys


def grid(n):
    return [["." for _ in range(n)] for _ in range(n)]


def tile(g, n):
    # Rounded tile: ink rim, red fill; the corner radius is 2 px at 20 and 24, 1 px at 16.
    rad = 1 if n <= 16 else 2
    for y in range(n):
        for x in range(n):
            g[y][x] = "b"
    for i in range(n):
        g[0][i] = g[n - 1][i] = g[i][0] = g[i][n - 1] = "r"
    corners = [(0, 0, 1, 1), (n - 1, 0, -1, 1), (0, n - 1, 1, -1), (n - 1, n - 1, -1, -1)]
    for cx, cy, dx, dy in corners:
        g[cy][cx] = "."
        if rad == 2:
            g[cy][cx + dx] = "."
            g[cy + dy][cx] = "."
            g[cy + dy][cx + dx] = "r"


def poly_fill(g, pts, ch):
    # Even-odd fill at pixel centers.
    n = len(g)
    for y in range(n):
        for x in range(n):
            px, py = x + 0.5, y + 0.5
            inside = False
            j = len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]
                xj, yj = pts[j]
                if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
                    inside = not inside
                j = i
            if inside:
                g[y][x] = ch


def line(g, x0, y0, x1, y1, ch):
    # Bresenham, so the 1:2 edges step evenly.
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        if 0 <= y0 < len(g) and 0 <= x0 < len(g):
            g[y0][x0] = ch
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def put(g, x, y, ch):
    if 0 <= y < len(g) and 0 <= x < len(g):
        g[y][x] = ch


def rect(g, x0, y0, x1, y1, ch):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(g, x, y, ch)


def rotated_rect(cx, cy, u, v, w, h):
    return [(cx + sa * u[0] * w / 2 + sb * v[0] * h / 2, cy + sa * u[1] * w / 2 + sb * v[1] * h / 2)
            for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def compose32():
    n = 32
    g = grid(n)
    for y in range(n):
        for x in range(n):
            g[y][x] = "b"
    for i in range(n):
        g[0][i] = g[n - 1][i] = g[i][0] = g[i][n - 1] = "r"
    for cx, cy, dx, dy in [(0, 0, 1, 1), (n - 1, 0, -1, 1), (0, n - 1, 1, -1), (n - 1, n - 1, -1, -1)]:
        for ox, oy in ((0, 0), (1, 0), (2, 0), (0, 1), (0, 2)):
            g[cy + oy * dy][cx + ox * dx] = "."
        g[cy + dy][cx + dx] = "r"; g[cy + dy][cx + 2 * dx] = "r"; g[cy + 2 * dy][cx + dx] = "r"
    # Scarf and neck.
    for x in range(10, 22):
        put(g, x, 29, "f" if (x // 2) % 2 == 0 else "w")
        put(g, x, 30, "f" if ((x + 1) // 2) % 2 == 0 else "w")
    rect(g, 14, 28, 17, 28, "e")
    # Face: x 10..21, y 15..27, rounded at the chin.
    rect(g, 11, 15, 20, 26, "S")
    for y in range(15, 26):
        put(g, 10, y, "K"); put(g, 21, y, "K")
    put(g, 11, 26, "K"); put(g, 20, 26, "K"); put(g, 10, 26, "b"); put(g, 21, 26, "b")
    rect(g, 12, 27, 19, 27, "K")
    # Left ear.
    for y in (20, 21, 22):
        put(g, 9, y, "e"); put(g, 8, y, "K")
    put(g, 9, 19, "K"); put(g, 9, 23, "K")
    # Hair where the box lifts off, with two tufts.
    for x, y in ((18, 14), (20, 14), (21, 15)):
        put(g, x, y, "h")
    rect(g, 16, 15, 20, 15, "h")
    rect(g, 15, 16, 21, 16, "h")
    rect(g, 19, 17, 20, 17, "h")
    # Face details: wink (left), open eye with a glint (right), brows, nose, grin.
    for x, y in ((12, 21), (13, 20), (14, 21)):
        put(g, x, y, "K")
    rect(g, 17, 19, 18, 21, "P"); put(g, 18, 19, "W")
    for x, y in ((12, 18), (13, 18), (14, 18)):
        put(g, x, y, "h")
    for x, y in ((16, 17), (17, 17), (18, 17)):
        put(g, x, y, "h")
    put(g, 15, 22, "e"); put(g, 16, 22, "e")
    for x in range(13, 19):
        put(g, x, 23, "K")
    rect(g, 14, 23, 17, 23, "W")
    put(g, 13, 24, "K"); put(g, 18, 24, "K"); rect(g, 14, 24, 17, 24, "K"); rect(g, 15, 24, 16, 24, "R")
    put(g, 14, 25, "K"); put(g, 15, 25, "K"); put(g, 16, 25, "K"); put(g, 17, 25, "K")
    # Box: TL (5,8) TR (17,2) BR (22,12) BL (10,18), 1:2 steps.
    box = [(5, 8), (17, 2), (22, 12), (10, 18)]
    poly_fill(g, [(x + 0.5, y + 0.5) for x, y in box], "T")
    for (x0, y0), (x1, y1) in zip(box, box[1:] + box[:1]):
        line(g, x0, y0, x1, y1, "K")
    u = (0.894, -0.447); v = (0.447, 0.894)
    bc = (14.0, 10.5)
    for a in (-3.2, 3.2):
        c = (bc[0] + a * u[0] - 0.78 * v[0], bc[1] + a * u[1] - 0.78 * v[1])
        poly_fill(g, rotated_rect(c[0], c[1], u, v, 3.8, 2.6), "H")
    # The drawn smile along the box's tilt, tips up.
    def at(a, b):
        return (int(round(bc[0] + a * u[0] + b * v[0] - 0.5)), int(round(bc[1] + a * u[1] + b * v[1] - 0.5)))
    pts = [at(-2.4, 2.0), at(-1.3, 3.0), at(1.3, 3.0), at(2.4, 2.0)]
    for p0, p1 in zip(pts, pts[1:]):
        line(g, p0[0], p0[1], p1[0], p1[1], "K")
    put(g, 6, 12, "n"); put(g, 6, 13, "n")
    # Arm: sleeve x 23..25 with outlines, stripes two rows each; cuff; glove on the box corner.
    for y in range(15, n - 1):
        put(g, 22, y, "K"); put(g, 26, y, "K")
        for x in (23, 24, 25):
            put(g, x, y, "s" if (y // 2) % 2 else "w")
    rect(g, 23, 14, 25, 14, "c")
    rect(g, 22, 10, 25, 13, "g")
    put(g, 22, 10, "b"); put(g, 25, 13, "g")
    return g


def compose(n):
    if n == 32:
        return compose32()
    g = grid(n)
    tile(g, n)
    if n == 24:
        # Face (behind the box): x 7..16, y 11..20.
        rect(g, 8, 11, 15, 19, "S")
        for y in range(11, 20):
            put(g, 7, y, "K"); put(g, 16, y, "K")
        rect(g, 8, 20, 15, 20, "K")
        put(g, 7, 19, "b"); put(g, 16, 19, "b"); put(g, 8, 19, "K"); put(g, 15, 19, "K")
        put(g, 7, 20, "b"); put(g, 16, 20, "b"); put(g, 8, 20, "b"); put(g, 15, 20, "b")
        rect(g, 9, 20, 14, 20, "K")
        # Hair on the right, where the box lifts off.
        rect(g, 12, 10, 16, 11, "h")
        put(g, 16, 10, "K"); put(g, 17, 11, "K")
        # Neck and scarf.
        rect(g, 10, 21, 13, 21, "e")
        for x in range(7, 17):
            put(g, x, 22, "f" if x % 2 == 0 else "w")
        # Box: corners TL (4,6) TR (14,1) BR (18,9) BL (8,14).
        box = [(4, 6), (14, 1), (18, 9), (8, 14)]
        poly_fill(g, [(x + 0.5, y + 0.5) for x, y in box], "T")
        for (x0, y0), (x1, y1) in zip(box, box[1:] + box[:1]):
            line(g, x0, y0, x1, y1, "K")
        # Arm: sleeve x 18..19 from y 11 down, stripes by row; cuff; glove on the box corner.
        for y in range(11, n - 1):
            put(g, 17, y, "K"); put(g, 20, y, "K")
            put(g, 18, y, "s" if y % 2 else "w"); put(g, 19, y, "s" if y % 2 else "w")
        put(g, 18, 10, "c"); put(g, 19, 10, "c")
        rect(g, 17, 7, 19, 9, "g")
    elif n == 20:
        rect(g, 7, 10, 13, 16, "S")
        for y in range(10, 16):
            put(g, 6, y, "K"); put(g, 14, y, "K")
        put(g, 6, 16, "b"); put(g, 14, 16, "b"); put(g, 7, 16, "K"); put(g, 13, 16, "K")
        rect(g, 8, 17, 12, 17, "K")
        rect(g, 10, 9, 14, 9, "h")
        rect(g, 9, 18, 11, 18, "e")
        for x in range(6, 15):
            put(g, x, 18, "f" if x % 2 == 0 else "w")
        box = [(3, 5), (11, 1), (15, 8), (7, 12)]
        poly_fill(g, [(x + 0.5, y + 0.5) for x, y in box], "T")
        for (x0, y0), (x1, y1) in zip(box, box[1:] + box[:1]):
            line(g, x0, y0, x1, y1, "K")
        for y in range(10, n - 1):
            put(g, 15, y, "K"); put(g, 17, y, "K")
            put(g, 16, y, "s" if y % 2 else "w")
        put(g, 16, 9, "c")
        rect(g, 15, 6, 16, 8, "g")
    else:
        rect(g, 5, 8, 11, 13, "S")
        for y in range(8, 13):
            put(g, 4, y, "K"); put(g, 12, y, "K")
        rect(g, 5, 14, 11, 14, "K")
        put(g, 4, 13, "b"); put(g, 12, 13, "b"); put(g, 5, 13, "K"); put(g, 11, 13, "K")
        box = [(2, 4), (8, 1), (11, 7), (5, 10)]
        poly_fill(g, [(x + 0.5, y + 0.5) for x, y in box], "T")
        for (x0, y0), (x1, y1) in zip(box, box[1:] + box[:1]):
            line(g, x0, y0, x1, y1, "K")
        for y in range(8, n - 1):
            put(g, 13, y, "s" if y % 2 else "w")
        put(g, 13, 7, "c")
        rect(g, 12, 5, 13, 6, "g")
    return g


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    for row in compose(n):
        print('            "' + "".join(row) + '",')
