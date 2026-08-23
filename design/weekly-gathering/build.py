#!/usr/bin/env python3
# LAMPLIGHT GEOMETRY — poster generator
import math, base64, pathlib, textwrap

HERE = pathlib.Path(__file__).parent
F = HERE / "fonts"

# ---------- geometry helpers ----------
def P(cx, cy, r, a):           # polar -> cartesian (a in degrees, 0 = up)
    t = math.radians(a - 90)
    return (cx + r*math.cos(t), cy + r*math.sin(t))

def fmt(pts, close=True):
    d = "M " + " L ".join(f"{x:.3f},{y:.3f}" for x, y in pts)
    return d + (" Z" if close else "")

def star_polygon(cx, cy, r, n, step, rot=0.0):
    """{n/step} star polygon, drawn as one or more closed paths."""
    paths, seen = [], set()
    for s in range(math.gcd(n, step)):
        if s in seen: continue
        pts, i = [], s
        while True:
            pts.append(P(cx, cy, r, rot + i*360.0/n))
            seen.add(i)
            i = (i + step) % n
            if i == s: break
        paths.append(fmt(pts))
    return paths

def polygon(cx, cy, r, n, rot=0.0):
    return fmt([P(cx, cy, r, rot + i*360.0/n) for i in range(n)])

def petal_ring(cx, cy, r_in, r_out, n, rot=0.0, bulge=0.42):
    """n almond/vesica petals standing between two radii."""
    out = []
    half = 360.0/n/2.0
    for i in range(n):
        a = rot + i*360.0/n
        tip  = P(cx, cy, r_out, a)
        base = P(cx, cy, r_in,  a)
        c1   = P(cx, cy, r_in + (r_out-r_in)*0.5, a - half*bulge*2)
        c2   = P(cx, cy, r_in + (r_out-r_in)*0.5, a + half*bulge*2)
        out.append(
            f"M {base[0]:.3f},{base[1]:.3f} Q {c1[0]:.3f},{c1[1]:.3f} {tip[0]:.3f},{tip[1]:.3f} "
            f"Q {c2[0]:.3f},{c2[1]:.3f} {base[0]:.3f},{base[1]:.3f} Z")
    return out

def tick_ring(cx, cy, r0, r1, n, rot=0.0, accents=(), acc_ext=0.0):
    out = []
    for i in range(n):
        a = rot + i*360.0/n
        e = acc_ext if i in accents else 0.0
        x0, y0 = P(cx, cy, r0 - e, a)
        x1, y1 = P(cx, cy, r1 + e, a)
        out.append(f"M {x0:.3f},{y0:.3f} L {x1:.3f},{y1:.3f}")
    return out

def annulus(cx, cy, ro, ri):
    return (f"M {cx-ro:.2f},{cy:.2f} a {ro:.2f},{ro:.2f} 0 1,0 {2*ro:.2f},0 "
            f"a {ro:.2f},{ro:.2f} 0 1,0 {-2*ro:.2f},0 Z "
            f"M {cx-ri:.2f},{cy:.2f} a {ri:.2f},{ri:.2f} 0 1,0 {2*ri:.2f},0 "
            f"a {ri:.2f},{ri:.2f} 0 1,0 {-2*ri:.2f},0 Z")


def circle(cx, cy, r, cls, w=1.0):
    return f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}" class="{cls}" stroke-width="{w}"/>'

def path(d, cls, w=1.0):
    return f'<path d="{d}" class="{cls}" stroke-width="{w}"/>'


# ---------- the medallion (hero) ----------
def halo(cx, cy, R, seal_r):
    """A drawn setting for the order's seal: a rim, and ninety-nine marks —
       a tasbih told in light, with three longer strokes at the thirds."""
    u = R/150.0
    g = [circle(cx, cy, 150*u, "hair-5", 0.65),
         circle(cx, cy, 146*u, "hair-2", 1.15)]
    g += [path(d, "hair-2", 0.85) for d in
          tick_ring(cx, cy, 132*u, 140*u, 99, accents=(0, 33, 66), acc_ext=4.5*u)]
    return "\n".join(g)


