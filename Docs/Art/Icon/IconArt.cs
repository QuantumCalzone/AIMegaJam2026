// T115: draws the game icon, No Humans On Set's costume box head, in 2D.
// The shapes and colors are measured from an in-engine render of SM_You_Head and BP_Robot's
// face parts (render/head_front.png): box 1.24:1, slots, eyeballs, marker smile, ping-pong antenna.
// Compiled and run by make_icon.ps1 (Windows PowerShell 5.1, System.Drawing, C# 5: no newer syntax).
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO;

public static class IconArt
{
    // UIStyle colors (Graphs/UIStyle/UIColor.txt, sRGB hex from the comments).
    static readonly Color Ink = ColorTranslator.FromHtml("#161225");
    static readonly Color Gold = ColorTranslator.FromHtml("#F2C14E");
    static readonly Color OldGold = ColorTranslator.FromHtml("#A9873A");
    static readonly Color Red = ColorTranslator.FromHtml("#C8202F");
    static readonly Color Paper = ColorTranslator.FromHtml("#F5E9CF");

    // The head, sampled from the render (face #2B7C70, liner #63482A, eyeball #CBC4BB),
    // lifted a little toward flat, bright light.
    static readonly Color Teal = ColorTranslator.FromHtml("#2F8A7C");
    static readonly Color TealLight = ColorTranslator.FromHtml("#3C9E8F");
    static readonly Color TealDark = ColorTranslator.FromHtml("#24695F");
    static readonly Color Knob = ColorTranslator.FromHtml("#237066");
    static readonly Color Liner = ColorTranslator.FromHtml("#6B4A2A");
    static readonly Color Scuff = ColorTranslator.FromHtml("#B98A55");
    static readonly Color Eye = ColorTranslator.FromHtml("#F7F1E6");
    static readonly Color Ball = ColorTranslator.FromHtml("#F4F0E8");
    static readonly Color Straw = ColorTranslator.FromHtml("#BDB9B2");

    // Level of detail: 0 for 16-24 px, 1 for 32-48 px, 2 for 64 px and up.
    static int Lod(int size) { return size <= 24 ? 0 : (size <= 48 ? 1 : 2); }

    static GraphicsPath RoundRect(float x, float y, float w, float h, float r)
    {
        GraphicsPath p = new GraphicsPath();
        r = Math.Min(r, Math.Min(w, h) / 2f);
        if (r <= 0.01f) { p.AddRectangle(new RectangleF(x, y, w, h)); return p; }
        float d = r * 2f;
        p.AddArc(x, y, d, d, 180, 90);
        p.AddArc(x + w - d, y, d, d, 270, 90);
        p.AddArc(x + w - d, y + h - d, d, d, 0, 90);
        p.AddArc(x, y + h - d, d, d, 90, 90);
        p.CloseFigure();
        return p;
    }

    // Snap a value to the pixel grid at small sizes.
    static float Sn(float v, int size) { return size < 64 ? (float)Math.Round(v) : v; }

