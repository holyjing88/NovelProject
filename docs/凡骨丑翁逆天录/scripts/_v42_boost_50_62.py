# -*- coding: utf-8 -*-
"""v42 坛温线 ch50-62 补至起点标准（不截断正文）"""
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_IDEAL, extract_body_and_footer, hz
from _v42_finalize import BOOST, EXTRA2, HOOKS, STATUS, DEFAULT_ST, insert_sentences, fix_tail

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

for n in range(50, 63):
    paths = glob.glob(os.path.join(PROSE, f"ch{n:03d}*.md"))
    if not paths:
        continue
    path = paths[0]
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    # 仅去掉重复状态/钩，不截正文
    body = re.sub(r"\n\n\*\*状态\*\*：.+", "", body)
    body = re.sub(r"\n\n<!-- v38-end -->.*?(?=\n\n---\n\n章末|\Z)", "", body, flags=re.S)
    body = body.rstrip()

    for s in BOOST.get(n, []) + EXTRA2.get(n, []):
        if hz(body) >= TARGET_IDEAL:
            break
        if s not in body:
            body = insert_sentences(body, [s])

    body = fix_tail(body, n)
    footer = re.sub(r"\n\*\*状态\*\*：.+", "", footer)
    if n == 55 and "符·凡符祛寒" not in footer:
        footer = footer.rstrip() + "\n\n**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍 · 符·凡符祛寒（凡品·防）"
    footer = re.sub(r"\*\*v41综合10\*\*", "**v42起点10**", footer)
    if "v42起点10" not in footer:
        footer = footer.replace("）", " · **v42起点10**）", 1)
    open(path, "w", encoding="utf-8", newline="\n").write(body + "\n\n" + footer)
    b, _ = extract_body_and_footer(open(path, encoding="utf-8").read())
    print(f"ch{n:03d} -> {hz(b)}")
