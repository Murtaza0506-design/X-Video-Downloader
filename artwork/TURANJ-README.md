# Turanj — the plate, opened out into a page that can be read

## What this is

`patient-gold-plate-I` is a closed object: one medallion, one reserved centre,
nothing to say. This takes the same illumination and opens it into a page.

The rule is the one that matters: **nothing is laid on top of the ornament.**
The writing lives in ground the illuminator reserved for it. One tall cusped
panel of ivory stands inside an illuminated border; the panel is crossed by
bands of the plate's own scrolling vine, and the reserves between those bands
are the registers. Move a line of type and a band has to move with it.

## How it is built, top to bottom

| element | what it does |
|---|---|
| burnished gold field | the sheet itself, marbled, full bleed |
| ruled margin | gold band between indigo keepers, the manuscript *jadval* |
| illuminated border | a cusped rose band carrying the full islimi vine — saz leaves, crimson rosettes, ivory blossoms, turquoise buds — drawn once per quadrant and mirrored fourfold, the way a pounced stencil works |
| *halkar* | gold-on-gold scroll in the bare ground between border and panel |
| the ivory panel | scalloped, gold-ruled, edged with a lapis pearl chain, sprinkled with *zarafshan* |
| three major bands | rose, lobed, tapered at the ends, each a run of the same vine |
| the *shamsa* | a sixteen-lobed seal riding its own band: a necklace of crimson rosettes and ivory blossoms around a crimson disc, the emblem in leaf gold at its centre |
| fine gold rules | where a band would shout — a hairline, a crimson lozenge, two gold stops |

Every boundary in the page is drawn: a fine ink contour, a gold rule outside it,
a lapis pearl chain inside. That is what keeps a text register from reading as a
box — it has the same edge treatment as the ornament, because it is made of the
same thing.

## Files

| file | what it is |
|---|---|
| `turanj-poster.png` / `.pdf` | the finished page, A3 at 300 dpi (3508 × 4961) |
| `turanj-poster-blank.png` / `.pdf` | every register empty |
| `turanj-poster-guide.jpg` | the blank with each register boxed and measured |
| `illuminated.py` | the generator |
| `generate.py` | the plate's motif engine — vine, leaf, blossom, rosette, pearls, grounds |
| `moroccan.py` | canvas, fonts, text fitting, and the emblem loader, shared |

## Setting your own text

Edit `CONTENT` near the top of `moroccan.py` — both posters read the same
dictionary — then:

```bash
python3 illuminated.py                     # draft
Q=2.0 PDF=1 python3 illuminated.py         # print quality
BLANK=1 Q=2.0 PDF=1 python3 illuminated.py
GUIDE=1 BLANK=1 python3 illuminated.py
```

Nothing can overflow. `set_lines` fits each line to its register and then
shrinks the whole stack together if the group is still too tall; `fit_block`
wraps and shrinks paragraphs. Long copy gets smaller, it does not spill.

To change how much room a register gets, edit `SEQ` in `illuminated.py`. The
numbers are relative weights, not fixed heights — `stack()` normalises them so
the registers, the bands and the rules fill the panel exactly. Add a register by
adding a `("b", "name", weight)` entry and a matching block in `typeset`; add a
band with `("M",)` or a hairline with `("m",)`.

## Type

| role | face | colour |
|---|---|---|
| headline, venue | Cinzel 600, letterspaced | crimson `#7C1C28` |
| figures, times | Cormorant Garamond 600 | crimson |
| body, address | Cormorant Garamond 400 | umber `#3E261E` |
| notes, subtitles | Cormorant Garamond italic | old gold `#926428` |
| small labels | Marcellus, widely letterspaced | rose `#963A3E` |
| Arabic | Amiri, shaped by Pillow's raqm backend | old gold / crimson |

## Colour

Gold `#8C642C` / `#C49C50` / `#F0DA9C` · rose `#E08584` / `#C06463` ·
crimson `#8C202C` / `#5E121E` · ivory `#F7F0E0` · lapis `#18204A` ·
sage `#7C9E76` · turquoise `#7CBEBC`.

## Printing

A3 at 300 dpi as supplied; scales to A2 at ~212 dpi or A4 at 300 with no change.
The ruled margin sits 54 units (4.5 mm) inside the sheet edge and the design does
not bleed, so trimming is safe.
