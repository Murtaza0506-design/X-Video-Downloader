#!/usr/bin/env python3
"""Build the wrap-around paperback cover from print/SPECS.json.

The spine is measured, not guessed: page count times the caliper of the paper
it is printed on. Two covers come out, one for white stock and one for cream,
because the two calipers differ and the wrap has to fit the book it goes round.

    python3 scripts/build_print_cover.py

Writes print/cover-white.pdf and print/cover-cream.pdf.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_print import IMPRINT

OUT = "print"
BLEED = 0.125          # trimmed off all four outer edges
SAFE = 0.25            # nothing that matters comes closer than this to a trim
BARCODE_W, BARCODE_H = 2.0, 1.2   # the box the printer drops the barcode into

# Caliper per leaf, in inches. Both are the printer's published figures for
# black-and-white interiors.
PAPER = {"white": 0.002252, "cream": 0.0025}

TITLE_1, TITLE_2 = "Lines Worth", "Keeping"
SUB = "A commonplace book of 315 quotations, each with what it means and where to put it."

BLURB = [
    "Most quotation books hand you a beautiful sentence and walk away. You read "
    "forty in a sitting, feel briefly elevated, and by Thursday you could not "
    "name one of them.",
    "This one is built the other way round. Every line arrives with two things: "
    "what it actually means, in plain English, and one specific place to put "
    "it. The row you are rehearsing in the car. The email you have not "
    "answered. The thing you keep not starting.",
    "Three hundred and fifteen entries, arranged by the problem you have rather "
    "than the century it came from. Marcus Aurelius on obstacles, Aesop on "
    "persuasion, an English proverb on knowing when to leave a thing alone. "
    "They contradict each other in places, which is what real advice does.",
]
PULL = ("Open it anywhere. Most chapters end by giving you permission to stop.")

# One entry, printed on the back board exactly as it is printed inside, so a
# reader can see the shape of the thing before buying it.
SPECIMEN = {
    "quote": "When angry, count to ten before you speak. If very angry, a hundred.",
    "attr": "Thomas Jefferson",
    "use": "Build the delay into the tools where you do the damage. Say out loud "
           "that you will answer tomorrow. Write the furious message in a blank "
           "note instead of the reply box.",
}


def cover_html(spec, paper):
    pages = spec["pages"]
    tw, th = spec["trim_w_in"], spec["trim_h_in"]
    spine = round(pages * PAPER[paper], 4)
    W = 2 * tw + spine + 2 * BLEED
    H = th + 2 * BLEED
    # the left edge of each panel, measured from the left edge of the wrap
    back_x = BLEED
    spine_x = BLEED + tw
    front_x = BLEED + tw + spine
    author = IMPRINT["author"] if IMPRINT.get("name_on_cover") else ""
    BYLINE = '<p class="by">%s</p>' % author if author else ""
    SPINE_BY = "<i>%s</i>" % author if author else ""

    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<title>Lines Worth Keeping — cover</title><style>
@font-face{{font-family:"EB Garamond";font-weight:400;font-style:normal;
  src:url("fonts/EBGaramond-Regular.ttf")format("truetype")}}
@font-face{{font-family:"EB Garamond";font-weight:500;font-style:normal;
  src:url("fonts/EBGaramond-Medium.ttf")format("truetype")}}
@font-face{{font-family:"EB Garamond";font-weight:600;font-style:normal;
  src:url("fonts/EBGaramond-SemiBold.ttf")format("truetype")}}
@font-face{{font-family:"EB Garamond";font-weight:400;font-style:italic;
  src:url("fonts/EBGaramond-Italic.ttf")format("truetype")}}
@page{{size:{W}in {H}in; margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;height:100%;
  font-family:"EB Garamond",Garamond,Georgia,serif;color:#F2EDE3}}
.wrap{{position:relative;width:{W}in;height:{H}in;
  background:linear-gradient(135deg,#7C2A22 0%,#6A2019 46%,#54180F 100%)}}
.panel{{position:absolute;top:0;height:{H}in}}
.back{{left:0;width:{BLEED + tw}in}}
.spine{{left:{spine_x}in;width:{spine}in}}
.front{{left:{front_x}in;width:{tw + BLEED}in}}

/* the front board, set like the jacket of the digital edition */
.front .pad{{position:absolute;top:{BLEED + SAFE}in;height:{H - 2*(BLEED+SAFE)}in;
  left:{SAFE + 0.46}in;right:{BLEED + SAFE + 0.1}in}}
.rule-v{{position:absolute;top:{BLEED + 0.5}in;height:{H - 2*BLEED - 1.0}in;
  left:{SAFE + 0.14}in;width:.5pt;background:rgba(242,237,227,.42)}}
.rule-v.inner{{left:{SAFE + 0.27}in;opacity:.55}}
.prick{{position:absolute;top:{BLEED + 0.62}in;height:{H - 2*BLEED - 1.24}in;
  right:{BLEED + SAFE + 0.02}in;width:.5pt;background:rgba(242,237,227,.3)}}
.eyebrow{{font-size:8.5pt;letter-spacing:.22em;text-transform:uppercase;
  opacity:.75;margin:0}}
.mid{{position:absolute;top:{(H - 2*(BLEED+SAFE)) * 0.40}in;left:0;right:.3in}}
.foot{{position:absolute;bottom:.12in;left:0}}
.title{{font-size:44pt;font-weight:500;line-height:.96;margin:0 0 .16in;
  letter-spacing:-.012em}}
.hr{{border:0;border-top:.7pt solid rgba(242,237,227,.62);width:1.55in;
  margin:0 0 .16in}}
.sub{{font-size:12pt;font-style:italic;line-height:1.42;margin:0;
  max-width:2.9in;opacity:.9}}
.by{{font-size:13pt;letter-spacing:.2em;text-transform:uppercase;
  margin:.32in 0 0;opacity:.95}}
.foot{{font-size:8.5pt;letter-spacing:.16em;text-transform:uppercase;opacity:.72;
  margin:0}}
.spec{{position:absolute;bottom:.34in;left:0;right:0;padding-top:.2in;
  border-top:.7pt solid rgba(242,237,227,.4)}}
.spec .q{{font-size:11.5pt;line-height:1.32;margin:0 0 .06in}}
.spec .a{{font-size:8.5pt;font-style:italic;opacity:.7;margin:0 0 .1in}}
.spec .g{{font-size:8.6pt;line-height:1.42;opacity:.85;margin:0}}
.spec .g b{{font-weight:600;letter-spacing:.11em;text-transform:uppercase;
  font-size:.85em;opacity:.75}}

/* the spine. The box is laid out long-side-horizontal and then turned a
   quarter clockwise, so the title reads downwards with the book face up. */
.spine .txt{{position:absolute;top:0;left:0;width:{H}in;height:{spine}in;
  transform:translateX({spine}in) rotate(90deg);transform-origin:0 0;
  display:flex;align-items:center;justify-content:center;
  font-size:{min(10.5, max(7, spine * 21)):.1f}pt;letter-spacing:.04em;
  white-space:nowrap;line-height:{spine}in}}
.spine .txt b{{font-weight:500}}
.spine .txt i{{font-style:normal;opacity:.82;letter-spacing:.14em;
  text-transform:uppercase;font-size:.72em;margin-left:.55in}}

/* the back board */
.back .pad{{position:absolute;top:{BLEED + SAFE + 0.15}in;
  left:{BLEED + SAFE + 0.1}in;right:{SAFE + 0.1}in;
  height:{H - 2*(BLEED+SAFE) - 0.15 - BARCODE_H - 0.3}in}}
.back .pull{{font-size:13pt;font-style:italic;line-height:1.34;margin:0 0 .22in;
  padding-bottom:.2in;border-bottom:.7pt solid rgba(242,237,227,.4)}}
.back p.b{{font-size:9.6pt;line-height:1.46;margin:0 0 .13in;opacity:.93;
  text-align:justify;hyphens:auto}}
.back .close{{font-size:10.5pt;font-style:italic;margin:.16in 0 0;opacity:.95}}
.back .tag{{position:absolute;bottom:0;left:0;font-size:8pt;letter-spacing:.18em;
  text-transform:uppercase;opacity:.66;margin:0}}
/* the printer prints the barcode into this box, so nothing else goes in it */
/* the printer drops the barcode into the lower outer corner of the back
   board, so that rectangle is left clear and pale */
.barcode{{position:absolute;right:{SAFE + 0.125}in;bottom:{BLEED + SAFE + 0.125}in;
  width:{BARCODE_W}in;height:{BARCODE_H}in;background:#F2EDE3;border-radius:2pt}}
</style></head><body>
<div class="wrap">
  <div class="panel back">
    <div class="pad">
      <p class="pull">{PULL}</p>
      {''.join('<p class="b">%s</p>' % p for p in BLURB)}
      <div class="spec">
        <p class="q">&#8220;{SPECIMEN['quote']}&#8221;</p>
        <p class="a">{SPECIMEN['attr']}</p>
        <p class="g"><b>How to use it&nbsp;&nbsp;</b>{SPECIMEN['use']}</p>
      </div>
      <p class="tag">315 entries · 21 chapters · 151 sources</p>
    </div>
    <div class="barcode"></div>
  </div>

  <div class="panel spine">
    <div class="txt"><b>{TITLE_1} {TITLE_2}</b>{SPINE_BY}</div>
  </div>

  <div class="panel front">
    <div class="rule-v"></div><div class="rule-v inner"></div><div class="prick"></div>
    <div class="pad">
      <p class="eyebrow">A commonplace book</p>
      <div class="mid">
        <p class="title">{TITLE_1}<br>{TITLE_2}</p>
        <hr class="hr">
        <p class="sub">{SUB}</p>
        {BYLINE}
      </div>
      <p class="foot">315 entries · 21 chapters</p>
    </div>
  </div>
</div>
</body></html>"""


