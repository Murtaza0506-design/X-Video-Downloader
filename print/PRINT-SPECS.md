# Lines Worth Keeping — print specification

Paperback, perfect bound, black-and-white interior, full-colour wrap cover.
Everything below is measured off the files in this folder, not estimated.

Files to send a printer:

| File | What it is | Size | Pages |
|---|---|---|---|
| `interior.pdf` | the book block | 5.5 × 8.5 in | 236 |
| `cover-cream.pdf` | wrap cover for **cream** stock | 11.84 × 8.75 in | 1 |
| `cover-white.pdf` | wrap cover for **white** stock | 11.7815 × 8.75 in | 1 |

Send the interior and **one** cover: the one matching the paper you choose.
The two covers differ only in spine width, because the two papers are
different thicknesses.

---

## 1. Interior

### Page

| | |
|---|---|
| Trim size | **5.5 × 8.5 in** — 139.7 × 215.9 mm — 396 × 612 pt |
| Page count | **236** (even, as a bound book must be) |
| Bleed | **none**. Nothing runs to the edge, so the block is supplied at trim size with no bleed and no crop marks |
| Orientation | portrait, single pages, **not** spreads, in reading order |
| Colour | **black only**, verified neutral on every sampled page (max channel spread 0/255) |
| PDF version | 1.7 |
| File size | 725 KB |

### Margins

Mirrored: odd pages are right-hand pages and carry the wide margin at the spine.

| | inches | mm |
|---|---|---|
| Inside (gutter) | **0.80** | 20.3 |
| Outside | **0.60** | 15.2 |
| Top | **0.72** | 18.3 |
| Bottom | **0.71** | 18.0 |
| Text block | **4.10 × 7.07** | 104.1 × 179.6 |

The gutter is set for a 236-page perfect-bound book. Amazon KDP requires a
minimum of 0.75 in inside for 301–500 pages and 0.5 in for 151–300; at 0.80 in
this clears both with room to spare, so the same file is safe if the page count
moves. Outside, top and bottom all clear the 0.25 in minimum by more than
double.

### Type

| | |
|---|---|
| Text face | **EB Garamond** (Octavio Pardo, SIL Open Font License 1.1) |
| Body | 10.5 pt on 14.6 pt leading |
| Measure | 4.10 in, about 65 characters |
| Setting | justified, hyphenated (en-GB), 2-line widow and orphan control |
| Figures | old-style, proportional |
| Quotation | 13 pt on 16.6 pt, ranged left |
| Attribution | 10 pt italic |
| Gloss | 10 pt on 13.5 pt, with 7.6 pt letterspaced small-cap labels |
| Chapter title | 21 pt medium, centred |
| Running head | 8 pt letterspaced caps — book title on versos, chapter title on rectos |
| Folio | 9.5 pt, centred in the bottom margin |
| Fonts | **four faces embedded and subset** — regular, medium, semibold, italic. Nothing relies on the printer having anything |

### Structure

Front matter, 6 pages, numbered in lower-case roman, folios printed only
where a folio belongs:

| Page | |
|---|---|
| i | half title |
| ii | blank |
| iii | title page |
| iv | copyright and permissions |
| v–vi | contents, with real page numbers |

Body, 230 pages, numbered in arabic from 1:

- How to Use This Book (introduction)
- Part I · Yourself — chapters 1–6
- Part II · Other People — chapters 7–13
- Part III · The Work — chapters 14–19
- Part IV · The Long View — chapters 20–21
- A Note on Attribution
- Index of Sources — 151 sources, alphabetical, two columns, real page numbers
- Colophon

Every part title and every chapter opens on a **right-hand page**. Blank versos
created by those breaks carry no running head and no folio, which is correct
and is checked automatically. Chapter openers carry a folio but no running
head.

### Content

315 entries · 21 chapters · 151 sources. Each entry is a quotation, an
attribution, what it means, and how to use it. Entry numbers run 001–315
continuously and the index points at them by page.

---

## 2. Cover

One flat wrap: back cover, spine and front cover on a single page, printed in
colour, laminated to the printer's usual finish (matte suits this design).

### Geometry

Spine width is page count × paper caliper. That is why there are two files.

