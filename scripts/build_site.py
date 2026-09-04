#!/usr/bin/env python3
"""Build book.html from content/*.md.

Parses the manuscript into structured data, derives the source index, and
injects both into scripts/book_template.html. Run after editing any chapter:

    python3 scripts/build_site.py
"""
import re
import csv
import glob
import json
import html
import collections

ANON = ("proverb", "adage", "maxim", "saying", "rhyme", "traditional",
        "memento mori", "inscription", "hanlon's razor", "delphi", "zen")
BIBLE = ("Proverbs", "Ecclesiastes", "Psalm", "Matthew", "Ephesians", "James", "Exodus")
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
ROMAN = {"One": "I", "Two": "II", "Three": "III", "Four": "IV"}


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


def person_key(name):
    if name in SURNAME:
        return SURNAME[name]
    if name in MONONYM or " " not in name:
        return name
    parts = name.replace(",", "").split()
    return f"{parts[-1]}, {' '.join(parts[:-1])}"


def parse_chapters():
    chapters, n = [], 0
    files = sorted(f for f in glob.glob("content/*.md")
                   if re.match(r"content/(0[1-9]|1[0-6])-", f))
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
            means = re.search(r"\*\*What it means\.\*\* (.+?)(?:\n|$)", sec, re.S).group(1).strip()
            use = re.search(r"\*\*How to use it\.\*\* (.+?)(?:\n|$)", sec, re.S).group(1).strip()
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


def build_index(chapters):
    groups = collections.defaultdict(list)
    for ch in chapters:
        for e in ch["entries"]:
            qualifier, base = "", e["attribution"]
            for pre in PREFIXES:
                if base.lower().startswith(pre):
                    qualifier, base = pre.strip(), base[len(pre):]
            if base.startswith("English proverb,"):
                base = "English proverb"
            low = base.lower()
            if any(a in low for a in ANON):
                head, sort = base, "~1" + low
            elif base.split()[0] in BIBLE:
                head, sort = "The Bible", "~0the bible"
            else:
                head = person_key(base)
                sort = head.lower()
            groups[(sort, head)].append(
                {"n": e["n"], "quote": e["quote"], "ch": e["ch"], "q": qualifier})
    out = []
    for sort, head in sorted(groups):
        out.append({
            "name": head,
            "letter": "¶" if sort.startswith("~") else head[0].upper(),
            "items": sorted(groups[(sort, head)], key=lambda i: i["n"]),
        })
    return out


def main():
    chapters = parse_chapters()
    intro_meta, intro_body = front_matter(open("content/00-introduction.md").read())
    note_meta, note_body = front_matter(open("content/90-note-on-attribution.md").read())
    def strip_heading(body):
        lines = body.strip().split("\n")
        if lines and lines[0].lstrip().startswith("#"):
            lines = lines[1:]
        return "\n".join(lines)

    data = {
        "title": "Lines Worth Keeping",
        "subtitle": "A commonplace book of 240 quotations, "
                    "each with what it means and where to put it.",
        "chapters": chapters,
        "index": build_index(chapters),
        "blurb": [ln.strip() for ln in open("content/blurb.txt").read().strip().split("\n") if ln.strip()],
        "intro": blocks_to_html(strip_heading(intro_body)),
        "note": blocks_to_html(strip_heading(note_body)),
    }
    total = sum(len(c["entries"]) for c in chapters)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    tpl = open("scripts/book_template.html").read()
    open("book.html", "w").write(tpl.replace("__BOOK_DATA__", payload))

    with open("book-entries.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "chapter", "chapter_title", "part", "quote",
                    "attribution", "what_it_means", "how_to_use_it"])
        for ch in chapters:
            for e in ch["entries"]:
                w.writerow([e["n"], ch["n"], ch["title"], ch["part"], e["quote"],
                            e["attribution"], e["means"], e["use"]])

    print(f"{len(chapters)} chapters, {total} entries, "
          f"{len(data['index'])} sources -> book.html ({len(payload)//1024} KB data)")


if __name__ == "__main__":
    main()
