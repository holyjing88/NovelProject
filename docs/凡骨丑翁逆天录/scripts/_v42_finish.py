# -*- coding: utf-8 -*-
"""v42 收尾：ch050补写 · 全章脚注v42 · 留存钩 · 去重"""
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_IDEAL, extract_body_and_footer, hz
from _v41_peak import EXTEND, dedupe_paras, extract_main
from v42_qidian_topup import V42_HOOK

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
V42 = {n for n in range(1, 64)} | {130}
END_M = "<!-- v38-end -->"


def rebuild_footer(n, old):
    m = re.search(r"（对照.*?）", old)
    note = m.group(0) if m else f"（对照 `05` §{n} · **v42起点10**）"
    note = re.sub(r" · \*\*v4\d[^*]+\*\*", "", note)
    if "v42起点10" not in note:
        note = note.rstrip("）") + " · **v42起点10**）"
    st_m = re.search(r"\*\*状态\*\*：.+", old)
    st = st_m.group(0) if st_m else ""
    if n == 63:
        st = "**状态**：大境·炼气一层 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·醒（瓮穴灵穴） · 宗门·丙九杂役 · 漏舍凡舍"
    elif n == 130:
        st = "**状态**：大境·炼气十三层 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·内光 · 宗门·丙九杂役 · 瓮穴灵穴"
    elif n >= 31 and not st:
        st = "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
    return f"\n\n---\n\n章末。\n\n{note}\n\n{st}\n"


for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in V42:
        continue
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    main = dedupe_paras(extract_main(body))
    if n == 50 and n in EXTEND:
        main = main.rstrip() + "\n\n" + EXTEND[50]
        main = dedupe_paras(main)
    if n in (56, 57) and hz(main) < TARGET_IDEAL and n in EXTEND:
        main = main.rstrip() + "\n\n" + EXTEND[n][:120]
    hook = V42_HOOK.get(n, "")
    if hook:
        main = re.sub(r"\n\n<!-- v38-end -->.*?(?=\n\n---\n\n章末|\Z)", "", main, flags=re.S)
        main = main.rstrip() + f"\n\n{END_M}\n\n{hook}"
    footer = rebuild_footer(n, footer if footer else raw)
    open(path, "w", encoding="utf-8", newline="\n").write(main + footer)

short = []
for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in V42:
        continue
    b, _ = extract_body_and_footer(open(path, encoding="utf-8").read())
    if hz(b) < TARGET_IDEAL:
        short.append((n, hz(b)))
print("short", short)
