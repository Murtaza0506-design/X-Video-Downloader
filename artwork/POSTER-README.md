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
   gold band is bevelled with a light and a shade rim, and its indigo ground
   carries a faint tooled damask of the same eight-pointed seal used in the
   border. It reads as recessed stucco.
2. **The registers are stone courses.** Alternate courses are a few percent
   lighter, separated by gold rules that terminate in knots at the frame. The
   divisions are drawn *first*; the text is placed into them.
3. **Everything shares one vocabulary.** The khatim (eight-pointed seal) governs
   the border, the flanking columns, the divider knots, the corner seals, the
   damask — and the emblem, which is itself a khatim. The logo is not an import;
   it is the motif the whole page is made from.

## Files

| file | what it is |
|---|---|
| `moroccan-poster.png` / `.pdf` | the finished poster, A3 at 300 dpi (3508 × 4961) |
| `moroccan-poster-blank.png` / `.pdf` | the same wall with every register empty |
| `moroccan-poster-guide.png` | the blank with each register boxed and measured |
| `moroccan.py` | the generator |
| `logo-khatim.png` | the emblem, re-cast in leaf gold at render time |
| `fonts/` | Cinzel, Cormorant Garamond, Marcellus, Amiri, Scheherazade New |

## Setting your own text

**The easy way** — edit `CONTENT` at the top of `moroccan.py` and re-render:

```bash
python3 moroccan.py                    # draft
Q=2.0 PDF=1 python3 moroccan.py        # print quality
BLANK=1 Q=2.0 PDF=1 python3 moroccan.py
GUIDE=1 BLANK=1 python3 moroccan.py
```

Every block is auto-fitted: `fit_line` shrinks a headline until it fits its
register, `fit_block` wraps and shrinks a paragraph until it fits. Longer text
gets smaller rather than overflowing, so you cannot break the layout by typing.

**The other way** — open `moroccan-poster-blank.png` in Canva, Affinity, Word or
Illustrator and set type inside the boxes `moroccan-poster-guide.png` marks. The
register boxes, in final-image pixels at 3508 × 4961:

| register | x | y | size |
|---|---|---|---|
| quote (the ayah) | 833 – 2675 | 586 – 874 | 156 × 24 mm |
| title | 640 – 2868 | 930 – 1566 | 189 × 54 mm |
| emblem | 640 – 2868 | 1622 – 2142 | 189 × 44 mm |
| date / time | 640 – 2868 | 2204 – 2474 | 189 × 23 mm |
| body | 640 – 2868 | 2532 – 2924 | 189 × 33 mm |
| programme | 640 – 2868 | 2982 – 3502 | 189 × 44 mm |
| venue | 640 – 2868 | 3560 – 3852 | 189 × 25 mm |
| contact | 640 – 2868 | 3912 – 4222 | 189 × 26 mm |
| web | 640 – 2868 | 4272 – 4398 | 189 × 11 mm |

Centre each block in its box and keep to the type scale below; the dividers are
already drawn between them, so nothing needs a border of its own.

## Type

| role | face | colour |
|---|---|---|
| headline, venue | Cinzel 600, letterspaced | warm white `#FBF5E6` |
| figures, times | Cormorant Garamond 600 | warm white |
| body, notes | Cormorant Garamond 400 / italic | warm white, gold `#EED69C` |
| small labels | Marcellus, widely letterspaced | turquoise `#7EC4C8` |
| Arabic | Amiri (Scheherazade New also supplied) | gold |

## Colour

Indigo `#0E1A36` → `#26447A` · gold `#8C642C` / `#C49C50` / `#F4E2AC` ·
tadelakt cream `#F2E7D0` · terracotta `#A23E2C` · turquoise `#166076`.

## Printing

A3 at 300 dpi as supplied. It scales to A2 at ~212 dpi and to A4 at 300 dpi with
no change. There is a 74-unit (6 mm) plain margin outside the outer gold rule, so
trimming is safe; the design does not bleed off the sheet.
