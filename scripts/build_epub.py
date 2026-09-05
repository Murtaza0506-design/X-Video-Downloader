#!/usr/bin/env python3
"""Build the Kindle edition from content/*.md.

    python3 scripts/build_epub.py

Writes ebook/lines-worth-keeping.epub and ebook/cover.jpg.

The EPUB is reflowable, which is what Amazon wants: no page size, no embedded
fonts, no fixed positions, so the reader chooses the typeface and size and the
text sets itself to whatever screen it lands on. Page numbers mean nothing
there, so the contents and the index of sources link by entry number instead.
"""
import html
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_site import parse_chapters, build_index, front_matter, CONTENT
from build_print import (IMPRINT, TITLE, NOTE_TITLE, INDEX_TITLE, INTRO_TITLE, FONT_DIR, smart, esc, prose, note_html,
                         quote_html, group_parts, paras, GLOSS)

OUT = os.environ.get("BOOK_EPUB_OUT", "ebook")
LANG = "en-GB"
SUBTITLE = os.environ.get("BOOK_SUBTITLE",
                          "A commonplace book of 315 quotations, each with "
                          "what it means and where to put it.")

# A stable identifier, so that a re-upload is recognised as the same book
# rather than a new one. Replace it with your ISBN once you have one.
BOOK_ID = os.environ.get("BOOK_ID",
                         "urn:uuid:8f4b1e0a-2d77-5a3c-9c61-7f0c2a5d9b41")

CSS = """/* Reflowable: no fixed sizes, no embedded fonts, no page geometry.
   The reader picks the typeface and the size; this sets relationships only. */
body { margin: 0 5%; line-height: 1.5; text-align: justify;
       widows: 2; orphans: 2; -webkit-hyphens: auto; hyphens: auto; }
p { margin: 0; text-indent: 1.2em; }
p.first, p.noindent { text-indent: 0; }
em { font-style: italic; }
a { text-decoration: none; }

.eyebrow { text-align: center; font-size: 0.72em; letter-spacing: 0.16em;
           text-transform: uppercase; margin: 2em 0 1.2em; text-indent: 0; }
h2.chapter { text-align: center; font-size: 1.5em; font-weight: normal;
             line-height: 1.2; margin: 0 0 0.7em; text-indent: 0;
             page-break-after: avoid; }
h3 { font-size: 1em; margin: 1.6em 0 0.4em; text-indent: 0; text-align: left;
     page-break-after: avoid; }
hr.orn { border: 0; border-top: 1px solid currentColor; width: 3em;
         margin: 0 auto 1.6em; }
hr.sep { border: 0; border-top: 1px solid currentColor; width: 2.5em;
         margin: 2em auto; }
ul { margin: 0.4em 0 1em 1.2em; padding: 0; }
li { margin-bottom: 0.4em; text-align: left; }

.entry-n { font-size: 0.75em; letter-spacing: 0.12em; margin: 0 0 0.3em;
           text-indent: 0; }
.quote { font-size: 1.15em; line-height: 1.35; margin: 0 0 0.35em;
         text-indent: 0; text-align: left; }
.attr { font-style: italic; font-size: 0.9em; margin: 0 0 0.9em;
        text-indent: 0; text-align: left; }
.label { font-size: 0.7em; font-weight: bold; letter-spacing: 0.13em;
         text-transform: uppercase; margin: 0 0 0.2em; text-indent: 0;
         page-break-after: avoid; }
.gloss { margin: 0 0 1em; text-indent: 0; }
.v { text-align: left; text-indent: 0; margin: 0 0 0.55em; }

.part { text-align: center; margin-top: 25%; }
.part .r { font-size: 2.6em; margin: 0 0 0.4em; text-indent: 0; }
.part .n { font-size: 0.8em; letter-spacing: 0.2em; text-transform: uppercase;
           margin: 0; text-indent: 0; }

.title-block { text-align: center; margin-top: 18%; }
.title-block .t { font-size: 2em; line-height: 1.1; margin: 0 0 0.6em;
                  text-indent: 0; }
.title-block .s { font-style: italic; margin: 0 0 2.2em; text-indent: 0;
                  text-align: center; }
.title-block .by { letter-spacing: 0.22em; text-transform: uppercase;
                   font-size: 0.85em; margin: 0; text-indent: 0;
                   text-align: center; }
.copyright p { font-size: 0.82em; margin: 0 0 1em; text-indent: 0;
               text-align: left; }

ul.toc { list-style: none; margin: 0; padding: 0; }
ul.toc li { margin: 0 0 0.45em; text-indent: 0; text-align: left; }
ul.toc li.part-row { margin: 1.4em 0 0.6em; font-size: 0.78em;
                     letter-spacing: 0.16em; text-transform: uppercase;
                     text-align: center; }
nav ol { list-style: none; margin: 0; padding: 0; }
nav li { margin: 0 0 0.4em; }

.index-src { margin: 0 0 0.5em; text-indent: -1.2em; padding-left: 1.2em;
             font-size: 0.92em; text-align: left; }
.index-letter { font-size: 0.95em; letter-spacing: 0.14em;
                text-transform: uppercase; margin: 1.4em 0 0.5em;
                text-indent: 0; text-align: left; }
.colophon { text-align: center; margin-top: 30%; }
.colophon p { text-indent: 0; text-align: center; margin: 0 0 1em;
              font-size: 0.9em; }
"""


