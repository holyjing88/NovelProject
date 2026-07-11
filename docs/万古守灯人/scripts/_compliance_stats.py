# -*- coding: utf-8 -*-
import re, os
ROOT = os.path.join(os.path.dirname(__file__), "..", "chapters")
FEED = re.compile(r"留灯账|馈缘|照路余恩|馈灯|同心灯|盟灯|纳绶|纳府|灯箓|万家火")
total = ch = hit = 0
for vol in ["vol01-青萝灯起.md","vol02-云岚杂役.md","vol03-幽灯枯骨.md","vol04-玄京封灯.md","vol05-万古长明.md"]:
    t = open(os.path.join(ROOT,vol),encoding="utf-8").read()
    parts = re.split(r"(?=### 第)", t)
    for p in parts[1:]:
        if re.match(r"### 第", p):
            ch += 1
            if FEED.search(p):
                hit += 1
    total += t.count("增叙第")
print("chapters", ch, "with_feed", hit, f"{100*hit/ch:.1f}%")
print("增叙", total, "章末", sum(open(os.path.join(ROOT,v),encoding='utf-8').read().count('章末，') for v in ["vol01-青萝灯起.md","vol02-云岚杂役.md","vol03-幽灯枯骨.md","vol04-玄京封灯.md","vol05-万古长明.md"]))
for k in ["留灯账","馈缘","照路余恩","同心灯","盟灯","吻","河灯鲤","老灰","墓灯鸦","照心斋","守灯静室","灯箓三转"]:
    c = sum(open(os.path.join(ROOT,v),encoding='utf-8').read().count(k) for v in ["vol01-青萝灯起.md","vol02-云岚杂役.md","vol03-幽灯枯骨.md","vol04-玄京封灯.md","vol05-万古长明.md"])
    print(k, c)
