# 99 Ways to Survive a Zombie Apocalypse — specification and publishing

Ninety-nine rules across nine chapters, in three parts. Built from
`books/zombie-apocalypse/content/*.md`.

```sh
sh books/zombie-apocalypse/build.sh   # everything, with all three preflights
```

Every figure below is measured off the files.

---

## 1. The files

| File | What it is | Size |
|---|---|---|
| `print/interior.pdf` | the book block | 5.5 × 8.5 in, 118 pages |
| `print/cover-cream.pdf` | wrap cover for **cream** stock | 11.5450 × 8.7500 in |
| `print/cover-white.pdf` | wrap cover for **white** stock | 11.5157 × 8.7500 in |
| `ebook/zombie-apocalypse.epub` | reflowable EPUB 3 | 20 documents |
| `ebook/cover.jpg` | the store cover | 1600 × 2560, 1:1.6 |
| `site/index.html` | the web edition | self-contained |
| `entries.csv` | all 99 rules as a flat table | |

## 2. Interior

| | |
|---|---|
| Trim | **5.5 × 8.5 in** (139.7 × 215.9 mm) |
| Pages | **118** (6 front + 112 body) |
| Bleed | none |
| Colour | black only, verified neutral on every sampled page |
| Margins | inside 0.80 in · outside 0.60 · top 0.72 · bottom 0.71, mirrored |
| Text face | EB Garamond, 10.5 pt on 14.6 pt, four faces embedded and subset |
| Entries | 99 rules · 39 named sources · 9 chapters in 3 parts |
| Back matter | A Note on the Sources · Index of Names · colophon |

The index files by person, with everything after the first comma stripped from
the attribution, so that `Priya Raghunathan, A&E nurse, day 1` files under R and
not under her trade. The three sources that are not people (the Beeston wall,
the Skipton radio log, the Long Room) are filed by hand in
`content/surnames.txt`, because the rule that inverts on the last word turns a
wall into "wall, the Beeston".

## 3. Cover

| | cream | white |
|---|---|---|
| **Spine** | **0.2950 in** (7.49 mm) | **0.2657 in** (6.75 mm) |
| **Full wrap** | **11.5450 × 8.7500 in** | **11.5157 × 8.7500 in** |

