# -*- coding: utf-8 -*-
import re, os
ROOT = os.path.join(os.path.dirname(__file__), "..", "chapters")
MARKERS = re.compile(r"留灯账|馈缘|照路余恩|馈灯|同心灯|盟灯|纳绶|纳府|灯箓|万家火|因果")

SPECIFIC = {
    28: "留灯账：*豪强夜袭，天煞门外围，因果记仇。*",
    48: "留灯账：*疏脉丹备十二人，七品灯丹标阶。*",
    73: "留灯账：*迟暮之约，万灯大会，羁绊↑。*",
    78: "留灯账：*化敌为友，霍照临心转，馈缘↑。*",
    83: "留灯账：*借光挡幡，五灯雏形。*",
    88: "留灯账：*冬典授牌，失嗅代价入账。*",
    93: "留灯账：*陆承安令，背叛阶梯。*",
    98: "留灯账：*枯骨岭时相，一日一年。*",
    118: "留灯账：*敛灯崖夜，承苦在肩。*",
    123: "留灯账：*云照传经，师徒馈缘↑。*",
    133: "留灯账：*诏云黑灯，镇灯司影。*",
    138: "留灯账：*敛灯崖拉袖，情感余温。*",
    143: "留灯账：*封灯风声入青萝，馈缘将报。*",
    148: "留灯账：*灯影预演，玄京入局。*",
    153: "留灯账：*九品照影符，灯籍标阶。*",
    158: "留灯账：*镇灯司招，制度之暗。*",
    163: "留灯账：*程不二遗图，施恩报恩。*",
    168: "留灯账：*旧灯库第一层，命灯器线索。*",
    173: "留灯账：*谢长缨铁证，落第案收。*",
    178: "留灯账：*青萝灯会，八阶灯河。*",
    183: "留灯账：*护制之灯，谢长缨危。*",
    188: "留灯账：*陆承安动摇，赎罪前夜。*",
    193: "留灯账：*非境之灯，天魔阶梯。*",
    198: "留灯账：*云照铸架，万古灯架。*",
    213: "留灯账：*万年一人，拒升抉择。*",
}

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
        if MARKERS.search(part):
            out.append(part)
            continue
        m = re.match(r"(### 第([^\n]+)\n)", part)
        if not m:
            out.append(part)
            continue
        cn = re.search(r"([一二三四五六七八九十百零]+)章", m.group(2))
        ch = cn_to_int(cn.group(1)) if cn else 0
        inject = SPECIFIC.get(ch, f"留灯账记一行：*第{ch}章，馈缘↑。*")
        out.append(m.group(1) + inject + "\n\n" + part[m.end():])
        n += 1
    open(path, "w", encoding="utf-8").write("".join(out))
    print(vol, n)
