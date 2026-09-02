# The chosen layout, in four colourways

The building silhouette is gone — this reverts to the order's own ten-point
star mark, in the halo of 99 tasbih marks, filling the arch where the
silhouette used to sit. Everything else (ayah, title, Arabic wordmark, date,
programme, venue, WhatsApp, footer) is unchanged from the layout that was
approved.

| File | Palette | Pattern |
|---|---|---|
| `final-gold.png` | Lamplight Gold — the original warm umber and gold | Khatim star-and-cross |
| `final-emerald.png` | Emerald Court — deep forest green, gold ornament | Khatim star-and-cross |
| `final-burgundy.png` | Royal Burgundy — deep wine red, gold ornament | Diamond lattice (mashrabiya) |
| `final-indigo.png` | Midnight Indigo — deep navy, **silver** ornament instead of gold | Khatim star-and-cross |
| `final-blackgold.png` | Black & Gold — true black ground; frame, star and headings stay gold, body copy turns white | Khatim star-and-cross |
| `final-earthy.png` | Earthy Gold — Black & Gold with the neutral black swapped for a warm terracotta-clay dark; every gold and white token is untouched | Khatim star-and-cross |
| `banner-<colour>.png` | The banner (1600×900, `banner.py`), redone as a crest — star, wordmark, name and venue only, no date/time/WhatsApp — against a much denser Islamic geometric ground (a large faint rosette behind the star, a tiled dado border). Rendered in all six palettes: gold, emerald, burgundy, indigo, blackgold, earthy. |
| `banner-blackgold.png` | Black & Gold only, further customised: the full street address under the venue name (bold, 24px), two **solid** gold minaret silhouettes with punched-through windows and their own glow (`minaret_group()`), a **crescent** moon (SVG mask, one circle subtracted from another) beside the left tower, and "A brothers-only gathering" dropped from the footer while the site URL stays. |

Indigo is the one structural departure: every gold token (hairlines, the
star's own gradient, all text) is swapped for a cool silver/platinum
palette, since gold over navy reads muddy — silver was the correct call,
not just a hue-shift.

## How the colourways work

`final.py` builds the whole poster — CSS, geometry, layout — from one
`palette` dict of named colour tokens (`hair1`…`hair5`, `rule`, the gold/mark
gradients, every text class, the scrim tone, pattern opacities). A colourway
is just a dict that overrides some of those keys; `render()` regenerates the
full HTML from any palette with no other changes.

`pattern` selects between two generated motifs — `"zellij"` (the eight-point
khatim star-and-cross used everywhere else in this project) and
`"lattice"` (a plainer nested-diamond trellis, added here for the "and
patterns" half of the brief). Burgundy uses lattice at a deliberately low
opacity — at full strength it read as a checked fabric rather than
stonework; gold, emerald and indigo keep the khatim pattern.

## Regenerating

```bash
python3 final.py
```

Renders all four. To add a colourway, copy one of the palette dicts near
the bottom of the file, override the tokens that should change, and add a
`render(...)` call.
