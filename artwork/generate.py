#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PATIENT GOLD - Plate I
A full-page illumination in the tazhib tradition: an original composition
(nested cusped registers, scrolling islimi vine, reserved centre) rendered
procedurally with hand-painted texture.
"""
import os, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps, ImageFont

# ----------------------------------------------------------------------------
# canvas
# ----------------------------------------------------------------------------
Q = float(os.environ.get("Q", "2.0"))          # 2.0 = 2x supersample of A4@300
PW, PH = 2480, 3508                            # A4 at 300 dpi (final page)
CW = int(PW * Q) // 2 * 2
CH = int(PH * Q) // 2 * 2
CX, CY = CW / 2.0, CH / 2.0

def u(v):                                       # page units -> canvas px
    return v * Q

RNG = np.random.default_rng(20260909)

# ----------------------------------------------------------------------------
# palette  (ground mineral pigments)
# ----------------------------------------------------------------------------
INK        = (44, 30, 26)
INK_SOFT   = (72, 52, 44)
NAVY       = (24, 32, 74)
NAVY_LT    = (58, 70, 122)
ROSE       = (224, 133, 132)
ROSE_DK    = (196, 100,  99)
ROSE_LT    = (238, 170, 162)
GREEN      = (124, 158, 118)
GREEN_DK   = (58,  92,  70)
GREEN_LT   = (182, 205, 166)
CRIMSON    = (140, 32, 44)
CRIMSON_DK = (94, 18, 30)
MINT       = (124, 190, 188)
MINT_DK    = (66, 140, 142)
IVORY      = (247, 240, 224)
GOLD       = (198, 158, 82)
GOLD_LT    = (240, 218, 156)
GOLD_DK    = (150, 112, 52)

# ----------------------------------------------------------------------------
# noise
# ----------------------------------------------------------------------------
def _vnoise(h, w, scale, rng):
    gh = max(2, int(h / scale)); gw = max(2, int(w / scale))
    g = (rng.random((gh, gw)) * 255).astype(np.uint8)
    return np.asarray(Image.fromarray(g).resize((w, h), Image.BICUBIC), np.float32) / 255.0

def fbm(h, w, octaves=6, base=None, gain=0.52, rng=None):
    rng = rng or RNG
    base = base or w / 2.5
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0.0; sc = base
    for _ in range(octaves):
        out += amp * _vnoise(h, w, sc, rng); tot += amp; amp *= gain; sc = max(2.0, sc / 2.0)
    return out / tot

def ramp(t, stops):
    t = np.clip(t, 0, 1)
    out = np.zeros(t.shape + (3,), np.float32)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]; p1, c1 = stops[i + 1]
        m = (t >= p0) & (t <= p1)
        if not m.any(): continue
        f = ((t[m] - p0) / (p1 - p0))[:, None]
        out[m] = np.array(c0, np.float32) * (1 - f) + np.array(c1, np.float32) * f
    out[t < stops[0][0]] = np.array(stops[0][1], np.float32)
    out[t > stops[-1][0]] = np.array(stops[-1][1], np.float32)
    return out

# ----------------------------------------------------------------------------
# grounds
# ----------------------------------------------------------------------------
GOLD_STOPS = [
    (0.00, (178, 130,  74)),
    (0.22, (203, 159,  97)),
    (0.42, (222, 184, 126)),
    (0.60, (236, 207, 156)),
    (0.78, (245, 226, 184)),
    (1.00, (251, 240, 213)),
]

def gold_ground(w, h, rng, pale=0.0):
    """Burnished, marbled gold leaf field."""
    sw, sh = w // 3, h // 3
    n1 = fbm(sh, sw, 6, sw / 2.2, rng=rng)
    n2 = fbm(sh, sw, 5, sw / 7.0, rng=rng)
    n3 = fbm(sh, sw, 4, sw / 22.0, rng=rng)
    # marbled turbulence: warped sinusoidal banding, like beaten leaf
    warp = np.sin(5.0 * n1 + 3.0 * n2 + 1.3 * n3)
    t = 0.60 + 0.170 * warp + 0.150 * (n2 - 0.5) + 0.085 * (n3 - 0.5)
    # raking light, upper-left
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    lig = 1.0 - 0.55 * np.sqrt(((xx / sw) - 0.34) ** 2 + ((yy / sh) - 0.24) ** 2)
    t = t * 0.90 + 0.13 * lig + pale * 0.16
    rgb = ramp(t, GOLD_STOPS)
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    a = np.asarray(img, np.float32)
    # fine tooth of the paper + gold granulation at full resolution
    grain = rng.normal(0.0, 3.4, (h, w)).astype(np.float32)
    grain = np.asarray(Image.fromarray(np.clip(grain * 12 + 128, 0, 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.6)), np.float32)
    a += ((grain - 128) / 12.0)[:, :, None] * np.array([1.15, 1.0, 0.72], np.float32)
    # burnish streaks
    st = _vnoise(h, w, max(3.0, u(2.2)), rng)
    st = np.asarray(Image.fromarray((st * 255).astype(np.uint8))
                    .filter(ImageFilter.GaussianBlur(u(0.5))), np.float32) / 255.0
    a += ((st - 0.5) * 9.0)[:, :, None] * np.array([1.0, 0.88, 0.55], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def rose_ground(w, h, rng):
    """Flesh-rose gouache: opaque, slightly granular, unevenly loaded brush."""
    sw, sh = w // 3, h // 3
    n1 = fbm(sh, sw, 5, sw / 3.0, rng=rng)
    n2 = fbm(sh, sw, 4, sw / 12.0, rng=rng)
    t = 0.5 + 0.62 * (n1 - 0.5) + 0.42 * (n2 - 0.5)
    stops = [(0.0, (190,  97,  99)), (0.35, (212, 121, 122)),
             (0.65, (226, 141, 139)), (1.0, (241, 173, 165))]
    rgb = ramp(t, stops)
    img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    a = np.asarray(img, np.float32)
    grain = rng.normal(0.0, 4.2, (h, w)).astype(np.float32)
    grain = np.asarray(Image.fromarray(np.clip(grain * 10 + 128, 0, 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(0.55)), np.float32)
    a += ((grain - 128) / 10.0)[:, :, None] * np.array([1.0, 0.72, 0.72], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

# ----------------------------------------------------------------------------
# geometry
# ----------------------------------------------------------------------------
NT = 3000
TH = np.linspace(0.0, 2 * np.pi, NT, endpoint=False)

class Shape:
    """A closed cusped outline: m fat lobes separated by sharp cusps,
    elongated vertically, optionally drawn to an ogee point top and bottom."""
    def __init__(self, lobes, amp, p, R, ky, rot=0.0, cx=None, cy=None,
                 point=0.0, pw=8.0):
        self.lobes, self.amp, self.p = lobes, amp, p
        self.R, self.ky, self.rot = R, ky, rot
        self.cx = CX if cx is None else cx
        self.cy = CY if cy is None else cy
        self.point, self.pw = point, pw

    def r(self, th):
        c = np.abs(np.cos(self.lobes * (th + self.rot) / 2.0))
        rr = (1.0 - self.amp) + self.amp * (c ** self.p)
        if self.point:
            rr = rr * (1.0 + self.point * np.abs(np.sin(th)) ** self.pw)
        return rr

    def pts(self, th=TH):
        rr = self.r(th) * self.R
        return np.stack([self.cx + rr * np.cos(th),
                         self.cy + self.ky * rr * np.sin(th)], 1)

    def scaled(self, f, dky=0.0):
        return Shape(self.lobes, self.amp, self.p, self.R * f, self.ky + dky,
                     self.rot, self.cx, self.cy, self.point, self.pw)

class Mandorla(Shape):
    """Vesica of two circular arcs - genuine ogee points top and bottom -
    with a shallow cusp notch on each diagonal."""
    def __init__(self, W, Hh, amp=0.0, p=0.75, lobes=4, rot=0.0,
                 cx=None, cy=None):
        Shape.__init__(self, lobes, amp, p, 1.0, 1.0, rot, cx, cy)
        self.Rm = (W + Hh * Hh / W) / 2.0
        self.d = self.Rm - W

    def r(self, th):
        c = np.abs(np.cos(th))
        base = -self.d * c + np.sqrt(self.d * self.d * c * c
                                     + self.Rm * self.Rm - self.d * self.d)
        if self.amp:
            k = np.abs(np.cos(self.lobes * (th + self.rot) / 2.0))
            base = base * ((1.0 - self.amp) + self.amp * k ** self.p)
        return base

    def pts(self, th=TH):
        rr = self.r(th)
        return np.stack([self.cx + rr * np.cos(th),
                         self.cy + rr * np.sin(th)], 1)


def poly_mask(pts, size=None, feather=0.0):
    size = size or (CW, CH)
    im = Image.new("L", size, 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in pts], fill=255)
    if feather: im = im.filter(ImageFilter.GaussianBlur(feather))
    return im

def offset_inward(pts, d):
    """Offset a closed polyline inward by d (positive = toward centroid side)."""
    p = np.asarray(pts, np.float64)
    t = np.roll(p, -1, 0) - np.roll(p, 1, 0)
    n = np.stack([t[:, 1], -t[:, 0]], 1)
    n /= (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
    c = p.mean(0)
    s = np.sign(((p - c) * n).sum(1))[:, None]
    return p - n * s * d

# --- band frame: medial line, half width, outward normal, arc parameter -----
class Band:
    def __init__(self, outer, inner, th=TH):
        self.o = outer.pts(th) if isinstance(outer, Shape) else np.asarray(outer, np.float64)
        self.i = inner.pts(th) if isinstance(inner, Shape) else np.asarray(inner, np.float64)
        self.th = th
        self.mid = (self.o + self.i) / 2.0
        d = self.o - self.i
        self.w = np.linalg.norm(d, axis=1)
        self.n = d / (self.w[:, None] + 1e-9)
        t = np.roll(self.mid, -1, 0) - np.roll(self.mid, 1, 0)
        self.t = t / (np.linalg.norm(t, axis=1, keepdims=True) + 1e-9)

    def at(self, ang):
        """Sample by angle (radians), wrapping."""
        k = (ang % (2 * np.pi)) / (2 * np.pi) * len(self.th)
        i0 = int(np.floor(k)) % len(self.th); i1 = (i0 + 1) % len(self.th); f = k - np.floor(k)
        mid = self.mid[i0] * (1 - f) + self.mid[i1] * f
        n = self.n[i0] * (1 - f) + self.n[i1] * f
        t = self.t[i0] * (1 - f) + self.t[i1] * f
        w = self.w[i0] * (1 - f) + self.w[i1] * f
        n /= np.linalg.norm(n) + 1e-9; t /= np.linalg.norm(t) + 1e-9
        return mid, n, t, w

    def p(self, ang, off):
        """Point at angle, offset across the band in [-1,1] (1 = outer edge)."""
        mid, n, t, w = self.at(ang)
        return mid + n * (off * w / 2.0), n, t, w

# ----------------------------------------------------------------------------
# stroke / transform helpers
# ----------------------------------------------------------------------------
def xf(local, x, y, s, ang, fx=1.0):
    p = np.asarray(local, np.float64) * np.array([s * fx, s])
    c, si = math.cos(ang), math.sin(ang)
    return np.stack([x + p[:, 0] * c - p[:, 1] * si,
                     y + p[:, 0] * si + p[:, 1] * c], 1)

def resample(pts, n):
    p = np.asarray(pts, np.float64)
    d = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    if d[-1] < 1e-9: return np.repeat(p[:1], n, 0)
    s = np.linspace(0, d[-1], n)
    return np.stack([np.interp(s, d, p[:, 0]), np.interp(s, d, p[:, 1])], 1)

def bezier(P, n=80):
    P = np.asarray(P, np.float64)
    t = np.linspace(0, 1, n)[:, None, None]
    pts = np.repeat(P[None, :, :], n, 0)
    for _ in range(P.shape[0] - 1):
        pts = pts[:, :-1, :] * (1 - t) + pts[:, 1:, :] * t
    return pts[:, 0, :]

def ribbon(pts, w0, w1, ease=1.0):
    p = resample(pts, max(12, len(pts)))
    t = np.roll(p, -1, 0) - np.roll(p, 1, 0)
    t[0] = p[1] - p[0]; t[-1] = p[-1] - p[-2]
    n = np.stack([-t[:, 1], t[:, 0]], 1)
    n /= (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
    s = np.linspace(0, 1, len(p)) ** ease
    w = (w0 * (1 - s) + w1 * s)[:, None] / 2.0
    return np.vstack([p + n * w, (p - n * w)[::-1]])

def wob(pts, amp, rng, k=3):
    """Smooth low-frequency wobble along the normal - the tremor of a hand."""
    p = np.asarray(pts, np.float64); n = len(p)
    g = rng.normal(0, 1, n)
    g = np.convolve(g, np.ones(max(3, n // k)) / max(3, n // k), "same")
    g -= np.linspace(g[0], g[-1], n)
    mx = np.abs(g).max()
    if mx < 1e-9: return p
    g = g / mx * amp
    t = np.roll(p, -1, 0) - np.roll(p, 1, 0)
    nv = np.stack([-t[:, 1], t[:, 0]], 1)
    nv /= (np.linalg.norm(nv, axis=1, keepdims=True) + 1e-9)
    return p + nv * g[:, None]

def log_spiral(turns=1.15, decay=0.36, n=150, dirn=1.0, r0=1.0):
    th = np.linspace(0, turns * 2 * np.pi, n)
    r = r0 * np.exp(-decay * th)
    a = dirn * th
    return np.stack([r * np.cos(a) - r0, dirn * r * np.sin(a)], 1)

def place(local, x, y, ang, s=1.0):
    p = np.asarray(local, np.float64) * s
    d = p[1] - p[0]; a0 = math.atan2(d[1], d[0]); da = ang - a0
    c, si = math.cos(da), math.sin(da)
    q = np.stack([p[:, 0] * c - p[:, 1] * si, p[:, 0] * si + p[:, 1] * c], 1)
    return q - q[0] + np.array([x, y])

# ----------------------------------------------------------------------------
# motif vocabulary  (stem, leaf, bud, blossom, rosette, palmette)
# ----------------------------------------------------------------------------
def lerp(c0, c1, f):
    return tuple(int(round(a * (1 - f) + b * f)) for a, b in zip(c0, c1))

def leaf_parts(n=88, curl=0.55, width=0.30, up=1.0, dn=0.62,
               s=1.0, x0=0.0, x1=1.0, serr=0.0, teeth=5.0):
    t = np.linspace(0.0, 1.0, n)
    x = x0 + t * (x1 - x0)
    spine = curl * (x ** 1.65)
    w = width * (np.sin(np.pi * np.clip(x, 0, 1) ** 0.78) ** 0.82) * (1 - 0.26 * x) * s
    wu = w * up
    if serr:
        wu = wu * (1.0 + serr * np.sin(x * np.pi * teeth * 2.0 + 0.9) * np.sin(np.pi * x) ** 0.45)
    return (np.stack([x, spine + wu], 1),
            np.stack([x, spine - w * dn], 1),
            np.stack([x, spine], 1))

def leaf_shape(**kw):
    a, b, _ = leaf_parts(**kw)
    return np.vstack([a, b[::-1]])

def petal_ring(pet=6, n=260, r0=0.40, r1=1.0, sharp=0.62, phase=0.0, s=1.0):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False) + phase
    r = (r0 + (r1 - r0) * np.abs(np.cos(pet * (t - phase) / 2.0)) ** sharp) * s
    return np.stack([r * np.cos(t), r * np.sin(t)], 1)

def fan_shape(lobes=5, n=220, spread=1.0, s=1.0):
    t = np.linspace(-np.pi * spread / 2, np.pi * spread / 2, n)
    r = (0.34 + 0.66 * np.abs(np.cos(lobes * t / spread / 2.0)) ** 0.55) * \
        (0.55 + 0.45 * np.cos(t / spread) ** 2) * s
    p = np.stack([r * np.cos(t), r * np.sin(t)], 1)
    return np.vstack([p, [[0.0, 0.0]]])

def drop_shape(n=70, width=0.34, curl=0.22, s=1.0):
    t = np.linspace(0, 1, n)
    spine = curl * t ** 2
    w = width * (np.sin(np.pi * t ** 0.62) ** 0.9) * (1 - 0.42 * t) * s
    return np.vstack([np.stack([t, spine + w], 1), np.stack([t, spine - w], 1)[::-1]])


class Painter:
    """Draws the motif vocabulary onto an RGBA layer."""
    def __init__(self, size, rng):
        self.im = Image.new("RGBA", size, (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
        self.rng = rng

    # -- primitives ---------------------------------------------------------
    def poly(self, pts, fill):
        self.d.polygon([tuple(p) for p in pts], fill=fill)

    def outline(self, pts, color, w, close=True):
        q = [tuple(p) for p in pts]
        if close: q = q + [q[0]]
        self.d.line(q, fill=color, width=max(1, int(round(w))), joint="curve")

    def dot(self, x, y, r, fill, ring=None, rw=0):
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=fill,
                       outline=ring, width=max(1, int(rw)) if ring else 0)

    def modelled(self, layers, ink=INK, ink_w=1.0):
        """layers: list of (points, colour) from outside in."""
        for pts, c in layers:
            self.poly(pts, c)
        if ink_w > 0:
            self.outline(layers[0][0], ink, ink_w)

    # -- vocabulary ---------------------------------------------------------
    def stem(self, pts, w0, w1, color=GREEN_DK, ink_w=0.0, wobble=0.0):
        p = resample(pts, 90)
        if wobble: p = wob(p, wobble, self.rng)
        self.poly(ribbon(p, w0, w1), color)
        return p

    def leaf(self, x, y, ang, L, fx=1.0, curl=0.55, width=0.30, serr=0.0,
             pal=(GREEN_DK, GREEN, GREEN_LT), ink_w=1.0, vein=True):
        c_dk, c_md, c_lt = pal
        kw = dict(curl=curl, width=width, serr=serr)
        up, dn, sp = leaf_parts(**kw)
        U = xf(up, x, y, L, ang, fx); D = xf(dn, x, y, L, ang, fx)
        SP = xf(sp, x, y, L, ang, fx)
        full = np.vstack([U, D[::-1]])
        self.poly(full, c_md)                                   # body
        self.poly(np.vstack([SP, D[::-1]]), c_dk)               # shaded half
        up2, _, sp2 = leaf_parts(curl=curl, width=width, s=0.52, x0=0.10, x1=0.86)
        self.poly(np.vstack([xf(up2, x, y, L, ang, fx),
                             xf(sp2, x, y, L, ang, fx)[::-1]]), c_lt)
        self.poly(ribbon(SP[2:-2], max(0.9, L * 0.020), max(0.5, L * 0.004)),
                  lerp(c_dk, INK, 0.35))                        # midrib
        self.outline(full, INK, ink_w)

    def bud(self, x, y, ang, L, fx=1.0, pal=(MINT_DK, MINT, IVORY), ink_w=1.0):
        c_e, c_m, c_i = pal
        o = xf(drop_shape(), x, y, L, ang, fx)
        m = xf(drop_shape(s=0.74), x, y, L * 0.95, ang, fx)
        i = xf(drop_shape(s=0.34), x, y, L * 0.76, ang, fx)
        self.modelled([(o, c_e), (m, c_m), (i, c_i)], ink=INK, ink_w=ink_w)

    def blossom(self, x, y, r, rot=0.0, pet=6,
                pal=(ROSE_DK, IVORY), heart=CRIMSON, ink_w=1.0):
        c_e, c_i = pal
        c = np.array([x, y], np.float64)
        o = petal_ring(pet, phase=rot, s=r) + c
        m = petal_ring(pet, phase=rot, s=r * 0.80, r0=0.44) + c
        i = petal_ring(pet, phase=rot, s=r * 0.56, r0=0.50) + c
        self.modelled([(o, c_e), (m, lerp(c_e, c_i, 0.55)), (i, c_i)], ink=INK, ink_w=ink_w)
        self.dot(x, y, r * 0.20, heart)
        self.dot(x, y, r * 0.10, GOLD_LT)
        # petal tips: a single lifted highlight each
        for k in range(pet):
            a = rot + k * 2 * np.pi / pet
            self.dot(x + math.cos(a) * r * 0.66, y + math.sin(a) * r * 0.66,
                     max(0.7, r * 0.055), IVORY)
        return

    def rosette(self, x, y, r, rot=0.0, ink_w=1.2):
        """The deep focal flower: crimson corolla, gold eye."""
        o = petal_ring(8, phase=rot, s=r, r0=0.68, sharp=0.5)
        self.modelled([(o + [x, y], CRIMSON_DK)], ink=INK, ink_w=ink_w)
        self.poly(petal_ring(8, phase=rot, s=r * 0.86, r0=0.70, sharp=0.5) + [x, y], CRIMSON)
        self.poly(petal_ring(8, phase=rot + np.pi / 8, s=r * 0.60, r0=0.74, sharp=0.6) + [x, y],
                  lerp(CRIMSON, ROSE, 0.30))
        self.dot(x, y, r * 0.30, CRIMSON_DK)
        self.dot(x, y, r * 0.20, GOLD)
        self.dot(x, y, r * 0.085, IVORY)
        for k in range(8):
            a = rot + k * np.pi / 4
            self.dot(x + math.cos(a) * r * 0.44, y + math.sin(a) * r * 0.44,
                     max(0.7, r * 0.045), GOLD_LT)

    def palmette(self, x, y, ang, L, lobes=9, fx=1.0, spread=1.95,
                 pal=(GREEN_DK, GREEN, GREEN_LT), ink_w=1.0):
        """A true palmette: a fan of separate pointed lobes rising from a base."""
        c_e, c_m, c_i = pal
        n = max(3, lobes)
        order = sorted(range(n), key=lambda k: -abs((k / (n - 1.0)) * 2 - 1))
        for k in order:
            f = (k / (n - 1.0)) * 2 - 1
            a = ang + f * spread / 2.0
            ln = L * (0.52 + 0.48 * math.cos(f * math.pi / 2) ** 1.25)
            wdt = 0.205 - 0.045 * abs(f)
            o = xf(drop_shape(width=wdt, curl=0.10 * f), x, y, ln, a, fx)
            m = xf(drop_shape(width=wdt, curl=0.10 * f, s=0.74), x, y, ln * 0.95, a, fx)
            i = xf(drop_shape(width=wdt, curl=0.10 * f, s=0.36), x, y, ln * 0.78, a, fx)
            self.modelled([(o, c_e), (m, c_m), (i, c_i)], ink=INK, ink_w=ink_w)
        self.dot(x, y, L * 0.115, c_m, ring=INK, rw=ink_w)
        self.dot(x, y, L * 0.048, GOLD_LT)

    def fanflower(self, x, y, ang, L, ink_w=1.0, rings=None):
        """A half-open palmette flower: tiered rings of pointed petals."""
        rings = rings or [(7, 1.00, 1.48, IVORY, lerp(IVORY, ROSE_LT, .45)),
                          (5, 0.62, 1.18, CRIMSON, lerp(ROSE_LT, IVORY, .35)),
                          (3, 0.32, 0.76, CRIMSON_DK, CRIMSON)]
        for n, sl, spread, cout, cin in rings:
            order = sorted(range(n), key=lambda k: -abs((k / (n - 1.0)) * 2 - 1))
            for k in order:
                f = (k / (n - 1.0)) * 2 - 1
                a = ang + f * spread / 2.0
                ln = L * sl * (0.56 + 0.44 * math.cos(f * math.pi / 2) ** 1.45)
                o = xf(drop_shape(width=0.520, curl=0.06 * f), x, y, ln, a)
                i = xf(drop_shape(width=0.520, curl=0.06 * f, s=0.55), x, y, ln * 0.82, a)
                self.poly(o, cout); self.poly(i, cin)
                self.outline(o, INK, ink_w)
        self.dot(x, y, L * 0.115, GOLD, ring=INK, rw=ink_w)
        self.dot(x, y, L * 0.048, IVORY)

    def pearls(self, pts, gap, r, fill=NAVY, hl=None, phase=0.0):
        p = np.asarray(pts, np.float64)
        d = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(np.vstack([p, p[:1]]), axis=0), axis=1))]
        n = max(8, int(round(d[-1] / gap)))
        s = (np.arange(n) + phase) * (d[-1] / n)
        pp = np.vstack([p, p[:1]])
        xs = np.interp(s, d, pp[:, 0]); ys = np.interp(s, d, pp[:, 1])
        for x, y in zip(xs, ys):
            self.dot(x, y, r, fill)
            if hl: self.dot(x - r * 0.28, y - r * 0.28, r * 0.30, hl)

    def tendril(self, x, y, ang, L, dirn=1.0, turns=1.15, w0=None, w1=None,
                color=GREEN_DK, tip=None):
        sp = place(log_spiral(turns=turns, dirn=dirn, r0=1.0), x, y, ang, L)
        w0 = w0 if w0 is not None else L * 0.085
        w1 = w1 if w1 is not None else L * 0.020
        self.poly(ribbon(sp, w0, w1), color)
        if tip: tip(sp[-1], sp)
        return sp

# ----------------------------------------------------------------------------
# the scrolling vine  (islimi) that fills a band
# ----------------------------------------------------------------------------
def band_scroll(pnt, band, A0, A1, waves=3.0, amp=0.50, ms=1.0, n=420,
                big=True, rng=None, leaf_gap=0.024, serr=0.14, minor=True,
                nvines=2, stem=1.0):
    """Two counter-phase vines braided down a band, every residual gap filled."""
    rng = rng or pnt.rng
    ss = np.linspace(0.0, 1.0, n)
    ang = A0 + ss * (A1 - A0)
    wid = np.array([band.p(a, 0.0)[3] for a in ang])
    wm = float(np.median(wid))
    idx = lambda t: int(np.clip(round(t * (n - 1)), 0, n - 1))

    vines = []
    for sign in ((1.0, -1.0) if nvines == 2 else (1.0,)):
        off = sign * amp * np.cos(2 * np.pi * waves * ss)
        P = np.array([band.p(a, o)[0] for a, o in zip(ang, off)])
        vines.append((P, off, sign))

    def tangent(P, i):
        j0 = max(0, i - 3); j1 = min(len(P) - 1, i + 3)
        d = P[j1] - P[j0]
        return math.atan2(d[1], d[0])

    # --- stems -------------------------------------------------------------
    for P, off, sign in vines:
        pnt.poly(ribbon(P, wm * 0.055 * stem, wm * 0.055 * stem), lerp(GREEN_DK, INK, 0.42))
        pnt.poly(ribbon(P[3:-3], wm * 0.030 * stem, wm * 0.030 * stem), lerp(GREEN, GREEN_LT, .30))

    # --- spiral tendrils, laid down before the foliage --------------------
    tips = []
    for P, off, sign in vines:
        for j in range(int(round(2 * waves)) + 1):
            t = j / (2.0 * waves)
            if t > 1.0: break
            i = idx(t)
            p, nv, tv, w = band.p(ang[i], off[i])
            a = tangent(P, i)
            inward = -np.sign(off[i]) if abs(off[i]) > 1e-6 else 1.0
            L = w * 0.330 * ms
            sp = pnt.tendril(p[0], p[1], a + inward * 0.95, L, dirn=inward,
                             turns=1.25, w0=w * 0.044, w1=w * 0.010,
                             color=lerp(GREEN_DK, INK, 0.42))
            pnt.poly(ribbon(sp[:-8], w * 0.024, w * 0.006),
                     lerp(GREEN, GREEN_LT, .30))
            tips.append((sp, w))

    # --- outward feathering: small leaves toward the band edges ------------
    for P, off, sign in vines:
        t = leaf_gap * 0.5; flip = 1.0
        while t < 1.0 - 1e-6:
            i = idx(t); a = tangent(P, i); w = wid[i]
            side = (1.0 if (off[i] * sign) < 0 else -1.0) * flip
            L = w * (0.185 + 0.060 * rng.random()) * ms
            pal = (GREEN_DK, GREEN, GREEN_LT) if flip > 0 else \
                  (lerp(GREEN_DK, INK, .18), lerp(GREEN, GREEN_DK, .38),
                   lerp(GREEN_LT, GREEN, .30))
            pnt.leaf(P[i][0], P[i][1], a + side * (0.95 + 0.30 * rng.random()),
                     L, curl=0.80 * side, width=0.295, serr=serr, pal=pal,
                     ink_w=max(1.0, wm * 0.0085))
            flip *= -1.0
            t += leaf_gap * (0.86 + 0.30 * rng.random())

    for sp, w in tips:
        e = sp[-1]; d = sp[-1] - sp[-6]
        pnt.bud(e[0], e[1], math.atan2(d[1], d[0]), w * 0.115 * ms,
                ink_w=max(1.0, wm * 0.008))

    # --- crossings: the focal flowers, alternating deep and pale ----------
    ncross = int(round(2 * waves))
    for j in range(ncross + 1):
        t = (2 * j + 1) / (4.0 * waves)
        if t > 1.0: break
        i = idx(t)
        p, nv, tv, w = band.p(ang[i], 0.0 if nvines == 2 else
                              (0.42 * amp * (1 if j % 2 else -1)))
        if big and j % 2 == 0:
            pnt.rosette(p[0], p[1], w * 0.200 * ms, rot=np.pi / 8,
                        ink_w=max(1.0, wm * 0.011))
        else:
            pnt.blossom(p[0], p[1], w * 0.132 * ms, rot=0.31, pet=6,
                        pal=(lerp(ROSE_DK, CRIMSON, .45), IVORY),
                        ink_w=max(1.0, wm * 0.009))


    # --- minor register: pale blossoms and seed clusters in the residue ---
    if minor:
        for j in range(int(round(4 * waves))):
            t = (j + 0.5) / (4.0 * waves)
            i = idx(t)
            for o in (0.72, -0.72):
                p, nv, tv, w = band.p(ang[i], o)
                if (j + (o > 0)) % 2 == 0:
                    pnt.blossom(p[0], p[1], w * 0.076 * ms, rot=0.2 + 0.7 * j, pet=5,
                                pal=(lerp(ROSE_DK, CRIMSON, .30), IVORY),
                                heart=CRIMSON_DK, ink_w=max(1.0, wm * 0.007))
                else:
                    pnt.bud(p[0], p[1], math.atan2(nv[1], nv[0]) + 0.4,
                            w * 0.115 * ms, ink_w=max(1.0, wm * 0.007))

    # --- seeding: minute five-petal stars in the last of the ground -------
    for k in range(int(11 * waves)):
        t = (k + 0.5) / (11 * waves)
        i = idx(t)
        for o in (0.90, -0.90):
            if (k + (o > 0)) % 2: continue
            p, nv, tv, w = band.p(ang[i], o)
            r = w * 0.044 * ms
            pnt.poly(petal_ring(5, phase=k * 1.1, s=r, r0=0.42) + p, IVORY)
            pnt.outline(petal_ring(5, phase=k * 1.1, s=r, r0=0.42) + p,
                        lerp(ROSE_DK, INK, .35), max(1.0, wm * 0.006))
            pnt.dot(p[0], p[1], r * 0.28, CRIMSON)


def gold_tracery(pnt, band, A0, A1, waves=4.0, amp=0.54, ms=1.0, n=380,
                 rng=None, ink=None, deep=None, mid=None, pale=None):
    """Halkar: a scroll drawn in gold on gold - present only in raking light."""
    rng = rng or pnt.rng
    ink = ink or lerp(GOLD_DK, INK, 0.56)
    deep = deep or GOLD_DK; mid = mid or GOLD; pale = pale or GOLD_LT
    ss = np.linspace(0.0, 1.0, n)
    ang = A0 + ss * (A1 - A0)
    wid = np.array([band.p(a, 0.0)[3] for a in ang])
    wm = float(np.median(wid))
    idx = lambda t: int(np.clip(round(t * (n - 1)), 0, n - 1))
    off = amp * np.cos(2 * np.pi * waves * ss)
    P = np.array([band.p(a, o)[0] for a, o in zip(ang, off)])

    pnt.poly(ribbon(P, wm * 0.026, wm * 0.026), deep)
    pnt.poly(ribbon(P[3:-3], wm * 0.012, wm * 0.012), pale)

    def tangent(i):
        j0 = max(0, i - 3); j1 = min(n - 1, i + 3)
        d = P[j1] - P[j0]; return math.atan2(d[1], d[0])

    for j in range(int(round(2 * waves)) + 1):            # tendrils
        t = j / (2.0 * waves)
        if t > 1.0: break
        i = idx(t); w = wid[i]
        inward = -np.sign(off[i]) if abs(off[i]) > 1e-6 else 1.0
        sp = pnt.tendril(P[i][0], P[i][1], tangent(i) + inward * 0.95,
                         w * 0.26 * ms, dirn=inward, turns=1.30,
                         w0=w * 0.026, w1=w * 0.006, color=deep)
        e = sp[-1]
        pnt.dot(e[0], e[1], max(1.0, w * 0.028), mid, ring=ink, rw=1)

    t = 0.020; flip = 1.0                                  # leaves
    while t < 1.0:
        i = idx(t); w = wid[i]
        side = (1.0 if off[i] < 0 else -1.0) * flip
        pnt.leaf(P[i][0], P[i][1], tangent(i) + side * 1.00, w * 0.155 * ms,
                 curl=0.80 * side, width=0.28, serr=0.0,
                 pal=(deep, mid, pale), ink_w=1.0, vein=False)
        flip *= -1.0; t += 0.034

    for j in range(int(round(2 * waves))):                 # rosettes
        t = (2 * j + 1) / (4.0 * waves)
        if t > 1.0: break
        i = idx(t); w = wid[i]
        p = band.p(ang[i], 0.0)[0]
        r = w * 0.085 * ms
        pnt.poly(petal_ring(6, s=r, r0=0.44, phase=j * 0.7) + p, mid)
        pnt.outline(petal_ring(6, s=r, r0=0.44, phase=j * 0.7) + p, ink, 1.0)
        pnt.dot(p[0], p[1], r * 0.26, deep)


def corner_lachak(pnt, cx_, cy_, ang, R, deep=None, mid=None, pale=None):
    """A gold quarter-medallion tucked into the corner of the field."""
    ink = lerp(GOLD_DK, INK, 0.58)
    deep = deep or GOLD_DK; mid = mid or GOLD; pale = pale or GOLD_LT
    for f, lw in ((1.00, 1.8), (0.955, 1.0)):
        sh = Shape(8, 0.150, 0.72, R=R * f, ky=1.0, cx=cx_, cy=cy_)
        pnt.outline(sh.pts(), ink, max(1.0, u(lw)))
    px = cx_ + math.cos(ang) * R * 0.235; py = cy_ + math.sin(ang) * R * 0.235
    pnt.fanflower(px, py, ang, R * 0.30, ink_w=max(1.0, u(1.0)),
                  rings=[(9, 1.00, 2.05, lerp(mid, pale, .55), pale),
                         (5, 0.55, 1.55, mid, lerp(pale, mid, .3))])
    for sgn in (1, -1):
        qx = cx_ + math.cos(ang + sgn * 1.02) * R * 0.52
        qy = cy_ + math.sin(ang + sgn * 1.02) * R * 0.52
        pnt.leaf(qx, qy, ang + sgn * 1.36, R * 0.235, curl=-0.75 * sgn,
                 width=0.28, pal=(deep, lerp(mid, pale, .4), pale),
                 ink_w=max(1.0, u(1.0)))
        pnt.dot(cx_ + math.cos(ang + sgn * 1.30) * R * 0.74,
                cy_ + math.sin(ang + sgn * 1.30) * R * 0.74,
                max(1.0, u(4.0)), mid, ring=ink, rw=1)


def axis_motif(pnt, band, ang, ms=1.0, lobes=9):
    """A bilaterally symmetric anchor sitting exactly on a mirror axis."""
    p, nv, tv, w = band.p(ang, 0.46)
    a = math.atan2(-nv[1], -nv[0])                    # opens toward the centre
    ta = math.atan2(tv[1], tv[0])
    iw = max(1.0, w * 0.010)
    for sgn in (1, -1):
        q = p + np.array([math.cos(ta), math.sin(ta)]) * (sgn * w * 0.30 * ms)
        pnt.leaf(q[0], q[1], a + sgn * 0.62, w * 0.46 * ms,
                 curl=-0.55 * sgn, width=0.25, serr=0.12, ink_w=iw)
    pnt.fanflower(p[0], p[1], a, w * 0.50 * ms, ink_w=iw)
    r, _, _, _ = band.p(ang, -0.34)
    pnt.rosette(r[0], r[1], w * 0.170 * ms, rot=np.pi / 8, ink_w=iw)

# ----------------------------------------------------------------------------
# page assembly
# ----------------------------------------------------------------------------
M = 188.0                                     # uniform margin, page units
FIELD = (u(M), u(M), CW - u(M), CH - u(M))

def field_mask():
    im = Image.new("L", (CW, CH), 0)
    ImageDraw.Draw(im).rectangle([FIELD[0], FIELD[1], FIELD[2] - 1, FIELD[3] - 1], fill=255)
    return im

def fourfold(layer):
    q = Image.new("L", (CW, CH), 0)
    ImageDraw.Draw(q).rectangle([CW // 2, 0, CW - 1, CH // 2 - 1], fill=255)
    layer.putalpha(ImageChops.multiply(layer.split()[3], q))
    out = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    for im in (layer, ImageOps.mirror(layer)):
        for jm in (im, ImageOps.flip(im)):
            out = Image.alpha_composite(out, jm)
    return out

def paint_band(canvas, paint, outer, inner, clip=None, pool=0.24, feather=u(7)):
    mo = poly_mask(outer); mi = poly_mask(inner)
    m = ImageChops.subtract(mo, mi)
    if clip is not None: m = ImageChops.multiply(m, clip)
    sh = np.asarray(m.filter(ImageFilter.GaussianBlur(feather)), np.float32) / 255.0
    arr = np.asarray(paint, np.float32) * ((1.0 - pool) + pool * sh)[:, :, None]
    canvas.paste(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)), (0, 0), m)
    del arr, sh
    return m

def zarafshan(dr, mask, n, rng, rmin, rmax, cols=(GOLD, GOLD_LT, GOLD_DK)):
    a = np.asarray(mask)
    ys, xs = np.nonzero(a[::7, ::7])
    if len(xs) == 0: return
    pick = rng.integers(0, len(xs), n)
    for k in pick:
        x = xs[k] * 7 + rng.integers(0, 7); y = ys[k] * 7 + rng.integers(0, 7)
        r = rmin + (rmax - rmin) * rng.random() ** 2
        c = cols[int(rng.integers(0, len(cols)))]
        dr.ellipse([x - r, y - r, x + r, y + r], fill=c)

def contour_dress(pnt, pts, ink_w, pearl_r, pearl_gap, inset,
                  gold_w=0.0, gold_off=0.0):
    if gold_w > 0:
        pnt.outline(offset_inward(pts, -gold_off), lerp(GOLD_DK, GOLD, .5), gold_w)
    pnt.outline(pts, INK, ink_w)
    pnt.pearls(offset_inward(pts, inset), pearl_gap, pearl_r, NAVY,
               hl=lerp(NAVY_LT, IVORY, 0.35))


def build():
    rng = np.random.default_rng(4242)
    canvas = gold_ground(CW, CH, rng).convert("RGB")
    yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
    halo = np.exp(-(((xx - CX) / (CW * 0.52)) ** 2 + ((yy - CY) / (CH * 0.46)) ** 2) * 2.0)
    ar = np.asarray(canvas, np.float32) * (1.0 + 0.055 * halo)[:, :, None]
    canvas = Image.fromarray(np.clip(ar, 0, 255).astype(np.uint8))
    del yy, xx, halo, ar
    rose = rose_ground(CW, CH, rng)
    fld = field_mask()

    # ---------------- shapes ------------------------------------------------
    A_out = Shape(8, 0.150, 0.72, R=u(1292), ky=1.200, rot=0.0)
    A_o = A_out.pts(); A_i = offset_inward(A_o, u(166))

    B_out = Shape(8, 0.245, 0.62, R=u(756), ky=1.42, rot=0.0, point=0.045)
    B_in  = Mandorla(u(336), u(650), amp=0.085, p=0.70, lobes=4)
    B_o, B_i = B_out.pts(), B_in.pts()

    P_up = Shape(8, 0.230, 0.85, R=u(122), ky=1.30, rot=0.0, cy=CY - u(1265))
    P_dn = Shape(8, 0.230, 0.85, R=u(122), ky=1.30, rot=0.0, cy=CY + u(1265))

    # ---------------- rose registers ---------------------------------------
    mA = paint_band(canvas, rose, A_o, A_i, clip=fld)
    mB = paint_band(canvas, rose, B_o, B_i, clip=fld)
    mP = None
    for P in (P_up, P_dn):
        po = P.pts(); pi = offset_inward(po, u(30))
        mm = paint_band(canvas, rose, po, pi, clip=fld, pool=0.30, feather=u(4))
        mP = mm if mP is None else ImageChops.lighter(mP, mm)

    # ---------------- reserved centre: paler ground + gold sprinkling -------
    m_res = ImageChops.multiply(poly_mask(B_i), fld)
    arr = np.asarray(canvas, np.float32)
    arr = np.clip(arr * 1.045 + 9.0, 0, 255)
    canvas.paste(Image.fromarray(arr.astype(np.uint8)), (0, 0),
                 m_res.filter(ImageFilter.GaussianBlur(u(2))))
    del arr

    # ---------------- ornament (one quadrant, mirrored fourfold) -----------
    pnt = Painter((CW, CH), rng)
    A0, A1 = -np.pi / 2, 0.0
    bandB = Band(B_out, B_in)
    band_scroll(pnt, bandB, A0, A1, waves=2.0, amp=0.46, ms=1.0,
                serr=0.11, leaf_gap=0.043)
    axis_motif(pnt, bandB, A0, ms=1.0)
    axis_motif(pnt, bandB, A1, ms=0.94)

    bandA = Band(A_o, A_i)
    band_scroll(pnt, bandA, A0, A1, waves=3.0, amp=0.48, ms=1.95, nvines=1,
                stem=1.05, big=True, leaf_gap=0.044, serr=0.10, minor=True)

    gp = Painter((CW, CH), rng)
    gap = Band(A_i, B_o)
    gold_tracery(gp, gap, A0, A1, waves=6.0, amp=0.36, ms=0.66)
    corner_lachak(gp, CW - u(M), u(M), math.radians(135), u(520))
    gpl = fourfold(gp.im)
    gold_zone = ImageChops.multiply(
        ImageChops.subtract(poly_mask(A_i), poly_mask(B_o)), fld)
    gold_zone = ImageChops.lighter(
        gold_zone, ImageChops.multiply(fld, ImageChops.invert(poly_mask(A_o))))
    gpl.putalpha(ImageChops.multiply(gpl.split()[3], gold_zone))
    gpl.putalpha(gpl.split()[3].point(lambda v: int(v * 0.90)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), gpl).convert("RGB")
    del gp, gpl

    orn = fourfold(pnt.im)
    orn.putalpha(ImageChops.multiply(orn.split()[3],
                 ImageChops.multiply(ImageChops.lighter(mA, mB), fld)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), orn).convert("RGB")
    del orn, pnt

    # ---------------- pendant hearts ---------------------------------------
    ov = Painter((CW, CH), rng)
    for P in (P_up, P_dn):
        c = (P.cx, P.cy)
        ov.rosette(c[0], c[1], u(46), rot=np.pi / 8, ink_w=max(1.0, u(1.6)))

    # ---------------- contours, pearls, gold rules -------------------------
    ov.outline(offset_inward(B_i, u(30)), lerp(GOLD_DK, INK, .40), u(1.5))
    ov.pearls(offset_inward(B_i, -u(3)), u(15.5), u(4.6), NAVY,
              hl=lerp(NAVY_LT, IVORY, .4))
    contour_dress(ov, B_o, u(2.6), u(4.8), u(16.0), u(11), gold_w=u(1.6), gold_off=u(6))
    ov.outline(B_i, INK, u(2.4))
    contour_dress(ov, A_o, u(2.2), u(3.9), u(13.0), u(9), gold_w=u(1.4), gold_off=u(5))
    ov.outline(A_i, INK, u(2.0))
    ov.pearls(offset_inward(A_i, -u(9)), u(13.0), u(3.9), NAVY,
              hl=lerp(NAVY_LT, IVORY, .4))
    for P in (P_up, P_dn):
        po = P.pts()
        ov.outline(po, INK, u(2.0))
        ov.pearls(offset_inward(po, u(9)), u(12.0), u(3.6), NAVY,
                  hl=lerp(NAVY_LT, IVORY, .4))

    ov.im.putalpha(ImageChops.multiply(ov.im.split()[3], fld)
                   .point(lambda v: int(v * 0.94)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), ov.im).convert("RGB")
    del ov

    # ---------------- gold sprinkling --------------------------------------
    spark = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    ds = ImageDraw.Draw(spark)
    zarafshan(ds, m_res, int(520 * Q * Q), rng, u(0.9), u(2.6),
              cols=(GOLD, GOLD_LT, lerp(GOLD, GOLD_LT, .5)))
    gold_field = ImageChops.subtract(ImageChops.subtract(fld, poly_mask(A_o)), poly_mask(B_i))
    gold_field = ImageChops.lighter(gold_field,
                 ImageChops.subtract(poly_mask(A_i), poly_mask(B_o)))
    zarafshan(ds, gold_field, int(420 * Q * Q), rng, u(0.8), u(2.1),
              cols=(GOLD, GOLD_LT, lerp(GOLD, GOLD_LT, .5)))
    spark = spark.filter(ImageFilter.GaussianBlur(u(0.35)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), spark).convert("RGB")
    del spark, ds

    return canvas

# ----------------------------------------------------------------------------
# jadval (ruled frame) + caption
# ----------------------------------------------------------------------------
FONTDIR = "/mnt/skills/examples/canvas-design/canvas-fonts"

def _font(name, size):
    for d in (FONTDIR, "/root/.claude/skills/synced"):
        p = os.path.join(FONTDIR, name)
        if os.path.exists(p):
            try: return ImageFont.truetype(p, int(size))
            except Exception: pass
    return ImageFont.load_default()

def jadval(canvas, rng):
    ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    def rule(inset, w, col):
        d.rectangle([u(inset), u(inset), CW - u(inset) - 1, CH - u(inset) - 1],
                    outline=col, width=max(1, int(round(u(w)))))
    rule(M,        3.0, INK)                      # innermost, hugs the field
    rule(M - 13,   1.6, lerp(GOLD_DK, INK, .35))
    rule(M - 29,  15.0, lerp(GOLD, GOLD_LT, .30)) # burnished gold band
    d.rectangle([u(M - 36), u(M - 36), CW - u(M - 36) - 1, CH - u(M - 36) - 1],
                outline=lerp(GOLD_DK, INK, .50), width=max(1, int(round(u(1.6)))))
    d.rectangle([u(M - 22), u(M - 22), CW - u(M - 22) - 1, CH - u(M - 22) - 1],
                outline=lerp(GOLD_DK, INK, .50), width=max(1, int(round(u(1.6)))))
    rule(M - 56,   3.0, NAVY)                     # outer indigo keeper
    rule(M - 66,   1.4, lerp(GOLD_DK, INK, .3))
    rule(M - 84,   1.4, lerp(GOLD_DK, INK, .2))
    return Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")

def caption(canvas):
    ov = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    f = _font("Italiana-Regular.ttf", u(23))
    txt = "TURANJ IN FOUR REGISTERS"
    sub = "PLATE I"
    def track(dr, s, cx, cy, font, sp, fill):
        ws = [dr.textlength(ch, font=font) for ch in s]
        total = sum(ws) + sp * (len(s) - 1)
        x = cx - total / 2.0
        for ch, w in zip(s, ws):
            dr.text((x, cy), ch, font=font, fill=fill, anchor="lm")
            x += w + sp
    col = (74, 52, 36, 232)
    track(d, sub, CW / 2, CH - u(126), _font("Italiana-Regular.ttf", u(19)), u(7.0), col)
    track(d, txt, CW / 2, CH - u(86), f, u(9.0), col)
    # two hairline keepers flanking the caption
    y = CH - u(86)
    for s in (-1, 1):
        x0 = CW / 2 + s * u(300); x1 = CW / 2 + s * u(430)
        d.line([x0, y, x1, y], fill=(120, 92, 60, 120), width=max(1, int(u(1.2))))
    return Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")

# ----------------------------------------------------------------------------
# finishing: paper, bloom, vignette
# ----------------------------------------------------------------------------
def finish(canvas, rng):
    canvas = canvas.filter(ImageFilter.GaussianBlur(u(0.32)))
    a = np.asarray(canvas, np.float32)
    h, w = a.shape[:2]
    # paper tooth
    grain = rng.normal(0, 1, (h, w)).astype(np.float32)
    grain = np.asarray(Image.fromarray(np.clip(grain * 26 + 128, 0, 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(u(0.45))), np.float32)
    a *= (1.0 + ((grain - 128) / 128.0) * 0.055)[:, :, None]
    # fibre streaks of the wasli
    fib = _vnoise(h, w, max(2.0, u(1.6)), rng)
    fib = np.asarray(Image.fromarray((fib * 255).astype(np.uint8))
                     .filter(ImageFilter.GaussianBlur(u(0.8))), np.float32) / 255.0
    a *= (1.0 + (fib - 0.5) * 0.045)[:, :, None]
    # raking light + vignette
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx = xx / w - 0.5; ny = yy / h - 0.5
    lig = 1.0 + 0.055 * (-nx * 0.8 - ny) - 0.30 * (nx * nx * 1.9 + ny * ny * 1.15) ** 1.35
    a *= lig[:, :, None]
    a = a * 1.022 + 3.0
    a[:, :, 0] *= 1.008; a[:, :, 2] *= 0.986
    del grain, fib, yy, xx, nx, ny, lig
    canvas = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    del a
    if Q != 1.0:
        canvas = canvas.resize((PW, PH), Image.LANCZOS)
    # final bite
    canvas = canvas.filter(ImageFilter.UnsharpMask(radius=1.6, percent=62, threshold=2))
    return canvas

def main():
    rng = np.random.default_rng(777)
    im = build()
    im = jadval(im, rng)
    im = caption(im)
    im = finish(im, rng)
    out = os.environ.get("OUT", "patient-gold-plate-I")
    im.save(out + ".png", "PNG", dpi=(300, 300))
    if os.environ.get("PDF", "0") == "1":
        im.save(out + ".pdf", "PDF", resolution=300.0)
    print("wrote", out + ".png", im.size)

if __name__ == "__main__":
    main()