def main():
    spec = json.load(open(os.path.join(OUT, "SPECS.json")))
    from weasyprint import HTML
    out = {}
    for paper in PAPER:
        html_text = cover_html(spec, paper)
        src = os.path.join(OUT, "cover-%s.html" % paper)
        open(src, "w").write(html_text)
        pdf = os.path.join(OUT, "cover-%s.pdf" % paper)
        HTML(filename=src).write_pdf(pdf, pdf_version="1.7")
        spine = round(spec["pages"] * PAPER[paper], 4)
        out[paper] = {
            "caliper_in": PAPER[paper],
            "spine_in": spine,
            "spine_mm": round(spine * 25.4, 2),
            "wrap_w_in": round(2 * spec["trim_w_in"] + spine + 2 * BLEED, 4),
            "wrap_h_in": round(spec["trim_h_in"] + 2 * BLEED, 4),
            "file": os.path.basename(pdf),
            "bytes": os.path.getsize(pdf),
        }
        print("cover-%s.pdf  %.4f x %.4f in  spine %.4f in (%.2f mm)"
              % (paper, out[paper]["wrap_w_in"], out[paper]["wrap_h_in"],
                 spine, out[paper]["spine_mm"]))
    spec["bleed_in"] = BLEED
    spec["safe_margin_in"] = SAFE
    spec["barcode_box_in"] = [BARCODE_W, BARCODE_H]
    spec["covers"] = out
    json.dump(spec, open(os.path.join(OUT, "SPECS.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
