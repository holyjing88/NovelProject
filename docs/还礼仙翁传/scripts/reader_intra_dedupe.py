#!/usr/bin/env python3
"""读者视角章内去重：同章重复段只留首条，标杆章跳过。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose_utils import extract_body_and_footer, norm

PROSE = Path(__file__).resolve().parent.parent / "prose"
CANON = re.compile(r"ch0(0[1-9]|[12][0-9]|30|3[1-9]|[4-5][0-9]|60|61)")
SKIP = {"ch001-劫后余寿.md", "ch003-塔鸣初缘.md", "ch037-丹堂大炼.md", "ch049-挽月反戈.md", "ch055-杖剑出.md", "ch061-天试旨到.md"}

# 同章内重复出现则只留第一条（归一化后 >=28 字）
MIN_DEDUPE = 20


def dedupe_intra(body: str) -> tuple[str, int]:
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    kept, seen = [], []
    removed = 0
    for p in paras:
        n = norm(p)
        if len(n) >= MIN_DEDUPE and n in seen:
            removed += 1
            continue
        if len(n) >= MIN_DEDUPE:
            seen.append(n)
        kept.append(p)
    return "\n\n".join(kept), removed


def main() -> None:
    total_removed = 0
    changed = 0
    for p in sorted(PROSE.glob("ch*.md")):
        if not CANON.match(p.name) or p.name in SKIP:
            continue
        text = p.read_text(encoding="utf-8")
        body, footer = extract_body_and_footer(text)
        new_body, n = dedupe_intra(body)
        if n:
            total_removed += n
            changed += 1
            p.write_text(new_body + "\n\n" + footer, encoding="utf-8")
            print(f"{p.name}: -{n} dup paras")
    print(f"done: {changed} files, {total_removed} paragraphs removed")


if __name__ == "__main__":
    main()
