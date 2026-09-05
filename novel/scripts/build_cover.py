#!/usr/bin/env python3
"""Build the covers: a print wrap for each paper stock, and the Kindle JPG.

The front board is an office elevation drawn as a spreadsheet. Twelve lettered
columns, rows numbered from 32 as though the sheet has been scrolled, most
cells unlit, and one cell warm. The warm cell is F41.

Spine width is measured from novel/print/SPECS.json, so build_interior.py runs
first. Two wraps come out because white and cream stock have different calipers
and the wrap has to fit the book it goes round.

    python3 novel/scripts/build_cover.py
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOVEL = os.path.join(ROOT, "novel")
CF = "/root/.claude/skills/synced/49e167cc-cc89-4688-953f-6da1ab7a8fea_87725a8c-1a80-4e6a-b85a-768fa690fa6c/canvas-design/canvas-fonts"
PRINT_OUT = os.path.join(NOVEL, "print")
EBOOK_OUT = os.path.join(NOVEL, "ebook")

SPECS = json.load(open(os.path.join(PRINT_OUT, "SPECS.json")))
PAGES = SPECS["pages"]
TRIM_W, TRIM_H = SPECS["trim_w_in"], SPECS["trim_h_in"]

BLEED, SAFE = 0.125, 0.25
BARCODE_W, BARCODE_H = 2.0, 1.2
PAPER = {"white": 0.002252, "cream": 0.0025}

TITLE_1, TITLE_2 = "The", "Handover"
AUTHOR = "Murtaza Raza"
IMPRINT = "Hillfoot Press"

# The one cell that is not like the others.
GRID_COLS, GRID_ROWS, ROW_START = 12, 14, 32
LIT_COL, LIT_ROW = 6, 41          # F41
REF = "6/WEL/04"

BLURB = [
    "There were eleven days between the first alarming Tuesday and the night "
    "the electricity stopped. The country did not panic. Quietly, "
    "individually, deniably, it got a few tins in.",
    "Neil Cowie was an assistant category manager. He did crisps. He was on "
    "floor six arguing about eleven centimetres of shelf when the phones "
    "started going, and what he remembers about the walk home is that it was "
    "a beautiful day, and that some part of him was relieved.",
    "What follows is a farm above a beck, a laminated sheet of rules on a "
    "parlour door, twenty-one tablets, and a decision made round a kitchen "
    "table in November that turns out, fourteen months later, to have been "
    "based on something nobody had bothered to tell anybody.",
]
PULL = "It was never the bite. It has only ever been the dying."

INK = "#EDE8DC"
AMBER = "#E9A63F"
G1, G2 = "#111815", "#070B09"


def fonts_css():
    return f"""
