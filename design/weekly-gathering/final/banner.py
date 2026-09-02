#!/usr/bin/env python3
"""A landscape banner (1600x900), redone as one centred composition under a
   flattened echo of the poster's own mihrab arch — not a poster cut down."""
import subprocess, pathlib
from PIL import Image
import variants as v
from final import BLACKGOLD as PAL

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

def lozenge(cx, cy, w=5.5, h=8.5, cls="fill-lit"):
    return v.lozenge(cx, cy, w, h, cls)

def css_diamond(cx, cy, size=8):
    """A lozenge divider as a plain rotated div — v.lozenge emits a bare SVG
       <path>, which HTML silently drops outside an <svg> wrapper."""
    return (f'<div style="position:absolute;left:{cx-size/2:.0f}px;top:{cy-size/2:.0f}px;'
            f'width:{size}px;height:{size}px;background:{PAL["fill_lit"]};'
            f'transform:rotate(45deg);box-shadow:0 0 6px rgba(217,185,120,.45)"></div>')

# ---------- a flattened echo of the poster's mihrab arch ----------
BL, BR, B_BASE, B_APEX, B_SH = 300, 1300, 600, 46, 300
def barch_d(inset=0.0):
    l, r = BL+inset, BR-inset
    b, a = B_BASE, B_APEX+inset*0.9
    sh = B_SH+inset*0.35
    return (f'M {l},{b} L {l},{sh} Q {l},{a+150} {CX},{a} '
            f'Q {r},{a+150} {r},{sh} L {r},{b}')

STAR_CY, STAR_R, STAR_D = 232, 120, 200
STAR_MARK = (f'<div class="mark seal" style="left:{CX-STAR_D/2:.0f}px;top:{STAR_CY-STAR_D/2:.0f}px;'
             f'width:{STAR_D}px;height:{STAR_D}px;'
             f'-webkit-mask-image:url({v.STAR_URI});mask-image:url({v.STAR_URI})"></div>')

WORD_W, WORD_H = 380, 67
WORD_Y = 358
WORDMARK = (f'<div class="mark wordmark" style="left:{CX-WORD_W/2:.0f}px;top:{WORD_Y}px;'
            f'width:{WORD_W}px;height:{WORD_H}px;'
            f'-webkit-mask-image:url({v.WORD_URI});mask-image:url({v.WORD_URI})"></div>')

def frame_svg():
    return f'''
<svg class="layer" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <radialGradient id="halo" cx="50%" cy="{STAR_CY/H*100:.1f}%" r="46%">
      <stop offset="0%"   stop-color="{PAL['halo0']}" stop-opacity="0.22"/>
      <stop offset="30%"  stop-color="{PAL['halo1']}" stop-opacity="0.11"/>
      <stop offset="55%"  stop-color="{PAL['halo2']}" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#halo)"/>

  <path d="{barch_d(0)}" fill="none" class="hair-5" stroke-width="1.1"/>
  <path d="{barch_d(10)}" fill="none" class="hair-5" stroke-width="0.6"/>

  <g class="med">{v.halo(CX, STAR_CY, STAR_R)}</g>

  {v.rule(CX, 566, 240)}

  <!-- outer frame -->
  <rect x="26" y="26" width="{W-52}" height="{H-52}" class="hair-3" stroke-width="1.1" fill="none"/>
  <rect x="33" y="33" width="{W-66}" height="{H-66}" class="hair-5" stroke-width="0.6" fill="none"/>
  {v.corner(52,52,1,1,0.5)}{v.corner(W-52,52,-1,1,0.5)}{v.corner(52,H-52,1,-1,0.5)}{v.corner(W-52,H-52,-1,-1,0.5)}
</svg>
<div class="grain"></div>
'''

def tiles_svg():
    big = v.zellij_layer(78, "zh", 0.85)
    small = v.zellij_layer(20, "zf", 0.5, studs=False)
    return f'''
<svg class="layer" style="opacity:{PAL['tile_big_op']}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>{big}{small}</defs>
  <rect width="{W}" height="{H}" fill="url(#zj20)" opacity="{PAL['tile_small_op']}"/>
  <rect width="{W}" height="{H}" fill="url(#zj78)"/>
</svg>
<div class="scrim"></div>
'''

