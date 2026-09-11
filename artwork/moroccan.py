#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DAR AL-DHIKR — a Moroccan poster base.

The text does not sit ON the ornament; the ornament is BUILT AROUND it.
A zellij border encloses a carved-stucco field; a polylobed mihrab niche
stands in the field, and every line of type occupies a register of that
niche, divided by gold interlace and khatim knots. Nothing floats.
"""
import os, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps, ImageFont

os.environ.setdefault("Q", "2.0")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import generate as G                                   # motif + texture engine

# ---------------------------------------------------------------- canvas ----
Q = G.Q
PW, PH = 3508, 4961                                    # A3 at 300 dpi
G.PW, G.PH = PW, PH
G.CW = int(PW * Q) // 2 * 2
G.CH = int(PH * Q) // 2 * 2
G.CX, G.CY = G.CW / 2.0, G.CH / 2.0
CW, CH, CX, CY = G.CW, G.CH, G.CX, G.CY
u = G.u
RNG = np.random.default_rng(31415)

lerp = G.lerp
Painter = G.Painter

# --------------------------------------------------------------- palette ----
INK        = (40,  26,  22)
GOLD       = (196, 156,  80)
GOLD_LT    = (244, 226, 172)
GOLD_MD    = (222, 190, 118)
GOLD_DK    = (140, 100,  44)

NIGHT      = (10,  20,  44)
INDIGO     = (20,  38,  78)
INDIGO_LT  = (38,  68, 122)
TEAL       = (22,  96, 118)
TEAL_LT    = (64, 156, 166)
TERRA      = (162,  62,  44)
TERRA_DK   = (112,  38,  30)

ROSE       = (223, 133, 131)
ROSE_DK    = (192,  96,  96)
ROSE_LT    = (238, 172, 164)
CRIMSON    = (138,  30,  42)
CRIMSON_DK = (92,  16,  28)
CREAM      = (242, 231, 208)
CREAM_DK   = (219, 201, 168)
CREAM_LT   = (251, 245, 230)
IVORY      = (250, 241, 222)
GREEN      = (30,  92,  74)

THEME = os.environ.get("THEME", "rose").lower()
_P = {
  "indigo": dict(
     strip_bg=INDIGO, star_inner=TERRA, saft_a=TEAL, saft_b=TEAL_LT,
     saft_dot=GOLD_LT, band_w=0.0, band=None, damask=INDIGO_LT, damask_a=44,
     knot_dot=TERRA, col_alt=(TERRA, TEAL), logo_disc=None, shadow=0.46,
     course=1.075, txt=(251, 245, 230), txt_h=(251, 245, 230),
     txt_g=(238, 214, 156), txt_t=(126, 196, 200),
     body=(226, 234, 240), addr=(206, 220, 230), quote=(214, 226, 232)),
  "rose": dict(
     strip_bg=ROSE, star_inner=CRIMSON, saft_a=CREAM, saft_b=ROSE_LT,
     saft_dot=CRIMSON, band_w=66.0, band="rose", damask=ROSE_DK, damask_a=40,
     knot_dot=CRIMSON, col_alt=(CRIMSON, ROSE_DK), logo_disc=CRIMSON_DK,
     shadow=0.34, course=0.978,
     txt=(62, 38, 30), txt_h=(124, 28, 40), txt_g=(146, 100, 44),
     txt_t=(150, 58, 62), body=(70, 46, 36), addr=(96, 62, 46),
     quote=(96, 60, 42)),
}[THEME]

STRIP_BG   = _P["strip_bg"]
STAR_INNER = _P["star_inner"]
SAFT_A, SAFT_B, SAFT_DOT = _P["saft_a"], _P["saft_b"], _P["saft_dot"]
BAND_W     = _P["band_w"]
DAMASK, DAMASK_A = _P["damask"], _P["damask_a"]
KNOT_DOT   = _P["knot_dot"]
COL_ALT    = _P["col_alt"]
LOGO_DISC  = _P["logo_disc"]
SHADOW     = _P["shadow"]
COURSE     = _P["course"]
ROSEY      = THEME == "rose"

# ----------------------------------------------------------------- fonts ----
FDIR = os.path.join(HERE, "fonts")
_FC = {}
def F(name, size):
    key = (name, int(size))
    if key not in _FC:
        _FC[key] = ImageFont.truetype(os.path.join(FDIR, name), max(1, int(size)))
    return _FC[key]

DISPLAY   = "Cinzel-600.ttf"
DISPLAY_B = "Cinzel-700.ttf"
BODY      = "Cormorant-400.ttf"
BODY_SB   = "Cormorant-600.ttf"
BODY_IT   = "Cormorant-400i.ttf"
LABEL     = "Marcellus-400.ttf"
ARABIC    = "Amiri-400.ttf"
ARABIC_B  = "Amiri-700.ttf"

def ar(s):
    """Pillow is built with raqm, which shapes and orders Arabic itself."""
    return s

# ------------------------------------------------------------ text layout ---
def _tw(d, s, f, rtl=False):
    return d.textlength(s, font=f, direction="rtl" if rtl else None)

def tracked(d, s, cx, cy, f, sp, fill, anchor="mm"):
    """Letterspaced line, centred on (cx, cy)."""
    ws = [_tw(d, ch, f) for ch in s]
    total = sum(ws) + sp * (len(s) - 1)
    x = cx - total / 2.0
    for ch, w in zip(s, ws):
        d.text((x, cy), ch, font=f, fill=fill, anchor="lm")
        x += w + sp
    return total

def wrap(d, text, f, maxw):
    out, line = [], ""
    for word in text.split():
        t = (line + " " + word).strip()
        if _tw(d, t, f) <= maxw or not line:
            line = t
        else:
            out.append(line); line = word
    if line: out.append(line)
    return out

def fit_block(d, text, fname, box, size, fill, lead=1.28, align="c",
              minsize=8, tracking=0.0):
    """Wrap and shrink until the paragraph fits the box. Returns (h, size)."""
    x0, y0, x1, y1 = box
    W, H = x1 - x0, y1 - y0
    s = size
    while s > minsize:
        f = F(fname, s)
        lines = []
        for para in text.split("\n"):
            lines += wrap(d, para, f, W) if para.strip() else [""]
        lh = s * lead
        if lh * len(lines) <= H: break
        s -= max(1, int(s * 0.04))
    f = F(fname, s)
    lines = []
    for para in text.split("\n"):
        lines += wrap(d, para, f, W) if para.strip() else [""]
    lh = s * lead
    total = lh * len(lines)
    y = y0 + (H - total) / 2.0 + lh / 2.0
    for ln in lines:
        if tracking:
            tracked(d, ln, (x0 + x1) / 2.0, y, f, tracking, fill)
        else:
            cx = (x0 + x1) / 2.0 if align == "c" else x0
            d.text((cx, y), ln, font=f, fill=fill,
                   anchor="mm" if align == "c" else "lm")
        y += lh
    return total, s

def fit_line(d, text, fname, maxw, size, minsize=8, tracking=0.0, rtl=False):
    """Largest size at or below `size` whose single line fits maxw."""
    s = size
    while s > minsize:
        f = F(fname, s)
        w = _tw(d, text, f, rtl) + tracking * max(0, len(text) - 1)
        if w <= maxw: break
        s -= max(1, int(s * 0.035))
    return s

def rtl_text(d, xy, text, font, fill):
    d.text(xy, text, font=font, fill=fill, anchor="mm", direction="rtl")

# -------------------------------------------------------------- geometry ----
def khatim(cx, cy, R, ratio=0.585, points=8, rot=0.0):
    """The eight-pointed seal-of-Solomon star that governs Moroccan zellij."""
    n = points * 2
    a = np.arange(n) * np.pi / points + rot
    r = np.where(np.arange(n) % 2 == 0, R, R * ratio)
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)

def saft(cx, cy, R, ratio=0.42, rot=np.pi / 4):
    """The four-armed cross that fills between the stars."""
    return khatim(cx, cy, R, ratio, 4, rot)

def superellipse(a, b, n, cx=None, cy=None, th=None):
    th = G.TH if th is None else th
    cx = CX if cx is None else cx
    cy = CY if cy is None else cy
    r = ((np.abs(np.cos(th)) / a) ** n + (np.abs(np.sin(th)) / b) ** n) ** (-1.0 / n)
    return np.stack([cx + r * np.cos(th), cy + r * np.sin(th)], 1)

def arclen(p):
    d = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    return d / (d[-1] + 1e-9)

def normals(p, closed=False):
    t = np.gradient(p, axis=0)
    n = np.stack([t[:, 1], -t[:, 0]], 1)
    return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)

def scallop_open(p, lobes, depth, power=0.62, outward=-1.0):
    """Cut `lobes` lobes into an open curve: cusps at the joins, full at the
    centres.  s = 0 and s = 1 land on cusps, so it springs cleanly."""
    p = G.resample(p, max(400, len(p)))
    s = arclen(p)
    nv = normals(p) * outward
    k = np.abs(np.sin(np.pi * lobes * s)) ** power
    return p + nv * ((k - 1.0) * depth)[:, None]

def arch_curve(cx, hw, y_spring, rise, k=2.35, n=600, horseshoe=0.0):
    """Half of a full, slightly stilted Moorish arch, left springing to right."""
    t = np.linspace(-1.0, 1.0, n)
    x = cx + hw * t
    y = y_spring - rise * (1.0 - np.abs(t) ** k) ** (1.0 / k)
    if horseshoe:                      # let the haunches swell below the spring
        y = y + horseshoe * rise * np.clip(np.abs(t) - 0.72, 0, None) ** 1.6 * 9.0
    return np.stack([x, y], 1)

def niche_outline(cx, hw, y_top, y_spring, y_base, lobes=11, depth=None,
                  k=2.35, foot=None):
    """Arch head + straight jambs + a stepped foot, as one closed form."""
    depth = hw * 0.052 if depth is None else depth
    foot = hw * 0.055 if foot is None else foot
    head = arch_curve(cx, hw, y_spring, y_spring - y_top, k=k)
    head = scallop_open(head, lobes, depth)
    right = np.stack([np.full(40, cx + hw),
                      np.linspace(y_spring, y_base - foot, 40)], 1)
    base = np.array([[cx + hw, y_base - foot], [cx + hw + foot * 0.55, y_base - foot],
                     [cx + hw + foot * 0.55, y_base],
                     [cx - hw - foot * 0.55, y_base],
                     [cx - hw - foot * 0.55, y_base - foot],
                     [cx - hw, y_base - foot]])
    left = np.stack([np.full(40, cx - hw),
                     np.linspace(y_base - foot, y_spring, 40)], 1)
    return np.vstack([head, right, base, left])

def rounded_rect(x0, y0, x1, y1, r, n=24):
    pts = []
    for (cx_, cy_, a0) in ((x1 - r, y0 + r, -np.pi / 2), (x1 - r, y1 - r, 0.0),
                           (x0 + r, y1 - r, np.pi / 2), (x0 + r, y0 + r, np.pi)):
        a = np.linspace(a0, a0 + np.pi / 2, n)
        pts.append(np.stack([cx_ + r * np.cos(a), cy_ + r * np.sin(a)], 1))
    return np.vstack(pts)

def lobed_tablet(cx, cy, hw, hh, lobes=9, depth=None, corner=None):
    """A cartouche: straight flanks, lobed ends - a real inlaid plaque."""
    depth = hh * 0.16 if depth is None else depth
    corner = hh * 0.34 if corner is None else corner
    base = rounded_rect(cx - hw, cy - hh, cx + hw, cy + hh, corner, 40)
    base = G.resample(base, 900)
    s = arclen(base)
    nv = normals(base)
    k = np.abs(np.sin(np.pi * lobes * s * 2.0)) ** 0.7
    return base - nv * ((k - 1.0) * depth)[:, None] * -1.0

# ------------------------------------------------------------------ logo ----
def load_logo(px, tint=(GOLD_LT, GOLD_MD, GOLD_DK)):
    """Key the emblem off its black disc and re-cast it in leaf gold."""
    src = Image.open(os.path.join(HERE, "logo-khatim.png")).convert("RGBA")
    a = np.asarray(src, np.float32)
    lum = (a[..., 0] * 0.30 + a[..., 1] * 0.59 + a[..., 2] * 0.11) / 255.0
    alpha = np.clip((lum - 0.14) / 0.52, 0, 1) * (a[..., 3] / 255.0)
    h, w = alpha.shape
    g = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    c0, c1, c2 = (np.array(c, np.float32) for c in tint)
    col = np.where(g[..., None] < 0.5,
                   c0 * (1 - g * 2)[..., None] + c1 * (g * 2)[..., None],
                   c1 * (2 - g * 2)[..., None] + c2 * (g * 2 - 1)[..., None])
    col = np.broadcast_to(col, (h, w, 3)).copy()
    out = np.dstack([col, alpha * 255.0]).astype(np.uint8)
    im = Image.fromarray(out, "RGBA")
    return im.resize((int(px), int(px * src.height / src.width)), Image.LANCZOS)

# ---------------------------------------------------------------- grounds ---
def tadelakt(w, h, rng, base=CREAM, stops=None):
    """Polished lime plaster: warm, faintly clouded, never flat."""
    sw, sh = w // 3, h // 3
    n1 = G.fbm(sh, sw, 6, sw / 2.4, rng=rng)
    n2 = G.fbm(sh, sw, 5, sw / 8.0, rng=rng)
    t = 0.52 + 0.20 * (n1 - 0.5) + 0.26 * (n2 - 0.5)
    stops = stops or [(0.0, (206, 184, 148)), (0.35, (228, 212, 182)),
                      (0.65, tuple(base)), (1.0, (252, 246, 232))]
    rgb = G.ramp(t, stops)
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    a = np.asarray(img, np.float32)
    grain = rng.normal(0, 3.0, (h, w)).astype(np.float32)
    grain = np.asarray(Image.fromarray(np.clip(grain * 12 + 128, 0, 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.7)), np.float32)
    a += ((grain - 128) / 12.0)[:, :, None] * np.array([1.1, 1.0, 0.82], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def field_ground(w, h, rng):
    """What the whole sheet is made of."""
    if not ROSEY: return tadelakt(w, h, rng)
    a = np.asarray(G.gold_ground(w, h, rng), np.float32) * 0.955
    a[:, :, 2] *= 0.965
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def panel_ground(w, h, rng):
    """The ground of the niche - the surface the writing sits on."""
    if ROSEY:
        return tadelakt(w, h, rng, stops=[(0.0, (234, 214, 176)),
                                          (0.34, (245, 231, 202)),
                                          (0.66, (252, 243, 223)),
                                          (1.0, (255, 251, 241))])
    return night_ground(w, h, rng)

def night_ground(w, h, rng):
    """The indigo of the niche - lapis over dark plaster."""
    sw, sh = w // 3, h // 3
    n1 = G.fbm(sh, sw, 6, sw / 2.0, rng=rng)
    n2 = G.fbm(sh, sw, 5, sw / 7.0, rng=rng)
    t = 0.5 + 0.34 * (n1 - 0.5) + 0.34 * (n2 - 0.5)
    stops = [(0.0, (6, 12, 30)), (0.35, (12, 24, 52)),
             (0.7, (20, 38, 78)), (1.0, (34, 58, 106))]
    rgb = G.ramp(t, stops)
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    a = np.asarray(img, np.float32)
    grain = rng.normal(0, 3.4, (h, w)).astype(np.float32)
    grain = np.asarray(Image.fromarray(np.clip(grain * 11 + 128, 0, 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.7)), np.float32)
    a += ((grain - 128) / 11.0)[:, :, None] * np.array([0.8, 0.9, 1.2], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def gold_leaf(w, h, rng):
    """Beaten leaf: laid in squares, overlapped at the seams, lightly crazed."""
    sw, sh = w // 3, h // 3
    n1 = G.fbm(sh, sw, 6, sw / 2.2, rng=rng)
    n2 = G.fbm(sh, sw, 5, sw / 6.0, rng=rng)
    t = 0.5 + 0.42 * np.sin(5.2 * n1 + 3.1 * n2) * 0.5 + 0.3 * (n2 - 0.5)

    leaf = max(10, int(u(840) / 3))                       # a leaf is about 70 mm
    ys, xs = np.mgrid[0:sh, 0:sw]
    cy, cx = ys // leaf, xs // leaf
    tone = np.modf(np.sin(cx * 12.9898 + cy * 78.233) * 43758.5453)[0]
    t = t + (tone - 0.5) * 0.085                          # each leaf sits differently
    ox = np.modf(np.sin(cy * 31.7 + 7.3) * 1237.0)[0] * leaf * 0.12
    seam = (((xs - ox) % leaf) < 2.2) | ((ys % leaf) < 2.2)
    t = t + seam * 0.055                                  # the overlap catches light
    del ys, xs, cy, cx, tone, ox, seam

    crz = G.fbm(sh, sw, 4, sw / 30.0, rng=rng)            # crazing in the size
    t = t - (np.abs(crz - 0.5) < 0.010) * 0.20
    del crz

    stops = [(0.0, (120, 82, 30)), (0.28, (168, 124, 52)), (0.52, (206, 166, 90)),
             (0.75, (236, 208, 144)), (1.0, (252, 240, 200))]
    rgb = G.ramp(t, stops)
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    a = np.asarray(img, np.float32)
    st = G._vnoise(h, w, max(2.0, u(1.8)), rng)           # the burnisher's strokes
    st = np.asarray(Image.fromarray((st * 255).astype(np.uint8))
                    .filter(ImageFilter.GaussianBlur(u(0.6))), np.float32) / 255.0
    a += ((st - 0.5) * 16.0)[:, :, None] * np.array([1.0, 0.86, 0.5], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

# ------------------------------------------------------------- inlay work ---
def inlay(canvas, mask, paint, shadow=True, sh_off=None, sh_blur=None, sh_amt=0.42):
    """Set a shape into the surface: cast shadow first, then the material."""
    if shadow:
        off = int(u(7)) if sh_off is None else int(sh_off)
        blur = u(11) if sh_blur is None else sh_blur
        sm = mask.filter(ImageFilter.GaussianBlur(blur))
        sm = ImageChops.offset(sm, off, off)
        a = np.asarray(canvas, np.float32)
        k = (np.asarray(sm, np.float32) / 255.0 * sh_amt)[:, :, None]
        canvas.paste(Image.fromarray(np.clip(a * (1 - k), 0, 255).astype(np.uint8)), (0, 0))
    canvas.paste(paint, (0, 0), mask)
    return canvas

def band_mask(outline, width):
    o = G.poly_mask(outline)
    i = G.poly_mask(G.offset_inward(outline, width))
    return ImageChops.subtract(o, i), i

def bevel(canvas, mask, up=0.30, down=0.34, r=None):
    """A soft light/shade rim so a form reads as carved, not printed."""
    r = u(6.5) if r is None else r
    m = np.asarray(mask, np.float32) / 255.0
    b = np.asarray(mask.filter(ImageFilter.GaussianBlur(r)), np.float32) / 255.0
    hi = np.clip(m - np.asarray(ImageChops.offset(mask, int(u(4)), int(u(4)))
                                .filter(ImageFilter.GaussianBlur(r)), np.float32) / 255.0, 0, 1)
    lo = np.clip(m - np.asarray(ImageChops.offset(mask, -int(u(4)), -int(u(4)))
                                .filter(ImageFilter.GaussianBlur(r)), np.float32) / 255.0, 0, 1)
    a = np.asarray(canvas, np.float32)
    a = a * (1.0 + up * hi[:, :, None]) * (1.0 - down * lo[:, :, None])
    canvas.paste(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), (0, 0))
    return canvas

# ---------------------------------------------------------------- layout ----
TRIM = 44.0
BS0, BS1 = 60.0, 223.0                    # zellij strip, outer and inner edge
FLD = 249.0                               # the plaster field begins
PIL_HW, PIL_BAND = 74.0, 14.0             # the flanking arcade
NCX = PW / 2.0
NHW = 1310.0                              # niche half width
NTOP, NSPR, NBASE = 290.0, 1600.0, 4645.0
FRAME = 40.0                              # gold band around the niche
INSET = FRAME + BAND_W                    # frame + any colour band inside it
PAD = 78.0                                # text inset from the band

REG = {                                   # every line of type owns a register
    "quote": (420.0, 732.0),
    "title": (792.7, 1481.6),
    "logo":  (1542.3, 2105.7),
    "when":  (2172.8, 2465.3),
    "body":  (2528.2, 2952.9),
    "sched": (3015.7, 3579.0),
    "venue": (3641.8, 3958.2),
    "rsvp":  (4023.1, 4359.0),
    "web":   (4413.2, 4549.7),
}
MAJOR = [1512.0, 2140.4, 2495.6, 3620.2, 3992.8]      # interlace rules + knot
MINOR = [760.1, 2983.2, 4387.1]                        # hairline + lozenge

def niche_at(t, lobes=9):
    """The niche outline inset by t page units, drawn concentrically."""
    hw = NHW - t
    return niche_outline(u(NCX), u(hw), u(NTOP + t * 0.94), u(NSPR), u(NBASE - t),
                         lobes=lobes, depth=u(hw * 0.064), foot=u(max(6.0, 58.0 - t)))

def niche_hw_at(y):
    """Interior half-width of the niche at height y."""
    if y >= NSPR: return NHW
    rise = NSPR - NTOP
    f = np.clip((NSPR - y) / rise, 0, 1)
    k = 2.35
    v = max(0.0, 1.0 - f ** k)
    return NHW * (v ** (1.0 / k))

def text_box(y0, y1, pad=None, frac=1.0):
    """Canvas-pixel box inscribed in the niche between two heights."""
    pad = PAD if pad is None else pad
    hw = (min(niche_hw_at(y0), niche_hw_at(y1)) - INSET - pad) * frac
    return (u(NCX - hw), u(y0), u(NCX + hw), u(y1))

# ---------------------------------------------------------------- zellij ----
def zellij(canvas, rng):
    """A cut border. Every piece is laid by hand, so none of them match."""
    lay = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    tiles = Image.new("L", (CW, CH), 0)                 # the pieces, for relief
    dt = ImageDraw.Draw(tiles)
    strip = Image.new("L", (CW, CH), 0)
    ds = ImageDraw.Draw(strip)
    ds.rectangle([u(BS0), u(BS0), CW - u(BS0) - 1, CH - u(BS0) - 1], fill=255)
    ds.rectangle([u(BS1), u(BS1), CW - u(BS1) - 1, CH - u(BS1) - 1], fill=0)

    joint = lerp(STRIP_BG, INK, 0.38)                   # the bed they are set in
    d.rectangle([u(BS0), u(BS0), CW - u(BS0) - 1, CH - u(BS0) - 1],
                fill=STRIP_BG + (255,))

    C = (BS0 + BS1) / 2.0
    R = u((BS1 - BS0) / 2.0 - 3.0)
    x0, x1 = u(C), CW - u(C)
    y0, y1 = u(C), CH - u(C)
    nh = max(2, int(round((x1 - x0) / (2 * R))))
    nv = max(2, int(round((y1 - y0) / (2 * R))))
    ph, pv = (x1 - x0) / nh, (y1 - y0) / nv

    nodes, mids = [], []
    for i in range(nh + 1):
        nodes += [(x0 + i * ph, y0), (x0 + i * ph, y1)]
    for j in range(1, nv):
        nodes += [(x0, y0 + j * pv), (x1, y0 + j * pv)]
    for i in range(nh):
        mids += [(x0 + (i + .5) * ph, y0), (x0 + (i + .5) * ph, y1)]
    for j in range(nv):
        mids += [(x0, y0 + (j + .5) * pv), (x1, y0 + (j + .5) * pv)]

    jz = u(1.7)
    lw = max(1, int(u(1.6)))
    def tone(c, k):
        return tuple(int(np.clip(v * (1.0 + 0.062 * k), 0, 255)) for v in c)
    def poly(dr, pp, **kw):
        dr.polygon([tuple(q) for q in pp], **kw)

    for (mx, my) in mids:                                   # the crosses
        k = float(rng.normal()) * 0.8
        rot = np.pi / 4 + float(rng.normal()) * 0.017
        mx += float(rng.normal()) * jz; my += float(rng.normal()) * jz
        poly(d, saft(mx, my, R * 0.91, 0.34, rot), fill=joint + (255,))
        poly(d, saft(mx, my, R * 0.86, 0.34, rot), fill=tone(SAFT_A, k) + (255,),
             outline=GOLD_DK + (255,), width=lw)
        poly(d, saft(mx, my, R * 0.60, 0.34, rot), fill=tone(SAFT_B, k) + (255,))
        d.ellipse([mx - R * .10, my - R * .10, mx + R * .10, my + R * .10],
                  fill=SAFT_DOT + (255,))
        poly(dt, saft(mx, my, R * 0.88, 0.34, rot), fill=255)

    for (sx, sy) in nodes:                                  # the seals
        k = float(rng.normal()) * 0.8
        rot = float(rng.normal()) * 0.015
        sx += float(rng.normal()) * jz; sy += float(rng.normal()) * jz
        poly(d, khatim(sx, sy, R * 1.030, 0.585, rot=rot), fill=joint + (255,))
        poly(d, khatim(sx, sy, R, 0.585, rot=rot), fill=tone(GOLD, k) + (255,))
        poly(d, khatim(sx, sy, R * 0.90, 0.585, rot=rot), fill=tone(CREAM, k) + (255,))
        poly(d, khatim(sx, sy, R * 0.56, 0.585, rot=rot + np.pi / 8),
             fill=tone(STAR_INNER, k) + (255,))
        poly(d, khatim(sx, sy, R * 0.30, 0.585, rot=rot), fill=GOLD_LT + (255,))
        d.ellipse([sx - R * .10, sy - R * .10, sx + R * .10, sy + R * .10],
                  fill=lerp(STAR_INNER, INK, .45) + (255,))
        poly(dt, khatim(sx, sy, R * 1.012, 0.585, rot=rot), fill=255)

    lay.putalpha(ImageChops.multiply(lay.split()[3], strip))
    tiles = ImageChops.multiply(tiles, strip)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), lay).convert("RGB")
    del lay, d, dt

    # glaze: granulation, a little crazing, and the light each piece catches
    a = np.asarray(canvas, np.float32)
    m = (np.asarray(strip, np.float32) / 255.0)[:, :, None]
    tf = np.asarray(tiles, np.float32) / 255.0
    gl = _field(CH, CW, CW // 3, CH // 3, rng)
    cz = G.fbm(CH // 3, CW // 3, 4, CW / 44.0, rng=rng)
    cz = np.asarray(Image.fromarray((cz * 255).astype(np.uint8))
                    .resize((CW, CH), Image.BICUBIC), np.float32) / 255.0
    craze = (np.abs(cz - 0.5) < 0.0060) * tf          # glaze crazes, the bed does not
    g = (1.0 + (gl - 0.5) * 0.090) * (1.0 - craze * 0.10)
    del gl, cz, craze, tf
    a = a * (1.0 - m) + a * m * g[:, :, None]
    del m, g
    canvas = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); del a
    canvas = bevel(canvas, tiles, up=0.24, down=0.27, r=u(3.0))
    del tiles, strip

    ov = ImageDraw.Draw(canvas)
    def rule(inset, w, col):
        ov.rectangle([u(inset), u(inset), CW - u(inset) - 1, CH - u(inset) - 1],
                     outline=col, width=max(1, int(round(u(w)))))
    rule(BS0 - 4, 7, GOLD)
    rule(BS0 - 9, 1.8, GOLD_DK)
    rule(BS1 + 4, 7, GOLD)
    rule(BS1 + 9, 1.8, GOLD_DK)
    rule(TRIM, 2.6, GOLD_DK)
    rule(TRIM - 7, 1.4, lerp(GOLD_DK, INK, .4))
    return canvas

# ----------------------------------------------------------------- niche ----
def carved_damask(mask, rng, pitch=214.0, col=None, alpha=None):
    """The same seal, repeated small and almost unseen - tooled, not printed."""
    col = DAMASK if col is None else col
    alpha = DAMASK_A if alpha is None else alpha
    lay = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    p = u(pitch); R = p * 0.47
    ys = np.arange(u(NTOP) - p, u(NBASE) + p, p)
    for j, y in enumerate(ys):
        xs = np.arange(CX - u(NHW) - p, CX + u(NHW) + p * 1.5, p)
        for x in xs:
            d.line([tuple(q) for q in khatim(x, y, R, 0.585)] +
                   [tuple(khatim(x, y, R, 0.585)[0])],
                   fill=col + (alpha,), width=max(1, int(u(1.7))), joint="curve")
            d.line([tuple(q) for q in saft(x + p / 2, y + p / 2, R * 0.62, 0.34)] +
                   [tuple(saft(x + p / 2, y + p / 2, R * 0.62, 0.34)[0])],
                   fill=col + (int(alpha * 0.8),), width=max(1, int(u(1.4))), joint="curve")
    lay.putalpha(ImageChops.multiply(lay.split()[3], mask))
    return lay

def knot(d, x, y, r, fill=GOLD, inner=GOLD_LT, ink=GOLD_DK, w=2.0):
    d.polygon([tuple(p) for p in khatim(x, y, r, 0.56)], fill=fill,
              outline=ink, width=max(1, int(u(w))))
    d.polygon([tuple(p) for p in khatim(x, y, r * 0.52, 0.56, rot=np.pi / 8)], fill=inner)

def divider(d, y, hw, major=True):
    y = u(y); x0, x1 = CX - u(hw), CX + u(hw)
    if major:
        d.rectangle([x0, y - u(3.0), x1, y + u(3.0)], fill=GOLD)
        d.rectangle([x0, y - u(4.6), x1, y - u(3.4)], fill=GOLD_LT)
        d.rectangle([x0, y + u(3.4), x1, y + u(4.6)], fill=GOLD_DK)
        for s in (-1, 1):
            knot(d, CX + s * u(hw - 26), y, u(17), GOLD_MD, GOLD_LT)
        knot(d, CX, y, u(31), GOLD, GOLD_LT)
        d.ellipse([CX - u(7), y - u(7), CX + u(7), y + u(7)], fill=KNOT_DOT)
    else:
        d.rectangle([x0, y - u(1.2), x1, y + u(1.2)], fill=GOLD_DK)
        d.polygon([tuple(p) for p in khatim(CX, y, u(15), 0.42, 4, np.pi / 4)],
                  fill=GOLD_MD, outline=GOLD_DK, width=max(1, int(u(1.4))))
        for s in (-1, 1):
            d.ellipse([CX + s * u(hw - 14) - u(5), y - u(5),
                       CX + s * u(hw - 14) + u(5), y + u(5)], fill=GOLD_MD)

def cell_rule(d, x, y0, y1, r=15.0):
    x, y0, y1 = u(x), u(y0), u(y1)
    d.rectangle([x - u(1.1), y0, x + u(1.1), y1], fill=GOLD_DK)
    ym = (y0 + y1) / 2.0
    d.polygon([tuple(p) for p in khatim(x, ym, u(r), 0.5, 4, np.pi / 4)],
              fill=GOLD_MD, outline=GOLD_DK, width=max(1, int(u(1.3))))

def sprig(pnt, x, y, ang, L, deep=GOLD_DK, mid=GOLD, pale=GOLD_LT):
    ink = lerp(GOLD_DK, INK, .45)
    spine = G.bezier([[x, y],
                      [x + math.cos(ang) * L * .5, y + math.sin(ang) * L * .5],
                      [x + math.cos(ang - .8) * L * .9, y + math.sin(ang - .8) * L * .9],
                      [x + math.cos(ang - 1.7) * L * 1.05,
                       y + math.sin(ang - 1.7) * L * 1.05]], 140)
    pnt.poly(G.ribbon(spine, L * .030, L * .010), deep)
    pnt.poly(G.ribbon(spine[3:-3], L * .014, L * .005), pale)
    for k, f in enumerate((0.18, 0.40, 0.62, 0.82)):
        i = int(f * (len(spine) - 1))
        dv = spine[min(i + 4, len(spine) - 1)] - spine[max(i - 4, 0)]
        a = math.atan2(dv[1], dv[0]); side = 1.0 if k % 2 == 0 else -1.0
        pnt.leaf(spine[i][0], spine[i][1], a + side * 1.02, L * .22,
                 curl=.80 * side, width=.29, pal=(deep, mid, pale),
                 ink_w=max(1.0, u(1.0)))
    e = spine[-1]; dv = spine[-1] - spine[-6]
    sp = pnt.tendril(e[0], e[1], math.atan2(dv[1], dv[0]), L * .30, dirn=-1.0,
                     turns=1.3, w0=L * .020, w1=L * .005, color=deep)
    q = sp[len(sp) // 3]; r = L * .085
    pnt.poly(G.petal_ring(6, s=r, r0=.44) + q, mid)
    pnt.outline(G.petal_ring(6, s=r, r0=.44) + q, ink, max(1.0, u(1.1)))
    pnt.dot(q[0], q[1], r * .30, deep)

def colonnette(pnt, xc, y0, y1, amp=44.0, waves=7.0, mirror=1.0):
    """A slender vine running the height of the plaster margin."""
    deep, mid, pale = GOLD_DK, GOLD, GOLD_LT
    t = np.linspace(0, 1, 900)
    y = u(y0) + t * u(y1 - y0)
    x = u(xc) + mirror * u(amp) * np.sin(2 * np.pi * waves * t)
    P = np.stack([x, y], 1)
    pnt.poly(G.ribbon(P, u(8.5), u(8.5)), deep)
    pnt.poly(G.ribbon(P[4:-4], u(3.6), u(3.6)), pale)
    for k in range(int(waves * 4)):
        f = (k + 0.5) / (waves * 4)
        i = int(f * (len(P) - 1))
        dv = P[min(i + 6, len(P) - 1)] - P[max(i - 6, 0)]
        a = math.atan2(dv[1], dv[0])
        side = 1.0 if k % 2 == 0 else -1.0
        pnt.leaf(P[i][0], P[i][1], a + side * 1.05, u(74), curl=0.82 * side,
                 width=0.30, pal=(deep, mid, pale), ink_w=max(1.0, u(1.2)))
    for k in range(int(waves * 2)):
        f = (k + 0.5) / (waves * 2)
        i = int(f * (len(P) - 1))
        r = u(20)
        pnt.poly(G.petal_ring(6, s=r, r0=0.44, phase=k) + P[i], mid)
        pnt.outline(G.petal_ring(6, s=r, r0=0.44, phase=k) + P[i],
                    lerp(GOLD_DK, INK, .4), max(1.0, u(1.3)))
        pnt.dot(P[i][0], P[i][1], r * 0.30, KNOT_DOT)

def zellij_column(d, cx, y0, y1, R, alt=None):
    """A narrow chain of seals - the border's rhythm, quietly repeated."""
    alt = COL_ALT if alt is None else alt
    n = max(2, int(round((y1 - y0) / (2 * R))))
    p = (y1 - y0) / n
    for i in range(n + 1):
        y = y0 + i * p
        d.polygon([tuple(q) for q in khatim(u(cx), u(y), u(R), 0.585)],
                  fill=GOLD, outline=lerp(GOLD_DK, INK, .5), width=max(1, int(u(1.8))))
        d.polygon([tuple(q) for q in khatim(u(cx), u(y), u(R * 0.87), 0.585)], fill=CREAM_LT)
        d.polygon([tuple(q) for q in khatim(u(cx), u(y), u(R * 0.50), 0.585, rot=np.pi / 8)],
                  fill=alt[i % 2])
        d.ellipse([u(cx - R * .15), u(y - R * .15), u(cx + R * .15), u(y + R * .15)],
                  fill=GOLD_LT)
    for i in range(n):
        y = y0 + (i + .5) * p
        d.polygon([tuple(q) for q in saft(u(cx), u(y), u(R * 0.60), 0.34)],
                  fill=GOLD_MD, outline=lerp(GOLD_DK, INK, .5), width=max(1, int(u(1.4))))
        d.ellipse([u(cx - R * .10), u(y - R * .10), u(cx + R * .10), u(y + R * .10)],
                  fill=lerp(KNOT_DOT, INK, .4))

