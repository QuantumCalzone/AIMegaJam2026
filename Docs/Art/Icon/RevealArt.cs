// T115, round 2: my person's idea (2026-11-20): "a human pulling off the robot headpiece".
// The costume parts are the game's own (SM_You_Head's teal box with its eye slots and marker
// smile, the red and cream knit scarf, the striped sleeves and tan garden gloves of the approved
// cast art); the person under the box is new, drawn here. Vector shapes in a 1024 canvas.
// Compiled with IconArt.cs by make_icon.ps1 (Windows PowerShell 5.1, C# 5).
using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;

public static class RevealArt
{
    static readonly Color Ink = ColorTranslator.FromHtml("#161225");
    static readonly Color Gold = ColorTranslator.FromHtml("#F2C14E");
    static readonly Color Red = ColorTranslator.FromHtml("#C8202F");

    static readonly Color Teal = ColorTranslator.FromHtml("#2F8A7C");
    static readonly Color TealLight = ColorTranslator.FromHtml("#3C9E8F");
    static readonly Color TealDark = ColorTranslator.FromHtml("#24695F");
    static readonly Color Knob = ColorTranslator.FromHtml("#237066");
    static readonly Color Hollow = ColorTranslator.FromHtml("#3A2716");
    static readonly Color Liner = ColorTranslator.FromHtml("#6B4A2A");

    static readonly Color Skin = ColorTranslator.FromHtml("#E3A87C");
    static readonly Color SkinShade = ColorTranslator.FromHtml("#C98A60");
    static readonly Color Blush = ColorTranslator.FromHtml("#EE8F7A");
    static readonly Color Hair = ColorTranslator.FromHtml("#3B2619");
    static readonly Color HairLight = ColorTranslator.FromHtml("#5C3D28");
    static readonly Color White = ColorTranslator.FromHtml("#F7F1E6");
    static readonly Color Tongue = ColorTranslator.FromHtml("#D9574F");

    static readonly Color Glove = ColorTranslator.FromHtml("#CDA673");
    static readonly Color GloveShade = ColorTranslator.FromHtml("#A9824F");
    static readonly Color Cuff = ColorTranslator.FromHtml("#6E4A33");
    static readonly Color Stripe = ColorTranslator.FromHtml("#B9332E");
    static readonly Color Cream = ColorTranslator.FromHtml("#EFE4CD");
    static readonly Color Scarf = ColorTranslator.FromHtml("#E8563F");

    static float OW; // outline width in canvas units, set per size
    static bool Lite; // 48 px and below: fewer, bolder details

    static GraphicsPath RR(float x, float y, float w, float h, float r)
    {
        GraphicsPath p = new GraphicsPath();
        r = Math.Min(r, Math.Min(w, h) / 2f);
        float d = r * 2f;
        p.AddArc(x, y, d, d, 180, 90);
        p.AddArc(x + w - d, y, d, d, 270, 90);
        p.AddArc(x + w - d, y + h - d, d, d, 0, 90);
        p.AddArc(x, y + h - d, d, d, 90, 90);
        p.CloseFigure();
        return p;
    }

    static void Fill(Graphics g, GraphicsPath p, Color c) { using (Brush b = new SolidBrush(c)) g.FillPath(b, p); }
    static void Line(Graphics g, GraphicsPath p, float w)
    {
        using (Pen pen = new Pen(Ink, w)) { pen.LineJoin = LineJoin.Round; g.DrawPath(pen, p); }
    }
    static void FillLine(Graphics g, GraphicsPath p, Color c) { Fill(g, p, c); Line(g, p, OW); }
    static GraphicsPath Ell(float cx, float cy, float w, float h)
    {
        GraphicsPath p = new GraphicsPath(); p.AddEllipse(cx - w / 2f, cy - h / 2f, w, h); return p;
    }

