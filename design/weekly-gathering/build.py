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
def medallion(cx, cy, R, scale_w=1.0):
    """A rosette built in legible concentric registers — each band given its own air.
       Radii are chosen so no two figures ever occupy the same ground."""
    u = R/150.0
    w = lambda v: round(v*scale_w, 3)
    g = []

    # register I — the outer rim, and 99 marks: a tasbih told in light,
    #              with three longer strokes at the thirds.
    g.append(circle(cx, cy, 150*u, "hair-2", w(1.2)))
    g.append(circle(cx, cy, 146.4*u, "hair-5", w(0.6)))
    g += [path(d, "hair-2", w(0.85)) for d in
          tick_ring(cx, cy, 138*u, 145*u, 99, accents=(0, 33, 66), acc_ext=4.5*u)]
    g.append(circle(cx, cy, 135*u, "hair-2", w(1.0)))

    # register II — a sixteen-pointed star band, its chords held to the band
    g.append(f'<defs><clipPath id="bandA" clipPathUnits="userSpaceOnUse">'
             f'<path clip-rule="evenodd" d="{annulus(cx, cy, 134*u, 102.5*u)}"/></clipPath>'
             f'<clipPath id="bandB" clipPathUnits="userSpaceOnUse">'
             f'<path clip-rule="evenodd" d="{annulus(cx, cy, 58.5*u, 22.5*u)}"/></clipPath></defs>')
    g.append('<g clip-path="url(#bandA)">')
    for d in star_polygon(cx, cy, 133.5*u, 16, 5):
        g.append(path(d, "hair-1", w(1.0)))
    for d in star_polygon(cx, cy, 133.5*u, 16, 5, rot=360/32):
        g.append(path(d, "hair-4", w(0.6)))
    g.append('</g>')
    g.append(circle(cx, cy, 103*u, "hair-3", w(0.85)))
    g.append(circle(cx, cy, 100*u, "hair-5", w(0.55)))

    # register III — a corona of sixteen petals in its own clear band
    for d in petal_ring(cx, cy, 62*u, 98*u, 16, rot=360/32):
        g.append(path(d, "petal", w(0.75)))
    g.append(circle(cx, cy, 60.5*u, "hair-3", w(0.85)))

    # register IV — the eight-fold heart
    g.append('<g clip-path="url(#bandB)">')
    for d in star_polygon(cx, cy, 58*u, 8, 3):
        g.append(path(d, "hair-1", w(0.95)))
    g.append('</g>')
    g.append(circle(cx, cy, 23*u, "hair-2", w(0.85)))
    for d in petal_ring(cx, cy, 8*u, 21*u, 8, rot=22.5, bulge=0.55):
        g.append(path(d, "petal-lit", w(0.6)))
    g.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{4.6*u:.3f}" class="dot"/>')
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

W, H = 1200, 1800
CX = W/2
PY_ = 0  # placeholder

# ---------- the scene ----------
ARCH_L, ARCH_R, ARCH_BASE, ARCH_APEX = 250, 950, 766, 118
def arch(inset=0.0, cls="hair-4", w=0.8):
    l, r = ARCH_L+inset, ARCH_R-inset
    b, a = ARCH_BASE, ARCH_APEX+inset*0.9
    sh = 430+inset*0.4
    return (f'<path d="M {l},{b} L {l},{sh} Q {l},{a+95} {CX},{a} '
            f'Q {r},{a+95} {r},{sh} L {r},{b}" class="{cls}" stroke-width="{w}" fill="none"/>')

MED_CY, MED_R = 386, 150

