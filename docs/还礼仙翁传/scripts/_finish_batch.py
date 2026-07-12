#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thicken_to_2000 import process_file, PROSE
from prose_utils import hz, extract_body_and_footer

LO, HI = 2000, 2600
names = [
    n.name
    for n in sorted(PROSE.glob("ch*.md"))
    if re.match(r"ch0(2[89]|3[0-9]|4[0-2])", n.name) and "ch037" not in n.name
]

for _ in range(8):
    for n in names:
        p = PROSE / n
        if hz(extract_body_and_footer(p.read_text(encoding="utf-8"))[0]) >= 2180:
            continue
        process_file(p)

for n in names:
    p = PROSE / n
    t = p.read_text(encoding="utf-8")
    b, f = extract_body_and_footer(t)
    paras = [x.strip() for x in re.split(r"\n\n+", b.strip()) if x.strip()]
    kept = [x for x in paras if "添油加醋" not in x]
    nb = "\n\n".join(kept)
    if nb != b:
        p.write_text(nb.rstrip() + "\n\n" + f, encoding="utf-8")
        b = nb
    c = hz(b)
    foot = t.count("*（上架连载稿")
    v16 = 1 if ("一念出塔" in b or "一念收塔" in b) else 0
    st = "OK" if LO <= c <= HI else ("LOW" if c < LO else "HIGH")
    print(f"{n}\t{c}\t{st}\tfooter={foot}\tv16={v16}")
