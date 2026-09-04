#!/usr/bin/env python3
"""Fail the build if the manuscript is not intact.

Runs in CI before publishing, so a bad edit cannot reach the live book.
"""
import glob
import os
import re
import sys

problems = []
chapters = sorted(f for f in glob.glob("content/*.md")
                  if re.match(r"content/(0[1-9]|1[0-9]|2[01])-", f))

if len(chapters) != 21:
    problems.append(f"expected 21 chapters, found {len(chapters)}")

total = 0
for path in chapters:
    text = open(path).read()
    quotes = re.findall(r"^> (.+)$", text, re.M)
    means = text.count("**What it means.**")
    uses = text.count("**How to use it.**")
    total += len(quotes)
    if not (len(quotes) == means == uses == 15):
        problems.append(f"{path}: {len(quotes)} quotes, {means} means, {uses} uses (want 15 each)")
    sources = [q.rsplit("—", 1)[1].strip() for q in quotes if "—" in q]
    for i in range(1, len(sources)):
        if sources[i] == sources[i - 1]:
            problems.append(f"{path}: same source twice running ({sources[i]})")
    # house rule: no em dashes in the prose, only in attribution lines
    for n, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if s and not s.startswith(("#", "> ", "---", "part:", "chapter:", "title:")) and "—" in s:
            problems.append(f"{path}:{n}: em dash in prose")

if total != 315:
    problems.append(f"expected 315 entries, found {total}")

for required in ("site/index.html", "book.html"):
    if not os.path.exists(required):
        problems.append(f"{required} was not built")

if os.path.exists("site/index.html"):
    page = open("site/index.html").read()
    if "__BOOK_DATA__" in page:
        problems.append("site/index.html still contains the data placeholder")
    for needle in ("<!doctype html>", 'name="viewport"', "<title>"):
        if needle not in page:
            problems.append(f"site/index.html is missing {needle}")

if problems:
    print("Manuscript check failed:")
    for p in problems:
        print(" -", p)
    sys.exit(1)
print(f"Manuscript intact: {len(chapters)} chapters, {total} entries, site built.")
