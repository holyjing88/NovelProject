# -*- coding: utf-8 -*-
"""v40 读者体验封顶：正文去重 · 通用 topup 剔除 · thicken 瘦身 · 章末钩刷新"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, extract_body_and_footer, hz
from _v38_fixup import (
    THICKEN_MARKER,
    TOPUP_MARKER,
    END_MARKER,
    clean_thicken_dict,
    apply_replacements,
    insert_topup,
    ensure_length,
    apply_retention_end,
    ensure_status,
    update_footer,
    chapter_num,
    strip_markers,
)
from retention_topup import TOPUP, FILL

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

GENERIC_TOPUP = (
    "他低声道：「手稳，恩不断；恩不断，汤就不凉。」",
    "坛沿他仍擦。擦时指节白，白像证：辱在册，恩在胸，分列不混。",
    "还远不怕，怕的是汤凉——汤在叶铺，在刘婆灶，在心里。",
    "泥岗根在，坛沿在，还路在——还路在，手就在；手在，恩就不断。",
    "独眼平，像看秤——秤在，铺就不关；铺不关，汤就能还热。",
    "末席也是席，席在，手就稳——稳了，才配听帖，才配上路。",
)

SPLIT = re.compile(r"(?<=[。！？])")


def split_sents(t: str) -> list[str]:
    return [s.strip() for s in SPLIT.split(t) if len(s.strip()) >= 8]


def dedupe_text(t: str) -> str:
    """按句去重，保留首次出现。"""
    chunks = [c.strip() for c in SPLIT.split(t) if c.strip()]
    if not chunks:
        return t
    seen: set[str] = set()
    out: list[str] = []
    for c in chunks:
        key = re.sub(r"\s+", "", c)
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return "".join(out)


def dedupe_paragraphs(t: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", t) if p.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for p in paras:
        key = re.sub(r"\s+", "", p)
        if key in seen:
            continue
        # 跳过通用 topup 段
        if any(g in p for g in GENERIC_TOPUP[:3]) and "手稳" in p:
            continue
        seen.add(key)
        out.append(dedupe_text(p))
    return "\n\n".join(out)


def scrub_topup_block(block: str) -> str:
    lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
    out: list[str] = []
    seen: set[str] = set()
    for ln in lines:
        if ln in GENERIC_TOPUP:
            continue
        key = re.sub(r"\s+", "", ln)
        if key in seen:
            continue
        if any(g in ln for g in ("手稳，恩不断", "坛沿他仍擦", "还远不怕，怕的是汤凉")):
            continue
        seen.add(key)
        out.append(ln)
    return "\n\n".join(out)


def process_file(path: str, thicken: dict[int, str]) -> tuple[int, int, float, bool]:
    n = chapter_num(path)
    if n < 1 or n > 49:
        return 0, 0, 0.0, False
    text = open(path, encoding="utf-8").read()
    before_hz = hz(extract_body_and_footer(text)[0])
    before_dup = _dup_ratio(extract_body_and_footer(text)[0])

    text = apply_replacements(text, n)
    body, footer = extract_body_and_footer(text)

    # 保留 marker 块，只洗主文
    th_m = re.search(
        rf"{re.escape(THICKEN_MARKER)}\s*\n\n(.*?)(?=\n\n{re.escape(TOPUP_MARKER)}|\n\n{re.escape(END_MARKER)}|\n\n\*\*状态\*\*)",
        body,
        re.S,
    )
    tu_m = re.search(
        rf"{re.escape(TOPUP_MARKER)}\s*\n\n(.*?)(?=\n\n{re.escape(END_MARKER)}|\n\n\*\*状态\*\*)",
        body,
        re.S,
    )
    en_m = re.search(
        rf"{re.escape(END_MARKER)}\s*\n\n(.*?)(?=\n\n\*\*状态\*\*|\n\n---\n\n章末)",
        body,
        re.S,
    )

    core = strip_markers(body)
    core = dedupe_paragraphs(core)

    if n in thicken and thicken[n].strip():
        core = insert_before_status(core, THICKEN_MARKER, dedupe_text(thicken[n].strip()))

    topup_parts: list[str] = []
    if n in TOPUP and TOPUP[n].strip():
        topup_parts.append(scrub_topup_block(TOPUP[n].strip()))
    if tu_m and tu_m.group(1).strip():
        scrubbed = scrub_topup_block(tu_m.group(1).strip())
        if scrubbed and scrubbed not in topup_parts:
            topup_parts.append(scrubbed)
    if topup_parts:
        merged = "\n\n".join(dict.fromkeys(topup_parts))  # 保序去重
        core = insert_before_status(core, TOPUP_MARKER, merged)

    core = ensure_length(core, n)
    core = apply_retention_end(core, n)
    core = ensure_length(core, n)
    core = ensure_status(core, n)

    footer = update_footer(footer.replace("**v39封顶**", "**v39封顶** · **v40读者10**"))
    if "v40读者10" not in footer:
        footer = footer.replace("**v39封顶**", "**v39封顶** · **v40读者10**")

    new_text = core + "\n\n" + footer if footer else core + "\n"
    after_hz = hz(extract_body_and_footer(new_text)[0])
    after_dup = _dup_ratio(extract_body_and_footer(new_text)[0])
    changed = new_text != text
    if changed:
        open(path, "w", encoding="utf-8", newline="\n").write(new_text)
    return before_hz, after_hz, after_dup, changed


def _dup_ratio(t: str) -> float:
    sents = split_sents(t)
    if not sents:
        return 0.0
    seen, dup = set(), 0
    for s in sents:
        k = re.sub(r"\s+", "", s)
        if k in seen:
            dup += 1
        seen.add(k)
    return dup / len(sents)


def insert_before_status(body: str, marker: str, block: str) -> str:
    insert = f"\n\n{marker}\n\n{block.strip()}"
    if marker in body:
        body = re.sub(
            rf"\n*{re.escape(marker)}.*?(?=\n\n{re.escape(TOPUP_MARKER)}|\n\n{re.escape(END_MARKER)}|\n\n\*\*状态\*\*|\n\n---\n\n章末|$)",
            "",
            body,
            flags=re.S,
        )
    if "**状态**" in body:
        return body.replace("\n\n**状态**", insert + "\n\n**状态**", 1)
    if "\n\n---\n\n章末" in body:
        return body.replace("\n\n---\n\n章末", insert + "\n\n---\n\n章末", 1)
    return body + insert


def main() -> None:
    thicken = clean_thicken_dict()
    updated = short = high_dup = 0
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = chapter_num(path)
        if n > 49:
            continue
        bh, ah, dup, changed = process_file(path, thicken)
        if changed:
            updated += 1
            print(f"ch{n:03d} {bh}->{ah} dup={dup:.3f}")
        if ah < TARGET_LO:
            short += 1
        if dup >= 0.02:
            high_dup += 1
    print(f"v40 done: updated={updated} short={short} dup>=2%={high_dup}")


if __name__ == "__main__":
    main()
