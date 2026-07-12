# -*- coding: utf-8 -*-
"""v47 仅补字至1780+ · 不裁剪"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz
from v47_topup_data import TOPUP

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
TARGET_CH = {2} | set(range(4, 31)) - {18, 24}
IDEAL_LO = 1780
END_MARK = "\n\n---\n\n章末"


def insert_before_end(body: str, block: str) -> str:
    block = block.strip()
    if not block or block in body:
        return body
    if END_MARK in body:
        head, tail = body.split(END_MARK, 1)
        return head.rstrip() + "\n\n" + block + END_MARK + tail
    return body.rstrip() + "\n\n" + block


def main():
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = int(re.search(r"ch(\d+)", p).group(1))
        if n not in TARGET_CH:
            continue
        raw = open(p, encoding="utf-8").read()
        body, footer = extract_body_and_footer(raw)
        before = hz(body)
        blocks = list(TOPUP.get(n, []))
        bi = 0
        while hz(body) < IDEAL_LO and bi < len(blocks):
            body = insert_before_end(body, blocks[bi])
            bi += 1
        if hz(body) != before:
            open(p, "w", encoding="utf-8").write(body + footer)
            print(f"ch{n:03d}: {before}->{hz(body)}")
        else:
            print(f"ch{n:03d}: {before} (no change)")


if __name__ == "__main__":
    main()
