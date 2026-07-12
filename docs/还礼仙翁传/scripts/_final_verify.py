#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hand_polish_strip import polish_body
from prose_utils import hz, extract_body_and_footer

LO, HI = 2000, 2600
prose = Path(__file__).resolve().parent.parent / "prose"

rows = []
for p in sorted(prose.glob("ch0*.md")):
    if not re.match(r"ch0(2[89]|3[0-9]|4[0-2])", p.name) or "ch037" in p.name:
        continue
    t = p.read_text(encoding="utf-8")
    b, f = extract_body_and_footer(t)
    cleaned = polish_body(b)
    if cleaned != b:
        p.write_text(cleaned.rstrip() + "\n\n" + f, encoding="utf-8")
        b = cleaned
    c = hz(b)
    foot = t.count("*（上架连载稿")
    v16 = 1 if ("一念出塔" in b or "一念收塔" in b) else 0
    st = "OK" if LO <= c <= HI else ("LOW" if c < LO else "HIGH")
    rows.append((p.stem, c, st, foot, v16))

for r in rows:
    print(f"{r[0]}\t{r[1]}\t{r[2]}\tfooter={r[3]}\tv16={r[4]}")
print("---")
print(f"OK: {sum(1 for r in rows if r[2]=='OK')}/{len(rows)}")
