# -*- coding: utf-8 -*-
import re, os
ROOT = os.path.join(os.path.dirname(__file__), "..", "chapters")
KEEP_CH = {52, 58, 64, 100, 140, 185, 216}

def cn_to_int(s):
    num_map = {"零":0,"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9}
    if not s: return 0
    if s == "十": return 10
    result = 0
    if "百" in s:
        parts = s.split("百", 1)
        result += (num_map.get(parts[0], 1) if parts[0] else 1) * 100
        s = parts[1] if len(parts) > 1 else ""
    if "十" in s:
        idx = s.index("十")
        left, right = s[:idx], s[idx+1:]
        tens = num_map.get(left, 1) if left else 1
        ones = num_map.get(right, 0) if right else 0
        return result + tens * 10 + ones
    if len(s) == 1 and s in num_map:
        return result + num_map[s]
    return result

path = os.path.join(ROOT, "vol02-云岚杂役.md")
text = open(path, encoding="utf-8").read()
parts = re.split(r"(?=### 第)", text)
out = [parts[0]]
removed = 0
for part in parts[1:]:
    m = re.match(r"### 第([^\n]+)", part)
    if not m or "灯箓三转" not in part:
        out.append(part)
        continue
    cn = re.search(r"([一二三四五六七八九十百零]+)章", m.group(1))
    ch = cn_to_int(cn.group(1)) if cn else 0
    if ch in KEEP_CH:
        out.append(part)
        continue
    new_part = part.replace("灯箓三转，古篆微闪", "守岁灯芯微温")
    new_part = new_part.replace("灯箓三转", "灯芯古篆")
    if new_part != part:
        removed += part.count("灯箓三转") - new_part.count("灯箓三转")
    out.append(new_part)
open(path, "w", encoding="utf-8").write("".join(out))
print("removed approx", removed)
