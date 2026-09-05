#!/bin/sh
# Build Confident and Wrong. Same pipeline as the other three; only the
# manuscript, the unit's labels and the strings differ.
set -e
export BOOK_CONTENT="books/confident-and-wrong/content"
export BOOK_GLOSS1="What happened"
export BOOK_GLOSS2="What the error was made of"
export BOOK_CHAPTERS=12
export BOOK_PER_CHAPTER=10
export BOOK_TITLE="Confident and Wrong"
export BOOK_TITLE_LINES="Confident|and Wrong"
export BOOK_SUBTITLE="A hundred and twenty predictions made by people who knew better, and what the mistake was made of."
export BOOK_SUBTITLE_LINES="A hundred and twenty predictions made by people|who knew better, and what the mistake was made of."
export BOOK_AUTHOR="Murtaza Raza"
export BOOK_NOTE_TITLE="A Note on Quotation"
# The attribution carries a date, which must not become the sort key.
export BOOK_INDEX_TITLE="Index of People"
export BOOK_INDEX_STRIP=",[^,]*[0-9]{4}[^,]*$"
export BOOK_ANON_HEADING="Unsigned and institutional"
export BOOK_COLOPHON="A hundred and twenty predictions across twelve chapters,<br>each one made by somebody in a position to know."
export BOOK_EYEBROW="A history of certainty"
export BOOK_C1="#8A5A1E"; export BOOK_C2="#6B4315"; export BOOK_C3="#412608"
export BOOK_SLUG="confident-and-wrong"
export BOOK_BLURB_FILE="books/confident-and-wrong/content/blurb.txt"
export BOOK_PULL="Almost nobody in this book was stupid. That is the whole difficulty: they were the people best placed to know."
export BOOK_SPEC_Q="Heavier-than-air flying machines are impossible."
export BOOK_SPEC_A="Lord Kelvin, 1895"
export BOOK_SPEC_U="Kelvin was not guessing. He was the most eminent physicist in Britain, and he was reasoning from the power-to-weight ratios of the engines he knew about, which were steam."
export BOOK_TAG="120 predictions · 12 chapters · 4 parts"
export BOOK_FOOT="120 predictions · 12 chapters"
export BOOK_ID="urn:uuid:9d4f61a2-7c38-4e15-b0a6-58e2f7c41b03"
export BOOK_OUT_FRAGMENT="books/confident-and-wrong/book.html"
export BOOK_OUT_SITE="books/confident-and-wrong/site/index.html"
export BOOK_OUT_CSV="books/confident-and-wrong/entries.csv"
export BOOK_PRINT_OUT="books/confident-and-wrong/print"
export BOOK_EPUB_OUT="books/confident-and-wrong/ebook"
mkdir -p "$BOOK_PRINT_OUT" "$BOOK_EPUB_OUT"
python3 scripts/build_site.py
python3 scripts/check_book.py
python3 scripts/build_print.py
python3 scripts/build_print_cover.py
python3 scripts/check_print.py
python3 scripts/build_epub.py
python3 scripts/check_epub.py
