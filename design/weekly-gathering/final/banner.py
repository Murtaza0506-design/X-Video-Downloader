#!/usr/bin/env python3
"""A landscape banner (1600x900) — a crest, not a flyer: the star, the
   wordmark, the tariqa's name and the venue, set against a much denser
   field of Islamic geometry. Renders every established palette in turn."""
import subprocess
from PIL import Image
import variants as v
import final as f

HERE = v.HERE
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W, H = 1600, 900
CX = W/2

def shot(html_path, out_png, w, h, scale=1):
    raw = out_png.with_name("_raw_" + out_png.stem + ".png")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                     f"--force-device-scale-factor={scale}", f"--window-size={w},{h+300}",
                     "--screenshot="+str(raw), "--virtual-time-budget=8000",
                     "file://"+str(html_path.resolve())], capture_output=True)
    im = Image.open(raw).convert("RGB").crop((0, 0, w*scale, h*scale))
    im.save(out_png, optimize=True); raw.unlink()
    print(out_png.name, im.size)

def css_diamond(cx, cy, pal, size=8):
    """A lozenge as a plain rotated div — an SVG <path> dropped straight into
       HTML (outside an <svg>) is silently ignored by the browser."""
    return (f'<div style="position:absolute;left:{cx-size/2:.0f}px;top:{cy-size/2:.0f}px;'
            f'width:{size}px;height:{size}px;background:{pal["fill_lit"]};'
            f'transform:rotate(45deg);box-shadow:0 0 6px rgba(217,185,120,.45)"></div>')

# ---------- a flattened echo of the poster's mihrab arch ----------
BL, BR, B_BASE, B_APEX, B_SH = 300, 1300, 640, 50, 320
def barch_d(inset=0.0):
    l, r = BL+inset, BR-inset
    b, a = B_BASE, B_APEX+inset*0.9
    sh = B_SH+inset*0.35
    return (f'M {l},{b} L {l},{sh} Q {l},{a+160} {CX},{a} '
            f'Q {r},{a+160} {r},{sh} L {r},{b}')

def arch_panel_d(base_y, inset=0.0):
    """The same mihrab curve as barch_d, but with the sides run straight
       down to base_y and closed — a solid niche the full height of the
       middle, not just the arch's cap."""
    l, r = BL+inset, BR-inset
    a = B_APEX+inset*0.9
    sh = B_SH+inset*0.35
    return (f'M {l},{base_y} L {l},{sh} Q {l},{a+160} {CX},{a} '
            f'Q {r},{a+160} {r},{sh} L {r},{base_y} Z')

STAR_CY, STAR_R, STAR_D = 250, 138, 230
WORD_W, WORD_H = 420, 74
WORD_Y = 408
TITLE_Y = WORD_Y + WORD_H + 26
VENUE_Y = TITLE_Y + 56
NOTE_Y = 800

def marks(invert=False):
    star = (f'<div class="mark seal" style="left:{CX-STAR_D/2:.0f}px;top:{STAR_CY-STAR_D/2:.0f}px;'
            f'width:{STAR_D}px;height:{STAR_D}px;'
            f'-webkit-mask-image:url({v.STAR_URI});mask-image:url({v.STAR_URI})"></div>')
    word_cls = "wordmarkInv" if invert else "mark wordmark"
    word = (f'<div class="{word_cls}" style="left:{CX-WORD_W/2:.0f}px;top:{WORD_Y}px;'
            f'width:{WORD_W}px;height:{WORD_H}px;'
            f'-webkit-mask-image:url({v.WORD_URI});mask-image:url({v.WORD_URI})"></div>')
    return star + word