    // Draws the box head with its box centered at (cx, cy), box width w.
    static void Head(Graphics g, int size, float cx, float cy, float w, bool antenna, bool knobs, float outline)
    {
        int lod = Lod(size);
        float h = w * 0.806f;
        float left = Sn(cx - w / 2f, size), right = Sn(cx + w / 2f, size);
        float top = Sn(cy - h / 2f, size), bottom = Sn(cy + h / 2f, size);
        w = right - left; h = bottom - top; cx = (left + right) / 2f;
        float r = lod == 0 ? Math.Max(1f, w * 0.08f) : w * 0.07f;
        Pen ol = new Pen(Ink, outline); ol.LineJoin = LineJoin.Round;

        if (antenna)
        {
            float bd = w * (lod == 2 ? 0.14f : 0.2f);
            float by = top - h * (lod == 2 ? 0.36f : 0.3f);
            float sw = Math.Max(lod == 2 ? w * 0.022f : 1f, 1f);
            using (Pen sp = new Pen(Ink, sw + outline * 2f)) g.DrawLine(sp, cx, top, cx, by);
            using (Pen sp = new Pen(Straw, sw)) g.DrawLine(sp, cx, top, cx, by);
            RectangleF br = new RectangleF(cx - bd / 2f, by - bd / 2f, bd, bd);
            using (Brush b = new SolidBrush(Ball)) g.FillEllipse(b, br);
            g.DrawEllipse(ol, br);
            if (lod == 2)
            {
                using (Brush b = new SolidBrush(Color.FromArgb(70, Straw)))
                    g.FillEllipse(b, br.X + bd * 0.45f, br.Y + bd * 0.5f, bd * 0.4f, bd * 0.35f);
            }
        }

        if (knobs)
        {
            float kw = w * 0.05f, kh = h * 0.24f, ky = top + h * 0.44f - kh / 2f;
            foreach (float kx in new float[] { left - kw, right })
            {
                using (GraphicsPath kp = RoundRect(kx, ky, kw, kh, kw * 0.45f))
                {
                    using (Brush b = new SolidBrush(Knob)) g.FillPath(b, kp);
                    g.DrawPath(ol, kp);
                }
            }
        }

        using (GraphicsPath box = RoundRect(left, top, w, h, r))
        {
            using (Brush b = new SolidBrush(Teal)) g.FillPath(b, box);
            if (lod >= 1)
            {
                // The lid catches the light; the bottom edge sits in shadow.
                Region keep = g.Clip; g.SetClip(box, CombineMode.Intersect);
                using (Brush b = new SolidBrush(TealLight)) g.FillRectangle(b, left, top, w, h * 0.09f);
                using (Brush b = new SolidBrush(TealDark)) g.FillRectangle(b, left, bottom - h * 0.08f, w, h * 0.08f);
                if (lod == 2)
                {
                    // Cardboard showing through the scuffed corners.
                    using (Brush b = new SolidBrush(Scuff))
                    {
                        float s = w * 0.05f;
                        g.FillPolygon(b, new PointF[] { new PointF(left, top), new PointF(left + s, top), new PointF(left, top + s * 1.3f) });
                        g.FillPolygon(b, new PointF[] { new PointF(right, top), new PointF(right - s * 0.8f, top), new PointF(right, top + s) });
                        g.FillPolygon(b, new PointF[] { new PointF(left, bottom), new PointF(left + s * 0.9f, bottom), new PointF(left, bottom - s) });
                    }
                }
                g.Clip = keep;
            }
            g.DrawPath(ol, box);
        }

        // Eye slots with the person's eyes peeking through.
        float slotW = w * (lod <= 1 ? 0.30f : 0.27f), slotH = h * (lod <= 1 ? 0.32f : 0.26f);
        float slotY = top + h * (lod <= 1 ? 0.41f : 0.43f);
        foreach (int side in new int[] { -1, 1 })
        {
            float sx = cx + side * w * 0.24f;
            float x0 = Sn(sx - slotW / 2f, size), x1 = Sn(sx + slotW / 2f, size);
            float y0 = Sn(slotY - slotH / 2f, size), y1 = Sn(slotY + slotH / 2f, size);
            if (x1 - x0 < 3 && size < 64) x1 = x0 + 3;
            if (y1 - y0 < 2 && size < 64) y1 = y0 + 2;
            using (Brush b = new SolidBrush(Liner)) g.FillRectangle(b, x0, y0, x1 - x0, y1 - y0);
            float ecx = (x0 + x1) / 2f, ecy = (y0 + y1) / 2f;
            float ed = Math.Min(x1 - x0, y1 - y0) * (lod <= 1 ? 1.0f : 0.92f);
            if (lod == 0)
            {
                // At 16-24 px a round eyeball blurs to gray: draw it as a pixel block with a pupil.
                float ew = (float)Math.Max(2, Math.Round(ed)), ex = (float)Math.Round(ecx - ew / 2f), ey = (float)Math.Round(ecy - ew / 2f);
                using (Brush b = new SolidBrush(Eye)) g.FillRectangle(b, ex, ey, ew, ew);
                float pw = (float)Math.Max(1, Math.Round(ew * 0.5f));
                using (Brush b = new SolidBrush(Ink)) g.FillRectangle(b, (float)Math.Round(ecx - pw / 2f), (float)Math.Round(ecy - pw / 2f), pw, pw);
            }
            else
            {
                using (Brush b = new SolidBrush(Eye)) g.FillEllipse(b, ecx - ed / 2f, ecy - ed / 2f, ed, ed);
                float pd = ed * (lod == 1 ? 0.52f : 0.48f);
                using (Brush b = new SolidBrush(Ink)) g.FillEllipse(b, ecx - pd / 2f, ecy - pd / 2f, pd, pd);
                if (lod == 2)
                {
                    float hd = ed * 0.14f;
                    using (Brush b = new SolidBrush(Eye)) g.FillEllipse(b, ecx + pd * 0.05f, ecy - pd * 0.38f, hd, hd);
                }
            }
        }

        // The marker smile: a flat bar with two strokes turning up at the ends (InkL, InkR).
        float mw = lod == 0 ? Math.Max(1f, (float)Math.Round(w * 0.06f)) : (lod == 1 ? Math.Max(1.6f, w * 0.065f) : w * 0.045f);
        float my = top + h * (lod <= 1 ? 0.78f : 0.80f);
        float bar = w * 0.09f, tip = w * (lod <= 1 ? 0.17f : 0.15f), rise = h * (lod <= 1 ? 0.08f : 0.055f);
        if (lod == 0)
        {
            my = (float)Math.Round(my) + (mw % 2 == 1 ? 0.5f : 0f);
            float bx0 = (float)Math.Round(cx - bar), bx1 = (float)Math.Round(cx + bar);
            using (Pen mp = new Pen(Ink, mw))
            {
                mp.StartCap = LineCap.Square; mp.EndCap = LineCap.Square;
                g.DrawLine(mp, bx0, my, bx1, my);
                g.DrawLine(mp, bx0 - mw, my - rise, bx0 - mw, my - rise);
                g.DrawLine(mp, bx1 + mw, my - rise, bx1 + mw, my - rise);
            }
        }
        else
        {
            using (Pen mp = new Pen(Ink, mw))
            {
                mp.LineJoin = LineJoin.Round; mp.StartCap = LineCap.Round; mp.EndCap = LineCap.Round;
                g.DrawLines(mp, new PointF[] {
                    new PointF(cx - tip, my - rise), new PointF(cx - bar, my),
                    new PointF(cx + bar, my), new PointF(cx + tip, my - rise) });
            }
        }
        ol.Dispose();
    }

