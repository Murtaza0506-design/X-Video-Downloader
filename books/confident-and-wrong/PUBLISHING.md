# Confident and Wrong — specification and publishing

A hundred and twenty predictions across twelve chapters, in four parts. Built
from `books/confident-and-wrong/content/*.md`.

```sh
./books/confident-and-wrong/build.sh   # everything, with all three preflights
```

Every figure below is measured off the files.

---

## 1. The files

| File | What it is | Size |
|---|---|---|
| `print/interior.pdf` | the book block | 5.5 × 8.5 in, 138 pages |
| `print/cover-cream.pdf` | wrap cover for **cream** stock | 11.5950 × 8.7500 in |
| `print/cover-white.pdf` | wrap cover for **white** stock | 11.5608 × 8.7500 in |
| `ebook/confident-and-wrong.epub` | reflowable EPUB 3 | 24 documents |
| `ebook/cover.jpg` | the store cover | 1600 × 2560, 1:1.6 |

## 2. Interior

| | |
|---|---|
| Trim | **5.5 × 8.5 in** (139.7 × 215.9 mm) |
| Pages | **138** |
| Bleed | none |
| Colour | black only, verified neutral on every sampled page |
| Margins | inside 0.80 in · outside 0.60 · top 0.72 · bottom 0.71, mirrored |
| Text face | EB Garamond, 10.5 pt on 14.6 pt, four faces embedded and subset |
| Entries | 120 predictions · 118 people and institutions · 12 chapters in 4 parts |
| Back matter | A Note on Quotation · Index of People · colophon |

The index files by person, with the date stripped from the attribution so that
`Ken Olsen, 1977` files under O and not under 1977.

## 3. Cover

| | cream | white |
|---|---|---|
| **Spine** | **0.3450 in** | **0.3108 in** |
| **Full wrap** | **11.5950 × 8.7500 in** | **11.5608 × 8.7500 in** |

Bleed 0.125 in on all four outer edges, safe margin 0.25 in, a 2.0 × 1.2 in
barcode rectangle reserved on the back. Bronze boards (#8A5A1E → #412608),
cream type. The author's name is not on the front board.

---

## 4. KDP

### Kindle eBook

| KDP field | What to enter |
|---|---|
| **Language** | English |
| **Book Title** | `Confident and Wrong` |
| **Subtitle** | `A hundred and twenty predictions made by people who knew better, and what the mistake was made of` |
| **Author** | Primary: `Murtaza` · Last: `Raza` |
| **Manuscript** | `ebook/confident-and-wrong.epub` |
| **Cover** | `ebook/cover.jpg` — **Upload a cover you already have**, not Cover Creator |

Description:

```html
<h4>Eight days before the crash of 1929, the leading economist in America announced that stock prices had reached a permanently high plateau.</h4>
<p>Eight years before Kitty Hawk, the most eminent physicist in Britain explained that heavier-than-air flight was impossible. Neither man was a fool. Both were reasoning carefully from what they knew.</p>
<p>A hundred and twenty predictions that were wrong, made by people who were in an unusually good position to be right. Each one comes with what actually happened, and with the part that transfers: what the mistake was made of.</p>
<h4>Twelve chapters, in four parts</h4>
<p>Flight and other impossibilities · Nobody will want one · The ones that never arrived · The science that was closed · Doctors, certain · Safe, according to the model · A permanently high plateau · The deal they turned down · The thing that only goes up · Over by Christmas · The verdict was in · When you are the one who is certain</p>
<ul>
<li><b>It is not a book about idiots.</b> If your reaction to an entry is that the person was a fool, the entry has failed. The note underneath each one is where the finding is.</li>
<li><b>The same shapes come round again.</b> A cost that prices only the interesting part. A model fitted to a stretch of history that did not contain the event. An opponent treated as an object rather than as somebody who will respond.</li>
<li><b>The quotations are checked.</b> The famous fabrications in this genre are left out, and a note at the back says which ones and why.</li>
<li><b>Somebody usually said so first.</b> Nearly every disaster here had one person, on the record, before the event, in the file.</li>
</ul>
<p>The last chapter is about ordinary estimates made by competent people, and about the four things that are known to help. It is the least entertaining chapter in the book and the reason for the other eleven.</p>
```

Keywords:

```
famous wrong predictions
history of forecasting
why experts get it wrong
decision making under uncertainty
cognitive bias examples
business failures case studies
overconfidence in experts
```

Categories:

```
History > World
Business & Money > Management & Leadership > Decision-Making
Science & Math > History & Philosophy
```

Pricing: all territories, decline KDP Select unless you want Kindle Unlimited,
**70% royalty**, **£4.99 / $5.99**.

### Paperback

*Create Paperback* from the finished Kindle title. Black & white interior on
**cream**, **5.5 × 8.5 in**, **no bleed**, **matte**. Upload
`print/interior.pdf` and `print/cover-cream.pdf`. List at **£9.99 / $12.99**.

The previewer will flag the missing bleed. That is intended: nothing runs to
the edge.

---

## 5. A note on the subject matter

Every entry names a real person or organisation and quotes or summarises a
position they actually held. Three tests were applied throughout: the wording
is verbatim only where a contemporary source supports it, the summary form is
used where it does not, and the most famous fabricated quotations in this genre
are excluded and listed at the back with the reason. Where somebody later
retracted, the entry says so. That policy is set out in *A Note on Quotation*
and is the book's only defence against being an example of itself.