def minaret_group(cx, base_y, pal, dark="#0B0805"):
    """A stylised Moroccan minaret — Koutoubia-esque: a tapered square shaft,
       a lantern stage and a jamour finial of stacked balls — as a solid
       gold silhouette, with the windows punched through as dark recesses
       rather than drawn as hairline outline. Bilaterally symmetric."""
    fill = "url(#towerGrad)"
    edge = pal["hair4"]
    g = [f'<rect x="-58" y="-26" width="116" height="26" fill="{fill}" stroke="{edge}" stroke-width="0.6"/>',
         f'<path d="M -52,-26 L -33,-560 L 33,-560 L 52,-26 Z" fill="{fill}" stroke="{edge}" stroke-width="0.6"/>',
         f'<rect x="-42" y="-580" width="84" height="20" fill="{fill}" stroke="{edge}" stroke-width="0.6"/>',
         f'<rect x="-24" y="-680" width="48" height="100" fill="{fill}" stroke="{edge}" stroke-width="0.6"/>',
         f'<rect x="-30" y="-692" width="60" height="12" fill="{fill}" stroke="{edge}" stroke-width="0.6"/>',
         f'<path d="M -22,-692 Q 0,-736 22,-692 Z" fill="{fill}" stroke="{edge}" stroke-width="0.6"/>',
         f'<line x1="0" y1="-736" x2="0" y2="-760" stroke="{pal["hair2"]}" stroke-width="2.2"/>',
         f'<circle cx="0" cy="-744" r="4.2" fill="{pal["hair1"]}"/>',
         f'<circle cx="0" cy="-754" r="2.8" fill="{pal["hair1"]}"/>',
         f'<path d="M -10,-590 L -10,-610 Q -10,-628 0,-628 Q 10,-628 10,-610 L 10,-590 Z" fill="{dark}"/>']
    for yc in (-150, -330, -480):
        ww, wh = 15, 32
        g.append(f'<path d="M {-ww/2},{yc+wh/2} L {-ww/2},{yc} Q {-ww/2},{yc-wh/2} 0,{yc-wh/2} '
                 f'Q {ww/2},{yc-wh/2} {ww/2},{yc} L {ww/2},{yc+wh/2} Z" fill="{dark}"/>')
    return f'<g class="tower" transform="translate({cx},{base_y})">' + "\n".join(g) + '</g>'

def tower_grad(pal):
    return (f'<linearGradient id="towerGrad" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0%" stop-color="{pal["hair1"]}"/>'
            f'<stop offset="45%" stop-color="{pal["hair2"]}"/>'
            f'<stop offset="100%" stop-color="{pal["hair4"]}"/>'
            f'</linearGradient>')

def moon_group(cx, cy, pal, r=40):
    """A solid, glowing crescent — a filled disc with a second circle
       subtracted through an SVG mask, not just an outline."""
    ox, oy = r*0.58, -r*0.12
    return f'''
  <defs>
    <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%"   stop-color="{pal['halo0']}" stop-opacity="0.55"/>
      <stop offset="35%"  stop-color="{pal['halo1']}" stop-opacity="0.30"/>
      <stop offset="70%"  stop-color="{pal['halo2']}" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="{pal['halo2']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="moonBody" cx="32%" cy="34%" r="75%">
      <stop offset="0%"   stop-color="#FFFBF0"/>
      <stop offset="45%"  stop-color="{pal['fill_lit']}"/>
      <stop offset="100%" stop-color="{pal['halo3']}"/>
    </radialGradient>
    <mask id="crescentMask">
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>
      <circle cx="{cx+ox:.1f}" cy="{cy+oy:.1f}" r="{r*0.86:.1f}" fill="#000"/>
    </mask>
  </defs>
  <circle cx="{cx}" cy="{cy}" r="{r*3.6:.0f}" fill="url(#moonGlow)"/>
  <g mask="url(#crescentMask)">
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#moonBody)"/>
  </g>'''

NICHE_EDGE  = "#8C6B2E"   # deep antique gold — the niche's own ornament, once it's light-filled
NICHE_TITLE = "linear-gradient(180deg,#96742F 0%,#6E5424 55%,#4C3A1B 100%)"
NICHE_WORD  = "linear-gradient(180deg,#96742F 0%,#6E5424 60%,#4C3A1B 100%)"
NICHE_VENUE = "#7A5B26"
NICHE_ADDR  = "#2E2013"
NICHE_NOTE  = "#4A3A24"
STAR_DISC   = "#050505"   # the plate that keeps the star on its own dark ground

