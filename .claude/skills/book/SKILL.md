---
name: book
description: Produce a structured non-fiction book from a markdown manuscript into three finished editions at once — a web reading edition, a print-ready paperback interior and cover, and a reflowable Kindle EPUB — with measured prose style and automated preflight. Use this whenever the user wants to write, extend, retypeset, or publish a book of repeating units (a quotation book, a field guide, a book of letters, rules, cases, fallacies, recipes, or entries of any fixed shape), or asks about KDP, trim size, spine width, EPUB validity, chapter structure, or making prose not read as machine-written. Reach for it even when the request sounds like a single small task, such as "add a chapter", "rebuild the PDF", "why was my upload rejected", or "make this sound less like AI wrote it" — the pipeline and the style targets only hold if changes go through them.
---

# Building a book

This skill encodes a working pipeline: one markdown manuscript compiles to a web
edition, a print-ready paperback, and a Kindle EPUB, with the prose measured
against stylometric targets and three preflight gates that fail loudly.

It exists because the expensive part of a book is not the writing tooling. It is
the several dozen decisions that are easy to get wrong and costly to discover
late: a page counter that cannot reset, a spine that does not match the paper, a
keyword that duplicates your subtitle, an index that files scripture under
proverbs. Those are all recorded here.

## Start with the unit, not the chapters

Everything downstream depends on one decision: **what shape does the repeating
element take, and what does it add that the source material lacks?**

A quotation on its own is decoration. A quotation plus *what it means* plus
*where to put it* is a tool. That third field is the entire book. Get it wrong
and no amount of good writing rescues it.

State the unit as named fields before writing a word:

| Book | The unit |
|---|---|
| A commonplace book | quotation · what it means · how to use it |
| A book of arguments | the move · what it sounds like in speech · why it works · what to say back |
| A book of letters | the situation · the full letter · the two sentences doing the work |
| Confident and wrong | the prediction · who and when · what happened · what the error was made of |

Two tests before committing:

1. **Could a reader get the last field anywhere else?** If not, that is the book.
2. **Does it survive 300 repetitions?** Three fields is usually right. Two is
   thin. Five becomes a form to fill in, and the writing goes dead.

Then arrange by **the reader's problem, not the source's chronology**. Nobody
arrives wanting the eighteenth century. They arrive having had a bad Tuesday.

## The manuscript

One markdown file per chapter in `content/`, numbered so they sort. Front
matter, an opening, then entries separated by `---`:

```markdown
---
part: One — Yourself
chapter: 6
title: Envy and Comparison
---

# Chapter 6 — Envy and Comparison

Opening prose, about 300 words. Each paragraph is ONE LINE with no hard wraps;
the parser treats every line as a paragraph.

---

> "The quotation, in double quotes." — Attribution

**What it means.** One paragraph, on a single line.

**How to use it.** One paragraph, on a single line.
```

Field names are the unit's names and are matched literally by the parser. When
the unit changes, change them in `scripts/build_site.py` and in the gate.

## The pipeline

Four builders, three gates. Run in this order, because each reads what the last
produced:

```bash
python3 scripts/build_site.py         # manuscript -> book.html + site/index.html
python3 scripts/check_book.py         # gate: structure and house rules
python3 scripts/build_print.py        # -> print/interior.pdf + SPECS.json
python3 scripts/build_print_cover.py  # -> covers, spine measured from the page count
python3 scripts/check_print.py        # gate: geometry, fonts, ink, colour, spine
python3 scripts/build_epub.py         # -> ebook/*.epub + cover.jpg
python3 scripts/check_epub.py         # gate: container, XHTML, links, cover
```

The cover must be built **after** the interior: spine width is page count times
paper caliper, and the interior decides the page count. `check_print.py` fails
if they have drifted apart.

Detail on each script, and what each gate actually checks, is in
`references/pipeline.md`. Read it before modifying a builder.

## Making the prose not read as machine-written

This matters more for this book shape than any other, because the format repeats
by design. Three hundred near-identical units is the worst case for the thing
that gives machine prose away: **low burstiness**, a near-constant sentence
length and rhythm holding across a whole document.

The method that works is draft, measure, revise **against numbers**:

```bash
python3 scripts/measure_style.py     # per chapter and whole book
python3 scripts/lint_prose.py        # flags hedges and -ly adverbs by line
```

Targets, and why each one is there, are in `references/style.md`. The headline:

- **Hedges are the biggest single lever.** One draft used "rather" 78 times,
  "usually" 50, "actually" 45. Every one is a small apology for the sentence it
  sits in. Cutting them moved the book more than any other edit.
- **Vary sentence length on purpose.** Every entry gets one sentence under six
  words. Every chapter opening gets one over thirty.
- **Chapters should not match each other statistically.** A chapter on anger
  should run short and clipped; one on ageing long and slow. If every chapter
  has the same mean, the voice is not moving.
- **Concrete beats abstract.** Not "a difficult conversation with a colleague"
  but the 8.40 stand-up, the quote from the builder, the WhatsApp group with
  your sisters in it.
- **No em dashes in prose.** A house rule, enforced by the gate, and also one of
  the loudest tells.

Write the new chapters, measure, then revise. Expect the first pass to come in
worse than the existing book; that is normal and the revision closes it.

## Two things that make a book of advice bearable

**Let entries contradict each other, and say so in the introduction.** One entry
tells you to persist, another to stop. Real advice conflicts because real
situations differ. A book that never disagrees with itself has been simplified
into uselessness.

**Give every chapter an exit.** The last entry gives the reader permission not
to apply the chapter: to leave the grievance unforgiven, to skip the difficult
conversation, to stop if stillness makes things worse. Advice without a limit
becomes pressure, and pressure is the last thing anyone needs when they are
already struggling. Readers consistently name these as the reason they trust the
book.

## Sourcing and permissions

If the book quotes anyone, this discipline keeps it publishable:

- **Public domain first.** Pre-1929 in the US, or life plus 70 years in the UK
  and EU. Antiquity, scripture, proverbs and the Enlightenment are all free.
- **Cap in-copyright quotations** at roughly two per chapter, quoted briefly,
  always attributed. That is fair dealing for criticism and review, and it is
  the same position as any annotated anthology.
- **Mark every disputed line** as "attributed to" or "after". Four names act as
  magnets for orphaned quotations: Twain, Einstein, Churchill and the Buddha. A
  neat line under any of them deserves suspicion.
- **Put a note on attribution at the back** explaining all of the above. It
  costs two pages and it is the single strongest trust signal in the book.

## Adapting the pipeline to a new book

Almost everything is reusable. What changes:

1. `content/*.md` — the manuscript.
2. `scripts/build_site.py` — the unit's field names in `parse_chapters`, the
   `ENTRIES` and `CHAPTERS` counts, the title and subtitle, and the index
   grouping rules if sources are people.
3. `scripts/check_book.py` — the expected counts.
4. `scripts/build_print.py` — `IMPRINT` (author, publisher, ISBN, whether the
   name goes on the cover art), `TITLE`, `TRIMS` if not 5.5 × 8.5.
5. `scripts/build_print_cover.py` and `build_epub.py` — the palette and blurb.

Do not rewrite the typesetting, the gates, or the EPUB assembly. They took
longer than they look and they encode the traps in `references/pipeline.md`.

## Publishing

`references/publishing.md` holds the print and KDP specifics: trim, gutter by
page count, bleed, the two paper calipers, the barcode reservation, and the KDP
form field by field including the description-box trap and the keyword slot
people routinely waste. Read it before generating upload files or advising on a
listing.
