# -*- coding: utf-8 -*-
import re
from pathlib import Path

code = Path(__file__).resolve().parent.joinpath("generate_vol45_expanded.py").read_text(encoding="utf-8")
ns = {}
for m in re.finditer(
    r'CHAPTERS\[(\d+)\]\s*=\s*\([^,]+,\s*\n\s*"""(.*?)"""\s*\)',
    code,
    re.DOTALL,
):
    ns[int(m.group(1))] = m.group(2)

BOILER_STARTS = (
    "围观百姓", "围观者", "章末，第", "长明不灭的，不是仙途",
    "夜风卷过承平门", "更鼓远传", "青萝镇口长明与皇城气运",
    "裴无妄虚影远观", "顾迟年立夜风中", "镇灯司甲士",
)


def clean(s):
    paras = [p.strip() for p in s.split("\n\n") if p.strip()]
    out, seen = [], set()
    for p in paras:
        if any(p.startswith(b) for b in BOILER_STARTS):
            continue
        if p.startswith("章回未完"):
            continue
        k = re.sub(r"\s+", "", p)[:80]
        if k in seen:
            continue
        seen.add(k)
        out.append(p)
    return "\n\n".join(out)


def cc(s):
    return len(re.sub(r"\s+", "", s))


for n in range(166, 221):
    c = cc(clean(ns[n]))
    flag = "LOW" if c < 2500 else ("HIGH" if c > 4500 else "OK")
    print(f"{n}: {c} {flag}")
