#!/bin/sh
set -e
export BOOK_CONTENT="books/what-to-say/content"
export BOOK_GLOSS1="The letter"
export BOOK_GLOSS2="What is doing the work"
export BOOK_CHAPTERS=12
export BOOK_PER_CHAPTER=5
export BOOK_SLUG="what-to-say"
export BOOK_TITLE="What to Say"
export BOOK_TITLE_LINES="What to|Say"
export BOOK_SUBTITLE="Sixty letters for the moments nobody teaches you how to write."
export BOOK_SUBTITLE_LINES="Sixty letters for the moments|nobody teaches you how to write."
export BOOK_AUTHOR="Murtaza Raza"
export BOOK_NOTE_TITLE="A Note on Using These"
export BOOK_INDEX_PEOPLE=0
export BOOK_INDEX_TITLE="Index of Situations"
export BOOK_ANON_HEADING="General"
export BOOK_COLOPHON="Sixty letters across twelve chapters,<br>for the occasions that arrive without warning."
export BOOK_EYEBROW="Letters for hard moments"
export BOOK_C1="#3E5540"; export BOOK_C2="#2C3E2E"; export BOOK_C3="#1A2820"
export BOOK_BLURB_FILE="books/what-to-say/content/blurb.txt"
export BOOK_PULL="Everybody has a drawer of things they never sent. This is a book about sending them."
export BOOK_SPEC_Q="A colleague's father has died. You met him twice."
export BOOK_SPEC_A="Condolence, at a distance"
export BOOK_SPEC_U="Say the death out loud, offer one concrete thing, and do not ask them to reply. The commonest mistake is a letter that gives the bereaved a job."
export BOOK_TAG="60 letters · 12 chapters · 6 parts"
export BOOK_FOOT="60 letters · 12 chapters"
export BOOK_ID="urn:uuid:5b71f0c3-4a29-4e7d-9f81-2c3ea6b74d15"
export BOOK_OUT_FRAGMENT="books/what-to-say/book.html"
export BOOK_OUT_SITE="books/what-to-say/site/index.html"
export BOOK_OUT_CSV="books/what-to-say/entries.csv"
export BOOK_PRINT_OUT="books/what-to-say/print"
export BOOK_EPUB_OUT="books/what-to-say/ebook"
mkdir -p "$BOOK_PRINT_OUT" "$BOOK_EPUB_OUT"
python3 scripts/build_site.py
python3 scripts/check_book.py
python3 scripts/build_print.py
python3 scripts/build_print_cover.py
python3 scripts/check_print.py
python3 scripts/build_epub.py
python3 scripts/check_epub.py
