# -*- coding: utf-8 -*-
"""Test merge counts from part files + embedded CHAPTERS."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent

BOILER_STARTS = (
    "围观百姓", "围观者", "章末，第", "长明不灭的，不是仙途",
    "夜风卷过承平门", "更鼓远传", "青萝镇口长明与皇城气运",
    "裴无妄虚影远观", "顾迟年立夜风中", "镇灯司甲士",
)


def cc(s):
    return len(re.sub(r"\s+", "", s))


def dedupe_paras(blocks):
    out, seen = [], set()
    for p in blocks:
        p = p.strip()
        if not p or any(p.startswith(b) for b in BOILER_STARTS):
            continue
        if p.startswith("章回未完"):
            continue
        if re.match(r"^章末，第\d+章", p) and "开灯令在，长明在，路还长" in p:
            continue
        key = re.sub(r"\s+", "", p)[:80]
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def load_parts():
    new = {}
    for name in ("_vol45_chapters_part1.py", "_vol45_chapters_part2.py"):
        spec = importlib.util.spec_from_file_location(name, TOOLS / name)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for k, v in mod.__dict__.items():
            if k.startswith("CH") and k[2:].isdigit():
                new[int(k[2:])] = v.strip()
    return new


def load_embedded():
    code = (TOOLS / "generate_vol45_expanded.py").read_text(encoding="utf-8")
    ns = {}
    for m in re.finditer(
        r'CHAPTERS\[(\d+)\]\s*=\s*\([^,]+,\s*\n\s*"""(.*?)"""\s*\)',
        code,
        re.DOTALL,
    ):
        ns[int(m.group(1))] = m.group(2).strip()
    return ns


parts = load_parts()
embedded = load_embedded()

for n in range(166, 221):
    blocks = []
    if n in parts:
        blocks.extend(parts[n].split("\n\n"))
    if n in embedded:
        blocks.extend(embedded[n].split("\n\n"))
    paras = dedupe_paras(blocks)
    c = cc("\n\n".join(paras))
    flag = "LOW" if c < 2500 else ("HIGH" if c > 4500 else "OK")
    print(f"{n}: {c} {flag}")
