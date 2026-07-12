# -*- coding: utf-8 -*-
"""v45b 仅追加补字至≥1670 · 不删减正文"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, TARGET_IDEAL, extract_body_and_footer, hz
from v45_topup_data import TOPUP

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
CHAPTERS = {n for n in range(1, 64)} | {130}
END_MARK = "\n\n---\n\n章末"


def insert_before_end(body: str, block: str) -> str:
    block = block.strip()
    if not block or block in body:
        return body
    if END_MARK in body:
        head, tail = body.split(END_MARK, 1)
        return head.rstrip() + "\n\n" + block + END_MARK + tail
    return body.rstrip() + "\n\n" + block


def fix_footer(footer: str) -> str:
    if "v45爆款10" not in footer and "对照" in footer:
        footer = footer.replace("）", " · **v45爆款10**）", 1)
    return footer


def process(path: str) -> tuple[int, int, int]:
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in CHAPTERS:
        return n, 0, 0
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    before = hz(body)
    blocks = list(TOPUP.get(n, []))
    bi = 0
    while hz(body) < TARGET_LO and bi < len(blocks):
        body = insert_before_end(body, blocks[bi])
        bi += 1
    footer = fix_footer(footer)
    open(path, "w", encoding="utf-8").write(body + footer)
    return n, before, hz(body)


def main():
    results = [process(p) for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md")))]
    short = [(n, a) for n, b, a in results if a < TARGET_LO]
    print("SHORT", len(short), short)
    print("OK", len(results) - len(short), "/", len(results))


if __name__ == "__main__":
    main()
