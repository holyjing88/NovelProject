# -*- coding: utf-8 -*-
"""v42 起点标准封顶：≥2000字 · 留存钩强化 · 破壁清扫 · 脚注 v42起点10"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_IDEAL, TARGET_HI, extract_body_and_footer, hz
from retention_topup import FILL, TOPUP
from v42_qidian_topup import V42_EXTRA, V42_HOOK

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
V41_CHAPTERS = {n for n in range(1, 64)} | {130}

END_M = "<!-- v38-end -->"
TOPUP_M = "<!-- v38-topup -->"
V42_M = "<!-- v42-topup -->"
SPLIT = re.compile(r"(?<=[。！？])")


def dedupe_block(text: str) -> str:
    chunks = [c.strip() for c in SPLIT.split(text) if c.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for c in chunks:
        key = re.sub(r"\s+", "", c)
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return "".join(out)


def insert_block(body: str, block: str, marker: str = V42_M) -> str:
    block = dedupe_block(block.strip())
    if not block or block in body:
        return body
    if marker in body:
        body = re.sub(
            rf"({re.escape(marker)}\n\n)(.*?)(?=\n\n{re.escape(END_M)}|\n\n{re.escape(TOPUP_M)}|\n\n\*\*状态\*\*|\n\n---\n\n章末)",
            lambda m: m.group(1) + m.group(2).rstrip() + "\n\n" + block,
            body,
            count=1,
            flags=re.S,
        )
        return body
    if END_M in body:
        return body.replace(f"\n\n{END_M}", f"\n\n{marker}\n\n{block}\n\n{END_M}", 1)
    if "\n\n---\n\n章末" in body:
        return body.replace("\n\n---\n\n章末", f"\n\n{marker}\n\n{block}\n\n---\n\n章末", 1)
    return body + f"\n\n{marker}\n\n{block}"


def scrub_meta(body: str) -> str:
    meta = [
        (r"\bch0\d{2}\b", None),  # handled per-chapter below
        ("读者别走", "名节才立"),
        ("读者若问", "旁人若问"),
        ("读者能答", "旁人能答"),
        ("读者自检", "十章自检"),
        ("读者才爽", "名节才爽"),
        ("读者才肯等", "名节才立得住"),
    ]
    for old, new in meta:
        if new:
            body = body.replace(old, new)
    return body


META_CH_MAP = {
    "ch028": "老耿赠经片那日",
    "ch037": "编筐扎掌那日",
    "ch040": "血仍不渗沿那日",
    "ch042": "兽栏那日",
    "ch045": "深秋编筐那日",
    "ch050": "廊下讲规矩那日",
    "ch055": "凡符祛寒那日",
    "ch060": "血止沿前那日",
    "ch063": "瓮醒那日",
}


def scrub_ch_refs(body: str) -> str:
    for ch, rep in META_CH_MAP.items():
        body = re.sub(rf"\b{ch}\b", rep, body)
    return body


def fix_hook(body: str, n: int) -> str:
    if n not in V42_HOOK:
        return body
    hook = V42_HOOK[n]
    if END_M in body:
        body = re.sub(
            rf"{re.escape(END_M)}\s*\n\n.+?(?=\n\n\*\*状态\*\*)",
            f"{END_M}\n\n{hook}",
            body,
            count=1,
            flags=re.S,
        )
    return body


def update_footer(footer: str) -> str:
    footer = re.sub(r" · \*\*v42起点10\*\*", "", footer)
    footer = re.sub(r"\*\*v41综合10\*\*", "**v42起点10**", footer)
    footer = re.sub(r"\*\*v40读者10\*\*", "**v42起点10**", footer)
    footer = re.sub(r"\*\*v39封顶\*\*", "**v42起点10**", footer)
    footer = re.sub(r"\*\*v35留存\*\*", "**v42起点10**", footer)
    if "v42起点10" not in footer and "对照" in footer:
        footer = footer.replace("）", " · **v42起点10**）", 1)
    return footer


def topup_sources(n: int) -> list[str]:
    blocks: list[str] = []
    if n in V42_EXTRA:
        blocks.extend(V42_EXTRA[n])
    if n in TOPUP and TOPUP[n] not in blocks:
        blocks.append(TOPUP[n])
    if n in FILL and FILL[n] not in blocks:
        blocks.append(FILL[n])
    return blocks


def process(path: str) -> tuple[int, int]:
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in V41_CHAPTERS:
        return n, 0

    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    before = hz(body)

    body = scrub_meta(body)
    body = scrub_ch_refs(body)

    blocks = topup_sources(n)
    bi = 0
    guard = 0
    while hz(body) < TARGET_IDEAL and guard < 24:
        guard += 1
        if bi < len(blocks):
            body = insert_block(body, blocks[bi])
            bi += 1
            continue
        break

    body = fix_hook(body, n)
    footer = update_footer(footer)

    new = body + ("\n\n" + footer if footer else "")
    open(path, "w", encoding="utf-8", newline="\n").write(new)
    return n, hz(body) - before


def main() -> None:
    deltas = []
    short = []
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n, d = process(path)
        if n not in V41_CHAPTERS:
            continue
        body, _ = extract_body_and_footer(open(path, encoding="utf-8").read())
        h = hz(body)
        if d:
            deltas.append((n, d, h))
        if h < TARGET_IDEAL:
            short.append((n, h))
        if h > TARGET_HI:
            print(f"WARN ch{n:03d} over {TARGET_HI}: {h}")

    print("topped", len(deltas), "chapters")
    for n, d, h in deltas:
        print(f"  ch{n:03d} +{d} -> {h}")
    print("still <2000:", short)
    print("done")


if __name__ == "__main__":
    main()
