#!/usr/bin/env python3
"""Flag hedges and weak adverbs in a chapter, with context, for a manual cut."""
import re, sys, glob

HEDGES = ["usually","often","generally","typically","roughly","quite","rather",
          "very","somewhat","genuinely","actually","simply","really","fairly",
          "arguably","perhaps","possibly","frequently","largely","mostly",
          "essentially","basically","particularly","especially","certainly",
          "considerably","remarkably","entirely","completely","absolutely"]
KEEP_ADV = {"only","early","family","likely","ugly","reply","apply","supply",
            "properly","exactly","daily","weekly","monthly","yearly"}

for path in sorted(sum((glob.glob(a) for a in sys.argv[1:]), [])):
    hits = []
    for i, line in enumerate(open(path), 1):
        s = line.strip()
        if not s or s.startswith(("#","---","> ","part:","chapter:","title:")):
            continue
        low = s.lower().replace("rather than","").replace("other than","")
        for h in HEDGES:
            for m in re.finditer(r"\b"+h+r"\b", low):
                hits.append((i, "HEDGE", h, s[max(0,m.start()-38):m.start()+len(h)+30]))
        for m in re.finditer(r"\b(\w{5,}ly)\b", s):
            w = m.group(1).lower()
            if w not in KEEP_ADV and w not in HEDGES:
                hits.append((i, "ADV", w, s[max(0,m.start()-38):m.start()+len(w)+30]))
    print(f"\n=== {path}  ({len(hits)} flags) ===")
    for i, kind, w, ctx in hits:
        print(f"{i:>4} {kind:<5} {w:<14} …{ctx}…")
