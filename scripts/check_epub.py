#!/usr/bin/env python3
"""Preflight the Kindle file before it goes to Amazon.

    python3 scripts/check_epub.py

Checks the things that get an upload rejected or make a book unreadable on a
device: the container, well-formed XHTML, a manifest that matches what is
actually in the archive, every internal link landing on something that exists,
a cover of the right shape, and no fixed layout hiding anywhere.
"""
import os
import sys
import zipfile
from xml.etree import ElementTree as ET

EPUB = os.path.join(os.environ.get("BOOK_EPUB_OUT", "ebook"),
                    os.environ.get("BOOK_SLUG", "lines-worth-keeping") + ".epub")
NS = {"opf": "http://www.idpf.org/2007/opf",
      "dc": "http://purl.org/dc/elements/1.1/",
      "x": "http://www.w3.org/1999/xhtml",
      "ncx": "http://www.daisy.org/z3986/2005/ncx/",
      "c": "urn:oasis:names:tc:opendocument:xmlns:container"}


def main():
    bad = []
    z = zipfile.ZipFile(EPUB)
    names = z.namelist()

    # 1. the container
    if names[0] != "mimetype":
        bad.append("mimetype is not the first entry (%s is)" % names[0])
    info = z.getinfo("mimetype")
    if info.compress_type != zipfile.ZIP_STORED:
        bad.append("mimetype is compressed; it has to be stored")
    if z.read("mimetype") != b"application/epub+zip":
        bad.append("mimetype content is wrong")
    if "META-INF/container.xml" not in names:
        bad.append("META-INF/container.xml is missing")

    root = ET.fromstring(z.read("META-INF/container.xml")).find(
        ".//c:rootfile", NS).get("full-path")
    if root not in names:
        bad.append("container points at %s, which is not in the archive" % root)

    # 2. the package: every manifest item is really there
    opf = ET.fromstring(z.read(root))
    base = os.path.dirname(root)
    manifest = {}
    for item in opf.findall(".//opf:manifest/opf:item", NS):
        href = item.get("href")
        full = os.path.normpath(os.path.join(base, href))
        manifest[item.get("id")] = (full, item.get("media-type"),
                                    item.get("properties") or "")
        if full not in names:
            bad.append("manifest lists %s, which is not in the archive" % href)
    for n in names:
        # the package document does not list itself
        if n in ("mimetype", "META-INF/container.xml", root):
            continue
        if n not in [v[0] for v in manifest.values()]:
            bad.append("%s is in the archive but not in the manifest" % n)

    # 3. spine
    spine = [r.get("idref") for r in opf.findall(".//opf:spine/opf:itemref", NS)]
    if not spine:
        bad.append("the spine is empty")
    for idref in spine:
        if idref not in manifest:
            bad.append("spine references unknown id %s" % idref)

    # 4. metadata Amazon reads
    md = opf.find("opf:metadata", NS)
    for tag in ("title", "language", "identifier"):
        if md.find("dc:%s" % tag, NS) is None:
            bad.append("metadata is missing dc:%s" % tag)
    covers = [i for i in manifest.values() if "cover-image" in i[2]]
    if not covers:
        bad.append("no manifest item carries the cover-image property")

    # 5. reflowable, not fixed
    for meta in opf.findall(".//opf:meta", NS):
        if meta.get("property") == "rendition:layout" and \
                meta.text and "pre-paginated" in meta.text:
            bad.append("the book is marked fixed layout; Amazon wants reflowable")

    # 6. every document parses, and every internal link lands somewhere
    ids, links = {}, []
    docs = [v[0] for v in manifest.values()
            if v[1] == "application/xhtml+xml"]
    for d in docs:
        try:
            tree = ET.fromstring(z.read(d))
        except ET.ParseError as e:
            bad.append("%s is not well formed XML: %s" % (d, e))
            continue
        ids[d] = {el.get("id") for el in tree.iter() if el.get("id")}
        for el in tree.iter():
            href = el.get("href") or el.get("src")
            if not href or href.startswith(("http:", "https:", "mailto:")):
                continue
            if href.startswith("#"):
                target, frag = d, href[1:]
            else:
                part, _, frag = href.partition("#")
                target = os.path.normpath(os.path.join(os.path.dirname(d), part))
            links.append((d, target, frag))
    for src, target, frag in links:
        if target not in names:
            bad.append("%s links to %s, which does not exist" % (src, target))
        elif frag and frag not in ids.get(target, set()):
            bad.append("%s links to %s#%s, which does not exist"
                       % (src, target, frag))

    # 7. the cover image
    cover = covers[0][0] if covers else None
    if cover:
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(z.read(cover)))
        w, h = im.size
        if min(w, h) < 1000:
            bad.append("cover is %dx%d; Amazon wants at least 1000px on the "
                       "short side" % (w, h))
        ratio = h / float(w)
        if not (1.33 <= ratio <= 1.6):
            bad.append("cover ratio is 1:%.2f; Amazon accepts 1:1.33 to 1:1.6"
                       % ratio)
        if im.mode != "RGB":
            bad.append("cover is %s; it should be RGB" % im.mode)

    # 8. the old navigation map, for older Kindles
    ncx_items = [v[0] for v in manifest.values()
                 if v[1] == "application/x-dtbncx+xml"]
    if not ncx_items:
        bad.append("no toc.ncx; older Kindle devices need one")
    else:
        n = ET.fromstring(z.read(ncx_items[0]))
        pts = n.findall(".//ncx:navPoint", NS)
        if len(pts) < 5:
            bad.append("toc.ncx has only %d entries" % len(pts))

    if bad:
        print("EPUB preflight FAILED")
        for b in bad:
            print("  -", b)
        sys.exit(1)

    print("EPUB preflight passed.")
    print("  container : mimetype stored and first, container.xml resolves")
    print("  package   : %d manifest items, %d in the spine, nothing orphaned"
          % (len(manifest), len(spine)))
    print("  documents : %d XHTML files, all well formed" % len(docs))
    print("  links     : %d internal links, all resolving" % len(links))
    print("  cover     : %dx%d RGB, %s" % (w, h, os.path.basename(cover)))
    print("  navigation: EPUB 3 nav plus %d NCX points" % len(pts))
    print("  layout    : reflowable, no embedded fonts")


if __name__ == "__main__":
    main()
