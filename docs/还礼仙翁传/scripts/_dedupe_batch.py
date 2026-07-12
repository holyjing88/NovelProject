#!/usr/bin/env python3
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hand_polish_strip import polish_body
from prose_utils import extract_body_and_footer, hz

prose = Path(__file__).resolve().parent.parent / "prose"
for p in sorted(prose.glob("ch0*.md")):
    if not re.match(r"ch0(2[89]|3[0-9]|4[0-2])", p.name):
        continue
    if p.name.startswith("ch037"):
        continue
    text = p.read_text(encoding="utf-8")
    body, footer = extract_body_and_footer(text)
    cleaned = polish_body(body)
    if not footer:
        footer = f"---\n\n*（上架连载稿 · {p.stem.split('-', 1)[1]}）*\n"
    p.write_text(cleaned.rstrip() + "\n\n" + footer, encoding="utf-8")
    print(f"{p.name}: {hz(cleaned)}")
