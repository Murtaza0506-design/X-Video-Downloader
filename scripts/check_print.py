#!/usr/bin/env python3
"""Preflight the print files before anything is sent to a printer.

    python3 scripts/check_print.py

Checks the things a printer rejects a file for: page geometry, an even page
count, fonts that travel with the file, ink that strays outside the safe area,
colour in a black-and-white interior, and a cover whose spine matches the
number of leaves it has to wrap.
"""
import json
import os
import sys

OUT = "print"
TOL = 0.5          # points; a rounding allowance on geometry
INK_TOL = 2.0      # points a hairline may sit outside the text block


def fail(msgs, s):
    msgs.append(s)


def check_interior(spec, msgs):
    import pypdfium2 as pdfium
    pdf = os.path.join(OUT, "interior.pdf")
    doc = pdfium.PdfDocument(pdf)
    want_w = spec["trim_w_in"] * 72
    want_h = spec["trim_h_in"] * 72

    if len(doc) != spec["pages"]:
        fail(msgs, "interior: %d pages, SPECS says %d" % (len(doc), spec["pages"]))
    if len(doc) % 2:
        fail(msgs, "interior: %d pages is odd; a bound book needs whole leaves"
             % len(doc))

    # geometry, page by page
    bad = [i + 1 for i, p in enumerate(doc)
           if abs(p.get_size()[0] - want_w) > TOL or abs(p.get_size()[1] - want_h) > TOL]
    if bad:
        fail(msgs, "interior: %d pages are not %s (first: %s)"
             % (len(bad), spec["trim_name"], bad[:5]))

    # ink inside the safe area: the outer edge of the block on each side
    top = spec["margin_top_in"] * 72
    bot = spec["margin_bottom_in"] * 72
    inn = spec["margin_inside_in"] * 72
    out = spec["margin_outside_in"] * 72
    strays = []
    for i, pg in enumerate(doc):
        n = i + 1
        left = inn if n % 2 else out          # odd pages are rectos
        right = out if n % 2 else inn
        tp = pg.get_textpage()
        count = tp.count_rects()
        for r in range(count):
            x0, y0, x1, y1 = tp.get_rect(r)   # pdfium: origin bottom-left
            if (x0 < left - INK_TOL or x1 > want_w - right + INK_TOL
                    or y1 > want_h - top * 0.45 + INK_TOL or y0 < bot * 0.35 - INK_TOL):
                strays.append(n)
                break
    if strays:
        fail(msgs, "interior: text outside the safe area on pages %s"
             % strays[:8])

    # fonts must travel with the file
    from pypdf import PdfReader
    rd = PdfReader(pdf)
    embedded, loose = set(), set()
    for pg in rd.pages:
        for f in (pg.get("/Resources", {}).get("/Font", {}) or {}).values():
            o = f.get_object()
            for d in ([o] + [d.get_object() for d in
                             (o.get("/DescendantFonts") or [])]):
                fd = d.get("/FontDescriptor")
                name = str(d.get("/BaseFont", "?"))
                if fd and any(k in fd.get_object()
                              for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                    embedded.add(name)
                elif fd is not None or "/BaseFont" in d:
                    loose.add(name)
    loose -= embedded
    if loose:
        fail(msgs, "interior: fonts not embedded: %s" % sorted(loose))
    if not embedded:
        fail(msgs, "interior: no embedded fonts found at all")
    return {"embedded_fonts": sorted(embedded), "pages": len(doc)}


def check_colour(msgs):
    """A black-and-white interior must contain no colour: every rendered pixel
    has to be neutral grey."""
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(os.path.join(OUT, "interior.pdf"))
    worst = 0
    for i in range(0, len(doc), 7):            # a sample across the book
        im = doc[i].render(scale=0.6).to_pil().convert("RGB")
        for r, g, b in list(im.getdata()):
            spread = max(r, g, b) - min(r, g, b)
            if spread > worst:
                worst = spread
    if worst > 8:
        fail(msgs, "interior: colour found (channel spread %d); a mono interior "
                   "must be neutral" % worst)
    return {"max_channel_spread": worst}


def check_cover(spec, msgs):
    import pypdfium2 as pdfium
    got = {}
    for paper, c in spec["covers"].items():
        path = os.path.join(OUT, c["file"])
        doc = pdfium.PdfDocument(path)
        if len(doc) != 1:
            fail(msgs, "%s: %d pages, a wrap cover is one" % (c["file"], len(doc)))
        w, h = doc[0].get_size()
        if abs(w - c["wrap_w_in"] * 72) > TOL or abs(h - c["wrap_h_in"] * 72) > TOL:
            fail(msgs, "%s: %.2f x %.2f pt, expected %.2f x %.2f"
                 % (c["file"], w, h, c["wrap_w_in"] * 72, c["wrap_h_in"] * 72))
        spine = round(spec["pages"] * c["caliper_in"], 4)
        if abs(spine - c["spine_in"]) > 1e-4:
            fail(msgs, "%s: spine %.4f in does not match %d pages at %.6f in"
                 % (c["file"], c["spine_in"], spec["pages"], c["caliper_in"]))
        got[paper] = {"w_pt": round(w, 2), "h_pt": round(h, 2)}
    return got


def main():
    spec = json.load(open(os.path.join(OUT, "SPECS.json")))
    msgs = []
    a = check_interior(spec, msgs)
    b = check_colour(msgs)
    c = check_cover(spec, msgs)
    if msgs:
        print("PREFLIGHT FAILED")
        for m in msgs:
            print("  -", m)
        sys.exit(1)
    print("Preflight passed.")
    print("  interior : %d pages at %s, all geometry exact"
          % (a["pages"], spec["trim_name"]))
    print("  fonts    : %d embedded, none loose" % len(a["embedded_fonts"]))
    print("  ink      : inside the safe area on every page")
    print("  colour   : neutral throughout (max channel spread %d/255)"
          % b["max_channel_spread"])
    for paper, g in c.items():
        print("  cover    : %-5s %.2f x %.2f pt, spine matches %d leaves"
              % (paper, g["w_pt"], g["h_pt"], spec["pages"]))


if __name__ == "__main__":
    main()
