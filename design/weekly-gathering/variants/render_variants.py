#!/usr/bin/env python3
import subprocess, pathlib
from PIL import Image
import variants as v

HERE = v.HERE
CX, W, H = v.CX, v.W, v.H
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

def shot(html_path, out_png, scale=1):
    raw = out_png.with_name("_raw_" + out_png.stem + ".png")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                     f"--force-device-scale-factor={scale}", "--window-size=1200,2000",
                     "--screenshot="+str(raw), "--virtual-time-budget=8000",
                     "file://"+str(html_path.resolve())], capture_output=True)
    im = Image.open(raw).convert("RGB").crop((0, 0, 1200*scale, 1800*scale))
    im.save(out_png, optimize=True); raw.unlink()
    print(out_png.name, im.size)

BLDG_ARCH_DARK = v.mask_uri("mask-building-wide-dark.png")
BLDG_ARCH_GOLD = v.mask_uri("mask-building-wide-gold.png")
BLDG_SQ_GOLD   = v.mask_uri("mask-building-square-gold.png")
AW, AH = 1016, 525          # native size of the wide silhouette crop

def title_block(t1a, gap1=54, gap2=62):
    return (f'<div class="at t1 gold" style="top:{t1a}px">TARIQA AL QADIRIYA</div>\n'
            f'<div class="at t1 gold" style="top:{t1a+gap1}px">AL BOUTCHICHIYA</div>\n'
            f'<div class="at t2" style="top:{t1a+gap1+gap2}px">Weekly Dhikr Gathering</div>')

def ayah_block(top=104, gloss=172):
    return (f'<div class="at ayah" style="top:{top}px">{v.AYAH}</div>\n'
            f'<div class="at gloss" style="top:{gloss}px">'
            f'“ Verily, in the remembrance of God do hearts find rest. ”</div>')

def wordmark(top, h, w=None):
    w = w or h*640/113
    return (f'<div class="mark wordmark" style="top:{top}px;width:{w:.0f}px;height:{h}px;'
            f'-webkit-mask-image:url({v.WORD_URI});mask-image:url({v.WORD_URI})"></div>')

def star(top, size=46):
    """The order's own ten-point star mark, as a small crest — not the hero here,
       the building is, but the brief was clear: keep the logo in view."""
    return (f'<div class="mark seal" style="top:{top}px;width:{size}px;height:{size}px;'
            f'-webkit-mask-image:url({v.STAR_URI});mask-image:url({v.STAR_URI})"></div>')


# ============================================================ A — Dusk Court
def variant_a():
    """The hall itself, seen through the mihrab arch at dusk."""
    bw = 600
    scale = bw/AW
    dw, dh = bw, AH*scale
    dx, dy = CX-dw/2, v.ARCH_BASE-dh          # foot of the silhouette on the arch base

    extra_defs = f'''
    <clipPath id="archClip"><path d="{v.arch_d(9)} Z"/></clipPath>
    <linearGradient id="duskSky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"  stop-color="#241407"/>
      <stop offset="42%" stop-color="#4A2A14"/>
      <stop offset="74%" stop-color="#A5652E"/>
      <stop offset="100%" stop-color="#E8B368"/>
    </linearGradient>'''

    extra_body = f'''
  <g clip-path="url(#archClip)">
    <rect x="{v.ARCH_L-20}" y="{v.ARCH_APEX-20}" width="{v.ARCH_R-v.ARCH_L+40}" height="{v.ARCH_BASE-v.ARCH_APEX+40}" fill="url(#duskSky)"/>
    <image href="{BLDG_ARCH_DARK}" x="{dx:.1f}" y="{dy:.1f}" width="{dw:.1f}" height="{dh:.1f}" preserveAspectRatio="none"/>
  </g>
  <path d="{v.arch_d(9)} Z" fill="none" class="hair-2" stroke-width="1.1"/>'''

    hero = f'''
{ayah_block(90, 150)}
{star(196, 44)}
{title_block(258, 50, 56)}
{wordmark(420, 72)}
'''
    return v.page(hero, extra_defs=extra_defs, glow_cy=430, glow_r=46, extra_svg_body=extra_body)


# ============================================================ B — Seal of the House
def variant_b():
    """The hall set as a cameo within the halo that once framed the seal."""
    MED_CY, R = 372, 140
    clip_r = 116
    d = clip_r*2 * 1.06                      # slight overscan so the crop fills the disc

    extra_defs = f'<clipPath id="cameoClip"><circle cx="{CX}" cy="{MED_CY}" r="{clip_r}"/></clipPath>'
    extra_body = f'''
  <g class="med">{v.halo(CX, MED_CY, R)}</g>
  <g clip-path="url(#cameoClip)">
    <rect x="{CX-clip_r}" y="{MED_CY-clip_r}" width="{clip_r*2}" height="{clip_r*2}" fill="#1B1208"/>
    <image href="{BLDG_SQ_GOLD}" x="{CX-d/2:.1f}" y="{MED_CY-d/2:.1f}" width="{d:.1f}" height="{d:.1f}" preserveAspectRatio="none"/>
  </g>
  <circle cx="{CX}" cy="{MED_CY}" r="{clip_r}" class="hair-4" stroke-width="0.9" fill="none"/>'''

    hero = f'''
{ayah_block()}
{wordmark(530, 88)}
{star(628, 42)}
{title_block(684, 44, 48)}
'''
    return v.page(hero, extra_defs=extra_defs, glow_cy=MED_CY, glow_r=50, extra_svg_body=extra_body)


