# Open items for TAZ

These are called out in the content brief as decisions rather than facts, so
nothing was invented — issue 1 ships with a clearly-marked placeholder or an
honest "TBC" in each case, and each is a one-line edit in a single file.

1. **Newsletter title.** Resolved — set to "Al Qadariya Al Bouchichia" per
   TAZ's instruction. Lives in `newsletter_name` in
   `content/evergreen/masthead.json`.

2. **Next Dhikr / next big gathering dates.** Both left as `"TBC"` in
   `content/issues/issue-01.json` under `at_a_glance.rows` — fill in once
   confirmed.

3. **thesufiway.co.uk as authoritative source.** Not something this build
   can verify — flagging per the brief that the site hadn't been updated
   since August 2025 as of this content package. Worth a quick check
   before this issue goes out.

4. **Photo strip from the last gathering.** Resolved — two photos from
   the 7 August 2026 gathering (Samaa, and the congregation) are in
   `assets/photos/` and wired into `content/issues/issue-01.json`'s
   `photo_strip`. The first photo (a phone screenshot with black
   letterboxing top and bottom) was cropped down to just the photo
   content before saving.

5. **Which Q&As and sayings to run.** Issue 1 uses 4 of the 8 banked Q&As
   (`idhn`, `wird_different`, `welcomes_all`, `samaa`). Of the 3 banked
   sayings, 2 run in "Words of the Shaykh" and the third
   (`divine_love_heart`) is reserved for the closing footer saying (see
   below) — swap either list in `content/issues/issue-01.json`.

6. **Theme.** Resolved — "Emerald Manuscript" (warm sand/terracotta
   ground, emerald + gold, a tessellated octagon pattern in the
   background) is now `ACTIVE_THEME` in `build.py`. Two other directions
   ("Midnight Gold", the original charcoal look, and "Modern Minimal", a
   borderless navy editorial layout) are still in `template/themes/` if
   worth revisiting.

7. **Closing saying, like the prayer timetables.** Added — the footer now
   ends with one saying (currently `divine_love_heart`), matching the
   convention TAZ uses on the prayer timetables. Set per issue via
   `footer_saying_id` in `content/issues/issue-01.json`, resolved from
   `content/banks/sayings_bank.json`.

## Correction: membership is Muslims only

The original content brief (drawn from thesufiway.co.uk) described the
tariqa as welcoming "Muslim and non-Muslim alike." TAZ has corrected this:
the tariqa is for Muslims. Updated two places to drop the non-Muslim
framing while keeping the genuine point — that people are welcome at any
level of knowledge or practice, not just the advanced:
- `content/banks/qa_bank.json` &rarr; the `welcomes_all` Q&A
- `content/issues/issue-01.json` &rarr; the closing line of the key article

Left untouched: "Guests of all backgrounds are always welcome" in
`content/evergreen/why_we_gather.json`, which is about visitors attending
a gathering, not about who the path itself is for. Worth confirming with
TAZ that this distinction is still correct before publishing.

## Asset note

The real khatim mark was supplied by TAZ and lives at
`assets/khatim-logo.jpg`, used in the masthead and footer. `build.py`
inlines it (and any photo-strip images) as a base64 data URI so each
built issue stays a single self-contained HTML file.
