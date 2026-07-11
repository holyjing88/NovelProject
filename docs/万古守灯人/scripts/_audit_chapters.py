# -*- coding: utf-8 -*-
import re, os
from collections import Counter

root = os.path.join(os.path.dirname(__file__), "..", "chapters")
vols = [
    "vol01-青萝灯起.md", "vol02-云岚杂役.md", "vol03-幽灯枯骨.md",
    "vol04-玄京封灯.md", "vol05-万古长明.md",
]
short = []
total_han = 0
ch_count = 0
issues = Counter()

for v in vols:
    path = os.path.join(root, v)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    for pat, desc in [
        (r"符录", "符录"),
        (r"合欢宗|圣辉教|思过崖|黑风林", "旧专名"),
        (r"增叙第", "增叙模板"),
        (r"章末，", "章末meta"),
        (r"下一章[，,]", "下一章meta"),
    ]:
        issues[(v, desc)] += len(re.findall(pat, text))
    parts = re.split(r"(?=### 第)", text)
    for p in parts:
        m = re.match(r"### (第[^\n]+)", p)
        if not m:
            continue
        title = m.group(1)[:24]
        body = p[m.end() :]
        han = len(re.findall(r"[\u4e00-\u9fff]", body))
        total_han += han
        ch_count += 1
        if han < 2500:
            short.append((v.replace(".md", ""), title, han))

print(f"总章数: {ch_count}")
print(f"总汉字约: {total_han // 10000}.{total_han % 10000 // 1000}万 ({total_han})")
print(f"偏短章(<2500): {len(short)}")
vc = Counter(x[0] for x in short)
for k, n in sorted(vc.items()):
    print(f"  {k}: {n}")
print("\n问题计数:")
for (v, d), c in sorted(issues.items()):
    if c:
        print(f"  {v} {d}: {c}")

path5 = os.path.join(root, "vol05-万古长明.md")
with open(path5, "r", encoding="utf-8") as f:
    t5 = f.read()
for phrase in [
    "拒飞升化灯，在后三章",
    "非化灯，是念在",
    "魔退一线，人未寂",
    "急什么，灯还亮",
]:
    print(f'vol05 "{phrase[:12]}...": {t5.count(phrase)}')
