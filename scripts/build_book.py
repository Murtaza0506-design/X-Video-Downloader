#!/usr/bin/env python3
"""Rebuild the generated parts of the book.

Reads content/*.md and writes:
  content/91-index-of-sources.md   index of quotations grouped by source
  manuscript.md                    every chapter assembled in reading order

Run after editing any chapter: python3 scripts/build_book.py
"""
import re
import glob
import collections

ANON = ("proverb", "adage", "maxim", "saying", "rhyme", "traditional",
        "memento mori", "inscription", "hanlon's razor", "delphi", "zen")
BIBLE = ("Proverbs", "Ecclesiastes", "Psalm", "Matthew", "Ephesians", "James", "Exodus")

# Sources whose surname cannot be derived by taking the last word.
SURNAME = {
    "Marcus Aurelius": "Aurelius, Marcus", "Lord Byron": "Byron, Lord",
    "Alfred, Lord Tennyson": "Tennyson, Alfred, Lord", "the Buddha": "Buddha, the",
    "François de La Rochefoucauld": "La Rochefoucauld, François de",
    "Michel de Montaigne": "Montaigne, Michel de",
    "Miguel de Cervantes": "Cervantes, Miguel de",
    "Antoine de Saint-Exupéry": "Saint-Exupéry, Antoine de",
    "Baltasar Gracián": "Gracián, Baltasar",
    "Søren Kierkegaard": "Kierkegaard, Søren",
}
# Single-name classical and other sources that are already in sort order.
MONONYM = {
    "Lao Tzu", "Sun Tzu", "Publilius Syrus", "Dionysius the Elder", "Charles I",
    "Leonardo da Vinci", "Ausonius", "Boethius", "Cicero", "Confucius", "Epictetus",
    "Epicurus", "Euripides", "Heraclitus", "Horace", "Lucretius", "Persius",
    "Pericles", "Plato", "Plautus", "Seneca", "Socrates", "Aesop", "Aristotle",
    "Voltaire", "Goethe", "Molière",
}
PREFIXES = ("attributed to ", "after ", "popular paraphrase of ")


def person_key(name):
    if name in SURNAME:
        return SURNAME[name]
    if name in MONONYM or " " not in name:
        return name
    parts = name.replace(",", "").split()
    return f"{parts[-1]}, {' '.join(parts[:-1])}"


def chapter_files():
    return sorted(f for f in glob.glob("content/*.md")
                  if re.match(r"content/(0[1-9]|1[0-6])-", f))


def build_index():
    titles, index = {}, collections.defaultdict(list)
    for path in chapter_files():
        text = open(path).read()
        m = re.search(r"^# Chapter (\d+) — (.+)$", text, re.M)
        ch, titles[int(m.group(1))] = int(m.group(1)), m.group(2)
        for line in re.findall(r"^> (.+)$", text, re.M):
            quote, attr = line.rsplit("—", 1)
            quote = quote.strip().strip("*").strip('"').rstrip('."')
            attr = attr.strip()
            qualifier, base = "", attr
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
            short = quote if len(quote) <= 58 else quote[:55].rsplit(" ", 1)[0] + "…"
            index[(sort, head)].append((ch, short, qualifier))

    out = ["---", "part: Back matter", "chapter: 91",
           "title: Index of Quotations by Source", "---", "",
           "# Index of Quotations by Source", "",
           "Chapter numbers in brackets. Where a line is disputed or paraphrased, the",
           "entry is marked *attributed* or *after*, matching the label used in the text.",
           ""]
    letter = None
    for key in sorted(index):
        sort, head = key
        if not sort.startswith("~"):
            if head[0].upper() != letter:
                letter = head[0].upper()
                out.append(f"### {letter}\n")
        elif letter != "~":
            letter = "~"
            out.append("### Proverbs, scripture and anonymous sources\n")
        out.append(f"**{head}**  ")
        for ch, short, qualifier in sorted(index[key]):
            mark = f" *({qualifier})*" if qualifier else ""
            out.append(f"&nbsp;&nbsp;“{short}”{mark} [{ch}]  ")
        out.append("")
    out += ["---", "", "## Chapters", ""]
    out += [f"{ch}. {titles[ch]}" for ch in sorted(titles)]
    open("content/91-index-of-sources.md", "w").write("\n".join(out) + "\n")
    return sum(len(v) for v in index.values()), len(index)


def build_manuscript():
    order = (["content/00-introduction.md"] + chapter_files()
             + ["content/90-note-on-attribution.md", "content/91-index-of-sources.md"])
    parts, seen_part, words = ["# Lines Worth Keeping\n"], None, 0
    for path in order:
        body = open(path).read()
        meta = re.match(r"---\n(.*?)\n---\n", body, re.S)
        part = re.search(r"^part: (.+)$", meta.group(1), re.M).group(1)
        body = body[meta.end():].strip()
        if part != seen_part and part not in ("Front matter", "Back matter"):
            parts.append(f"\n# Part {part}\n")
            seen_part = part
        parts.append(body + "\n")
        words += len(body.split())
    open("manuscript.md", "w").write("\n".join(parts))
    return words


if __name__ == "__main__":
    entries, sources = build_index()
    total = build_manuscript()
    print(f"{entries} entries from {sources} distinct sources")
    print(f"manuscript.md: {total:,} words")
