#!/usr/bin/env python3
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose_utils import extract_body_and_footer, clean_body, norm, hz

PROSE = Path(__file__).resolve().parent.parent / "prose"
for name in ["ch016-赤焰来使.md", "ch023-赵之妒火.md", "ch024-小满情报.md", "ch025-卷末集结.md", "ch026-坊市闲逛.md", "ch027-第二次妖讯.md"]:
    f = PROSE / name
    body, _ = extract_body_and_footer(f.read_text(encoding="utf-8"))
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    cleaned_paras = [p.strip() for p in re.split(r"\n\n+", clean_body(body).strip()) if p.strip()]
    print(f"\n{name}: paras {len(paras)} -> {len(cleaned_paras)}, hz {hz(body)} -> {hz(clean_body(body))}")
    seen = {}
    for i, p in enumerate(paras):
        n = norm(p)
        if len(n) >= 36 and n in seen:
            print(f"  DUP para {seen[n]} and {i}: {p[:50]}...")
        if len(n) >= 36:
            seen[n] = i
