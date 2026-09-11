# Dar al-Dhikr — a Moroccan poster whose text *is* the design

## The problem this solves

A decorative background with translucent boxes laid over it always reads as two
separate things: a pattern, and some text sitting on top of it. The eye sees the
seam immediately — straight edges cutting through ornament, panels that could be
dragged anywhere without the design noticing.

This poster is built the other way round. There is no background and no text
boxes. There is a **wall**: a zellij border encloses a plaster field; a slender
arcade flanks a polylobed **mihrab niche**; and the niche is divided into
horizontal **registers** by gold interlace rules with khatim knots at their
centres. Every line of type lives in a register. Move a line and the architecture
has to move with it — which is exactly the relationship you want.

Three things do the work:

1. **The niche is cut, not pasted.** It casts a real shadow onto the plaster, its
   gold band is bevelled with a light and a shade rim, and its ground
   carries a faint tooled damask of the same eight-pointed seal used in the
   border. It reads as recessed stucco.
2. **The registers are stone courses.** Alternate courses are a few percent
   lighter, separated by gold rules that terminate in knots at the frame. The
   divisions are drawn *first*; the text is placed into them.
3. **Everything shares one vocabulary.** The khatim (eight-pointed seal) governs
   the border, the flanking columns, the divider knots, the corner seals, the
   damask — and the emblem, which is itself a khatim. The logo is not an import;
   it is the motif the whole page is made from.

## Two colourways

`THEME=rose` (the default) is the palette of the plate: a burnished gold sheet,
a rose zellij border, ivory plaster in the niche with a rose band and a lapis
pearl chain holding it, and a deep crimson boss behind the emblem. Type is
crimson and warm umber on ivory, which is how an illuminated page actually
works — dark ink on a light ground.

`THEME=indigo` is the night version: lapis ground, warm white type, turquoise
labels. Same architecture, same registers, same generator.

| file | what it is |
|---|---|
| `moroccan-poster.png` / `.pdf` | the finished poster, gold and rose, A3 at 300 dpi (3508 × 4961) |
| `moroccan-poster-blank.png` / `.pdf` | the same wall with every register empty |
| `moroccan-poster-indigo.png` / `.pdf` | the night colourway |
| `moroccan-poster-indigo-blank.png` / `.pdf` | and its blank |
| `moroccan-poster-guide.jpg` | the blank with each register boxed and measured |
| `moroccan.py` | the generator |
| `logo-khatim.png` | the emblem, re-cast in leaf gold at render time |
| `fonts/` | Cinzel, Cormorant Garamond, Marcellus, Amiri, Scheherazade New |

## Setting your own text

**The easy way** — edit `CONTENT` at the top of `moroccan.py` and re-render:

```bash
python3 moroccan.py                              # draft, gold and rose
THEME=rose   Q=2.0 PDF=1 python3 moroccan.py     # print quality
THEME=indigo Q=2.0 PDF=1 python3 moroccan.py     # the night colourway
BLANK=1 Q=2.0 PDF=1 python3 moroccan.py          # empty registers
GUIDE=1 BLANK=1 python3 moroccan.py              # measured overlay
```

Every block is auto-fitted: `fit_line` shrinks a headline until it fits its
register, `fit_block` wraps and shrinks a paragraph until it fits. Longer text
gets smaller rather than overflowing, so you cannot break the layout by typing.

**The other way** — open `moroccan-poster-blank.png` in Canva, Affinity, Word or
Illustrator and set type inside the boxes `moroccan-poster-guide.jpg` marks. The
register boxes, in final-image pixels at 3508 × 4961:

| register | x | y | size |
|---|---|---|---|
| quote (the ayah) | 1253 – 2254 | 420 – 732 | 85 × 26 mm |
| title | 826 – 2681 | 792 – 1481 | 157 × 58 mm |
| emblem | 628 – 2879 | 1542 – 2105 | 191 × 48 mm |
| date / time | 628 – 2880 | 2172 – 2465 | 191 × 25 mm |
| body | 628 – 2880 | 2528 – 2952 | 191 × 36 mm |
| programme | 628 – 2880 | 3015 – 3579 | 191 × 48 mm |
| venue | 628 – 2880 | 3641 – 3958 | 191 × 27 mm |
| contact | 628 – 2880 | 4023 – 4359 | 191 × 28 mm |
| web | 628 – 2880 | 4413 – 4549 | 191 × 12 mm |

The quote and title registers are narrower because they sit up inside the curve
of the arch — `niche_hw_at(y)` returns the real interior half-width at any
height, and the generator uses it so nothing can run into the haunch.

Centre each block in its box and keep to the type scale below; the dividers are
already drawn between them, so nothing needs a border of its own.

## Type

| role | face | rose colourway | indigo colourway |
|---|---|---|---|
| headline, venue | Cinzel 600, letterspaced | crimson `#7C1C28` | warm white `#FBF5E6` |
| figures, times | Cormorant Garamond 600 | crimson | warm white |
| body, notes | Cormorant Garamond 400 / italic | umber `#462E24` | warm white |
| small labels | Marcellus, widely letterspaced | rose `#963A3E` | turquoise `#7EC4C8` |
| Arabic | Amiri (Scheherazade New also supplied) | old gold `#92642C` | gold |

## Colour

**Rose** — burnished gold sheet `#B2824A` → `#FBF0D5` · rose `#DF8583` /
`#C06060` · crimson `#8A1E2A` / `#5C101C` · ivory `#FAF1DE` · lapis pearls
`#1A224C` · gold `#8C642C` / `#C49C50` / `#F4E2AC`.

**Indigo** — `#0E1A36` → `#26447A` · terracotta `#A23E2C` · turquoise `#166076` ·
tadelakt cream `#F2E7D0` · the same golds.

## The surface

The poster is finished as an object rather than a file. After the supersampled
render is brought down to size, `finish()`:

- **displaces everything by a hair** — a smooth random field of about two pixels,
  so no line is perfectly straight. This one step does more for the hand-made
  read than any amount of texture.
- lays a **paper tooth**, long **laid lines**, and a low-frequency **relief**
  whose gradient is lit from the upper left, so the sheet has a surface.
- **pools pigment at every edge** — a touch of darkening wherever the image
  changes, the way paint gathers where a brush stops.
- ages it slightly: uneven warmth, a little foxing.
- finishes with a raking light and a soft vignette.

The **border is cut, not printed**. Every piece is set by hand, so no two match:
each seal and cross gets its own tone, its own fraction of a degree of rotation,
and its own pixel or two of drift. Each sits in a darker joint, the whole course
is bevelled so the pieces stand proud of their bed, and the glaze crazes — but
only on the pieces, never on the plaster between them.

The gold is laid as **beaten leaf**: squares of about 70 mm, each with its own
tone, offset row by row, with the overlap at the seams catching the light and a
fine crazing through the size. The emblem is tinted from that same leaf rather
than a flat gradient, and the crimson ground behind it is ground pigment, not a
fill.

## Printing

A3 at 300 dpi as supplied. It scales to A2 at ~212 dpi and to A4 at 300 dpi with
no change. There is a 44-unit (3.7 mm) plain margin outside the outer gold rule, so
trimming is safe; the design does not bleed off the sheet.
