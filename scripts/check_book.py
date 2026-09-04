#!/usr/bin/env python3
"""Fail the build if the manuscript is not intact.

Runs in CI before publishing, so a bad edit cannot reach the live book.
"""
import glob
import os
import re
import sys

GLOSS = (os.environ.get("BOOK_GLOSS1", "What it means"),
         os.environ.get("BOOK_GLOSS2", "How to use it"))
WANT_CH = int(os.environ.get("BOOK_CHAPTERS", "21"))
WANT_PER = int(os.environ.get("BOOK_PER_CHAPTER", "15"))
WANT_TOTAL = WANT_CH * WANT_PER

problems = []
CONTENT = os.environ.get("BOOK_CONTENT", "content")
chapters = sorted(f for f in glob.glob(os.path.join(CONTENT, "*.md"))
                  if re.match(r"(0[1-9]|1[0-9]|2[01])-", os.path.basename(f)))

if len(chapters) != WANT_CH:
    problems.append(f"expected {WANT_CH} chapters, found {len(chapters)}")

total = 0
for path in chapters:
    text = open(path).read()
    quotes = re.findall(r"^> (.+)$", text, re.M)
    means = text.count("**%s.**" % GLOSS[0])
    uses = text.count("**%s.**" % GLOSS[1])
    total += len(quotes)
    if not (len(quotes) == means == uses == WANT_PER):
        problems.append(f"{path}: {len(quotes)} quotes, {means}/{uses} glosses "
                        f"(want {WANT_PER} each)")
    sources = [q.rsplit("—", 1)[1].strip() for q in quotes if "—" in q]
    for i in range(1, len(sources)):
        if sources[i] == sources[i - 1]:
            problems.append(f"{path}: same source twice running ({sources[i]})")
    # house rule: no em dashes in the prose, only in attribution lines
    for n, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if s and not s.startswith(("#", "> ", "---", "part:", "chapter:", "title:")) and "—" in s:
            problems.append(f"{path}:{n}: em dash in prose")

if total != WANT_TOTAL:
    problems.append(f"expected {WANT_TOTAL} entries, found {total}")

OUT_SITE = os.environ.get("BOOK_OUT_SITE", "site/index.html")
OUT_FRAGMENT = os.environ.get("BOOK_OUT_FRAGMENT", "book.html")
for required in (OUT_SITE, OUT_FRAGMENT):
    if not os.path.exists(required):
        problems.append(f"{required} was not built")

if os.path.exists(OUT_SITE):
    page = open(OUT_SITE).read()
    if "__BOOK_DATA__" in page:
        problems.append(f"{OUT_SITE} still contains the data placeholder")
    for needle in ("<!doctype html>", 'name="viewport"', "<title>"):
        if needle not in page:
            problems.append(f"{OUT_SITE} is missing {needle}")

if problems:
    print("Manuscript check failed:")
    for p in problems:
        print(" -", p)
    sys.exit(1)
print(f"Manuscript intact: {len(chapters)} chapters, {total} entries, site built.")
