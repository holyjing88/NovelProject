# -*- coding: utf-8 -*-
"""v38 留存优先精修：加厚 · 章末钩 · 去重（ch001-049）"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import body_chars, extract_body_and_footer, hz
from retention_data import REPLACE_PAIRS, RETENTION_END, THICKEN

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
TARGET_LO, TARGET_HI = 2000, 3000
MARKER = "<!-- v38-thicken -->"
END_MARKER = "<!-- v38-end -->"


def chapter_num(path: str) -> int:
    m = re.search(r"ch(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else 0


def apply_replacements(text: str, n: int) -> str:
    for old, new, chapters in REPLACE_PAIRS:
        if n in chapters and old in text:
            text = text.replace(old, new, 1)
    return text


def strip_old_markers(body: str) -> str:
    body = re.sub(r"\n*<!-- v38-thicken -->.*?(?=\n\n\*\*状态\*\*|\n\n---\n\n章末|$)", "", body, flags=re.S)
    body = re.sub(r"\n*<!-- v38-end -->.*?(?=\n\n\*\*状态\*\*|\n\n---\n\n章末|$)", "", body, flags=re.S)
    return body.rstrip()


def insert_thicken(body: str, n: int) -> str:
    body = strip_old_markers(body)
    if n not in THICKEN or MARKER in body:
        return body
    block = THICKEN[n].strip()
    if block in body:
        return body
    insert = f"\n\n{MARKER}\n\n{block}"
    if "**状态**" in body:
        return body.replace("\n\n**状态**", insert + "\n\n**状态**", 1)
    if "\n\n---\n\n章末" in body:
        return body.replace("\n\n---\n\n章末", insert + "\n\n---\n\n章末", 1)
    return body + insert


def apply_retention_end(body: str, n: int) -> str:
    if n not in RETENTION_END:
        return body
    end = RETENTION_END[n].strip()
    # remove prior v38-end block
    body = re.sub(r"\n*<!-- v38-end -->.*?(?=\n\n<!-- v38-thicken -->|\n\n\*\*状态\*\*|\n\n---\n\n章末|$)", "", body, flags=re.S)
    anchor = "\n\n**状态**" if "**状态**" in body else "\n\n---\n\n章末"
    if anchor not in body:
        return body
    head, tail = body.split(anchor, 1)
    # drop last short narrative paragraph if replacing weak ending
    paras = [p.strip() for p in re.split(r"\n\n+", head.strip()) if p.strip()]
    if paras and hz(paras[-1]) < 90:
        paras = paras[:-1]
    head = "\n\n".join(paras)
    return f"{head}\n\n{END_MARKER}\n\n{end}{anchor}{tail}"


def update_footer(footer: str) -> str:
    if "v38留存" not in footer:
        footer = footer.replace(
            "**v37正文迭代**",
            "**v37正文迭代** · **v38留存**",
        )
    return footer


def process(path: str) -> tuple[bool, int, int]:
    n = chapter_num(path)
    if n < 1 or n > 49:
        return False, 0, 0
    text = open(path, encoding="utf-8").read()
    before = body_chars(text)
    text = apply_replacements(text, n)
    body, footer = extract_body_and_footer(text)
    body = insert_thicken(body, n)
    body = apply_retention_end(body, n)
    footer = update_footer(footer)
    new_text = body + "\n\n" + footer if footer else body + "\n"
    after = hz(body)
    if new_text != text:
        open(path, "w", encoding="utf-8", newline="\n").write(new_text)
        return True, before, after
    return False, before, after


def main() -> None:
    updated = 0
    short = 0
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        changed, before, after = process(path)
        n = chapter_num(path)
        if n > 49:
            continue
        if after < TARGET_LO:
            short += 1
        if changed:
            updated += 1
            print(f"ch{n:03d} {before}->{after} hz")
    print(f"updated {updated}, still short {short}")


if __name__ == "__main__":
    main()
