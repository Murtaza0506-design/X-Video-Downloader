# The pipeline, and the traps in it

Every trap below cost real time to find. They are recorded so the next book does
not pay for them again.

## Contents

- [The builders](#the-builders)
- [The gates](#the-gates)
- [Print typesetting traps](#print-typesetting-traps)
- [EPUB traps](#epub-traps)
- [Index traps](#index-traps)

## The builders

### build_site.py

Parses `content/*.md` into structured data, derives the source index, and
injects both into `scripts/book_template.html`. Everything else imports its
`parse_chapters`, `build_index` and `front_matter`, so it is the single source
of truth for what a manuscript means.

Outputs `book.html` (a fragment, for embedding, no `<head>`) and
`site/index.html` (standalone, with doctype, charset and viewport). A file
served directly needs its own viewport meta or phones fall back to a 980px
layout viewport and every size calculation is wrong.

The chapter regex is numeric and has to widen when the book grows past its
current chapter count. Miss it and chapters silently vanish from the build.

### build_print.py

Typesets the paperback with WeasyPrint. Two documents, merged with pypdf,
because of the counter trap below.

### build_print_cover.py

Reads `print/SPECS.json` for the page count and emits one wrap per paper stock.
Never hardcode a spine.

### build_epub.py

Assembles a reflowable EPUB 3 by hand into a zip. No library, because the
libraries all want to own the document model and the document model is already
`content/*.md`.

## The gates

`check_book.py` — chapter and entry counts, the unit's fields present in equal
numbers, no chapter repeating a source back to back, no em dash in prose, and
the built site free of placeholders.

`check_print.py` — page geometry on every page, an even page count, fonts
embedded and none loose, no text outside the safe area, no colour anywhere in a
mono interior (sampled by rendering and checking channel spread), and a spine
matching the number of leaves.

`check_epub.py` — mimetype stored and first, container resolves, manifest
matches the archive exactly in both directions, spine ids resolve, metadata
present, every XHTML well formed, every internal link landing on a real anchor,
cover size and ratio, and an NCX for older hardware.

Run all three before shipping anything. They are fast and they have caught real
defects that visual inspection missed.

## Print typesetting traps

**The page counter cannot be reset mid-document.** WeasyPrint ignores
`counter-reset: page` on an element. Front matter in roman and a body restarting
at 1 therefore needs two documents merged: render the body first, read the page
numbers back off `page.anchors`, then render the front matter with those numbers
baked in as text, then concatenate with pypdf. This is why `build_print.py` is
shaped the way it is.

**`target-counter(attr(href), page)` resolves `attr()` against the element it
sits on.** Putting it on a child span of an anchor yields nothing, silently. It
must be on the `<a>` itself. This is how the index of sources gets real page
numbers, and it fails invisibly if moved.

**Blank leaves from forced breaks keep their running head and folio** unless you
add `@page :blank { @top-center{content:none} @bottom-center{content:none} }`.
A blank verso before a chapter opener carrying a page number looks like a
printing error.

**A named page applies to any page whose first box carries it.** Put
`page: opener` on the chapter's title block only, not on the whole chapter, or
every page of the chapter loses its running head.

**`::first-letter` with float does not make a drop cap.** Build it explicitly:
wrap the first letter in a span, float it, and set line-height under 1. Aim for
two lines rather than three; three needs a font size that overwhelms the page.

**Rules that separate entries need `break-after: avoid`,** or a separator
strands itself at the foot of a page with its entry overleaf.

**Hyphenation needs both** `hyphens: auto` and a `lang` attribute, plus pyphen
installed. Without the lang it silently does nothing and justified text in a
narrow measure goes gappy.

## EPUB traps

**mimetype must be the first entry and stored, not deflated.** Write it with an
explicit `ZipInfo` and `ZIP_STORED` before anything else.

**The package document does not list itself** in its own manifest. A validator
that checks "every archive entry is in the manifest" must exempt it.

**Do not embed fonts.** Kindle readers expect to choose the typeface, and the
accessibility settings depend on it. An ebook that overrides them reads as
broken, not as designed.

**Page numbers do not exist.** An index of page numbers is meaningless. Convert
it to entry numbers, each one a link into the chapter file that holds it.

**Ship both navigations.** EPUB 3 `nav.xhtml` for current devices and a legacy
`toc.ncx` for older Kindle hardware. Costs nothing, avoids a dead contents menu
on a five-year-old device.

## Index traps

**Test scripture before the general word.** "Proverbs 15:1" contains the
substring "proverb". If the anonymous-sources test runs first, the book of
Proverbs is filed under proverbs, as a separate heading per verse. Check the
Bible book names first.

**Books whose names begin with a number** ("1 Timothy 6:10") break any rule that
looks at the first word. Match on the whole string with `startswith`.

**Sort keys need surnames.** "Marcus Aurelius" is not "Aurelius, Marcus" by any
generic rule, and mononyms ("Seneca", "Aesop") must not be inverted at all. Keep
explicit sets for both, and add to them as sources accumulate.
