# -*- coding: utf-8 -*-
"""Fix ch054-062: single title, body before footer, hz 1900-2100"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prose_utils import hz  # noqa: E402

PROSE = ROOT / "prose"
TARGET_LO, TARGET_HI = 1900, 2100

META = {
    54: ("第五十四章 坛温起伏", "§54坛温起伏 · 褐袍人候冬",
         "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    55: ("第五十五章 凡符祛寒", "§55凡符祛寒 · 老耿引僧赠符",
         "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍 · 符·凡符祛寒（凡品·防）"),
    56: ("第五十六章 编筐季末", "§56编筐季末 · 掌茧裂无血",
         "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    57: ("第五十七章 掌茧再裂", "§57掌茧再裂 · 试手前夜",
         "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    58: ("第五十八章 血线将至", "§58血线将至 · 试手过手稳",
         "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    59: ("第五十九章 沿前即止", "§59沿前即止 · 血不渗沿",
         "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    60: ("第六十章 血止沿前", "§60血止沿前 · 瓮温加剧",
         "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    61: ("第六十一章 丑时坛温", "§61丑时坛温 · 符影半闪",
         "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    62: ("第六十二章 席盖更严", "§62席盖更严 · 钩瓮醒",
         "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
}

SKIP_LINES = re.compile(r"^(#\s|章末。|---\s*$|（对照|^\*\*状态\*\*)")


def extract_prose_paras(text: str) -> list[str]:
    paras: list[str] = []
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block.startswith("# "):
            continue
        if block == "---":
            continue
        if block == "章末。":
            continue
        if block.startswith("（对照 `05`"):
            continue
        if block.startswith("**状态**"):
            continue
        # multi-line blocks: skip if every line is metadata
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if all(SKIP_LINES.match(ln) or ln == "---" for ln in lines):
            continue
        clean_lines = []
        for ln in lines:
            if ln.startswith("# ") or ln == "章末。" or ln == "---":
                continue
            if ln.startswith("（对照 `05`") or ln.startswith("**状态**"):
                continue
            clean_lines.append(ln)
        if clean_lines:
            paras.append("\n".join(clean_lines))
    # dedupe
    seen: set[str] = set()
    out: list[str] = []
    for p in paras:
        key = re.sub(r"\s+", "", p)
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def make_file(n: int, paras: list[str]) -> str:
    title_s, ref, status = META[n]
    body = "\n\n".join(paras)
    return (
        f"# {title_s}\n\n{body}\n\n"
        f"---\n\n章末。\n\n"
        f"（对照 `05` {ref} · **v45爆款10**）\n"
        f"**状态**：{status}\n"
    )


def main() -> None:
    fails = 0
    for n in range(54, 63):
        f = list(PROSE.glob(f"ch0{n}-*.md"))[0]
        paras = extract_prose_paras(f.read_text(encoding="utf-8"))
        body_hz = hz("\n\n".join(paras))
        text = make_file(n, paras)
        f.write_text(text, encoding="utf-8")
        h = hz("\n\n".join(paras))
        ok = TARGET_LO <= h <= TARGET_HI
        titles = text.count("\n# ")
        print(f"ch{n:03d}: {h} titles_extra={titles} {'OK' if ok else 'FAIL'}")
        if not ok:
            fails += 1
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
