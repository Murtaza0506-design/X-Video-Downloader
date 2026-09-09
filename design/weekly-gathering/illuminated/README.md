# Illuminated Manuscript background

The leaflet's background, for the `final-illuminated.png` colourway, is not
generated at all — it's a real photograph of the user's own hand-painted
tazhib (Persian/Islamic illumination: gouache and gold leaf, still
in progress with the brush in shot), turned into a full-page background
without redrawing it as vector art, so the actual paint and gold-leaf
texture shows.

## Files

| File | What it is |
|---|---|
| `source-crop.jpg` | The painted corner motif, cropped out of the user's photo (desk, dried roses, paintbrush removed) — original blue/purple/teal colouring |
| `tiled-background.jpg` | The 1200×1800 leaflet background built from the original colouring: `source-crop.jpg` mirrored into a 2×2 symmetric medallion, then tiled down the page |
| `source-crop-redgreen.jpg` | The same crop, hue-shifted: the two blues become a rich red and a vivid green (gold and purple untouched) — see "Recolouring" below |
| `tiled-background-redgreen.jpg` | The tiled background built from the red/green crop — **this is the one `final.py` actually uses** (copied to `final/illum-bg.jpg`) |

## How it was built

1. **Crop.** The photo was of a triangular corner ornament sitting on a desk
   next to dried roses, shot at an angle, brush still in hand. `source-crop.jpg`
   is a tight rectangular crop that's entirely painted surface — no desk, no
   flowers, no brush, negligible paper margin.
2. **Mirror into a medallion.** One corner motif doesn't tile on its own —
   its edges don't match up with each other. Flipping it horizontally,
   vertically, and both (a standard trick for turning a quarter-motif into a
   symmetric "carpet page" tile, and how a lot of real manuscript
   backgrounds are actually constructed) turns it into a self-contained,
   roughly-seamless 2×2 block that reads as one bigger, deliberate design
   rather than four repeats of a triangle.
3. **Tile down the page.** That mirrored block is scaled to the leaflet's
   1200px width and repeated down the full 1800px height, then cropped to
   size. `tiled-background.jpg` is the result — a real photographed texture,
   filling the whole page.

## Wiring it into `final.py`

The `ILLUMINATED` palette (bottom of `final.py`) is the first colourway
whose ground isn't a CSS gradient: a new `bg_image_uri` palette key, read by
`.page{background:...}` in `css()` — when it's set, the page background
becomes `url(...) center/cover no-repeat` instead of `{bg1},{bg2}`. Every
generated overlay that exists to add "Islamic ornament" on top of a plain
gradient (the zellij/lattice tiles, the ground rosette, the dado band, the
halo glow, the pattern-hiding scrim) is switched off for this palette —
they were built to decorate an empty ground, and layering vector pattern
over a photograph just fights it rather than adding to it.

Two more things needed solving once the ground was a genuinely busy photo
instead of a flat colour or soft gradient:

- **Every actual line of text** (title, subtitle, ayah + translation,
  date/time, body, programme, venue, address, WhatsApp, footer) is flat
  white. The per-class `-webkit-text-stroke` hack from Sandstone's gold-text
  pass was consolidated into one rule on the shared `.at` class
  (`outline_stroke` palette key, default `"0 transparent"` — invisible, so
  no other colourway is affected).
- **The star and Arabic wordmark are gold-on-mask images, not text** — they
  can't take a CSS text outline at all.

The first pass tried to make white-with-a-heavy-black-outline text legible
sitting *directly* on the photo, with only a soft dark vignette behind the
star/wordmark. Two problems: it was still genuinely hard to read in places
(blue-on-blue, gold-on-gold), and a heavy outline on long lines of body copy
started reading as solid black rather than white. The request that followed
— make the text sit on something opaque, but not a plain box — is what's
actually in `final.py` now:

