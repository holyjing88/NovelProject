# -*- coding: utf-8 -*-
import re, os
ROOT = os.path.join(os.path.dirname(__file__), "..", "chapters")
MARKERS = re.compile(r"留灯账|馈缘|照路余恩|馈灯|同心灯|盟灯|纳绶|纳府")
for vol in ["vol01-青萝灯起.md","vol02-云岚杂役.md","vol03-幽灯枯骨.md","vol04-玄京封灯.md","vol05-万古长明.md"]:
    t = open(os.path.join(ROOT,vol),encoding="utf-8").read()
    parts = re.split(r"(?=### 第)", t)
    missing = []
    for p in parts[1:]:
        m = re.match(r"### 第([^\n]+)", p)
        if m and not MARKERS.search(p):
            missing.append(m.group(1)[:20])
    print(vol, "missing", len(missing), missing[:8])
