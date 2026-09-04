# What to Say — specification and publishing

Sixty letters across twelve chapters, in six parts. Built from
`books/what-to-say/content/*.md` by the same pipeline as the other two books.

```sh
./books/what-to-say/build.sh      # everything, with all three preflights
```

Every figure below is measured off the files, not estimated.

---

## 1. The files

| File | What it is | Size |
|---|---|---|
| `print/interior.pdf` | the book block | 5.5 × 8.5 in, 100 pages |
| `print/cover-cream.pdf` | wrap cover for **cream** stock | 11.5000 × 8.7500 in |
| `print/cover-white.pdf` | wrap cover for **white** stock | 11.4752 × 8.7500 in |
| `ebook/what-to-say.epub` | reflowable EPUB 3 | 26 documents |
| `ebook/cover.jpg` | the cover Amazon shows in the store | 1600 × 2560, 1:1.6 |

Send a printer the interior and **one** cover, the one matching the paper. The
two differ only in spine width, because the papers are different thicknesses.

---

## 2. Interior

| | |
|---|---|
| Trim | **5.5 × 8.5 in** (139.7 × 215.9 mm) |
| Pages | **100** |
| Bleed | none. Nothing runs to the edge, so the block is supplied at trim size |
| Colour | black only, verified neutral on every sampled page |
| Margins | inside 0.80 in · outside 0.60 · top 0.72 · bottom 0.71, mirrored |
| Text face | EB Garamond, 10.5 pt on 14.6 pt, four faces embedded and subset |
| Letters | ranged left, spaced between paragraphs, so a letter reads as a letter and not as a block of commentary |
| Front matter | 6 pages in lower-case roman: half title, blank, title, copyright, contents |
| Back matter | A Note on Using These · Index of Situations · colophon |

Every part title and every chapter opens on a right-hand page. Blank versos
carry no running head and no folio.

Spine text is permitted by KDP at 100 pages or more. At exactly 100 it is
allowed, but if you edit the manuscript and the count drops, rebuild the
covers: `check_print.py` fails loudly if the spine and the page count drift.

## 3. Cover

| | cream | white |
|---|---|---|
| Caliper per leaf | 0.0025 in | 0.002252 in |
| **Spine** | **0.2500 in** | **0.2252 in** |
| **Full wrap** | **11.5000 × 8.7500 in** | **11.4752 × 8.7500 in** |

Bleed 0.125 in on all four outer edges; safe margin 0.25 in inside every trim
edge; a clear 2.0 × 1.2 in rectangle reserved for the barcode in the lower
outer corner of the back cover. Green boards (#3E5540 → #1A2820), cream type.
The author's name is deliberately not on the front board.

## 4. Kindle edition

Reflowable EPUB 3, no embedded fonts, en-GB, EPUB 3 `nav.xhtml` plus a legacy
`toc.ncx`, 130 internal links all resolving. The index lists entry numbers
instead of page numbers, and every number is a link to that letter.

---

## 5. KDP, field by field

### Kindle eBook

| KDP field | What to enter |
|---|---|
| **Language** | English |
| **Book Title** | `What to Say` |
| **Subtitle** | `Sixty letters for the moments nobody teaches you how to write` |
| **Author** | Primary: `Murtaza` · Last: `Raza` |
| **Publishing Rights** | *I own the copyright and hold the necessary publishing rights* |
| **Manuscript** | `ebook/what-to-say.epub` |
| **Cover** | `ebook/cover.jpg` — **Upload a cover you already have**, not Cover Creator |

Description, pasted in as it is:

```html
<h4>Somebody at work has lost their father and you have been staring at an empty message box for two days.</h4>
<p>A friend has been diagnosed with something serious. You owe an apology you have been avoiding for a month, you need to ask for money, or you have to say no to somebody who will take it badly.</p>
<p>These are the letters nobody teaches you to write, and the reason they go unwritten is almost never that people do not care. It is the fear of getting it wrong, which produces the one outcome that is certainly wrong.</p>
<h4>Sixty letters, written out in full</h4>
<p>Condolence · Illness and other people's bad news · Apologising properly · Owning it at work · Asking · Chasing · Declining · Ending it · Money between people · Money with institutions · Praise and thanks · Letters with no purpose</p>
<p>Each one comes with the situation it answers and a short note on what is actually doing the work: which sentence carries the weight, what has deliberately been left out, and why the paragraph you would have added is the one to cut.</p>
<ul>
<li><b>They are shorter than you would have written.</b> The instinct under pressure is to add. Almost every letter here got better when a paragraph came out of it, and the paragraph that came out was the one about the writer.</li>
<li><b>The hard ones are not softened.</b> Three chapters contain letters the recipient will not enjoy. A refusal blurred until it can be read as a maybe has failed at the only thing it was for.</li>
<li><b>Nothing is a template.</b> Every name and detail is invented, and the note under each letter tells you what is transferable and what is not.</li>
</ul>
<p>The last chapter is about the letters that have no purpose at all: the ones written for no reason, the thanks owed to somebody still alive, the letter meant to be opened afterwards, and the one you never send.</p>
<p><i>Those are the ones people keep.</i></p>
```

Keywords, one per slot:

```
what to say when someone dies
condolence letter examples
how to apologise properly
difficult conversations at work
letter writing guide
how to say no politely
sympathy message wording
```

Categories:

```
Reference > Writing, Research & Publishing Guides
Self-Help > Communication & Social Skills
Business & Money > Business Life > Etiquette
```

Rights and pricing: all territories; decline KDP Select unless you want Kindle
Unlimited; **70% royalty**; **£3.99 / $4.99**. It is a short, high-utility
book, and the 70% band starts at £1.77 / $2.99.

### Paperback

Use *Create Paperback* from the finished Kindle title so the two link on one
product page.

| KDP field | What to enter |
|---|---|
| **ISBN** | *Get a free KDP ISBN* |
| **Print options** | Black & white interior, **cream** paper |
| **Trim size** | **5.5 × 8.5 in** |
| **Bleed** | **No bleed** |
| **Cover finish** | **Matte** |
| **Manuscript** | `print/interior.pdf` |
| **Cover** | `print/cover-cream.pdf` (or `cover-white.pdf` if you pick white) |
| List price | **£7.99 / $9.99**. Check the printing cost KDP shows and keep the royalty above about £2 |

The previewer will flag that the interior has no bleed. That is correct and
intentional: nothing runs to the edge. Accept it and continue.

---

## 6. What is still blank

`IMPRINT` at the top of `scripts/build_print.py` holds the author, and leaves
the publisher and the ISBN empty. Neither is needed to publish. Fill either in
and rebuild; nothing else needs touching.
