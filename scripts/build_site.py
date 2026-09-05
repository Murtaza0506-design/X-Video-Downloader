#!/usr/bin/env python3
"""Build book.html from content/*.md.

Parses the manuscript into structured data, derives the source index, and
injects both into scripts/book_template.html. Run after editing any chapter:

    python3 scripts/build_site.py
"""
import os
import re
import csv
import glob
import json
import html
import collections

ANON = ("proverb", "adage", "maxim", "saying", "rhyme", "traditional",
        "memento mori", "inscription", "hanlon's razor", "delphi", "zen")
BIBLE = ("Proverbs", "Ecclesiastes", "Psalm", "Matthew", "Ephesians", "James",
         "Exodus", "Genesis", "1 Timothy")
SURNAME = {
    "Marcus Aurelius": "Aurelius, Marcus", "Lord Byron": "Byron, Lord",
    "Alfred, Lord Tennyson": "Tennyson, Alfred, Lord", "the Buddha": "Buddha, the",
    "François de La Rochefoucauld": "La Rochefoucauld, François de",
    "Michel de Montaigne": "Montaigne, Michel de",
    "Miguel de Cervantes": "Cervantes, Miguel de",
    "Antoine de Saint-Exupéry": "Saint-Exupéry, Antoine de",
    "Baltasar Gracián": "Gracián, Baltasar", "Søren Kierkegaard": "Kierkegaard, Søren",
}
MONONYM = {
    "Lao Tzu", "Sun Tzu", "Publilius Syrus", "Dionysius the Elder", "Charles I",
    "Leonardo da Vinci", "Ausonius", "Boethius", "Cicero", "Confucius", "Epictetus",
    "Epicurus", "Euripides", "Heraclitus", "Horace", "Lucretius", "Persius",
    "Pericles", "Plato", "Plautus", "Seneca", "Socrates", "Aesop", "Aristotle",
    "Voltaire", "Goethe", "Molière",
}
PREFIXES = ("attributed to ", "after ", "popular paraphrase of ")
ROMAN = {"One": "I", "Two": "II", "Three": "III", "Four": "IV",
         "Five": "V", "Six": "VI", "Seven": "VII", "Eight": "VIII"}

# The two glosses under each quotation. Their labels are the unit's, so a
# different book renames them here and everything downstream follows.
GLOSS = (os.environ.get("BOOK_GLOSS1", "What it means"),
         os.environ.get("BOOK_GLOSS2", "How to use it"))
# Where the manuscript lives, and what the book is called. A second book sets
# these and the whole pipeline follows it.
CONTENT = os.environ.get("BOOK_CONTENT", "content")
BOOK_TITLE = os.environ.get("BOOK_TITLE", "Lines Worth Keeping")
BOOK_SUBTITLE = os.environ.get(
    "BOOK_SUBTITLE",
    "A commonplace book of 315 quotations, each with what it means "
    "and where to put it.")
BOOK_AUTHOR = os.environ.get("BOOK_AUTHOR", "Murtaza Raza")
NOTE_TITLE = os.environ.get("BOOK_NOTE_TITLE", "A Note on Attribution")
INDEX_TITLE = os.environ.get("BOOK_INDEX_TITLE", "Index of Sources")
INTRO_TITLE = os.environ.get("BOOK_INTRO_TITLE", "How to Use This Book")
# Each book writes to its own files, so building one never clobbers another.
OUT_FRAGMENT = os.environ.get("BOOK_OUT_FRAGMENT", "book.html")
OUT_SITE = os.environ.get("BOOK_OUT_SITE", "site/index.html")
OUT_CSV = os.environ.get("BOOK_OUT_CSV", "book-entries.csv")
ENTRIES = 315
CHAPTERS = 21


