#!/usr/bin/env python3
"""The chosen layout — arch, ayah, title, wordmark — with the order's own
   star mark (not a building) filling the arch, in a halo of 99 tasbih marks.
   A palette dict swaps the whole poster's colourway without touching layout."""
import base64, pathlib, subprocess
from PIL import Image
import variants as v
from render_variants import title_block, ayah_block, wordmark, HERE

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


def build_hero(pal=None):
    pal = pal or DEFAULT_PALETTE
    MED_CY, R, SEAL_D = 656, 150, 252          # SEAL_D deliberately smaller than R —
    extra_body = f'<g class="med">{v.halo(CX, MED_CY, R)}</g>'  # daylight for the 99-mark ring
    # against a busy photographed background, the gold star/wordmark need a
    # dark backing of their own to stay legible — off by default (transparent,
    # 0 radius/size), a palette can opt in via mark_backing.
    backing = pal.get('mark_backing')
    word_backing = (f'<div style="position:absolute;left:50%;top:{420+36}px;width:640px;height:220px;'
                     f'transform:translate(-50%,-50%);border-radius:50%;'
                     f'background:radial-gradient(50% 50% at 50% 50%,{backing} 0%,{backing} 42%,transparent 78%)"></div>') if backing else ''
    seal_backing = (f'<div style="position:absolute;left:50%;top:{MED_CY}px;width:{R*2+90}px;height:{R*2+90}px;'
                     f'transform:translate(-50%,-50%);border-radius:50%;'
                     f'background:radial-gradient(50% 50% at 50% 50%,{backing} 0%,{backing} 55%,transparent 82%)"></div>') if backing else ''
    hero = f'''
{ayah_block(90, 150)}
{title_block(258, 50, 56, cls=pal.get('title_cls', 'gold'))}
{word_backing}
{wordmark(420, 72)}
{seal_backing}
<div class="mark seal" style="top:{MED_CY-SEAL_D//2}px;width:{SEAL_D}px;height:{SEAL_D}px;
  -webkit-mask-image:url({v.STAR_URI});mask-image:url({v.STAR_URI})"></div>
'''
    return hero, extra_body


# ---------- opaque "inscription panel" shapes, for text over a busy photo ----------
# Plain rectangles read as pasted-on boxes; these two shapes are drawn from the
# manuscript's own visual language instead — the mihrab arch already used as a
# decorative outline (closed into a solid field), and a cusped cartouche bar,
# the shape Persian/Islamic illumination actually uses to carry an inscription.
def hero_arch_panel(base_y, inset=0.0):
    l, r = v.ARCH_L+inset, v.ARCH_R-inset
    a = v.ARCH_APEX+inset*0.9
    sh = 430+inset*0.4
    return (f'M {l},{base_y} L {l},{sh} Q {l},{a+95} {CX},{a} '
            f'Q {r},{a+95} {r},{sh} L {r},{base_y} Z')

def cartouche_bar(cx, cy, w, h, tip=None):
    hw, hh = w/2, h/2
    # a shallower cusp than a true lens — enough to read as a pointed cartouche
    # without narrowing the top/bottom edges so much that wrapped text overflows.
    tip = tip if tip is not None else min(hh*1.4, hw*0.35)
    bow = hh*0.55
    return (f'M {cx-hw:.1f},{cy:.1f} '
            f'Q {cx-hw+tip*0.5:.1f},{cy-bow:.1f} {cx-hw+tip:.1f},{cy-hh:.1f} '
            f'L {cx+hw-tip:.1f},{cy-hh:.1f} '
            f'Q {cx+hw-tip*0.5:.1f},{cy-bow:.1f} {cx+hw:.1f},{cy:.1f} '
            f'Q {cx+hw-tip*0.5:.1f},{cy+bow:.1f} {cx+hw-tip:.1f},{cy+hh:.1f} '
            f'L {cx-hw+tip:.1f},{cy+hh:.1f} '
            f'Q {cx-hw+tip*0.5:.1f},{cy+bow:.1f} {cx-hw:.1f},{cy:.1f} Z')

def cartouche_panels_svg(pal):
    zones = pal.get('cartouche_zones')
    if not zones:
        return ''
    fill = pal.get('cartouche_fill', 'rgba(10,14,40,.86)')
    edge = pal.get('cartouche_edge', '#D8B870')
    out = []
    for z in zones:
        if z['shape'] == 'arch':
            d_outer = hero_arch_panel(z['base_y'])
            d_inner = hero_arch_panel(z['base_y']-14, inset=14)
        else:
            d_outer = cartouche_bar(z['cx'], z['cy'], z['w'], z['h'])
            d_inner = cartouche_bar(z['cx'], z['cy'], z['w']-24, z['h']-24)
        out.append(f'<path d="{d_outer}" fill="{fill}" stroke="{edge}" stroke-width="1.4"/>')
        out.append(f'<path d="{d_inner}" fill="none" stroke="{edge}" stroke-width="0.6" opacity="0.75"/>')
    return "\n".join(out)


