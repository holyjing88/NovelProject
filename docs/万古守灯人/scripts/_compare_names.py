# -*- coding: utf-8 -*-
import os, re
from collections import Counter

ROOTS = {
    "万古守灯人": r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\万古守灯人",
    "还礼仙翁传": r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\还礼仙翁传",
}

# Core entities from setting docs (post-refactor v2)
WSG_CORE = [
    "顾迟年", "沈青禾", "霍照临", "陆承安", "程不二", "姜小满", "铁柱", "温言",
    "谢长缨", "燕不渡", "裴无妄", "云照", "赵元青", "孙福娘", "秦照", "赵魁", "管慎",
    "青萝镇", "云岚宗", "玄京", "幽灯集", "枯骨岭", "镇灯司", "守岁灯", "不二斋",
    "照心斋", "守夜林", "双焰宗", "照途教", "噬命魔宫", "熄灯教", "玄真道门",
    "青莲照心寺", "持明真言坛", "万灯大会", "旧灯库", "守灯经", "续灯诀", "灯箓账",
    "灯符册", "云岚灯鹤", "驮灯駮", "槐下萤", "河灯鲤", "墓灯鸦", "天煞门",
    "照刑司", "敛灯崖", "云岚坊", "盏兽厩", "杂役堂", "执灯堂", "藏经阁",
    "走灯节", "长明灯", "命灯", "灯油", "灯芯", "守夜林外围灯位图",
    "裴无妄", "女相", "太后", "幼帝", "镇国公", "豪强联盟",
]

HL_CORE = [
    "莫长春", "柳青鸢", "苏念慈", "顾小满", "霍镇山", "韩铁山", "沈晚晴", "厉无殇",
    "周德海", "魏无涯", "赵玄机", "萧燃", "清虚子", "不动上师", "慧明禅师", "秦商言",
    "段承焰", "噬宫主吞名", "青岚门", "赤焰谷", "万妖岭", "镇妖司", "百宝阁",
    "九府盟会", "赠缘簿", "青竹杖", "青霜剑", "因果玉佩", "竹灵青焰", "霜雀",
    "灵鹤晚晴", "扫把灵满满", "墨云雕", "药玉兔", "合欢宗", "圣辉教廷", "圣辉教",
    "净慈寺", "真言宗", "落花洲", "玄魔宗", "血魔殿", "夺缘宗", "血莲教",
    "缘箓", "符录", "续命丹", "回春丹", "破境丹", "培元丹", "思过崖", "青岚坊",
    "灵兽栏", "执法堂", "黑风林",
]

def read_all_text(root):
    parts = []
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn.endswith((".md", ".py", ".txt")):
                p = os.path.join(dirpath, fn)
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        parts.append(f.read())
                except Exception:
                    pass
    return "\n".join(parts)

texts = {k: read_all_text(v) for k, v in ROOTS.items()}

print("=== EXACT CORE TERM OVERLAP ===")
for term in WSG_CORE:
    if term in HL_CORE or any(term in t for t in HL_CORE):
        w = texts["万古守灯人"].count(term)
        h = texts["还礼仙翁传"].count(term)
        if w and h:
            print(f"{term!r}: WSG={w}, HL={h}")

print("\n=== HL terms appearing in WSG text ===")
for term in HL_CORE:
    c = texts["万古守灯人"].count(term)
    if c:
        print(f"{term!r}: {c}")

print("\n=== WSG terms appearing in HL text ===")
for term in WSG_CORE:
    c = texts["还礼仙翁传"].count(term)
    if c:
        print(f"{term!r}: {c}")