    // Hand-placed pixels for the sizes where vector shapes blur: 16, 20 and 24 px.
    // . clear, r tile rim, b tile fill, K ink outline, T teal, t lid, d bottom edge, N side knob,
    // L slot liner, W eyeball, P pupil, A ping-pong ball, s straw. A and B share a grid (only the
    // tile colors swap); C is the face alone.
    static readonly Dictionary<string, string[]> Pix = new Dictionary<string, string[]>
    {
        { "tile16", new string[] {
            ".rrrrrrrrrrrrrr.",
            "rbbbbbbbbbbbbbbr",
            "rbbbbbbbbbbbbbbr",
            "rbbKKKKKKKKKKbbr",
            "rbKttttttttttKbr",
            "rbKTWWWTTWWWTKbr",
            "rNKTWPWTTWPWTKNr",
            "rNKTWWWTTWWWTKNr",
            "rbKTTTTTTTTTTKbr",
            "rbKTTKTTTTKTTKbr",
            "rbKTTTKKKKTTTKbr",
            "rbKddddddddddKbr",
            "rbbKKKKKKKKKKbbr",
            "rbbbbbbbbbbbbbbr",
            "rbbbbbbbbbbbbbbr",
            ".rrrrrrrrrrrrrr." } },
        { "tile20", new string[] {
            "..rrrrrrrrrrrrrrrr..",
            ".rbbbbbbbbbbbbbbbbr.",
            "rbbbbbbbbbbbbbbbbbbr",
            "rbbbbbbbbbbbbbbbbbbr",
            "rbbbKKKKKKKKKKKKbbbr",
            "rbbKttttttttttttKbbr",
            "rbbKTLWWLTTLWWLTKbbr",
            "rbNKTWPPWTTWPPWTKNbr",
            "rbNKTWPPWTTWPPWTKNbr",
            "rbbKTLWWLTTLWWLTKbbr",
            "rbbKTTTTTTTTTTTTKbbr",
            "rbbKTTTKTTTTKTTTKbbr",
            "rbbKTTTTKKKKTTTTKbbr",
            "rbbKTTTTTTTTTTTTKbbr",
            "rbbKddddddddddddKbbr",
            "rbbbKKKKKKKKKKKKbbbr",
            "rbbbbbbbbbbbbbbbbbbr",
            "rbbbbbbbbbbbbbbbbbbr",
            ".rbbbbbbbbbbbbbbbbr.",
            "..rrrrrrrrrrrrrrrr.." } },
        { "tile24", new string[] {
            "..rrrrrrrrrrrrrrrrrrrr..",
            ".rbbbbbbbbbbbbbbbbbbbbr.",
            "rbbbbbbbbbbKKbbbbbbbbbbr",
            "rbbbbbbbbbKAAKbbbbbbbbbr",
            "rbbbbbbbbbKAAKbbbbbbbbbr",
            "rbbbbbbbbbbssbbbbbbbbbbr",
            "rbbbbbbbbbbssbbbbbbbbbbr",
            "rbbbbbbbbbbssbbbbbbbbbbr",
            "rbbbKKKKKKKKKKKKKKKKbbbr",
            "rbbKttttttttttttttttKbbr",
            "rbbKTTTTTTTTTTTTTTTTKbbr",
            "rbbKTTTTTTTTTTTTTTTTKbbr",
            "rbNKTTLWWLTTTTLWWLTTKNbr",
            "rbNKTTWPPWTTTTWPPWTTKNbr",
            "rbNKTTWPPWTTTTWPPWTTKNbr",
            "rbbKTTLWWLTTTTLWWLTTKbbr",
            "rbbKTTTTTTTTTTTTTTTTKbbr",
            "rbbKTTTTTKTTTTKTTTTTKbbr",
            "rbbKTTTTTTKKKKTTTTTTKbbr",
            "rbbKTTTTTTTTTTTTTTTTKbbr",
            "rbbKddddddddddddddddKbbr",
            "rbbbKKKKKKKKKKKKKKKKbbbr",
            ".rbbbbbbbbbbbbbbbbbbbbr.",
            "..rrrrrrrrrrrrrrrrrrrr.." } },
        { "face16", new string[] {
            "................",
            ".KKKKKKKKKKKKKK.",
            "KttttttttttttttK",
            "KTTTTTTTTTTTTTTK",
            "KTTTTTTTTTTTTTTK",
            "KTLWWLTTTTLWWLTK",
            "KTWPPWTTTTWPPWTK",
            "KTWPPWTTTTWPPWTK",
            "KTLWWLTTTTLWWLTK",
            "KTTTTTTTTTTTTTTK",
            "KTTTTKTTTTKTTTTK",
            "KTTTTTKKKKTTTTTK",
            "KTTTTTTTTTTTTTTK",
            "KddddddddddddddK",
            ".KKKKKKKKKKKKKK.",
            "................" } },
        { "face20", new string[] {
            "....................",
            "....................",
            ".KKKKKKKKKKKKKKKKKK.",
            "KttttttttttttttttttK",
            "KTTTTTTTTTTTTTTTTTTK",
            "KTTTTTTTTTTTTTTTTTTK",
            "KTTTLWWLTTTTLWWLTTTK",
            "KTTTWPPWTTTTWPPWTTTK",
            "KTTTWPPWTTTTWPPWTTTK",
            "KTTTLWWLTTTTLWWLTTTK",
            "KTTTTTTTTTTTTTTTTTTK",
            "KTTTTTTTTTTTTTTTTTTK",
            "KTTTTTTKTTTTKTTTTTTK",
            "KTTTTTTTKKKKTTTTTTTK",
            "KTTTTTTTTTTTTTTTTTTK",
            "KTTTTTTTTTTTTTTTTTTK",
            "KddddddddddddddddddK",
            ".KKKKKKKKKKKKKKKKKK.",
            "....................",
            "...................." } },
        { "face24", new string[] {
            "........................",
            "........................",
            "........................",
            ".KKKKKKKKKKKKKKKKKKKKKK.",
            "KttttttttttttttttttttttK",
            "KTTTTTTTTTTTTTTTTTTTTTTK",
            "KTTTTTTTTTTTTTTTTTTTTTTK",
            "KTTTTTTTTTTTTTTTTTTTTTTK",
            "KTTLWWWWLTTTTTTLWWWWLTTK",
            "KTTWWPPWWTTTTTTWWPPWWTTK",
            "KTTWWPPWWTTTTTTWWPPWWTTK",
            "KTTLWWWWLTTTTTTLWWWWLTTK",
            "KTTTTTTTTTTTTTTTTTTTTTTK",
            "KTTTTTTTTTTTTTTTTTTTTTTK",
            "KTTTTTTTTTTTTTTTTTTTTTTK",
            "KTTTTTTTKTTTTTTKTTTTTTTK",
            "KTTTTTTTTKKKKKKTTTTTTTTK",
            "KTTTTTTTTTTTTTTTTTTTTTTK",
            "KTTTTTTTTTTTTTTTTTTTTTTK",
            "KddddddddddddddddddddddK",
            ".KKKKKKKKKKKKKKKKKKKKKK.",
            "........................",
            "........................",
            "........................" } },
    };

