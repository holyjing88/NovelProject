# -*- coding: utf-8 -*-
import glob, re, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, extract_body_and_footer, hz

def dup(t):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)

short, high = [], []
for p in sorted(glob.glob(os.path.join("..", "prose", "ch*.md"))):
    n = int(re.search(r"ch(\d+)", p).group(1))
    if n > 49:
        continue
    b, _ = extract_body_and_footer(open(p, encoding="utf-8").read())
    h, d = hz(b), dup(b)
    if h < TARGET_LO:
        short.append((n, h))
    if d >= 0.02:
        high.append((n, round(d, 3), h))

print("SHORT", short)
print("HIGH_DUP", high)
d = json.load(open("_churn_data.json", encoding="utf-8"))
risks = [c["n"] for c in d["chapters"] if c["daily_risk"] > 1.05 or c["batch_risk"] > 1.05 or c["dup"] >= 0.02]
print("RISK", risks)
print("ALL_OK", len(short) == 0 and len(high) <= 3)
