# -*- coding: utf-8 -*-
"""Validate ch091-110 prose."""
import re, glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import hz, extract_body_and_footer, TARGET_LO, TARGET_HI

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")


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


def main():
    files = sorted(
        glob.glob(os.path.join(PROSE, "ch09*.md"))
        + glob.glob(os.path.join(PROSE, "ch10*.md"))
    )
    print("FILE\tCHARS\tDUP\tOK")
    bad = []
    for p in files:
        raw = open(p, encoding="utf-8").read()
        b, footer = extract_body_and_footer(raw)
        h, d = hz(b), dup(b)
        ok = TARGET_LO <= h <= TARGET_HI and d < 0.02 and "**状态**" in raw
        print(f"{os.path.basename(p)}\t{h}\t{round(d,4)}\t{ok}")
        if not ok:
            bad.append((os.path.basename(p), h, round(d, 4)))
    print("TOTAL", len(files))
    if bad:
        print("NEEDS_FIX", bad)
        sys.exit(1)
    print("ALL_OK")

if __name__ == "__main__":
    main()