def _polygon(cx, cy, r, n, rot=0.0):
    return v.fmt([v.P(cx, cy, r, rot + i*360.0/n) for i in range(n)])

def lattice(p_):
    """An alternative motif: a nested diamond trellis — mashrabiya rather than khatim."""
    outer = _polygon(p_/2, p_/2, p_/2*0.94, 4, 45)
    inner = _polygon(p_/2, p_/2, p_/2*0.58, 4, 45)
    return [outer, inner]

def lattice_layer(p_, cls="zh", w=0.75):
    g = [f'<pattern id="lat{int(p_)}" width="{p_}" height="{p_}" patternUnits="userSpaceOnUse">']
    for d in lattice(p_):
        g.append(f'<path d="{d}" fill="none" class="{cls}" stroke-width="{w}"/>')
    g.append('</pattern>')
    return "\n".join(g)


DEFAULT_PALETTE = dict(
    name="Lamplight Gold",
    pattern="zellij", tile_small_op=0.22, tile_big_op=0.20, band_op=0.34,
    bg1="radial-gradient(112% 62% at 50% 24%, #6B4A22 0%, #4C3316 34%, #302012 62%, #211609 100%)",
    bg2="radial-gradient(88% 42% at 50% 96%, #3E2A14 0%, #2A1C0E 46%, #1D1409 100%)",
    print_bg="#211609",
    hair1="#E8CE95", hair2="#C6A25C", hair3="#9A7A3C", hair4="#7E6230", hair5="#6A5228",
    petal="rgba(200,160,86,.055)", petal_stroke="#B08F4E",
    petal_lit="rgba(232,198,124,.10)", petal_lit_stroke="#E2C284",
    dot="#F2DFAE", fill_lit="#D9B978", stroke_node="#9A7A3C",
    rule="#8A6C34", rule_lit="#DCBB79",
    zh="#C9A25C", zf="#9A7A3C", zstud="#C9A25C", zb="#C6A059",
    scrim="23,15,7",
    gold_grad="linear-gradient(178deg,#FBEECB 0%,#E7CD92 26%,#C69E56 58%,#F3E3B7 82%,#D3AE68 100%)",
    mark_grad="linear-gradient(176deg,#FBEECB 0%,#EBD49B 22%,#C89F55 54%,#F4E5BB 78%,#D2AC64 100%)",
    ayah="#E9CE95", gloss="#D5B87E", t2="#EDD29E", lab="#D0B16A", val="#F5E4B6",
    body="#E3C994", pt="#F1DBA9", pd="#CDB07A", rn="#B99A55", vsub="#C8A974",
    addr="#EFD8A6", wa="#F0D9A2", note="#B99C66", url="#C0A05C",
    halo0="#EFCB8A", halo1="#DCB068", halo2="#C79A4E", halo3="#A87F3A",
)

