# -*- coding: utf-8 -*-
"""拆 WALL 长段（>180 字无空白）· 按句切分 · 保字闸 dup"""
import glob
import os
import re

from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
WALL_LIMIT = 180
CHUNK_TARGET = 150

SPLIT = re.compile(r"(?<=[。！？])")


def para_len(p: str) -> int:
    return len(re.sub(r"\s+", "", p))


def split_para(p):
    if para_len(p) <= WALL_LIMIT:
        return [p.strip()] if p.strip() else []
    sents = [x for x in SPLIT.split(p.strip()) if x.strip()]
    if len(sents) <= 1:
        return [p.strip()]
    chunks = []
    cur = ""
    for s in sents:
        trial = cur + s
        if cur and para_len(trial) > CHUNK_TARGET:
            chunks.append(cur.strip())
            cur = s
        else:
            cur = trial
    if cur.strip():
        chunks.append(cur.strip())
    # 若仍超长，硬二分
    out = []
    for c in chunks:
        if para_len(c) <= WALL_LIMIT:
            out.append(c)
        else:
            mid = len(c) // 2
            cut = c.rfind("。", 0, mid + 40)
            if cut < 40:
                cut = c.find("。", mid - 40)
            if cut > 0:
                out.append(c[: cut + 1].strip())
                rest = c[cut + 1 :].strip()
                if rest:
                    out.append(rest)
            else:
                out.append(c)
    return out


def wall_paras(body: str) -> int:
    n = 0
    for para in re.split(r"\n\s*\n", body):
        if para_len(para) > WALL_LIMIT:
            n += 1
    return n


def process_body(body: str) -> str:
    blocks = re.split(r"\n\s*\n", body)
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            new_blocks.append(block)
            continue
        new_blocks.extend(split_para(block))
    return "\n\n".join(new_blocks)


def main():
    updated = 0
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        raw = open(p, encoding="utf-8").read()
        body, footer = extract_body_and_footer(raw)
        before_w = wall_paras(body)
        if not before_w:
            continue
        new_body = process_body(body)
        after_w = wall_paras(new_body)
        if new_body == body:
            continue
        h = hz(new_body)
        if h < TARGET_LO or h > TARGET_HI:
            print(f"SKIP {os.path.basename(p)} hz={h} (字闸)")
            continue
        new_text = new_body + ("\n" + footer if footer else "")
        open(p, "w", encoding="utf-8", newline="\n").write(new_text)
        updated += 1
        print(f"{os.path.basename(p)} walls {before_w}->{after_w} hz={h}")
    print(f"done: updated={updated}")


if __name__ == "__main__":
    main()