def xhtml(title, body):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s">\n'
            '<head><meta charset="utf-8"/><title>%s</title>'
            '<link rel="stylesheet" type="text/css" href="../style.css"/></head>\n'
            '<body>\n%s\n</body>\n</html>\n'
            % (LANG, LANG, html.escape(title), body))


def first_noindent(p):
    return p.replace("<p>", '<p class="first">', 1)


def section(eyebrow, title, opening, entries, sid):
    h = ['<section id="%s">' % sid,
         '<p class="eyebrow">%s</p>' % esc(eyebrow),
         '<h2 class="chapter">%s</h2>' % esc(title),
         '<hr class="orn"/>', opening]
    for i, en in enumerate(entries):
        if i:
            h.append('<hr class="sep"/>')
        h.append('<div id="e%d">' % en["n"])
        h.append('<p class="entry-n">%03d</p>' % en["n"])
        h.append(quote_html(en).replace('entry__quote', 'quote'))
        h.append('<p class="attr">%s</p>' % esc(en["attribution"]))
        h.append('<p class="label">%s</p>%s' % (esc(GLOSS[0]), paras(en["means"])))
        h.append('<p class="label">%s</p>%s' % (esc(GLOSS[1]), paras(en["use"])))
        h.append('</div>')
    h.append('</section>')
    return "\n".join(h)


def cover_jpeg(path):
    """A 1600 by 2560 cover, the shape Amazon asks for, drawn from the same
    design as the printed board."""
    W, H = 10.0, 16.0          # inches, a 1 to 1.6 rectangle
    byline = ('<p class="by">%s</p>' % html.escape(IMPRINT["author"])
              if IMPRINT["author"] and IMPRINT.get("name_on_cover") else "")
    page = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:"EB Garamond";font-weight:400;
  src:url("%(FONT)s/EBGaramond-Regular.ttf")format("truetype")}
@font-face{font-family:"EB Garamond";font-weight:500;
  src:url("%(FONT)s/EBGaramond-Medium.ttf")format("truetype")}
@font-face{font-family:"EB Garamond";font-weight:400;font-style:italic;
  src:url("%(FONT)s/EBGaramond-Italic.ttf")format("truetype")}