    // The costume's box head, front face, centered at (cx, cy), width w, turned by deg.
    // Off the person its slots are empty: you see into the hollow box.
    static void Box(Graphics g, float cx, float cy, float w, float deg, bool small)
    {
        GraphicsState st = g.Save();
        g.TranslateTransform(cx, cy); g.RotateTransform(deg);
        float h = w * 0.806f, l = -w / 2f, t = -h / 2f;
        float kw = w * 0.06f, kh = h * 0.24f;
        foreach (float kx in new float[] { l - kw * 0.8f, -l - kw * 0.2f })
            using (GraphicsPath k = RR(kx, t + h * 0.44f - kh / 2f, kw, kh, kw * 0.45f)) FillLine(g, k, Knob);
        using (GraphicsPath box = RR(l, t, w, h, w * 0.07f))
        {
            Fill(g, box, Teal);
            if (!small)
            {
                Region keep = g.Clip; g.SetClip(box, CombineMode.Intersect);
                using (Brush b = new SolidBrush(TealLight)) g.FillRectangle(b, l, t, w, h * 0.09f);
                using (Brush b = new SolidBrush(TealDark)) g.FillRectangle(b, l, -t - h * 0.08f, w, h * 0.08f);
                g.Clip = keep;
            }
            Line(g, box, OW);
        }
        float sw = w * 0.27f, sh = h * 0.26f, sy = t + h * 0.43f;
        foreach (int side in new int[] { -1, 1 })
        {
            float sx = side * w * 0.24f;
            using (Brush b = new SolidBrush(Hollow)) g.FillRectangle(b, sx - sw / 2f, sy - sh / 2f, sw, sh);
            if (!small)
                using (Brush b = new SolidBrush(Liner)) g.FillRectangle(b, sx - sw / 2f, sy + sh * 0.18f, sw, sh * 0.32f);
        }
        float mw = Math.Max(OW * 0.9f, w * 0.045f), my = t + h * 0.80f, bar = w * 0.09f, tip = w * 0.15f, rise = h * 0.055f;
        using (Pen mp = new Pen(Ink, mw))
        {
            mp.LineJoin = LineJoin.Round; mp.StartCap = LineCap.Round; mp.EndCap = LineCap.Round;
            g.DrawLines(mp, new PointF[] { new PointF(-tip, my - rise), new PointF(-bar, my), new PointF(bar, my), new PointF(tip, my - rise) });
        }
        g.Restore(st);
    }

    // A striped sleeve from the shoulder p0 to the wrist p1, with a thin brown cuff.
    static void Arm(Graphics g, PointF p0, PointF p1, float width)
    {
        float dx = p1.X - p0.X, dy = p1.Y - p0.Y;
        float len = (float)Math.Sqrt(dx * dx + dy * dy);
        float ang = (float)(Math.Atan2(dy, dx) * 180.0 / Math.PI);
        GraphicsState st = g.Save();
        g.TranslateTransform(p0.X, p0.Y); g.RotateTransform(ang);
        using (GraphicsPath sl = RR(-width * 0.2f, -width / 2f, len + width * 0.2f, width, width * 0.3f))
        {
            Fill(g, sl, Cream);
            Region keep = g.Clip; g.SetClip(sl, CombineMode.Intersect);
            float band = width * (Lite ? 0.55f : 0.42f);
            using (Brush b = new SolidBrush(Stripe))
                for (float x = len - band * 0.6f; x > -width; x -= band * 2f) g.FillRectangle(b, x - band, -width, band, width * 2f);
            g.Clip = keep;
            Line(g, sl, OW);
        }
        using (GraphicsPath cf = RR(len - width * 0.22f, -width * 0.56f, width * 0.26f, width * 1.12f, width * 0.1f)) FillLine(g, cf, Cuff);
        g.Restore(st);
    }

    // A garden glove gripping an edge: fingers wrap onto the front, seen from the front.
    // (cx, cy) is the glove's middle; deg turns it to point along the arm (0 = fingers up).
    static void GloveAt(Graphics g, float cx, float cy, float w, float deg)
    {
        GraphicsState st = g.Save();
        g.TranslateTransform(cx, cy); g.RotateTransform(deg);
        float h = w * 1.15f;
        using (GraphicsPath m = RR(-w / 2f, -h / 2f, w, h, w * 0.42f))
        {
            Fill(g, m, Glove);
            Region keep = g.Clip; g.SetClip(m, CombineMode.Intersect);
            using (Brush b = new SolidBrush(GloveShade)) g.FillRectangle(b, -w / 2f, h * 0.22f, w, h);
            g.Clip = keep;
            using (Pen p = new Pen(GloveShade, Math.Max(OW * 0.7f, w * 0.06f)))
            {
                p.StartCap = LineCap.Round; p.EndCap = LineCap.Round;
                g.DrawLine(p, -w * 0.17f, -h * 0.36f, -w * 0.17f, -h * 0.02f);
                g.DrawLine(p, w * 0.17f, -h * 0.36f, w * 0.17f, -h * 0.02f);
            }
            Line(g, m, OW);
        }
        g.Restore(st);
    }