def corner_seal(d, x, y, R):
    d.polygon([tuple(p) for p in khatim(u(x), u(y), u(R), 0.585)],
              fill=GOLD, outline=lerp(GOLD_DK, INK, .5), width=max(1, int(u(2.4))))
    d.polygon([tuple(p) for p in khatim(u(x), u(y), u(R * 0.86), 0.585)], fill=CREAM)
    d.polygon([tuple(p) for p in khatim(u(x), u(y), u(R * 0.50), 0.585, rot=np.pi / 8)],
              fill=STAR_INNER)
    d.ellipse([u(x - R * .16), u(y - R * .16), u(x + R * .16), u(y + R * .16)],
              fill=GOLD_LT)

# --------------------------------------------------------------- content ----
CONTENT = {
  "quote_ar": "أَلا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ",
  "quote_en": "Verily, in the remembrance of God do hearts find rest.",
  "title":    ["TARIQA AL QADIRIYA", "AL BOUTCHICHIYA"],
  "subtitle": "Weekly Dhikr Gathering",
  "title_ar": "الطريقة القادرية البودشيشية",
  "when": [("SATURDAY", "29 August 2026"), ("EVENING", "7:00 – 9:00 pm")],
  "body": "The tariqa's weekly Moroccan dhikr — guided remembrance, recited with "
          "idhn (spiritual permission), in the company of those walking the path "
          "of spiritual refinement.",
  "sched": [("I", "7:00 – 8:15", "Wadhifa Dhikr\nand Dhikr al Faraj"),
            ("II", "8:15 – 8:30", "Talk"),
            ("III", "8:30", "Maghrib, followed\nby refreshments")],
  "venue":  "CRESCENT HALL",
  "venue_sub": "Crescent Nursery",
  "venue_addr": "162 EDMUND STREET · ROCHDALE OL12 6QG",
  "rsvp_label": "PLEASE CONFIRM YOUR ATTENDANCE",
  "rsvp": "WhatsApp 07884 053544",
  "rsvp_note": "A brothers-only gathering",
  "web": "WWW.THESUFIWAY.CO.UK",
}
BLANK = os.environ.get("BLANK", "0") == "1"
TXT   = _P["txt"]          # figures and running text
TXT_H = _P["txt_h"]        # display type
TXT_G = _P["txt_g"]        # gilt accents
TXT_T = _P["txt_t"]        # small letterspaced labels
TXT_B = _P["body"]
TXT_A = _P["addr"]
TXT_Q = _P["quote"]

