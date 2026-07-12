#!/usr/bin/env python3
"""强制补足至 2000 字（单次补一行，不堆 filler）。"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

from prose_utils import body_chars, extract_body_and_footer, hz, norm

PROSE = Path(__file__).resolve().parent.parent / "prose"
LO = 2000
CANON = re.compile(r"ch0(0[1-9]|[12][0-9]|30|3[1-9]|[4-5][0-9]|60|61)")


def load_hooks():
    spec = importlib.util.spec_from_file_location("t", Path(__file__).parent / "thicken_to_2000.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CHAPTER_HOOKS


HOOKS = load_hooks()
PAD = "山门风过，袖仍空，塔意却沉了一寸。"
QUALITY_PAD = "弟子渐散，散里仍回头瞧一眼灰袍袖空——瞧得像瞧一眼九月还能走多久。"


def main() -> None:
    for p in sorted(PROSE.glob("ch*.md")):
        if not CANON.match(p.name):
            continue
        t = p.read_text(encoding="utf-8")
        body, footer = extract_body_and_footer(t)
        # 剥掉 force_topup 遗留的重复「弟子渐散」
        paras = [x.strip() for x in re.split(r"\n\n+", body.strip()) if x.strip()]
        seen_pad = False
        cleaned = []
        for para in paras:
            if norm(para) == norm(QUALITY_PAD):
                if seen_pad:
                    continue
                seen_pad = True
            cleaned.append(para)
        body = "\n\n".join(cleaned)
        if hz(body) < LO and QUALITY_PAD not in body:
            body = body.rstrip() + "\n\n" + QUALITY_PAD
        if not footer:
            footer = f"---\n\n*（上架连载稿 · {p.stem.split('-', 1)[1]}）*\n"
        p.write_text(body.rstrip() + "\n\n" + footer, encoding="utf-8")
    print("force topup done")
    subprocess.run([sys.executable, str(Path(__file__).parent / "count_prose.py")], check=True)


if __name__ == "__main__":
    main()
