# -*- coding: utf-8 -*-
"""Force inject feed marker immediately after chapter title if missing."""
import re, os

ROOT = os.path.join(os.path.dirname(__file__), "..", "chapters")
MARKERS = re.compile(r"留灯账|馈缘|照路余恩|馈灯|同心灯|盟灯|纳绶|纳府")

ANCHOR = {
    13: "花甲入宗杂役，低谷蓄力；留灯账：*杂役堂，三十人，皆在账上。*",
    28: "天煞门外围夜袭，豪强梯一；因果：赵家→联盟，背叛当场见。",
    33: "全镇神迹，**照路余恩**铺展——记名者命灯各亮一线。",
    43: "程不二坊市，三块灵石规矩；留灯账：*程不二，换路，馈缘↑。*",
    48: "**七品疏脉丹**配续灯诀，灯丹一句标阶。",
    53: "十二杂役入岭，留灯账：*十二命，馈缘↑。*",
    58: "沈青禾抉择自主，馈灯③主动靠近。",
    73: "迟暮之约万灯大会，羁绊↑。",
    78: "化敌为友，霍照临认输前夜。",
    83: "借光挡幡，五灯雏形。",
    88: "冬典授牌，失嗅觉代价。",
    93: "陆承安令，背叛阶梯。",
    98: "一日一年，枯骨岭时相。",
    113: "五灯同心阵名册**纳绶**，馈灯⑤。",
    118: "敛灯崖夜，陆承安名未全。",
    123: "云照传经，师徒传承链。",
    128: "铁柱**万家火**起，馈灯④报恩。",
    133: "诏云黑灯，镇灯司影。",
    138: "敛灯崖拉袖，情感余温。",
    143: "青萝风声，封灯诏至。",
    148: "灯影预演，玄京线。",
    153: "**九品照影符**丁字三号，灯籍标阶。",
    158: "镇灯司招，制度之暗。",
    163: "程不二遗图到手，施恩报恩。",
    168: "旧灯库第一层交锋。",
    173: "谢长缨铁证，落第案。",
    178: "青萝灯会，**八阶灯河**初展。",
    183: "谢长缨危，护制之灯。",
    188: "陆承安动摇，赎罪前夜。",
    193: "非境之灯，天魔阶梯。",
    198: "云照残魂铸架，万古灯架。",
    213: "万年一人，拒升抉择。",
    218: "姜小满第九传人，馈灯⑧传承。",
}

POOL = [
    "他在留灯账记一行：*帮一人，记一笔；账在，恩在。*",
    "守岁灯芯微温，馈缘↑，灯箓古篆闪了一闪。",
    "馈灯链：赠礼已入账，只等后文当场还。",
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
    fixed = 0
    for part in parts[1:]:
        if MARKERS.search(part):
            out.append(part)
            continue
        m = re.match(r"(### 第([^\n]+)\n)", part)
        if not m:
            out.append(part)
            continue
        cn = re.search(r"([一二三四五六七八九十百零]+)章", m.group(2))
        ch = cn_to_int(cn.group(1)) if cn else fixed
        inject = ANCHOR.get(ch) or POOL[ch % len(POOL)]
        out.append(m.group(1) + inject + "\n\n" + part[m.end():])
        fixed += 1
    open(path, "w", encoding="utf-8").write("".join(out))
    print(vol, "fixed", fixed)
