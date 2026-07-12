# -*- coding: utf-8 -*-
"""v40 修复：去重 topup/thicken · 单章末钩 · 补字闸"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, extract_body_and_footer, hz
from retention_data import RETENTION_END, THICKEN
from retention_topup import TOPUP, FILL
from _v38_fixup import (
    THICKEN_MARKER,
    TOPUP_MARKER,
    END_MARKER,
    clean_thicken_text,
    default_status,
    update_footer,
    chapter_num,
)

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
SPLIT = re.compile(r"(?<=[。！？])")
GENERIC = (
    "他低声道：「手稳，恩不断；恩不断，汤就不凉。」",
    "坛沿他仍擦。擦时指节白，白像证：辱在册，恩在胸，分列不混。",
    "还远不怕，怕的是汤凉——汤在叶铺，在刘婆灶，在心里。",
    "泥岗根在，坛沿在，还路在——还路在，手就在；手在，恩就不断。",
    "独眼平，像看秤——秤在，铺就不关；铺不关，汤就能还热。",
    "末席也是席，席在，手就稳——稳了，才配听帖，才配上路。",
)


def dedupe_sents(text: str) -> str:
    chunks = [c.strip() for c in SPLIT.split(text) if c.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for c in chunks:
        if c in GENERIC:
            continue
        key = re.sub(r"\s+", "", c)
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return "".join(out)


def dedupe_paras(text: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", text.strip()) if p.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for p in paras:
        key = re.sub(r"\s+", "", p)
        if key in seen:
            continue
        seen.add(key)
        out.append(dedupe_sents(p))
    return "\n\n".join(out)


def extract_main(body: str) -> str:
    m = re.search(rf"^(.*?)(?=\n\n{re.escape(THICKEN_MARKER)}|\n\n{re.escape(TOPUP_MARKER)}|\n\n{re.escape(END_MARKER)}|\n\n\*\*状态\*\*)", body, re.S)
    return m.group(1).strip() if m else body.strip()


def rebuild(n: int, main: str) -> str:
    parts = [dedupe_paras(main)]
    if n in THICKEN:
        th = dedupe_sents(clean_thicken_text(THICKEN[n]))
        if th:
            parts.append(f"{THICKEN_MARKER}\n\n{th}")
    top = ""
    if n in TOPUP:
        top = dedupe_paras(TOPUP[n].strip())
    elif n in FILL:
        top = dedupe_paras(FILL[n].strip())
    if top:
        parts.append(f"{TOPUP_MARKER}\n\n{top}")
    end = RETENTION_END.get(n, "").strip()
    if end:
        parts.append(f"{END_MARKER}\n\n{end}")
    parts.append(default_status(n))
    return "\n\n".join(parts)


def pad_main(n: int, main: str) -> str:
    h = hz(main)
    if h >= TARGET_LO:
        return main
    extra = FILL.get(n) or TOPUP.get(n, "")
    if extra:
        main = main.rstrip() + "\n\n" + dedupe_paras(extra.split("\n\n")[0])
    return main


def process(path: str) -> tuple[int, int, float, bool]:
    n = chapter_num(path)
    if n < 1 or n > 49:
        return 0, 0, 0.0, False
    text = open(path, encoding="utf-8").read()
    before = hz(extract_body_and_footer(text)[0])
    body, footer = extract_body_and_footer(text)
    main = extract_main(body)
    main = pad_main(n, dedupe_paras(main))
    new_body = rebuild(n, main)
    footer = update_footer(footer)
    if "v40读者10" not in footer:
        footer = footer.replace("**v39封顶**", "**v39封顶** · **v40读者10**")
    new_text = new_body + "\n\n" + footer
    after = hz(extract_body_and_footer(new_text)[0])
    dup = _dup(new_body)
    changed = new_text != text
    if changed:
        open(path, "w", encoding="utf-8", newline="\n").write(new_text)
    return before, after, dup, changed


def _dup(t: str) -> float:
    s = [x.strip() for x in SPLIT.split(t) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)


def main() -> None:
    updated = short = high = 0
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = chapter_num(path)
        if n > 49:
            continue
        b, a, dup, ch = process(path)
        if ch:
            updated += 1
            print(f"ch{n:03d} {b}->{a} dup={dup:.3f}")
        if a < TARGET_LO:
            short += 1
        if dup >= 0.02:
            high += 1
    print(f"repair: updated={updated} short={short} dup>=2%={high}")


if __name__ == "__main__":
    main()
