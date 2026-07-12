#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 thicken 污染 + 手修收尾。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hand_polish_strip import polish_body, is_filler, is_template_summary
from prose_utils import extract_body_and_footer, hz, norm

PROSE = Path(__file__).resolve().parent.parent / "prose"
LO, HI = 2000, 2600
CANON = re.compile(r"ch0(2[89]|3[0-9]|4[0-2])")

BOILER = (
    "他笑：「等。」",
    "添油加醋",
    "霍镇山按刀，刀稳半寸",
    "柳青鸢远观，剑穗无风",
    "塔意沉一寸",
    "莫长春不辩，只记这一日的礼",
    "还礼路长，一步是一记",
    "盼九月老头再送一礼",
    "弟子把宗主拍桌讲成戏本",
)


def clean_body(body: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    kept = []
    seen: set[str] = set()
    for p in paras:
        if any(b in p for b in BOILER):
            continue
        if is_filler(p) or is_template_summary(p):
            continue
        n = norm(p)
        if len(n) >= 36 and n in seen:
            continue
        if len(n) >= 36:
            seen.add(n)
        kept.append(p)
    return polish_body("\n\n".join(kept))


def main() -> None:
    from thicken_to_2000 import process_file

    names = [p.name for p in sorted(PROSE.glob("ch*.md")) if CANON.match(p.name) and "ch037" not in p.name]
    # 先清理
    for name in names:
        p = PROSE / name
        t = p.read_text(encoding="utf-8")
        b, f = extract_body_and_footer(t)
        b2 = clean_body(b)
        if b2 != b:
            p.write_text(b2.rstrip() + "\n\n" + f, encoding="utf-8")
    # 不足则 thicken
    for _ in range(4):
        for name in names:
            p = PROSE / name
            b, _ = extract_body_and_footer(p.read_text(encoding="utf-8"))
            if hz(b) < LO:
                process_file(p)
        # 再清污染
        for name in names:
            p = PROSE / name
            t = p.read_text(encoding="utf-8")
            b, f = extract_body_and_footer(t)
            b2 = clean_body(b)
            if b2 != b:
                p.write_text(b2.rstrip() + "\n\n" + f, encoding="utf-8")
    # 报告
    for name in names:
        p = PROSE / name
        t = p.read_text(encoding="utf-8")
        b, _ = extract_body_and_footer(t)
        c = hz(b)
        foot = t.count("*（上架连载稿")
        v16 = 1 if ("一念出塔" in b or "一念收塔" in b) else 0
        st = "OK" if LO <= c <= HI else ("LOW" if c < LO else "HIGH")
        print(f"{name}\t{c}\t{st}\tfooter={foot}\tv16={v16}")


if __name__ == "__main__":
    main()
