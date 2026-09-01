#!/usr/bin/env python3
"""A landscape banner (1600x900) in the Black & Gold poster's own language —
   for a WhatsApp/Facebook cover, not the print poster itself."""
import subprocess, pathlib
from PIL import Image
import variants as v
from final import BLACKGOLD as PAL

HERE = v.HERE
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W, H = 1600, 900
CX, CY = W/2, H/2

def shot(html_path, out_png, w, h, scale=1):
    raw = out_png.with_name("_raw_" + out_png.stem + ".png")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                     f"--force-device-scale-factor={scale}", f"--window-size={w},{h+300}",
                     "--screenshot="+str(raw), "--virtual-time-budget=8000",
                     "file://"+str(html_path.resolve())], capture_output=True)
    im = Image.open(raw).convert("RGB").crop((0, 0, w*scale, h*scale))
    im.save(out_png, optimize=True); raw.unlink()
    print(out_png.name, im.size)

def zellij_layer(p_, cls, w_, studs=True):
    return v.zellij_layer(p_, cls, w_, studs=studs)

def lozenge(cx, cy, w=6, h=9.5, cls="fill-lit"):
    return v.lozenge(cx, cy, w, h, cls)

def hrule(cx, y, half, node=True):
    return v.rule(cx, y, half, node)

def vrule(x, y0, y1):
    return f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" class="rule"/>'

# ---------- star + halo, sized for the banner's own height ----------
STAR_CX, STAR_CY, STAR_R, STAR_D = 300, CY, 210, 350
def star_group():
    g = [f'<g class="med">{v.halo(STAR_CX, STAR_CY, STAR_R)}</g>']
    return "\n".join(g)

STAR_MARK = (f'<div class="mark seal" style="left:{STAR_CX-STAR_D/2:.0f}px;top:{STAR_CY-STAR_D/2:.0f}px;'
             f'width:{STAR_D}px;height:{STAR_D}px;'
             f'-webkit-mask-image:url({v.STAR_URI});mask-image:url({v.STAR_URI})"></div>')

WORD_W, WORD_H = 430, 76
WORD_X, WORD_Y = CX - WORD_W/2, 176
WORDMARK = (f'<div class="mark wordmark" style="left:{WORD_X:.0f}px;top:{WORD_Y}px;'
            f'width:{WORD_W}px;height:{WORD_H}px;'
            f'-webkit-mask-image:url({v.WORD_URI});mask-image:url({v.WORD_URI})"></div>')

DIV1_X = 520   # star | centre
DIV2_X = 1080  # centre | info

