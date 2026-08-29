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
   (`idhn`, `wird_different`, `welcomes_all`, `samaa`). The saying section
   (renamed "Words of the Masters" — see below) runs one saying each from
   Sidi Hamza, Sidi Jamal, and Sidi Mounir — swap either list in
   `content/issues/issue-01.json`.

6. **Theme.** Resolved — "Emerald Manuscript" (warm sand/terracotta
   ground, emerald + gold, a tessellated octagon pattern in the
   background) is now `ACTIVE_THEME` in `build.py`. Two other directions
   ("Midnight Gold", the original charcoal look, and "Modern Minimal", a
   borderless navy editorial layout) are still in `template/themes/` if
   worth revisiting.

7. **Closing saying, like the prayer timetables.** Added — the footer now
   ends with one saying, matching the convention TAZ uses on the prayer
   timetables. It went through two picks: first the Mulla Nasruddin
   "looking for my key" tale, then TAZ asked to swap it for Ibn 'Ata'
   Allah al-Iskandari's "What has he found who has lost God? And what
   has he lost who has found God?" (`ataillah_lost_god` in
   `content/banks/sayings_bank.json`), which is what issue 1 now closes
   with. Set per issue via `footer_saying_id` in
   `content/issues/issue-01.json`; `nasruddin_key` is still in the bank
   if a future issue wants something lighter.
   Note on `quote_html` in the sayings bank: every entry carries its own
   opening/closing quotation marks (the template doesn't add them
   automatically) so a narrative quote with its own nested dialogue can
   use single quotes inside without a doubled-up outer quote mark. Wrap
   the whole thing in &ldquo;/&rdquo;, and use &lsquo;/&rsquo; for any
   quoted speech inside it.

8. **Locations, so people can find both places.** Added a "Find Us"
   section (`content/evergreen/locations.json`) with the Rochdale
   gathering address and the Madagh zawiya in Morocco, each with a photo
   and a map link. The footer's address is now a clickable link to the
   same Rochdale map link. Rochdale uses the exact coordinates TAZ gave
   (53°37'17.75"N 2°10'12.95"W); Madagh uses the village's coordinates
   from Wikipedia (35°00'48"N 2°20'23"W) as a general reference point
   rather than a pin on the zawiya building itself, since I didn't have
   an exact address for that. Worth double-checking the Madagh pin
   lands where TAZ expects.

9. **Writing pass.** Went through every content file and removed every
   em dash from newsletter-facing text (the ones left are only in
   `_note`/`_source` fields, which are editorial comments and never
   render), replacing them with periods, colons, or commas depending on
   what read most naturally. Also loosened a couple of stiff "not X, but
   Y" sentence constructions in the key article. Nothing in any direct
   quote (sayings, the hadith qudsi, the Nasruddin tale) was reworded,
   only my own connecting prose.

## One saying from each of the three masters

TAZ asked for the main sayings section (previously all 3 quotes from Sidi
Hamza) to carry one saying each from Sidi Hamza, Sidi Jamal, and Sidi
Mounir instead. Renamed the section from "Words of the Shaykh" to "Words
of the Masters" since it's no longer just the one figure.

Sidi Hamza's sayings all came from thesufiway.co.uk's own "Sayings" page
(76 of them are listed there — plenty more to draw from for future
issues). Neither thesufiway.co.uk nor Sidi Jamal's or Sidi Mounir's own
biography pages had any directly-quoted sayings from either of them
(everything there is written about them, not by them), so I searched
further and found two verbatim, sourced quotes from an address both of
them gave at the same event — the World Symposium of Sufism (Mawlid),
21 November 2018 — published on tariqausa.com:
- `sidi_jamal_companionship`: &ldquo;Companionship is an obligation for
  those who want to make their way towards God.&rdquo;
  (tariqausa.com/16-sidi-jamal)
- `sidi_mounir_home`: &ldquo;You are not guests here. This is your
  home.&rdquo; (tariqausa.com/13-sidi-mounir-speech)

Both are genuine direct quotes, not paraphrases, but tariqausa.com is a
different chapter's site than thesufiway.co.uk — worth a quick check that
TAZ is comfortable citing it as a source before this goes out. Each entry
in `content/banks/sayings_bank.json` carries a `_source` note recording
where it came from (ignored by the build, just for editorial reference).

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
