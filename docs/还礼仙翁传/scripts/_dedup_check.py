#!/usr/bin/env python3
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose_utils import hz, norm, clean_body, BOILERPLATE

PROSE = Path(__file__).resolve().parent.parent / "prose"

def dedup_paras(body):
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    seen = set()
    kept = []
    for p in paras:
        if any(m in p for m in BOILERPLATE):
            continue
        n = norm(p)
        if len(n) >= 30 and n in seen:
            continue
        if len(n) >= 30:
            seen.add(n)
        kept.append(p)
    return "\n\n".join(kept)

for n in range(15, 28):
    f = sorted(PROSE.glob(f"ch0{n:02d}-*.md"))[0]
    body = f.read_text(encoding="utf-8").split("---")[0]  # rough
    # proper split
    from prose_utils import extract_body_and_footer
    body, _ = extract_body_and_footer(f.read_text(encoding="utf-8"))
    d = dedup_paras(body)
    print(f"{f.name}: paras {len(body.split(chr(10)+chr(10)))} -> {len(d.split(chr(10)+chr(10)))}, hz {hz(body)} -> {hz(d)}")