def css(pal):
    return f'''
{v.FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#000}}
@page{{size:12.5in 18.75in;margin:0}}
@media print{{html,body{{background:{pal['print_bg']};-webkit-print-color-adjust:exact;print-color-adjust:exact}}}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;
  background:{f"url({pal['bg_image_uri']}) center/cover no-repeat" if pal.get('bg_image_uri') else f"{pal['bg1']},{pal['bg2']}"};
  font-kerning:normal;-webkit-font-smoothing:antialiased;}}
.layer{{position:absolute;inset:0;width:100%;height:100%}}
.grain{{position:absolute;inset:0;opacity:.05;mix-blend-mode:overlay;pointer-events:none;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4'/><feColorMatrix type='saturate' values='0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>");}}

.hair-1{{fill:none;stroke:{pal['hair1']};opacity:.97}}
.hair-2{{fill:none;stroke:{pal['hair2']};opacity:.85}}
.hair-3{{fill:none;stroke:{pal['hair3']};opacity:.80}}
.hair-4{{fill:none;stroke:{pal['hair4']};opacity:.75}}
.hair-5{{fill:none;stroke:{pal['hair5']};opacity:.55}}
.brd1{{fill:none;stroke:{pal.get('border1', pal['hair3'])};opacity:.80}}
.brd2{{fill:none;stroke:{pal.get('border2', pal['hair5'])};opacity:.55}}
.brd3{{fill:none;stroke:{pal.get('border3', pal['hair4'])};opacity:.75}}
.petal{{fill:{pal['petal']};stroke:{pal['petal_stroke']};opacity:.75}}
.petal-lit{{fill:{pal['petal_lit']};stroke:{pal['petal_lit_stroke']};opacity:.9}}
.dot{{fill:{pal['dot']}}}
.fill-lit{{fill:{pal['fill_lit']}}}
.fill-ink{{fill:#150E06}}
.stroke-node{{fill:none;stroke:{pal['stroke_node']};stroke-width:1}}
.rule{{stroke:{pal['rule']};stroke-width:1;opacity:.85}}
.rule-lit{{stroke:{pal['rule_lit']};stroke-width:1;opacity:.9}}
.ground{{opacity:{pal.get('ground_op', 0.072)}}}
.zh{{stroke:{pal['zh']}}}
.zf{{stroke:{pal['zf']}}}
.zstud{{fill:{pal['zstud']}}}
.zb{{stroke:{pal['zb']}}}
.band{{opacity:.34}}
.tiles{{opacity:.20}}
.scrim{{position:absolute;inset:0;pointer-events:none;
  background:
    radial-gradient(62% 34% at 50% 21%, rgba({pal['scrim']},{0.64*pal.get('scrim_mult',1.0):.3f}) 0%, rgba({pal['scrim']},{0.30*pal.get('scrim_mult',1.0):.3f}) 58%, rgba({pal['scrim']},0) 100%),
    radial-gradient(72% 40% at 50% 61%, rgba({pal['scrim']},{0.70*pal.get('scrim_mult',1.0):.3f}) 0%, rgba({pal['scrim']},{0.36*pal.get('scrim_mult',1.0):.3f}) 55%, rgba({pal['scrim']},0) 100%),
    radial-gradient(64% 26% at 50% 87%, rgba({pal['scrim']},{0.68*pal.get('scrim_mult',1.0):.3f}) 0%, rgba({pal['scrim']},{0.32*pal.get('scrim_mult',1.0):.3f}) 58%, rgba({pal['scrim']},0) 100%);}}
.med{{filter:{pal.get('med_shadow', 'drop-shadow(0 0 16px rgba(230,192,116,.26))')}}}

.at{{position:absolute;left:0;right:0;text-align:center;
  -webkit-text-stroke:{pal.get('outline_stroke','0 transparent')};
  text-shadow:{pal.get('text_shadow', '0 1px 3px rgba(6,4,2,.72), 0 0 14px rgba(6,4,2,.45)')}}}
.mark{{position:absolute;left:50%;transform:translateX(-50%);
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
  -webkit-mask-size:contain;mask-size:contain;
  -webkit-mask-position:center;mask-position:center;
  background-image:{pal['mark_grad']};}}
.seal{{filter:{pal.get('seal_shadow', 'drop-shadow(0 0 20px rgba(232,194,116,.30)) drop-shadow(0 1px 1px rgba(0,0,0,.5))')}}}
.wordmark{{filter:{pal.get('wordmark_shadow', 'drop-shadow(0 0 16px rgba(226,186,108,.24)) drop-shadow(0 1px 1px rgba(0,0,0,.55))')}}}
.gold{{background:{pal['gold_grad']};
  -webkit-background-clip:text;background-clip:text;color:transparent;
  filter:{pal.get('gold_shadow', 'drop-shadow(0 1px 0 rgba(0,0,0,.6)) drop-shadow(0 2px 5px rgba(6,4,2,.7)) drop-shadow(0 0 20px rgba(214,172,100,.26))')}}}
.at.gold{{text-shadow:none}}
.ink{{color:{pal.get('title_color', '#1A1006')}}}
.ayah{{font-family:Amiri,serif;font-size:40px;line-height:1.55;color:{pal['ayah']};
  direction:rtl;filter:{pal.get('ayah_shadow', 'drop-shadow(0 0 16px rgba(214,172,100,.28))')}}}
.gloss{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:31px;
  letter-spacing:.03em;color:{pal['gloss']}}}
.t1{{font-family:Cinzel,serif;font-weight:600;font-size:50px;letter-spacing:.135em;
  text-indent:.135em;line-height:1}}
.t2{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:43px;
  letter-spacing:.045em;color:{pal['t2']}}}
.lab{{font-family:Cinzel,serif;font-weight:400;font-size:12.5px;letter-spacing:.5em;
  text-indent:.5em;color:{pal['lab']}}}
.val{{font-family:Cormorant,serif;font-weight:{pal.get('val_weight',400)};font-size:{pal.get('val_size','26px')};letter-spacing:.075em;
  text-indent:.075em;color:{pal['val']}}}
.body{{font-family:Cormorant,serif;font-weight:{pal.get('body_weight',400)};font-size:35px;line-height:1.24;
  letter-spacing:.005em;color:{pal['body']}}}
.body em{{font-style:italic;color:{pal['gloss']}}}
.pt{{font-variant-numeric:lining-nums;font-family:Cinzel,serif;font-weight:600;font-size:{pal.get('pt_size','27px')};letter-spacing:.03em;
  text-indent:.03em;color:{pal['pt']}}}
.pd{{font-family:Cormorant,serif;font-weight:{pal.get('pd_weight',400)};font-size:21.5px;line-height:1.46;
  letter-spacing:.03em;color:{pal['pd']}}}
.rn{{font-family:Cinzel,serif;font-size:11.5px;letter-spacing:.34em;text-indent:.34em;color:{pal['rn']}}}
.venue{{font-family:Cinzel,serif;font-weight:600;font-size:39px;letter-spacing:.18em;text-indent:.18em}}
.vsub{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:23px;
  letter-spacing:.06em;color:{pal['vsub']}}}
.addr{{font-variant-numeric:lining-nums;font-feature-settings:'lnum' 1;font-family:Cormorant,serif;font-weight:{pal.get('addr_weight',400)};font-size:24px;letter-spacing:.13em;
  text-indent:.13em;color:{pal['addr']};text-transform:uppercase}}
.wa{{font-variant-numeric:lining-nums;font-feature-settings:'lnum' 1;font-family:Cormorant,serif;font-weight:{pal.get('wa_weight',400)};font-size:34.5px;letter-spacing:.1em;
  text-indent:.1em;color:{pal['wa']}}}
.note{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:20px;
  letter-spacing:.05em;color:{pal['note']}}}
.url{{font-family:Cinzel,serif;font-size:12.5px;letter-spacing:.42em;text-indent:.42em;color:{pal['url']}}}
.cols{{position:absolute;left:{CX-350}px;width:700px;display:grid;
  grid-template-columns:1fr 1fr 1fr;text-align:center}}
.cols > div{{padding:0 14px}}
.cols > div + div{{border-left:1px solid rgba(138,108,52,.5)}}
'''

