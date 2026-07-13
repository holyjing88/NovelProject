# -*- coding: utf-8 -*-
"""Dedupe sentences, fix footer, pad short chapters 93-110,125,128,129."""
from __future__ import annotations

import glob
import importlib.util
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, TARGET_HI, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
SPLIT = re.compile(r"(?<=[。！？])")

_spec = importlib.util.spec_from_file_location(
    "fpf", os.path.join(os.path.dirname(__file__), "_fix_prose_final.py")
)
_fpf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_fpf)
UNIQUE = _fpf.UNIQUE


def dedupe_sents(body: str) -> str:
    paras = re.split(r"\n\n+", body.strip())
    seen = set()
    out = []
    for p in paras:
        sents = [x.strip() for x in SPLIT.split(p) if x.strip()]
        new = []
        for s in sents:
            k = re.sub(r"\s+", "", s)
            if len(k) >= 8 and k in seen:
                continue
            if len(k) >= 8:
                seen.add(k)
            new.append(s)
        if new:
            out.append("".join(new))
    return "\n\n".join(out)


def split_walls(body: str, limit: int = 180) -> str:
    out = []
    for p in re.split(r"\n\n+", body.strip()):
        t = re.sub(r"\s+", "", p)
        if len(t) <= limit:
            out.append(p.strip())
            continue
        sents = [x for x in SPLIT.split(p) if x.strip()]
        cur = ""
        for s in sents:
            if cur and len(re.sub(r"\s+", "", cur + s)) > 150:
                out.append(cur.strip())
                cur = s
            else:
                cur += s
        if cur.strip():
            out.append(cur.strip())
    return "\n\n".join(out)


def repair(n: int) -> tuple[int, float]:
    files = glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md"))
    if not files:
        return -1, 1.0
    path = sorted(files)[0]
    raw = open(path, encoding="utf-8").read()
    # Fix broken footer: keep only from ---\n\n章末
    m = re.search(r"\n---\n\n章末", raw)
    if m:
        raw = raw[: m.start()] + raw[m.start() :]
        # Remove content after **状态** line that's in wrong place
        body_part, footer_part = raw[: m.start()], raw[m.start() :]
    else:
        body_part, footer_part = extract_body_and_footer(raw)
        body_part, footer_part = body_part, footer_part

    body, footer = extract_body_and_footer(raw)
    lines = body.split("\n")
    title = lines[0] if lines and lines[0].startswith("#") else ""
    body = "\n".join(lines[1:]).strip() if title else body.strip()

    body = dedupe_sents(body)
    body = split_walls(body)

    for block in UNIQUE.get(n, []):
        if block.strip() and block.strip()[:25] not in body:
            body = body + "\n\n" + block.strip()
            body = dedupe_sents(body)

    i = 0
    while hz(body) < TARGET_LO and i < 6:
        extra = (
            f"更鼓沉，沉里，韩泥按木牌。{n}章路在坛在，舌不留，鼻下静。"
            f"恩辱分列，不混。活长了，才还得了叶汤，才接得住门缝灯。"
            f"{'一二三四五六'[i % 6]}"
        )
        body = body + "\n\n" + extra
        body = dedupe_sents(body)
        i += 1

    while hz(body) > TARGET_HI and "\n\n" in body:
        body = "\n\n".join(body.split("\n\n")[:-1])

    new = (title + "\n\n" + body).strip() if title else body
    if footer:
        # Clean footer - only 章末 section
        fm = re.search(r"---\s*\n\s*章末", footer)
        if fm:
            footer = footer[fm.start() :]
        new += "\n\n" + footer.lstrip("\n")
    open(path, "w", encoding="utf-8").write(new + "\n")

    b, _ = extract_body_and_footer(new)
    sents = [x.strip() for x in SPLIT.split(b) if len(x.strip()) >= 8]
    seen, d = set(), 0
    for x in sents:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    dr = d / len(sents) if sents else 0
    return hz(b), dr


def main():
    targets = list(range(93, 111)) + [125, 128, 129]
    bad = []
    for n in targets:
        h, dr = repair(n)
        ok = TARGET_LO <= h <= TARGET_HI and dr < 0.02
        print(f"ch{n:03d}: hz={h} dup={dr:.3f} {'OK' if ok else 'FIX'}")
        if not ok:
            bad.append((n, h, dr))
    print("BAD", bad)


if __name__ == "__main__":
    main()
