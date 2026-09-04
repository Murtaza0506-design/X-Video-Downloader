import re, glob, sys, statistics, collections

HEDGES = ["usually","often","generally","typically","roughly","quite","rather",
          "very","somewhat","genuinely","actually","simply","really","fairly",
          "almost always","tends to","tend to","a bit","sort of","kind of",
          "arguably","perhaps","possibly","frequently","largely","mostly",
          "essentially","basically","particularly","especially","certainly",
          "considerably","remarkably","entirely","completely","absolutely"]

def prose(path):
    out = []
    for line in open(path):
        s = line.strip()
        if not s or s.startswith(("#","---","> ","|","part:","chapter:","title:")):
            continue
        s = re.sub(r"\*\*(What it means|How to use it)\.\*\*\s*", "", s)
        s = s.replace("**","")
        out.append(s)
    return " ".join(out)

def sentences(text):
    text = re.sub(r"\b([A-Z])\.", r"\1", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 1]

rows = []
allsent, allwords = [], []
for f in sorted(glob.glob(sys.argv[1] if len(sys.argv)>1 else "content/[012]*.md")):
    t = prose(f)
    ss = sentences(t)
    lens = [len(s.split()) for s in ss]
    words = re.findall(r"[a-z']+", t.lower())
    allsent += lens; allwords += words
    low = t.lower()
    low = low.replace("rather than", "").replace("other than", "")
    hedge = sum(len(re.findall(r"\b"+h+r"\b", low)) for h in HEDGES)
    # Words ending in -ly that are not adverbs. Without this the count is
    # inflated by whatever the book happens to be about: a book about replies
    # scores badly for the word "reply".
    NOT_ADV = {"only", "reply", "replies", "family", "families", "supply",
               "supplies", "apply", "applies", "imply", "implies", "rely",
               "relies", "multiply", "assembly", "ally", "allies", "ugly",
               "early", "likely", "unlikely", "lonely", "holy", "italy",
               "july", "jelly", "belly", "silly", "daily", "weekly",
               "monthly", "yearly", "friendly", "costly", "deadly", "lively",
               "orderly", "elderly", "wholly", "solely", "namely", "supply"}
    adv = len([w for w in words
               if w.endswith("ly") and len(w) > 5 and w not in NOT_ADV])
    short = sum(1 for l in lens if l <= 8)
    long_ = sum(1 for l in lens if l >= 30)
    rows.append((f.split("/")[-1][:2], len(ss), statistics.mean(lens),
                 statistics.pstdev(lens), 100*short/len(ss), 100*long_/len(ss),
                 1000*hedge/len(words), 1000*adv/len(words)))

print(f"{'ch':>3} {'sents':>5} {'mean':>6} {'stdev':>6} {'%<=8w':>6} {'%>=30w':>7} {'hedge/1k':>9} {'-ly/1k':>7}")
for r in rows:
    print(f"{r[0]:>3} {r[1]:>5} {r[2]:>6.1f} {r[3]:>6.1f} {r[4]:>6.1f} {r[5]:>7.1f} {r[6]:>9.1f} {r[7]:>7.1f}")
print(f"\nBOOK: {len(allsent)} sentences, mean {statistics.mean(allsent):.1f}, "
      f"stdev {statistics.pstdev(allsent):.1f}, "
      f"{100*sum(1 for l in allsent if l<=8)/len(allsent):.1f}% short, "
      f"{100*sum(1 for l in allsent if l>=30)/len(allsent):.1f}% long")

means = [r[2] for r in rows]
tot_h = sum(r[6]*r[1] for r in rows)/sum(r[1] for r in rows)
tot_a = sum(r[7]*r[1] for r in rows)/sum(r[1] for r in rows)
print(f"      hedges/1k {tot_h:.1f} | -ly/1k {tot_a:.1f} | "
      f"chapter mean spread {max(means)-min(means):.1f}")

c = collections.Counter(allwords)
print("\nmost-used hedges:", ", ".join(f"{h}({c[h]})" for h in
      sorted([h for h in HEDGES if " " not in h], key=lambda h:-c[h])[:12]))
