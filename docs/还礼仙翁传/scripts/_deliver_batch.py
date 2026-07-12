#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终交付：thicken → 剥离垫字/ rumor 模板 → 校验≥2000。"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from thicken_to_2000 import process_file, PROSE
from prose_utils import hz, extract_body_and_footer

LO, HI = 2000, 2600
CANON = re.compile(r"ch0(2[89]|3[0-9]|4[0-2])")

BAD = (
    "添油加醋",
    "传到最后",
    "有人说",
    "他笑：「等。」",
    "霍镇山按刀，刀稳半寸",
    "柳青鸢远观，剑穗无风",
    "盼九月老头再送一礼",
)


def strip_bad(body: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    kept = []
    seen = set()
    for p in paras:
        if any(b in p for b in BAD):
            continue
        n = re.sub(r"\s+", "", p)
        if len(n) >= 40 and n in seen:
            continue
        if len(n) >= 40:
            seen.add(n)
        kept.append(p)
    return "\n\n".join(kept)


def main() -> None:
    names = [p.name for p in sorted(PROSE.glob("ch*.md")) if CANON.match(p.name) and "ch037" not in p.name]
    for _ in range(10):
        for n in names:
            p = PROSE / n
            if hz(extract_body_and_footer(p.read_text(encoding="utf-8"))[0]) >= 2200:
                continue
            process_file(p)
    for n in names:
        p = PROSE / n
        t = p.read_text(encoding="utf-8")
        b, f = extract_body_and_footer(t)
        b2 = strip_bad(b)
        if b2 != b:
            p.write_text(b2.rstrip() + "\n\n" + f, encoding="utf-8")
    # 若仍不足，再 thicken 一次并清 bad
    for n in names:
        p = PROSE / n
        if hz(extract_body_and_footer(p.read_text(encoding="utf-8"))[0]) < LO:
            for _ in range(6):
                process_file(p)
                t = p.read_text(encoding="utf-8")
                b, f = extract_body_and_footer(t)
                b2 = strip_bad(b)
                p.write_text(b2.rstrip() + "\n\n" + f, encoding="utf-8")
                if hz(b2) >= LO:
                    break
    print("chapter\tchars\tstatus\tfooter\tv16")
    for n in names:
        p = PROSE / n
        t = p.read_text(encoding="utf-8")
        b, _ = extract_body_and_footer(t)
        c = hz(b)
        foot = t.count("*（上架连载稿")
        v16 = 1 if ("一念出塔" in b or "一念收塔" in b) else 0
        st = "OK" if LO <= c <= HI else ("LOW" if c < LO else "HIGH")
        print(f"{n}\t{c}\t{st}\t{foot}\t{v16}")


if __name__ == "__main__":
    main()