# ============================================================ C — Skyline Banner
def variant_c():
    """A bold graphic skyline as the poster's own letterhead."""
    bw = 740
    scale = bw/AW
    dw, dh = bw, AH*scale
    dx, dy = CX-dw/2, 100

    extra_body = f'''
  <image href="{BLDG_ARCH_GOLD}" x="{dx:.1f}" y="{dy:.1f}" width="{dw:.1f}" height="{dh:.1f}"
         preserveAspectRatio="none" style="filter:drop-shadow(0 0 22px rgba(230,190,110,.32))"/>
  <line x1="{dx+34:.1f}" y1="{dy+dh+22:.1f}" x2="{dx+dw-34:.1f}" y2="{dy+dh+22:.1f}" class="rule"/>'''

    star_top = dy+dh+38
    hero = f'''
{star(star_top, 42)}
{wordmark(star_top+58, 82)}
{title_block(star_top+58+82+16, 44, 48)}
'''
    return v.page(hero, glow_cy=300, glow_r=58, extra_svg_body=extra_body)


# ============================================================ D — Framed Keepsake
def variant_d():
    """A framed photograph of the hall, hung beneath the order's own words."""
    cw = 520
    scale = cw/AW
    dw, dh = cw, AH*scale
    pad = 20
    cy0 = 210

    extra_defs = f'<clipPath id="frameClip"><rect x="{CX-dw/2:.1f}" y="{cy0}" width="{dw:.1f}" height="{dh:.1f}"/></clipPath>'
    extra_body = f'''
  <rect x="{CX-dw/2-pad:.1f}" y="{cy0-pad}" width="{dw+2*pad:.1f}" height="{dh+2*pad:.1f}" class="hair-3" stroke-width="1.1" fill="none"/>
  <rect x="{CX-dw/2-pad+7:.1f}" y="{cy0-pad+7}" width="{dw+2*pad-14:.1f}" height="{dh+2*pad-14:.1f}" class="hair-5" stroke-width="0.6" fill="none"/>
  <g clip-path="url(#frameClip)">
    <rect x="{CX-dw/2:.1f}" y="{cy0}" width="{dw:.1f}" height="{dh:.1f}" fill="#1B1208"/>
    <image href="{BLDG_ARCH_GOLD}" x="{CX-dw/2:.1f}" y="{cy0}" width="{dw:.1f}" height="{dh:.1f}" preserveAspectRatio="none"/>
  </g>
  {v.lozenge(CX, cy0-pad, 5, 8, "fill-lit")}
  {v.lozenge(CX, cy0+dh+pad, 5, 8, "fill-lit")}'''

    frame_bottom = cy0 + dh + pad
    wm_top = frame_bottom+22
    star_top = wm_top+84+12
    hero = f'''
{ayah_block(100, 164)}
{wordmark(wm_top, 84)}
{star(star_top, 38)}
{title_block(star_top+38+12, 42, 46)}
'''
    return v.page(hero, extra_defs=extra_defs, glow_cy=cy0+dh/2, glow_r=44, extra_svg_body=extra_body)


# ============================================================ E — Sacred Dome
import json as _json
DOME_MASK_URI = v.mask_uri("mask-dome.png")
DOME_DARK_URI = v.mask_uri("mask-dome-dark.png")
DOME_W, DOME_H = 1488, 966
_DOME_PATHS = _json.loads((HERE/"engrave.json").read_text())

def dome_group(x, y, w, h, mask_id, stroke="#F0D8A0", sw=1.7):
    sx, sy = w/DOME_W, h/DOME_H
    lines = "\n".join(
        f'<path d="{p}" fill="none" stroke="{stroke}" stroke-width="{sw}" vector-effect="non-scaling-stroke"/>'
        for p in _DOME_PATHS["ribs"]+_DOME_PATHS["drum"]+_DOME_PATHS["facade"]+_DOME_PATHS["cornices"])
    return (
        f'<defs><mask id="{mask_id}" maskUnits="userSpaceOnUse">'
        f'<image href="{DOME_MASK_URI}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/>'
        f'</mask></defs>\n'
        f'<image href="{DOME_DARK_URI}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/>\n'
        f'<g mask="url(#{mask_id})" transform="translate({x:.1f},{y:.1f}) scale({sx:.5f},{sy:.5f})">{lines}</g>'
    )

def variant_e():
    """The Dome of the Rock, engraved: ribs, drum arcade, facade arcade — not a flat block."""
    bw = 620
    dh = bw*DOME_H/DOME_W
    dx, dy = CX-bw/2, 90

    extra_body = (
        dome_group(dx, dy, bw, dh, "domeMaskE") +
        f'\n  <line x1="{dx+30:.1f}" y1="{dy+dh+20:.1f}" x2="{dx+bw-30:.1f}" y2="{dy+dh+20:.1f}" class="rule"/>'
    )

    wm_top = dy+dh+38
    star_top = wm_top+78+10
    hero = f'''
{wordmark(wm_top, 78)}
{star(star_top, 36)}
{title_block(star_top+36+10, 40, 44)}
'''
    return v.page(hero, glow_cy=dy+dh*0.4, glow_r=54, extra_svg_body=extra_body)


VARIANTS = {"A": variant_a, "B": variant_b, "C": variant_c, "D": variant_d, "E": variant_e}

if __name__ == "__main__":
    for key, fn in VARIANTS.items():
        html = fn()
        p = HERE / f"poster-{key}.html"
        p.write_text(html, encoding="utf-8")
        shot(p, HERE / f"variant-{key}.png", scale=1)