def frame_svg(pal, hero_extra):
    band_pat = lattice_layer(36, "zb", 0.75) if pal["pattern"] == "lattice" else v.zellij_layer(36, "zb", 0.75, studs=False)
    band_id = "lat36" if pal["pattern"] == "lattice" else "zj36"
    return f'''
<svg class="layer" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" stitchTiles="stitch"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
    <radialGradient id="halo" cx="50%" cy="{656/H*100:.1f}%" r="52%">
      <stop offset="0%"   stop-color="{pal['halo0']}" stop-opacity="{0.20*pal.get('halo_mult',1.0):.4f}"/>
      <stop offset="26%"  stop-color="{pal['halo1']}" stop-opacity="{0.105*pal.get('halo_mult',1.0):.4f}"/>
      <stop offset="48%"  stop-color="{pal['halo2']}" stop-opacity="{0.048*pal.get('halo_mult',1.0):.4f}"/>
      <stop offset="72%"  stop-color="{pal['halo3']}" stop-opacity="{0.016*pal.get('halo_mult',1.0):.4f}"/>
      <stop offset="100%" stop-color="{pal['halo3']}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#halo)"/>

  <g class="ground">{v.ground_rosette(CX, 1060, 720)}</g>

  {v.arch(0, "brd2", 1.0)}
  {v.arch(11, "brd2", 0.6)}

  {cartouche_panels_svg(pal)}

  {hero_extra}

  <!-- frame: a tiled band, the way a Moroccan wall carries its dado -->
  <defs>{band_pat}</defs>
  <path fill-rule="evenodd" fill="url(#{band_id})" style="opacity:{pal['band_op']}"
        d="M38,38 H{W-38} V{H-38} H38 Z M74,74 H{W-74} V{H-74} H74 Z"/>
  <rect x="38" y="38" width="{W-76}" height="{H-76}" class="brd1" stroke-width="1.15" fill="none"/>
  <rect x="45" y="45" width="{W-90}" height="{H-90}" class="brd2" stroke-width="0.6" fill="none"/>
  <rect x="74" y="74" width="{W-148}" height="{H-148}" class="brd1" stroke-width="1.0" fill="none"/>
  <rect x="81" y="81" width="{W-162}" height="{H-162}" class="brd2" stroke-width="0.6" fill="none"/>
  {v.corner(74,74,1,1,0.66,cls1="brd1",cls2="brd3")}{v.corner(W-74,74,-1,1,0.66,cls1="brd1",cls2="brd3")}{v.corner(74,H-74,1,-1,0.66,cls1="brd1",cls2="brd3")}{v.corner(W-74,H-74,-1,-1,0.66,cls1="brd1",cls2="brd3")}

  {v.rule(CX, v.ARCH_BASE, 350)}
  <line x1="{CX}" y1="{v.ARCH_BASE+34}" x2="{CX}" y2="{v.ARCH_BASE+128}" class="rule"/>

  {v.rule(CX, 1366, 350) if not pal.get('cartouche_zones') else ''}
  {f'<rect x="{CX-322}" y="1536" width="644" height="140" rx="2" class="hair-3" stroke-width="1" fill="none"/><rect x="{CX-315}" y="1543" width="630" height="126" rx="1" class="hair-5" stroke-width="0.6" fill="none"/>' if not pal.get('cartouche_zones') else ''}
  {v.lozenge(CX-322,1606,5,8,"fill-ink")}{v.lozenge(CX+322,1606,5,8,"fill-ink")}
  {v.lozenge(CX-322,1606,5,8,"stroke-node")}{v.lozenge(CX+322,1606,5,8,"stroke-node")}
</svg>
<div class="grain"></div>
'''