    // The person: face centered at (cx, cy), face width fw. mood: "grin", "wink", "peek".
    static void Person(Graphics g, float cx, float cy, float fw, string mood, float hairTop)
    {
        float fh = fw * 1.06f, l = cx - fw / 2f, t = cy - fh / 2f;
        // Ears.
        foreach (int s in new int[] { -1, 1 })
            using (GraphicsPath e = Ell(cx + s * fw * 0.5f, cy + fh * 0.04f, fw * 0.2f, fw * 0.28f)) FillLine(g, e, SkinShade);
        using (GraphicsPath face = RR(l, t, fw, fh, fw * 0.46f)) FillLine(g, face, Skin);
        // Hair: a cap over the top of the head with tufts standing up, static from the box.
        if (hairTop < cy)
        {
            using (GraphicsPath hp = new GraphicsPath())
            {
                float hl = l - fw * 0.04f, hr = l + fw * 1.04f, hb = t + fh * 0.30f;
                PointF[] pts = new PointF[] {
                    new PointF(hl, hb), new PointF(hl - fw * 0.02f, t + fh * 0.12f),
                    new PointF(l + fw * 0.06f, hairTop + fh * 0.10f), new PointF(l + fw * 0.16f, hairTop + fh * 0.02f),
                    new PointF(l + fw * 0.26f, t - fh * 0.02f), new PointF(l + fw * 0.33f, hairTop - fh * 0.03f),
                    new PointF(l + fw * 0.44f, t - fh * 0.04f), new PointF(l + fw * 0.52f, hairTop - fh * 0.08f),
                    new PointF(l + fw * 0.60f, t - fh * 0.04f), new PointF(l + fw * 0.70f, hairTop - fh * 0.02f),
                    new PointF(l + fw * 0.76f, t - fh * 0.01f), new PointF(l + fw * 0.88f, hairTop + fh * 0.05f),
                    new PointF(hr + fw * 0.02f, t + fh * 0.12f), new PointF(hr, hb),
                    new PointF(l + fw * 0.80f, t + fh * 0.17f), new PointF(l + fw * 0.62f, t + fh * 0.22f),
                    new PointF(l + fw * 0.44f, t + fh * 0.16f), new PointF(l + fw * 0.24f, t + fh * 0.22f) };
                hp.AddClosedCurve(pts, 0.25f);
                FillLine(g, hp, Hair);
            }
        }
        float ey = cy - fh * 0.02f, ex = fw * 0.2f, ew = fw * 0.13f, eh = fw * 0.17f;
        // Cheeks.
        if (!Lite)
        using (Brush b = new SolidBrush(Color.FromArgb(150, Blush)))
            foreach (int s in new int[] { -1, 1 }) g.FillEllipse(b, cx + s * fw * 0.3f - fw * 0.09f, ey + fh * 0.12f, fw * 0.18f, fw * 0.11f);
        // Eyes and brows.
        foreach (int s in new int[] { -1, 1 })
        {
            float x = cx + s * ex;
            bool wink = mood == "wink" && s < 0;
            if (wink)
            {
                using (Pen p = new Pen(Ink, Math.Max(OW, fw * 0.045f))) { p.StartCap = LineCap.Round; p.EndCap = LineCap.Round; g.DrawArc(p, x - ew * 0.75f, ey - eh * 0.2f, ew * 1.5f, eh * 0.9f, 200, 140); }
            }
            else if (mood == "peek")
            {
                using (GraphicsPath e = Ell(x, ey, ew * 1.5f, eh * 1.1f)) FillLine(g, e, White);
                using (Brush b = new SolidBrush(Ink)) g.FillEllipse(b, x + ew * 0.05f, ey - eh * 0.28f, ew * 0.66f, eh * 0.66f);
            }
            else
            {
                using (Brush b = new SolidBrush(Ink)) g.FillEllipse(b, x - ew / 2f, ey - eh / 2f, ew, eh);
                using (Brush b = new SolidBrush(White)) g.FillEllipse(b, x + ew * 0.02f, ey - eh * 0.32f, ew * 0.36f, ew * 0.36f);
            }
            using (Pen p = new Pen(Hair, Math.Max(OW, fw * 0.045f)))
            {
                p.StartCap = LineCap.Round; p.EndCap = LineCap.Round;
                float by = ey - eh * (mood == "peek" ? 1.05f : 1.0f);
                g.DrawArc(p, x - ew * 0.9f, by - eh * 0.25f, ew * 1.8f, eh * 0.7f, 205, 130);
            }
        }
        // Nose.
        if (!Lite)
        using (Pen p = new Pen(SkinShade, Math.Max(OW * 0.8f, fw * 0.035f)))
        { p.StartCap = LineCap.Round; p.EndCap = LineCap.Round; g.DrawArc(p, cx - fw * 0.06f, ey + fh * 0.1f, fw * 0.12f, fw * 0.08f, 20, 140); }
        // Mouth: a big open grin.
        float mt = ey + fh * 0.25f, mw2 = fw * (mood == "peek" ? 0.34f : (Lite ? 0.36f : 0.42f)), mh = fw * (mood == "peek" ? 0.17f : (Lite ? 0.16f : 0.22f));
        using (GraphicsPath m = new GraphicsPath())
        {
            m.AddLine(cx - mw2 / 2f, mt, cx + mw2 / 2f, mt);
            m.AddArc(cx - mw2 / 2f, mt - mh, mw2, mh * 2f, 0, 180);
            m.CloseFigure();
            Fill(g, m, Ink);
            Region keep = g.Clip; g.SetClip(m, CombineMode.Intersect);
            using (Brush b = new SolidBrush(White)) g.FillRectangle(b, cx - mw2, mt - 1, mw2 * 2f, mh * (Lite ? 0.5f : 0.32f));
            using (Brush b = new SolidBrush(Tongue)) g.FillEllipse(b, cx - mw2 * 0.28f, mt + mh * (Lite ? 0.45f : 0.55f), mw2 * 0.56f, mh * 0.8f);
            g.Clip = keep;
            Line(g, m, OW);
        }
    }

