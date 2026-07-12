# -*- coding: utf-8 -*-
"""v39 修复章末结构：去重状态行 · 补 v38-end · 规范 footer"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import _v38_fixup as f
from prose_utils import body_chars, extract_body_and_footer, hz
from retention_data import RETENTION_END

PROSE = f.PROSE
END_M = f.END_MARKER


def strip_tail_garbage(text: str) -> str:
    # 保留首个脚注，去掉重复状态
    m = re.search(r"（对照 `05`", text)
    foot = m.group(0) + text[m.end() :].split("\n")[0] if m else ""
    if m:
        text = text[: m.start()].rstrip()
    text = re.sub(r"\n*<!-- v38-thicken -->.*", "", text, flags=re.S)
    text = re.sub(r"\n*<!-- v38-topup -->.*", "", text, flags=re.S)
    text = re.sub(r"\n*<!-- v38-end -->.*", "", text, flags=re.S)
    text = re.sub(r"\n*\*\*状态\*\*[^\n]*", "", text)
    text = re.sub(r"\n*---\s*\n*", "\n", text)
    text = re.sub(r"\n*章末。?\s*", "\n", text)
    return text.strip(), foot


def rebuild(n: int, text: str, thicken: dict[int, str]) -> str:
    body, old_foot = strip_tail_garbage(text)
    for old, new in f.META_INLINE:
        body = body.replace(old, new)
    body = f.apply_replacements(body, n)

    if n in thicken and thicken[n].strip():
        block = thicken[n].strip()
        if block not in body:
            body = f.insert_before_status(body, f.THICKEN_MARKER, block)

    body = f.insert_topup(body, f.TOPUP.get(n, "")) if n in f.TOPUP else body
    body = f.ensure_length(body, n)
    body = f.apply_retention_end(body, n)
    body = f.ensure_length(body, n)
    body = f.ensure_status(body, n)

    foot = old_foot or f"（对照 `05` §ch{n:03d} · **v37正文迭代**）"
    foot = f.update_footer(foot if foot.startswith("（") else f"（{foot}）")
    return body + f"\n\n---\n\n章末。\n\n{foot}\n"


def main() -> None:
    thicken = f.clean_thicken_dict()
    short = []
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = int(re.search(r"ch(\d+)", path).group(1))
        if n > 49:
            continue
        text = open(path, encoding="utf-8").read()
        new = rebuild(n, text, thicken)
        open(path, "w", encoding="utf-8", newline="\n").write(new)
        c = body_chars(new)
        print(f"ch{n:03d} {c}")
        if c < 2000:
            short.append((n, c))
    print("short:", short)


if __name__ == "__main__":
    main()
