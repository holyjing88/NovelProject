# -*- coding: utf-8 -*-
import re, os
ROOT = os.path.join(os.path.dirname(__file__), "..", "chapters")
rows = []
for vol in ["vol01-青萝灯起.md","vol02-云岚杂役.md","vol03-幽灯枯骨.md","vol04-玄京封灯.md","vol05-万古长明.md"]:
    t = open(os.path.join(ROOT, vol), encoding="utf-8").read()
    parts = re.split(r"(?=### 第)", t)
    for p in parts[1:]:
        m = re.match(r"### 第([^\n]+)", p)
        if m:
            hz = len(re.sub(r"\s", "", p))
            rows.append((hz, vol, m.group(1).strip()))
rows.sort()
for hz, vol, title in rows[:40]:
    print(hz, vol.split("-")[0], title)
