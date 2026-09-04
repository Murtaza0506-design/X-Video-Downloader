#!/usr/bin/env python3
"""Typeset the paperback interior from content/*.md.

    python3 scripts/build_print.py                # 5.5 x 8.5 in, the default
    python3 scripts/build_print.py --trim 6x9     # 6 x 9 in

The book is set as two documents and then bound together, because the front
matter counts in roman and the body starts again at 1, and CSS cannot restart
a page counter mid-document. The body is set first, its page numbers are read
back off the rendered pages, and the contents is then set with those numbers
already in it.

Writes print/interior.pdf and print/SPECS.json. Run build_print_cover.py after
this: the spine is measured from the page count this produces.
"""
import argparse
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import (parse_chapters, build_index, front_matter,
                        blocks_to_html)

OUT = "print"

# The three fields nobody but the publisher can supply. Fill them in and
# rebuild; nothing else in the book needs touching.
IMPRINT = {
    "author":    "Murtaza Raza",   # the byline on the title page and the cover
    "publisher": "",          # an imprint name, or "" for none
    "isbn":      "",          # 13 digits, or "" to leave the line out
    "year":      "2026",
    "edition":   "First edition",
}

TITLE = "Lines Worth Keeping"

TRIMS = {
    "5.5x8.5": dict(w=5.5, h=8.5, top=0.72, bot=0.71, inn=0.80, out=0.60,
                    body=10.5, lead=14.6, name="5.5 x 8.5 in (139.7 x 215.9 mm)"),
    "6x9":     dict(w=6.0, h=9.0, top=0.80, bot=0.78, inn=0.85, out=0.65,
                    body=11.0, lead=15.4, name="6 x 9 in (152.4 x 228.6 mm)"),
}


# ---------------------------------------------------------------- text ----
def smart(text):
    """Typographic punctuation. The manuscript is written with typewriter
    marks; a printed page wants the real ones."""
    t = text.replace("...", "…")
    t = re.sub(r'(^|[\s(\[{])"', r"\1“", t)        # opening double
    t = t.replace('"', "”")                        # anything left closes
    t = re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "’", t)   # don't, isn't
    t = re.sub(r"(?<=[A-Za-z])'(?=\s|$|[.,;:!?)])", "’", t)  # plurals
    t = re.sub(r"(^|[\s(\[{])'", r"\1‘", t)        # opening single
    return t


def esc(s):
    return html.escape(smart(s), quote=False)


def strip_heading(body):
    lines = body.strip().split("\n")
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    return "\n".join(lines)


def prose(text):
    return blocks_to_html(smart(strip_heading(text)))


def note_html(body):
    """The attribution note keeps its subheadings and its lists."""
    out, buf = [], []

    def flush():
        if buf:
            out.append(blocks_to_html(smart("\n".join(buf))))
            del buf[:]

    for line in strip_heading(body).split("\n"):
        if line.startswith("## "):
            flush()
            out.append("<h3>%s</h3>" % esc(line[3:].strip()))
        else:
            buf.append(line)
    flush()
    return "".join(out)


def dropcap(html_prose):
    """Set the first letter of the opening paragraph as a two-line initial."""
    m = re.match(r"<p>(\W*)(\w)", html_prose)
    if not m:
        return html_prose
    pre, letter = m.group(1), m.group(2)
    return ('<p><span class="dropcap">%s%s</span>' % (pre, letter)
            + html_prose[m.end():])


def quote_html(e):
    q = esc(e["quote"])
    if e["bare"]:
        return '<p class="entry__quote">%s</p>' % q
    return '<p class="entry__quote">“%s”</p>' % q


def css(cfg):
    s = open(os.path.join("scripts", "print_style.css")).read()
    for k, v in {"__TRIM_W__": cfg["w"], "__TRIM_H__": cfg["h"],
                 "__M_TOP__": cfg["top"], "__M_BOT__": cfg["bot"],
                 "__M_IN__": cfg["inn"], "__M_OUT__": cfg["out"],
                 "__BODY_PT__": cfg["body"], "__LEAD_PT__": cfg["lead"],
                 "__TRIM_NAME__": cfg["name"],
                 "__BOOK_TITLE__": TITLE}.items():
        s = s.replace(k, str(v))
    return s


