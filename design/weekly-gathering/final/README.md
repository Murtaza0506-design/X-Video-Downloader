# The chosen layout, in four colourways

The building silhouette is gone — this reverts to the order's own ten-point
star mark, in the halo of 99 tasbih marks, filling the arch where the
silhouette used to sit. Everything else (ayah, title, Arabic wordmark, date,
programme, venue, WhatsApp, footer) is unchanged from the layout that was
approved.

The body copy now reads as a standing notice for the tariqa's regular
members, not an invitation for newcomers to "experience" the practice:
*"The tariqa's weekly Moroccan dhikr, held for its regular members. Guided
remembrance, recited with idhn (spiritual permission), in the company of
those walking the path of spiritual refinement."* — shared by every
colourway, `bottom_html()` in `final.py`.

| File | Palette | Pattern |
|---|---|---|
| `final-gold.png` | Lamplight Gold — the original warm umber and gold | Khatim star-and-cross |
| `final-emerald.png` | Emerald Court — deep forest green, gold ornament | Khatim star-and-cross |
| `final-burgundy.png` | Royal Burgundy — deep wine red, gold ornament | Diamond lattice (mashrabiya) |
| `final-indigo.png` | Midnight Indigo — deep navy, **silver** ornament instead of gold | Khatim star-and-cross |
| `final-blackgold.png` | Black & Gold — true black ground; frame, star and headings stay gold, body copy turns white | Khatim star-and-cross |
| `final-earthy.png` | Earthy Gold — Black & Gold with the neutral black swapped for a warm terracotta-clay dark; every gold and white token is untouched | Khatim star-and-cross |
| `final-sandstone.png` | Sandstone & Gold — the leaflet, but light: a genuinely pale, sun-baked sand-and-terracotta ground (not a dark palette at all), with every gold token and every reading-text token pushed down to a deep antique bronze / espresso ink so it stays fully legible against the pale ground | Khatim star-and-cross |
| `banner-<colour>.png` | The banner (1600×900, `banner.py`), redone as a crest — star, wordmark, name and venue only, no date/time/WhatsApp — against a much denser Islamic geometric ground (a large faint rosette behind the star, a tiled dado border). Rendered in all six palettes: gold, emerald, burgundy, indigo, blackgold, earthy. |
| `banner-blackgold.png` | The fully customised banner (full address, solid minarets, crescent moon, no "brothers-only" line), on the **Earthy Gold** ground — same warm terracotta-clay gradient as `final-earthy.png` — with the mihrab arch filled as a genuinely solid niche (not a soft vignette): `arch_panel_d()` closes the same curve straight down near the bottom frame, filled ~0.94 opacity, with a faint clipped zellij texture and an inset moulding line inside it. |
| `banner-ivory.png` / `banner-blush.png` / `banner-sage.png` / `banner-powder.png` | Four **light** grounds — ivory, blush, sage, powder blue — built the same way as Earthy Gold: only the outer background and the ornament that has to read against it (frame hairlines, pattern, minaret fill — dropped to a deeper antique bronze, `_DEEP_GOLD`) change. The niche itself stays exactly black-and-gold; every reading token inside it is untouched. |
| `banner-invert-ivory.png` / `banner-invert-blush.png` / `banner-invert-sage.png` / `banner-invert-powder.png` | The **reverse** of the four above: outer frame, minarets, moon and pattern stay dark (true Black & Gold), and it's the niche panel itself that takes the pastel fill this time. The star sits on its own small dark disc (`STAR_DISC`) behind the halo ring, so it still reads as a gold mark on black even with a light panel around it; the title, wordmark, venue, address and note all switch to a deep-gold/espresso ink (`NICHE_*` tokens, `page(..., invert=True, niche_fill=...)`) tuned for the pale ground instead of the dark one. |

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

## Sandstone & Gold — going light without losing "earthy"

Every other colourway keeps the ground dark and lets gold or white text sit
on top of it. Sandstone inverts that relationship instead of just lightening
the existing dark tones: the page itself is pale sand/terracotta, and it's
the *text and ornament* that go dark — a deep antique-bronze gold and an
espresso ink — so contrast is carried the same way a printed page carries
it, not by a glow.

Getting there took three real fixes, all now controlled by palette keys
(each defaults to the original dark-palette behaviour, so none of the other
colourways changed):

- **The page's own background gradient became a visible "glow".** `bg1`/
  `bg2` are radial gradients centred above the medallion — on a dark ground
  the falloff reads as atmospheric lamplight; on a light, saturated ground
  the same falloff shows as a hard-edged pale dome behind the star. Fixed by
  widening the gradients' radii and softening their stops so the transition
  runs off the edge of the page instead of resolving inside it.
- **The "felt, not seen" ground rosette actually showed.** `ground_rosette()`
  draws ~200 overlapping hairlines at 7% opacity — invisible on a dark
  ground, but the sheer density of overlapping strokes visibly tints a light
  one even at 2% opacity. New `ground_op` key, set to 0 for Sandstone.
- **Shadows tuned for a dark backdrop muddied a light one.** `text-shadow`,
  and the `drop-shadow` filters on `.gold`/`.seal`/`.wordmark`/`.ayah`/
  `.med`, were dark blurs meant to lift light text off a dark/busy ground;
  behind already-dark text on a pale ground they just read as smudging.
  Each is now a palette key (`text_shadow`, `gold_shadow`, `seal_shadow`,
  `wordmark_shadow`, `ayah_shadow`, `med_shadow`) with the original dark
  values as the default, so Sandstone can supply much quieter light-ground
  equivalents. `halo_mult` and `scrim_mult` were added the same way, to turn
  down (not remove) the warm glow and the pattern-hiding scrim to the much
  smaller doses a pale ground needs.

Sandstone was then pushed further on the same two complaints — "looks a bit
dull" and "make the writing easier to read":

- The background gradient was deepened into real sunset colour (warm ochre
  through to burnt terracotta, not sand-and-beige) and the pattern/dado
  opacities raised, now that the gradient itself no longer bands. The gold
  tokens moved from a muted olive-bronze to a properly saturated amber.
- The body paragraph, the date/time values, the programme description, the
  address and the WhatsApp number all render **bold** on Sandstone. Weight
  is a palette key too (`body_weight`, `val_weight`, `pd_weight`,
  `addr_weight`, `wa_weight`, default 400 = unchanged for every other
  colourway) — genuine Cormorant Garamond SemiBold/Bold faces were added to
  the shared `FONTS` block in `variants.py` rather than left to the
  browser's synthetic bold, so the letterforms stay properly drawn at
  weight.

## Regenerating

```bash
python3 final.py
```

Renders all seven. To add a colourway, copy one of the palette dicts near
the bottom of the file, override the tokens that should change, and add a
`render(...)` call.