def zellij(p_, R=None):
    """One repeat of the Moroccan star-and-cross. One khatim per tile, its
       eight points reaching exactly to the tile edge, so neighbouring stars
       meet tip to tip and the square between four of them is the cross."""
    R = R or p_/2
    inner = R*0.76537                      # where the two squares cross
    star = fmt([P(p_/2, p_/2, R if i % 2 == 0 else inner, i*22.5) for i in range(16)])
    h = R*(1 - 0.70711)                    # the small square, cornered on four star tips
    sq = [f"M {cx-h:.2f},{cy-h:.2f} h {2*h:.2f} v {2*h:.2f} h {-2*h:.2f} Z"
          for cx, cy in ((0,0), (p_,0), (0,p_), (p_,p_))]
    return [star] + sq


def zellij_layer(p_, cls="zh", w=0.9, studs=True):
    g = [f'<pattern id="zj{int(p_)}" width="{p_}" height="{p_}" patternUnits="userSpaceOnUse">']
    for d in zellij(p_):
        g.append(f'<path d="{d}" fill="none" class="{cls}" stroke-width="{w}"/>')
    if studs:
        for cx, cy in ((p_/2, p_/2),):
            g.append(f'<path d="{fmt([P(cx,cy,p_*0.052,a*90) for a in range(4)])}" class="zstud"/>')
    g.append('</pattern>')
    return "\n".join(g)


def ground_rosette(cx, cy, R):
    """Vast, faint field geometry — felt more than seen."""
    u = R/150.0
    g = []
    g += [path(d, "gh", 0.8) for d in tick_ring(cx, cy, 150*u, 158*u, 192)]
    g.append(circle(cx, cy, 150*u, "gh", 0.9))
    g.append(circle(cx, cy, 118*u, "gh", 0.7))
    for d in star_polygon(cx, cy, 148*u, 24, 11): g.append(path(d, "gh", 0.7))
    for d in star_polygon(cx, cy, 116*u, 12, 5):  g.append(path(d, "gh", 0.7))
    g.append(circle(cx, cy, 74*u, "gh", 0.7))
    for d in petal_ring(cx, cy, 74*u, 114*u, 24, rot=360/48): g.append(path(d, "gh", 0.55))
    return "\n".join(g)


def corner(x, y, sx, sy, s=1.0):
    """Quarter-rosette joinery for the frame corners."""
    g, R = [], 96*s
    g.append(f'<g transform="translate({x},{y}) scale({sx},{sy})">')
    g.append(f'<path d="M 0,{R:.1f} A {R:.1f},{R:.1f} 0 0 1 {R:.1f},0" class="hair-3" stroke-width="0.9"/>')
    g.append(f'<path d="M 0,{R*0.62:.1f} A {R*0.62:.1f},{R*0.62:.1f} 0 0 1 {R*0.62:.1f},0" class="hair-4" stroke-width="0.7"/>')
    for i in range(7):
        a = 90*i/6.0
        x0, y0 = P(0, 0, R*0.62, a); x1, y1 = P(0, 0, R, a)
        g.append(f'<path d="M {x0:.2f},{-y0:.2f} L {x1:.2f},{-y1:.2f}" class="hair-4" stroke-width="0.65"/>')
    g.append(f'<path d="M 0,{R*1.5:.1f} L 0,{R*0.62:.1f}" class="hair-4" stroke-width="0.65"/>')
    g.append(f'<path d="M {R*0.62:.1f},0 L {R*1.5:.1f},0" class="hair-4" stroke-width="0.65"/>')
    g.append('</g>')
    return "\n".join(g)


def lozenge(cx, cy, w=7.0, h=11.0, cls="fill-lit"):
    return (f'<path d="M {cx:.1f},{cy-h:.1f} L {cx+w:.1f},{cy:.1f} '
            f'L {cx:.1f},{cy+h:.1f} L {cx-w:.1f},{cy:.1f} Z" class="{cls}"/>')