    static Bitmap FromPix(string v, int size)
    {
        string[] rows = Pix[(v == "C" ? "face" : "tile") + size];
        Dictionary<char, Color> pal = new Dictionary<char, Color>();
        pal['.'] = Color.Transparent;
        pal['r'] = v == "A" ? Gold : Ink;
        pal['b'] = v == "A" ? Ink : Gold;
        pal['s'] = v == "A" ? Straw : Ink;
        pal['K'] = Ink; pal['P'] = Ink;
        pal['T'] = Teal; pal['t'] = TealLight; pal['d'] = TealDark; pal['N'] = Knob;
        pal['L'] = Liner; pal['W'] = Eye; pal['A'] = Ball;
        Bitmap bmp = new Bitmap(size, size, PixelFormat.Format32bppArgb);
        for (int y = 0; y < size; y++)
        {
            if (rows[y].Length != size) throw new Exception("pixel row " + y + " of " + v + size + " is " + rows[y].Length + " wide");
            for (int x = 0; x < size; x++) bmp.SetPixel(x, y, pal[rows[y][x]]);
        }
        return bmp;
    }

    // Renders one candidate at one size, on a transparent background.
    public static Bitmap Render(string v, int size)
    {
        if (v.StartsWith("R")) return RevealArt.Render(v, size);
        if (size == 16 || size == 20 || size == 24) return FromPix(v, size);
        Bitmap bmp = new Bitmap(size, size, PixelFormat.Format32bppArgb);
        using (Graphics g = Graphics.FromImage(bmp))
        {
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.PixelOffsetMode = PixelOffsetMode.Half;
            g.CompositingQuality = CompositingQuality.HighQuality;
            g.Clear(Color.Transparent);
            int lod = Lod(size);
            float S = size;
            float outline = lod == 0 ? 1f : (lod == 1 ? Math.Max(1.5f, S * 0.045f) : S * 0.024f);

            if (v == "A" || v == "B")
            {
                // A tile in a UIStyle color: A is ink with a gold rim, B is gold.
                float m = lod == 0 ? 0f : S * 0.03f;
                float rr = S * 0.2f;
                Color fill = v == "A" ? Ink : Gold;
                using (GraphicsPath tile = RoundRect(m, m, S - 2 * m, S - 2 * m, rr))
                {
                    using (Brush b = new SolidBrush(fill)) g.FillPath(b, tile);
                    float rim = lod == 0 ? 1f : S * 0.03f;
                    Color rc = v == "A" ? Gold : Ink;
                    if (lod == 0)
                    {
                        using (GraphicsPath t2 = RoundRect(0.5f, 0.5f, S - 1f, S - 1f, rr))
                        using (Pen p = new Pen(rc, 1f)) g.DrawPath(p, t2);
                    }
                    else
                    {
                        using (GraphicsPath t2 = RoundRect(m + rim / 2f, m + rim / 2f, S - 2 * m - rim, S - 2 * m - rim, rr - rim / 2f))
                        using (Pen p = new Pen(rc, rim)) g.DrawPath(p, t2);
                    }
                }
                if (lod == 0)
                    Head(g, size, S / 2f, S * 0.53f, S * 0.78f, false, false, outline);
                else
                    Head(g, size, S / 2f, S * 0.59f, S * 0.62f, true, true, outline);
            }
            else if (v == "C")
            {
                // The box's front fills the icon: no tile, the face is the shape.
                float m = lod == 0 ? 0f : S * 0.035f;
                float w = S - 2 * m;
                float hh = w * 0.806f;
                // Keep it square-ish at icon sizes: stretch the box a little taller than the model.
                Head(g, size, S / 2f, S / 2f + (lod == 0 ? 0.5f : 0f), w, false, false, outline * (lod == 0 ? 1f : 1.3f));
            }
        }
        return bmp;
    }

