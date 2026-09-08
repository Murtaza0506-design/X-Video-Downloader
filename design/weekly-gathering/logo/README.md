# The star mark, extracted standalone

The order's own ten-point star (khatim), cut out from the poster/banner
artwork as a clean transparent asset — for use outside this project.

| File | Use |
|---|---|
| `star-gold.png` | Gold gradient, transparent background |
| `star-black.png` | Solid black, transparent background — for light backgrounds, single-colour print, embroidery |
| `star-white.png` | Solid white, transparent background — for dark backgrounds |
| `star-gold-on-black.png` | Gold star on a solid black circular disc — a self-contained "black and gold" lockup that doesn't depend on what's behind it |

All four are ~1750×1750px (the black-on-disc version slightly larger, to
include the disc's own margin), RGBA PNG, trimmed tight to the artwork with
a small transparent margin.

## Regenerating / making more variants

The star's shape comes from `mask-star.png` (in the parent `weekly-gathering/`
folder — and duplicated for the scratch build under `variants/`) — a pure
alpha mask, not a vector, so it can't be exported as a clean SVG directly.
Any new colour is a matter of re-rendering that mask through CSS
`-webkit-mask-image` with a different `background` (flat colour or
gradient) and screenshotting on a transparent page background:

```python
import final as f, variants as v
html = f'''<!doctype html><html><head><style>
html,body{{margin:0;padding:0;background:transparent;width:2000px;height:2000px}}
.mark{{position:absolute;left:50%;top:50%;width:1720px;height:1720px;transform:translate(-50%,-50%);
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-size:contain;mask-size:contain;
  -webkit-mask-position:center;mask-position:center;
  -webkit-mask-image:url({v.STAR_URI});mask-image:url({v.STAR_URI});
  background:YOUR_COLOUR_OR_GRADIENT_HERE;}}
</style></head><body><div class="mark"></div></body></html>'''
```

Render with headless Chrome using `--default-background-color=00000000` (not
just a transparent CSS background — Chrome's screenshot flag needs that
argument too, or it fills white) to get an RGBA PNG with real alpha, then
crop to `im.getbbox()` to trim the transparent margin.
