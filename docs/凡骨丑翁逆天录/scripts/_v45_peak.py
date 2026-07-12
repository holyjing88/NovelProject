# -*- coding: utf-8 -*-
"""v45 爆款封顶：补字至≥1900 · 修状态行 · 去末段复读 · 脚注 v45"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, TARGET_IDEAL, TARGET_HI, extract_body_and_footer, hz
from v45_topup_data import TOPUP

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
CHAPTERS = {n for n in range(1, 64)} | {130}
END_MARK = "\n\n---\n\n章末"
SPLIT = re.compile(r"(?<=[。！？])")

DEFAULT_STATUS = (
    "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · "
    "鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
)
STATUS_130 = (
    "**状态**：大境·炼气十三层 · 资质·丑骨末席（伪灵根） · "
    "鸿蒙九劫瓮·醒（未显真名） · 宗门·外门复测 · 洞府·瓮穴灵穴"
)
STATUS_63 = (
    "**状态**：大境·炼气一层 · 资质·丑骨末席（伪灵根） · "
    "鸿蒙九劫瓮·醒（瓮穴灵穴） · 宗门·丙九杂役 · 漏舍凡舍"
)


def dedupe_sentences(text: str) -> str:
    chunks = [c.strip() for c in SPLIT.split(text) if c.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for c in chunks:
        key = re.sub(r"\s+", "", c)
        if len(key) >= 8 and key in seen:
            continue
        seen.add(key)
        out.append(c)
    return "".join(out)


def reflow_paras(body: str) -> str:
    if "\n\n" in body and body.count("\n\n") >= 4:
        paras = [dedupe_sentences(p.strip()) for p in body.split("\n\n") if p.strip()]
        return "\n\n".join(paras)
    parts = SPLIT.split(body)
    paras: list[str] = []
    buf = ""
    for p in parts:
        if not p.strip():
            continue
        buf += p
        if len(buf) >= 100 or p.strip().endswith("」"):
            if len(buf) >= 30:
                paras.append(buf.strip())
                buf = ""
    if buf.strip():
        paras.append(buf.strip())
    return "\n\n".join(paras)


def insert_before_chapter_end(body: str, block: str) -> str:
    block = block.strip()
    if not block or block in body:
        return body
    if END_MARK in body:
        head, tail = body.split(END_MARK, 1)
        return head.rstrip() + "\n\n" + block + END_MARK + tail
    return body.rstrip() + "\n\n" + block


def fix_footer(footer: str, n: int) -> str:
    footer = re.sub(r" · \*\*v44爆款精修\*\*", "", footer)
    footer = re.sub(r" · \*\*v42起点10\*\*", "", footer)
    footer = re.sub(r"\*\*v41综合10\*\*", "", footer)
    footer = re.sub(r" ·\s*·", " ·", footer)
    if "v45爆款10" not in footer and "对照" in footer:
        footer = footer.replace("）", " · **v45爆款10**）", 1)
    return footer


def ensure_status(raw: str, n: int) -> str:
    if "**状态**" in raw:
        return raw
    if n == 130:
        st = STATUS_130
    elif n == 63:
        st = STATUS_63
    elif n >= 31:
        st = DEFAULT_STATUS
    else:
        st = "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠 · 洞府·漏舍凡舍"
    if END_MARK in raw:
        return raw.replace(END_MARK, f"\n\n{st}{END_MARK}", 1)
    return raw + f"\n\n{st}\n"


def process(path: str) -> tuple[int, int, int]:
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in CHAPTERS:
        return n, 0, 0

    raw = open(path, encoding="utf-8").read()
    raw = ensure_status(raw, n)
    body, footer = extract_body_and_footer(raw)
    before = hz(body)

    body = reflow_paras(body)
    body = re.sub(r"<!-- v38-end -->", "", body)
    body = re.sub(r"<!-- v38-topup -->.*?<!--", "<!--", body)

    blocks = list(TOPUP.get(n, []))
    bi = 0
    guard = 0
    while hz(body) < TARGET_IDEAL and guard < 20:
        guard += 1
        if bi < len(blocks):
            body = insert_before_chapter_end(body, blocks[bi])
            bi += 1
            continue
        break

    body = dedupe_sentences(body)
    body = reflow_paras(body)

    if hz(body) > TARGET_HI:
        while hz(body) > TARGET_HI and "\n\n" in body:
            paras = body.rsplit("\n\n", 1)
            if len(paras) < 2:
                break
            body = paras[0]
            if hz(body) < TARGET_LO:
                body = paras[0] + "\n\n" + paras[1]
                break

    footer = fix_footer(footer, n)
    new_raw = body + footer
    open(path, "w", encoding="utf-8").write(new_raw)
    return n, before, hz(body)


def main():
    results = []
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        results.append(process(p))
    short = [(n, a) for n, b, a in results if a < TARGET_LO]
    print("PROCESSED", len(results))
    print("SHORT", short)
    print("BELOW_IDEAL", [(n, a) for n, b, a in results if a < TARGET_IDEAL])


if __name__ == "__main__":
    main()
