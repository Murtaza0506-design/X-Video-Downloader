# 99 Ways to Survive a Zombie Apocalypse

The manuscript. One file per chapter, numbered so they sort. Everything
published is generated from these files by the shared pipeline in
`scripts/`, so the book cannot drift from the text.

    00-introduction.md          How to Use This Book
    01..09-*.md                 nine chapters, eleven entries each
    90-note-on-attribution.md   A Note on the Sources
    blurb.txt                   back cover and store description
    surnames.txt                index filing for sources that are not people

Build from the repository root:

    sh books/zombie-apocalypse/build.sh

## The unit

Each entry is four fields:

    > "The rule, as somebody wrote it down." — Name, trade, day N

    **Why it works.** One paragraph, one line, no hard wraps.

    **How it goes wrong.** One paragraph, one line, no hard wraps.

The second gloss is the reason the book exists. Every listicle carries the
tip. None of them tells you the circumstance in which the tip kills you.

## House rules the gate enforces

Nine chapters, eleven entries each, ninety-nine total. No source twice
running inside a chapter. No em dashes anywhere except the attribution line
of an entry and the chapter heading.
