#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TURANJ — the plate, opened out into a page that can be read.

Nothing is laid on top of the illumination. The writing lives in ground that
the illuminator reserved for it: one tall cusped panel of ivory, crossed by
bands of the plate's own scrolling vine. The bands are the dividers; the
reserves between them are the registers; the crowning turanj carries the seal.
"""
import os, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps, ImageFont

os.environ.setdefault("Q", "2.0")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import generate as G
import moroccan as M                    # canvas, fonts, text fitting, the seal

Q, CW, CH, CX, CY = M.Q, M.CW, M.CH, M.CX, M.CY
PW, PH, u = M.PW, M.PH, M.u
F, tracked, fit_block, fit_line, rtl_text = M.F, M.tracked, M.fit_block, M.fit_line, M.rtl_text
DISPLAY, BODY, BODY_SB, BODY_IT = M.DISPLAY, M.BODY, M.BODY_SB, M.BODY_IT
LABEL, ARABIC = M.LABEL, M.ARABIC
lerp, Painter = G.lerp, G.Painter

# --------------------------------------------------------------- pigments ---
INK        = (44,  30,  26)
NAVY       = (24,  32,  74)
NAVY_LT    = (58,  70, 122)
ROSE       = (224, 133, 132)
ROSE_DK    = (196, 100,  99)
ROSE_LT    = (238, 170, 162)
CRIMSON    = (140,  32,  44)
CRIMSON_DK = (94,   18,  30)
IVORY      = (247, 240, 224)
GOLD       = (198, 158,  82)
GOLD_LT    = (240, 218, 156)
GOLD_MD    = (222, 190, 118)
GOLD_DK    = (150, 112,  52)

TXT   = (62,  38,  30)
TXT_H = (124, 28,  40)
TXT_G = (146, 100, 44)
TXT_T = (150, 58,  62)
TXT_Q = (96,  60,  42)

# ---------------------------------------------------------------- geometry --
NT = 2600
def cusped_rect(a, b, n=6.0, lobes=48, depth=24.0, power=0.62, cx=None, cy=None):
    """A rounded rectangle with a scalloped edge - the plate's cusping, squared."""
    cx = PW / 2.0 if cx is None else cx
    cy = PH / 2.0 if cy is None else cy
    th = np.linspace(-np.pi / 2, 3 * np.pi / 2, NT, endpoint=False)
    r = ((np.abs(np.cos(th)) / a) ** n + (np.abs(np.sin(th)) / b) ** n) ** (-1.0 / n)
    p = np.stack([cx + r * np.cos(th), cy + r * np.sin(th)], 1)
    s = M.arclen(np.vstack([p, p[:1]]))[:-1]
    nv = M.normals(p)
    c = p.mean(0)
    nv *= np.sign(((p - c) * nv).sum(1))[:, None]        # outward
    k = np.abs(np.sin(np.pi * lobes * s)) ** power
    return p + nv * ((k - 1.0) * depth)[:, None]

def cartouche_band(x0, x1, yc, hh, lobes=26, depth=9.0, taper=0.46):
    """A horizontal illuminated band with lobed edges and tapered ends."""
    xs = np.linspace(x0, x1, 1100)
    s = (xs - x0) / (x1 - x0)
    prof = taper + (1.0 - taper) * np.sin(np.pi * s) ** 0.30
    k = np.abs(np.sin(np.pi * lobes * s)) ** 0.62
    h = hh * prof - (1.0 - k) * depth
    top = np.stack([xs, yc - h], 1)
    bot = np.stack([xs, yc + h], 1)
    return top, bot

