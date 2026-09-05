#!/bin/sh
# Build The Art of Being Right. Same pipeline as the first book; only the
# manuscript, the unit's labels and the strings differ.
set -e
export BOOK_CONTENT="books/art-of-being-right/content"
export BOOK_GLOSS1="Why it works"
export BOOK_GLOSS2="What to say back"
export BOOK_CHAPTERS=12
export BOOK_PER_CHAPTER=12
export BOOK_TITLE="The Art of Being Right"
export BOOK_SUBTITLE="One hundred and forty-four ways an argument is won unfairly, and what to say back."
export BOOK_AUTHOR="Murtaza Raza"
export BOOK_INTRO_TITLE="Introduction"
export BOOK_NOTE_TITLE="A Note on Sources"
# The index files by move name, not by person, so it must not be inverted on
# the last word. Both are read by the web build too, so they go before it.
export BOOK_INDEX_PEOPLE=0
export BOOK_INDEX_TITLE="Index of Moves"
export BOOK_OUT_FRAGMENT="books/art-of-being-right/book.html"
export BOOK_OUT_SITE="books/art-of-being-right/site/index.html"
export BOOK_OUT_CSV="books/art-of-being-right/entries.csv"
python3 scripts/build_site.py
python3 scripts/check_book.py

# print and Kindle
export BOOK_TITLE_LINES="The Art of|Being Right"
export BOOK_SUBTITLE_LINES="One hundred and forty-four ways an argument|is won unfairly, and what to say back."
export BOOK_ANON_HEADING="Unnamed and traditional moves"
export BOOK_COLOPHON="One hundred and forty-four moves across twelve chapters,<br>catalogued from Aristotle, Schopenhauer and ordinary rooms."
export BOOK_SLUG="the-art-of-being-right"
export BOOK_PRINT_OUT="books/art-of-being-right/print"
export BOOK_EPUB_OUT="books/art-of-being-right/ebook"
export BOOK_BLURB_FILE="books/art-of-being-right/content/blurb.txt"
export BOOK_PULL="The counter to a rhetorical move is not a better one. It is a boring, specific question asked in an ordinary voice."
export BOOK_EYEBROW="A field guide to argument"
export BOOK_C1="#25455A"
export BOOK_C2="#1A3243"
export BOOK_C3="#0D1F2B"
export BOOK_SPEC_Q="So what you are saying is we should just do nothing."
export BOOK_SPEC_A="The Straw Man"
export BOOK_SPEC_U="Give the sentence, not the objection. What I am saying is we should do the first two and wait on the third. No indignation, no accusation."
export BOOK_TAG="144 moves · 12 chapters · 4 parts"
export BOOK_FOOT="144 moves · 12 chapters"
export BOOK_ID="urn:uuid:3c9f27b4-8e51-4d62-a7f3-1b6e05c8d290"
mkdir -p "$BOOK_PRINT_OUT" "$BOOK_EPUB_OUT"
python3 scripts/build_print.py
python3 scripts/build_print_cover.py
python3 scripts/check_print.py
python3 scripts/build_epub.py
python3 scripts/check_epub.py