@font-face {{ font-family: Display; src: url('file://{CF}/BigShoulders-Bold.ttf'); font-weight:700; }}
@font-face {{ font-family: Display; src: url('file://{CF}/BigShoulders-Regular.ttf'); font-weight:400; }}
@font-face {{ font-family: Clerk;   src: url('file://{CF}/GeistMono-Regular.ttf'); }}
@font-face {{ font-family: Text;    src: url('file://{CF}/WorkSans-Regular.ttf'); font-weight:400; }}
@font-face {{ font-family: Text;    src: url('file://{CF}/WorkSans-Italic.ttf'); font-style:italic; }}
"""


def ground(x, y, w, h):
    return (f'<div style="position:absolute;left:{x}in;top:{y}in;'
            f'width:{w}in;height:{h}in;'
            f'background:linear-gradient(168deg,{G1} 0%,{G2} 62%,#050806 100%);"></div>'
            f'<div style="position:absolute;left:{x}in;top:{y}in;'
            f'width:{w}in;height:{h}in;'
            f'background:radial-gradient(ellipse 135% 95% at 50% 26%,'
            f'rgba(237,232,220,0.034) 0%,rgba(237,232,220,0.010) 55%,'
            f'rgba(0,0,0,0) 78%);"></div>'
            f'<div style="position:absolute;left:{x}in;top:{y}in;'
            f'width:{w}in;height:{h}in;'
            f'background:linear-gradient(to bottom,rgba(0,0,0,0) 0%,'
            f'rgba(0,0,0,0.045) 58%,rgba(0,0,0,0.12) 80%,'
            f'rgba(0,0,0,0.26) 100%);"></div>')


def facade(cx, cy, s):
    """The elevation. cx, cy is the top-left of the cell matrix, in inches."""
    cw, ch = 0.145 * s, 0.180 * s          # a window is taller than it is wide
    gx, gy = 0.062 * s, 0.070 * s
    px, py = cw + gx, ch + gy
    letters = "ABCDEFGHIJKL"
    out = []

    # Column letters and row numbers: the clerk's voice, small enough to require intent.
    for c in range(GRID_COLS):
        out.append(
            f'<div style="position:absolute;left:{cx + c * px:.4f}in;'
            f'top:{cy - 0.175 * s:.4f}in;width:{cw:.4f}in;'
            f'font-family:Clerk;font-size:{4.6 * s:.2f}pt;color:rgba(237,232,220,0.30);'
            f'text-align:center;letter-spacing:0.04em;">{letters[c]}</div>')
    for r in range(GRID_ROWS):
        out.append(
            f'<div style="position:absolute;left:{cx - 0.30 * s:.4f}in;'
            f'top:{cy + r * py + ch * 0.30:.4f}in;width:{0.235 * s:.4f}in;'
            f'font-family:Clerk;font-size:{4.6 * s:.2f}pt;color:rgba(237,232,220,0.26);'
            f'text-align:right;">{ROW_START + r}</div>')

    # The occupied cells. Fixed pattern, not random: a building has floors, and
    # the lower ones hold more light than the upper ones.
    lit = {
        (0, 1), (0, 4), (0, 8), (1, 2), (1, 3), (1, 9), (2, 0), (2, 6), (2, 7),
        (3, 5), (3, 10), (4, 1), (4, 4), (4, 11), (5, 2), (5, 8), (6, 0),
        (6, 3), (6, 9), (7, 5), (7, 6), (7, 11), (8, 1), (8, 7), (8, 10),
        (9, 0), (9, 2), (9, 4), (9, 8), (10, 3), (10, 5), (10, 9), (10, 11),
        (11, 1), (11, 2), (11, 6), (11, 7), (11, 10), (12, 0), (12, 3),
        (12, 4), (12, 5), (12, 8), (12, 9), (12, 11), (13, 1), (13, 2),
        (13, 4), (13, 6), (13, 7), (13, 9), (13, 10),
    }
    # A handful burning harder than the rest, weighted to the lower floors.
    bright = {(2, 6), (5, 2), (7, 11), (9, 4), (10, 9), (11, 2), (12, 5),
              (12, 9), (13, 6)}
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            x, y = cx + c * px, cy + r * py
            if (r, c) in bright:
                fill = "rgba(237,232,220,0.150)"
            elif (r, c) in lit:
                fill = "rgba(237,232,220,0.072)"
            else:
                fill = "rgba(237,232,220,0.014)"
            out.append(
                f'<div style="position:absolute;left:{x:.4f}in;top:{y:.4f}in;'
                f'width:{cw:.4f}in;height:{ch:.4f}in;background:{fill};'
                f'border:{0.35 * s:.2f}pt solid rgba(237,232,220,0.075);'
                f'box-sizing:border-box;"></div>')

    # F41.
    lc, lr = letters.index("F"), LIT_ROW - ROW_START
    lx, ly = cx + lc * px, cy + lr * py
    out.append(
        f'<div style="position:absolute;left:{lx - 0.10 * s:.4f}in;top:{ly - 0.10 * s:.4f}in;'
        f'width:{cw + 0.20 * s:.4f}in;height:{ch + 0.20 * s:.4f}in;'
        f'background:radial-gradient(ellipse at 50% 50%,rgba(233,166,63,0.34) 0%,'
        f'rgba(233,166,63,0.10) 52%,rgba(233,166,63,0) 100%);"></div>')
    out.append(
        f'<div style="position:absolute;left:{lx:.4f}in;top:{ly:.4f}in;'
        f'width:{cw:.4f}in;height:{ch:.4f}in;background:{AMBER};'
        f'border:{0.35 * s:.2f}pt solid rgba(233,166,63,0.85);box-sizing:border-box;"></div>')

    # The hairline leader out to the coordinate, the way a plate labels a specimen.
    ex = cx + GRID_COLS * px - gx
    out.append(
        f'<div style="position:absolute;left:{lx + cw:.4f}in;'
        f'top:{ly + ch / 2:.4f}in;width:{ex - lx - cw + 0.30 * s:.4f}in;'
        f'height:0.4pt;background:rgba(233,166,63,0.42);"></div>')
    out.append(
        f'<div style="position:absolute;left:{ex + 0.36 * s:.4f}in;'
        f'top:{ly + ch / 2 - 0.052 * s:.4f}in;font-family:Clerk;'
        f'font-size:{5.0 * s:.2f}pt;color:rgba(233,166,63,0.78);'
        f'letter-spacing:0.10em;">{REF}</div>')
    return "".join(out)


def front(x, y, w, h):
    """The front board. Positions derive from the board, so print and Kindle
    ratios lay out from the same rules rather than being stretched."""
    s = w / 5.5
    m = 0.62 * s
    o = []
    o.append(f'<div style="position:absolute;left:{x + m:.4f}in;top:{y + 0.86 * h / 8.5:.4f}in;'
             f'font-family:Clerk;font-size:{6.4 * s:.2f}pt;letter-spacing:0.50em;'
             f'color:rgba(237,232,220,0.42);">A NOVEL</div>')
    o.append(f'<div style="position:absolute;left:{x + m:.4f}in;top:{y + 1.16 * h / 8.5:.4f}in;'
             f'font-family:Display;font-weight:400;font-size:{25 * s:.2f}pt;'
             f'letter-spacing:0.40em;color:rgba(237,232,220,0.72);'
             f'text-transform:uppercase;line-height:1;">{TITLE_1}</div>')
    o.append(f'<div style="position:absolute;left:{x + m - 0.035 * s:.4f}in;'
             f'top:{y + 1.55 * h / 8.5:.4f}in;'
             f'font-family:Display;font-weight:700;font-size:{78 * s:.2f}pt;'
             f'letter-spacing:0.012em;color:{INK};text-transform:uppercase;'
             f'line-height:0.94;">{TITLE_2}</div>')
    o.append(f'<div style="position:absolute;left:{x + m:.4f}in;top:{y + 2.60 * h / 8.5:.4f}in;'
             f'width:{0.86 * s:.4f}in;height:0.7pt;background:rgba(233,166,63,0.80);"></div>')

    cw, gx = 0.145 * s, 0.062 * s
    grid_w = GRID_COLS * (cw + gx) - gx
    cx = x + (w - grid_w) / 2 + 0.10 * s
    o.append(facade(cx, y + 3.34 * h / 8.5, s))

    o.append(f'<div style="position:absolute;left:{x + m:.4f}in;'
             f'top:{y + h - 0.92 * h / 8.5:.4f}in;font-family:Text;'
             f'font-size:{10.5 * s:.2f}pt;letter-spacing:0.34em;color:{INK};'
             f'text-transform:uppercase;">{AUTHOR}</div>')
    return "".join(o)


def back(x, y, w, h, spine_x):
    s = w / 5.5
    m = 0.68
    tw = w - 2 * m
    paras = "".join(
        f'<p style="margin:0 0 0.150in 0;font-family:Text;font-size:9.1pt;'
        f'line-height:1.62;color:rgba(237,232,220,0.88);">{p}</p>' for p in BLURB)
    o = [f'<div style="position:absolute;left:{x + m:.4f}in;top:{y + 0.86:.4f}in;'
         f'width:{tw:.4f}in;">'
         f'<div style="font-family:Text;font-style:italic;font-size:10.4pt;'
         f'line-height:1.50;color:{AMBER};margin-bottom:0.40in;">{PULL}</div>'
         f'{paras}'
         f'<div style="width:0.70in;height:0.6pt;background:rgba(237,232,220,0.30);'
         f'margin:0.30in 0 0.16in 0;"></div>'
         f'<div style="font-family:Clerk;font-size:6.2pt;letter-spacing:0.30em;'
         f'color:rgba(237,232,220,0.40);">FICTION &#183; {REF}</div>'
         f'</div>']

    # The printer drops a barcode into the lower outer corner of the back board.
    bx = spine_x - 0.34 - BARCODE_W
    by = y + h - 0.30 - BARCODE_H
    o.append(f'<div style="position:absolute;left:{bx:.4f}in;top:{by:.4f}in;'
             f'width:{BARCODE_W}in;height:{BARCODE_H}in;background:#FFFFFF;'
             f'opacity:0.93;"></div>')
    o.append(f'<div style="position:absolute;left:{x + m:.4f}in;'
             f'top:{y + h - 0.62:.4f}in;font-family:Clerk;font-size:6.4pt;'
             f'letter-spacing:0.26em;color:rgba(237,232,220,0.50);">'
             f'{IMPRINT.upper()}</div>')
    return "".join(o)


def spine(x, y, w, h):
    cy = y + h / 2
    o = [f'<div style="position:absolute;left:{x + w / 2 - h / 2:.4f}in;'
         f'top:{cy - w / 2:.4f}in;width:{h:.4f}in;height:{w:.4f}in;'
         f'transform:rotate(90deg);display:flex;align-items:center;'
         f'justify-content:center;line-height:1;">'
         f'<span style="font-family:Display;font-weight:700;font-size:11pt;'
         f'letter-spacing:0.10em;color:{INK};text-transform:uppercase;'
         f'line-height:1;">'
         f'{TITLE_1} {TITLE_2}</span>'
         f'<span style="width:0.55in;"></span>'
         f'<span style="font-family:Clerk;font-size:5.6pt;letter-spacing:0.22em;'
         f'color:rgba(237,232,220,0.62);text-transform:uppercase;'
         f'line-height:1;">{AUTHOR}</span>'
         f'</div>']
    return "".join(o)


def render(doc, w, h, path):
    from weasyprint import HTML
    page = (f'<html><head><meta charset="utf-8"><style>{fonts_css()}'
            f'@page {{ size:{w}in {h}in; margin:0; }} '
            f'body {{ margin:0; background:{G2}; }}</style></head>'
            f'<body>{doc}</body></html>')
    HTML(string=page).write_pdf(path)


def main():
    os.makedirs(EBOOK_OUT, exist_ok=True)
    out = []
    for stock, caliper in PAPER.items():
        sp = PAGES * caliper
        W = TRIM_W * 2 + sp + BLEED * 2
        H = TRIM_H + BLEED * 2
        back_x, spine_x, front_x = BLEED, BLEED + TRIM_W, BLEED + TRIM_W + sp
        doc = (ground(0, 0, W, H)
               + back(back_x, BLEED, TRIM_W, TRIM_H, spine_x)
               + spine(spine_x, BLEED, sp, TRIM_H)
               + front(front_x, BLEED, TRIM_W, TRIM_H))
        p = os.path.join(PRINT_OUT, f"cover-{stock}.pdf")
        render(doc, W, H, p)
        out.append(f"cover-{stock}.pdf  {W:.4f} x {H:.4f} in  "
                   f"spine {sp:.4f} in ({sp * 25.4:.2f} mm)")

    # Kindle: 1600 x 2560 is 1:1.6, which is not the paperback's ratio, so the
    # front board is laid out again to that shape rather than stretched.
    KW, KH = 1600 / 300.0, 2560 / 300.0
    kp = os.path.join(EBOOK_OUT, "cover.pdf")
    render(ground(0, 0, KW, KH) + front(0, 0, KW, KH), KW, KH, kp)

    import pypdfium2 as pdfium
    from PIL import Image
    page = pdfium.PdfDocument(kp)[0]
    img = page.render(scale=300 / 72).to_pil().convert("RGB")
    img = img.resize((1600, 2560), Image.LANCZOS)
    jpg = os.path.join(EBOOK_OUT, "cover.jpg")
    img.save(jpg, "JPEG", quality=94, subsampling=0, dpi=(300, 300))
    img.save(os.path.join(EBOOK_OUT, "cover.png"), "PNG")
    os.remove(kp)
    out.append(f"cover.jpg  {img.size[0]} x {img.size[1]}  "
               f"{os.path.getsize(jpg) / 1024:.0f} KB")
    print("\n".join(out))


if __name__ == "__main__":
    main()
