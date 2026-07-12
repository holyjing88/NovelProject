#!/usr/bin/env python3
"""移除重复垫字段 + 保留单一留存钩。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose_utils import extract_body_and_footer, hz, norm
from retention_polish import RETENTION_END, SKIP, dedupe_paras, ensure_hook, is_bad_para

PROSE = Path(__file__).resolve().parent.parent / "prose"
LO = 2000
CANON = re.compile(r"ch0(0[1-9]|[12][0-9]|30|3[1-9]|[4-5][0-9]|60|61)")
PAD = "山门风过，袖仍空，塔意却沉了一寸"
QUALITY_PAD = "弟子渐散，散里仍回头瞧一眼灰袍袖空——瞧得像瞧一眼九月还能走多久。"


def scrub_body(body: str, name: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    kept = []
    seen_pad = False
    for p in paras:
        n = norm(p)
        if n == norm(PAD + "。") or n == norm(PAD):
            continue
        if p.strip().startswith("塔鸣极轻，轻像") and len(p) < 90:
            continue
        if "塔鸣轻荡，荡完又静" in p and len(p) < 60:
            continue
        if norm(p) == norm(QUALITY_PAD):
            if seen_pad:
                continue
            seen_pad = True
        kept.append(p)
    kept = dedupe_paras(kept)
    body = "\n\n".join(kept)
    if name not in SKIP:
        body = ensure_hook(name, body)
    return body


def main():
    for p in sorted(PROSE.glob("ch*.md")):
        if not CANON.match(p.name):
            continue
        t = p.read_text(encoding="utf-8")
        body, footer = extract_body_and_footer(t)
        body = scrub_body(body, p.name)
        if not footer:
            footer = f"---\n\n*（上架连载稿 · {p.stem.split('-', 1)[1]}）*\n"
        p.write_text(body.rstrip() + "\n\n" + footer, encoding="utf-8")
    print("dedupe_pad done")


if __name__ == "__main__":
    main()