    public static void SavePng(Bitmap b, string path) { b.Save(path, ImageFormat.Png); }

    // A preview sheet: each size at 1:1 on a light and a dark background, then 16, 24 and 32 zoomed.
    public static void Sheet(string[] variants, string path)
    {
        int[] sizes = new int[] { 16, 20, 24, 32, 48, 256 };
        int[] zooms = new int[] { 16, 24, 32 };
        int colW = 24;
        foreach (int s in sizes) colW += s + 24;
        colW += zooms.Length * (120 + 24);
        int rowH = 256 + 48;
        int W = colW, H = variants.Length * rowH * 2 + 40;
        using (Bitmap sheet = new Bitmap(W, H))
        using (Graphics g = Graphics.FromImage(sheet))
        {
            g.Clear(Color.White);
            g.InterpolationMode = InterpolationMode.NearestNeighbor;
            g.PixelOffsetMode = PixelOffsetMode.Half;
            using (Font f = new Font("Segoe UI", 14, FontStyle.Bold))
            {
                int y = 0;
                foreach (string v in variants)
                {
                    foreach (bool dark in new bool[] { false, true })
                    {
                        Color bg = dark ? ColorTranslator.FromHtml("#1F1F1F") : ColorTranslator.FromHtml("#F3F3F3");
                        using (Brush b = new SolidBrush(bg)) g.FillRectangle(b, 0, y, W, rowH);
                        using (Brush b = new SolidBrush(dark ? Color.White : Color.Black))
                            g.DrawString(v + (dark ? "  on dark" : "  on light"), f, b, 8, y + 6);
                        int x = 24;
                        foreach (int s in sizes)
                        {
                            using (Bitmap im = Render(v, s))
                                g.DrawImageUnscaled(im, x, y + rowH - 24 - s);
                            x += s + 24;
                        }
                        foreach (int z in zooms)
                        {
                            int zs = (120 / z) * z;
                            using (Bitmap im = Render(v, z)) g.DrawImage(im, x, y + rowH - 24 - zs, zs, zs);
                            x += 120 + 24;
                        }
                        y += rowH;
                    }
                }
            }
            sheet.Save(path, ImageFormat.Png);
        }
    }

