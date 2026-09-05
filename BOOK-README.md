# Lines Worth Keeping

By Murtaza Raza. A commonplace book of 315 quotations. Every line comes with what it actually
means, in plain English, and one specific place to put it.

**Read it: https://murtaza0506-design.github.io/X-Video-Downloader/**
(the workflow publishes to `gh-pages`; the address works once Pages is switched
on for the repository, under Settings > Pages > Deploy from a branch >
`gh-pages` / `(root)`)

It opens as a book on a desk. Drag the background to turn it in space, drag the
cover to open it, and fold a page over by its corner. Wheel or pinch to zoom.

On a phone the screen is too narrow to hold a whole spread at a readable size,
so the book is framed one page at a time and drawn twice as large. The type is
not re-set for the screen: page 41 holds the same words everywhere, and a swipe
steps across the spread and then turns the leaf.

## What is in it

315 entries across 21 chapters, arranged by the problem you have rather than the
century it came from: starting before you feel ready, when things go wrong,
anger, worry, wanting less, listening, saying the hard thing, being wronged,
persuading, being wrong in public, starting, keeping going, stopping, time,
getting older, and what actually matters.

151 distinct sources, weighted heavily toward material that is out of copyright:
the Stoics, Aesop, Shakespeare, the Bible, Enlightenment writers, and proverbs.
Quotations from authors still in copyright are capped at roughly two per chapter,
kept to a sentence, and always attributed. Disputed or paraphrased lines are
marked *attributed to* or *after*, and there is a note at the back on why so many
famous quotations belong to nobody in particular.

## How it is built

The manuscript is the source of truth. `content/*.md` holds one file per chapter;
everything else is generated from it, so the published book cannot drift from the
text.

```
content/                one markdown file per chapter, plus front and back matter
scripts/build_site.py   parses the manuscript, derives the source index, builds the book
scripts/book_template.html   markup, styles and behaviour
scripts/check_book.py   fails the build if the manuscript is not intact
site/index.html         GENERATED - the published book
book.html               GENERATED - the same book as an embeddable fragment
manuscript.md           GENERATED - the whole text in reading order
book-entries.csv        GENERATED - all 315 entries as a flat table
STYLE.md                the prose rules, with the measurements behind them
```

Rebuild after editing any chapter:

```
python3 scripts/build_site.py
python3 scripts/check_book.py
```

Every push to `main` rebuilds the book and republishes it, after the check
confirms 21 chapters, 315 entries, no chapter repeating a source back to back,
and no em dashes in the prose.

## Other books built from the same pipeline

`scripts/` is shared. Each book in `books/` carries its own manuscript, its own
`build.sh` with the strings and the unit's field names in it, and its own
`PUBLISHING.md`. Building one never touches another, and every push checks all
four manuscripts.

| Book | The unit | Shape |
|---|---|---|
| `books/art-of-being-right` | the move · why it works · what to say back | 144 in 12 chapters |
| `books/confident-and-wrong` | the prediction · what happened · what the error was made of | 120 in 12 chapters |
| `books/what-to-say` | the situation · the letter · the two sentences doing the work | 60 in 12 chapters |
| `books/zombie-apocalypse` | the rule · why it works · how it goes wrong | 99 in 9 chapters |

Build any of them from the repository root:

```
sh books/zombie-apocalypse/build.sh
```

That runs the four builders and the three preflight gates: manuscript
structure, print geometry and colour, then EPUB container and links.

## A note on the quotations

Short attributed quotations are ordinary use, but this is a book whose substance
is the quotations, which is a weaker position than one that quotes in passing.
The material is weighted to pre-1929 sources for that reason. This is not legal
advice, and anyone publishing it commercially should take an hour with a lawyer
first.