def panel_texture(pal, edge):
    """A faint geometric weave inside the solid niche — felt more than seen,
       the same way the poster's own ground carries texture under its text.
       The pattern's own class carries no colour (fill:none only, in css()),
       so `edge` reaches it purely by inheriting the wrapper's stroke —
       one code path serves both the dark niche and the inverted light one."""
    lattice = pal.get("pattern") == "lattice"
    pat = f.lattice_layer(46, "nicheTex", 0.55) if lattice else v.zellij_layer(46, "nicheTex", 0.65, studs=False)
    pid = "lat46" if lattice else "zj46"
    return (f'<defs><clipPath id="panelClip"><path d="{arch_panel_d(824)}"/></clipPath>{pat}</defs>'
            f'<g clip-path="url(#panelClip)" style="stroke:{edge}">'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{pid})" opacity="0.20"/>'
            f'</g>')

def dado_band(pal):
    """A tiled border, the way the poster's own frame carries a dado —
       far more Islamic detail at the edge than a bare hairline."""
    lattice = pal.get("pattern") == "lattice"
    pat = f.lattice_layer(34, "zb", 0.65) if lattice else v.zellij_layer(34, "zb", 0.7, studs=False)
    band_id = "lat34" if lattice else "zj34"
    return f'''
  <defs>{pat}</defs>
  <path fill-rule="evenodd" fill="url(#{band_id})" style="opacity:{pal.get('band_op', 0.30)}"
        d="M30,30 H{W-30} V{H-30} H30 Z M62,62 H{W-62} V{H-62} H62 Z"/>'''

def frame_svg(pal, minarets=False, moon=False, rule_y=None, invert=False, niche_fill=None):
    rule_y = rule_y if rule_y is not None else VENUE_Y+40
    towers = (f'<defs>{tower_grad(pal)}</defs>' +
              minaret_group(150, H-60, pal) + minaret_group(W-150, H-60, pal)) if minarets else ""
    moon_svg = moon_group(300, 168, pal) if moon else ""
    niche_paint = f'fill="{niche_fill}"' if invert else f'fill="rgba({pal["scrim"]},0.94)"'
    edge = NICHE_EDGE if invert else pal['hair4']
    star_disc = f'<circle cx="{CX}" cy="{STAR_CY}" r="{STAR_R+26}" fill="{STAR_DISC}"/>' if invert else ""
    return f'''
<svg class="layer" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <radialGradient id="halo" cx="50%" cy="{STAR_CY/H*100:.1f}%" r="50%">
      <stop offset="0%"   stop-color="{pal['halo0']}" stop-opacity="{0.24*pal.get('halo_mult',1.0):.3f}"/>
      <stop offset="30%"  stop-color="{pal['halo1']}" stop-opacity="{0.12*pal.get('halo_mult',1.0):.3f}"/>
      <stop offset="55%"  stop-color="{pal['halo2']}" stop-opacity="{0.05*pal.get('halo_mult',1.0):.3f}"/>
      <stop offset="100%" stop-color="{pal['halo2']}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#halo)"/>

  <g class="ground">{v.ground_rosette(CX, H*0.52, 520)}</g>

  <path d="{arch_panel_d(824)}" {niche_paint}/>
  {panel_texture(pal, edge)}

  {towers}
  {moon_svg}

  <path d="{barch_d(0)}" fill="none" class="hair-4" stroke-width="1.3"/>
  <path d="{barch_d(11)}" fill="none" class="hair-5" stroke-width="0.6"/>
  <path d="{arch_panel_d(824)}" fill="none" stroke="{edge}" stroke-width="1"/>
  <path d="{arch_panel_d(808, inset=16)}" fill="none" stroke="{edge}" stroke-width="0.7" opacity="0.8"/>

  {star_disc}
  <g class="med">{v.halo(CX, STAR_CY, STAR_R)}</g>

  {v.rule(CX, rule_y, 200)}

  {dado_band(pal)}
  <rect x="30" y="30" width="{W-60}" height="{H-60}" class="hair-3" stroke-width="1.1" fill="none"/>
  <rect x="37" y="37" width="{W-74}" height="{H-74}" class="hair-5" stroke-width="0.6" fill="none"/>
  <rect x="62" y="62" width="{W-124}" height="{H-124}" class="hair-3" stroke-width="0.9" fill="none"/>
  <rect x="69" y="69" width="{W-138}" height="{H-138}" class="hair-5" stroke-width="0.5" fill="none"/>
  {v.corner(62,62,1,1,0.5)}{v.corner(W-62,62,-1,1,0.5)}{v.corner(62,H-62,1,-1,0.5)}{v.corner(W-62,H-62,-1,-1,0.5)}
</svg>
<div class="grain"></div>
'''

