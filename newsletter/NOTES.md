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

4. **Photo strip from the last gathering.** Built — the template has a
   `photo_strip` section (framed thumbnails between the masthead and "At
   a Glance"), on if `issue.photo_strip` is set. Still waiting on the
   actual photo(s) from TAZ to populate it for issue 1; drop the files
   into `assets/photos/` and add entries to `content/issues/issue-01.json`
   (see the `photo_strip` field shape in that file once populated).

5. **Which Q&As and sayings to run.** Issue 1 uses 4 of the 8 banked Q&As
   (`idhn`, `wird_different`, `welcomes_all`, `samaa`) and all 3 banked
   sayings (only 3 were supplied). Swap the `qa_ids` / `saying_ids` lists
   in `content/issues/issue-01.json` — ids are listed in
   `content/banks/qa_bank.json` and `content/banks/sayings_bank.json`.

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
