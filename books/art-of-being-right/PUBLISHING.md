# The Art of Being Right — specification and publishing

One hundred and forty-four moves across twelve chapters, in four parts. Built
from `books/art-of-being-right/content/*.md`.

```sh
./books/art-of-being-right/build.sh    # everything, with all three preflights
```

Every figure below is measured off the files.

---

## 1. The files

| File | What it is | Size |
|---|---|---|
| `print/interior.pdf` | the book block | 5.5 × 8.5 in, 120 pages |
| `print/cover-cream.pdf` | wrap cover for **cream** stock | 11.5500 × 8.7500 in |
| `print/cover-white.pdf` | wrap cover for **white** stock | 11.5202 × 8.7500 in |
| `ebook/the-art-of-being-right.epub` | reflowable EPUB 3 | 24 documents |
| `ebook/cover.jpg` | the store cover | 1600 × 2560, 1:1.6 |

## 2. Interior

| | |
|---|---|
| Trim | **5.5 × 8.5 in** (139.7 × 215.9 mm) |
| Pages | **120** |
| Bleed | none |
| Colour | black only, verified neutral |
| Margins | inside 0.80 in · outside 0.60 · top 0.72 · bottom 0.71, mirrored |
| Text face | EB Garamond, 10.5 pt on 14.6 pt, four faces embedded and subset |
| Back matter | A Note on Sources · Index of Moves · colophon |

## 3. Cover

| | cream | white |
|---|---|---|
| **Spine** | **0.3000 in** | **0.2702 in** |
| **Full wrap** | **11.5500 × 8.7500 in** | **11.5202 × 8.7500 in** |

Bleed 0.125 in on all four outer edges, safe margin 0.25 in, a 2.0 × 1.2 in
barcode rectangle reserved on the back. Blue boards (#25455A → #0D1F2B).

---

## 4. KDP

### Kindle eBook

| KDP field | What to enter |
|---|---|
| **Language** | English |
| **Book Title** | `The Art of Being Right` |
| **Subtitle** | `One hundred and forty-four ways an argument is won unfairly, and what to say back` |
| **Author** | Primary: `Murtaza` · Last: `Raza` |
| **Manuscript** | `ebook/the-art-of-being-right.epub` |
| **Cover** | `ebook/cover.jpg` — not Cover Creator |

Description:

```html
<h4>Somebody changed the subject and you did not notice for ten minutes.</h4>
<p>Somebody cited a study that does not exist. Somebody said "with respect" and then said something else entirely, and by the time you worked out what had happened, the room had moved on.</p>
<p>This is a catalogue of one hundred and forty-four ways an argument is won without being right. Each one is a line you would actually hear, the name of the move underneath it, why it works on people rather than why it is invalid, and something to say back.</p>
<h4>Twelve chapters, arranged by the shape of the move</h4>
<p>Changing the subject · Rigging the terms · The straw man and his family · Playing the man · Borrowed authority · Purity tests · Numbers that lie · Weaponising doubt · False choices · Emotional leverage · Running out the clock · When you are the one doing it</p>
<ul>
<li><b>The replies are deliberately unimpressive.</b> Almost none of them are clever, because cleverness escalates and escalation is how you lose a room.</li>
<li><b>Nearly all of them do the same two things.</b> Concede whatever is true, at once and without reluctance, then put the original question back on the table.</li>
<li><b>It assumes good faith for longer than feels natural.</b> Perhaps half of these moves are committed by people who are tired, not dishonest.</li>
</ul>
<p>The last chapter is about the moves you use yourself. It is the reason the book exists.</p>
```

Keywords:

```
how to win an argument
logical fallacies explained
what to say to a bad argument
critical thinking for everyday life
rhetoric and persuasion
dealing with difficult people at work
debate techniques for beginners
```

Categories:

```
Philosophy > Logic & Language
Self-Help > Communication & Social Skills
Reference > Words, Language & Grammar > Rhetoric
```

Pricing: 70% royalty, **£4.99 / $5.99**.

### Paperback

*Create Paperback* from the finished Kindle title. Black & white interior on
**cream**, **5.5 × 8.5 in**, **no bleed**, **matte**. Upload
`print/interior.pdf` and `print/cover-cream.pdf`. List at **£8.99 / $11.99**.

The previewer will flag the missing bleed. That is intended: nothing runs to
the edge.
