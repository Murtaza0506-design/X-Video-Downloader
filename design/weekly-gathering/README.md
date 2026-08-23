# Weekly Dhikr Gathering — poster

Tariqa Qadiriyya Boutchichiya · Crescent Hall, Rochdale.

| File | Use |
|---|---|
| `Weekly-Dhikr-Gathering-share.png` | 1200 × 1800 — WhatsApp, Instagram, email |
| `Weekly-Dhikr-Gathering-print.png` | 3600 × 5400 — 300 dpi at 12″ × 18″ |
| `Weekly-Dhikr-Gathering.pdf` | Vector text, 12.5″ × 18.75″ — send to a print shop |
| `DESIGN-PHILOSOPHY.md` | The aesthetic the poster is built on |
| `build.py` | Regenerates the artwork |

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