class ArcBand:
    """Two curves paired by arc length, so ornament spaces evenly along them."""
    def __init__(self, outer, inner, n=1400, closed=False):
        o = np.asarray(outer, float); i = np.asarray(inner, float)
        if closed:
            o = np.vstack([o, o[:1]]); i = np.vstack([i, i[:1]])
        o = G.resample(o, n); i = G.resample(i, n)      # pair by each curve's own length
        mid = (o + i) / 2.0
        d = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(mid, axis=0), axis=1))]
        t = d / (d[-1] + 1e-9)
        tt = np.linspace(0, 1, n)
        idx = np.interp(tt, t, np.arange(len(t)))
        def samp(arr):
            lo = np.clip(np.floor(idx).astype(int), 0, len(arr) - 1)
            hi = np.clip(lo + 1, 0, len(arr) - 1)
            f = (idx - lo)[:, None]
            return arr[lo] * (1 - f) + arr[hi] * f
        self.o, self.i = samp(o), samp(i)
        self.mid = (self.o + self.i) / 2.0
        dd = self.o - self.i
        self.w = np.linalg.norm(dd, axis=1)
        self.n = dd / (self.w[:, None] + 1e-9)
        tv = np.gradient(self.mid, axis=0)
        self.t = tv / (np.linalg.norm(tv, axis=1, keepdims=True) + 1e-9)
        self.N = n

    def at(self, s):
        k = float(np.clip(s, 0.0, 1.0)) * (self.N - 1)
        i0 = int(np.floor(k)); i1 = min(i0 + 1, self.N - 1); f = k - i0
        mid = self.mid[i0] * (1 - f) + self.mid[i1] * f
        nv = self.n[i0] * (1 - f) + self.n[i1] * f
        tv = self.t[i0] * (1 - f) + self.t[i1] * f
        w = self.w[i0] * (1 - f) + self.w[i1] * f
        return mid, nv / (np.linalg.norm(nv) + 1e-9), tv / (np.linalg.norm(tv) + 1e-9), w

    def p(self, s, off):
        mid, nv, tv, w = self.at(s)
        return mid + nv * (off * w / 2.0), nv, tv, w

# ----------------------------------------------------------------- layout ---
MARG   = 148.0
FA, FB = PW / 2.0 - MARG, PH / 2.0 - MARG          # field half-extents
BORD_W = 140.0                                     # illuminated border band
PAN_A, PAN_B = 1232.0, 1966.0                      # ivory panel half-extents
PAN_LOBES, PAN_DEPTH = 32, 22.0
PAN_PAD = 66.0

SEQ = [("b", "ayah", 260.0), ("M",),
       ("b", "title", 560.0), ("E", 700.0),
       ("b", "when", 250.0), ("m",), ("b", "body", 370.0), ("M",),
       ("b", "sched", 430.0), ("M",),
       ("b", "venue", 285.0), ("m",), ("b", "rsvp", 295.0), ("m",),
       ("b", "web", 150.0)]
MAJ_H, MAJ_GAP = 88.0, 34.0
MIN_GAP, EMB_GAP = 40.0, 24.0

def stack():
    """Lay the registers, the illuminated bands and the fine rules end to end."""
    y0 = PH / 2.0 - PAN_B + PAN_PAD
    y1 = PH / 2.0 + PAN_B - PAN_PAD
    fixed = 0.0
    for it in SEQ:
        if it[0] == "M": fixed += MAJ_H + 2 * MAJ_GAP
        elif it[0] == "m": fixed += 2 * MIN_GAP
        elif it[0] == "E": fixed += it[1] + 2 * EMB_GAP
    k = (y1 - y0 - fixed) / sum(it[2] for it in SEQ if it[0] == "b")
    reg, majors, minors, emb, y = {}, [], [], None, y0
    for it in SEQ:
        if it[0] == "b":
            reg[it[1]] = (y, y + it[2] * k); y += it[2] * k
        elif it[0] == "M":
            y += MAJ_GAP; majors.append(y + MAJ_H / 2.0); y += MAJ_H + MAJ_GAP
        elif it[0] == "m":
            y += MIN_GAP; minors.append(y); y += MIN_GAP
        elif it[0] == "E":
            y += EMB_GAP; emb = (y, y + it[1]); y += it[1] + EMB_GAP
    return reg, majors, minors, emb

REG, MAJORS, MINORS, EMB = stack()
TXT_HW = PAN_A - PAN_DEPTH - PAN_PAD               # half-width for type
def box(name, frac=1.0, pad=0.0):
    y0, y1 = REG[name]
    hw = (TXT_HW - pad) * frac
    return (u(PW / 2.0 - hw), u(y0), u(PW / 2.0 + hw), u(y1))

