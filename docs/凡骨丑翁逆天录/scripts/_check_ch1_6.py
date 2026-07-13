# -*- coding: utf-8 -*-
import glob, re
from prose_utils import extract_body_and_footer, hz, TARGET_LO, TARGET_HI

for n in range(1, 7):
    p = [x for x in glob.glob("../prose/ch*.md") if f"ch{n:03d}" in x][0]
    raw = open(p, encoding="utf-8").read()
    b, _ = extract_body_and_footer(raw)
    h = hz(b)
    sents = [x.strip() for x in re.split(r"(?<=[。！？])", b) if len(x.strip()) >= 8]
    seen, d = set(), 0
    for x in sents:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    dr = d / len(sents) if sents else 0
    wall = sum(1 for p in re.split(r"\n\s*\n", b) if len(re.sub(r"\s+", "", p)) > 180)
    tag = "OK" if TARGET_LO <= h <= TARGET_HI and dr < 0.02 and wall == 0 else "FAIL"
    print(f"ch{n:03d} {h} dup={dr:.3f} wall={wall} {tag}")
