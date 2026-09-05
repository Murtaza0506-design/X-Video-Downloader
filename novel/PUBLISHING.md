# The Handover — cover and print specification

Every figure below is measured off the built files, not estimated.

```sh
python3 novel/scripts/build_interior.py   # sets the page count
python3 novel/scripts/build_cover.py      # reads it and cuts the spine to fit
```

Run in that order. The spine is page count times paper caliper, so the cover
cannot be built correctly until the interior has been typeset.

## The files

| File | What it is | Size |
|---|---|---|
| `ebook/cover.jpg` | Kindle cover | 1600 × 2560 px, RGB, 249 KB |
| `ebook/cover.png` | the same, lossless, for reworking | 1600 × 2560 px |
| `print/cover-cream.pdf` | wrap for **cream** stock | 11.5750 × 8.7500 in |
| `print/cover-white.pdf` | wrap for **white** stock | 11.5428 × 8.7500 in |
| `print/interior.pdf` | the book block | 5.5 × 8.5 in, 130 pages |
| `cover/PHILOSOPHY.md` | the design brief the covers were built against | |

## Interior

| | |
|---|---|
| Trim | **5.5 × 8.5 in** (139.7 × 215.9 mm) |
| Pages | **130**, even, as a book block must be |
| Bleed | none |
| Colour | black only |
| Margins | inside 0.78 in · outside 0.58 · top 0.72 · bottom 0.70, mirrored |
| Text face | EB Garamond 10.5 pt on 15.1 pt, justified, hyphenated en-GB |
| Running heads | book title on verso, chapter title on recto, none on chapter openers |
| Extent | 32,874 words · 24 chapters |

## Cover

| | cream | white |
|---|---|---|
| **Spine** | **0.3250 in** (8.25 mm) | **0.2928 in** (7.44 mm) |
| **Full wrap** | **11.5750 × 8.7500 in** | **11.5428 × 8.7500 in** |

Bleed 0.125 in on all four outer edges. Nothing that matters comes within
0.25 in of a trim. Spine text is set at 11 pt with 0.07 in of clear spine
either side on the thinner of the two stocks, which is inside KDP's 0.0625 in
requirement, and spine text is permitted at all only because the book is over
100 pages.

A 2.0 × 1.2 in white rectangle is reserved in the lower outer corner of the
back board for the barcode KDP prints. If you buy your own ISBN and supply your
own barcode, delete the `barcode` block in `build_cover.py` and rebuild.

### The design

The front board is an office elevation drawn as a spreadsheet: twelve lettered
columns, rows numbered from 32 as though the sheet has been scrolled down, most
cells unlit, and one cell warm. The lit cell is **F41**, annotated `6/WEL/04`
on a hairline leader. Both of those are the novel's own coordinates and neither
is explained on the cover.

Type is Big Shoulders for the title and spine, Geist Mono for anything in the
clerk's voice, Work Sans for the back-board copy. One warm colour, spent once.

The cover was tested at 115 px wide, which is roughly the size of an Amazon
search result: at that size the title, the author and the single warm mark are
all that survive, and all three remain legible.

## KDP

### Kindle eBook

| KDP field | What to enter |
|---|---|
| **Language** | English |
| **Book Title** | `The Handover` |
| **Subtitle** | leave empty |
| **Author** | Primary: `Murtaza` · Last: `Raza` |
| **Cover** | `novel/ebook/cover.jpg` — **Upload a cover you already have**, not Cover Creator |
| **Manuscript** | not built yet, see below |

Description:

```html
<h4>There were eleven days between the first alarming Tuesday and the night the electricity stopped.</h4>
<p>The country did not panic. Quietly, individually, deniably, it got a few tins in.</p>
<p>Neil Cowie was an assistant category manager. He did crisps. He was on floor six arguing about eleven centimetres of shelf when the phones started going, and what he remembers about the walk home is that it was a beautiful day, and that some part of him was relieved.</p>
<p>What follows is a farm above a beck, a laminated sheet of rules on a parlour door, twenty-one tablets, and a decision made round a kitchen table in November that turns out, fourteen months later, to have been based on something nobody had bothered to tell anybody.</p>
<ul>
<li><b>The dead are not the subject.</b> Water is. More people in this valley died of what was in a jug on a table than of anything that came up the lane.</li>
<li><b>Nobody here fails to what is outside the wall.</b> They fail over the rota, over who counts the stores, over a grievance nobody raised for a fortnight.</li>
<li><b>Everybody gets up.</b> It does not matter how you died, and it never did, and the people who worked that out deferred the finding pending further review.</li>
</ul>
<p>A novel about ordinary competence in a world with no use for it.</p>
```

Keywords:

```
post apocalyptic survival fiction
british dystopian novel
literary zombie fiction
societal collapse story
quiet apocalypse novel
survival group dynamics
pandemic aftermath fiction
```

Categories:

```
Fiction > Science Fiction > Post-Apocalyptic
Fiction > Literary
Fiction > Horror > Suspense
```

Pricing: all territories, **70% royalty**, **£4.99 / $5.99**.

### Paperback

*Create Paperback* from the finished Kindle title. Black & white interior on
**cream**, **5.5 × 8.5 in**, **no bleed**, **matte**. Upload
`print/interior.pdf` and `print/cover-cream.pdf`. List at **£8.99 / $11.99**.

The previewer will flag the missing interior bleed. That is intended: nothing
in the book block runs to the edge.

## The one thing still missing

There is no EPUB. The paperback is complete and uploadable; the Kindle listing
has its cover but not its manuscript, because KDP needs a reflowable EPUB and
the interior PDF is not one. That is a separate build and it is not written
yet.