    // The sheet my person picks from: one column per candidate, every image at real pixels.
    public static void CompareSheet(string[] variants, string[] names, string path, int zoomB = 24)
    {
        int colW = 360, pad = 20, W = variants.Length * colW;
        int H = 985;
        Color light = ColorTranslator.FromHtml("#F3F3F3"), dark = ColorTranslator.FromHtml("#202020");
        using (Bitmap sheet = new Bitmap(W, H))
        using (Graphics g = Graphics.FromImage(sheet))
        using (Font title = new Font("Segoe UI", 15, FontStyle.Bold))
        using (Font small = new Font("Segoe UI", 9))
        {
            g.Clear(Color.White);
            g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;
            for (int i = 0; i < variants.Length; i++)
            {
                string v = variants[i];
                int x0 = i * colW;
                int y = 0;
                using (Brush b = new SolidBrush(i % 2 == 0 ? Color.White : ColorTranslator.FromHtml("#FAFAFA"))) g.FillRectangle(b, x0, 0, colW, H);
                g.DrawString(names[i], title, Brushes.Black, x0 + pad, y + 10);
                y += 50;
                // 256 px, half on light and half on dark.
                using (Brush b = new SolidBrush(light)) g.FillRectangle(b, x0 + pad, y, (colW - 2 * pad) / 2, 296);
                using (Brush b = new SolidBrush(dark)) g.FillRectangle(b, x0 + pad + (colW - 2 * pad) / 2, y, (colW - 2 * pad) / 2, 296);
                using (Bitmap im = Render(v, 256)) g.DrawImageUnscaled(im, x0 + (colW - 256) / 2, y + 20);
                y += 296 + 16;
                // Every Windows size at 1:1 on light and dark.
                int[] sizes = new int[] { 16, 20, 24, 32, 40, 48, 64 };
                foreach (bool isDark in new bool[] { false, true })
                {
                    using (Brush b = new SolidBrush(isDark ? dark : light)) g.FillRectangle(b, x0 + pad, y, colW - 2 * pad, 84);
                    int x = x0 + pad + 8;
                    foreach (int s in sizes)
                    {
                        using (Bitmap im = Render(v, s)) g.DrawImageUnscaled(im, x, y + 76 - s);
                        x += s + 6;
                    }
                    y += 84;
                }
                g.DrawString("16  20  24  32  40  48  64 px, real size", small, Brushes.Gray, x0 + pad, y + 2);
                y += 24;
                // 16 and 24 zoomed, so each pixel shows.
                foreach (bool isDark in new bool[] { false, true })
                {
                    using (Brush b = new SolidBrush(isDark ? dark : light)) g.FillRectangle(b, x0 + pad, y, colW - 2 * pad, 112);
                    g.InterpolationMode = InterpolationMode.NearestNeighbor;
                    g.PixelOffsetMode = PixelOffsetMode.Half;
                    using (Bitmap im = Render(v, 16)) g.DrawImage(im, x0 + pad + 16, y + 8, 96, 96);
                    using (Bitmap im = Render(v, zoomB)) g.DrawImage(im, x0 + pad + 140, y + 8, 96, 96);
                    g.PixelOffsetMode = PixelOffsetMode.Default;
                    y += 112;
                }
                g.DrawString("16 px and " + zoomB + " px, zoomed", small, Brushes.Gray, x0 + pad, y + 2);
                y += 24;
                // A Windows 11 taskbar (24 px icons at 100%) and a title bar (16 px).
                foreach (bool isDark in new bool[] { false, true })
                {
                    Color bar = isDark ? ColorTranslator.FromHtml("#1C1C1C") : ColorTranslator.FromHtml("#EEEEEE");
                    Color chip = isDark ? ColorTranslator.FromHtml("#3A3A3A") : ColorTranslator.FromHtml("#D6D6D6");
                    using (Brush b = new SolidBrush(bar)) g.FillRectangle(b, x0 + pad, y, colW - 2 * pad, 48);
                    int cx = x0 + pad + 40;
                    for (int k = 0; k < 5; k++)
                    {
                        if (k == 2)
                        {
                            using (Brush b = new SolidBrush(Color.FromArgb(isDark ? 40 : 30, isDark ? Color.White : Color.Black)))
                                g.FillRectangle(b, cx - 8, y + 4, 40, 40);
                            using (Bitmap im = Render(v, 24)) g.DrawImageUnscaled(im, cx, y + 12);
                            using (Brush b = new SolidBrush(ColorTranslator.FromHtml("#4CC2FF"))) g.FillRectangle(b, cx + 4, y + 42, 16, 3);
                        }
                        else using (Brush b = new SolidBrush(chip)) g.FillRectangle(b, cx + 2, y + 14, 20, 20);
                        cx += 52;
                    }
                    y += 48;
                    Color tb = isDark ? ColorTranslator.FromHtml("#2B2B2B") : Color.White;
                    using (Brush b = new SolidBrush(tb)) g.FillRectangle(b, x0 + pad, y, colW - 2 * pad, 30);
                    using (Bitmap im = Render(v, 16)) g.DrawImageUnscaled(im, x0 + pad + 8, y + 7);
                    using (Brush b = new SolidBrush(isDark ? Color.White : Color.Black))
                        g.DrawString("No Humans On Set", small, b, x0 + pad + 32, y + 7);
                    y += 30 + 6;
                }
            }
            sheet.Save(path, ImageFormat.Png);
        }
    }

