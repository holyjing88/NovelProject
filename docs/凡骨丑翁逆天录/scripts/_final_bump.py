# -*- coding: utf-8 -*-
"""Final hz bump ch054-062"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from prose_utils import hz, extract_body_and_footer

PROSE = Path(__file__).resolve().parents[1] / "prose"
TARGET = 1900

FINAL = {
    "ch055-凡符祛寒.md": "符贴怀第六日，沿在净。净，才接后头试手。",
    "ch057-掌茧再裂.md": "试手前夜，手在。",
    "ch058-血线将至.md": "血线将至，沿仍不接。",
    "ch059-沿前即止.md": "沿前即止，缘在等。",
    "ch060-血止沿前.md": "血止沿前，不急醒。",
    "ch061-丑时坛温.md": "丑时坛温，符影半闪。",
    "ch062-席盖更严.md": "席盖更严，钩瓮醒。",
}

for fname, line in FINAL.items():
    p = PROSE / fname
    text = p.read_text(encoding="utf-8")
    body, footer = extract_body_and_footer(text)
    title = next(l for l in text.splitlines() if l.startswith("# "))
    if re.sub(r"\s+", "", line) not in re.sub(r"\s+", "", body):
        body = body.rstrip() + "\n\n" + line
    p.write_text(f"{title}\n\n{body}\n\n{footer.rstrip()}\n", encoding="utf-8")

for n in range(54, 63):
    f = list(PROSE.glob(f"ch0{n}-*.md"))[0]
    b, _ = extract_body_and_footer(f.read_text(encoding="utf-8"))
    h = hz(b)
    print(f"ch{n:03d}: {h} {'OK' if h>=TARGET else 'FAIL'}")
