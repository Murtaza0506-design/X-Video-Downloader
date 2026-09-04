# Lines Worth Keeping — Kindle specification

Reflowable EPUB 3 for Amazon Kindle Direct Publishing. Every figure below is
measured off the file in this folder.

Files to upload:

| File | What it is | Size |
|---|---|---|
| `lines-worth-keeping.epub` | the book | 248 KB |
| `cover.jpg` | the cover Amazon shows in the store | 1600 × 2560, 1:1.6 |

KDP takes the EPUB as the manuscript and the JPEG as the cover. The EPUB also
carries the cover internally, so it appears as the first page on the device.

---

## 1. The file

| | |
|---|---|
| Format | **EPUB 3.0**, reflowable |
| Documents | 33 XHTML files, one per chapter, plus front and back matter |
| Fonts | **none embedded**, on purpose. The reader chooses the typeface and the size, which is what Kindle readers expect and what the accessibility settings need |
| Layout | reflowable. No page size, no fixed positions, nothing pre-paginated |
| Language | en-GB |
| Identifier | a UUID, stable across re-uploads, so Amazon treats a new upload as a revision of the same book rather than a new one. Swap it for your ISBN if you buy one |
| Navigation | EPUB 3 `nav.xhtml` **and** a legacy `toc.ncx`, so older Kindle hardware gets a working table of contents too |
| Internal links | 408, every one of them resolving |

## 2. Structure

Cover · Title page · Copyright · Contents · How to Use This Book · four part
titles · 21 chapters · A Note on Attribution · Index of Sources · Colophon.

Two things are done differently from the paperback, because page numbers do
not exist on a Kindle:

- **The contents** links to each chapter instead of listing a page.
- **The index of sources** lists entry numbers instead of page numbers, and
  every number is a link straight to that entry. 151 sources, 315 links.

The device's own table of contents (the one under the menu button) is built
from the same list, with chapters nested under their parts.

## 3. Content

| | |
|---|---|
| Entries | **315** |
| Chapters | **21**, in four parts |
| Sources | **151** |
| Words | about 39,000, of which the quotations are 3,800 |

## 4. What is still blank

The same three fields as the paperback, in the same place, at the top of
`scripts/build_print.py`, shared by both editions:

```python
IMPRINT = {
    "author":    "",     # becomes dc:creator, and the byline on the title page
    "publisher": "",     # becomes dc:publisher
    "isbn":      "",     # printed on the copyright page
    ...
}
```

`author` matters more here than in print: Amazon requires an author name on
the product page, and if `dc:creator` is empty you will have to type it into
the KDP form instead, where it will not match the file.

## 5. Rebuilding

```bash
python3 scripts/build_epub.py     # writes the EPUB and the cover JPEG
python3 scripts/check_epub.py     # preflight
```

Both editions are generated from `content/*.md`, the same manuscript as the
web edition and the paperback. Change a chapter and everything downstream
follows.

### Preflight, last run

```
EPUB preflight passed.
  container : mimetype stored and first, container.xml resolves
  package   : 37 manifest items, 33 in the spine, nothing orphaned
  documents : 34 XHTML files, all well formed
  links     : 408 internal links, all resolving
  cover     : 1600x2560 RGB, cover.jpg
  navigation: EPUB 3 nav plus 31 NCX points
  layout    : reflowable, no embedded fonts
```

## 6. Uploading to KDP

1. **Create a new Kindle eBook** at kdp.amazon.com. If you are also publishing
   the paperback, do the ebook first and then use *Create Paperback* from the
   same title, so the two are linked on one product page.
2. **Language** English. **Publishing rights**: you own the copyright in the
   commentary. The quotations are covered by the note on the copyright page.
3. **Categories.** Two are allowed. Self-Help > Motivational and Reference >
   Quotations are the obvious pair; Philosophy > Stoicism is a strong third if
   you get the option.
4. **Keywords.** Seven slots. Use phrases people search rather than words that
   describe the book: *stoic quotes daily*, *quotation book with explanations*,
   *what to say when*, *commonplace book*, *practical philosophy*, *quotes for
   difficult times*, *gift book quotations*.
5. **Upload** `lines-worth-keeping.epub` as the manuscript and `cover.jpg` as
   the cover. Do not use the Cover Creator; it will overwrite this design.
6. **Preview.** Open the online previewer and check three things: the cover
   appears first, the table of contents under the menu button lists all 21
   chapters, and a number in the index of sources jumps to the right entry.
7. **Pricing.** The 70% royalty band runs from £1.77 to £9.99 in the UK and
   $2.99 to $9.99 in the US. Below or above that band the royalty drops to 35%.
   A 315-entry reference book sits comfortably at the top of the band.
8. **KDP Select** is optional and locks you out of every other retailer for 90
   days at a time. Worth declining if you might sell the same file elsewhere.

## 7. Note on quality review

Amazon's automated review flags books whose content is freely available
elsewhere. The quotations here are, and the commentary is not. The numbers
are on your side: of roughly 39,000 words, the quoted lines account for 3,800,
under a tenth. The other 35,000 are original, and they are the reason to buy
it. If the review does query the book, that is the answer: the quotations are
source material and the commentary is the work, which is the position of every
annotated anthology ever published.