def tiles_svg(pal):
    lattice = pal.get("pattern") == "lattice"
    if lattice:
        big, small = f.lattice_layer(82, "zh", 0.7), f.lattice_layer(20, "zf", 0.45)
        big_id, small_id = "lat82", "lat20"
    else:
        big, small = v.zellij_layer(64, "zh", 0.9), v.zellij_layer(16, "zf", 0.55, studs=False)
        big_id, small_id = "zj64", "zj16"
    return f'''
<svg class="layer" style="opacity:{min(pal['tile_big_op']*1.6, 0.36)}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>{big}{small}</defs>
  <rect width="{W}" height="{H}" fill="url(#{small_id})" opacity="{min(pal['tile_small_op']*1.3, 0.32)}"/>
  <rect width="{W}" height="{H}" fill="url(#{big_id})"/>
</svg>
<div class="scrim"></div>
'''

def css(pal):
    return f'''
{v.FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#000}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
  background:{pal['bg1']},{pal['bg2']};
  font-kerning:normal;-webkit-font-smoothing:antialiased;}}
.layer{{position:absolute;inset:0;width:100%;height:100%}}
.grain{{position:absolute;inset:0;opacity:.05;mix-blend-mode:overlay;pointer-events:none;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4'/><feColorMatrix type='saturate' values='0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>");}}
.scrim{{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient({pal.get('scrim_reach','60% 68%')} at 50% 46%, rgba({pal['scrim']},.92) 0%, rgba({pal['scrim']},.78) 30%, rgba({pal['scrim']},.42) 56%, rgba({pal['scrim']},0) 82%);}}

.hair-1{{fill:none;stroke:{pal['hair1']};opacity:.97}}
.hair-2{{fill:none;stroke:{pal['hair2']};opacity:.85}}
.hair-3{{fill:none;stroke:{pal['hair3']};opacity:.80}}
.hair-4{{fill:none;stroke:{pal['hair4']};opacity:.75}}
.hair-5{{fill:none;stroke:{pal['hair5']};opacity:.6}}
.fill-lit{{fill:{pal['fill_lit']}}}
.rule{{stroke:{pal['rule']};stroke-width:1;opacity:.85}}
.rule-lit{{stroke:{pal['rule_lit']};stroke-width:1;opacity:.9}}
.zh{{stroke:{pal['zh']}}}
.zf{{stroke:{pal['zf']}}}
.zb{{stroke:{pal['zb']}}}
.gh{{fill:none;stroke:{pal['hair5']}}}
.nicheTex{{fill:none}}
.ground{{opacity:.10}}
.med{{filter:drop-shadow(0 0 18px rgba(230,192,116,.28))}}
.tower{{filter:drop-shadow(0 0 9px rgba(230,192,116,.40))}}

.mark{{position:absolute;
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
  -webkit-mask-size:contain;mask-size:contain;
  -webkit-mask-position:center;mask-position:center;
  background-image:{pal['mark_grad']};}}
.seal{{filter:drop-shadow(0 0 18px rgba(232,194,116,.30)) drop-shadow(0 1px 1px rgba(0,0,0,.5))}}
.wordmark{{filter:drop-shadow(0 0 12px rgba(226,186,108,.24)) drop-shadow(0 1px 1px rgba(0,0,0,.5))}}

.at{{position:absolute;left:0;right:0;text-align:center;
  text-shadow:0 1px 3px rgba(0,0,0,.75), 0 0 12px rgba(0,0,0,.5)}}
.gold{{background:{pal['gold_grad']};
  -webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 1px 0 rgba(0,0,0,.6)) drop-shadow(0 2px 4px rgba(0,0,0,.7))
         drop-shadow(0 0 16px rgba(214,172,100,.24))}}
.at.gold{{text-shadow:none}}
.goldInv{{background:{NICHE_TITLE};-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 1px 1px rgba(0,0,0,.16))}}
.at.goldInv{{text-shadow:none}}
.wordmarkInv{{position:absolute;
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
  -webkit-mask-size:contain;mask-size:contain;
  -webkit-mask-position:center;mask-position:center;
  background-image:{NICHE_WORD};filter:drop-shadow(0 1px 1px rgba(0,0,0,.16))}}

.t1{{font-family:Cinzel,serif;font-weight:600;font-size:40px;letter-spacing:.115em;
  text-indent:.115em;line-height:1.24}}
.venue{{font-family:Cinzel,serif;font-weight:400;font-size:19px;letter-spacing:.32em;
  text-indent:.32em;color:{pal['lab']}}}
.venueInv{{font-family:Cinzel,serif;font-weight:400;font-size:19px;letter-spacing:.32em;
  text-indent:.32em;color:{NICHE_VENUE};text-shadow:none}}
.addr{{font-family:Cormorant,serif;font-weight:700;font-size:24px;letter-spacing:.07em;
  text-indent:.07em;color:{pal['addr']};text-transform:uppercase}}
.addrInv{{font-family:Cormorant,serif;font-weight:700;font-size:24px;letter-spacing:.07em;
  text-indent:.07em;color:{NICHE_ADDR};text-transform:uppercase;text-shadow:none}}
.vsub{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:19px;
  letter-spacing:.03em;color:{pal['vsub']}}}
.note{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:15px;
  letter-spacing:.03em;color:{pal['note']}}}
.noteInv{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:15px;
  letter-spacing:.03em;color:{NICHE_NOTE};text-shadow:none}}
'''

