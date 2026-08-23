# Venue silhouette — four options

Four treatments of Crescent Hall's own facade, cut to a silhouette from the
submitted photo and set into the poster four different ways. Pick one and it
becomes the poster; the other three stay here as a record of what else was
tried.

| File | Treatment |
|---|---|
| `A-dusk-court.png` | The hall fills the mihrab arch itself, dark against a dusk sky glowing gold at the horizon — the arch becomes a window onto the real building. |
| `B-seal-of-the-house.png` | The roofline set as a cameo inside the same 99-mark halo that used to frame the star — an abstract gold/dark disc, more emblem than photograph. |
| `C-skyline-banner.png` | The boldest option — a wide gold skyline banner across the top of the poster, no medallion, closer to a letterhead. |
| `D-framed-keepsake.png` | A small framed photograph of the hall, hairline-bordered like something hung on a wall, sitting above the order's name. |

## How the silhouette was made

The source photo (stone facade, blue sky, foreground plants) doesn't cut out
with a single colour threshold — the building's own blue-and-white tilework
reads the same as sky by hue alone. `silhouette/` (not committed here — see
the render scripts) classifies sky by colour, then keeps only the region
**flood-filled from the top edge**, so enclosed patches of sky-toned colour
inside the facade (the mosaic panels, the archway) don't get cut out as
holes. What survives is one clean silhouette: the castellated roofline,
the facade, the stairs.

That silhouette is then baked into three coloured rasters — because a
raw alpha mask painted with `mask-image` can't easily take a vertical
gradient the way `.mark` (the star, the wordmark) can in CSS alone:

- `mask-building-wide-dark.png` — solid dark umber, for a silhouette seen
  against a lit sky (variant A).
- `mask-building-wide-gold.png` — a baked vertical gold gradient, for a
  silhouette that reads as metal against the dark page (variants C, D).
- `mask-building-square-gold.png` — the same gold bake, cropped square,
  for the circular cameo (variant B).

## Regenerating

```bash
python3 variants.py            # shared geometry, fonts, CSS — imported, not run directly
python3 render_variants.py     # writes poster-A.html … poster-D.html and renders each to PNG
```

Everything from the date band down (programme, venue, WhatsApp, footer) is
identical across all four — `variants.py:bottom_html()` — only the hero
area above it changes per variant. Whichever is chosen can be folded back
into the main `build.py` as the new hero treatment.
