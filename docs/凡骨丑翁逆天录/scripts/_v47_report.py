# -*- coding: utf-8 -*-
"""v47 目标章字数+摘要报告"""
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz

TARGET = {2} | set(range(4, 31)) - {18, 24}
PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
SUMMARY = {
    2: "瓮眠·老蛇藤十六文·丑时坛沿水汽",
    4: "赵绣春脏水·童谣卡壳·坛应恩辱分列",
    5: "谣起·井台回嘴·叶送姜·秤声压赵",
    6: "稀粥·赖扒皮爪牙骂走·暗护芽儿",
    7: "陈姑棉袄·冬前井台让人半步",
    8: "馒头四形齐·卖筐十二文·张麻婆护",
    9: "克扣告示·税吏少收三文·醉鬼退半步",
    10: "绝户在册·筐在手·坛应还",
    11: "牵连叶家危·井台替活路·秤在铺不关",
    12: "露凶短签连坐·张麻婆双馒·攒十文",
    13: "狼口戳狼退·张麻婆扎臂·拖伤回",
    14: "村议·韩泥立起认恩·辱叶怒值满",
    15: "村议定公审·坛符影一闪",
    16: "跟风辱二·醉鬼推不动·秤声压风",
    17: "芽儿送药·药叶记心·公审将至",
    19: "旱谣起·井台压赵·姜苗点头",
    20: "采药榜末名·集尾九文·张麻婆骂扒皮",
    21: "新谣出街·叶塞别念·野果",
    22: "独白先还叶·心记叶汤加深",
    23: "审前备心·沈芽怯送药·明日公审钩",
    25: "公审余波·叶家松气·村让半步",
    26: "血祠旱灾谣·邪教伏笔",
    27: "伤复臂肿消·赵退半步·荐帖风声钩",
    28: "老耿赠经片·密宗线起",
    29: "沉丹宗荐帖·心动不乱·宗门篇开",
    30: "叶振东暗送草药·辞村六笔恩上路",
}

def dup(t):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]
    if not s: return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen: d += 1
        seen.add(k)
    return d / len(s)

for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", p).group(1))
    if n not in TARGET: continue
    raw = open(p, encoding="utf-8").read()
    b, footer = extract_body_and_footer(raw)
    h, d = hz(b), dup(b)
    en = len(re.findall(r"韩泥[「\"]?嗯", b))
    st = "**状态**" in b
    v47 = "v47爆款10" in raw
    flag = "OK" if 1670 <= h <= 2500 and d < 0.02 and en <= 1 and not st and v47 else "WARN"
    print(f"ch{n:03d} {h} dup={d:.3f} en={en} {flag} | {SUMMARY[n]}")