def typeset(canvas):
    lay = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    C = CONTENT

    # -- the ayah, in the head of the arch -----------------------------------
    b = text_box(*REG["quote"], frac=0.80)
    w = b[2] - b[0]
    s = fit_line(d, C["quote_ar"], ARABIC, w, u(104), rtl=True)
    rtl_text(d, (CX, u(690)), C["quote_ar"], F(ARABIC, s), TXT_G)
    s = fit_line(d, C["quote_en"], BODY_IT, w * 0.94, u(76))
    d.text((CX, u(812)), C["quote_en"], font=F(BODY_IT, s), fill=TXT_Q, anchor="mm")

    # -- the name of the order ----------------------------------------------
    b = text_box(*REG["title"], frac=0.94); w = b[2] - b[0]
    s = min(fit_line(d, C["title"][0], DISPLAY, w, u(146), tracking=u(9)),
            fit_line(d, C["title"][1], DISPLAY, w, u(146), tracking=u(9)))
    y_t = u(1042)
    tracked(d, C["title"][0], CX, y_t, F(DISPLAY, s), u(9), TXT_H)
    tracked(d, C["title"][1], CX, y_t + s * 1.20, F(DISPLAY, s), u(9), TXT_H)
    s2 = fit_line(d, C["subtitle"], BODY_IT, w * 0.8, u(94))
    d.text((CX, u(1360)), C["subtitle"], font=F(BODY_IT, s2), fill=TXT_G, anchor="mm")
    s3 = fit_line(d, C["title_ar"], ARABIC, w * 0.78, u(96), rtl=True)
    rtl_text(d, (CX, u(1496)), C["title_ar"], F(ARABIC, s3), TXT_G)

    # -- when ----------------------------------------------------------------
    y0, y1 = REG["when"]; hw = NHW - INSET - PAD
    for i, (lab, val) in enumerate(C["when"]):
        cx = CX + (-1 if i == 0 else 1) * u(hw / 2.0)
        tracked(d, lab, cx, u(y0 + 44), F(LABEL, u(34)), u(11), TXT_T)
        s = fit_line(d, val, BODY_SB, u(hw * 0.86), u(114))
        d.text((cx, u(y0 + 168)), val, font=F(BODY_SB, s), fill=TXT_H, anchor="mm")

    # -- the body ------------------------------------------------------------
    fit_block(d, C["body"], BODY, text_box(*REG["body"], frac=0.92), u(82),
              TXT_B, lead=1.32)

    # -- the order of the evening -------------------------------------------
    y0, y1 = REG["sched"]; W = 2 * (NHW - INSET - PAD)
    for i, (num, tm, desc) in enumerate(C["sched"]):
        cx = CX + u((i - 1) * W / 3.0)
        tracked(d, num, cx, u(y0 + 40), F(LABEL, u(30)), u(9), TXT_G)
        s = fit_line(d, tm, BODY_SB, u(W / 3.0 * 0.88), u(98))
        d.text((cx, u(y0 + 152)), tm, font=F(BODY_SB, s), fill=TXT_H, anchor="mm")
        fit_block(d, desc, BODY, (cx - u(W / 6.6), u(y0 + 212), cx + u(W / 6.6), u(y1 - 14)),
                  u(60), TXT_B, lead=1.28)

    # -- where ---------------------------------------------------------------
    y0, y1 = REG["venue"]; w = 2 * (NHW - INSET - PAD)
    s = fit_line(d, C["venue"], DISPLAY, u(w * 0.88), u(112), tracking=u(11))
    tracked(d, C["venue"], CX, u(y0 + 58), F(DISPLAY, s), u(11), TXT_H)
    s = fit_line(d, C["venue_sub"], BODY_IT, u(w * 0.7), u(60))
    d.text((CX, u(y0 + 158)), C["venue_sub"], font=F(BODY_IT, s), fill=TXT_G, anchor="mm")
    s = fit_line(d, C["venue_addr"], LABEL, u(w * 0.9), u(46), tracking=u(5))
    tracked(d, C["venue_addr"], CX, u(y0 + 246), F(LABEL, s), u(5), TXT_A)

    # -- rsvp ----------------------------------------------------------------
    y0, y1 = REG["rsvp"]
    tracked(d, C["rsvp_label"], CX, u(y0 + 44), F(LABEL, u(32)), u(13), TXT_T)
    s = fit_line(d, C["rsvp"], BODY_SB, u(w * 0.8), u(106))
    d.text((CX, u(y0 + 164)), C["rsvp"], font=F(BODY_SB, s), fill=TXT_H, anchor="mm")
    s = fit_line(d, C["rsvp_note"], BODY_IT, u(w * 0.6), u(54))
    d.text((CX, u(y0 + 264)), C["rsvp_note"], font=F(BODY_IT, s), fill=TXT_G, anchor="mm")

    # -- the address of the way ---------------------------------------------
    y0, y1 = REG["web"]
    tracked(d, C["web"], CX, u((y0 + y1) / 2.0), F(LABEL, u(34)), u(13), TXT_G)
    return Image.alpha_composite(canvas.convert("RGBA"), lay).convert("RGB")

