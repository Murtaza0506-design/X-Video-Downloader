# Tariqa Newsletter

A template + swappable data build for the Al Qadariya Al Bouchichia
newsletter (Tariqa Al Qadiriya Al Boutchichiya). Active theme is "Emerald
Manuscript": a warm sand/terracotta ground with a tessellated octagon
pattern (classic zellige geometry) woven faintly through the page, deep
emerald headings, antique-gold accents, the tariqa's khatim medallion, and
serif display type throughout.

## Structure

```
newsletter/
  template/
    newsletter.html.jinja   # masthead, ornaments, section chrome — edit rarely
    themes/
      emerald-manuscript.css  # ACTIVE theme — earthy parchment, emerald + gold
      midnight-gold.css       # original charcoal + gold direction (kept for reference)
      modern-minimal.css      # navy, left-aligned, borderless, editorial (kept for reference)
  assets/
    khatim-logo.jpg           # the tariqa's khatim mark, used in masthead + footer
    corner.svg                # gold corner ornament used at all 4 corners
    photos/                   # source images for an issue's photo strip
    locations/                # photos for the Find Us section (evergreen)
  content/
    STYLE.md                   # language rules to check new copy against
    evergreen/                # stable across issues: masthead, Wird, Why We
                               # Gather, New to the Path, locations, footer
    banks/                    # larger pools an issue picks a few items from:
                               # qa_bank.json, sayings_bank.json,
                               # did_you_know_bank.json, history_series.json
    issues/
      issue-01.json           # everything specific to one issue
  output/
    issue-01.html             # generated (active theme) — do not hand-edit
  build.py
```

**To publish a new issue**, copy `content/issues/issue-01.json` to
`issue-02.json`, update its dates, key article, featured history subject,
and the `qa_ids`/`saying_ids`/`did_you_know_id` selections (pick 3-5 from
the banks in `content/banks/`), then run:

```
pip install -r requirements.txt
python3 build.py issue-02
```

Open `output/issue-02.html` directly in a browser, or print it to PDF from
there for a print layout. Running `python3 build.py` with no argument
rebuilds every issue found in `content/issues/`.

No template or CSS edits are needed for a routine issue — only the one
JSON data file.

## Themes

The same content and HTML structure can render in any of the stylesheets
under `template/themes/`. Only colors, type, and a handful of structural
CSS rules (alignment, borders, card layout) differ between them — no
content or template changes needed to compare or switch.

```
python3 build.py issue-01 --all-themes    # one output file per theme, for comparing
python3 build.py issue-01 --theme emerald-manuscript   # build just one theme
```

Once a theme is chosen, set `ACTIVE_THEME` at the top of `build.py` to its
name — that's what plain `python3 build.py` builds from then on.

Adding a fourth theme is a new `template/themes/NAME.css` file using the
same class names as `midnight-gold.css`; no other file needs to change.

## Open decisions (see NOTES.md)

A few items from the content brief are still open (newsletter title, next
Dhikr/gathering dates, whether to run a photo strip, and which 3-5 Q&As /
sayings to feature). See `NOTES.md` for the placeholder chosen for issue 1
and where to change it.
