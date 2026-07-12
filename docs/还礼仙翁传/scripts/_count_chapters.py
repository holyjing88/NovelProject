#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose_utils import body_chars, extract_body_and_footer, clean_body, hz

PROSE = Path(__file__).resolve().parent.parent / "prose"
for n in range(15, 28):
    files = sorted(PROSE.glob(f"ch0{n:02d}-*.md"))
    if not files:
        continue
    f = files[0]
    t = f.read_text(encoding="utf-8")
    body, footer = extract_body_and_footer(t)
    cleaned = clean_body(body)
    print(f"{f.name}: raw_hz={hz(body)}, cleaned_hz={hz(cleaned)}, footers={t.count('*（上架连载稿')}")
