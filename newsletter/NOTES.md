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
   (`idhn`, `wird_different`, `welcomes_all`, `samaa`) and all 3 of Sidi
   Hamza's banked sayings in "Words of the Shaykh" — swap either list in
   `content/issues/issue-01.json`.

6. **Theme.** Resolved — "Emerald Manuscript" (warm sand/terracotta
   ground, emerald + gold, a tessellated octagon pattern in the
   background) is now `ACTIVE_THEME` in `build.py`. Two other directions
   ("Midnight Gold", the original charcoal look, and "Modern Minimal", a
   borderless navy editorial layout) are still in `template/themes/` if
   worth revisiting.

7. **Closing saying, like the prayer timetables.** Added — the footer now
   ends with one saying, matching the convention TAZ uses on the prayer
   timetables. TAZ asked for it to be able to draw from any prominent
   Sufi (not only Sidi Hamza) and allowed some humor, so issue 1 closes
   with the well-known Mulla Nasruddin "looking for my key" teaching
   tale (`nasruddin_key` in `content/banks/sayings_bank.json`) rather
   than another Sidi Hamza saying. Set per issue via `footer_saying_id`
   in `content/issues/issue-01.json`.
   Note on `quote_html` in the sayings bank: every entry now carries its
   own opening/closing quotation marks (the template no longer adds
   them automatically) so that a narrative quote like Nasruddin's, which
   has its own nested dialogue, can use single quotes inside without a
   doubled-up outer quote mark. Follow that pattern for any new saying:
   wrap the whole thing in &ldquo;/&rdquo;, and use &lsquo;/&rsquo; for
   any quoted speech inside it.

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