# ------------------------------------------------------------------ paint ---
def paint(canvas, mask, tex, pool=0.20, feather=None):
    feather = u(8) if feather is None else feather
    sh = np.asarray(mask.filter(ImageFilter.GaussianBlur(feather)), np.float32) / 255.0
    a = np.asarray(tex, np.float32) * ((1 - pool) + pool * sh)[:, :, None]
    canvas.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), (0, 0), mask)
    del a, sh
    return canvas

def twofold_x(layer):
    q = Image.new("L", (CW, CH), 0)
    ImageDraw.Draw(q).rectangle([0, 0, CW // 2 - 1, CH - 1], fill=255)
    layer.putalpha(ImageChops.multiply(layer.split()[3], q))
    return Image.alpha_composite(layer, ImageOps.mirror(layer))

def pts(arr):
    return np.asarray(arr, float) * Q

def dress(pnt, outline, ink_w=3.0, pearl_gap=17.0, pearl_r=5.2, inset=13.0,
          gold_off=6.0, gold_w=1.8):
    pnt.outline(G.offset_inward(outline, -u(gold_off)), lerp(GOLD_DK, GOLD, .5), u(gold_w))
    pnt.outline(outline, INK, u(ink_w))
    pnt.pearls(G.offset_inward(outline, u(inset)), u(pearl_gap), u(pearl_r),
               NAVY, hl=lerp(NAVY_LT, IVORY, .35))

def ivory_ground(w, h, rng):
    return M.tadelakt(w, h, rng, stops=[(0.0, (232, 212, 176)), (0.34, (243, 229, 200)),
                                        (0.66, (250, 241, 222)), (1.0, (255, 250, 239))])

def mirror_half(layer, right=False):
    q = Image.new("L", (CW, CH), 0)
    d = ImageDraw.Draw(q)
    d.rectangle([CW // 2, 0, CW - 1, CH - 1] if right else [0, 0, CW // 2 - 1, CH - 1],
                fill=255)
    layer.putalpha(ImageChops.multiply(layer.split()[3], q))
    return Image.alpha_composite(layer, ImageOps.mirror(layer))

def circle(cx, cy, r, n=1800, start=-np.pi / 2):
    th = np.linspace(start, start + 2 * np.pi, n, endpoint=False)
    return np.stack([cx + r * np.cos(th), cy + r * np.sin(th)], 1)

# ------------------------------------------------------------------ build ---
def build():
    rng = np.random.default_rng(20260911)
    canvas = G.gold_ground(CW, CH, rng).convert("RGB")
    rose_tex = G.rose_ground(CW, CH, rng)

    # ---- the illuminated border ------------------------------------------
    bo = pts(cusped_rect(FA, FB, 6.0, 48, 26.0))
    bi = pts(cusped_rect(FA - BORD_W, FB - BORD_W, 6.0, 48, 26.0))
    m_border = ImageChops.subtract(G.poly_mask(bo), G.poly_mask(bi))
    canvas = paint(canvas, m_border, rose_tex, pool=0.22, feather=u(7))

    pb = Painter((CW, CH), rng)
    G.band_scroll(pb, ArcBand(bo, bi, 1700, closed=True), 0.0, 0.25, waves=4.0,
                  amp=0.46, ms=2.35, nvines=1, stem=1.05, big=True,
                  leaf_gap=0.046, serr=0.10, minor=True)
    orn = G.fourfold(pb.im)
    orn.putalpha(ImageChops.multiply(orn.split()[3], m_border))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), orn).convert("RGB")
    del pb, orn

    # ---- the reserved panel ----------------------------------------------
    po = pts(cusped_rect(PAN_A, PAN_B, 7.0, PAN_LOBES, PAN_DEPTH))
    m_pan = G.poly_mask(po)
    ivory_tex = ivory_ground(CW, CH, rng)
    canvas = paint(canvas, m_pan, ivory_tex, pool=0.16, feather=u(10))
    del ivory_tex

    # ---- gold on gold, in the ground the writing does not use -------------
    gp = Painter((CW, CH), rng)
    G.gold_tracery(gp, ArcBand(bi, po, 1500, closed=True), 0.0, 0.25,
                   waves=5.0, amp=0.42, ms=1.15)
    gl = G.fourfold(gp.im)
    zone = ImageChops.subtract(G.poly_mask(bi), m_pan)
    gl.putalpha(ImageChops.multiply(gl.split()[3], zone))
    gl.putalpha(gl.split()[3].point(lambda v: int(v * 0.96)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), gl).convert("RGB")
    del gp, gl

    # ---- the bands that divide the registers ------------------------------
    dx = PAN_A - PAN_DEPTH - 44.0
    def maj_edges(yc):
        return cartouche_band(PW / 2.0 - dx, PW / 2.0 + dx, yc, MAJ_H / 2.0,
                              lobes=22, depth=7.0)
    for yc in MAJORS:
        top, bot = maj_edges(yc)
        m_d = G.poly_mask(np.vstack([pts(top), pts(bot)[::-1]]))
        canvas = paint(canvas, m_d, rose_tex, pool=0.26, feather=u(4))
        dp = Painter((CW, CH), rng)
        G.band_scroll(dp, ArcBand(pts(top), pts(bot), 900), 0.0, 0.5, waves=4.0,
                      amp=0.44, ms=1.45, nvines=1, stem=0.9, big=True,
                      leaf_gap=0.050, serr=0.10, minor=False)
        dl = mirror_half(dp.im)
        dl.putalpha(ImageChops.multiply(dl.split()[3], m_d))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), dl).convert("RGB")
        del dp, dl

    # ---- the seal, riding a band of its own -------------------------------
    ey = sum(EMB) / 2.0
    eh = (EMB[1] - EMB[0]) / 2.0
    etop, ebot = cartouche_band(PW / 2.0 - dx, PW / 2.0 + dx, ey, eh * 0.48,
                                lobes=18, depth=8.0, taper=0.42)
    m_e = G.poly_mask(np.vstack([pts(etop), pts(ebot)[::-1]]))
    canvas = paint(canvas, m_e, rose_tex, pool=0.26, feather=u(5))
    ep = Painter((CW, CH), rng)
    G.band_scroll(ep, ArcBand(pts(etop), pts(ebot), 900), 0.0, 0.5, waves=4.0,
                  amp=0.44, ms=1.55, nvines=1, stem=0.95, big=True,
                  leaf_gap=0.048, serr=0.10, minor=False)
    el = mirror_half(ep.im)
    el.putalpha(ImageChops.multiply(el.split()[3], m_e))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), el).convert("RGB")
    del ep, el

    eR = eh * 0.98
    so = pts(G.Shape(16, 0.080, 0.70, R=eR, ky=1.0, cx=PW / 2.0, cy=ey).pts())
    si = pts(circle(PW / 2.0, ey, eR * 0.545))
    m_s = ImageChops.subtract(G.poly_mask(so), G.poly_mask(si))
    canvas = paint(canvas, m_s, rose_tex, pool=0.26, feather=u(5))
    sp = Painter((CW, CH), rng)
    rm = u(eR * 0.775)                      # a necklace, not a cramped scroll
    for k in range(16):
        a = -np.pi / 2 + k * np.pi / 8
        px, py = CX + rm * math.cos(a), u(ey) + rm * math.sin(a)
        if k % 2 == 0:
            sp.rosette(px, py, u(eR * 0.150), rot=np.pi / 8, ink_w=max(1.0, u(1.6)))
        else:
            sp.blossom(px, py, u(eR * 0.118), rot=0.3, pet=6,
                       pal=(lerp(ROSE_DK, CRIMSON, .45), IVORY),
                       ink_w=max(1.0, u(1.4)))
        b = a + np.pi / 16
        sp.dot(CX + u(eR * 0.945) * math.cos(b), u(ey) + u(eR * 0.945) * math.sin(b),
               max(1.0, u(eR * 0.020)), GOLD_DK)
        sp.dot(CX + u(eR * 0.610) * math.cos(b), u(ey) + u(eR * 0.610) * math.sin(b),
               max(1.0, u(eR * 0.018)), GOLD_DK)
    sp.im.putalpha(ImageChops.multiply(sp.im.split()[3], m_s))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), sp.im).convert("RGB")
    del sp

    # ---- rules, pearls, the gold sprinkling -------------------------------
    ov = Painter((CW, CH), rng)
    ds = ov.d
    reserved = ImageChops.lighter(ImageChops.lighter(m_e, m_s), G.poly_mask(si))
    for yc in MAJORS:
        t_, b_ = maj_edges(yc)
        reserved = ImageChops.lighter(
            reserved, G.poly_mask(np.vstack([pts(t_), pts(b_)[::-1]])))
    G.zarafshan(ds, ImageChops.subtract(m_pan, reserved),
                int(950 * Q * Q), rng, u(0.8), u(2.3),
                cols=(GOLD, GOLD_LT, lerp(GOLD, GOLD_LT, .5)))
    canvas.paste(Image.fromarray(
        (np.asarray(canvas, np.float32) * 1.05 + 8).clip(0, 255).astype(np.uint8)),
        (0, 0), G.poly_mask(si))
    ds.polygon([tuple(p) for p in si], fill=CRIMSON_DK)
    ds.polygon([tuple(p) for p in pts(circle(PW / 2.0, ey, eR * 0.545))], fill=CRIMSON)

    dress(ov, bo, 3.0, u(19) / Q, u(6.0) / Q, 14.0, 7.0, 2.0)
    ov.outline(bi, INK, u(2.6))
    ov.pearls(G.offset_inward(bi, -u(13)), u(18), u(5.4), NAVY,
              hl=lerp(NAVY_LT, IVORY, .35))
    dress(ov, po, 2.8, u(17) / Q, u(5.4) / Q, 13.0, 6.0, 1.8)
    for yc in MAJORS:
        top, bot = maj_edges(yc)
        out = np.vstack([pts(top), pts(bot)[::-1]])
        ov.outline(out, INK, u(2.2))
        ov.pearls(G.offset_inward(out, u(9)), u(14), u(4.2), NAVY,
                  hl=lerp(NAVY_LT, IVORY, .35))
    oe = np.vstack([pts(etop), pts(ebot)[::-1]])
    ov.outline(oe, INK, u(2.2))
    ov.pearls(G.offset_inward(oe, u(9)), u(14), u(4.2), NAVY,
              hl=lerp(NAVY_LT, IVORY, .35))
    for y in MINORS:                       # a hair rule where a band would shout
        x0, x1 = CX - u(dx * 0.80), CX + u(dx * 0.80)
        ds.line([x0, u(y), x1, u(y)], fill=lerp(GOLD_DK, GOLD, .45),
                width=max(1, int(u(2.0))))
        for sgn in (-1, 1):
            ds.ellipse([CX + sgn * u(dx * 0.80) - u(6), u(y) - u(6),
                        CX + sgn * u(dx * 0.80) + u(6), u(y) + u(6)], fill=GOLD_MD)
        ds.polygon([tuple(q) for q in M.khatim(CX, u(y), u(21), 0.45, 4, np.pi / 4)],
                   fill=CRIMSON, outline=lerp(GOLD_DK, INK, .4),
                   width=max(1, int(u(1.4))))
        ds.polygon([tuple(q) for q in M.khatim(CX, u(y), u(9), 0.45, 4, np.pi / 4)],
                   fill=GOLD_LT)
    ov.outline(so, INK, u(2.6))
    ov.pearls(G.offset_inward(so, u(11)), u(15), u(4.6), NAVY,
              hl=lerp(NAVY_LT, IVORY, .35))
    ov.outline(si, INK, u(2.6))
    ov.outline(pts(circle(PW / 2.0, ey, eR * 0.562)), lerp(GOLD_DK, GOLD, .5), u(2.2))
    ov.pearls(pts(circle(PW / 2.0, ey, eR * 0.602)), u(15), u(4.4), GOLD_MD, hl=GOLD_LT)
    ov.im.putalpha(ov.im.split()[3].point(lambda v: int(v * 0.95)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), ov.im).convert("RGB")
    del ov

    logo = M.load_logo(u(eR * 0.92))
    canvas.paste(logo, (int(CX - logo.width / 2), int(u(ey) - logo.height / 2)), logo)

    # ---- the ruled margin -------------------------------------------------
    jd = ImageDraw.Draw(canvas)
    def rule(inset, w, col):
        jd.rectangle([u(inset), u(inset), CW - u(inset) - 1, CH - u(inset) - 1],
                     outline=col, width=max(1, int(round(u(w)))))
    rule(MARG - 30, 3.0, lerp(GOLD_DK, INK, .45))
    rule(MARG - 44, 11.0, lerp(GOLD, GOLD_LT, .30))
    rule(MARG - 56, 1.8, lerp(GOLD_DK, INK, .5))
    rule(MARG - 82, 2.4, NAVY)
    rule(MARG - 94, 1.4, lerp(GOLD_DK, INK, .35))
    return canvas

