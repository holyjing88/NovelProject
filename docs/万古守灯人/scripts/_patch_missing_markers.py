# -*- coding: utf-8 -*-
import re, os
ROOT = os.path.join(os.path.dirname(__file__), "..", "chapters")
MARKERS = re.compile(r"留灯账|馈缘|照路余恩|馈灯|同心灯|盟灯|纳绶|纳府")
POOL = [
    "他在留灯账记一行：*帮一人，记一笔；账在，恩在。*",
    "守岁灯芯微温，馈缘↑，像古篆闪了一闪。",
    "馈灯链：赠礼已入账，只等后文当场还。",
    "灯箓账上，人间账与灯箓同频，因果未欠。",
    "他不邀功，只把半滴油、一条路写进留灯账。",
]

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

for vol in ["vol01-青萝灯起.md","vol02-云岚杂役.md","vol03-幽灯枯骨.md","vol04-玄京封灯.md","vol05-万古长明.md"]:
    path = os.path.join(ROOT, vol)
    text = open(path, encoding="utf-8").read()
    parts = re.split(r"(?=### 第)", text)
    out = [parts[0]]
    n = 0
    for part in parts[1:]:
        m = re.match(r"(### 第([^\n]+)\n)", part)
        if not m or MARKERS.search(part):
            out.append(part)
            continue
        cn = re.search(r"([一二三四五六七八九十百零]+)章", m.group(2))
        ch = cn_to_int(cn.group(1)) if cn else n
        inject = POOL[ch % len(POOL)]
        body = part[m.end():]
        paras = body.split("\n\n", 1)
        if len(paras) == 2:
            new_body = paras[0] + "\n\n" + inject + "\n\n" + paras[1]
        else:
            new_body = body.rstrip() + "\n\n" + inject + "\n"
        out.append(m.group(1) + new_body)
        n += 1
    open(path, "w", encoding="utf-8").write("".join(out))
    print("patched", vol, n)
