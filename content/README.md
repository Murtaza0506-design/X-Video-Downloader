# The book — status

A digital book of quotations for a general adult audience. Every quotation is
paired with a plain-English explanation and a concrete instruction for using it
in ordinary life. The value is in the commentary, not the collection.

Working title: **Lines Worth Keeping**. Placeholder, chosen for the manuscript
heading. Change it in `scripts/build_book.py`.

## What exists

| | Target | Actual |
|---|---|---|
| Chapters | 16 | 16 |
| Entries | 240 | 240 |
| Words | ~32,000 | ~35,300 |
| Distinct sources | — | 130 |

All sixteen chapters are drafted: a ~300 word opening plus fifteen entries each,
in the format set by Chapter 9. Front and back matter are written. Nothing is
outstanding on the writing side.

## Files

```
content/00-introduction.md          how to read it, why entries contradict
content/01..16-*.md                 the chapters, one file each
content/90-note-on-attribution.md   why so many quotations belong to nobody
content/91-index-of-sources.md      GENERATED — do not edit by hand
manuscript.md                       GENERATED — every chapter in reading order
scripts/build_book.py               rebuilds both generated files
```

Front matter on each chapter carries `part`, `chapter` and `title`, ready for a
static site generator to consume.

After editing any chapter:

```
python3 scripts/build_book.py
```

## Prose style

Every chapter was revised against `STYLE.md`, which is derived from Provost on
sentence rhythm, Zinsser on clutter and hedging, Orwell's six rules, Le Guin on
hearing your own prose, and published work on what makes machine-written text
identifiable. That last body of research is the reason the targets are numeric:
the signature of generated prose is low variance held steady across a whole
document, and a book of 240 near-identical units is the worst possible case for
it. The format repeats by design, so the prose inside it has to move.

`scripts/measure_style.py` reports the numbers; `scripts/lint_prose.py` flags
individual hedges and adverbs with context for cutting.

## Conventions used throughout

- Second person. Ordinary British examples: queues, group chats, GP appointments,
  builders' quotes. No boardrooms, no battlefields.
- Four parts per entry, always in the same order: quotation, attribution,
  **What it means**, **How to use it**.
- Em dashes are kept out of the prose. Chapter 9 was rewritten to match; its
  content is otherwise unchanged from the original sample.
- Entries contradict each other across chapters, on purpose.
- Most chapters end with an **exit entry** giving the reader permission to stop:
  to leave the grievance unforgiven, to stay angry about ageing, to put the book
  down. Advice without a limit becomes pressure.

## Copyright position

Weighted heavily toward pre-1929 material: Stoics, Aesop, Shakespeare, the Bible,
proverbs, Enlightenment writers. Quotations from authors still in copyright are
capped at two per chapter, kept to a sentence, and always attributed.

Chapter 9 is the one exception, at three (Sinclair, Covey, Saint-Exupéry). It came
from the original sample and was left as written. Saint-Exupéry and Valéry (ch 13)
both died in the 1940s and are out of copyright in the UK and most of the EU under
life plus seventy.

Verify before publishing. **This is not legal advice** — the original handover
recommends an hour with a lawyer, and that recommendation stands.

## Not started

The website. No decisions have been made on stack, reading model, monetisation,
search or favourites, and the handover asks that these be put to the owner rather
than assumed. The content pipeline is ready for whatever gets chosen: markdown
per chapter, front matter for chapter and part, generated index.
