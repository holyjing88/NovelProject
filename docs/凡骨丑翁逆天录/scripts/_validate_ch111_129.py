# -*- coding: utf-8 -*-
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz, TARGET_LO, TARGET_HI

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

def dup_rate(text):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", text) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)

short, over, high = [], [], []
files = []
for n in range(111, 130):
    p = glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md"))[0]
    files.append(os.path.basename(p))
    body, _ = extract_body_and_footer(open(p, encoding="utf-8").read())
    h, d = hz(body), dup_rate(body)
    ok = TARGET_LO <= h <= TARGET_HI and d < 0.02
    if h < TARGET_LO:
        short.append((n, h))
    if h > TARGET_HI:
        over.append((n, h))
    if d >= 0.02:
        high.append((n, round(d, 3)))
    print(f"ch{n:03d}: {h} dup={d:.3f} {'OK' if ok else 'FAIL'}")

print("SHORT", short)
print("OVER", over)
print("DUP", high)
print("FILES", len(files))