def frame_svg():
    return f'''
<svg class="layer" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <radialGradient id="halo" cx="{STAR_CX/W*100:.1f}%" cy="50%" r="46%">
      <stop offset="0%"   stop-color="{PAL['halo0']}" stop-opacity="0.20"/>
      <stop offset="30%"  stop-color="{PAL['halo1']}" stop-opacity="0.10"/>
      <stop offset="55%"  stop-color="{PAL['halo2']}" stop-opacity="0.045"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    {zellij_layer(30, "zb", 0.7, studs=False)}
  </defs>

  <rect width="{W}" height="{H}" fill="url(#halo)"/>

  {star_group()}

  <line x1="{DIV1_X}" y1="70" x2="{DIV1_X}" y2="{H-70}" class="rule"/>
  {lozenge(DIV1_X, H/2)}
  <line x1="{DIV2_X}" y1="70" x2="{DIV2_X}" y2="{H-70}" class="rule"/>
  {lozenge(DIV2_X, H/2)}

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
    radial-gradient(78% 92% at 20% 50%, #2A2A2A 0%, #1A1A1A 30%, #0D0D0D 58%, #050505 100%),
    radial-gradient(70% 90% at 82% 50%, #1D1D1D 0%, #0E0E0E 40%, #050505 100%);
  font-kerning:normal;-webkit-font-smoothing:antialiased;}}
.layer{{position:absolute;inset:0;width:100%;height:100%}}
.grain{{position:absolute;inset:0;opacity:.05;mix-blend-mode:overlay;pointer-events:none;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4'/><feColorMatrix type='saturate' values='0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>");}}
.scrim{{position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(60% 70% at 50% 50%, rgba(4,4,4,.30) 0%, rgba(4,4,4,0) 70%);}}

.hair-1{{fill:none;stroke:{PAL['hair1']};opacity:.97}}
.hair-2{{fill:none;stroke:{PAL['hair2']};opacity:.85}}
.hair-3{{fill:none;stroke:{PAL['hair3']};opacity:.80}}
.hair-4{{fill:none;stroke:{PAL['hair4']};opacity:.75}}
.hair-5{{fill:none;stroke:{PAL['hair5']};opacity:.55}}
.fill-lit{{fill:{PAL['fill_lit']}}}
.fill-ink{{fill:#0A0A0A}}
.rule{{stroke:{PAL['rule']};stroke-width:1;opacity:.85}}
.zh{{stroke:{PAL['zh']}}}
.zf{{stroke:{PAL['zf']}}}
.zb{{stroke:{PAL['zb']}}}
.med{{filter:drop-shadow(0 0 14px rgba(230,192,116,.24))}}

.mark{{position:absolute;
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
  -webkit-mask-size:contain;mask-size:contain;
  -webkit-mask-position:center;mask-position:center;
  background-image:{PAL['mark_grad']};}}
.seal{{filter:drop-shadow(0 0 16px rgba(232,194,116,.28)) drop-shadow(0 1px 1px rgba(0,0,0,.5))}}
.wordmark{{filter:drop-shadow(0 0 12px rgba(226,186,108,.22)) drop-shadow(0 1px 1px rgba(0,0,0,.5))}}

.at{{position:absolute;text-align:center;
  text-shadow:0 1px 3px rgba(0,0,0,.75), 0 0 12px rgba(0,0,0,.5)}}
.gold{{background:{PAL['gold_grad']};
  -webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 1px 0 rgba(0,0,0,.6)) drop-shadow(0 2px 4px rgba(0,0,0,.7))
         drop-shadow(0 0 16px rgba(214,172,100,.24))}}
.at.gold{{text-shadow:none}}

.t1{{font-family:Cinzel,serif;font-weight:600;font-size:34px;letter-spacing:.09em;
  text-indent:.09em;line-height:1.22}}
.t2{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:24px;
  letter-spacing:.03em;color:{PAL['t2']}}}
.lab{{font-family:Cinzel,serif;font-weight:400;font-size:12px;letter-spacing:.4em;
  text-indent:.4em;color:{PAL['lab']}}}
.val{{font-family:Cormorant,serif;font-weight:400;font-size:26px;letter-spacing:.04em;
  text-indent:.04em;color:{PAL['val']}}}
.venue{{font-family:Cinzel,serif;font-weight:600;font-size:26px;letter-spacing:.1em;
  text-indent:.1em}}
.vsub{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:18px;
  letter-spacing:.03em;color:{PAL['vsub']}}}
.wa{{font-family:Cormorant,serif;font-weight:400;font-size:24px;letter-spacing:.04em;
  text-indent:.04em;color:{PAL['wa']}}}
.note{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:15px;
  letter-spacing:.03em;color:{PAL['note']}}}
'''

def page():
    title = f'''
<div class="at t1 gold" style="left:{DIV1_X}px;width:{DIV2_X-DIV1_X}px;top:284px">TARIQA AL QADIRIYA</div>
<div class="at t1 gold" style="left:{DIV1_X}px;width:{DIV2_X-DIV1_X}px;top:326px">AL BOUTCHICHIYA</div>
<div class="at t2" style="left:{DIV1_X}px;width:{DIV2_X-DIV1_X}px;top:392px">Weekly Dhikr Gathering</div>
'''
    info_x, info_w = DIV2_X, W-70-DIV2_X
    info = f'''
<div class="at lab" style="left:{info_x}px;width:{info_w}px;top:196px">SATURDAY</div>
<div class="at val" style="left:{info_x}px;width:{info_w}px;top:222px">29 August 2026</div>
<div class="at lab" style="left:{info_x}px;width:{info_w}px;top:280px">EVENING</div>
<div class="at val" style="left:{info_x}px;width:{info_w}px;top:306px">7:00 – 9:00 pm</div>

{hrule((info_x+W-70)/2, 372, (info_w-40)/2, node=False)}

<div class="at venue gold" style="left:{info_x}px;width:{info_w}px;top:404px">CRESCENT HALL</div>
<div class="at vsub" style="left:{info_x}px;width:{info_w}px;top:444px">Crescent Nursery, Rochdale</div>

{hrule((info_x+W-70)/2, 494, (info_w-40)/2, node=False)}

<div class="at lab" style="left:{info_x}px;width:{info_w}px;top:520px">CONFIRM YOUR ATTENDANCE</div>
<div class="at wa" style="left:{info_x}px;width:{info_w}px;top:548px">WhatsApp 07884 053544</div>
<div class="at note" style="left:{info_x}px;width:{info_w}px;top:588px">A brothers-only gathering</div>
'''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Weekly Dhikr Gathering — Banner</title>
<style>{css()}</style></head>
<body><div class="page">
{tiles_svg()}
{frame_svg()}
{STAR_MARK}
{WORDMARK}
{title}
{info}
</div></body></html>'''

if __name__ == "__main__":
    html = page()
    p = HERE / "banner.html"
    p.write_text(html, encoding="utf-8")
    shot(p, HERE / "banner.png", W, H, scale=2)