    // The Mac master at 1024 px: the tile on Apple's icon grid (an 824 px body at 100 px from each
    // edge), with a soft shadow under it, as macOS app icons are drawn since Big Sur.
    public static Bitmap MacMaster(string v)
    {
        Bitmap m = new Bitmap(1024, 1024, PixelFormat.Format32bppArgb);
        using (Graphics g = Graphics.FromImage(m))
        {
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.Clear(Color.Transparent);
            // A blur made of stacked, fading rounded rectangles.
            for (int i = 24; i >= 1; i--)
            {
                using (GraphicsPath p = RoundRect(100 - i, 100 - i + 14, 824 + 2 * i, 824 + 2 * i, 185 + i))
                using (Brush b = new SolidBrush(Color.FromArgb(5, 0, 0, 0))) g.FillPath(b, p);
            }
            // The Windows art's tile spans 28..996 of 1024; at 872 px it spans 24..848, so it
            // lands on 100..924 when drawn at 76.
            using (Bitmap art = Render(v, 872)) g.DrawImageUnscaled(art, 76, 76);
        }
        return m;
    }

    // Writes the Mac asset catalog that UE 5.8's Xcode build compiles as the app icon
    // (Build/Mac/Resources/Assets.xcassets/AppIcon.appiconset, ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon).
    public static void WriteMac(string v, string xcassets)
    {
        string set = Path.Combine(xcassets, "AppIcon.appiconset");
        Directory.CreateDirectory(set);
        File.WriteAllText(Path.Combine(xcassets, "Contents.json"),
            "{\n  \"info\" : {\n    \"author\" : \"xcode\",\n    \"version\" : 1\n  }\n}\n");
        int[] pts = new int[] { 16, 32, 128, 256, 512 };
        System.Text.StringBuilder json = new System.Text.StringBuilder();
        json.Append("{\n  \"images\" : [\n");
        using (Bitmap master = MacMaster(v))
        {
            bool first = true;
            foreach (int pt in pts)
                foreach (int scale in new int[] { 1, 2 })
                {
                    int px = pt * scale;
                    string name = "icon_" + pt + "x" + pt + (scale == 2 ? "@2x" : "") + ".png";
                    using (Bitmap b = new Bitmap(px, px, PixelFormat.Format32bppArgb))
                    {
                        using (Graphics g = Graphics.FromImage(b))
                        {
                            g.InterpolationMode = InterpolationMode.HighQualityBicubic;
                            g.PixelOffsetMode = PixelOffsetMode.HighQuality;
                            g.CompositingMode = CompositingMode.SourceCopy;
                            using (ImageAttributes ia = new ImageAttributes())
                            {
                                ia.SetWrapMode(WrapMode.TileFlipXY);
                                g.DrawImage(master, new Rectangle(0, 0, px, px), 0, 0, 1024, 1024, GraphicsUnit.Pixel, ia);
                            }
                        }
                        b.Save(Path.Combine(set, name), ImageFormat.Png);
                    }
                    if (!first) json.Append(",\n");
                    first = false;
                    json.Append("    {\n      \"filename\" : \"" + name + "\",\n      \"idiom\" : \"mac\",\n      \"scale\" : \"" + scale + "x\",\n      \"size\" : \"" + pt + "x" + pt + "\"\n    }");
                }
        }
        json.Append("\n  ],\n  \"info\" : {\n    \"author\" : \"xcode\",\n    \"version\" : 1\n  }\n}\n");
        File.WriteAllText(Path.Combine(set, "Contents.json"), json.ToString());
    }