def rule(cx, y, half, node=True):
    """Hairline rule that thins to nothing at both ends, with a lozenge node."""
    g = [f'<line x1="{cx-half}" y1="{y}" x2="{cx+half}" y2="{y}" class="rule"/>']
    if node:
        g.append(lozenge(cx, y, 6.5, 10))
        g.append(f'<line x1="{cx-half}" y1="{y}" x2="{cx-half+28}" y2="{y}" class="rule-lit"/>')
        g.append(f'<line x1="{cx+half-28}" y1="{y}" x2="{cx+half}" y2="{y}" class="rule-lit"/>')
    return "\n".join(g)


# ---------- fonts ----------
def face(fam, file, weight="400", style="normal"):
    b64 = base64.b64encode((F/file).read_bytes()).decode()
    return (f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")

FONTS = "\n".join([
    face("Cinzel", "Cinzel-400.woff2", "400 600"),
    face("Cormorant", "CormorantGaramond-300.woff2", "300"),
    face("Cormorant", "CormorantGaramond-400.woff2", "400"),
    face("Cormorant", "CormorantGaramond-500.woff2", "500"),
    face("Cormorant", "CormorantGaramond-300-italic.woff2", "300", "italic"),
    face("Cormorant", "CormorantGaramond-400-italic.woff2", "400", "italic"),
    face("Marcellus", "Marcellus-400.woff2", "400"),
    face("Amiri", "Amiri-Regular-400.woff2", "400"),
])

def mask_uri(name):
    return "data:image/png;base64," + base64.b64encode((HERE/name).read_bytes()).decode()

SEAL_URI = mask_uri("mask-seal.png")
WORD_URI = mask_uri("mask-wordmark.png")

W, H = 1200, 1800
CX = W/2
PY_ = 0  # placeholder

# ---------- the scene ----------
ARCH_L, ARCH_R, ARCH_BASE, ARCH_APEX = 250, 950, 840, 118
def arch(inset=0.0, cls="hair-4", w=0.8):
    l, r = ARCH_L+inset, ARCH_R-inset
    b, a = ARCH_BASE, ARCH_APEX+inset*0.9
    sh = 430+inset*0.4
    return (f'<path d="M {l},{b} L {l},{sh} Q {l},{a+95} {CX},{a} '
            f'Q {r},{a+95} {r},{sh} L {r},{b}" class="{cls}" stroke-width="{w}" fill="none"/>')

MED_CY, MED_R, SEAL_D = 360, 149, 252

tiles = f'''
<svg class="layer tiles" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    {zellij_layer(104, "zh", 1.0)}
    {zellij_layer(26, "zf", 0.55, studs=False)}
  </defs>
  <rect width="{W}" height="{H}" fill="url(#zj26)" opacity="0.22"/>
  <rect width="{W}" height="{H}" fill="url(#zj104)"/>
</svg>
<div class="scrim"></div>
'''

svg = f'''
<svg class="layer" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
    <radialGradient id="halo" cx="50%" cy="{MED_CY/H*100:.1f}%" r="52%">
      <stop offset="0%"   stop-color="#EFCB8A" stop-opacity="0.20"/>
      <stop offset="26%"  stop-color="#DCB068" stop-opacity="0.105"/>
      <stop offset="48%"  stop-color="#C79A4E" stop-opacity="0.048"/>
      <stop offset="72%"  stop-color="#A87F3A" stop-opacity="0.016"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#halo)"/>

  <g class="ground">{ground_rosette(CX, 1060, 720)}</g>

  {arch(0, "hair-5", 1.0)}
  {arch(11, "hair-5", 0.6)}

  <!-- frame: a tiled band, the way a Moroccan wall carries its dado -->
  <defs>{zellij_layer(36, "zb", 0.75, studs=False)}</defs>
  <path class="band" fill-rule="evenodd" fill="url(#zj36)"
        d="M38,38 H{W-38} V{H-38} H38 Z M74,74 H{W-74} V{H-74} H74 Z"/>
  <rect x="38" y="38" width="{W-76}" height="{H-76}" class="hair-3" stroke-width="1.15" fill="none"/>
  <rect x="45" y="45" width="{W-90}" height="{H-90}" class="hair-5" stroke-width="0.6" fill="none"/>
  <rect x="74" y="74" width="{W-148}" height="{H-148}" class="hair-3" stroke-width="1.0" fill="none"/>
  <rect x="81" y="81" width="{W-162}" height="{H-162}" class="hair-5" stroke-width="0.6" fill="none"/>
  {corner(74,74,1,1,0.66)}{corner(W-74,74,-1,1,0.66)}{corner(74,H-74,1,-1,0.66)}{corner(W-74,H-74,-1,-1,0.66)}

  <g class="med">{halo(CX, MED_CY, MED_R, SEAL_D/2)}</g>

  {rule(CX, ARCH_BASE, 350)}
  <line x1="{CX}" y1="{ARCH_BASE+34}" x2="{CX}" y2="{ARCH_BASE+128}" class="rule"/>

  {rule(CX, 1272, 350)}
  <rect x="{CX-322}" y="1444" width="644" height="152" rx="2" class="hair-3" stroke-width="1" fill="none"/>
  <rect x="{CX-315}" y="1451" width="630" height="138" rx="1" class="hair-5" stroke-width="0.6" fill="none"/>
  {lozenge(CX-322,1520,5,8,"fill-ink")}{lozenge(CX+322,1520,5,8,"fill-ink")}
  {lozenge(CX-322,1520,5,8,"stroke-node")}{lozenge(CX+322,1520,5,8,"stroke-node")}
</svg>
<div class="grain"></div>
'''

AYAH = "أَلَا بِذِكْرِ ٱللَّٰهِ تَطْمَئِنُّ ٱلْقُلُوبُ"

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Weekly Dhikr Gathering</title>
<style>
{FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#000}}
@page{{size:12.5in 18.75in;margin:0}}
@media print{{html,body{{background:#0C0704;-webkit-print-color-adjust:exact;print-color-adjust:exact}}}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
  background:
    radial-gradient(112% 62% at 50% 24%, #3B2711 0%, #26190B 34%, #150E07 62%, #0C0704 100%),
    radial-gradient(88% 42% at 50% 96%, #241809 0%, #120C06 46%, #0A0603 100%);
  font-kerning:normal;-webkit-font-smoothing:antialiased;}}
.layer{{position:absolute;inset:0;width:100%;height:100%}}
.grain{{position:absolute;inset:0;opacity:.05;mix-blend-mode:overlay;pointer-events:none;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4'/><feColorMatrix type='saturate' values='0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>");}}

/* --- the metal --- */
.hair-1{{fill:none;stroke:#E8CE95;opacity:.97}}
.hair-2{{fill:none;stroke:#C6A25C;opacity:.85}}
.hair-3{{fill:none;stroke:#9A7A3C;opacity:.80}}
.hair-4{{fill:none;stroke:#7E6230;opacity:.75}}
.hair-5{{fill:none;stroke:#6A5228;opacity:.55}}
.petal{{fill:rgba(200,160,86,.055);stroke:#B08F4E;opacity:.75}}
.petal-lit{{fill:rgba(232,198,124,.10);stroke:#E2C284;opacity:.9}}
.dot{{fill:#F2DFAE}}
.fill-lit{{fill:#D9B978}}
.fill-ink{{fill:#150E06}}
.stroke-node{{fill:none;stroke:#9A7A3C;stroke-width:1}}
.rule{{stroke:#8A6C34;stroke-width:1;opacity:.85}}
.rule-lit{{stroke:#DCBB79;stroke-width:1;opacity:.9}}
.ground{{opacity:.072}}
.zh{{stroke:#C9A25C}}
.zf{{stroke:#9A7A3C}}
.zstud{{fill:#C9A25C}}
.zb{{stroke:#C6A059}}
.band{{opacity:.30}}
.tiles{{opacity:.17}}
.scrim{{position:absolute;inset:0;pointer-events:none;
  background:
    radial-gradient(62% 34% at 50% 21%, rgba(10,7,4,.80) 0%, rgba(10,7,4,.42) 58%, rgba(10,7,4,0) 100%),
    radial-gradient(72% 40% at 50% 61%, rgba(10,7,4,.86) 0%, rgba(10,7,4,.50) 55%, rgba(10,7,4,0) 100%),
    radial-gradient(64% 26% at 50% 87%, rgba(10,7,4,.84) 0%, rgba(10,7,4,.44) 58%, rgba(10,7,4,0) 100%);}}
.med{{filter:drop-shadow(0 0 16px rgba(230,192,116,.26))}}

/* --- type --- */
.at{{position:absolute;left:0;right:0;text-align:center;
  text-shadow:0 1px 3px rgba(6,4,2,.72), 0 0 14px rgba(6,4,2,.45)}}
.mark{{position:absolute;left:50%;transform:translateX(-50%);
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
  -webkit-mask-size:contain;mask-size:contain;
  -webkit-mask-position:center;mask-position:center;
  background-image:linear-gradient(176deg,#FBEECB 0%,#EBD49B 22%,#C89F55 54%,#F4E5BB 78%,#D2AC64 100%);}}
.seal{{filter:drop-shadow(0 0 20px rgba(232,194,116,.30)) drop-shadow(0 1px 1px rgba(0,0,0,.5))}}
.wordmark{{filter:drop-shadow(0 0 16px rgba(226,186,108,.24)) drop-shadow(0 1px 1px rgba(0,0,0,.55))}}
.gold{{background:linear-gradient(178deg,#FBEECB 0%,#E7CD92 26%,#C69E56 58%,#F3E3B7 82%,#D3AE68 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 1px 0 rgba(0,0,0,.6)) drop-shadow(0 2px 5px rgba(6,4,2,.7))
         drop-shadow(0 0 20px rgba(214,172,100,.26))}}
.at.gold{{text-shadow:none}}
.ayah{{font-family:Amiri,serif;font-size:40px;line-height:1.55;color:#E9CE95;
  direction:rtl;filter:drop-shadow(0 0 16px rgba(214,172,100,.28))}}
.gloss{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:20.5px;
  letter-spacing:.055em;color:#D5B87E}}
.t1{{font-family:Cinzel,serif;font-weight:600;font-size:50px;letter-spacing:.135em;
  text-indent:.135em;line-height:1}}
.t2{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:43px;
  letter-spacing:.045em;color:#EDD29E}}
.lab{{font-family:Cinzel,serif;font-weight:400;font-size:12.5px;letter-spacing:.5em;
  text-indent:.5em;color:#D0B16A}}
.val{{font-family:Cormorant,serif;font-weight:400;font-size:33px;letter-spacing:.075em;
  text-indent:.075em;color:#F5E4B6}}
.body{{font-family:Cormorant,serif;font-weight:400;font-size:24.5px;line-height:1.62;white-space:nowrap;
  letter-spacing:.022em;color:#E3C994}}
.body em{{font-style:italic;color:#E0C289}}
.pt{{font-variant-numeric:lining-nums;font-family:Cinzel,serif;font-weight:400;font-size:14.5px;letter-spacing:.16em;
  text-indent:.16em;color:#F1DBA9}}
.pd{{font-family:Cormorant,serif;font-weight:400;font-size:21.5px;line-height:1.46;
  letter-spacing:.03em;color:#CDB07A}}
.rn{{font-family:Cinzel,serif;font-size:11px;font-size:11.5px;letter-spacing:.34em;text-indent:.34em;color:#B99A55}}
.venue{{font-family:Cinzel,serif;font-weight:600;font-size:39px;letter-spacing:.18em;text-indent:.18em}}
.vsub{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:23px;
  letter-spacing:.06em;color:#C8A974}}
.addr{{font-variant-numeric:lining-nums;font-feature-settings:'lnum' 1;font-family:Cormorant,serif;font-weight:400;font-size:24px;letter-spacing:.13em;
  text-indent:.13em;color:#EFD8A6;text-transform:uppercase}}
.wa{{font-variant-numeric:lining-nums;font-feature-settings:'lnum' 1;font-family:Cormorant,serif;font-weight:400;font-size:34.5px;letter-spacing:.1em;
  text-indent:.1em;color:#F0D9A2}}
.note{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:20px;
  letter-spacing:.05em;color:#B99C66}}
.url{{font-family:Cinzel,serif;font-size:12.5px;letter-spacing:.42em;text-indent:.42em;color:#C0A05C}}
.cols{{position:absolute;left:{CX-350}px;width:700px;display:grid;
  grid-template-columns:1fr 1fr 1fr;text-align:center}}
.cols > div{{padding:0 14px}}
.cols > div + div{{border-left:1px solid rgba(138,108,52,.5)}}
</style></head>
<body><div class="page">
{tiles}
{svg}

<div class="at ayah" style="top:104px">{AYAH}</div>
<div class="at gloss" style="top:172px">“ Verily, in the remembrance of God do hearts find rest. ”</div>

<div class="mark seal" style="top:{MED_CY-SEAL_D//2}px;width:{SEAL_D}px;height:{SEAL_D}px;
  -webkit-mask-image:url({SEAL_URI});mask-image:url({SEAL_URI})"></div>

<div class="mark wordmark" style="top:528px;width:640px;height:113px;
  -webkit-mask-image:url({WORD_URI});mask-image:url({WORD_URI})"></div>

<div class="at t1 gold" style="top:664px">TARIQA AL QADIRIYA</div>
<div class="at t1 gold" style="top:718px">AL BOUTCHICHIYA</div>
<div class="at t2" style="top:780px">Weekly Dhikr Gathering</div>

<div class="at lab" style="top:{ARCH_BASE+32}px;left:{CX-350}px;width:340px">SATURDAY</div>
<div class="at val" style="top:{ARCH_BASE+58}px;left:{CX-350}px;width:340px">29 August 2026</div>
<div class="at lab" style="top:{ARCH_BASE+32}px;left:{CX+10}px;width:340px">EVENING</div>
<div class="at val" style="top:{ARCH_BASE+58}px;left:{CX+10}px;width:340px">7:00 – 9:00 pm</div>

<div class="at body" style="top:976px;left:{CX-440}px;width:880px">
Direct Sufi practice of the Moroccan <em>dhikr</em>, with trained practitioners<br>
reciting with <em>idhn</em> — permission — from a recognised master<br>
of the Qadiriyya Boutchichiya Sufi order.
</div>

<div class="cols" style="top:1128px">
  <div><div class="rn">I</div><div class="pt" style="margin-top:9px">7:00 – 8:15</div>
       <div class="pd" style="margin-top:11px">Wadhifa Dhikr<br>and Dhikr al&nbsp;Faraj</div></div>
  <div><div class="rn">II</div><div class="pt" style="margin-top:9px">8:15 – 8:30</div>
       <div class="pd" style="margin-top:11px">Talk</div></div>
  <div><div class="rn">III</div><div class="pt" style="margin-top:9px">8:30</div>
       <div class="pd" style="margin-top:11px">Maghrib, followed<br>by refreshments</div></div>
</div>

<div class="at venue gold" style="top:1302px">CRESCENT HALL</div>
<div class="at vsub" style="top:1356px">Crescent Nursery</div>
<div class="at addr" style="top:1392px">162 EDMUND STREET · ROCHDALE OL12 6QG</div>

<div class="at lab" style="top:1478px">PLEASE CONFIRM YOUR ATTENDANCE</div>
<div class="at wa" style="top:1508px">WhatsApp 07884 053544</div>
<div class="at note" style="top:1554px">A brothers-only gathering</div>

<div class="at url" style="top:1668px">WWW.THESUFIWAY.CO.UK</div>
</div></body></html>'''

(HERE/"poster.html").write_text(html, encoding="utf-8")
print("html:", (HERE/"poster.html").stat().st_size, "bytes")
