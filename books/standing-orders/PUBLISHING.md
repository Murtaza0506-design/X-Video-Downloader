# Standing Orders — specification and publishing

Ninety-nine rules across eleven chapters, in four parts. Built from
`books/standing-orders/content/*.md`.

```sh
./books/standing-orders/build.sh   # everything, with all three preflights
```

Every figure below is measured off the files.

---

## 1. The files

| File | What it is | Size |
|---|---|---|
| `print/interior.pdf` | the book block | 5.5 × 8.5 in, 110 pages |
| `print/cover-cream.pdf` | wrap cover for **cream** stock | 11.5250 × 8.7500 in |
| `print/cover-white.pdf` | wrap cover for **white** stock | 11.4977 × 8.7500 in |
| `ebook/standing-orders.epub` | reflowable EPUB 3 | 23 documents |
| `ebook/cover.jpg` | the store cover | 1600 × 2560, 1:1.6 |
| `site/index.html` | the web reading edition | the book on a desk |
| `entries.csv` | all 99 rules as a flat table | one row per rule |

## 2. Interior

| | |
|---|---|
| Trim | **5.5 × 8.5 in** (139.7 × 215.9 mm) |
| Pages | **110** (6 front, 104 body) |
| Bleed | none |
| Colour | black only, verified neutral on every sampled page |
| Margins | inside 0.80 in · outside 0.60 · top 0.72 · bottom 0.71, mirrored |
| Text face | EB Garamond, 10.5 pt on 14.6 pt, four faces embedded and subset |
| Entries | 99 rules · 19 sources · 11 chapters in 4 parts |
| Back matter | A Note on This Book · Index of Sources · colophon |

The unit is not a quotation. Each entry is a **rule**, the **source** it came
from, **what it buys you**, and **what ignoring it costs**, and the last of
those four is the book. Nothing is quoted from outside the fiction, so the
index files each source under the phrase as written (`BOOK_INDEX_PEOPLE=0`):
*the Bracewell standing orders* files under B, not under *orders, Bracewell
standing*.

## 3. Cover

| | cream | white |
|---|---|---|
| **Spine** | **0.2750 in** | **0.2477 in** |
| **Full wrap** | **11.5250 × 8.7500 in** | **11.4977 × 8.7500 in** |

Bleed 0.125 in on all four outer edges, safe margin 0.25 in, a 2.0 × 1.2 in
barcode rectangle reserved on the back. Field-green boards (#3E4A3C →
#151B14), bone type. The author's name is not on the front board.

---

## 4. KDP

### Kindle eBook

| KDP field | What to enter |
|---|---|
| **Language** | English |
| **Book Title** | `Standing Orders` |
| **Subtitle** | `Ninety-nine rules for staying alive after the outbreak, and what each one costs` |
| **Author** | Primary: `Murtaza` · Last: `Raza` |
| **Manuscript** | `ebook/standing-orders.epub` |
| **Cover** | `ebook/cover.jpg` — **Upload a cover you already have**, not Cover Creator |

Description:

```html
<h4>Seven rules were nailed to the door of a milking parlour in the first spring. Boil it. Don't shout. Two doors.</h4>
<p>By the third winter there were ninety-nine, and the man keeping the list had stopped writing down anything he had not watched cost somebody something.</p>
<p>Ninety-nine rules for staying alive after the outbreak. Each one carries the name of whoever paid for it, what keeping it buys you, and, in the paragraph that matters, what ignoring it costs.</p>
<h4>Eleven chapters, in four parts</h4>
<p>The First Hour · Leaving · Noise, Light and Smell · Water and Waste · Wounds and Fever · Food and the Long Hunger · Ground You Can Hold · Strangers · Living in a Group · Winter · When to Break a Rule</p>
<ul>
<li><b>The rules contradict each other, and the book says so.</b> One tells you to keep the ground you know. Another tells you the place is worth less than the people in it. Both halves of every pair were written by people who were right where they stood.</li>
<li><b>Nobody here failed to what was outside the wall.</b> They failed over the rota, over who counted the stores, over a grievance nobody raised for a fortnight.</li>
<li><b>Every chapter ends with a rule that lets you off.</b> Permission to stand down, to stay put, to stop treating and start comforting, to spend the winter doing nothing.</li>
<li><b>The dead are not the subject.</b> Water is. More people in this valley died of what was in a jug on a table than of anything that came up the lane.</li>
</ul>
<p>The last chapter is about when to break the rules, and about a man who wrote three of them and was right about all three and is dead. It is the shortest chapter in the book and the reason for the other ten.</p>
```

Keywords:

```
post apocalyptic survival fiction
zombie outbreak novel
british dystopian fiction
found document fiction
quiet literary horror
societal collapse story
survival handbook novel
```

Categories:

```
Fiction > Science Fiction > Post-Apocalyptic
Fiction > Horror > Suspense
Fiction > Literary
```

Pricing: all territories, decline KDP Select unless you want Kindle Unlimited,
**70% royalty**, **£4.99 / $5.99**.

### Paperback

*Create Paperback* from the finished Kindle title. Black & white interior on
**cream**, **5.5 × 8.5 in**, **no bleed**, **matte**. Upload
`print/interior.pdf` and `print/cover-cream.pdf`. List at **£8.99 / $11.99**.

The previewer will flag the missing bleed. That is intended: nothing runs to
the edge.

---

## 5. A note on the subject matter

This one is fiction, and it is shaped like a manual, which is a combination
that needs handling in the listing as well as in the book.

Every person, place, camp and document credited in the index is invented, and
the rules are written to be true inside their own world and repeatable by
frightened people, not to be correct in ours. Several are kept precisely
because they are the sort of thing survivors would believe. *A Note on This
Book* says all of that at the back, in the author's own voice rather than the
narrator's, and points the reader at real first aid, water treatment and civil
emergency guidance instead.

Keep that note in the sample. It is the back matter, so set the Kindle sample
to open at the introduction and leave the note where it is, but do not cut it
from any edition. The book should never be mistakeable for advice, and the
listing should not be written in a way that invites the mistake either: the
description above sells it as a novel, and the categories are all fiction.