# ---------------------------------------------------------------- writing ---
BLANK = os.environ.get("BLANK", "0") == "1"

def set_lines(d, bx, items, lead=0.40):
    """Fit a short stack of lines to a register and centre it. Cannot overflow."""
    x0, y0, x1, y1 = bx
    W, H = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2.0
    for it in items:
        it["size"] = fit_line(d, it["text"], it["font"], W * it.get("w", 1.0),
                              it["size"], tracking=it.get("tr", 0.0),
                              rtl=it.get("rtl", False))
    hs = [float(it["size"]) for it in items]
    gaps = [0.0] + [lead * (hs[i - 1] + hs[i]) / 2.0 * items[i].get("gap", 1.0)
                    for i in range(1, len(items))]
    total = sum(hs) + sum(gaps)
    if total > H:
        f = H / total
        hs = [h * f for h in hs]; gaps = [g * f for g in gaps]
        total = sum(hs) + sum(gaps)
    y = y0 + (H - total) / 2.0
    for it, h, g in zip(items, hs, gaps):
        y += g
        fnt = F(it["font"], max(6, int(round(h))))
        yc = y + h / 2.0
        if it.get("rtl"):   rtl_text(d, (cx, yc), it["text"], fnt, it["fill"])
        elif it.get("tr"):  tracked(d, it["text"], cx, yc, fnt, it["tr"], it["fill"])
        else: d.text((cx, yc), it["text"], font=fnt, fill=it["fill"], anchor="mm")
        y += h

