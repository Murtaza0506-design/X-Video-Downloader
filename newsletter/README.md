# Tariqa Newsletter

A template + swappable data build for the Al Qadariya Al Bouchichia
newsletter (Tariqa Al Qadiriya Al Boutchichiya). Reuses the gold-on-charcoal
aesthetic of the existing "Weekly Dhikr Gathering" leaflet: ornamental gold
border and corners, the tariqa's khatim medallion, serif display type, and
letter-spaced gold eyebrow labels.

## Structure

```
newsletter/
  template/
    newsletter.html.jinja   # masthead, ornaments, section chrome — edit rarely
    style.css                # all visual styling
  assets/
    khatim-logo.jpg           # the tariqa's khatim mark, used in masthead + footer
    corner.svg                # gold corner ornament used at all 4 corners
    photos/                   # source images for an issue's photo strip
  content/
    evergreen/                # stable across issues: masthead, Wird, Why We
                               # Gather, New to the Path, footer
    banks/                    # larger pools an issue picks a few items from:
                               # qa_bank.json, sayings_bank.json,
                               # did_you_know_bank.json, history_series.json
    issues/
      issue-01.json           # everything specific to one issue
  output/
    issue-01.html             # generated — do not hand-edit
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

## Open decisions (see NOTES.md)

A few items from the content brief are still open (newsletter title, next
Dhikr/gathering dates, whether to run a photo strip, and which 3-5 Q&As /
sayings to feature). See `NOTES.md` for the placeholder chosen for issue 1
and where to change it.
