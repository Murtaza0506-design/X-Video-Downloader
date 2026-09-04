# Print and Kindle specifics

## Paperback geometry

**Trim.** 5.5 × 8.5 in (139.7 × 215.9 mm) is a standard trade size and a KDP
standard. 6 × 9 is the other safe choice. Both are in the `TRIMS` table.

**Margins, mirrored.** Odd pages are rectos and carry the wide margin at the
spine. Inside 0.80 in, outside 0.60, top 0.72, bottom 0.71 gives a 4.10 in
measure of about 65 characters at 10.5 pt, which is inside the comfortable band.

**The gutter scales with page count.** KDP's minimum inside margin is 0.375 in
up to 150 pages, 0.5 in to 300, 0.75 in to 500, 0.875 in to 700. Setting 0.80
clears every band up to 500 pages, so the same file survives the book growing.

**Bleed: none.** If nothing runs to the page edge, supply at trim size with no
crop marks. The previewer will warn about it. The warning is correct and should
be accepted; it is not an error.

**Spine width is page count times paper caliper.** Cream is 0.0025 in per leaf,
white 0.002252. A 236-page book is 0.5900 in on cream and 0.5315 on white. Build
one cover per stock and upload only the one matching the paper chosen, or the
spine prints off centre.

**Cover wrap** = 2 × trim width + spine + 0.125 in bleed each side, by trim
height + 0.25 in. Keep everything that matters 0.25 in inside each trim edge,
and reserve a 2 × 1.2 in rectangle in the lower outer corner of the back board
for the barcode.

**Spine text** needs 100 pages minimum on KDP, and 0.0625 in clearance from each
fold.

**Colour.** A black-and-white interior must be neutral everywhere, which
`check_print.py` verifies by rendering pages and measuring channel spread. One
accent colour forces colour printing and multiplies the unit cost.

## Kindle

**Reflowable, no embedded fonts, no fixed layout.** See the EPUB traps in
`pipeline.md`.

**Cover art:** 1600 × 2560, ratio between 1:1.33 and 1:1.6, RGB, at least
1000 px on the short side.

**Identifier:** a stable UUID so a re-upload is recognised as a revision rather
than a new book. Kindle needs no ISBN; Amazon assigns an ASIN.

**Author metadata:** `dc:creator` is what Amazon reads onto the product page.
Leave it empty and the name has to be typed into the form, where it will not
match the file. The name on the cover art is a separate, optional choice.

## The KDP form

**Description.** The box may be rich text with formatting buttons, or a plain
textarea. Pasting HTML into the rich-text version shows literal tags. Prepare
both a plain-text and an HTML version and check which box is on screen. Limit is
4,000 characters. Allowed tags are `p`, `br`, `b`, `i`, `u`, `h4`–`h6`, `ul`,
`ol`, `li`.

**Keywords: seven slots, and the commonest waste is duplicating your own title
or subtitle.** Amazon already indexes both. Spend the slots on searches you are
otherwise invisible for. Cover four intents: what the book is, the tradition it
belongs to, the problem the reader has today, and buying it as a gift. No other
authors' names, no book titles, no subjective claims like "bestselling", nothing
about price.

**Categories:** three.

**Royalty.** 70% requires a list price of £1.77–£9.99 or $2.99–$9.99, and
charges a delivery fee by file size. On a text-only book of a few hundred KB
that fee is pennies, so 70% wins decisively; it only loses above £9.99, where
35% of a higher price pays more. If a print edition exists, the ebook must be at
least 20% below its list price.

**Territories:** all. Sales outside the 70% programme pay 35% for those sales
only, automatically.

**AI disclosure.** KDP asks whether AI tools were used for text, images or
translation. Answer honestly. It is recorded, it does not block publication, and
it does not appear on the product page.

## Order of operations

Publish the Kindle edition first, then use *Create Paperback* from the finished
title so both editions share one product page.
