# Prose style, measured

The targets below come from craft sources turned into numbers that a script can
check. The point is not to hit numbers. It is that a book of several hundred
near-identical units cannot be assessed by reading a few of them, so the numbers
catch what reading cannot.

## Where the targets come from

**Provost** on rhythm: five-word sentences are fine, but several together become
monotonous. The ear demands variety.

**Le Guin**: a sentence's first duty is coherence, its second is rhythm, and you
control rhythm by hearing it. Read it aloud or you are guessing.

**Zinsser** on clutter, naming the enemy directly: "a bit", "a little", "sort
of", "kind of", "rather", "quite", "very", "in a sense". Every qualifier whittles
away a fraction of the reader's trust.

**Orwell**: never a long word where a short one will do; if a word can be cut,
cut it; never a stale metaphor you are used to seeing in print.

**Research on machine-written prose**: the signature is low burstiness. Models
hold near-constant sentence length across a document where humans swing between
short punchy sentences and long constructions. The other markers are repetitive
hedging, repeated transitional phrases, structural predictability, and a voice
that does not change between sections.

That last finding is the one that matters here, because the format repeats by
design. The prose inside it has to vary or the whole thing reads as output.

## Targets

| Measure | Typical first draft | Target |
|---|---|---|
| Hedges per 1,000 words | 14 | under 6 |
| `-ly` adverbs per 1,000 | 20 | under 13 |
| Sentence-length standard deviation | 8 | over 9.5 |
| Sentences of 8 words or fewer | 26% | 28–38% |
| Sentences of 30 words or more | 4.5% | 6–12% |
| Spread of mean length across chapters | 3 | over 4 |

Missing one or two narrowly is fine and better than padding sentences to serve a
number. Missing the hedge target is not fine; it is the one that most changes how
the prose reads.

## The revision loop that works

1. Draft the chapter without watching the numbers. Watching them while drafting
   produces careful, dead prose.
2. `python3 scripts/measure_style.py` and compare the new chapter to the book.
3. `python3 scripts/lint_prose.py` to get hedges and adverbs by line.
4. Revise specifically. Expect the first pass to land worse than the existing
   book. A recent set of five new chapters came in at 5.1 hedges per thousand
   against a book at 4.5; the revision took the whole book to 3.9, better than
   before the chapters were written.

## What to cut, concretely

**Hedges.** "Usually", "generally", "genuinely", "actually", "rather", "quite",
"somewhat", "very", "entirely", "simply", "mostly", "slightly". State the claim
or do not. Keep one only where the uncertainty is the point.

**Watch "rather than" separately.** It is a legitimate comparison, not a hedge,
but eight of them in one chapter is a repeated transitional phrase, which is its
own tell. Vary with "instead of", "and not", or "not X but Y".

**Adverbs that repeat the verb.** Not "shouting loudly".

**Stale metaphor.** If you have seen the phrase in print, cut it.

## Rules that are not measurable but matter

- Fragments are allowed. For emphasis, not by accident.
- Read it aloud. Anything you stumble over gets rewritten.
- Every entry gets at least one sentence under six words.
- Every chapter opening gets at least one sentence over thirty.
- Let chapters differ. The statistics per chapter should not match.