def typeset(canvas):
    lay = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    C = M.CONTENT

    set_lines(d, box("ayah", pad=40), [
        dict(text=C["quote_ar"], font=ARABIC, size=u(100), fill=TXT_G, rtl=True, w=0.94),
        dict(text=C["quote_en"], font=BODY_IT, size=u(70), fill=TXT_Q, gap=0.9)],
        lead=0.34)

    set_lines(d, box("title", pad=30), [
        dict(text=C["title"][0], font=DISPLAY, size=u(150), fill=TXT_H, tr=u(10)),
        dict(text=C["title"][1], font=DISPLAY, size=u(150), fill=TXT_H, tr=u(10), gap=0.42),
        dict(text=C["subtitle"], font=BODY_IT, size=u(96), fill=TXT_G, gap=1.35, w=0.72),
        dict(text=C["title_ar"], font=ARABIC, size=u(96), fill=TXT_H, rtl=True,
             gap=1.05, w=0.70)], lead=0.40)

    y0, y1 = REG["when"]; h = y1 - y0; HW = TXT_HW
    for i, (lab, val) in enumerate(C["when"]):
        cx = CX + (-1 if i == 0 else 1) * u(HW * 0.50)
        tracked(d, lab, cx, u(y0 + h * 0.26), F(LABEL, u(38)), u(13), TXT_T)
        s = fit_line(d, val, BODY_SB, u(HW * 0.86), u(120))
        d.text((cx, u(y0 + h * 0.70)), val, font=F(BODY_SB, s), fill=TXT_H, anchor="mm")
    ym = (y0 + y1) / 2.0
    d.line([CX, u(y0 + h * 0.10), CX, u(ym - h * 0.16)], fill=lerp(GOLD_DK, GOLD, .45),
           width=max(1, int(u(2))))
    d.line([CX, u(ym + h * 0.16), CX, u(y1 - h * 0.10)], fill=lerp(GOLD_DK, GOLD, .45),
           width=max(1, int(u(2))))
    d.polygon([tuple(q) for q in M.khatim(CX, u(ym), u(17), 0.45, 4, np.pi / 4)],
              fill=CRIMSON)

    fit_block(d, C["body"], BODY, box("body", frac=0.90), u(88), TXT, lead=1.34)

    y0, y1 = REG["sched"]; h = y1 - y0; W = 2 * TXT_HW
    for i, (num, tm, desc) in enumerate(C["sched"]):
        cx = CX + u((i - 1) * W / 3.0)
        tracked(d, num, cx, u(y0 + h * 0.11), F(LABEL, u(34)), u(11), TXT_G)
        s = fit_line(d, tm, BODY_SB, u(W / 3.0 * 0.84), u(108))
        d.text((cx, u(y0 + h * 0.38)), tm, font=F(BODY_SB, s), fill=TXT_H, anchor="mm")
        fit_block(d, desc, BODY, (cx - u(W / 6.9), u(y0 + h * 0.57), cx + u(W / 6.9),
                                  u(y1 - h * 0.04)), u(64), TXT, lead=1.28)
    for s_ in (-1, 1):
        x = CX + s_ * u(W / 6.0)
        d.line([x, u(y0 + h * 0.06), x, u(y1 - h * 0.06)], fill=lerp(GOLD_DK, GOLD, .45),
               width=max(1, int(u(1.8))))
        d.polygon([tuple(q) for q in M.khatim(x, u(ym if False else (y0 + y1) / 2),
                                              u(15), 0.45, 4, np.pi / 4)], fill=CRIMSON)

    set_lines(d, box("venue", pad=30), [
        dict(text=C["venue"], font=DISPLAY, size=u(122), fill=TXT_H, tr=u(12), w=0.86),
        dict(text=C["venue_sub"], font=BODY_IT, size=u(70), fill=TXT_G, gap=0.8, w=0.6),
        dict(text=C["venue_addr"], font=LABEL, size=u(52), fill=TXT, tr=u(6),
             gap=0.9, w=0.94)], lead=0.40)

    set_lines(d, box("rsvp", pad=30), [
        dict(text=C["rsvp_label"], font=LABEL, size=u(36), fill=TXT_T, tr=u(15), w=0.8),
        dict(text=C["rsvp"], font=BODY_SB, size=u(118), fill=TXT_H, gap=1.0, w=0.82),
        dict(text=C["rsvp_note"], font=BODY_IT, size=u(62), fill=TXT_G, gap=0.9, w=0.6)],
        lead=0.38)

    set_lines(d, box("web"), [
        dict(text=C["web"], font=LABEL, size=u(38), fill=TXT_G, tr=u(15), w=0.7)])
    return Image.alpha_composite(canvas.convert("RGBA"), lay).convert("RGB")

