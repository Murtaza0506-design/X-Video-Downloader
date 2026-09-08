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
| `source-crop.jpg` | The painted corner motif, cropped out of the user's photo (desk, dried roses, paintbrush removed) |
| `tiled-background.jpg` | The actual 1200×1800 leaflet background: `source-crop.jpg` mirrored into a 2×2 symmetric medallion, then tiled down the page |

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

- **The star and Arabic wordmark are gold-on-mask images, not text** — they
  can't take a CSS text outline. Both get a soft dark radial-gradient
  vignette behind them instead (`build_hero()`'s `word_backing`/
  `seal_backing`, driven by a new `mark_backing` palette key, default unset
  so no other colourway is affected) so the gold reads clearly wherever it
  lands on the pattern.
- **Every actual line of text** (title, subtitle, ayah + translation,
  date/time, body, programme, venue, address, WhatsApp, footer) is flat
  white with a bold black outline, since it has to stay readable over blue,
  purple, teal and gold in different places depending on where it falls.
  The per-class `-webkit-text-stroke` hack from Sandstone's gold-text pass
  was consolidated into one rule on the shared `.at` class
  (`outline_stroke` palette key, default `"0 transparent"` — invisible,
  so every other colourway is unaffected) rather than scattered per element.

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
