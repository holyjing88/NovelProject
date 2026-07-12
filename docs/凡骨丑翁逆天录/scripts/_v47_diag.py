# -*- coding: utf-8 -*-
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz

TARGET = {2} | set(range(4, 31)) - {18, 24}
PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

def dup(t):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)

for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", p).group(1))
    if n not in TARGET:
        continue
    raw = open(p, encoding="utf-8").read()
    b, footer = extract_body_and_footer(raw)
    h = hz(b)
    d = dup(b)
    en = len(re.findall(r"韩泥[「\"]?嗯", b))
    status_in_body = "**状态**" in b
    v47 = "v47爆款10" in raw
    flag = []
    if h < 1670:
        flag.append("SHORT")
    elif h < 1780:
        flag.append("LOW")
    elif h > 1950:
        flag.append("HIGH")
    if h > 2500:
        flag.append("OVER")
    if d >= 0.02:
        flag.append("DUP")
    if en > 1:
        flag.append(f"嗯x{en}")
    if status_in_body:
        flag.append("STAT_BODY")
    if not v47:
        flag.append("NO_V47")
    print(f"ch{n:03d}: {h} dup={d:.3f} en={en} {' '.join(flag) if flag else 'OK'}")