# ----------------------------------------------------------------- build ----
def build():
    rng = np.random.default_rng(9001)
    canvas = field_ground(CW, CH, rng)
    gold_tex = gold_leaf(CW, CH, rng)
    night_tex = panel_ground(CW, CH, rng)
    canvas = zellij(canvas, rng)

    out = niche_at(0.0)
    m_out = G.poly_mask(out)

    # the niche is cut into the wall, not laid on it
    canvas = inlay(canvas, m_out, night_tex, sh_off=u(9), sh_blur=u(16), sh_amt=SHADOW)
    canvas = Image.alpha_composite(canvas.convert("RGBA"),
                                   carved_damask(m_out, rng)).convert("RGB")

    courses = [NTOP] + sorted(MAJOR + MINOR) + [NBASE]
    cw_ = Image.new("L", (CW, CH), 0); dc = ImageDraw.Draw(cw_)
    for i in range(len(courses) - 1):
        if i % 2: continue
        dc.rectangle([0, u(courses[i]), CW, u(courses[i + 1])], fill=255)
    m_txt = G.poly_mask(niche_at(INSET))
    cw_ = ImageChops.multiply(cw_.filter(ImageFilter.GaussianBlur(u(1.2))), m_txt)
    a_ = np.asarray(canvas, np.float32) * COURSE + (5.0 if COURSE > 1 else 0.0)
    canvas.paste(Image.fromarray(np.clip(a_, 0, 255).astype(np.uint8)), (0, 0), cw_)
    del a_

    inner = niche_at(FRAME)
    m_in = G.poly_mask(inner)
    if BAND_W:                       # a register of colour between gold and ground
        rose_tex = G.rose_ground(CW, CH, rng)
        bandm = ImageChops.subtract(m_in, m_txt)
        sh = np.asarray(bandm.filter(ImageFilter.GaussianBlur(u(9))), np.float32) / 255.0
        rt = np.asarray(rose_tex, np.float32) * (0.80 + 0.20 * sh)[:, :, None]
        canvas.paste(Image.fromarray(np.clip(rt, 0, 255).astype(np.uint8)), (0, 0), bandm)
        del rose_tex, rt, sh
    bm = ImageChops.subtract(m_out, m_in)
    canvas = inlay(canvas, bm, gold_tex, shadow=False)
    canvas = bevel(canvas, bm, up=0.26, down=0.30)

    pnt = Painter((CW, CH), rng)
    pnt.outline(out, lerp(GOLD_DK, INK, .55), u(3.4))
    pnt.outline(inner, lerp(GOLD_DK, INK, .55), u(2.6))
    if BAND_W:
        pnt.outline(niche_at(INSET), lerp(GOLD_DK, INK, .55), u(2.4))
        pnt.pearls(niche_at(FRAME + BAND_W * 0.5), u(33), u(8.4),
                   (26, 34, 76), hl=(120, 140, 190))
    else:
        pnt.pearls(niche_at(FRAME + 23), u(31), u(7.2), GOLD_MD, hl=GOLD_LT)

    d = pnt.d
    hw_txt = NHW - INSET - 30
    for y in MAJOR: divider(d, y, hw_txt, True)
    for y in MINOR:
        divider(d, y, min(hw_txt, niche_hw_at(y) - INSET - 30), False)

    y0, y1 = REG["when"]; cell_rule(d, NCX, y0 + 14, y1 - 14, 17)
    y0, y1 = REG["sched"]; W = 2 * (NHW - INSET - PAD)
    for s_ in (-1, 1): cell_rule(d, NCX + s_ * W / 6.0, y0 + 14, y1 - 14, 15)

    # the emblem, ringed like a boss in the plaster
    lx, ly = CX, u((REG["logo"][0] + REG["logo"][1]) / 2.0)
    R = u(276)
    d.ellipse([lx - R, ly - R, lx + R, ly + R], fill=None,
              outline=GOLD, width=max(1, int(u(7))))
    d.ellipse([lx - R * .90, ly - R * .90, lx + R * .90, ly + R * .90],
              outline=GOLD_DK, width=max(1, int(u(2.4))))
    ring = np.stack([lx + R * 1.10 * np.cos(G.TH), ly + R * 1.10 * np.sin(G.TH)], 1)
    pnt.pearls(ring, u(30), u(6.2), GOLD_MD, hl=GOLD_LT)
    for k in range(8):
        a = k * np.pi / 4 + np.pi / 8
        knot(d, lx + R * 1.10 * math.cos(a), ly + R * 1.10 * math.sin(a),
             u(15), GOLD_MD, GOLD_LT)

    if LOGO_DISC:                       # ground pigment, not a flat fill
        rr = int(R * .93) + 2
        disc = tadelakt(2 * rr, 2 * rr, np.random.default_rng(613),
                        stops=[(0.0, (62, 8, 20)), (0.36, (94, 18, 30)),
                               (0.70, (128, 30, 42)), (1.0, (156, 48, 58))])
        dm = Image.new("L", (2 * rr, 2 * rr), 0)
        ImageDraw.Draw(dm).ellipse([0, 0, 2 * rr - 1, 2 * rr - 1], fill=255)
        canvas.paste(disc, (int(lx - rr), int(ly - rr)), dm)
        del disc, dm

    pnt.im.putalpha(pnt.im.split()[3].point(lambda v: int(v * 0.97)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), pnt.im).convert("RGB")
    del pnt

    logo = load_logo(u(446))
    lw, lh = logo.size
    bx, by = int(lx - lw / 2), int(ly - lh / 2)
    leafp = gold_tex.crop((bx, by, bx + lw, by + lh)).convert("RGBA")
    la = np.asarray(leafp, np.float32); lo = np.asarray(logo, np.float32)
    la[..., :3] = la[..., :3] * 0.55 + lo[..., :3] * 0.45      # leaf, but still a logo
    la[..., 3] = lo[..., 3]
    leafp = Image.fromarray(np.clip(la, 0, 255).astype(np.uint8), "RGBA")
    canvas.paste(leafp, (bx, by), leafp)
    del la, lo, leafp

    # the niche is flanked by a slender arcade, so it belongs to a wall
    mx = (FLD + (NCX - NHW)) / 2.0
    plaster = tadelakt(CW, CH, np.random.default_rng(77),
                       base=CREAM if ROSEY else CREAM_DK)
    sp = Painter((CW, CH), rng)
    for cx_ in (mx, PW - mx):
        po = niche_outline(u(cx_), u(PIL_HW), u(FLD + 48), u(FLD + 216),
                           u(PH - FLD - 48), lobes=5, depth=u(9), foot=u(19))
        pm = G.poly_mask(po)
        canvas = inlay(canvas, pm, plaster, sh_off=u(6), sh_blur=u(11), sh_amt=0.34)
        pbm, pim = band_mask(po, u(PIL_BAND))
        canvas = inlay(canvas, pbm, gold_tex, shadow=False)
        canvas = bevel(canvas, pbm, up=0.22, down=0.26, r=u(4))
        sp.outline(po, lerp(GOLD_DK, INK, .55), u(2.2))
        sp.outline(G.offset_inward(po, u(PIL_BAND)), lerp(GOLD_DK, INK, .5), u(1.6))
        vine = Painter((CW, CH), rng)
        zellij_column(vine.d, cx_, FLD + 286, PH - FLD - 108, 48.0)
        vine.im.putalpha(ImageChops.multiply(vine.im.split()[3],
                         G.poly_mask(G.offset_inward(po, u(20)))))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), vine.im).convert("RGB")
        del vine
        corner_seal(sp.d, cx_, FLD + 142, 40)
    del plaster
    field = Image.new("L", (CW, CH), 0)
    ImageDraw.Draw(field).rectangle([u(FLD), u(FLD), CW - u(FLD) - 1, CH - u(FLD) - 1],
                                    fill=255)
    zone = ImageChops.multiply(field, ImageChops.invert(m_out))
    sp.im.putalpha(ImageChops.multiply(sp.im.split()[3], zone))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), sp.im).convert("RGB")
    return canvas

