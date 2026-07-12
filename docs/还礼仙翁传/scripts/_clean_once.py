#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _final_clean import clean_body, CANON, PROSE, LO, HI
from prose_utils import extract_body_and_footer, hz
from thicken_to_2000 import process_file

names = [p.name for p in sorted(PROSE.glob("ch*.md")) if CANON.match(p.name) and "ch037" not in p.name]
for name in names:
    p = PROSE / name
    t = p.read_text(encoding="utf-8")
    b, f = extract_body_and_footer(t)
    b2 = clean_body(b)
    if b2 != b:
        p.write_text(b2.rstrip() + "\n\n" + f, encoding="utf-8")
for name in names:
    p = PROSE / name
    if hz(extract_body_and_footer(p.read_text(encoding="utf-8"))[0]) < LO:
        process_file(p)
for name in names:
    p = PROSE / name
    t = p.read_text(encoding="utf-8")
    b, f = extract_body_and_footer(t)
    b2 = clean_body(b)
    if b2 != b:
        p.write_text(b2.rstrip() + "\n\n" + f, encoding="utf-8")
        b = b2
    c = hz(b)
    foot = t.count("*（上架连载稿")
    v16 = 1 if ("一念出塔" in b or "一念收塔" in b) else 0
    st = "OK" if LO <= c <= HI else ("LOW" if c < LO else "HIGH")
    print(f"{name}\t{c}\t{st}\tfooter={foot}\tv16={v16}")