def page(pal, full_address=False, minarets=False, moon=False, note=True, invert=False, niche_fill=None):
    venue_text = "CRESCENT HALL" if full_address else "CRESCENT HALL &nbsp;·&nbsp; ROCHDALE"
    addr_cls = "addrInv" if invert else "addr"
    venue_cls = "venueInv" if invert else "venue"
    note_cls = "noteInv" if invert else "note"
    gold_cls = "goldInv" if invert else "gold"
    addr_line = ('<div class="at %s" style="top:%dpx">162 Edmund Street &nbsp;·&nbsp; Rochdale OL12 6QG</div>'
                 % (addr_cls, VENUE_Y+34)) if full_address else ""
    rule_y = VENUE_Y + (76 if full_address else 40)
    note_line = ('<div class="at %s" style="top:%dpx">A brothers-only gathering &nbsp;·&nbsp; www.thesufiway.co.uk</div>'
                 % (note_cls, NOTE_Y)) if note else ('<div class="at %s" style="top:%dpx">www.thesufiway.co.uk</div>' % (note_cls, NOTE_Y))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Tariqa Al Qadiriya Al Boutchichiya</title>
<style>{css(pal)}</style></head>
<body><div class="page">
{tiles_svg(pal)}
{frame_svg(pal, minarets=minarets, moon=moon, rule_y=rule_y, invert=invert, niche_fill=niche_fill)}
{marks(invert=invert)}
<div class="at t1 {gold_cls}" style="top:{TITLE_Y}px">TARIQA AL QADIRIYA AL BOUTCHICHIYA</div>
<div class="at {venue_cls}" style="top:{VENUE_Y}px">{venue_text}</div>
{addr_line}
{note_line}
</div></body></html>'''

PALETTES = {
    "gold":      f.DEFAULT_PALETTE,
    "emerald":   f.EMERALD,
    "burgundy":  f.BURGUNDY,
    "indigo":    f.INDIGO,
    "blackgold": f.BLACKGOLD,
    "earthy":    f.EARTHY,
}

# ---------- light grounds ----------
# The niche stays exactly as dark and gold as Black & Gold — every reading
# token (gold_grad, mark_grad, ayah..url) carries over untouched, since that
# text sits inside the still-dark panel. Only two things change: the outer
# ground goes pale, and the ornament that has to read against it (hairlines,
# the pattern, the minarets' own fill) drops to a deeper antique bronze so it
# doesn't wash out on cream/blush/sage/powder. The soft scrim, which used to
# bleed dark across most of the canvas, is pulled in tight to the niche —
# on a light ground that bleed would read as a dirty smudge, not a vignette.
_DEEP_GOLD = dict(
    hair1="#8C6B2E", hair2="#75592A", hair3="#5F4922", hair4="#4C3A1B", hair5="#3C2E15",
    zh="#75592A", zf="#5F4922", zb="#6E5424",
    fill_lit="#B8934A", rule="#6E5424", rule_lit="#9A7A3C",
    petal="rgba(117,89,42,.10)", petal_stroke="#6E5424",
    petal_lit="rgba(140,107,46,.16)", petal_lit_stroke="#8C6B2E",
    stroke_node="#5F4922", dot="#8C6B2E",
    scrim_reach="34% 40%", halo_mult=0.18,
)

IVORY = dict(f.BLACKGOLD); IVORY.update(_DEEP_GOLD)
IVORY.update(
    name="Ivory & Gold",
    bg1="radial-gradient(115% 65% at 50% 26%, #FAF4E6 0%, #F0E6D2 40%, #E4D6B8 70%, #D8C79E 100%)",
    bg2="radial-gradient(90% 45% at 50% 96%, #ECDFC4 0%, #E0D0AE 50%, #D2BF94 100%)",
    print_bg="#F0E6D2",
)

BLUSH = dict(f.BLACKGOLD); BLUSH.update(_DEEP_GOLD)
BLUSH.update(
    name="Blush & Gold",
    bg1="radial-gradient(115% 65% at 50% 26%, #F7E9E4 0%, #EFD9D1 40%, #E3C2B6 70%, #D6AC9C 100%)",
    bg2="radial-gradient(90% 45% at 50% 96%, #E9D2C8 0%, #DDBBAC 50%, #CFA290 100%)",
    print_bg="#EFD9D1",
)

SAGE = dict(f.BLACKGOLD); SAGE.update(_DEEP_GOLD)
SAGE.update(
    name="Sage & Gold",
    bg1="radial-gradient(115% 65% at 50% 26%, #EEF0E2 0%, #E1E5CE 40%, #CFD6B2 70%, #BCC796 100%)",
    bg2="radial-gradient(90% 45% at 50% 96%, #D9DFC2 0%, #C7D0A6 50%, #B4C08C 100%)",
    print_bg="#E1E5CE",
)

POWDER = dict(f.BLACKGOLD); POWDER.update(_DEEP_GOLD)
POWDER.update(
    name="Powder & Gold",
    bg1="radial-gradient(115% 65% at 50% 26%, #E9F0F3 0%, #D8E5EA 40%, #BFD5DE 70%, #A6C3D0 100%)",
    bg2="radial-gradient(90% 45% at 50% 96%, #CFE0E6 0%, #B8D0D8 50%, #9FBCC6 100%)",
    print_bg="#D8E5EA",
)

LIGHT_PALETTES = {"ivory": IVORY, "blush": BLUSH, "sage": SAGE, "powder": POWDER}

# ---------- inverted: dark outer, colourful niche ----------
# The reverse of the light grounds above — the outer field (frame, minarets,
# moon, pattern) stays exactly Black & Gold, dark as originally designed;
# only the niche panel itself takes a pastel fill. The star keeps its own
# small dark disc (STAR_DISC) behind the halo ring so it still reads as a
# gold mark on black even though the panel around it has gone light, and
# every reading token inside the niche switches to the deep-gold/espresso
# *Inv colours (NICHE_TITLE/NICHE_WORD/NICHE_VENUE/NICHE_ADDR/NICHE_NOTE)
# tuned for legibility on a pale ground rather than a dark one.
NICHE_FILLS = {
    "ivory":  "#F2E9D8",
    "blush":  "#F0DCD3",
    "sage":   "#E4E8D2",
    "powder": "#DCEAEF",
}

if __name__ == "__main__":
    for key, pal in PALETTES.items():
        opts = dict(full_address=True, minarets=True, moon=True, note=False) if key == "blackgold" else {}
        html = page(pal, **opts)
        p = HERE / f"banner-{key}.html"
        p.write_text(html, encoding="utf-8")
        shot(p, HERE / f"banner-{key}.png", W, H, scale=2)

    for key, pal in LIGHT_PALETTES.items():
        html = page(pal, full_address=True, minarets=True, moon=True, note=False)
        p = HERE / f"banner-{key}.html"
        p.write_text(html, encoding="utf-8")
        shot(p, HERE / f"banner-{key}.png", W, H, scale=2)

    for key, fill in NICHE_FILLS.items():
        html = page(f.BLACKGOLD, full_address=True, minarets=True, moon=True, note=False,
                     invert=True, niche_fill=fill)
        p = HERE / f"banner-invert-{key}.html"
        p.write_text(html, encoding="utf-8")
        shot(p, HERE / f"banner-invert-{key}.png", W, H, scale=2)