svg = f'''
<svg class="layer" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
    <radialGradient id="halo" cx="50%" cy="{MED_CY/H*100:.1f}%" r="34%">
      <stop offset="0%"   stop-color="#EDC784" stop-opacity="0.19"/>
      <stop offset="55%"  stop-color="#C79A4E" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#halo)"/>

  <g class="ground">{ground_rosette(CX, 1060, 720)}</g>

  {arch(0, "hair-5", 1.0)}
  {arch(11, "hair-5", 0.6)}

  <!-- frame -->
  <rect x="44" y="44" width="{W-88}" height="{H-88}" class="hair-3" stroke-width="1.1" fill="none"/>
  <rect x="57" y="57" width="{W-114}" height="{H-114}" class="hair-5" stroke-width="0.7" fill="none"/>
  {corner(44,44,1,1)}{corner(W-44,44,-1,1)}{corner(44,H-44,1,-1)}{corner(W-44,H-44,-1,-1)}

  <g class="med">{medallion(CX, MED_CY, MED_R)}</g>

  {rule(CX, ARCH_BASE, 350)}
  <line x1="{CX}" y1="{ARCH_BASE+34}" x2="{CX}" y2="{ARCH_BASE+128}" class="rule"/>

  {rule(CX, 1246, 350)}
  <rect x="{CX-322}" y="1424" width="644" height="152" rx="2" class="hair-3" stroke-width="1" fill="none"/>
  <rect x="{CX-315}" y="1431" width="630" height="138" rx="1" class="hair-5" stroke-width="0.6" fill="none"/>
  {lozenge(CX-322,1500,5,8,"fill-ink")}{lozenge(CX+322,1500,5,8,"fill-ink")}
  {lozenge(CX-322,1500,5,8,"stroke-node")}{lozenge(CX+322,1500,5,8,"stroke-node")}
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
.ground{{opacity:.085}}
.med{{filter:drop-shadow(0 0 16px rgba(230,192,116,.26))}}

/* --- type --- */
.at{{position:absolute;left:0;right:0;text-align:center}}
.gold{{background:linear-gradient(178deg,#FBEECB 0%,#E7CD92 26%,#C69E56 58%,#F3E3B7 82%,#D3AE68 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 1px 0 rgba(0,0,0,.55)) drop-shadow(0 0 18px rgba(214,172,100,.22))}}
.ayah{{font-family:Amiri,serif;font-size:40px;line-height:1.55;color:#E9CE95;
  direction:rtl;filter:drop-shadow(0 0 16px rgba(214,172,100,.28))}}
.gloss{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:20.5px;
  letter-spacing:.055em;color:#A98D5C}}
.t1{{font-family:Cinzel,serif;font-weight:600;font-size:57px;letter-spacing:.135em;
  text-indent:.135em;line-height:1}}
.t2{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:43px;
  letter-spacing:.045em;color:#E0C289}}
.lab{{font-family:Cinzel,serif;font-weight:400;font-size:12.5px;letter-spacing:.5em;
  text-indent:.5em;color:#A5874A}}
.val{{font-family:Cormorant,serif;font-weight:400;font-size:33px;letter-spacing:.075em;
  text-indent:.075em;color:#EDD59B}}
.body{{font-family:Cormorant,serif;font-weight:300;font-size:24.5px;line-height:1.62;white-space:nowrap;
  letter-spacing:.022em;color:#CBB080}}
.body em{{font-style:italic;color:#E0C289}}
.pt{{font-variant-numeric:lining-nums;font-family:Cinzel,serif;font-weight:400;font-size:14.5px;letter-spacing:.16em;
  text-indent:.16em;color:#E6CB93}}
.pd{{font-family:Cormorant,serif;font-weight:300;font-size:21.5px;line-height:1.46;
  letter-spacing:.03em;color:#B09462}}
.rn{{font-family:Cinzel,serif;font-size:11px;font-size:11.5px;letter-spacing:.34em;text-indent:.34em;color:#A08142}}
.venue{{font-family:Cinzel,serif;font-weight:600;font-size:39px;letter-spacing:.18em;text-indent:.18em}}
.vsub{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:23px;
  letter-spacing:.06em;color:#AC9060}}
.addr{{font-variant-numeric:lining-nums;font-feature-settings:'lnum' 1;font-family:Cormorant,serif;font-weight:400;font-size:24px;letter-spacing:.13em;
  text-indent:.13em;color:#D3B67F;text-transform:uppercase}}
.wa{{font-variant-numeric:lining-nums;font-feature-settings:'lnum' 1;font-family:Cormorant,serif;font-weight:400;font-size:34.5px;letter-spacing:.1em;
  text-indent:.1em;color:#F0D9A2}}
.note{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:20px;
  letter-spacing:.05em;color:#9C8250}}
.url{{font-family:Cinzel,serif;font-size:12.5px;letter-spacing:.42em;text-indent:.42em;color:#8A6F3A}}
.cols{{position:absolute;left:{CX-350}px;width:700px;display:grid;
  grid-template-columns:1fr 1fr 1fr;text-align:center}}
.cols > div{{padding:0 14px}}
.cols > div + div{{border-left:1px solid rgba(138,108,52,.5)}}
</style></head>
<body><div class="page">
{svg}

<div class="at ayah" style="top:112px">{AYAH}</div>
<div class="at gloss" style="top:180px">“ Verily, in the remembrance of God do hearts find rest. ”</div>

<div class="at t1 gold" style="top:568px">TARIQA QADIRIYYA</div>
<div class="at t1 gold" style="top:634px">BOUTCHICHIYA</div>
<div class="at t2" style="top:704px">Weekly Dhikr Gathering</div>

<div class="at lab" style="top:{ARCH_BASE+32}px;left:{CX-350}px;width:340px">SATURDAY</div>
<div class="at val" style="top:{ARCH_BASE+58}px;left:{CX-350}px;width:340px">29 August 2026</div>
<div class="at lab" style="top:{ARCH_BASE+32}px;left:{CX+10}px;width:340px">EVENING</div>
<div class="at val" style="top:{ARCH_BASE+58}px;left:{CX+10}px;width:340px">7:00 – 9:00 pm</div>

<div class="at body" style="top:940px;left:{CX-440}px;width:880px">
Direct Sufi practice of the Moroccan <em>dhikr</em>, with trained practitioners<br>
reciting with <em>idhn</em> — permission — from a recognised master<br>
of the Qadiriyya Boutchichiya Sufi order.
</div>

<div class="cols" style="top:1100px">
  <div><div class="rn">I</div><div class="pt" style="margin-top:9px">7:00 — 8:15</div>
       <div class="pd" style="margin-top:11px">Wadhifa Dhikr<br>and Dhikr al&nbsp;Faraj</div></div>
  <div><div class="rn">II</div><div class="pt" style="margin-top:9px">8:15 — 8:30</div>
       <div class="pd" style="margin-top:11px">Talk</div></div>
  <div><div class="rn">III</div><div class="pt" style="margin-top:9px">8:30</div>
       <div class="pd" style="margin-top:11px">Maghrib, followed<br>by refreshments</div></div>
</div>

<div class="at venue gold" style="top:1276px">CRESCENT HALL</div>
<div class="at vsub" style="top:1332px">Crescent Nursery</div>
<div class="at addr" style="top:1368px">162 Edmund Street · Rochdale OL12 6QG</div>

<div class="at lab" style="top:1458px">PLEASE CONFIRM YOUR ATTENDANCE</div>
<div class="at wa" style="top:1488px">WhatsApp 07884 053544</div>
<div class="at note" style="top:1534px">A brothers-only gathering</div>

<div class="at url" style="top:1660px">WWW.THESUFIWAY.CO.UK</div>
</div></body></html>'''

(HERE/"poster.html").write_text(html, encoding="utf-8")
print("html:", (HERE/"poster.html").stat().st_size, "bytes")
