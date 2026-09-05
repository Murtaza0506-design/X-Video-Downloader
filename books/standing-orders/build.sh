#!/bin/sh
# Build Standing Orders. Same pipeline as the other books, but a different
# unit: the entry is a rule and its two prices, not a quotation and its
# commentary. Nothing is quoted, so the index files under the source as
# written and the back note is about the fiction rather than about attribution.
set -e
export BOOK_CONTENT="books/standing-orders/content"
export BOOK_GLOSS1="What it buys you"
export BOOK_GLOSS2="What ignoring it costs"
export BOOK_CHAPTERS=11
export BOOK_PER_CHAPTER=9
export BOOK_TITLE="Standing Orders"
export BOOK_SUBTITLE="Ninety-nine rules for staying alive after the outbreak, and what each one costs."
export BOOK_AUTHOR="Murtaza Raza"
export BOOK_INTRO_TITLE="Introduction"
export BOOK_NOTE_TITLE="A Note on This Book"
# The source line is a name or a posted document, never a quoted author, so it
# must not be inverted on its last word: Bracewell standing orders files under B.
export BOOK_INDEX_PEOPLE=0
export BOOK_INDEX_TITLE="Index of Sources"
export BOOK_OUT_FRAGMENT="books/standing-orders/book.html"
export BOOK_OUT_SITE="books/standing-orders/site/index.html"
export BOOK_OUT_CSV="books/standing-orders/entries.csv"
python3 scripts/build_site.py
python3 scripts/check_book.py

# print and Kindle
export BOOK_TITLE_LINES="Standing|Orders"
export BOOK_SUBTITLE_LINES="Ninety-nine rules for staying alive after|the outbreak, and what each one costs."
export BOOK_ANON_HEADING="Posted, unsigned"
export BOOK_COLOPHON="Ninety-nine rules across eleven chapters,<br>every one of them paid for by somebody."
export BOOK_SLUG="standing-orders"
export BOOK_PRINT_OUT="books/standing-orders/print"
export BOOK_EPUB_OUT="books/standing-orders/ebook"
export BOOK_BLURB_FILE="books/standing-orders/content/blurb.txt"
export BOOK_PULL="A rule is not advice. It is a price somebody has already paid, written down so that you do not have to pay it twice."
export BOOK_EYEBROW="A survivor's manual"
export BOOK_C1="#3E4A3C"
export BOOK_C2="#2B352A"
export BOOK_C3="#151B14"
export BOOK_SPEC_Q="Never open a door you cannot shut behind you."
export BOOK_SPEC_A="Marta Ellison"
export BOOK_SPEC_U="You will be in a room with one exit and a noise in it. The rule is not about doors. It is about the habit of counting your way out before you go in, which is the only habit that has kept anybody I know alive for three winters."
export BOOK_TAG="99 rules · 11 chapters · 4 parts"
export BOOK_FOOT="99 rules · 11 chapters"
export BOOK_ID="urn:uuid:5e2b74c1-9a03-4d68-b1f7-6c04e39a8d52"
mkdir -p "$BOOK_PRINT_OUT" "$BOOK_EPUB_OUT"
python3 scripts/build_print.py
python3 scripts/build_print_cover.py
python3 scripts/check_print.py
python3 scripts/build_epub.py
python3 scripts/check_epub.py
