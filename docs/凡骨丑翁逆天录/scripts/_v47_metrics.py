# -*- coding: utf-8 -*-
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz

targets = [1,3,10,18,24,25,28,30,34,36,37,38,39,40,42,43,46,47,48,49,63,130]
prose = os.path.join(os.path.dirname(__file__), "..", "prose")

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

for n in targets:
    p = glob.glob(os.path.join(prose, f"ch{n:03d}*.md"))
    if not p:
        print(f"ch{n:03d}: MISSING")
        continue
    raw = open(p[0], encoding="utf-8").read()
    b, _ = extract_body_and_footer(raw)
    h = hz(b)
    en = b.count("嗯")
    d = dup(b)
    flags = []
    if h < 1780:
        flags.append("SHORT")
    if h > 1950:
        flags.append("OVER")
    if d >= 0.02:
        flags.append("DUP")
    if en > 1:
        flags.append(f"EN={en}")
    status = " ".join(flags) if flags else "OK"
    print(f"ch{n:03d}: {h} dup={d:.3f} en={en} {status}")