def inline(text):
    """Markdown emphasis and links to HTML, on escaped text."""
    out = html.escape(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", out)
    out = re.sub(r"\[(.+?)\]\((https?://[^)]+)\)",
                 r'<a href="\2" rel="noopener">\1</a>', out)
    return out


def blocks_to_html(text):
    """A small markdown subset: paragraphs and dash lists."""
    parts, buf = [], []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- "):
            if buf and buf[-1][0] != "li":
                pass
            buf.append(("li", line[2:]))
        else:
            buf.append(("p", line))
    for kind, body in buf:
        if kind == "li":
            if not parts or not parts[-1].startswith("<ul>"):
                parts.append("<ul>")
            parts[-1] += f"<li>{inline(body)}</li>"
        else:
            if parts and parts[-1].startswith("<ul>") and not parts[-1].endswith("</ul>"):
                parts[-1] += "</ul>"
            parts.append(f"<p>{inline(body)}</p>")
    if parts and parts[-1].startswith("<ul>") and not parts[-1].endswith("</ul>"):
        parts[-1] += "</ul>"
    return "".join(parts)


def front_matter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    meta = dict(re.findall(r"^(\w+): (.+)$", m.group(1), re.M))
    return meta, text[m.end():]


def load_surnames():
    """A book may carry its own inversions in content/surnames.txt, one per
    line as "Full Name = Sorted, Name". Nobody can guess that Lord Kelvin
    files under K by rule."""
    path = os.path.join(CONTENT, "surnames.txt")
    if not os.path.exists(path):
        return
    for line in open(path):
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            SURNAME[k.strip()] = v.strip()


def person_key(name):
    if name in SURNAME:
        return SURNAME[name]
    if name in MONONYM or " " not in name:
        return name
    parts = name.replace(",", "").split()
    return f"{parts[-1]}, {' '.join(parts[:-1])}"


def parse_chapters():
    load_surnames()
    chapters, n = [], 0
    files = sorted(f for f in glob.glob(os.path.join(CONTENT, "*.md"))
                   if re.match(r"(0[1-9]|1[0-9]|2[01])-", os.path.basename(f)))
    for path in files:
        meta, body = front_matter(open(path).read())
        sections = [s.strip() for s in body.split("\n---\n")]
        head = sections[0]
        title = re.search(r"^# Chapter \d+ — (.+)$", head, re.M).group(1)
        opening = head.split("\n", 1)[1].strip()
        part_num, part_name = [s.strip() for s in meta["part"].split("—")]
        entries = []
        for sec in sections[1:]:
            if not sec.startswith(">"):
                continue
            n += 1
            qline = re.search(r"^> (.+)$", sec, re.M).group(1)
            quote, attribution = qline.rsplit("—", 1)
            quote = quote.strip()
            display = quote.strip('"') if quote.startswith('"') else quote.strip("*")
            means = re.search(r"\*\*%s\.\*\* (.+?)(?:\n|$)" % re.escape(GLOSS[0]),
                              sec, re.S).group(1).strip()
            use = re.search(r"\*\*%s\.\*\* (.+?)(?:\n|$)" % re.escape(GLOSS[1]),
                            sec, re.S).group(1).strip()
            entries.append({
                "n": n,
                "quote": display,
                "bare": quote.startswith("**"),
                "attribution": attribution.strip(),
                "means": means,
                "use": use,
                "ch": int(meta["chapter"]),
            })
        chapters.append({
            "n": int(meta["chapter"]),
            "title": title,
            "part": part_num,
            "partRoman": ROMAN[part_num],
            "partName": part_name,
            "opening": blocks_to_html(opening),
            "entries": entries,
        })
    return chapters


# A commonplace book indexes people, so "Marcus Aurelius" is filed under A and
# scripture is gathered under one heading. A book whose attribution line is a
# label rather than a name ("The late apology", "The straw man") must not be
# inverted on its last word: it files itself under the phrase as written.
INDEX_PEOPLE = os.environ.get("BOOK_INDEX_PEOPLE", "1") != "0"
INDEX_STRIP = os.environ.get("BOOK_INDEX_STRIP", "")


def build_index(chapters):
    groups = collections.defaultdict(list)
    for ch in chapters:
        for e in ch["entries"]:
            if not INDEX_PEOPLE:
                head = e["attribution"]
                # File under the first word that carries meaning, as a title
                # index does, so half the book does not end up under T.
                sort = re.sub(r"^(the|a|an) ", "", head.lower())
                groups[(sort, head)].append(
                    {"n": e["n"], "quote": e["quote"], "ch": e["ch"], "q": ""})
                continue
            qualifier, base = "", e["attribution"]
            # An attribution that carries a date ("Ken Olsen, 1977") indexes
            # under the person, not the year. The book says what to cut.
            if INDEX_STRIP:
                base = re.sub(INDEX_STRIP, "", base).strip()
            for pre in PREFIXES:
                if base.lower().startswith(pre):
                    qualifier, base = pre.strip(), base[len(pre):]
            if base.startswith("English proverb,"):
                base = "English proverb"
            low = base.lower()
            # the book of Proverbs before the general word: check scripture first
            if any(base.startswith(b) for b in BIBLE):
                head, sort = "The Bible", "~0the bible"
            elif any(a in low for a in ANON):
                head, sort = base, "~1" + low
            else:
                head = person_key(base)
                sort = head.lower()
            groups[(sort, head)].append(
                {"n": e["n"], "quote": e["quote"], "ch": e["ch"], "q": qualifier})
    out = []
    for sort, head in sorted(groups):
        out.append({
            "name": head,
            "letter": "¶" if sort.startswith("~") else sort[0].upper(),
            "items": sorted(groups[(sort, head)], key=lambda i: i["n"]),
        })
    return out


def main():
    chapters = parse_chapters()
    intro_meta, intro_body = front_matter(
        open(os.path.join(CONTENT, "00-introduction.md")).read())
    note_meta, note_body = front_matter(
        open(os.path.join(CONTENT, "90-note-on-attribution.md")).read())
    def strip_heading(body):
        lines = body.strip().split("\n")
        if lines and lines[0].lstrip().startswith("#"):
            lines = lines[1:]
        return "\n".join(lines)

    data = {
        "title": BOOK_TITLE,
        "gloss": list(GLOSS),
        "author": BOOK_AUTHOR,
        "subtitle": BOOK_SUBTITLE,
        "chapters": chapters,
        "index": build_index(chapters),
        "blurb": [ln.strip() for ln in open(os.path.join(CONTENT, "blurb.txt")).read().strip().split("\n") if ln.strip()],
        "intro": blocks_to_html(strip_heading(intro_body)),
        "note": blocks_to_html(strip_heading(note_body)),
        "introTitle": INTRO_TITLE,
        "noteTitle": NOTE_TITLE,
        "indexTitle": INDEX_TITLE,
    }
    total = sum(len(c["entries"]) for c in chapters)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    tpl = open("scripts/book_template.html").read()
    page = tpl.replace("__BOOK_DATA__", payload)
    # book.html is the Artifact fragment: the host supplies <html>, <head> and
    # the charset and viewport meta. A file served directly needs its own, or
    # phones fall back to a 980px layout viewport and the sizing breaks.
    open(OUT_FRAGMENT, "w").write(page)
    split = page.index("</style>") + len("</style>")
    head, body = page[:split], page[split:]
    os.makedirs(os.path.dirname(OUT_SITE) or ".", exist_ok=True)
    with open(OUT_SITE, "w") as fh:
        fh.write(
            "<!doctype html>\n<html lang=\"en-GB\">\n<head>\n"
            "<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, "
            "viewport-fit=cover\">\n"
            "<meta name=\"description\" content=\"" + data["subtitle"] + "\">\n"
            "<meta name=\"color-scheme\" content=\"light\">\n"
            + head + "\n</head>\n<body>" + body + "\n</body>\n</html>\n")

    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "chapter", "chapter_title", "part", "quote",
                    "attribution", "what_it_means", "how_to_use_it"])
        for ch in chapters:
            for e in ch["entries"]:
                w.writerow([e["n"], ch["n"], ch["title"], ch["part"], e["quote"],
                            e["attribution"], e["means"], e["use"]])

    print(f"{len(chapters)} chapters, {total} entries, "
          f"{len(data['index'])} sources -> book.html + site/index.html "
          f"({len(payload)//1024} KB data)")


if __name__ == "__main__":
    main()