@page{size:%(W)sin %(H)sin;margin:0}
*{box-sizing:border-box}
html,body{margin:0;height:100%%;font-family:"EB Garamond",Garamond,serif;
  color:#F2EDE3}
.b{position:relative;width:%(W)sin;height:%(H)sin;
  background:linear-gradient(135deg,%(C1)s 0%%,%(C2)s 46%%,%(C3)s 100%%)}
.r1,.r2{position:absolute;top:1in;bottom:1in;width:1pt;
  background:rgba(242,237,227,.42)}
.r1{left:.72in}.r2{left:.96in;opacity:.55}
.pad{position:absolute;top:1.15in;bottom:1.15in;left:1.5in;right:1.1in}
.eyebrow{font-size:19pt;letter-spacing:.22em;text-transform:uppercase;
  opacity:.75;margin:0}
.mid{position:absolute;top:33%%;left:0;right:0}
.t{font-size:96pt;font-weight:500;line-height:.96;margin:0 0 .3in;
  letter-spacing:-.012em}
.hr{border:0;border-top:1.5pt solid rgba(242,237,227,.62);width:3in;
  margin:0 0 .3in}
.s{font-size:26pt;font-style:italic;line-height:1.42;margin:0;
  max-width:6in;opacity:.9}
.by{font-size:30pt;letter-spacing:.2em;text-transform:uppercase;
  margin:.75in 0 0;opacity:.95}
.f{position:absolute;bottom:0;left:0;font-size:19pt;letter-spacing:.16em;
  text-transform:uppercase;opacity:.72;margin:0}
</style></head><body><div class="b">
<div class="r1"></div><div class="r2"></div>
<div class="pad">
  <p class="eyebrow">%(EYEBROW)s</p>
  <div class="mid"><p class="t">%(TITLE)s</p><hr class="hr">
    <p class="s">%(SUB)s</p>%(BY)s</div>
  <p class="f">%(FOOT)s</p>
</div></div></body></html>""" % {
        "W": W, "H": H, "BY": byline, "FONT": FONT_DIR,
        "SUB": html.escape(SUBTITLE),
        "TITLE": "<br>".join(html.escape(x) for x in os.environ.get(
            "BOOK_TITLE_LINES", "Lines Worth|Keeping").split("|")),
        "EYEBROW": html.escape(os.environ.get("BOOK_EYEBROW", "A commonplace book")),
        "FOOT": html.escape(os.environ.get("BOOK_FOOT", "315 entries \u00b7 21 chapters")),
        "C1": os.environ.get("BOOK_C1", "#7C2A22"),
        "C2": os.environ.get("BOOK_C2", "#6A2019"),
        "C3": os.environ.get("BOOK_C3", "#54180F")}
    src = os.path.join(OUT, "cover.html")
    open(src, "w").write(page)
    from weasyprint import HTML
    pdf = os.path.join(OUT, "_cover.pdf")
    HTML(filename=src).write_pdf(pdf)
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(pdf)
    scale = 1600.0 / (W * 72)
    im = doc[0].render(scale=scale).to_pil().convert("RGB")
    im = im.resize((1600, 2560))
    im.save(path, "JPEG", quality=92, optimize=True)
    os.remove(pdf)
    return im.size


def build():
    chapters = parse_chapters()
    index = build_index(chapters)
    _, intro_body = front_matter(
        open(os.path.join(CONTENT, "00-introduction.md")).read())
    _, note_body = front_matter(
        open(os.path.join(CONTENT, "90-note-on-attribution.md")).read())
    parts = group_parts(chapters)

    # which file each entry lives in, so the index can point at it
    entry_file = {}
    for ch in chapters:
        for en in ch["entries"]:
            entry_file[en["n"]] = "ch%02d.xhtml" % ch["n"]

    docs = []        # (href, id, title, body, in_nav, nav_level)

    def add(href, ident, title, body, nav=None, level=1):
        docs.append((href, ident, title, body, nav, level))

    add("text/cover.xhtml", "cover-page", TITLE,
        '<div style="text-align:center;margin:0;padding:0">'
        '<img src="../images/cover.jpg" alt="%s" '
        'style="max-width:100%%;height:auto"/></div>' % html.escape(TITLE))

    add("text/title.xhtml", "title-page", "Title page",
        '<div class="title-block"><p class="t">%s</p><hr class="orn"/>'
        '<p class="s">%s</p>%s%s</div>'
        % (esc(TITLE), esc(SUBTITLE),
           '<p class="by">%s</p>' % esc(IMPRINT["author"])
           if IMPRINT["author"] else "",
           '<p class="noindent">%s</p>' % esc(IMPRINT["publisher"])
           if IMPRINT["publisher"] else ""),
        nav="Title page")

    cr = ["<p>%s</p>" % esc(TITLE),
          "<p>Copyright &#169; %s%s. All rights reserved.</p>"
          % (IMPRINT["year"],
             " " + esc(IMPRINT["author"]) if IMPRINT["author"] else ""),
          "<p>The moral right of the compiler has been asserted. No part of this "
          "book may be reproduced or transmitted in any form without written "
          "permission, except for brief quotations in a review.</p>",
          "<p>The quotations collected here are drawn overwhelmingly from material "
          "out of copyright. Lines from writers still in copyright are quoted "
          "briefly and with attribution, as fair dealing for the purposes of "
          "criticism and review. Attributions have been checked against primary "
          "sources where those exist; where a line is disputed, paraphrased or "
          "traditional it is marked as such in the text and in the note on "
          "attribution at the back. The commentary is original.</p>"]
    if IMPRINT["isbn"]:
        cr.append("<p>ISBN %s</p>" % esc(IMPRINT["isbn"]))
    if IMPRINT["publisher"]:
        cr.append("<p>%s</p>" % esc(IMPRINT["publisher"]))
    cr.append("<p>%s</p>" % esc(IMPRINT["edition"]))
    add("text/copyright.xhtml", "copyright-page", "Copyright",
        '<div class="copyright">%s</div>' % "".join(cr), nav="Copyright")

    # a contents page the reader can browse, separate from the device menu
    toc = ['<p class="eyebrow">Contents</p>', '<ul class="toc">',
           '<li><a href="intro.xhtml">%s</a></li>' % esc(INTRO_TITLE)]
    for p in parts:
        toc.append('<li class="part-row">Part %s &#183; %s</li>'
                   % (p["roman"], esc(p["name"])))
        for ch in p["chs"]:
            toc.append('<li><a href="ch%02d.xhtml">%d. %s</a></li>'
                       % (ch["n"], ch["n"], esc(ch["title"])))
    toc.append('<li class="part-row">End matter</li>')
    toc.append('<li><a href="note.xhtml">%s</a></li>' % esc(NOTE_TITLE))
    toc.append('<li><a href="sources.xhtml">%s</a></li>' % esc(INDEX_TITLE))
    toc.append('</ul>')
    add("text/contents.xhtml", "contents", "Contents", "\n".join(toc),
        nav="Contents")

    add("text/intro.xhtml", "intro", INTRO_TITLE,
        section("Before you begin", INTRO_TITLE,
                first_noindent(prose(intro_body)), [], "intro"),
        nav=INTRO_TITLE)

    for p in parts:
        pid = "part%s" % p["roman"]
        add("text/%s.xhtml" % pid, pid, "Part %s" % p["roman"],
            '<div class="part"><p class="r">%s</p><p class="n">%s</p></div>'
            % (p["roman"], esc(p["name"]).upper()),
            nav="Part %s &#183; %s" % (p["roman"], esc(p["name"])))
        for ch in p["chs"]:
            add("text/ch%02d.xhtml" % ch["n"], "ch%02d" % ch["n"], ch["title"],
                section("Chapter %d" % ch["n"], ch["title"],
                        first_noindent(ch["opening"]), ch["entries"],
                        "c%d" % ch["n"]),
                nav="%d. %s" % (ch["n"], esc(ch["title"])), level=2)

    add("text/note.xhtml", "note", NOTE_TITLE,
        section("End matter", NOTE_TITLE,
                first_noindent(note_html(note_body)), [], "note"),
        nav=NOTE_TITLE)

    idx = ['<section id="sources"><p class="eyebrow">End matter</p>',
           '<h2 class="chapter">' + esc(INDEX_TITLE) + '</h2><hr class="orn"/>',
           '<p class="first">The numbers are entry numbers, not pages, and every '
           'one of them is a link.</p>']
    letter = None
    for src in index:
        if src["letter"] != letter:
            letter = src["letter"]
            idx.append('<p class="index-letter">%s</p>'
                       % ("Proverbs and traditional sayings"
                          if letter == "¶" else esc(letter)))
        links = ", ".join('<a href="%s#e%d">%03d</a>'
                          % (entry_file[i["n"]], i["n"], i["n"])
                          for i in src["items"])
        idx.append('<p class="index-src">%s&#160;&#160;%s</p>'
                   % (esc(src["name"]), links))
    idx.append('</section>')
    add("text/sources.xhtml", "sources", INDEX_TITLE, "\n".join(idx),
        nav=INDEX_TITLE)

    entries = sum(len(c["entries"]) for c in chapters)
    add("text/colophon.xhtml", "colophon", "Colophon",
        '<div class="colophon"><p>&#10087;</p><p>%s</p>'
        '<p>%d entries across %d chapters,<br/>drawn from %d sources.</p></div>'
        % (esc(TITLE), entries, len(chapters), len(index)))

    return docs, entries, len(chapters), len(index)


def opf(docs):
    items, spine = [], []
    for href, ident, _t, _b, _n, _l in docs:
        items.append('<item id="%s" href="%s" media-type="application/xhtml+xml"/>'
                     % (ident, href))
        spine.append('<itemref idref="%s"/>' % ident)
    items.append('<item id="css" href="style.css" media-type="text/css"/>')
    items.append('<item id="cover-image" href="images/cover.jpg" '
                 'media-type="image/jpeg" properties="cover-image"/>')
    items.append('<item id="nav" href="nav.xhtml" '
                 'media-type="application/xhtml+xml" properties="nav"/>')
    items.append('<item id="ncx" href="toc.ncx" '
                 'media-type="application/x-dtbncx+xml"/>')
    creator = ('<dc:creator id="author">%s</dc:creator>' % esc(IMPRINT["author"])
               if IMPRINT["author"] else "")
    publisher = ('<dc:publisher>%s</dc:publisher>' % esc(IMPRINT["publisher"])
                 if IMPRINT["publisher"] else "")
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
            'unique-identifier="pub-id" xml:lang="%s">\n'
            '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            '<dc:identifier id="pub-id">%s</dc:identifier>\n'
            '<dc:title>%s</dc:title>\n'
            '<dc:language>%s</dc:language>\n'
            '%s%s'
            '<dc:description>%s</dc:description>\n'
            '<dc:rights>Copyright &#169; %s. All rights reserved.</dc:rights>\n'
            '<meta property="dcterms:modified">2026-09-04T00:00:00Z</meta>\n'
            '<meta name="cover" content="cover-image"/>\n'
            '</metadata>\n<manifest>\n%s\n</manifest>\n'
            '<spine toc="ncx">\n%s\n</spine>\n</package>\n'
            % (LANG, BOOK_ID, esc(TITLE), LANG, creator, publisher,
               esc(SUBTITLE),
               IMPRINT["year"] + (" " + esc(IMPRINT["author"])
                                  if IMPRINT["author"] else ""),
               "\n".join(items), "\n".join(spine)))


def nav_xhtml(docs):
    out = []
    for href, _i, _t, _b, label, level in docs:
        if not label:
            continue
        out.append('<li%s><a href="%s">%s</a></li>'
                   % (' class="sub"' if level > 1 else "", href, label))
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s">\n'
            '<head><meta charset="utf-8"/><title>Contents</title>'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
            '<body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>\n%s\n'
            '</ol></nav>\n'
            '<nav epub:type="landmarks" hidden="hidden"><ol>'
            '<li><a epub:type="cover" href="text/cover.xhtml">Cover</a></li>'
            '<li><a epub:type="toc" href="text/contents.xhtml">Contents</a></li>'
            '<li><a epub:type="bodymatter" href="text/intro.xhtml">Start</a></li>'
            '</ol></nav></body></html>\n'
            % (LANG, LANG, "\n".join(out)))


def ncx(docs):
    points, n = [], 0
    for href, ident, _t, _b, label, _l in docs:
        if not label:
            continue
        n += 1
        points.append('<navPoint id="np%d" playOrder="%d">'
                      '<navLabel><text>%s</text></navLabel>'
                      '<content src="%s"/></navPoint>' % (n, n, label, href))
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
            '<head><meta name="dtb:uid" content="%s"/>'
            '<meta name="dtb:depth" content="1"/>'
            '<meta name="dtb:totalPageCount" content="0"/>'
            '<meta name="dtb:maxPageNumber" content="0"/></head>\n'
            '<docTitle><text>%s</text></docTitle>\n<navMap>\n%s\n</navMap>\n</ncx>\n'
            % (BOOK_ID, esc(TITLE), "\n".join(points)))


def main():
    os.makedirs(OUT, exist_ok=True)
    jpg = os.path.join(OUT, "cover.jpg")
    size = cover_jpeg(jpg)
    docs, entries, nch, nsrc = build()

    path = os.path.join(OUT, os.environ.get("BOOK_SLUG",
                                            "lines-worth-keeping") + ".epub")
    with zipfile.ZipFile(path, "w") as z:
        # the mimetype must be first and stored, not deflated
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0" encoding="utf-8"?>\n'
                   '<container version="1.0" '
                   'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" '
                   'media-type="application/oebps-package+xml"/></rootfiles>'
                   '</container>\n', zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf(docs), zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav_xhtml(docs), zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/toc.ncx", ncx(docs), zipfile.ZIP_DEFLATED)
        z.write(jpg, "OEBPS/images/cover.jpg", zipfile.ZIP_DEFLATED)
        for href, _i, title, body, _n, _l in docs:
            z.writestr("OEBPS/" + href, xhtml(title, body), zipfile.ZIP_DEFLATED)

    kb = os.path.getsize(path) / 1024
    print("%s  %d documents  %.0f KB" % (os.path.basename(path), len(docs), kb))
    print("cover.jpg  %d x %d" % size)
    print("%d entries, %d chapters, %d sources" % (entries, nch, nsrc))


if __name__ == "__main__":
    main()