Bleed 0.125 in on all four outer edges, safe margin 0.25 in, a 2.0 × 1.2 in
barcode rectangle reserved on the back. Olive boards (#4A5D3A → #1C2617), cream
type, in the register of a field manual rather than a horror novel, which is
the correct register for the contents. The author's name is not on the front
board.

The spine is thin. At 118 pages KDP will print it, but the title is set small
and there is no room for an author line; if the book grows past about 130 pages
in a later edition the spine can carry both.

---

## 3a. Positioning

The comparable title is Max Brooks, *The Zombie Survival Guide* (2003), and it
owns this shelf. Anyone browsing will have it in mind, so it is worth being
precise about where this book differs, because four of the standing criticisms
of Brooks are things this book does the other way round. That is a description,
not a disparagement: his book invented the form and this one would not exist
without it.

| The criticism of Brooks | What this book does |
|---|---|
| Falls back on "science still can't explain it", which undercuts the realist premise | The mechanism is fully specified and internally consistent, and `CANON.md` fixes it so the spinoffs cannot drift |
| Solanum has no incubation period: bitten, symptomatic and dead inside a day, which no real pathogen does | Four hours to nine days, tracking body mass and dose, which is what gives the book its bite protocol, its six-day compromise and two of its worst scenes |
| Long stretches of firearms lore, much of it wrong | There is no weapons chapter at all, and the introduction says why: killing them is what you do once the rest of the manual has failed |
| Dry, reads like a textbook | Every rule is signed by a named person with the day they were on, half of them are dead, and the rules argue with each other |

The other useful bearing is the British one. This sits in the line that runs
from Wyndham, and it is worth knowing that the standing charge against that
tradition is Aldiss's: the cosy catastrophe, where the middle-class hero has a
pretty good time while everyone else dies off. This book is built against that
charge rather than into it. The compiler counts the dead, every rule carries its
cost, and the one entry that reads like comfort is the one that gives you
permission to leave a group.

Two notes on the genre from current commentary, both of which the book is on
the right side of. The tropes readers name as exhausted are superhuman speed,
superhuman strength and stealth; these are slow, weak, loud and stopped by a
hard frost. And the observation worth remembering when an agent says zombies
are finished: readers do not get fatigued, editors do.

---

## 4. KDP

### Kindle eBook

| KDP field | What to enter |
|---|---|
| **Language** | English |
| **Book Title** | `99 Ways to Survive a Zombie Apocalypse` |
| **Subtitle** | `Ninety-nine rules collected from the people who wrote them down, what each one is worth, and the place where it fails` |
| **Author** | Primary: `Murtaza` · Last: `Raza` |
| **Manuscript** | `ebook/zombie-apocalypse.epub` |
| **Cover** | `ebook/cover.jpg` — **Upload a cover you already have**, not Cover Creator |

Description:

```html
<h4>They do not eat. They bite once and walk on.</h4>
<p>That is why almost everybody bitten lived long enough to turn, and why there are so many of them and so few of us. They are slower than you. They never stop. In a hard frost they stand still in the road like furniture, and in August they are quick and falling apart, and the difference between those two facts is the difference between a working season and a season you survive.</p>
<p>Ninety-nine rules for staying alive, collected out of eleven hundred notebooks by the woman who runs the Long Room, and set down with what each rule is worth and the exact place where it fails.</p>
<h4>Nine chapters, in three parts</h4>
<p>The first hour · What you believe · Moving · Doors, and where you sleep · Noise · Water, food, and teeth · Other people · The group · The long middle</p>
<ul>
<li><b>Every rule has a body attached.</b> Under each one is the failure: how far you can walk before your feet decide the matter, why the fire doors were the wrong fight, which sounds carry two miles and which cannot be heard at forty feet.</li>
<li><b>The rules argue with each other.</b> Rule 70 says the door never opens. Rule 77 was written by a woman who has opened hers every time she has been asked, for four years, and whose settlement is the largest in the valley. Both are printed in full and neither is arbitrated.</li>
<li><b>Every rule is signed</b>, and the signature carries the day the writer was on. The index at the back is a cast list and a memorial at the same time.</li>
<li><b>Almost nobody in it was a fool.</b> The man who welded the fire doors was a locksmith of thirty years and was reasoning correctly about intrusion.</li>
</ul>
<p>The last chapter is about the fourth year, when it stops being an emergency and becomes the place you live. It has the fewest deaths in it. It is the chapter people ask for.</p>
```

Keywords:

```
post apocalyptic fiction british
zombie survival guide fiction
found document novel
epistolary post apocalyptic
slow zombies realistic
quiet apocalypse literary horror
cosy catastrophe wyndham
```

Do not spend a keyword slot on `zombie` or on `99 ways` — both are already in
the title and the title is indexed. The slots above buy reach the title does
not already have, which is the whole point of them.

Categories:

```
Fiction > Science Fiction > Post-Apocalyptic
Fiction > Horror > Occult & Supernatural
Fiction > Literary
```

**File this as fiction.** It is written as a found manual and it is convincing
enough that a browsing reader could take it for one. The categories, the
description and the copyright page all have to say novel, and section 5 below
is why.

Pricing: all territories, decline KDP Select unless you want Kindle Unlimited,
**70% royalty**, **£4.99 / $5.99**.

### Paperback

*Create Paperback* from the finished Kindle title. Black & white interior on
**cream**, **5.5 × 8.5 in**, **no bleed**, **matte**. Upload
`print/interior.pdf` and `print/cover-cream.pdf`. List at **£8.99 / $10.99**,
a pound under the other three, because it is a shorter book and the price
should say so.

The previewer will flag the missing bleed. That is intended: nothing runs to
the edge.

---

## 5. A note on the subject matter

This is a novel. There is no Long Room, there is no Priya Raghunathan, and
nobody has ever been bitten. Every person named in it is invented, and the two
hundred and six of them were invented so that the index at the back would read
as a list of people rather than a table of contents.

It needs saying plainly here because the book works by not saying it. The
register is a real field manual, the compiler is careful, the numbers are
specific, and a reader who opens it in the middle will find a paragraph about
boiling water that is true and a paragraph about turn times that is not. That
mixture is the craft of the thing and it is also the risk of it.

Where the book touches the real world it has been kept honest, because a manual
that is wrong about the checkable parts is not convincing about the rest:

- **True and usable.** A minute at a rolling boil. Thirty yards and downhill
  between a latrine and drinking water. Sound losing six decibels per doubling
  of distance, high frequencies dying first, and night inversions carrying a
  voice two or three times as far. Protein without fat as a way to starve while
  eating. Scurvy at about three months. Dental sepsis as a killer with no
  antibiotic. March rates of twelve miles a day under load. Pack weight at
  roughly a fifth of body weight. Alarm fatigue.
- **Invented.** All of the biology: saliva-to-blood transmission, four hours to
  nine days by body mass, four miles an hour without rest, temperature
  dependence, the smell trick, and the walking-along-the-canal-bed. It is
  internally consistent and it is fiction, and `CANON.md` sets it out so that
  it stays consistent across the spinoffs.
- **Deliberately dangerous if taken as advice.** The amputation entry is
  written as a procedure with three survivors and eight graves. That ratio is
  invented and it is in the book to make a point about survivorship, not to be
  followed.

Two bodies of real evidence sit under the book and are worth naming, because
they are what keeps the invented parts from floating free.

**What actually kills people after a disaster.** The public health literature
puts diarrhoeal disease and acute respiratory infection at the top of the list,
with malnutrition, measles and untreated wounds behind them, and injury from the
event itself well down the order once the first days are past. Chapter six is
built on that finding and states it as the compiler's own count: cold, dirty
water, chests, teeth and jaws, wounds that were not cleaned, other people, and
then a long way down, them. The respiratory line is the one the chapter admits
it has no rule for, and the admission is honest rather than decorative: the
small warm room that chapter four recommends against the cold is exactly how a
cough reaches everybody in it, and no survival manual has ever squared that.

**The siege of Sarajevo, 1,425 days.** The closest documented analogue to the
long middle, and the source of the chapter nine thesis. Survivors describe the
deliberate manufacture of small normal routines, basement film screenings and
theatre, and going back to work because you cannot hide at home for four years,
and more than one account puts theatre level with food and water. That is the
argument chapter nine makes and it is not a sentimental one. It is the reason
the book ends with weddings, a tree, a haircut and a day when the names are read
out, and the reason the compiler treats an hour of uselessness as a stock to be
laid in like food.

Nothing here should be read as medical or survival instruction. The one thing
in it that is genuinely worth carrying out of the book is the shape of the
unit: every rule has a failure printed underneath it, and any rule you are
given anywhere that does not come with one has not been thought about.
