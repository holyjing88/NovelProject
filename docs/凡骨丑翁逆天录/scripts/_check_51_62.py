# -*- coding: utf-8 -*-
import re, glob, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import hz, extract_body_and_footer

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

ok = 0
for n in range(51, 63):
    raw = open(glob.glob(os.path.join("..", "prose", f"ch{n:03d}-*.md"))[0], encoding="utf-8").read()
    b, footer = extract_body_and_footer(raw)
    h, d = hz(b), dup(b)
    bad = bool(re.search(r"稳[。！？]\s*等[。！？]", b))
    flag = 2000 <= h <= 2500 and d < 0.02 and "仙凡笔锋 v2" in footer and not bad
    if flag:
        ok += 1
    st = "OK" if flag else "FIX"
    print(f"ch{n:03d}: {h} dup={d:.3%} bad={bad} [{st}]")
print(f"PASS {ok}/12")
