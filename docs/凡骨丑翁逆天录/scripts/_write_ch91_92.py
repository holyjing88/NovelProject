# -*- coding: utf-8 -*-
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from prose_utils import body_chars

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "scripts" / "ch091_110_bodies.txt").read_text(encoding="utf-8")


def extract(n: int) -> str:
    m = re.search(rf"===CH{n}===(.*?)===CH{n + 1}===", text, re.S)
    return m.group(1).strip()


CHAPTERS = {
    91: (
        "第九十一章 废窑试炉",
        "（对照 `05` §91废窑试炉 · 药山占穴 · **仙凡笔锋 v2**）",
        "**状态**：大境·炼气五层 · 资质·丑骨末席（伪灵根） · 嗅诀·小成 · 丹路·开（渣） · 鸿蒙九劫瓮·醒 · 宗门·丙九杂役",
    ),
    92: (
        "第九十二章 废窑再试",
        "（对照 `05` §92废窑再试 · 控火渐熟 · **仙凡笔锋 v2**）",
        "**状态**：大境·炼气五层 · 资质·丑骨末席 · 嗅诀·小成 · 丹路·开（渣） · 鸿蒙九劫瓮·醒 · 宗门·丙九杂役",
    ),
}

for n, (title, note, status) in CHAPTERS.items():
    body = extract(n)
    content = f"# {title}\n\n{body}\n\n---\n\n章末\n\n{note}\n\n{status}\n"
    path = sorted((ROOT / "prose").glob(f"ch{n:03d}-*.md"))[0]
    path.write_text(content, encoding="utf-8")
    print(f"ch{n:03d}: {body_chars(content)}")
