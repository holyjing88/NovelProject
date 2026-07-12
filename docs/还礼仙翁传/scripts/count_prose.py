#!/usr/bin/env python3
"""上架连载稿汉字计数 · 硬性区间 2000～3000"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose_utils import body_chars

PROSE = Path(__file__).resolve().parent.parent / "prose"
LO, HI = 2000, 3000
# 正文章节 ch001～061（排除草稿/重复稿）
CANONICAL_RE = re.compile(r"ch0(0[1-9]|[12][0-9]|30|3[1-9]|[4-5][0-9]|60|61)")

total = 0
rows = []
for p in sorted(PROSE.glob("ch*.md")):
    if not CANONICAL_RE.match(p.name):
        continue
    c = body_chars(p.read_text(encoding="utf-8"))
    total += c
    rows.append((p.name, c))

print(f"ch001-061: total={total}, avg={total/len(rows):.0f}, count={len(rows)}")
print(f"in_range_{LO}-{HI}: {sum(1 for _,c in rows if LO <= c <= HI)}/{len(rows)}")
print(f"below{LO}: {sum(1 for _,c in rows if c < LO)}")
for n, c in sorted(rows, key=lambda x: x[1]):
    if c < LO:
        print(f"  {n}: {c}")
print(f"over{HI}: {sum(1 for _,c in rows if c > HI)}")
for n, c in sorted(rows, key=lambda x: -x[1]):
    if c > HI:
        print(f"  {n}: {c}")
print("top5:")
for n, c in sorted(rows, key=lambda x: -x[1])[:5]:
    print(f"  {n}: {c}")