    // The costume's body box and knit scarf along the bottom of the icon.
    static void Body(Graphics g, float cx, float top, float w, float scarfW)
    {
        using (GraphicsPath neck = RR(cx - scarfW * 0.22f, top - scarfW * 0.3f, scarfW * 0.44f, scarfW * 0.4f, 4f)) FillLine(g, neck, SkinShade);
        using (GraphicsPath body = RR(cx - w / 2f, top + scarfW * 0.12f, w, 600f, w * 0.06f))
        {
            Fill(g, body, Teal);
            Line(g, body, OW);
        }
        float sh = scarfW * 0.26f;
        using (GraphicsPath sc = RR(cx - scarfW / 2f, top - sh * 0.15f, scarfW, sh, sh * 0.5f))
        {
            Fill(g, sc, Scarf);
            Region keep = g.Clip; g.SetClip(sc, CombineMode.Intersect);
            using (Pen p = new Pen(Cream, sh * 0.28f))
                for (float x = cx - scarfW; x < cx + scarfW; x += sh * 0.75f) g.DrawLine(p, x, top + sh, x + sh * 0.9f, top - sh * 0.4f);
            g.Clip = keep;
            Line(g, sc, OW);
        }
    }

    static void Tile(Graphics g, Color fill, Color rim)
    {
        using (GraphicsPath t = RR(28, 28, 968, 968, 200)) Fill(g, t, rim);
        using (GraphicsPath t = RR(60, 60, 904, 904, 170)) Fill(g, t, fill);
    }

