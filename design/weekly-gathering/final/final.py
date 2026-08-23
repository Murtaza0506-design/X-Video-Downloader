#!/usr/bin/env python3
"""The chosen layout — arch, ayah, title, wordmark — with the order's own
   star mark (not a building) filling the arch, in a halo of 99 tasbih marks.
   A palette dict swaps the whole poster's colourway without touching layout."""
import pathlib, subprocess
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


def build_hero():
    MED_CY, R, SEAL_D = 656, 150, 252          # SEAL_D deliberately smaller than R —
    extra_body = f'<g class="med">{v.halo(CX, MED_CY, R)}</g>'  # daylight for the 99-mark ring
    hero = f'''
{ayah_block(90, 150)}
{title_block(258, 50, 56)}
{wordmark(420, 72)}
<div class="mark seal" style="top:{MED_CY-SEAL_D//2}px;width:{SEAL_D}px;height:{SEAL_D}px;
  -webkit-mask-image:url({v.STAR_URI});mask-image:url({v.STAR_URI})"></div>
'''
    return hero, extra_body


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
  background:{pal['bg1']},{pal['bg2']};
  font-kerning:normal;-webkit-font-smoothing:antialiased;}}
.layer{{position:absolute;inset:0;width:100%;height:100%}}
.grain{{position:absolute;inset:0;opacity:.05;mix-blend-mode:overlay;pointer-events:none;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4'/><feColorMatrix type='saturate' values='0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>");}}

.hair-1{{fill:none;stroke:{pal['hair1']};opacity:.97}}
.hair-2{{fill:none;stroke:{pal['hair2']};opacity:.85}}
.hair-3{{fill:none;stroke:{pal['hair3']};opacity:.80}}
.hair-4{{fill:none;stroke:{pal['hair4']};opacity:.75}}
.hair-5{{fill:none;stroke:{pal['hair5']};opacity:.55}}
.petal{{fill:{pal['petal']};stroke:{pal['petal_stroke']};opacity:.75}}
.petal-lit{{fill:{pal['petal_lit']};stroke:{pal['petal_lit_stroke']};opacity:.9}}
.dot{{fill:{pal['dot']}}}
.fill-lit{{fill:{pal['fill_lit']}}}
.fill-ink{{fill:#150E06}}
.stroke-node{{fill:none;stroke:{pal['stroke_node']};stroke-width:1}}
.rule{{stroke:{pal['rule']};stroke-width:1;opacity:.85}}
.rule-lit{{stroke:{pal['rule_lit']};stroke-width:1;opacity:.9}}
.ground{{opacity:.072}}
.zh{{stroke:{pal['zh']}}}
.zf{{stroke:{pal['zf']}}}
.zstud{{fill:{pal['zstud']}}}
.zb{{stroke:{pal['zb']}}}
.band{{opacity:.34}}
.tiles{{opacity:.20}}
.scrim{{position:absolute;inset:0;pointer-events:none;
  background:
    radial-gradient(62% 34% at 50% 21%, rgba({pal['scrim']},.64) 0%, rgba({pal['scrim']},.30) 58%, rgba({pal['scrim']},0) 100%),
    radial-gradient(72% 40% at 50% 61%, rgba({pal['scrim']},.70) 0%, rgba({pal['scrim']},.36) 55%, rgba({pal['scrim']},0) 100%),
    radial-gradient(64% 26% at 50% 87%, rgba({pal['scrim']},.68) 0%, rgba({pal['scrim']},.32) 58%, rgba({pal['scrim']},0) 100%);}}
.med{{filter:drop-shadow(0 0 16px rgba(230,192,116,.26))}}

.at{{position:absolute;left:0;right:0;text-align:center;
  text-shadow:0 1px 3px rgba(6,4,2,.72), 0 0 14px rgba(6,4,2,.45)}}
.mark{{position:absolute;left:50%;transform:translateX(-50%);
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;
  -webkit-mask-size:contain;mask-size:contain;
  -webkit-mask-position:center;mask-position:center;
  background-image:{pal['mark_grad']};}}
.seal{{filter:drop-shadow(0 0 20px rgba(232,194,116,.30)) drop-shadow(0 1px 1px rgba(0,0,0,.5))}}
.wordmark{{filter:drop-shadow(0 0 16px rgba(226,186,108,.24)) drop-shadow(0 1px 1px rgba(0,0,0,.55))}}
.gold{{background:{pal['gold_grad']};
  -webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 1px 0 rgba(0,0,0,.6)) drop-shadow(0 2px 5px rgba(6,4,2,.7))
         drop-shadow(0 0 20px rgba(214,172,100,.26))}}
.at.gold{{text-shadow:none}}
.ayah{{font-family:Amiri,serif;font-size:40px;line-height:1.55;color:{pal['ayah']};
  direction:rtl;filter:drop-shadow(0 0 16px rgba(214,172,100,.28))}}
.gloss{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:20.5px;
  letter-spacing:.055em;color:{pal['gloss']}}}
.t1{{font-family:Cinzel,serif;font-weight:600;font-size:50px;letter-spacing:.135em;
  text-indent:.135em;line-height:1}}
.t2{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:43px;
  letter-spacing:.045em;color:{pal['t2']}}}
.lab{{font-family:Cinzel,serif;font-weight:400;font-size:12.5px;letter-spacing:.5em;
  text-indent:.5em;color:{pal['lab']}}}
.val{{font-family:Cormorant,serif;font-weight:400;font-size:33px;letter-spacing:.075em;
  text-indent:.075em;color:{pal['val']}}}
.body{{font-family:Cormorant,serif;font-weight:400;font-size:24.5px;line-height:1.62;white-space:nowrap;
  letter-spacing:.022em;color:{pal['body']}}}
.body em{{font-style:italic;color:{pal['gloss']}}}
.pt{{font-variant-numeric:lining-nums;font-family:Cinzel,serif;font-weight:400;font-size:14.5px;letter-spacing:.16em;
  text-indent:.16em;color:{pal['pt']}}}
.pd{{font-family:Cormorant,serif;font-weight:400;font-size:21.5px;line-height:1.46;
  letter-spacing:.03em;color:{pal['pd']}}}
.rn{{font-family:Cinzel,serif;font-size:11.5px;letter-spacing:.34em;text-indent:.34em;color:{pal['rn']}}}
.venue{{font-family:Cinzel,serif;font-weight:600;font-size:39px;letter-spacing:.18em;text-indent:.18em}}
.vsub{{font-family:Cormorant,serif;font-style:italic;font-weight:300;font-size:23px;
  letter-spacing:.06em;color:{pal['vsub']}}}
.addr{{font-variant-numeric:lining-nums;font-feature-settings:'lnum' 1;font-family:Cormorant,serif;font-weight:400;font-size:24px;letter-spacing:.13em;
  text-indent:.13em;color:{pal['addr']};text-transform:uppercase}}
.wa{{font-variant-numeric:lining-nums;font-feature-settings:'lnum' 1;font-family:Cormorant,serif;font-weight:400;font-size:34.5px;letter-spacing:.1em;
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
      <stop offset="0%"   stop-color="{pal['halo0']}" stop-opacity="0.20"/>
      <stop offset="26%"  stop-color="{pal['halo1']}" stop-opacity="0.105"/>
      <stop offset="48%"  stop-color="{pal['halo2']}" stop-opacity="0.048"/>
      <stop offset="72%"  stop-color="{pal['halo3']}" stop-opacity="0.016"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#halo)"/>

  <g class="ground">{v.ground_rosette(CX, 1060, 720)}</g>

  {v.arch(0, "hair-5", 1.0)}
  {v.arch(11, "hair-5", 0.6)}

  {hero_extra}

  <!-- frame: a tiled band, the way a Moroccan wall carries its dado -->
  <defs>{band_pat}</defs>
  <path fill-rule="evenodd" fill="url(#{band_id})" style="opacity:{pal['band_op']}"
        d="M38,38 H{W-38} V{H-38} H38 Z M74,74 H{W-74} V{H-74} H74 Z"/>
  <rect x="38" y="38" width="{W-76}" height="{H-76}" class="hair-3" stroke-width="1.15" fill="none"/>
  <rect x="45" y="45" width="{W-90}" height="{H-90}" class="hair-5" stroke-width="0.6" fill="none"/>
  <rect x="74" y="74" width="{W-148}" height="{H-148}" class="hair-3" stroke-width="1.0" fill="none"/>
  <rect x="81" y="81" width="{W-162}" height="{H-162}" class="hair-5" stroke-width="0.6" fill="none"/>
  {v.corner(74,74,1,1,0.66)}{v.corner(W-74,74,-1,1,0.66)}{v.corner(74,H-74,1,-1,0.66)}{v.corner(W-74,H-74,-1,-1,0.66)}

  {v.rule(CX, v.ARCH_BASE, 350)}
  <line x1="{CX}" y1="{v.ARCH_BASE+34}" x2="{CX}" y2="{v.ARCH_BASE+128}" class="rule"/>

  {v.rule(CX, 1272, 350)}
  <rect x="{CX-322}" y="1444" width="644" height="152" rx="2" class="hair-3" stroke-width="1" fill="none"/>
  <rect x="{CX-315}" y="1451" width="630" height="138" rx="1" class="hair-5" stroke-width="0.6" fill="none"/>
  {v.lozenge(CX-322,1520,5,8,"fill-ink")}{v.lozenge(CX+322,1520,5,8,"fill-ink")}
  {v.lozenge(CX-322,1520,5,8,"stroke-node")}{v.lozenge(CX+322,1520,5,8,"stroke-node")}
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

def bottom_html():
    return f'''
<div class="at lab" style="top:{v.ARCH_BASE+32}px;left:{CX-350}px;width:340px">SATURDAY</div>
<div class="at val" style="top:{v.ARCH_BASE+58}px;left:{CX-350}px;width:340px">29 August 2026</div>
<div class="at lab" style="top:{v.ARCH_BASE+32}px;left:{CX+10}px;width:340px">EVENING</div>
<div class="at val" style="top:{v.ARCH_BASE+58}px;left:{CX+10}px;width:340px">7:00 – 9:00 pm</div>

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
'''

def render(pal, out_name, scale=1):
    hero, hero_extra = build_hero()
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Weekly Dhikr Gathering</title>
<style>{css(pal)}</style></head>
<body><div class="page">
{tiles_svg(pal)}
{frame_svg(pal, hero_extra)}
{hero}
{bottom_html()}
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

if __name__ == "__main__":
    render(DEFAULT_PALETTE, "final-gold")
    render(EMERALD, "final-emerald")
    render(BURGUNDY, "final-burgundy")
    render(INDIGO, "final-indigo")
