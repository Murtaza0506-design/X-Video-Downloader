# Open items for TAZ

These are called out in the content brief as decisions rather than facts, so
nothing was invented — issue 1 ships with a clearly-marked placeholder or an
honest "TBC" in each case, and each is a one-line edit in a single file.

1. **Newsletter title.** Defaulted to reusing "The Sufi Way" (the jama'a's
   existing site name) as the publication title, since the brief floated
   that option. Change `newsletter_name` in
   `content/evergreen/masthead.json` if a distinct name is preferred.

2. **Next Dhikr / next big gathering dates.** Both left as `"TBC"` in
   `content/issues/issue-01.json` under `at_a_glance.items` — fill in once
   confirmed.

3. **thesufiway.co.uk as authoritative source.** Not something this build
   can verify — flagging per the brief that the site hadn't been updated
   since August 2025 as of this content package. Worth a quick check
   before this issue goes out.

4. **Photo strip from the last gathering.** Not built — no photos were
   supplied. The template has room for one (a simple image row could sit
   between the masthead and "At a Glance") if TAZ supplies photos for a
   future issue; ask and it can be added as its own template partial that
   issue data can turn on/off, without touching the rest of the layout.

5. **Which Q&As and sayings to run.** Issue 1 uses 4 of the 8 banked Q&As
   (`idhn`, `wird_different`, `welcomes_all`, `samaa`) and all 3 banked
   sayings (only 3 were supplied). Swap the `qa_ids` / `saying_ids` lists
   in `content/issues/issue-01.json` — ids are listed in
   `content/banks/qa_bank.json` and `content/banks/sayings_bank.json`.

## Asset note

No source file for the leaflet's khatim star (`IMG_4446.png`) was available
in this session, so `assets/khatim.svg` is a freshly-drawn vector redraw of
the classic eight-point khatim (two overlapping squares in a ring) rather
than an extraction from that image. Swap in the real asset if the exact
mark from the leaflet needs to match pixel-for-pixel.