    // Hand-placed pixels at 16 px. . clear, r rim, b tile, K ink, T teal, H hollow slot, g glove,
    // c cuff, s red stripe, w cream stripe, S skin, h hair, P pupil, W white, f scarf.
    static readonly System.Collections.Generic.Dictionary<string, string[]> Pix = new System.Collections.Generic.Dictionary<string, string[]>
    {
        { "R1", new string[] {
            ".rrrrrrrrrrrrrr.",
            "rbbKKKKKKKKKKbbr",
            "rbbKTTTTTTTTKbbr",
            "rbgKTHHTTHHTKgbr",
            "rbgKTTKKKKTTKgbr",
            "rbgKKKKKKKKKKgbr",
            "rbcbbhbhhbhbbcbr",
            "rbsKhhhhhhhhKsbr",
            "rbwKhSSSSSShKwbr",
            "rbsKSSPSSPSSKsbr",
            "rbwKSSSSSSSSKwbr",
            "rbsKSSKWWKSSKsbr",
            "rbwbKSSKKSSKbwbr",
            "rbsbbKKKKKKbbsbr",
            "rbwbbbffffbbbwbr",
            ".rrrrrrrrrrrrrr." } },
        { "R2", new string[] {
            ".rrrrrrrrrrrrrr.",
            "rbbbbbbKKbbbbbbr",
            "rbbbbKKTTKbbbbbr",
            "rbbKKTTTTKbbbbbr",
            "rbKTTTTHHTKbbbbr",
            "rbKTTTTTTTKbggbr",
            "rbbKHHTTKTTKggbr",
            "rbbKTTKKTTTKbcbr",
            "rbbbKTTTTKKhKsKr",
            "rbbbKTTKKShhKwKr",
            "rbbbKKKSSSPSKsKr",
            "rbbbKSKKSSPSKwKr",
            "rbbbKSSKWWKSKsKr",
            "rbbbbKSSKKSKbwKr",
            "rbbbbKKKKKKKbsKr",
            ".rrrrrrrrrrrrrr." } },
        { "R2_20", new string[] {
            "..rrrrrrrrrrrrrrrr..",
            ".rbbbbbbbbKKbbbbbbr.",
            "rbbbbbbbKKTTKbbbbbbr",
            "rbbbbbKKTTTTKbbbbbbr",
            "rbbbKKTTTTTHHKbbbbbr",
            "rbbKTTTTTTHHTKbbbbbr",
            "rbbbKTTHHTTTTTKggbbr",
            "rbbbKTHHTTTTTTKggbbr",
            "rbbbnKTTTTKKTTTggbbr",
            "rbbbnKTTKKTTTKKbcbbr",
            "rbbbbbKTTTTKKhKKwKbr",
            "rbbbbbKTTKKhhhKKsKbr",
            "rbbbbbKKKSSShhKKwKbr",
            "rbbbbbKSSSSSPSKKsKbr",
            "rbbbbbKSKKSSPSKKwKbr",
            "rbbbbbKSKWWWKSKKsKbr",
            "rbbbbbbKSKRKSKbKwKbr",
            "rbbbbbbbKKKKKbbKsKbr",
            ".rbbbbfwfwfwfwfKwKr.",
            "..rrrrrrrrrrrrrrrr.." } },
        { "R2_24", new string[] {
            "..rrrrrrrrrrrrrrrrrrrr..",
            ".rbbbbbbbbbbbKKbbbbbbbr.",
            "rbbbbbbbbbbKKTTKbbbbbbbr",
            "rbbbbbbbbKKTTTTKbbbbbbbr",
            "rbbbbbbKKTTTTTTTKbbbbbbr",
            "rbbbbKKTTTTTTHHTKbbbbbbr",
            "rbbbKTTTTTTTHHTTTKbbbbbr",
            "rbbbKTTTTTTTTTTTTgggbbbr",
            "rbbbnKTTHHTTTTKTTgggbbbr",
            "rbbbnKTHHTTTKKTTTgggbbbr",
            "rbbbbbKTTTKKTTTTKKccbbbr",
            "rbbbbbKTTTTTTTKKhKssKbbr",
            "rbbbbbbKTTTTKKhhKKwwKbbr",
            "rbbbbbbKTTKKSSSSKKssKbbr",
            "rbbbbbbKKKSSSPWSKKwwKbbr",
            "rbbbbbbKSKKSSPPSKKssKbbr",
            "rbbbbbbKSSSSSSSSKKwwKbbr",
            "rbbbbbbKSKWWWWKSKKssKbbr",
            "rbbbbbbKSSKRRKSSKKwwKbbr",
            "rbbbbbbbKSSKKSSKbKssKbbr",
            "rbbbbbbbbKKKKKKbbKwwKbbr",
            "rbbbbbbbbbeeeebbbKssKbbr",
            ".rbbbbbwfwfwfwfwfKwwKbr.",
            "..rrrrrrrrrrrrrrrrrrrr.." } },
        { "R2_32", new string[] {
            "...rrrrrrrrrrrrrrrrrrrrrrrrrr...",
            ".rrbbbbbbbbbbbbbbbbbbbbbbbbbbrr.",
            ".rbbbbbbbbbbbbbbKKbbbbbbbbbbbbr.",
            "rbbbbbbbbbbbbbKKTTKbbbbbbbbbbbbr",
            "rbbbbbbbbbbbKKTTTTKbbbbbbbbbbbbr",
            "rbbbbbbbbbKKTTTTTTTKbbbbbbbbbbbr",
            "rbbbbbbbKKTTTTTTTHHKbbbbbbbbbbbr",
            "rbbbbbKKTTTTTTTHHHHTKbbbbbbbbbbr",
            "rbbbbKTTTTTTTTTHHTTTKbbbbbbbbbbr",
            "rbbbbKTTTTHHTTTTTTTTTKbbbbbbbbbr",
            "rbbbbbKTHHHHTTTTTTTTTKbgggbbbbbr",
            "rbbbbbKTHHTTTTTTTTKTTTggggbbbbbr",
            "rbbbbbnKTTTTKTTTKKTTTTggggbbbbbr",
            "rbbbbbnKTTTTTKKKTTTTKKggggbbbbbr",
            "rbbbbbbbKTTTTTTTTTKKhbbcccbbbbbr",
            "rbbbbbbbKTTTTTTTKKhhhhKsssKbbbbr",
            "rbbbbbbbbKTTTTKKhhhhhhKwwwKbbbbr",
            "rbbbbbbbbKTTKKSShhhShKKwwwKbbbbr",
            "rbbbbbbbbbKKhhhSSSSSSKKsssKbbbbr",
            "rbbbbbbbbKKSSSSSSPWSSKKsssKbbbbr",
            "rbbbbbbbKeKSSKSSSPPSSKKwwwKbbbbr",
            "rbbbbbbbKeKSKSKSSPPSSKKwwwKbbbbr",
            "rbbbbbbbKeKSSSSeeSSSSKKsssKbbbbr",
            "rbbbbbbbbKKSSKWWWWKSSKKsssKbbbbr",
            "rbbbbbbbbbKSSKKRRKKSSKKwwwKbbbbr",
            "rbbbbbbbbbKSSSKKKKSSSKKwwwKbbbbr",
            "rbbbbbbbbbbKSSSSSSSSKbKsssKbbbbr",
            "rbbbbbbbbbbbKKKKKKKKbbKsssKbbbbr",
            "rbbbbbbbbbbbbbeeeebbbbKwwwKbbbbr",
            ".rbbbbbbbbwwffwwffwwffKwwwKbbbr.",
            ".rrbbbbbbbwffwwffwwffwKsssKbbrr.",
            "...rrrrrrrrrrrrrrrrrrrrrrrrrr..." } },
        { "R3", new string[] {
            ".rrrrrrrrrrrrrr.",
            "rbKKKKKKKKKKKKbr",
            "rbKTTTTTTTTTTKbr",
            "rbKTHHHTTHHHTKbr",
            "rbKTHHHTTHHHTKbr",
            "rbKTTTTTTTTTTKbr",
            "rgKTTTKKKKTTTKgr",
            "rgKKKKKKKKKKKKgr",
            "rcbKSWPSSWPSKbcr",
            "rsbKSWWSSWWSKbsr",
            "rwbKSSSSSSSSKbwr",
            "rsbKSSKWWKSSKbsr",
            "rwbbKSSKKSSKbbwr",
            "rsbbbKKKKKKbbbsr",
            "rwbbbbffffbbbbwr",
            ".rrrrrrrrrrrrrr." } },
    };