| | cream | white |
|---|---|---|
| Caliper per leaf | 0.0025 in | 0.002252 in |
| **Spine** | **0.5900 in** (14.99 mm) | **0.5315 in** (13.50 mm) |
| **Full wrap** | **11.8400 × 8.7500 in** | **11.7815 × 8.7500 in** |
| In points | 852.48 × 630 pt | 848.27 × 630 pt |

The arithmetic, for cream: 5.5 + 0.5900 + 5.5 = 11.5900 in of printed cover, plus
0.125 in bleed on the left and right = 11.8400 in wide; 8.5 + 0.125 + 0.125 =
8.75 in tall.

| | |
|---|---|
| Bleed | **0.125 in on all four outer edges** (the background runs into it) |
| Safe margin | 0.25 in inside every trim edge; nothing that matters is closer |
| Spine text | title only, reading downwards, centred, clear of both spine folds by more than the 0.0625 in minimum |
| Barcode | a clear cream rectangle **2.0 × 1.2 in** is reserved in the lower outer corner of the back cover. Leave it empty and let the printer drop the barcode in, or place your own ISBN barcode there |
| Colour space | RGB. POD printers convert; if your printer demands CMYK, convert with US Web Coated (SWOP) and the board reads slightly darker |
| PDF version | 1.7 |

Spine text is only permitted by KDP at 100 pages or more. At 236 it is fine.

### Design

Oxblood board (#7C2A22 → #54180F), cream type (#F2EDE3), two hairline rules
inboard of the fore edge on the front, matching the digital edition's jacket.
The back carries the blurb and one complete specimen entry, so a reader can see
the shape of the thing before buying it.

---

## 3. What is still blank, and only you can fill it

Three fields are deliberately empty. They are all in one dictionary at the top
of `scripts/build_print.py`:

```python
IMPRINT = {
    "author":    "",     # a byline for the title page, or "" for none
    "publisher": "",     # an imprint name, or "" for none
    "isbn":      "",     # 13 digits, or "" to leave the line out
    "year":      "2026",
    "edition":   "First edition",
}
```

- **Author or compiler name.** The title page and copyright line currently
  carry none. The commentary is original work and should be credited.
- **ISBN.** KDP will give you a free one; if you want to sell outside KDP, buy
  your own. Print it on the copyright page and put its barcode in the reserved
  rectangle.
- **Imprint.** Optional, but a name on the copyright page looks like a book
  rather than a document.

Fill them in and rebuild. Nothing else needs touching.

---

## 4. Rebuilding

```bash
python3 scripts/build_print.py          # interior, 5.5 x 8.5 (default)
python3 scripts/build_print.py --trim 6x9
python3 scripts/build_print_cover.py    # covers, spine measured from the interior
python3 scripts/check_print.py          # preflight
```

Run them in that order: the cover reads the page count the interior produced,
so a change to the text changes the spine, and building the cover second keeps
the two in step. `check_print.py` fails loudly if they ever drift.

The interior is generated from `content/*.md`, the same manuscript the digital
edition is built from. There is no separate print copy to keep in sync.

### Preflight, last run

```
Preflight passed.
  interior : 236 pages at 5.5 x 8.5 in (139.7 x 215.9 mm), all geometry exact
  fonts    : 4 embedded, none loose
  ink      : inside the safe area on every page
  colour   : neutral throughout (max channel spread 0/255)
  cover    : white 848.27 x 630.00 pt, spine matches 236 leaves
  cover    : cream 852.48 x 630.00 pt, spine matches 236 leaves
```

---

## 5. Ordering notes

**Amazon KDP.** 5.5 × 8.5 in is a standard trim. Choose Black & White interior
on cream or white paper, matte cover. Upload `interior.pdf` and the matching
cover. KDP's previewer will re-derive the spine from the page count; it should
agree with the file to the thousandth of an inch.

**Lulu, IngramSpark, or a local printer.** Same files. Ingram wants a 0.125 in
bleed on the cover, which is what is there, and will ask for the spine width:
give them the figure for the paper they are using from the table above. If they
use a different caliper, change `PAPER` in `scripts/build_print_cover.py` and
rebuild the cover; the interior does not change.

**A proof first.** Order one physical copy before approving. The gutter is the
thing to check by eye: hold the book open at page 100 and confirm the inside
margin is comfortable. If it is tight, raise `inn` in the `TRIMS` table and
rebuild.