def tiles_svg(pal):
    if pal["pattern"] == "lattice":
        big = lattice_layer(130, "zh", 0.75); small = lattice_layer(32, "zf", 0.5)
        big_id, small_id = "lat130", "lat32"
    else:
        big = v.zellij_layer(104, "zh", 1.0); small = v.zellij_layer(26, "zf", 0.55, studs=False)
        big_id, small_id = "zj104", "zj26"
    return f'''
<svg class="layer" style="opacity:{pal['tile_big_op']}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>{big}{small}</defs>
  <rect width="{W}" height="{H}" fill="url(#{small_id})" opacity="{pal['tile_small_op']}"/>
  <rect width="{W}" height="{H}" fill="url(#{big_id})"/>
</svg>
<div class="scrim"></div>
'''

# the current, manually-set example date — kept as the default so every
# existing render (and every colourway's __main__ call) stays unchanged.
# Pass a dict from prayer_times.build_schedule(event_date) to render(..., sched=...)
# to compute these from the real Maghrib time for a different date instead.
DEFAULT_SCHED = dict(
    weekday="SATURDAY", date_str="29 August 2026", event_window="7:00 – 9:00 pm",
    slot1_time="7:00 – 8:15", slot2_time="8:15 – 8:30", slot3_time="8:30",
)

def bottom_html(sched=None):
    s = dict(DEFAULT_SCHED, **(sched or {}))
    return f'''
<div class="at lab" style="top:{v.ARCH_BASE+32}px;left:{CX-350}px;width:340px">{s['weekday']}</div>
<div class="at val" style="top:{v.ARCH_BASE+58}px;left:{CX-350}px;width:340px">{s['date_str']}</div>
<div class="at lab" style="top:{v.ARCH_BASE+32}px;left:{CX+10}px;width:340px">EVENING</div>
<div class="at val" style="top:{v.ARCH_BASE+58}px;left:{CX+10}px;width:340px">{s['event_window']}</div>

<div class="at body" style="top:980px;left:{CX-500}px;width:1000px">
The tariqa's weekly Moroccan <em>dhikr</em> — guided remembrance, recited with
<em>idhn</em> (spiritual permission), in the company of those walking the path
of spiritual refinement.
</div>

<div class="cols" style="top:1220px">
  <div><div class="rn">I</div><div class="pt" style="margin-top:11px">{s['slot1_time']}</div>
       <div class="pd" style="margin-top:13px">Wadhifa Dhikr<br>and Dhikr al&nbsp;Faraj</div></div>
  <div><div class="rn">II</div><div class="pt" style="margin-top:11px">{s['slot2_time']}</div>
       <div class="pd" style="margin-top:13px">Talk</div></div>
  <div><div class="rn">III</div><div class="pt" style="margin-top:11px">{s['slot3_time']}</div>
       <div class="pd" style="margin-top:13px">Maghrib, followed<br>by refreshments</div></div>
</div>

<div class="at venue gold" style="top:1396px">CRESCENT HALL</div>
<div class="at vsub" style="top:1450px">Crescent Nursery</div>
<div class="at addr" style="top:1486px">162 EDMUND STREET · ROCHDALE OL12 6QG</div>

<div class="at lab" style="top:1566px">PLEASE CONFIRM YOUR ATTENDANCE</div>
<div class="at wa" style="top:1594px">WhatsApp 07884 053544</div>
<div class="at note" style="top:1636px">A brothers-only gathering</div>

<div class="at url" style="top:1700px">WWW.THESUFIWAY.CO.UK</div>
'''