    static Bitmap FromPix(string v, int size)
    {
        string[] rows = Pix[v];
        v = v.Split('_')[0];
        System.Collections.Generic.Dictionary<char, Color> pal = new System.Collections.Generic.Dictionary<char, Color>();
        pal['.'] = Color.Transparent;
        pal['r'] = v == "R3" ? Gold : Ink;
        pal['b'] = v == "R1" ? Gold : (v == "R2" ? Red : Ink);
        pal['K'] = Ink; pal['P'] = Ink; pal['T'] = Teal; pal['H'] = Hollow;
        pal['g'] = Glove; pal['c'] = Cuff; pal['s'] = Stripe; pal['w'] = Cream;
        pal['S'] = Skin; pal['h'] = Hair; pal['W'] = White; pal['f'] = Scarf;
        pal['t'] = TealLight; pal['L'] = Liner; pal['e'] = SkinShade; pal['R'] = Tongue; pal['d'] = TealDark; pal['n'] = Knob;
        Bitmap bmp = new Bitmap(size, size, PixelFormat.Format32bppArgb);
        for (int y = 0; y < size; y++)
        {
            if (rows[y].Length != size) throw new Exception("pixel row " + y + " of " + v + " is " + rows[y].Length + " wide");
            for (int x = 0; x < size; x++) bmp.SetPixel(x, y, pal[rows[y][x]]);
        }
        return bmp;
    }