    // Writes a Windows .ico: 32-bit DIB entries below 256 px, a PNG entry at 256 px.
    public static void WriteIco(string v, int[] sizes, string path)
    {
        List<byte[]> blobs = new List<byte[]>();
        foreach (int s in sizes)
        {
            using (Bitmap b = Render(v, s))
            {
                if (s >= 256)
                {
                    using (MemoryStream ms = new MemoryStream()) { b.Save(ms, ImageFormat.Png); blobs.Add(ms.ToArray()); }
                }
                else blobs.Add(Dib(b));
            }
        }
        using (FileStream fs = new FileStream(path, FileMode.Create))
        using (BinaryWriter w = new BinaryWriter(fs))
        {
            w.Write((ushort)0); w.Write((ushort)1); w.Write((ushort)sizes.Length);
            int offset = 6 + 16 * sizes.Length;
            for (int i = 0; i < sizes.Length; i++)
            {
                int s = sizes[i];
                w.Write((byte)(s >= 256 ? 0 : s)); w.Write((byte)(s >= 256 ? 0 : s));
                w.Write((byte)0); w.Write((byte)0);
                w.Write((ushort)1); w.Write((ushort)32);
                w.Write(blobs[i].Length); w.Write(offset);
                offset += blobs[i].Length;
            }
            foreach (byte[] d in blobs) w.Write(d);
        }
    }

    static byte[] Dib(Bitmap b)
    {
        int s = b.Width;
        int maskStride = ((s + 31) / 32) * 4;
        using (MemoryStream ms = new MemoryStream())
        using (BinaryWriter w = new BinaryWriter(ms))
        {
            w.Write(40); w.Write(s); w.Write(s * 2); w.Write((ushort)1); w.Write((ushort)32);
            w.Write(0); w.Write(s * s * 4 + maskStride * s); w.Write(0); w.Write(0); w.Write(0); w.Write(0);
            for (int y = s - 1; y >= 0; y--)
                for (int x = 0; x < s; x++)
                {
                    Color c = b.GetPixel(x, y);
                    w.Write(c.B); w.Write(c.G); w.Write(c.R); w.Write(c.A);
                }
            for (int y = s - 1; y >= 0; y--)
            {
                byte[] row = new byte[maskStride];
                for (int x = 0; x < s; x++)
                    if (b.GetPixel(x, y).A == 0) row[x / 8] |= (byte)(0x80 >> (x % 8));
                w.Write(row);
            }
            return ms.ToArray();
        }
    }
}
