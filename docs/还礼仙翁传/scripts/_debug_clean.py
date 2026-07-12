#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose_utils import extract_body_and_footer, clean_body, BOILERPLATE, hz

PROSE = Path(__file__).resolve().parent.parent / "prose"
for name in ["ch016-赤焰来使.md", "ch023-赵之妒火.md", "ch024-小满情报.md", "ch026-坊市闲逛.md"]:
    f = PROSE / name
    body, _ = extract_body_and_footer(f.read_text(encoding="utf-8"))
    import re
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    cleaned_paras = [p.strip() for p in re.split(r"\n\n+", clean_body(body).strip()) if p.strip()]
    removed = set(paras) - set(cleaned_paras)
    print(f"\n{name}: {hz(body)} -> {hz(clean_body(body))}, removed {len(removed)} paras")
    for p in removed:
        for m in BOILERPLATE:
            if m in p:
                print(f"  BOILERPLATE [{m}]: {p[:60]}...")
                break
        else:
            print(f"  DUP?: {p[:80]}...")
