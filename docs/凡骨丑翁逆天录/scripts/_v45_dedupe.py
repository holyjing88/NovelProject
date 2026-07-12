# -*- coding: utf-8 -*-
"""v45c 句级去重（保留首句）· 去重后不足则补独段"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, TARGET_IDEAL, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
CHAPTERS = {n for n in range(1, 64)} | {130}
SPLIT = re.compile(r"(?<=[。！？])")
END_MARK = "\n\n---\n\n章末"

FILL: dict[int, list[str]] = {
    54: ["第四日，霜白。韩泥绕驿亭三步，像界——界内杂役，界外五脉。他不凑，只记：沿净，才接得住后头赠。"],
    55: ["僧离亭那日，他符藏怀，不示，不燃，像经片挪了地方。缘，不在符，在瓮眠等的那一日。"],
    56: ["第五日清晨，筐末扎紧。扎紧，像秤杆落盘。管事验筐底：「底不塌，季末记功。」"],
    57: ["试手前夜，坡下霜白。他摸木牌，与试手帖并放。并放，像命与规矩挨着。"],
    58: ["试手日午后，肩稳，像坡下站出来的实。实不在灵，在手。"],
    59: ["清晨霜白，丙九静一寸。静一寸，像沿前那一止。编筐末藤，藤刺再扎，血珠饱满。"],
    60: ["雪细停，棚静。静里更鼓远。远，像瓮将醒未醒，醒在缘，不在人催。"],
    61: ["丑时尽，天边白一线。白一线，像瓮醒前夜将至。将至，接席盖更严。"],
    62: ["风硬，席更严。严，像五十八年命跟坛，坛跟席，席跟沿。"],
}


def dup_rate(text: str) -> float:
    s = [x.strip() for x in SPLIT.split(text) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)


def dedupe_body(body: str) -> str:
    paras = body.split("\n\n")
    out_paras = []
    global_seen: set[str] = set()
    for para in paras:
        if para.strip() in ("---",) or para.startswith("#"):
            out_paras.append(para)
            continue
        chunks = [c.strip() for c in SPLIT.split(para) if c.strip()]
        kept = []
        for c in chunks:
            key = re.sub(r"\s+", "", c)
            if len(key) >= 8 and key in global_seen:
                continue
            global_seen.add(key)
            kept.append(c)
        if kept:
            out_paras.append("".join(kept))
    return "\n\n".join(out_paras)


def insert_before_end(body: str, block: str) -> str:
    block = block.strip()
    if not block or block in body:
        return body
    if END_MARK in body:
        head, tail = body.split(END_MARK, 1)
        return head.rstrip() + "\n\n" + block + END_MARK + tail
    return body + "\n\n" + block


def process(path: str) -> tuple[int, float, float, int]:
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in CHAPTERS:
        return n, 0, 0, 0
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    before_d = dup_rate(body)
    before_h = hz(body)
    body = dedupe_body(body)
    fi = 0
    fills = list(FILL.get(n, []))
    while (dup_rate(body) >= 0.02 or hz(body) < TARGET_LO) and fi < len(fills):
        body = insert_before_end(body, fills[fi])
        fi += 1
        body = dedupe_body(body)
    while hz(body) < TARGET_LO and fi < len(fills):
        body = insert_before_end(body, fills[fi])
        fi += 1
    open(path, "w", encoding="utf-8").write(body + footer)
    return n, before_d, dup_rate(body), hz(body)


def main():
    results = []
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        results.append(process(p))
    bad = [(n, bd, ad, h) for n, bd, ad, h in results if ad >= 0.02 or h < TARGET_LO]
    print("BAD", bad)
    print("OK", len(results) - len(bad), "/", len(results))


if __name__ == "__main__":
    main()