def guide(canvas):
    lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    mm = 25.4 / 300.0
    f = ImageFont.truetype(os.path.join(M.FDIR, "Marcellus-400.ttf"), 46)
    for name, (y0, y1) in REG.items():
        x0, x1 = PW / 2.0 - TXT_HW, PW / 2.0 + TXT_HW
        d.rectangle([x0, y0, x1, y1], outline=(210, 40, 40, 235), width=4)
        d.rectangle([x0, y0, x1, y1], fill=(210, 40, 40, 24))
        d.text((x0 + 18, y0 + 12),
               f"{name.upper()}  x {int(x0)}-{int(x1)}  y {int(y0)}-{int(y1)} px"
               f"   ({(x1-x0)*mm:.0f} x {(y1-y0)*mm:.0f} mm)", font=f,
               fill=(140, 16, 16, 255))
    return Image.alpha_composite(canvas.convert("RGBA"), lay).convert("RGB")

def main():
    rng = np.random.default_rng(4801)
    im = build()
    if not BLANK: im = typeset(im)
    im = M.finish(im, rng)
    if os.environ.get("GUIDE", "0") == "1": im = guide(im)
    out = os.environ.get("OUT", "turanj-poster" + ("-blank" if BLANK else ""))
    im.save(out + ".png", "PNG", dpi=(300, 300))
    if os.environ.get("PDF", "0") == "1":
        im.save(out + ".pdf", "PDF", resolution=300.0)
    print("wrote", out + ".png", im.size)

if __name__ == "__main__":
    main()
