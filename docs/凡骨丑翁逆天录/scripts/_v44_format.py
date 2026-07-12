# -*- coding: utf-8 -*-
"""v44b 恢复段落换行 · 句级去重保留结构"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
CHAPTERS = {n for n in range(1, 64)} | {130}
SPLIT = re.compile(r"(?<=[。！？])")


def dedupe_para(p: str) -> str:
    chunks = [c.strip() for c in SPLIT.split(p) if c.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for c in chunks:
        key = re.sub(r"\s+", "", c)
        if key in seen and len(key) >= 8:
            continue
        seen.add(key)
        out.append(c)
    return "".join(out)


def reflow(body: str) -> str:
    # 先按现有块切
    blocks = [b.strip() for b in re.split(r"\n\s*\n", body) if b.strip()]
    if len(blocks) <= 3:
        # 长块按对话/场景重分段
        text = "".join(blocks)
        parts = SPLIT.split(text)
        paras: list[str] = []
        buf = ""
        for p in parts:
            if not p.strip():
                continue
            buf += p
            if len(buf) >= 120 or p.strip().endswith("」") or p.strip().startswith("「"):
                if len(buf) >= 40:
                    paras.append(buf.strip())
                    buf = ""
        if buf.strip():
            paras.append(buf.strip())
        blocks = paras if paras else blocks
    cleaned = [dedupe_para(b) for b in blocks]
    return "\n\n".join(cleaned)


def fix_status(raw: str) -> str:
    raw = re.sub(r"\*\*状态\*\*：[^\n]+\n?", "", raw)
    m = re.search(r"（对照 `05`[^）]+）", raw)
    if m and "**状态**" not in raw:
        status = "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠 · 宗门·丙九杂役 · 漏舍凡舍"
        if "炼气" in raw or "ch063" in raw or "ch130" in raw:
            pass  # keep manual
        raw = raw.replace("\n\n---\n\n章末", f"\n\n{status}\n\n---\n\n章末", 1)
    return raw


def process(path: str):
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in CHAPTERS:
        return
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    body = reflow(body)
    # 去掉重复末钩（连续相似段）
    paras = body.split("\n\n")
    if len(paras) >= 2:
        last, prev = paras[-1], paras[-2]
        if len(set(last) & set(prev)) / max(len(set(last)), 1) > 0.6:
            paras = paras[:-1]
    body = "\n\n".join(paras)
    open(path, "w", encoding="utf-8").write(body + "\n\n" + footer)


for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    process(p)
print("FORMAT DONE")
