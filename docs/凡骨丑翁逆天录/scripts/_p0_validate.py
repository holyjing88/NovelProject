# -*- coding: utf-8 -*-
import glob, re, sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, body_chars, extract_body_and_footer

def dup_ratio(t):
    sents = [s.strip() for s in re.split(r"(?<=[。！？])", t) if len(s.strip()) >= 8]
    if not sents:
        return 0.0
    seen, dup = set(), 0
    for s in sents:
        k = re.sub(r"\s+", "", s)
        if k in seen:
            dup += 1
        seen.add(k)
    return dup / len(sents)

for n in [13, 14, 15, 16, 44]:
    p = [x for x in glob.glob(os.path.join("..", "prose", "ch*.md")) if re.search(rf"ch{n:03d}", x)][0]
    t = open(p, encoding="utf-8").read()
    body, _ = extract_body_and_footer(t)
    print(
        f"ch{n:03d} hz={body_chars(t)} dup={dup_ratio(body):.3f} "
        f"meta={('读者' in body)} pad={body.count('坛沿一线温')}"
    )

short = []
for p in sorted(glob.glob(os.path.join("..", "prose", "ch*.md"))):
    nn = int(re.search(r"ch(\d+)", p).group(1))
    if nn > 49:
        continue
    c = body_chars(open(p, encoding="utf-8").read())
    if c < TARGET_LO:
        short.append((nn, c))
print("short:", short)

d = json.load(open("_churn_data.json", encoding="utf-8"))
for c in d["chapters"]:
    if c["n"] in (13, 14, 15, 16, 44):
        print(f"risk ch{c['n']:03d} daily={c['daily_risk']} batch={c['batch_risk']} dup={c['dup']}")
for s in d["segments"]:
    if s["lo"] <= 16 <= s["hi"] or s["lo"] <= 44 <= s["hi"]:
        print(f"seg {s['name']} daily={s['daily']} batch={s['batch']}")
