# -*- coding: utf-8 -*-
"""Rewrite ch053-062 clean at >=1500 body chars."""
from __future__ import annotations

import re
from pathlib import Path

from prose_utils import TARGET_LO, body_chars

PROSE = Path(__file__).resolve().parent.parent / "prose"

FOOTERS = {
    53: (
        "（对照 `05` §52～54霜夜柴房 · 钩试手五日条 · **v41综合10**）\n\n"
        "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
    ),
    54: (
        "（对照 `05` §52～54坛温起伏 · 褐袍人候冬 · **v41综合10**）\n\n"
        "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
    ),
    55: (
        "（对照 `05` §55凡符祛寒 · `17` 密宗僧经老耿赠符 · 符录起KPI · **v41综合10**）\n\n"
        "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍 · 符·凡符祛寒（凡品·防）"
    ),
    56: (
        "（对照 `05` §56编筐季末 · 掌茧裂无血 · **v41综合10**）\n\n"
        "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
    ),
    57: (
        "（对照 `05` §57掌茧再裂 · 试手前夜手稳 · **v41综合10**）\n\n"
        "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
    ),
    58: (
        "（对照 `05` §58血近沿 · 试手过手稳 · **v41综合10**）\n\n"
        "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
    ),
    59: (
        "（对照 `05` §59血至沿前即止 · **v41综合10**）\n\n"
        "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
    ),
    60: (
        "（对照 `05` §60血止沿前·瓮温加剧 · **v41综合10**）\n\n"
        "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
    ),
    61: (
        "（对照 `05` §61丑时坛温加剧·符影半闪 · **v41综合10**）\n\n"
        "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（符影半闪） · 宗门·丙九杂役 · 漏舍凡舍"
    ),
    62: (
        "（对照 `05` §62席盖更严·不主动滴血 · 钩→瓮醒 · **v41综合10**）\n\n"
        "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
    ),
}

TITLES = {
    53: "霜夜柴房",
    54: "坛温起伏",
    55: "凡符祛寒",
    56: "编筐季末",
    57: "掌茧再裂",
    58: "血线将至",
    59: "沿前即止",
    60: "血止沿前",
    61: "丑时坛温",
    62: "席盖更严",
}


def dup_ratio(t: str) -> float:
    sents = [s.strip() for s in re.split(r"[。！？\n]", t) if len(s.strip()) >= 4]
    if not sents:
        return 0.0
    seen, dup = set(), 0
    for s in sents:
        if s in seen:
            dup += 1
        seen.add(s)
    return dup / len(sents)


def write_ch(n: int, body: str) -> tuple[int, float]:
    cn = "一二三四五六七八九十"[n // 10 - 5] + ("十" if n % 10 == 0 else "") + (
        "一二三四五六七八九十"[n % 10 - 1] if n % 10 else ""
    )
    if n == 53:
        cn = "五十三"
    elif n == 54:
        cn = "五十四"
    elif n == 55:
        cn = "五十五"
    elif n == 56:
        cn = "五十六"
    elif n == 57:
        cn = "五十七"
    elif n == 58:
        cn = "五十八"
    elif n == 59:
        cn = "五十九"
    elif n == 60:
        cn = "六十"
    elif n == 61:
        cn = "六十一"
    elif n == 62:
        cn = "六十二"
    text = (
        f"# 第{cn}章 {TITLES[n]}\n\n"
        f"{body.strip()}\n\n---\n\n章末。\n\n{FOOTERS[n]}\n"
    )
    path = next(PROSE.glob(f"ch{n:03d}-*.md"))
    path.write_text(text, encoding="utf-8")
    return body_chars(text), dup_ratio(body)


# Bodies loaded from companion module to keep script readable
from _bodies_clean_53_62 import BODIES  # noqa: E402

if __name__ == "__main__":
    for n in range(53, 63):
        hz, dup = write_ch(n, BODIES[n])
        flag = []
        if hz < TARGET_LO:
            flag.append("SHORT")
        if dup >= 0.02:
            flag.append(f"dup={dup:.3f}")
        print(f"ch{n:03d} hz={hz} dup={dup:.3f} {'OK' if not flag else ','.join(flag)}")