    public static string[] Ascii(string v, int size)
    {
        bool keepAA = Aliased; Aliased = true;
        Bitmap b = Render(v, size, true);
        Aliased = keepAA;
        string keys = ".rbKTtHLgcswShWPfeR";
        Color[] cols = new Color[] { Color.Transparent, Ink, v == "R1" ? Gold : (v == "R2" ? Red : Ink), Ink, Teal, TealLight, Hollow, Liner,
            Glove, Cuff, Stripe, Cream, Skin, Hair, White, Ink, Scarf, SkinShade, Tongue };
        string[] rows = new string[size];
        for (int y = 0; y < size; y++)
        {
            char[] row = new char[size];
            for (int x = 0; x < size; x++)
            {
                Color c = b.GetPixel(x, y);
                if (c.A < 128) { row[x] = '.'; continue; }
                int best = 1; double bd = 1e9;
                for (int i = 1; i < cols.Length; i++)
                {
                    double d = Math.Pow(c.R - cols[i].R, 2) + Math.Pow(c.G - cols[i].G, 2) + Math.Pow(c.B - cols[i].B, 2);
                    if (d < bd) { bd = d; best = i; }
                }
                row[x] = keys[best];
            }
            rows[y] = new string(row);
        }
        b.Dispose();
        return rows;
    }

    static bool Aliased = false;

    public static Bitmap Render(string v, int size) { return Render(v, size, false); }

    static Bitmap Render(string v, int size, bool noPix)
    {
        if (!noPix && Pix.ContainsKey(v + "_" + size)) return FromPix(v + "_" + size, size);
        if (!noPix && size == 16 && Pix.ContainsKey(v)) return FromPix(v, size);
        Bitmap bmp = new Bitmap(size, size, PixelFormat.Format32bppArgb);
        using (Graphics g = Graphics.FromImage(bmp))
        {
            g.SmoothingMode = Aliased ? SmoothingMode.None : SmoothingMode.AntiAlias;
            g.PixelOffsetMode = Aliased ? PixelOffsetMode.Half : PixelOffsetMode.HighQuality;
            g.Clear(Color.Transparent);
            g.ScaleTransform(size / 1024f, size / 1024f);
            OW = Math.Max(18f, 1024f / size * (size <= 48 ? 1.0f : 0.9f));
            bool small = size <= 48;
            Lite = small;
            Color fill = v == "R1" ? Gold : (v == "R2" ? Red : Ink);
            Color rim = v == "R3" ? Gold : Ink;
            Tile(g, fill, rim);
            using (GraphicsPath clip = RR(56, 56, 912, 912, 174))
            {
                g.SetClip(clip);
                if (v == "R1")
                {
                    // Lift: both gloves hold the box up over the head; the whole face shows.
                    Body(g, 512, 905, 470, 300);
                    Arm(g, new PointF(300, 960), new PointF(290, 470), 96);
                    Arm(g, new PointF(724, 960), new PointF(738, 450), 96);
                    Person(g, 512, 690, 330, "grin", 470);
                    Box(g, 512, 270, 430, -5f, small);
                    GloveAt(g, 300, 395, 110, -4f);
                    GloveAt(g, 728, 372, 110, -4f);
                }
                else if (v == "R2")
                {
                    // Tilt: one glove pushes the box up and off; the box still rests on the left of the head.
                    Body(g, 512, 905, 470, 300);
                    Person(g, 512, 670, 350, "wink", 450);
                    Arm(g, new PointF(735, 990), new PointF(768, 500), 100);
                    Box(g, 455, 330, 500, -24f, small);
                    GloveAt(g, 768, 420, 116, -24f);
                }
                else
                {
                    // Peek: the box is lifted a crack, and the person's eyes peek out from under it.
                    Body(g, 512, 930, 470, 300);
                    Person(g, 512, 735, 340, "peek", 2000);
                    Arm(g, new PointF(250, 1000), new PointF(222, 670), 96);
                    Arm(g, new PointF(774, 1000), new PointF(802, 670), 96);
                    Box(g, 512, 395, 600, 0f, small);
                    GloveAt(g, 218, 590, 112, 0f);
                    GloveAt(g, 806, 590, 112, 0f);
                }
                g.ResetClip();
            }
        }
        return bmp;
    }
}
