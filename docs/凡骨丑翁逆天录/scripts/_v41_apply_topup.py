# -*- coding: utf-8 -*-
"""v41 应用扩写块 · 清扫重复段 · 校验字闸"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, extract_body_and_footer, hz
from v41_topup_data import V41_TOPUP

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
SPLIT = re.compile(r"(?<=[。！？])")


def chapter_num(path: str) -> int:
    m = re.search(r"ch(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else 0


def dedupe_paras(text: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", text.strip()) if p.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for p in paras:
        key = re.sub(r"\s+", "", p)
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return "\n\n".join(out)


def scrub_double_phrases(text: str) -> str:
    for pat in ("那日那日", "扎掌那日扎掌那日", "兽栏那日那日"):
        text = text.replace(pat, pat.replace("那日那日", "那日").replace("扎掌那日扎掌那日", "扎掌那日"))
    return text


def extract_main(body: str) -> str:
    m = re.search(r"^(.*?)(?=\n\n---\n\n章末)", body, re.S)
    return m.group(1).strip() if m else body.strip()


def apply_topup(path: str) -> tuple[int, int]:
    n = chapter_num(path)
    if n not in V41_TOPUP:
        return 0, 0
    text = open(path, encoding="utf-8").read()
    before = hz(extract_body_and_footer(text)[0])
    body, footer_part = extract_body_and_footer(text)
    main = scrub_double_phrases(dedupe_paras(extract_main(body)))
    block = V41_TOPUP[n].strip()
    # 先移除旧 topup 重复段（连续无换行的大块）
    main = re.sub(r"\n[^\n#]{200,}(?=\n\n---)", "", main)
    main = main.rstrip() + "\n\n" + block
    main = dedupe_paras(main)
    # rebuild footer
    fm = re.search(r"（对照.*?）", text)
    note = fm.group(0) if fm else f"（对照 `05` §{n} · **v41综合10**）"
    if "v41" not in note:
        note = note.rstrip("）") + " · **v41综合10**）"
    st_m = re.search(r"\*\*状态\*\*：[^\n]+", text)
    status = st_m.group(0) if st_m else "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
    new_text = f"{main}\n\n---\n\n章末。\n\n{note}\n\n{status}\n"
    open(path, "w", encoding="utf-8", newline="\n").write(new_text)
    after = hz(extract_body_and_footer(new_text)[0])
    return before, after


def main() -> None:
    short = []
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = chapter_num(path)
        if n not in V41_TOPUP:
            continue
        b, a = apply_topup(path)
        flag = "OK" if a >= TARGET_LO else "SHORT"
        if a < TARGET_LO:
            short.append((n, a))
        print(f"ch{n:03d} {b}->{a} {flag}")
    print(f"short={short}")


if __name__ == "__main__":
    main()
