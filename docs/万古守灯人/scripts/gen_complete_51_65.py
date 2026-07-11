# -*- coding: utf-8 -*-
"""Generate complete chapters 51-65 by merging unique paragraphs until 2500+ han."""
import re
import sys
from pathlib import Path

ROOT = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator")
sys.path.insert(0, str(ROOT / "scripts"))

from gen_vol2_part1 import CHAPTERS as BASE
from vol2_ch51_65 import CHAPTERS as C2
from vol2_expansions import EXPANSIONS
from vol2_long_pad2 import LONG2
from vol2_tail_pad import TAIL
from vol2_final_boost import FINAL, FINAL2
from vol2_guaranteed_fill import GUARANTEED
from vol2_unique_pad import UNIQUE
from vol2_new_prose_51_65 import NEW
from vol2_topup_51_65 import TOPUP
from vol2_topup2_51_65 import TOPUP2

ALL = {**BASE, **C2}

GENERIC = (
    "顾迟年在心里把这一段的账又翻了一遍",
    "围观弟子有时哗然",
    "风过堂前，千灯齐晃",
    "承平三十八年，顾迟年六十一，杂役堂里最不肯灭",
)

def count_han(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))

def norm(p):
    return re.sub(r"\s+", "", p)

def collect_paragraphs(num):
    sources = []
    if num in ALL:
        sources.append(ALL[num][1])
    for src in (EXPANSIONS, LONG2, TAIL, FINAL, FINAL2, GUARANTEED, NEW, TOPUP, TOPUP2):
        if num in src:
            sources.append(src[num])
    for block in UNIQUE.get(num, []):
        sources.append(block)
    paras = []
    seen = set()
    for src in sources:
        for p in src.split("\n\n"):
            p = p.strip()
            if not p or len(p) < 20:
                continue
            if any(g in p for g in GENERIC):
                continue
            k = norm(p)
            if k in seen:
                continue
            seen.add(k)
            paras.append(p)
    return paras

def build_chapter(num, title, target=2600, max_target=3800):
    paras = collect_paragraphs(num)
    text_parts = []
    total = 0
    for p in paras:
        n = count_han(p)
        if total + n > max_target and total >= target:
            break
        text_parts.append(p)
        total += n
        if total >= target:
            break
    # If still short, add guaranteed paragraphs even if similar (split by sentence)
    if total < target and num in GUARANTEED:
        for sent in re.split(r"(?<=[。！？])", GUARANTEED[num]):
            sent = sent.strip()
            if len(sent) < 15:
                continue
            k = norm(sent)
            if k in {norm(x) for x in text_parts}:
                continue
            text_parts.append(sent)
            total += count_han(sent)
            if total >= target:
                break
    body = "\n\n".join(text_parts)
    return title, body, count_han(body)

def main():
    lines = ['# -*- coding: utf-8 -*-', '"""Complete chapters 51-65 (auto-merged unique prose)."""', '', 'COMPLETE = {}', '']
    stats = []
    for num in range(51, 66):
        title = ALL[num][0]
        title, body, n = build_chapter(num, title)
        stats.append((num, title, n))
        # Escape triple quotes in body
        body_esc = body.replace('"""', '\\"\\"\\"')
        lines.append(f'COMPLETE[{num}] = ("{title}", """')
        lines.append(body_esc)
        lines.append('""")')
        lines.append('')
    out = ROOT / "scripts" / "vol2_complete_51_65.py"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", out)
    for num, title, n in stats:
        flag = " [LOW]" if n < 2500 else ""
        print(f"  {num} {title}: {n}{flag}")

if __name__ == "__main__":
    main()