def _field(h, w, cx_, cy_, rng):
    """A smooth random field, generated small and grown - cheap at poster size."""
    g = (rng.random((max(2, int(cy_)), max(2, int(cx_)))) * 255).astype(np.uint8)
    return np.asarray(Image.fromarray(g).resize((w, h), Image.BICUBIC), np.float32) / 255.0

def handwarp(im, rng, amp, cells=30):
    """Displace everything by a hair. Nothing drawn by hand is truly straight."""
    from scipy import ndimage
    a = np.asarray(im, np.float32)
    h, w = a.shape[:2]
    dx = (_field(h, w, cells, cells * h // w, rng) - 0.5) * 2.0 * amp
    dy = (_field(h, w, cells, cells * h // w, rng) - 0.5) * 2.0 * amp
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    co = np.stack([yy + dy, xx + dx]); del yy, xx, dx, dy
    out = np.empty_like(a)
    for c in range(3):
        ndimage.map_coordinates(a[..., c], co, order=1, mode="nearest",
                                output=out[..., c])
    del co, a
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def finish(canvas, rng):
    canvas = canvas.filter(ImageFilter.GaussianBlur(u(0.34)))
    if Q != 1.0:
        canvas = canvas.resize((PW, PH), Image.LANCZOS)   # everything below is at size
    canvas = handwarp(canvas, rng, amp=2.4, cells=34)

    a = np.asarray(canvas, np.float32)
    h, w = a.shape[:2]

    # --- the sheet: tooth, laid lines, and the shadow each fibre raises ------
    tooth = _field(h, w, w // 3, h // 3, rng)
    a *= (1.0 + (tooth - 0.5) * 0.050)[:, :, None]
    del tooth
    fibre = _field(h, w, int(w / 2.2), h // 90, rng)
    a *= (1.0 + (fibre - 0.5) * 0.030)[:, :, None]
    del fibre
    relief = _field(h, w, w // 240, h // 240, rng)
    gy, gx = np.gradient(relief)
    a *= (1.0 + np.clip((gx + gy) * 55.0, -1.0, 1.0) * 0.042)[:, :, None]
    del gy, gx, relief

    # --- pigment pools where the brush stopped ------------------------------
    lum = a.mean(2)
    ey, ex = np.gradient(lum)
    edge = np.clip(np.sqrt(ex * ex + ey * ey) / 34.0, 0, 1); del ex, ey, lum
    edge = np.asarray(Image.fromarray((edge * 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(1.0)), np.float32) / 255.0
    a *= (1.0 - 0.075 * edge)[:, :, None]
    del edge

    # --- age: uneven warmth, a very little foxing ---------------------------
    cloud = _field(h, w, w // 34, h // 34, rng)
    a[:, :, 2] *= (1.0 - 0.030 * cloud)
    a[:, :, 0] *= (1.0 + 0.010 * cloud)
    fox = _field(h, w, w // 110, h // 110, rng)
    spot = np.clip((fox - 0.935) * 12.0, 0, 1)
    a[:, :, 1] *= (1.0 - 0.045 * spot)
    a[:, :, 2] *= (1.0 - 0.080 * spot)
    del fox, spot, cloud

    # --- the light in the room ----------------------------------------------
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = xx / w - 0.5; ny = yy / h - 0.5; del yy, xx
    a *= (1.0 + 0.050 * (-nx * .7 - ny)
          - 0.26 * (nx * nx * 1.9 + ny * ny * 1.1) ** 1.35)[:, :, None]
    del nx, ny

    canvas = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); del a
    return canvas.filter(ImageFilter.UnsharpMask(radius=1.3, percent=52, threshold=3))

def guide(canvas):
    """Overlay the register boxes, in final-image pixels and millimetres."""
    lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    mm = 25.4 / 300.0
    order = ["quote", "title", "logo", "when", "body", "sched", "venue", "rsvp", "web"]
    for name in order:
        y0, y1 = REG[name]
        hw = min(niche_hw_at(y0), niche_hw_at(y1)) - INSET - PAD
        x0, x1 = NCX - hw, NCX + hw
        d.rectangle([x0, y0, x1, y1], outline=(255, 90, 90, 230), width=4)
        d.rectangle([x0, y0, x1, y1], fill=(255, 90, 90, 26))
        f = ImageFont.truetype(os.path.join(FDIR, "Marcellus-400.ttf"), 48)
        d.text((x0 + 20, y0 + 14),
               f"{name.upper()}  x {int(x0)}-{int(x1)}  y {int(y0)}-{int(y1)} px"
               f"   ({(x1-x0)*mm:.0f} x {(y1-y0)*mm:.0f} mm)",
               font=f, fill=(150, 20, 20, 255))
    return Image.alpha_composite(canvas.convert("RGBA"), lay).convert("RGB")

def main():
    rng = np.random.default_rng(5150)
    im = build()
    if not BLANK: im = typeset(im)
    im = finish(im, rng)
    if os.environ.get("GUIDE", "0") == "1": im = guide(im)
    out = os.environ.get("OUT", "moroccan-poster" + ("-blank" if BLANK else ""))
    im.save(out + ".png", "PNG", dpi=(300, 300))
    if os.environ.get("PDF", "0") == "1":
        im.save(out + ".pdf", "PDF", resolution=300.0)
    print("wrote", out + ".png", im.size)

if __name__ == "__main__":
    main()