def css():
    return f'''
{v.FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#000}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
  background:
    radial-gradient(80% 90% at 50% 30%, #262626 0%, #171717 34%, #0C0C0C 64%, #050505 100%),
    radial-gradient(90% 60% at 50% 100%, #161616 0%, #0A0A0A 50%, #040404 100%);
  font-kerning:normal;-webkit-font-smoothing:antialiased;}}
.layer{{position:absolute;inset:0;width:100%;height:100%}}
.grain{{position:absolute;inset:0;opacity:.05;mix-blend-mode:overlay;pointer-events:none;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4'/><feColorMatrix type='saturate' values='0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>");}}
.scrim{{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(56% 64% at 50% 46%, rgba(4,4,4,.34) 0%, rgba(4,4,4,0) 72%);}}

.hair-1{{fill:none;stroke:{PAL['hair1']};opacity:.97}}
.hair-2{{fill:none;stroke:{PAL['hair2']};opacity:.85}}
.hair-3{{fill:none;stroke:{PAL['hair3']};opacity:.80}}
.hair-4{{fill:none;stroke:{PAL['hair4']};opacity:.75}}
.hair-5{{fill:none;stroke:{PAL['hair5']};opacity:.6}}
.fill-lit{{fill:{PAL['fill_lit']}}}
.rule{{stroke:{PAL['rule']};stroke-width:1;opacity:.85}}
.rule-lit{{stroke:{PAL['rule_lit']};stroke-width:1;opacity:.9}}
.zh{{stroke:{PAL['zh']}}}
.zf{{stroke:{PAL['zf']}}}
.med{{filter:drop-shadow(0 0 16px rgba(230,192,116,.26))}}

.mark{{position:absolute;
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
  -webkit-mask-size:contain;mask-size:contain;
  -webkit-mask-position:center;mask-position:center;
  background-image:{PAL['mark_grad']};}}
.seal{{filter:drop-shadow(0 0 18px rgba(232,194,116,.30)) drop-shadow(0 1px 1px rgba(0,0,0,.5))}}
.wordmark{{filter:drop-shadow(0 0 12px rgba(226,186,108,.24)) drop-shadow(0 1px 1px rgba(0,0,0,.5))}}

.at{{position:absolute;left:0;right:0;text-align:center;
  text-shadow:0 1px 3px rgba(0,0,0,.75), 0 0 12px rgba(0,0,0,.5)}}
.gold{{background:{PAL['gold_grad']};
  -webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 1px 0 rgba(0,0,0,.6)) drop-shadow(0 2px 4px rgba(0,0,0,.7))
         drop-shadow(0 0 16px rgba(214,172,100,.24))}}
.at.gold{{text-shadow:none}}

.t1{{font-family:Cinzel,serif;font-weight:600;font-size:38px;letter-spacing:.11em;
  text-indent:.11em;line-height:1.24}}
.t2{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:25px;
  letter-spacing:.03em;color:{PAL['t2']}}}
.info{{font-family:Cormorant,serif;font-weight:400;font-size:23px;letter-spacing:.04em;
  color:{PAL['val']}}}
.info b{{font-weight:600;color:{PAL['wa']}}}
.rn{{font-family:Cinzel,serif;font-weight:400;font-size:12.5px;letter-spacing:.42em;
  text-indent:.42em;color:{PAL['lab']}}}
.note{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:15px;
  letter-spacing:.03em;color:{PAL['note']}}}
'''

INFO_Y = 616
def info_row():
    """One centred line, gold diamonds standing where a caption would break the flow."""
    parts = ["29 August 2026", "7:00 – 9:00 pm", "Crescent Hall, Rochdale", "WhatsApp 07884 053544"]
    seg_w = 1100/len(parts)
    x0 = CX - 1100/2
    spans = []
    for i, txt in enumerate(parts):
        cxp = x0 + seg_w*(i+0.5)
        spans.append(f'<div class="at info" style="top:0;left:{cxp-seg_w/2:.0f}px;width:{seg_w:.0f}px">{txt}</div>')
        if i < len(parts)-1:
            spans.append(css_diamond(x0+seg_w*(i+1), 15))
    return f'<div style="position:absolute;left:0;top:{INFO_Y}px;width:{W}px;height:32px">' + "".join(spans) + '</div>'

def page():
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Weekly Dhikr Gathering — Banner</title>
<style>{css()}</style></head>
<body><div class="page">
{tiles_svg()}
{frame_svg()}
{STAR_MARK}
{WORDMARK}
<div class="at t1 gold" style="top:{WORD_Y+WORD_H+20}px">TARIQA AL QADIRIYA AL BOUTCHICHIYA</div>
<div class="at t2" style="top:{WORD_Y+WORD_H+70}px">Weekly Dhikr Gathering</div>
{info_row()}
<div class="at note" style="top:{INFO_Y+52}px">A brothers-only gathering &nbsp;·&nbsp; www.thesufiway.co.uk</div>
</div></body></html>'''

if __name__ == "__main__":
    html = page()
    p = HERE / "banner.html"
    p.write_text(html, encoding="utf-8")
    shot(p, HERE / "banner.png", W, H, scale=2)
