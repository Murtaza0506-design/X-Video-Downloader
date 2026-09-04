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

That last finding is the important one for a book of 240 near-identical units. The
format repeats by design, so the prose inside it has to vary or the whole thing
reads as machine output.

## Targets

| Measure | Before | Target | After | |
|---|---|---|---|---|
| Hedges per 1,000 words | 13.9 | under 6 | **4.5** | met |
| `-ly` adverbs per 1,000 | 19.8 | under 13 | **10.5** | met |
| Sentence-length stdev | 7.9 | over 9.5 | **9.2** | close |
| Sentences of 8 words or fewer | 26.3% | 28–38% | **33.0%** | met |
| Sentences of 30 words or more | 4.5% | 6–12% | **6.3%** | met |
| Spread of mean length across chapters | 2.9 | over 4 | **3.6** | close |

Two targets are narrowly missed and have been left alone. Both could be hit by
padding a few sentences out, which would serve the number and not the reader.
Per chapter the range now runs from a stdev of 8.1 (ch 11) to 10.3 (ch 1 and 6),
and mean sentence length from 12.1 (ch 5) to 15.6 (ch 15), so the voice does move
between chapters even where the aggregate falls short.

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