def page(title, body, cfg, cls=""):
    return ("<!doctype html>\n<html lang=\"en-GB\"><head><meta charset=\"utf-8\">"
            "<title>%s</title><style>\n%s\n</style></head>"
            "<body class=\"%s\">%s</body></html>"
            % (html.escape(title), css(cfg), cls, body))


# ---------------------------------------------------------------- body ----
def group_parts(chapters):
    parts, seen = [], {}
    for ch in chapters:
        if ch["part"] not in seen:
            seen[ch["part"]] = {"roman": ch["partRoman"], "name": ch["partName"],
                                "chs": []}
            parts.append(seen[ch["part"]])
        seen[ch["part"]]["chs"].append(ch)
    return parts


def body_html(chapters, index, intro, note, cfg):
    h = []
    a = h.append

    a('<section class="chapter" id="intro">'
      '<div class="chap-open"><p class="eyebrow">Before you begin</p>'
      '<h2>How to Use This Book</h2><hr class="hr"></div>'
      '<div class="chap-prose">%s</div></section>' % dropcap(intro))

    for p in group_parts(chapters):
        a('<section class="part-open"><p class="r">%s</p>'
          '<p class="n">%s</p><hr class="hr"></section>'
          % (p["roman"], esc(p["name"]).upper()))
        for ch in p["chs"]:
            e = ['<section class="chapter" id="c%d">' % ch["n"]]
            e.append('<div class="chap-open"><p class="eyebrow">Chapter %d</p>'
                     '<h2>%s</h2><hr class="hr"></div>' % (ch["n"], esc(ch["title"])))
            e.append('<div class="chap-prose">%s</div>' % dropcap(ch["opening"]))
            for i, en in enumerate(ch["entries"]):
                e.append(
                    '<div class="entry%s" id="e%d"><hr class="sep">'
                    '<div class="entry__head"><p class="entry__n">%03d</p>%s'
                    '<p class="entry__attr">%s</p></div>'
                    '<div class="gloss"><p class="gloss__label">What it means</p>'
                    '<p>%s</p></div>'
                    '<div class="gloss"><p class="gloss__label">How to use it</p>'
                    '<p>%s</p></div></div>'
                    % (" first" if i == 0 else "", en["n"], en["n"],
                       quote_html(en), esc(en["attribution"]),
                       esc(en["means"]), esc(en["use"])))
            e.append('</section>')
            a("".join(e))

    a('<section class="chapter note" id="note">'
      '<div class="chap-open"><p class="eyebrow">End matter</p>'
      '<h2>A Note on Attribution</h2><hr class="hr"></div>'
      '<div class="chap-prose">%s</div></section>' % note)

    idx = ['<section class="chapter index" id="index">'
           '<div class="chap-open"><p class="eyebrow">End matter</p>'
           '<h2>Index of Sources</h2><hr class="hr"></div>',
           '<div class="index-body">']
    letter, first = None, True
    for src in index:
        if src["letter"] != letter:
            letter = src["letter"]
            idx.append('<p class="letter%s">%s</p>'
                       % (" first" if first else "",
                          "Proverbs and traditional sayings"
                          if letter == "¶" else esc(letter)))
            first = False
        pages = "".join('<a class="pg" href="#e%d"></a>' % i["n"]
                        for i in src["items"])
        idx.append('<p class="index-src">%s&nbsp;&nbsp;%s</p>'
                   % (esc(src["name"]), pages))
    idx.append('</div></section>')
    a("".join(idx))

    a('<section class="colophon"><p class="mark">❧</p><p>%s</p>'
      '<p>Three hundred and fifteen entries across twenty-one chapters,<br>'
      'drawn from a hundred and fifty-one sources.</p>'
      '<p>Set in EB Garamond, cut by Octavio Pardo<br>'
      'after the types of Claude Garamont and Robert Granjon.</p>'
      '</section>' % esc(TITLE))

    return page(TITLE, "".join(h), cfg)


