#!/usr/bin/env python3
"""Typeset the novel as a 5.5 x 8.5 in paperback interior.

The novel is prose, not entries, so it does not go through the entry pipeline
in scripts/. Chapters are markdown: a level-one heading carrying the chapter
number in words, a level-two heading carrying the title, then paragraphs, with
a horizontal rule for a scene break.

    python3 novel/scripts/build_interior.py

Writes novel/print/interior.pdf and novel/print/SPECS.json. The page count in
SPECS.json is what sets the spine width on the cover, so this runs first.
"""
import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOVEL = os.path.join(ROOT, "novel")
FONTS = os.path.join(ROOT, "fonts")
OUT = os.path.join(NOVEL, "print")

TITLE = "The Handover"
AUTHOR = "Murtaza Raza"
IMPRINT = "Hillfoot Press"
YEAR = "2026"

TRIM_W, TRIM_H = 5.5, 8.5
# Gutter grows with the page count; at this extent KDP wants 0.75 in inside.
M_IN, M_OUT, M_TOP, M_BOT = 0.78, 0.58, 0.72, 0.70


def inline(text):
    """The small amount of markdown the manuscript actually uses."""
    out = html.escape(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", out)
    return out


def parse(path):
    num, title, blocks = None, None, []
    for raw in open(path).read().split("\n"):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("## "):
            title = line[3:].strip()
        elif line.startswith("# "):
            num = line[2:].strip()
        elif line == "---":
            blocks.append(("break", ""))
        else:
            blocks.append(("p", line))
    return {"num": num, "title": title, "blocks": blocks}


def chapter_html(ch, first):
    parts = ['<section class="chapter">',
             '<div class="opener">',
             f'<div class="chnum">{html.escape(ch["num"])}</div>',
             f'<h1>{html.escape(ch["title"])}</h1>',
             '</div>']
    lead, opening = True, True
    for kind, text in ch["blocks"]:
        if kind == "break":
            parts.append('<p class="scenebreak">&#183; &#183; &#183;</p>')
            lead = True
        else:
            classes = ["lead"] if lead else []
            attr = ""
            if opening:
                classes.append("chapterstart")
                attr = f' data-title="{html.escape(ch["title"])}"'
                opening = False
            cls = f' class="{" ".join(classes)}"' if classes else ""
            parts.append(f"<p{cls}{attr}>{inline(text)}</p>")
            lead = False
    parts.append("</section>")
    return "\n".join(parts)


def main():
    os.makedirs(OUT, exist_ok=True)
    files = sorted(f for f in glob.glob(os.path.join(NOVEL, "*.md"))
                   if re.match(r"\d\d-", os.path.basename(f)))
    chapters = [parse(f) for f in files]

    css = f"""
@font-face {{ font-family: Garamond; src: url('file://{FONTS}/EBGaramond-Regular.ttf'); font-weight: 400; }}
@font-face {{ font-family: Garamond; src: url('file://{FONTS}/EBGaramond-Italic.ttf'); font-style: italic; }}
@font-face {{ font-family: Garamond; src: url('file://{FONTS}/EBGaramond-SemiBold.ttf'); font-weight: 600; }}

@page {{
  size: {TRIM_W}in {TRIM_H}in;
  margin: {M_TOP}in {M_OUT}in {M_BOT}in {M_IN}in;
  @bottom-center {{
    content: counter(page);
    font-family: Garamond; font-size: 9pt; color: #000;
    margin-top: 0.16in;
  }}
}}
@page :left {{
  margin: {M_TOP}in {M_IN}in {M_BOT}in {M_OUT}in;
  @top-center {{
    content: string(booktitle);
    font-family: Garamond; font-size: 8.5pt; letter-spacing: 0.09em;
    text-transform: uppercase; color: #000; margin-bottom: 0.20in;
  }}
}}
@page :right {{
  @top-center {{
    content: string(chaptertitle);
    font-family: Garamond; font-size: 8.5pt; letter-spacing: 0.09em;
    text-transform: uppercase; color: #000; margin-bottom: 0.20in;
  }}
}}
/* No running head on a chapter's opening page. string() takes the first value
   set on the page, so the opener blanks it and the paragraph after the opener
   sets the real title, which then carries forward to the pages that follow. */
@page blank {{ @top-center {{ content: none; }} @bottom-center {{ content: none; }} }}

html {{ font-family: Garamond; font-size: 10.5pt; line-height: 15.1pt; color: #000; }}
body {{ margin: 0; hyphens: auto; }}

p {{ margin: 0; text-indent: 1.05em; text-align: justify; orphans: 2; widows: 2; }}
p.lead {{ text-indent: 0; }}
p.lead::first-letter {{ }}
em {{ font-style: italic; }}

p.scenebreak {{
  text-indent: 0; text-align: center; margin: 15.1pt 0; letter-spacing: 0.5em;
  font-size: 8pt; color: #444;
}}

section.chapter {{ break-before: right; }}
.opener {{ string-set: chaptertitle ""; }}
p.chapterstart {{ string-set: chaptertitle attr(data-title); }}
.opener {{ padding-top: 1.15in; margin-bottom: 0.42in; text-align: center; }}
.chnum {{
  font-size: 8.5pt; letter-spacing: 0.34em; text-transform: uppercase;
  color: #555; margin-bottom: 0.30in;
}}
.opener h1 {{
  font-size: 15pt; font-weight: 400; letter-spacing: 0.055em; margin: 0;
  text-transform: uppercase;
}}

/* Front matter */
.fm {{ break-after: page; page: blank; text-align: center; }}
.halftitle {{ padding-top: 3.1in; font-size: 12pt; letter-spacing: 0.30em;
  text-transform: uppercase; }}
.titlepage {{ padding-top: 2.35in; }}
.titlepage .t {{ font-size: 25pt; letter-spacing: 0.10em; text-transform: uppercase;
  line-height: 1.16; }}
.titlepage .rule {{ width: 1.05in; height: 0.5pt; background: #000; margin: 0.42in auto; }}
.titlepage .n {{ font-size: 8.5pt; letter-spacing: 0.34em; text-transform: uppercase;
  color: #555; }}
.titlepage .a {{ margin-top: 2.05in; font-size: 11pt; letter-spacing: 0.22em;
  text-transform: uppercase; }}
.copy {{ padding-top: 4.5in; font-size: 8.2pt; line-height: 1.62; color: #222; }}
.copy p {{ text-indent: 0; text-align: center; margin: 0 0 0.7em 0; }}
"""

    body = [
        '<div class="fm"><div class="halftitle">%s</div></div>' % html.escape(TITLE),
        '<div class="fm"><div class="titlepage">'
        f'<div class="t">{html.escape(TITLE)}</div>'
        '<div class="rule"></div>'
        '<div class="n">A Novel</div>'
        f'<div class="a">{html.escape(AUTHOR)}</div></div></div>',
        '<div class="fm"><div class="copy">'
        f'<p>{html.escape(TITLE)}</p>'
        f'<p>Copyright &#169; {YEAR} {html.escape(AUTHOR)}</p>'
        '<p>This is a work of fiction. Names, characters, places, organisations '
        'and incidents are the product of the author&#8217;s imagination or are '
        'used fictitiously. Any resemblance to actual persons, living or dead, '
        'events or localities is entirely coincidental.</p>'
        '<p>Nothing in this book is medical, clinical or emergency guidance, and '
        'it should not be relied on as any of those things.</p>'
        '<p>All rights reserved.</p>'
        f'<p>{html.escape(IMPRINT)}</p></div></div>',
    ]
    for i, ch in enumerate(chapters):
        body.append(chapter_html(ch, i == 0))

    doc = (f'<html lang="en-GB"><head><meta charset="utf-8">'
           f'<style>{css}</style></head>'
           f'<body><span style="string-set: booktitle \'{TITLE}\'"></span>'
           + "\n".join(body) + "</body></html>")

    from weasyprint import HTML
    pdf_path = os.path.join(OUT, "interior.pdf")
    HTML(string=doc, base_url=NOVEL).write_pdf(pdf_path)

    # A book block has to be an even number of leaves, so pad the last one.
    from pypdf import PdfReader, PdfWriter
    reader = PdfReader(pdf_path)
    if len(reader.pages) % 2:
        w = PdfWriter()
        for pg in reader.pages:
            w.add_page(pg)
        box = reader.pages[0].mediabox
        w.add_blank_page(width=float(box.width), height=float(box.height))
        with open(pdf_path, "wb") as fh:
            w.write(fh)
    pages = len(PdfReader(pdf_path).pages)
    words = sum(len(open(f).read().split()) for f in files)

    specs = {"title": TITLE, "author": AUTHOR, "trim_w_in": TRIM_W,
             "trim_h_in": TRIM_H, "pages": pages, "chapters": len(chapters),
             "words": words,
             "margins_in": {"inside": M_IN, "outside": M_OUT,
                            "top": M_TOP, "bottom": M_BOT}}
    json.dump(specs, open(os.path.join(OUT, "SPECS.json"), "w"), indent=2)
    print(f"interior.pdf  {pages} pages  {TRIM_W} x {TRIM_H} in  "
          f"{len(chapters)} chapters  {words:,} words")


if __name__ == "__main__":
    main()
