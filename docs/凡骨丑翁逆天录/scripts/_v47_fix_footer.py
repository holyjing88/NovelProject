# -*- coding: utf-8 -*-
"""Fix duplicate 章末 blocks from v47 batch pass."""
import glob, re, os

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
STATUS = (
    "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · "
    "鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"
)
FOOT_RE = re.compile(r"（对照 `05`[^）]*）")

for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", p).group(1))
    if n not in range(31, 51) or n in (35, 41):
        continue
    raw = open(p, encoding="utf-8").read()
    m = re.search(r"\n---\n", raw)
    if not m:
        continue
    body = raw[: m.start()].rstrip()
    foot_m = FOOT_RE.search(raw)
    if not foot_m:
        print(f"ch{n:03d}: no footnote")
        continue
    footnote = foot_m.group(0)
    if "v47爆款10" not in footnote:
        footnote = footnote.replace("）", " · **v47爆款10**）", 1)
    new_raw = body + "\n\n---\n\n章末\n\n" + footnote + "\n\n" + STATUS + "\n"
    open(p, "w", encoding="utf-8").write(new_raw)
    print(f"ch{n:03d}: fixed footer")