# --------------------------------------------------------------- front ----
def front_html(chapters, folio, cfg):
    h = []
    a = h.append
    a('<section class="display halftitle"><h1>%s</h1></section>' % esc(TITLE))
    a('<section class="blank verso"></section>')

    # the byline sits with the title; the foot of the page is the publisher's
    a('<section class="display titlepage">'
      '<p class="tp-title">Lines Worth<br>Keeping</p><hr class="tp-rule">'
      '<p class="tp-sub">A commonplace book of 315 quotations,<br>'
      'each with what it means and where to put it.</p>%s%s</section>'
      % ('<p class="tp-by">%s</p>' % esc(IMPRINT["author"])
         if IMPRINT["author"] else "",
         '<p class="tp-foot">%s</p>' % esc(IMPRINT["publisher"])
         if IMPRINT["publisher"] else ""))

    cr = ["<p>%s</p>" % esc(TITLE)]
    cr.append("<p>Copyright © %s%s. All rights reserved.</p>"
              % (IMPRINT["year"],
                 " " + esc(IMPRINT["author"]) if IMPRINT["author"] else ""))
    cr.append("<p>The moral right of the compiler has been asserted. No part of "
              "this book may be reproduced or transmitted in any form without "
              "written permission, except for brief quotations in a review.</p>")
    cr.append("<p>The quotations collected here are drawn overwhelmingly from "
              "material out of copyright. Lines from writers still in copyright "
              "are quoted briefly and with attribution, as fair dealing for the "
              "purposes of criticism and review. Attributions have been checked "
              "against primary sources where those exist; where a line is "
              "disputed, paraphrased or traditional it is marked as such in the "
              "text and in the note on attribution at the back. The commentary "
              "is original.</p>")
    if IMPRINT["isbn"]:
        cr.append("<p>ISBN %s</p>" % esc(IMPRINT["isbn"]))
    if IMPRINT["publisher"]:
        cr.append("<p>%s</p>" % esc(IMPRINT["publisher"]))
    cr.append("<p>%s</p>" % esc(IMPRINT["edition"]))
    cr.append("<p>Set in EB Garamond. Printed and bound on demand.</p>")
    a('<section class="copyright"><div class="cr-top">%s</div></section>'
      % "".join(cr))

    def row(href, num, title, cls=""):
        return ('<span class="toc-row %s"><span class="n">%s</span>'
                '<span class="p">%s</span><span class="t">%s</span></span>'
                % (cls, num, folio.get(href, ""), esc(title)))

    # The contents runs to two pages. Break it at whichever part boundary
    # comes nearest the middle, so the second page is not a stub.
    parts = group_parts(chapters)
    rows = [1] + [len(p["chs"]) for p in parts] + [2]
    total = sum(rows)
    cuts = [(abs(sum(rows[:i + 1]) - total / 2.0), i) for i in range(1, len(parts))]
    cut = min(cuts)[1] if cuts else -1

    toc = ['<h2 class="fm-head">Contents</h2>',
           row("intro", "", "How to Use This Book")]
    for i, p in enumerate(parts):
        toc.append('<p class="toc-part%s">Part %s · %s</p>'
                   % (" cut" if i == cut else "", p["roman"], esc(p["name"])))
        for ch in p["chs"]:
            toc.append(row("c%d" % ch["n"], str(ch["n"]), ch["title"]))
    toc.append('<p class="toc-part">End matter</p>')
    toc.append(row("note", "", "A Note on Attribution"))
    toc.append(row("index", "", "Index of Sources"))
    a('<section class="contents">%s</section>' % "".join(toc))
    return page(TITLE, "".join(h), cfg)