def render(pal, out_name, scale=1, sched=None):
    hero, hero_extra = build_hero(pal)
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Weekly Dhikr Gathering</title>
<style>{css(pal)}</style></head>
<body><div class="page">
{tiles_svg(pal)}
{frame_svg(pal, hero_extra)}
{hero}
{bottom_html(sched)}
</div></body></html>'''
    hp = HERE / f"{out_name}.html"
    hp.write_text(html, encoding="utf-8")
    shot(hp, HERE / f"{out_name}.png", scale=scale)

EMERALD = dict(DEFAULT_PALETTE)
EMERALD.update(
    name="Emerald Court", pattern="zellij",
    bg1="radial-gradient(112% 62% at 50% 24%, #2E5B3E 0%, #1F4030 34%, #142A20 62%, #0C1B14 100%)",
    bg2="radial-gradient(88% 42% at 50% 96%, #1B3A28 0%, #12291C 46%, #0B1B12 100%)",
    print_bg="#0C1B14",
    scrim="8,20,14",
    zh="#B8CBA8", zf="#8FA37C", zstud="#C9A25C", zb="#9FB48C",
    rule="#6E8A5C", rule_lit="#DCBB79",
)

BURGUNDY = dict(DEFAULT_PALETTE)
BURGUNDY.update(
    name="Royal Burgundy", pattern="lattice",
    tile_small_op=0.10, tile_big_op=0.13, band_op=0.20,
    bg1="radial-gradient(112% 62% at 50% 24%, #6B2430 0%, #4A1620 34%, #2E0E16 62%, #1C0910 100%)",
    bg2="radial-gradient(88% 42% at 50% 96%, #3A121A 0%, #260D12 46%, #19090D 100%)",
    print_bg="#1C0910",
    scrim="24,8,12",
    zh="#C99A9E", zf="#9A6468", zstud="#C9A25C", zb="#B98488",
    rule="#8A4C52", rule_lit="#DCBB79",
)

INDIGO = dict(DEFAULT_PALETTE)
INDIGO.update(
    name="Midnight Indigo", pattern="zellij",
    bg1="radial-gradient(112% 62% at 50% 24%, #223655 0%, #16253C 34%, #0E1826 62%, #0A121D 100%)",
    bg2="radial-gradient(88% 42% at 50% 96%, #17293F 0%, #101D2D 46%, #0A141F 100%)",
    print_bg="#0A121D",
    hair1="#EDEFF3", hair2="#C7CEDA", hair3="#98A2B3", hair4="#77839A", hair5="#4A5468",
    petal="rgba(180,190,205,.06)", petal_stroke="#A9B4C6",
    petal_lit="rgba(220,226,236,.10)", petal_lit_stroke="#DDE3ED",
    dot="#F2F4F8", fill_lit="#C9D2E0", stroke_node="#8FA0B8",
    rule="#7C8AA0", rule_lit="#D7DEE9",
    zh="#B7C2D3", zf="#8895A8", zstud="#B7C2D3", zb="#B0BBCC",
    scrim="10,18,29",
    gold_grad="linear-gradient(178deg,#FFFFFF 0%,#E4E9F1 26%,#B7C2D3 58%,#F2F5F9 82%,#C7D0DE 100%)",
    mark_grad="linear-gradient(176deg,#FFFFFF 0%,#E9EDF4 22%,#C3CCDA 54%,#F5F7FA 78%,#CDD5E2 100%)",
    ayah="#E7ECF4", gloss="#B7C2D3", t2="#DCE2EC", lab="#C3CBDA", val="#F0F3F8",
    body="#D7DDE8", pt="#EDF0F5", pd="#B9C2D2", rn="#96A2B5", vsub="#B0BBCC",
    addr="#E9EDF4", wa="#EEF1F6", note="#9CA8BB", url="#8D99AC",
    halo0="#F3F6FA", halo1="#D7DEE9", halo2="#B7C2D3", halo3="#8FA0B8",
)

BLACKGOLD = dict(DEFAULT_PALETTE)
BLACKGOLD.update(
    name="Black & Gold", pattern="zellij",
    bg1="radial-gradient(112% 62% at 50% 24%, #2A2A2A 0%, #1A1A1A 34%, #0D0D0D 62%, #050505 100%)",
    bg2="radial-gradient(88% 42% at 50% 96%, #161616 0%, #0C0C0C 46%, #040404 100%)",
    print_bg="#050505",
    scrim="4,4,4",
    # hairlines, the frame, the star's own gradient — the "gold" — stay as DEFAULT_PALETTE's.
    # only the reading text splits: headings and small accents stay gold, body copy turns white.
    ayah="#F3F1EA", gloss="#D9D6CC", t2="#EDEAE1", val="#F5F3EC",
    body="#E6E3D9", pt="#F5F3EC", pd="#CFCBBE", vsub="#C9C5B8",
    addr="#EDEAE0", wa="#F2EFE6", note="#C7C3B6",
    # the small tracked-caps gold accents were tuned against a warm brown ground —
    # against true black they read dim, so lift them a step for this palette.
    lab="#E2C685", rn="#D6B876", url="#CDAF77",
)

EARTHY = dict(BLACKGOLD)
EARTHY.update(
    name="Earthy Gold",
    # Everything gold — hairlines, the star, the two titles, the small caps
    # accents — and the white reading text are untouched from BLACKGOLD.
    # Only the ground itself changes: from neutral near-black to a warm
    # terracotta-clay dark, so the gold still sits on black at heart, just
    # a black with sun-baked earth in it rather than studio neutral.
    bg1="radial-gradient(115% 65% at 50% 26%, #4E2C16 0%, #35200F 34%, #211408 62%, #130B04 100%)",
    bg2="radial-gradient(90% 45% at 50% 96%, #2C190B 0%, #1A0F06 46%, #0E0803 100%)",
    print_bg="#130B04",
    scrim="19,11,5",
)

# ---------- Sandstone & Gold — earthy, but light ----------
# EARTHY kept the ground dark (terracotta-clay black) with light gold/white
# reading text. This flips that: a genuinely light, sun-baked sandstone and
# terracotta ground, with every gold token and every reading-text token
# pushed down to a deep antique bronze / espresso ink so it still reads
# clearly against the pale ground. The warm glows and dark contact-shadows
# tuned for a dark backdrop are replaced with much quieter light-appropriate
# equivalents (text_shadow/gold_shadow/seal_shadow/wordmark_shadow/
# ayah_shadow/med_shadow, halo_mult) rather than muddying a light page with
# shadow tones built for a dark one.
SANDSTONE = dict(DEFAULT_PALETTE)
SANDSTONE.update(
    name="Sandstone & Gold", pattern="zellij",
    tile_small_op=0.30, tile_big_op=0.27, band_op=0.40,
    body_weight=600, val_weight=600, pd_weight=600, addr_weight=600, wa_weight=600,
    # a properly saturated clay-and-terracotta ground, pushed further into real
    # sunset colour — warm ochre at top through to a deep, live burnt terracotta.
    bg1="radial-gradient(160% 100% at 50% 20%, #F4DEA0 0%, #EEC876 60%, #E0A455 88%, #D18F42 100%)",
    bg2="radial-gradient(140% 90% at 50% 100%, #E0A455 0%, #CC8740 50%, #A8672E 100%)",
    print_bg="#EEC876",
    # richer, warmer antique amber-gold — more saturated than a muted olive-bronze —
    # for the hairlines, frame and pattern.
    hair1="#B8862E", hair2="#9C6F27", hair3="#7E5A20", hair4="#63451A", hair5="#4C3414",
    petal="rgba(156,111,39,.11)", petal_stroke="#9C6F27",
    petal_lit="rgba(184,134,46,.18)", petal_lit_stroke="#B8862E",
    dot="#8A5F22", fill_lit="#B8862E", stroke_node="#7E5A20",
    rule="#8A5F22", rule_lit="#B8862E",
    zh="#9C6F27", zf="#7E5A20", zstud="#9C6F27", zb="#8A5F22",
    scrim="230,180,110", scrim_mult=0.24, halo_mult=0.38, ground_op=0.0,
    # every reading text — title, subtitle, wordmark, star, ayah + translation,
    # date/time, body, programme, venue and its details, WhatsApp, footer —
    # in one plain black ink. Simplest possible read against the terracotta
    # ground; only the outer border stays a deliberate accent colour (red).
    gold_grad="linear-gradient(178deg,#140D06 0%,#140D06 100%)",
    title_cls="ink", title_color="#140D06",
    mark_grad="linear-gradient(176deg,#140D06 0%,#140D06 100%)",
    ayah="#140D06", gloss="#140D06", t2="#140D06", lab="#140D06", val="#140D06",
    body="#140D06", pt="#140D06", pd="#140D06", rn="#140D06", vsub="#140D06",
    addr="#140D06", wa="#140D06", note="#140D06", url="#140D06",
    # the actual clock times — the top event window and the three programme
    # slots — enlarged to fill their columns rather than sitting small in them.
    val_size="38px", pt_size="34px",
    halo0="#B8862E", halo1="#9C6F27", halo2="#7E5A20", halo3="#63451A",
    # the page border — outer frame, arch outline, corner flourishes — a rich red,
    # kept separate from hair3/hair4/hair5 so the star's own halo ring (which
    # reuses hair-5) isn't dragged red along with it.
    border1="#8A1A1A", border2="#6E1414", border3="#7A1717",
    text_shadow="0 1px 1px rgba(255,250,240,.55)",
    gold_shadow="drop-shadow(0 1px 0 rgba(255,255,255,.35)) drop-shadow(0 1px 3px rgba(58,33,13,.24))",
    seal_shadow="drop-shadow(0 1px 3px rgba(58,33,13,.24)) drop-shadow(0 1px 1px rgba(255,255,255,.3))",
    wordmark_shadow="drop-shadow(0 1px 3px rgba(58,33,13,.22)) drop-shadow(0 1px 1px rgba(255,255,255,.3))",
    ayah_shadow="drop-shadow(0 1px 2px rgba(58,33,13,.20))",
    med_shadow="drop-shadow(0 0 12px rgba(184,134,46,.24))",
)

# ---------- Illuminated Manuscript — the user's own hand-painted tazhib ----------
# Not a generated pattern at all: bg-illum-1200x1800.jpg is built from a photo of
# the user's own illumination work (mirrored 2x2 into a symmetric medallion tile,
# then tiled down the page — see design/weekly-gathering/illuminated/README.md).
# Real photographed paint/gold-leaf texture as the actual background, so every
# generated overlay (zellij tiles, ground rosette, dado band, halo glow, scrim)
# is switched off — layering vector pattern on top of a photograph would just
# fight it. The star and Arabic wordmark keep their gold on a soft dark backing
# (mark_backing) so they don't get lost in the busy artwork; every actual line
# of text is flat white with a bold black outline (outline_stroke) instead,
# since it has to read against blue, purple, teal and gold in different places.
def _jpeg_uri(name):
    return "data:image/jpeg;base64," + base64.b64encode((HERE / name).read_bytes()).decode()

ILLUMINATED = dict(DEFAULT_PALETTE)
ILLUMINATED.update(
    name="Illuminated Manuscript", pattern="zellij",
    bg_image_uri=_jpeg_uri("illum-bg.jpg"), print_bg="#1B2A4A",
    tile_small_op=0, tile_big_op=0, band_op=0, ground_op=0, halo_mult=0, scrim_mult=0,
    hair1="#F0D8A0", hair2="#D8B870", hair3="#C6A055", hair4="#A9853E", hair5="#8C6B2E",
    mark_grad="linear-gradient(176deg,#F8ECC8 0%,#E0BE72 30%,#B8862E 62%,#F0D8A0 82%,#C6A055 100%)",
    # no mark_backing needed — the hero arch cartouche panel already gives the
    # star/wordmark a solid navy ground to sit on.
    gold_grad="linear-gradient(178deg,#FFFFFF 0%,#FFFFFF 100%)",
    # opaque cartouche panels now carry the contrast, so text just needs a
    # crisp hairline + a light lift, not the heavy outline needed when it
    # sat directly on the busy photo — that combination was reading as
    # solid black on the bigger, longer lines (body copy) instead of white.
    outline_stroke="0.6px #000000",
    ayah="#FFFFFF", gloss="#FFFFFF", t2="#FFFFFF", lab="#FFFFFF", val="#FFFFFF",
    body="#FFFFFF", pt="#FFFFFF", pd="#FFFFFF", rn="#FFFFFF", vsub="#FFFFFF",
    addr="#FFFFFF", wa="#FFFFFF", note="#FFFFFF", url="#FFFFFF",
    val_size="38px", pt_size="34px", body_weight=600, val_weight=600, pd_weight=600,
    addr_weight=600, wa_weight=600,
    text_shadow="0 1px 3px rgba(0,0,0,.6)",
    gold_shadow="drop-shadow(0 1px 2px rgba(0,0,0,.4))",
    seal_shadow="drop-shadow(0 2px 4px rgba(0,0,0,.4))",
    wordmark_shadow="drop-shadow(0 2px 4px rgba(0,0,0,.4))",
    ayah_shadow="none", med_shadow="none",
    # opaque "inscription panels" behind every text zone, shaped like the
    # manuscript's own vocabulary (the mihrab arch, a cusped cartouche bar)
    # rather than plain boxes — see hero_arch_panel()/cartouche_bar() above.
    cartouche_fill="rgba(8,12,36,.88)", cartouche_edge="#D8B870",
    cartouche_zones=[
        dict(shape="arch", base_y=812),
        dict(shape="bar", cx=CX, cy=907, w=820, h=110),
        dict(shape="bar", cx=CX, cy=1046, w=1080, h=150),
        dict(shape="bar", cx=CX, cy=1288, w=1080, h=187),
        dict(shape="bar", cx=CX, cy=1462, w=950, h=145),
        dict(shape="bar", cx=CX, cy=1606, w=700, h=140),
        dict(shape="bar", cx=CX, cy=1707, w=440, h=45),
    ],
)

if __name__ == "__main__":
    render(DEFAULT_PALETTE, "final-gold")
    render(EMERALD, "final-emerald")
    render(BURGUNDY, "final-burgundy")
    render(INDIGO, "final-indigo")
    render(BLACKGOLD, "final-blackgold")
    render(EARTHY, "final-earthy")
    render(SANDSTONE, "final-sandstone")
    render(ILLUMINATED, "final-illuminated")
