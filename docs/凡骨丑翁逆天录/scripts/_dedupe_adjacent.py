# -*- coding: utf-8 -*-
"""去除相邻重复句（拆段副产物）· 保字闸"""
import glob
import os
import re

from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
SPLIT = re.compile(r"(?<=[。！？])")


def norm(s):
    return re.sub(r"\s+", "", s)


def dedupe_para(p):
    p = p.strip()
    if not p or p.startswith("#"):
        return p
    parts = [x for x in SPLIT.split(p) if x.strip()]
    if len(parts) <= 1:
        return p
    out = []
    prev = None
    for s in parts:
        k = norm(s)
        if k != prev:
            out.append(s)
            prev = k
    return "".join(out)


def process_body(body):
    blocks = re.split(r"\n\s*\n", body)
    return "\n\n".join(dedupe_para(b) for b in blocks if b.strip())


def main():
    updated = 0
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        raw = open(p, encoding="utf-8").read()
        body, footer = extract_body_and_footer(raw)
        new_body = process_body(body)
        if new_body == body:
            continue
        h = hz(new_body)
        if h < TARGET_LO:
            print(f"SKIP {os.path.basename(p)} hz={h}")
            continue
        open(p, "w", encoding="utf-8", newline="\n").write(
            new_body + ("\n" + footer if footer else "")
        )
        updated += 1
        print(f"{os.path.basename(p)} hz={h}")
    print(f"done: updated={updated}")


if __name__ == "__main__":
    main()
