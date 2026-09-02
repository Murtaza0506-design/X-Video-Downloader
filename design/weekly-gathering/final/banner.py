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

STAR_CY, STAR_R, STAR_D = 250, 138, 230
WORD_W, WORD_H = 420, 74
WORD_Y = 408
TITLE_Y = WORD_Y + WORD_H + 26
VENUE_Y = TITLE_Y + 56
NOTE_Y = 800

def marks():
    star = (f'<div class="mark seal" style="left:{CX-STAR_D/2:.0f}px;top:{STAR_CY-STAR_D/2:.0f}px;'
            f'width:{STAR_D}px;height:{STAR_D}px;'
            f'-webkit-mask-image:url({v.STAR_URI});mask-image:url({v.STAR_URI})"></div>')
    word = (f'<div class="mark wordmark" style="left:{CX-WORD_W/2:.0f}px;top:{WORD_Y}px;'
            f'width:{WORD_W}px;height:{WORD_H}px;'
            f'-webkit-mask-image:url({v.WORD_URI});mask-image:url({v.WORD_URI})"></div>')
    return star + word

def minaret_group(cx, base_y, cls="hair-3"):
    """A stylised Moroccan minaret — Koutoubia-esque: a tapered square shaft,
       blind pointed-arch windows, a lantern stage, and a jamour finial of
       stacked balls. Bilaterally symmetric, so no mirroring is needed."""
    g = ['<rect x="-58" y="-26" width="116" height="26" class="%s" stroke-width="0.9"/>' % cls,
         '<path d="M -52,-26 L -33,-560 L 33,-560 L 52,-26 Z" class="%s" stroke-width="0.9"/>' % cls,
         '<rect x="-42" y="-580" width="84" height="20" class="%s" stroke-width="0.9"/>' % cls,
         '<rect x="-24" y="-680" width="48" height="100" class="%s" stroke-width="0.85"/>' % cls,
         '<path d="M -10,-590 L -10,-610 Q -10,-628 0,-628 Q 10,-628 10,-610 L 10,-590" class="%s" stroke-width="0.65"/>' % cls,
         '<rect x="-30" y="-692" width="60" height="12" class="%s" stroke-width="0.85"/>' % cls,
         '<path d="M -22,-692 Q 0,-736 22,-692 Z" class="%s" stroke-width="0.85"/>' % cls,
         '<line x1="0" y1="-736" x2="0" y2="-760" class="%s" stroke-width="0.8"/>' % cls,
         '<circle cx="0" cy="-744" r="4" class="%s" stroke-width="0.7"/>' % cls,
         '<circle cx="0" cy="-754" r="2.6" class="%s" stroke-width="0.6"/>' % cls]
    for yc in (-150, -330, -480):
        ww, wh = 15, 32
        g.append(f'<path d="M {-ww/2},{yc+wh/2} L {-ww/2},{yc} Q {-ww/2},{yc-wh/2} 0,{yc-wh/2} '
                 f'Q {ww/2},{yc-wh/2} {ww/2},{yc} L {ww/2},{yc+wh/2}" class="{cls}" stroke-width="0.65"/>')
    return f'<g transform="translate({cx},{base_y})" fill="none">' + "\n".join(g) + '</g>'

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

def frame_svg(pal, minarets=False, rule_y=None):
    rule_y = rule_y if rule_y is not None else VENUE_Y+40
    towers = (minaret_group(150, H-60) + minaret_group(W-150, H-60)) if minarets else ""
    return f'''
<svg class="layer" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <radialGradient id="halo" cx="50%" cy="{STAR_CY/H*100:.1f}%" r="50%">
      <stop offset="0%"   stop-color="{pal['halo0']}" stop-opacity="0.24"/>
      <stop offset="30%"  stop-color="{pal['halo1']}" stop-opacity="0.12"/>
      <stop offset="55%"  stop-color="{pal['halo2']}" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#halo)"/>

  <g class="ground">{v.ground_rosette(CX, H*0.52, 520)}</g>

  {towers}

  <path d="{barch_d(0)}" fill="none" class="hair-5" stroke-width="1.1"/>
  <path d="{barch_d(11)}" fill="none" class="hair-5" stroke-width="0.6"/>

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
  background:radial-gradient(56% 64% at 50% 46%, rgba({pal['scrim']},.30) 0%, rgba({pal['scrim']},0) 72%);}}

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
.ground{{opacity:.10}}
.med{{filter:drop-shadow(0 0 18px rgba(230,192,116,.28))}}

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

.t1{{font-family:Cinzel,serif;font-weight:600;font-size:40px;letter-spacing:.115em;
  text-indent:.115em;line-height:1.24}}
.venue{{font-family:Cinzel,serif;font-weight:400;font-size:19px;letter-spacing:.32em;
  text-indent:.32em;color:{pal['lab']}}}
.addr{{font-family:Cormorant,serif;font-weight:400;font-size:17px;letter-spacing:.1em;
  text-indent:.1em;color:{pal['addr']};text-transform:uppercase}}
.vsub{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:19px;
  letter-spacing:.03em;color:{pal['vsub']}}}
.note{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:15px;
  letter-spacing:.03em;color:{pal['note']}}}
'''

def page(pal, full_address=False, minarets=False, note=True):
    venue_text = "CRESCENT HALL" if full_address else "CRESCENT HALL &nbsp;·&nbsp; ROCHDALE"
    addr_line = ('<div class="at addr" style="top:%dpx">162 Edmund Street &nbsp;·&nbsp; Rochdale OL12 6QG</div>'
                 % (VENUE_Y+34)) if full_address else ""
    rule_y = VENUE_Y + (76 if full_address else 40)
    note_line = ('<div class="at note" style="top:%dpx">A brothers-only gathering &nbsp;·&nbsp; www.thesufiway.co.uk</div>'
                 % NOTE_Y) if note else ('<div class="at note" style="top:%dpx">www.thesufiway.co.uk</div>' % NOTE_Y)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Tariqa Al Qadiriya Al Boutchichiya</title>
<style>{css(pal)}</style></head>
<body><div class="page">
{tiles_svg(pal)}
{frame_svg(pal, minarets=minarets, rule_y=rule_y)}
{marks()}
<div class="at t1 gold" style="top:{TITLE_Y}px">TARIQA AL QADIRIYA AL BOUTCHICHIYA</div>
<div class="at venue" style="top:{VENUE_Y}px">{venue_text}</div>
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

if __name__ == "__main__":
    for key, pal in PALETTES.items():
        opts = dict(full_address=True, minarets=True, note=False) if key == "blackgold" else {}
        html = page(pal, **opts)
        p = HERE / f"banner-{key}.html"
        p.write_text(html, encoding="utf-8")
        shot(p, HERE / f"banner-{key}.png", W, H, scale=2)
