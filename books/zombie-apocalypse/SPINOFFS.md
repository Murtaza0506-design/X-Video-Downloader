# Spinoffs

What this book was built to be the first of, and what is already planted in it.

## The asset is the unit, not the zombies

Worth saying before the list. The thing that makes this book work is not the
setting. It is the shape of the entry:

> **a rule, signed by somebody, with the day they were on · why it works · how
> it goes wrong**

The second gloss is the whole franchise. Every listicle on earth carries the
tip; almost none of them tells you the circumstance in which the tip kills you,
and a rule with no stated failure is a slogan. That unit is portable to any
subject where people hand each other confident advice, and the last section
below is the version of this series with no zombies in it at all.

Everything here fits the existing pipeline unchanged: a `book.json`, a
`build.sh` with the strings in it, one markdown file per chapter, and the three
gates. Nothing in `scripts/` needs touching.

---

## 1. Already planted in the manuscript

These are load-bearing gaps, put in deliberately. The compiler names each of
them as something she will not write about, which is the cheapest and most
honest way to open a door.

| Planted in | The seed |
|---|---|
| *A Note on the Sources* | "There is nothing about the coast, which is a different apocalypse with different rules, and Hana Sørensen has a notebook of her own and is welcome to it." |
| *A Note on the Sources* | "There is nothing about London." |
| *A Note on the Sources* | "There is nothing in here about children under four, because the two people who knew most about that both died in the second summer." |
| Entry 94 | Sørensen went to the coast in the fourth May and did not come back. A man called Bell returned with a letter. The letter is in the Long Room and is not quoted. |
| Entry 99 | "Bring it here, and if it is better than what is in this book then this book will be shorter next year." The mechanism for a second edition, in the compiler's own voice. |
| Entry 89 | The count of walkers is falling. Errai will not build anything on the trend. Somebody else will. |

## 2. The four strong ones

### 99 Ways to Survive the Water
**Hana Sørensen's notebook.** The Humber, the east coast, working boats out of
Paull. The strongest spinoff because the seed is explicit, the narrator is
already loved, and the setting inverts every rule in book one: a boat is a
sealed community where the door problem is absolute, the noise problem
disappears, the water problem vanishes and the food problem becomes everything.
Tides replace seasons as the engine. 9 × 11.

The turn: she is not coming back, and the reader of book one knows it before
she does.

### 99 Ways to Survive Being Rescued
**The sequel proper, and the best idea here.** The Beeston wall said *nobody is
coming*. Three words that did more work in that county than any three, and the
compiler flags twice that it is one of the four rules with no author and no
body behind it. So: somebody comes. A functioning authority arrives in the
fifth year with fuel, medicine, a register and a plan, and every rule that kept
these people alive becomes the thing that marks them as a problem. Do not open
the door. Never show them the way home. Lie about the number.

The unit survives intact and every entry can quote a rule from book one and
show it failing in the new conditions. That is a sequel that needs the first
book without repeating it. 9 × 11.

### 99 Ways to Survive London
The compiler's flattest refusal, and the reason is scale. A drift of two
thousand is book one's worst case; London's problem is drifts of six figures,
which makes distance the only tactic and turns the whole manual inside out.
Different compiler, colder voice, and the Long Room's rules arriving
second-hand and misapplied. 9 × 11, or 11 × 9 if the city wants more chapters
and shorter ones.

### 99 Ways to Be Wrong About Them
The folklore book. Every rumour that went round in the first two years, who
started it, what it cost, and what the truth turned out to be: that fire
frightens them, that running water stops them, that a fever means you are
turning, that children were being used as bait. Ivy Okonjo and the Skipton
radio log are the sources; Okonjo already did the counting in entry 72.

This is the closest sibling to *Confident and Wrong* on the same shelf, and the
two books can be sold as a pair. Unit: **the belief · what it cost · what was
actually true**. 9 × 11.

### 99 Ways to Raise a Child in It
Promoted out of the maybes by one fact from the epidemiology. Measles needs
about ninety-three per cent immunity in a population to stay away, and nothing
in this county has been vaccinated for four years, and there is now a cohort of
children born into it with no protection at all and no cold chain within two
hundred miles. Whooping cough is worse, because the protection adults think they
have has been waning since they were teenagers.

That is a second-order consequence almost nobody writes, and it is the right
size for this format: it is invisible, it is arithmetic, it arrives in year five
or six rather than year one, and it cannot be fought with anything in book one.
Ivy Okonjo is already the midwife, already carries three entries, and already
has the gap in *A Note on the Sources* held open for her. The unit does not
change. The register does: this is the book where the compiler's careful
counting stops being a comfort.

Pairs with the vaccination entry the fourth book does not have, and gives the
series its first genuine antagonist that is not a person or a corpse.

## 3. The three that need more work

- **The Long Room Ledger.** Nell Okafor's day-by-day record of the first two
  years, ending where her handwriting does. A different shape from a manual, so
  it needs a different unit (**the date · what happened · what it cost**) and
  it loses the argument structure that makes the format bearable. Beautiful and
  harder.
- **99 Ways to Survive the Fifth Winter.** A straight continuation, same
  compiler, same valley, shorter, as entry 99 promises. Cheap to write and the
  least interesting, because nothing in the world has changed. Best held back
  as a short companion volume rather than a fourth full book.

## 4. The version with no zombies in it

The unit does not need an apocalypse. Same three fields, same nine-by-eleven,
same pipeline, same gates:

- **99 Ways to Survive a Hospital** — signed by patients, porters, nurses and
  one consultant. Why the rule works, and the case where following it killed
  somebody.
- **99 Ways to Survive a Company** — the advice people actually hand each other
  at work, with the failure printed underneath. The natural sibling to *The Art
  of Being Right*.
- **99 Ways to Survive Your Own Family** — the hardest to write well and the
  one that would sell.
- **99 Ways to Survive Being New** — a first year at anything: a trade, a
  country, a prison, a ward.

Each of these is the same book with the fear swapped out, and each of them
inherits the two things that make this one work: the rules disagree with each
other and are left disagreeing, and every chapter's last entry gives the reader
permission not to follow the chapter.

---

## Practical notes for whoever writes the next one

1. **Read `CANON.md` first** and do not contradict it. Where a spinoff needs to
   break a rule of the world, break it in the text, in somebody's voice, with
   the compiler noting the disagreement. Never break it silently.
2. **Copy `build.sh` and change the strings.** Nine chapters of eleven is the
   right shape: it gives 99, it fits a 116-page paperback, and the gate checks
   the count for you.
3. **Draft, measure, revise.** `python3 scripts/measure_style.py
   'books/<slug>/content/0[0-9]*.md'`. Expect the first pass to run long; this
   book's first draft came in at a mean of 22.9 words against a house norm of
   15.4 and took four passes of splitting to land.
4. **A new cast, mostly.** Two or three names from book one crossing over is a
   pleasure. Ten is a soap opera and it stops the new book standing alone.
5. **Keep the contradiction pairs and the chapter exits.** They are the two
   things readers name as the reason they trust the book, and they are the
   first things to fall out of a draft written in a hurry.