- **`hero_arch_panel(base_y)`** is a wide, flat horseshoe dome (a half-ellipse,
  not the sharper pointed-mihrab curve used for the decorative outline
  elsewhere) closed into a filled region. One solid arch, coloured
  `cartouche_fill` (a deep navy pulled from the artwork's own palette) with a
  `cartouche_edge` gold hairline, sits behind the entire top of the page —
  ayah, title, subtitle, wordmark and the star medallion all read straight
  off it. It started as a direct reuse of `v.arch()`'s own pointed-gothic
  curve, which tapers to a near-zero-width point at the very top — fine for
  a hairline outline, but the ayah (a full line of Arabic sitting right up
  near the top of the panel) spilled straight off the sides of it onto the
  bare photo. The wider ellipse stays close to full width much further up.
  Below the title/subtitle/wordmark it now tapers inward to a narrower
  `waist_y`/`waist_l`/`waist_r`, running straight down past the star instead
  of staying at the full dome width all the way to the base — the user
  circled that space in black on a rendered copy: full width there was just
  dead solid-colour panel either side of the medallion, holding nothing,
  and read as empty rather than deliberate. The result is closer to a
  genuine keyhole/mihrab silhouette than the dome-on-a-rectangle it was.
- **`cartouche_bar(cx, cy, w, h)`** is the shape for everything below the
  arch: a horizontal bar with a smooth pointed-oval cap at each end — the
  same vocabulary Persian/Islamic illumination actually uses to carry an
  inscription, not a rectangle with corners rounded off. One bar each for
  the date/time row, the body paragraph, the programme columns, the venue
  block, the WhatsApp confirmation, and the footer line. Its first version
  built the cusp from a single hand-tuned bezier control point per corner;
  on the wider bars that pinched into a hard, jagged-looking point right
  where wrapped text sat — read as a "cut off" corner rather than a
  deliberate one. It's now two true elliptical arcs (`A rx,ry ...`), smooth
  by construction with no tuning needed.
- Both shapes are driven by one `cartouche_zones` palette key (a list of
  `{shape, ...}` dicts) read by `cartouche_panels_svg()` in `frame_svg()`,
  default empty so every other colourway is untouched. With the panels
  doing the contrast work, `outline_stroke` dropped back down to a thin
  hairline and the old `mark_backing` vignette was removed — the star and
  wordmark now just sit on the arch panel like everything else.
- The old hairline "confirm attendance" box (a plain rounded rectangle)
  is suppressed on any colourway that supplies `cartouche_zones`, so it
  doesn't draw on top of the WhatsApp cartouche.
- The programme columns (`.cols`, previously a fixed 700px) and the venue
  block's letter-spacing (`.venue`/`.vsub`/`.addr`) were both noticeably
  narrower than the wide cartouche bars sitting behind them — the user
  circled the dead space at both ends of those bars in red. `cols_hw`/
  `cols_pad` and `venue_ls`/`vsub_ls`/`addr_ls` are now palette keys
  (defaults match the previous hardcoded values, so every other colourway
  is unaffected); Illuminated widens the columns and roughly doubles the
  venue block's tracking so the writing actually fills the bar instead of
  sitting in a narrow strip in the middle of it.

### The panel fill itself: four colourways, real gradients not flat tints

A flat `rgba(...)` fill behind the text — the original approach — read as a
dull, pasted-on tint sitting on top of the photo, not part of it. Two fixes,
plus four colours to choose from:

- **`cartouche_stops`** replaces the flat colour with an SVG radial gradient
  (`cartouche_panels_svg()` builds a `<radialGradient>` in `<defs>` and
  points every panel's `fill` at it). The three stops per colour aren't
  picked by eye — `dark`/`mid`/`light` are the actual 6th/50th/93rd-
  percentile-by-brightness pixel values sampled from that colour's own hue
  band in the real photo, so the gradient reads as light catching folded
  fabric or lacquer rather than a UI tint. `cartouche_opacity` controls how
  much of the photo shows through underneath (0.90–0.95 — enough that the
  colour reads as solid, not so much that the sampling that made it
  "realistic" gets lost).
- **Four colourways** — `ILLUMINATED_RED` (the default), `_GREEN`, `_GOLD`,
  `_PURPLE` — same background photo and layout, only `cartouche_stops` and
  the text colours it forces differ, so they render side by side for
  comparison. Red and the default gold-leaf `outline_stroke` green were
  already close in value to white text, so green/purple panels use a gold
  outline instead (`0.9px #E8C46A`) to avoid a same-colour-on-itself clash.
  Gold is the one true swap: a light panel needs dark ink, not white, so
  `ILLUMINATED_GOLD` flips every reading-text colour and `gold_grad` to a
  near-black bronze (`#2A1B0A`) with a soft cream outline and a light-lift
  shadow instead of a dark one — the same swap `final-sandstone` made
  going from a dark ground to a light one, just localised to one panel
  colourway here instead of the whole page.

## Recolouring (`source-crop-redgreen.jpg`)

The request was "turn the light blue and dark blue background to red and
green, with the same realism" — a hue rotation of specific colour bands in
the actual photo, not a redraw, so all the shading, gold-leaf shimmer and
brush texture had to survive untouched.

Converting to HSV makes this precise: hue carries *which* colour a pixel is,
saturation and value carry *how* it's shaded (both left alone, which is what
keeps the realism). Sampling the artwork found two distinct blue bands —
a darker, more saturated royal blue (hue ≈ 208–242°) and a lighter teal
(hue ≈ 188–203°) — clearly separated from the gold (≈ 30–60°) and the purple
swirl accent (≈ 250°+), so each band could be rotated independently:

```python
navy_w = band_weight(hue_deg, 208, 242, feather=8)   # dark blue
teal_w = band_weight(hue_deg, 188, 203, feather=10)  # light blue
offset = navy_w*136 + teal_w*(-68)     # navy -> red, teal -> green
new_hue = (hue_deg + offset) % 360     # saturation & value untouched
```

`band_weight()` is a smoothstep-feathered band, not a hard cutoff — pixels
right at a band's edge get a *partial* rotation that fades in/out, so there's
no hard seam where (say) a slightly-blue-purple pixel suddenly jumps to full
red. The **offset is added, not set to a fixed hue** — every pixel keeps its
own position within the band, so the natural variation from shading and
brush texture carries straight through into the new colour instead of
flattening into one flat red and one flat green.

Gold and purple are far enough away in hue (and get zero weight from both
bands) to pass through completely unchanged.

The rest of the pipeline (mirror into a 2×2 tile, scale, repeat down the
page) is identical to the original — see below. `cartouche_fill` (the
opaque panel colour) and `outline_stroke` (the text edge) in `final.py`'s
`ILLUMINATED` palette were then repicked to match: a deep red sampled from
the recoloured artwork for the panels, a bright green for the outline
(previously navy and aqua-blue, picked to match the blue original).

## Regenerating with a different source photo

Replace `source-crop.jpg` with a new tight crop (all painted surface, no
background clutter), then:

```python
from PIL import Image, ImageOps
src = Image.open("source-crop.jpg").convert("RGB")
w, h = src.size
block = Image.new("RGB", (w*2, h*2))
block.paste(src, (0, 0))
block.paste(ImageOps.mirror(src), (w, 0))
block.paste(ImageOps.flip(src), (0, h))
block.paste(ImageOps.flip(ImageOps.mirror(src)), (w, h))

W, H = 1200, 1800
scale = W / block.width
block = block.resize((W, round(block.height * scale)))
n = -(-H // block.height)
canvas = Image.new("RGB", (W, block.height * n))
for i in range(n):
    canvas.paste(block, (0, i * block.height))
canvas.crop((0, 0, W, H)).save("tiled-background.jpg", quality=92)
```

Then re-run `python3 final.py` (`ILLUMINATED` picks up `tiled-background.jpg`
via `_jpeg_uri("illum-bg.jpg")` — copy the new file to that name in the
`final/` working directory, or update the filename in the palette).
