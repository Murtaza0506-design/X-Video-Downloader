#!/bin/sh
# Build 99 Ways to Survive a Zombie Apocalypse. Same pipeline as the other
# three; only the manuscript, the unit's labels and the strings differ.
set -e
export BOOK_CONTENT="books/zombie-apocalypse/content"
export BOOK_GLOSS1="Why it works"
export BOOK_GLOSS2="How it goes wrong"
export BOOK_CHAPTERS=9
export BOOK_PER_CHAPTER=11
export BOOK_TITLE="99 Ways to Survive a Zombie Apocalypse"
export BOOK_TITLE_LINES="99 Ways to Survive|a Zombie Apocalypse"
export BOOK_SUBTITLE="Ninety-nine rules collected from the people who wrote them down, what each one is worth, and the place where it fails."
export BOOK_SUBTITLE_LINES="Ninety-nine rules collected from the people who wrote|them down, what each one is worth, and where it fails."
export BOOK_AUTHOR="Murtaza Raza"
export BOOK_INTRO_TITLE="How to Use This Book"
export BOOK_NOTE_TITLE="A Note on the Sources"
# The attribution carries a trade and a day count. Neither is the sort key:
# the index files under the person, from the first comma back.
export BOOK_INDEX_TITLE="Index of Names"
export BOOK_INDEX_STRIP=",.*$"
export BOOK_ANON_HEADING="Unsigned, and written on walls"
export BOOK_COLOPHON="Ninety-nine rules across nine chapters,<br>kept by people who for the most part did not last the year."
export BOOK_EYEBROW="A field manual"
export BOOK_C1="#4A5D3A"; export BOOK_C2="#33422A"; export BOOK_C3="#1C2617"
export BOOK_SLUG="zombie-apocalypse"
export BOOK_BLURB_FILE="books/zombie-apocalypse/content/blurb.txt"
export BOOK_PULL="They do not eat. They bite once and walk on. A thing that fed would have left us more survivors and far fewer of them."
export BOOK_SPEC_Q="Count the doors before you count the exits."
export BOOK_SPEC_A="Terrance Bello, locksmith, day 9"
export BOOK_SPEC_U="Bello counted eleven doors in the leisure centre and made all eleven fast. When the fire took the east stand there were eleven doors and no exits, because he had welded the difference out of the building."
export BOOK_TAG="99 rules · 9 chapters · 3 parts"
export BOOK_FOOT="99 rules · 9 chapters"
export BOOK_ID="urn:uuid:5c81f0d7-3ab4-46e2-9f11-27d6a8b45e03"
export BOOK_OUT_FRAGMENT="books/zombie-apocalypse/book.html"
export BOOK_OUT_SITE="books/zombie-apocalypse/site/index.html"
export BOOK_OUT_CSV="books/zombie-apocalypse/entries.csv"
export BOOK_PRINT_OUT="books/zombie-apocalypse/print"
export BOOK_EPUB_OUT="books/zombie-apocalypse/ebook"
mkdir -p "$BOOK_PRINT_OUT" "$BOOK_EPUB_OUT"
python3 scripts/build_site.py
python3 scripts/check_book.py
python3 scripts/build_print.py
python3 scripts/build_print_cover.py
python3 scripts/check_print.py
python3 scripts/build_epub.py
python3 scripts/check_epub.py
