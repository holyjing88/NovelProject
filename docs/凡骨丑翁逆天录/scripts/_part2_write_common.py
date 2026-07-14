# -*- coding: utf-8 -*-
"""Shared write pipeline for Part 2 prose clusters.

笔法：新稿脚注用「通俗笔锋」（见 31）；禁止再输出「仙凡笔锋 v2」为新稿标准。
"""
import importlib.util
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import _split_walls as split_walls
from _purify_v2_style import fix_v2_style, pad_part2, strip_meta_prefix
from prose_utils import TARGET_HI, TARGET_LO, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
_RW = None


def get_rw():
    global _RW
    if _RW is None:
        spec = importlib.util.spec_from_file_location(
            "rw", os.path.join(os.path.dirname(__file__), "..", "prose", "_rewrite_v2.py")
        )
        _RW = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_RW)
    return _RW


def sentence_keys(text: str):
    keys = set()
    for sent in re.split(r"(?<=[。！？])", text):
        s = sent.strip()
        if len(s) < 8:
            continue
        keys.add(re.sub(r"\s+", "", s))
    return keys


def filter_new_block(block: str, seen: set) -> str:
    out = []
    for full in re.split(r"(?<=[。！？])", block):
        s = full.strip()
        if not s:
            continue
        k = re.sub(r"\s+", "", s)
        if len(s) >= 8 and k in seen:
            continue
        seen.add(k)
        out.append(full)
    return "".join(out).strip()


def merge_expansions(body: str, n: int, pools: dict) -> str:
    seen = sentence_keys(body)
    for key in ("MIDDLE", "MIDDLE2", "MEGA", "TOPUP", "ULTRA", "TOPUP2"):
        block = pools.get(key, {}).get(n, "")
        block = block.strip()
        if not block:
            continue
        block = strip_meta_prefix(block)
        add = filter_new_block(block, seen)
        if add:
            body = body + "\n\n" + add if body else add
    return body


def write_chapter(n: int, body_core: str, meta: dict, pools: dict) -> tuple:
    """meta: CN, NAMES, FOOTERS callables/dicts"""
    rw = get_rw()
    CN, NAMES, FOOTERS = meta["CN"], meta["NAMES"], meta["FOOTERS"]
    body = merge_expansions(body_core.strip(), n, pools)
    body = rw.dedupe_sentences_light(body)
    final_pad = pools.get("FINAL_PAD", {}).get(n, "")
    if final_pad:
        add = filter_new_block(strip_meta_prefix(final_pad), sentence_keys(body))
        if add:
            body = body + "\n\n" + add
    body = fix_v2_style(body, n, light=True)
    h = hz(body)
    if h < TARGET_LO or h > TARGET_HI:
        raise SystemExit(f"ch{n:03d} hz={h} FAIL")
    if split_walls.wall_paras(body):
        raise SystemExit(f"ch{n:03d} WALL FAIL")
    ref, st = FOOTERS[n]
    footer = f"\n---\n\n章末\n\n（对照 `16` {ref} · **通俗笔锋**）\n\n**状态**：{st}\n"
    title = f"# 第{CN[n]}章 {NAMES[n]}"
    fname = f"ch{n:03d}-{NAMES[n]}.md"
    path = os.path.join(PROSE, fname)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(title + "\n\n" + body.strip() + footer)
    return fname, h