# ---------------------------------------------------------------- main ----
def render(html_text, path):
    from weasyprint import HTML
    doc = HTML(string=html_text, base_url=os.path.abspath(OUT) + "/").render()
    doc.write_pdf(path, pdf_version="1.7")
    return doc


def anchor_pages(doc):
    out = {}
    for i, pg in enumerate(doc.pages, start=1):
        for name in pg.anchors:
            out.setdefault(name, i)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trim", default="5.5x8.5", choices=sorted(TRIMS))
    args = ap.parse_args()
    cfg = TRIMS[args.trim]
    os.makedirs(OUT, exist_ok=True)

    chapters = parse_chapters()
    index = build_index(chapters)
    _, intro_body = front_matter(open("content/00-introduction.md").read())
    _, note_body = front_matter(open("content/90-note-on-attribution.md").read())

    body = body_html(chapters, index, prose(intro_body), note_html(note_body), cfg)
    open(os.path.join(OUT, "body.html"), "w").write(body)
    bdoc = render(body, os.path.join(OUT, "_body.pdf"))
    folio = {k: str(v) for k, v in anchor_pages(bdoc).items()}
    body_pages = len(bdoc.pages)

    front = front_html(chapters, folio, cfg)
    open(os.path.join(OUT, "front.html"), "w").write(front)
    fdoc = render(front, os.path.join(OUT, "_front.pdf"))
    front_pages = len(fdoc.pages)

    # The front matter must fill whole leaves, so that page 1 of the body falls
    # on a recto; the body must too, so the book ends on a verso.
    from pypdf import PdfReader, PdfWriter
    w = PdfWriter()
    fr, bo = PdfReader(os.path.join(OUT, "_front.pdf")), PdfReader(
        os.path.join(OUT, "_body.pdf"))
    for p in fr.pages:
        w.add_page(p)
    pad_front = front_pages % 2
    if pad_front:
        w.add_blank_page(width=cfg["w"] * 72, height=cfg["h"] * 72)
    for p in bo.pages:
        w.add_page(p)
    pad_back = body_pages % 2
    if pad_back:
        w.add_blank_page(width=cfg["w"] * 72, height=cfg["h"] * 72)

    meta = {"/Title": TITLE,
            "/Subject": "A commonplace book of 315 quotations",
            "/Creator": "WeasyPrint", "/Producer": "WeasyPrint"}
    if IMPRINT["author"]:
        meta["/Author"] = IMPRINT["author"]
    w.add_metadata(meta)
    pdf = os.path.join(OUT, "interior.pdf")
    with open(pdf, "wb") as fh:
        w.write(fh)
    for tmp in ("_front.pdf", "_body.pdf"):
        os.remove(os.path.join(OUT, tmp))

    total = front_pages + pad_front + body_pages + pad_back
    entries = sum(len(c["entries"]) for c in chapters)
    specs = {
        "trim": args.trim, "trim_name": cfg["name"],
        "trim_w_in": cfg["w"], "trim_h_in": cfg["h"],
        "margin_top_in": cfg["top"], "margin_bottom_in": cfg["bot"],
        "margin_inside_in": cfg["inn"], "margin_outside_in": cfg["out"],
        "text_block_w_in": round(cfg["w"] - cfg["inn"] - cfg["out"], 3),
        "text_block_h_in": round(cfg["h"] - cfg["top"] - cfg["bot"], 3),
        "body_pt": cfg["body"], "leading_pt": cfg["lead"],
        "front_pages": front_pages + pad_front, "body_pages": body_pages + pad_back,
        "pages": total, "chapters": len(chapters), "entries": entries,
        "sources": len(index), "bytes": os.path.getsize(pdf),
    }
    json.dump(specs, open(os.path.join(OUT, "SPECS.json"), "w"), indent=2)
    print("interior.pdf  %d pages (%d front + %d body)  %.2f MB  %s"
          % (total, specs["front_pages"], specs["body_pages"],
             specs["bytes"] / 1e6, cfg["name"]))


if __name__ == "__main__":
    main()
