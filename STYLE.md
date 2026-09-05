# Style guide

Derived from craft sources, then turned into numbers that can be measured against
the manuscript. Run `python3 scripts/measure_style.py` after editing.

## What the sources say

**Gary Provost, *100 Ways to Improve Your Writing*.** The famous passage: five-word
sentences are fine, "but several together become monotonous." The ear demands
variety. Mix short sentences, medium ones, and occasionally a sentence of
considerable length that burns with energy and builds like a crescendo. Prose has
rhythm or it has nothing.

**Ursula Le Guin, *Steering the Craft*.** A sentence's first duty is coherence, its
second is rhythm. You control rhythm by hearing it. Read it aloud or you are
guessing.

**William Zinsser, *On Writing Well*.** Clutter is the disease. Strip every sentence
to its cleanest components. He names the enemy directly: "a bit," "a little," "sort
of," "kind of," "rather," "quite," "very," "in a sense." Every little qualifier
whittles away a fraction of the reader's trust. Most adverbs are clutter, above all
the ones repeating a meaning the verb already carries.

**George Orwell, "Politics and the English Language."** Never use a long word where a
short one will do. If a word can be cut, cut it. Prefer the active. Never use a
stale metaphor you are used to seeing in print.

**Research on detecting machine-written prose.** The signature is low burstiness:
models hold a near-constant sentence length and rhythm across a whole document,
where humans swing between short punchy sentences and long constructions. The other
markers are repetitive hedging, repeated transitional phrases, structural
predictability, generic terminology, shallow specificity, and a voice that does not
change between sections.

That last finding is the important one for a book of 315 near-identical units. The
format repeats by design, so the prose inside it has to vary or the whole thing
reads as machine output.

## Targets

| Measure | First draft | Target | 16 chapters | 21 chapters | |
|---|---|---|---|---|---|
| Hedges per 1,000 words | 13.9 | under 6 | 4.5 | **3.9** | met |
| `-ly` adverbs per 1,000 | 19.8 | under 13 | 10.5 | **10.2** | met |
| Sentence-length stdev | 7.9 | over 9.5 | 9.2 | **9.1** | close |
| Sentences of 8 words or fewer | 26.3% | 28–38% | 33.0% | **32.9%** | met |
| Sentences of 30 words or more | 4.5% | 6–12% | 6.3% | **6.3%** | met |
| Spread of mean length across chapters | 2.9 | over 4 | 3.6 | **3.6** | close |

The fourth column is the original sixteen chapters; the fifth is the book as it
now stands, with envy, friendship, being alone, rest and money added. The five
new chapters were drafted, measured, and then revised against these numbers:
the first pass came in at 5.1 hedges per thousand and the revision took the
whole book to 3.9, below where it was before they were written.

Two targets are still narrowly missed and have been left alone. Both could be
hit by padding sentences out, which would serve the number and not the reader.
Per chapter the stdev runs from 7.9 to 10.3, and mean sentence length from 12.1
to 15.6, so the voice does move between chapters even where the aggregate falls
short.

## The other books measured against the same targets

The pipeline now carries four books and the same script measures all of them.
The numbers are worth keeping together, because they show which targets are
house rules and which were artefacts of the first book.

| Measure | Target | Lines Worth Keeping | The Art of Being Right | Confident and Wrong | 99 Ways to Survive a Zombie Apocalypse |
|---|---|---|---|---|---|
| Hedges per 1,000 | under 6 | 3.9 | 4.8 | 3.3 | **1.5** |
| `-ly` adverbs per 1,000 | under 13 | 10.2 | 13.5 | 10.4 | **3.6** |
| Mean sentence length | around 15 | 14.0 | 15.4 | 15.4 | 15.5 |
| Sentence-length stdev | over 9.5 | 9.1 | 9.0 | 8.7 | 8.8 |
| Sentences of 8 words or fewer | 28-38% | 32.9% | 28.4% | 27.2% | 26.1% |
| Sentences of 30 words or more | 6-12% | 6.3% | 7.7% | 5.3% | 7.9% |
| Spread of mean length across chapters | over 4 | 3.6 | 3.1 | 3.7 | **6.4** |

Two things come out of putting them side by side.

The stdev target of 9.5 and the chapter-spread target of 4 have now been missed
by every book, which means they were set from one draft and not from anything
achievable. The spread target is the one worth keeping and chasing: the zombie
book is the only one to clear it, and it clears it because chapter 1 was cut
down on purpose to a mean of 11.6 to enact the line in its own opening about
reading it fast, while chapter 5 sits at 18.1. That is voice moving between
chapters, and it was a deliberate edit rather than a lucky one.

The fourth book's first draft came in at a mean of 22.9 words with 32.5% of its
sentences over thirty, which is far outside anything in this table and was the
worst first draft of the four. Four passes of splitting long sentences brought
it to 15.5 and 7.9%. The technique that fixed both numbers at once was to split
towards a short punch rather than into two mediums: a fifty-word sentence
becomes a thirty and a five, not two twenty-fives. Padding was never used, and
the sub-eight-word share is still a point and a half under the band as a result,
which is the right trade.

### Why the numbers matter here

Hedges were the worst of it. The first draft used "rather" 78 times, "usually"
50, "actually" 45, "genuinely" 26. Every one of them was a small apology for the
sentence it sat in. Cutting them is most of the difference between the draft and
this version.

## Rules

1. **Vary the length on purpose.** Every entry gets at least one sentence under six
   words. Every chapter opening gets at least one over thirty.
2. **Delete the hedge.** "Usually," "generally," "genuinely," "actually," "rather,"
   "quite," "somewhat." State the claim or don't. Keep a hedge only where the
   uncertainty is the point.
3. **Cut adverbs that repeat the verb.** Not "shouting loudly."
4. **Concrete beats abstract.** Not "a difficult conversation with a colleague" but
   the specific thing: the 8.40 stand-up, the quote from the builder, the WhatsApp
   group with your sisters in it.
5. **Fragments are allowed.** Used for emphasis, not by accident.
6. **No stale metaphor.** If you have seen the phrase in print, cut it.
7. **Let chapters differ.** Ch 3 on anger runs short and clipped. Ch 15 on ageing
   runs long and slow. The statistics per chapter should not match.
8. **Read it aloud.** Anything you stumble over gets rewritten.
9. **No em dashes in the prose.** House rule, kept from the original brief.

## Sources

- Provost, *100 Ways to Improve Your Writing* — https://www.goodreads.com/quotes/373814-this-sentence-has-five-words-here-are-five-more-words
- Le Guin, *Steering the Craft* — https://www.goodreads.com/work/quotes/717892-steering-the-craft-exercises-and-discussions-on-story-writing-for-the-l
- Zinsser, *On Writing Well* — https://www.goodreads.com/work/quotes/1139032-on-writing-well-the-classic-guide-to-writing-nonfiction
- Orwell's six rules — https://history201news.voices.wooster.edu/wp-content/uploads/sites/67/2020/02/orwellsrulesforwriters.pdf
- Sentence structure in human and machine text — https://www.researchgate.net/publication/393286245_SENTENCE_STRUCTURE_IN_HUMAN_AND_AI-GENERATED_TEXTS_A_COMPARATIVE_STUDY
- Stylometric markers in current models — https://www.researchgate.net/publication/398588043_Feature-Based_Detection_of_AI-Generated_Text_An_Analysis_of_Stylometric_and_Perplexity_Markers_in_Contemporary_Large_Language_Models
