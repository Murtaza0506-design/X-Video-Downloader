# Weekly Dhikr Gathering — poster

Tariqa Qadiriyya Boutchichiya · Crescent Hall, Rochdale.

| File | Use |
|---|---|
| `Weekly-Dhikr-Gathering-share.png` | 1200 × 1800 — WhatsApp, Instagram, email |
| `Weekly-Dhikr-Gathering-print.png` | 3600 × 5400 — 300 dpi at 12″ × 18″ |
| `Weekly-Dhikr-Gathering.pdf` | Vector text, 12.5″ × 18.75″ — send to a print shop |
| `DESIGN-PHILOSOPHY.md` | The aesthetic the poster is built on |
| `build.py` | Regenerates the artwork |
| `assets.py` | Lifts the supplied marks off their backgrounds |
| `mask-star.png`, `mask-wordmark.png` | The ten-point star mark and the Arabic wordmark, as alpha masks |
| `mask-seal.png` | The earlier circular seal — kept, no longer used in the poster |

## The ground

The field is a Moroccan *zellij* tessellation, generated rather than tiled from
an image: one eight-pointed khatim per repeat, its points reaching exactly to
the edge of its square so neighbouring stars meet tip to tip and the small
square between four of them falls out as the cross. The same pattern at a
finer pitch runs as a dado band between the two frame rules.

A three-lobe scrim sits between the tilework and the type, dimming the pattern
only where words fall, so the ground stays rich at the margins without ever
competing with the text.

## The supplied marks

The ten-point star and the Arabic wordmark arrived as flat images — the star
gold on black, the calligraphy gold on black. `assets.py` reduces each to a
pure alpha mask, which the page then paints in the poster's own gold
gradient, so neither sits on the page as a pasted-in rectangle. The red rule
beneath the calligraphy is removed while the red dots of the *shin* letters
are kept and carried into gold — they are orthography, not ornament.

The star sits inside the same halo — the outer rim and the 99-mark tasbih
ring — that previously framed the circular seal; only the mark at the centre
changed. The seal extraction is kept in `assets.py` and `mask-seal.png` in
case it's wanted again.

Re-run `python3 assets.py` only if the source marks change.

## Regenerating

The typefaces (Cinzel, Cormorant Garamond, Amiri, Marcellus) are fetched from
Google Fonts into `fonts/` and embedded in the HTML, so the output is self-contained:

```bash
python3 build.py          # writes poster.html
```

Render with headless Chromium:

```bash
chrome --headless --screenshot=out.png --window-size=1200,2000 \
       --force-device-scale-factor=3 file://$PWD/poster.html   # crop to 1200×1800 ratio
chrome --headless --print-to-pdf=out.pdf file://$PWD/poster.html
```

## Editing the details

Date, time, programme, venue and contact number are plain text near the bottom
of `build.py`. The geometry — the rosette, the arch, the frame — is generated,
so nothing needs redrawing when the wording changes.
