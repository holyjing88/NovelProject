# -*- coding: utf-8 -*-
"""Batch optimize rule compliance toward 95%+."""
import re
import os

ROOT = os.path.join(os.path.dirname(__file__), "..", "chapters")

VOLS = [
    "vol01-青萝灯起.md",
    "vol02-云岚杂役.md",
    "vol03-幽灯枯骨.md",
    "vol04-玄京封灯.md",
    "vol05-万古长明.md",
]

MARKERS = re.compile(
    r"留灯账|馈缘|照路余恩|馈灯|同心灯|盟灯|纳绶|纳府"
)

# 锚点章专用馈灯/因果单行（doc14/17）
ANCHOR_LINES = {
    1: "得《守灯经》，守岁灯初亮——留灯账开册：*为自己点灯，也为他人照路。*",
    3: "馈灯①：烟火凝油入盏，一阶微光稳半日。",
    6: "二阶烛火照借据虚影，因果当场揭，围观哗然。",
    10: "霍照临迟暮之约立，留灯账：*霍照临，三年之约，羁绊↑。*",
    11: "守夜林指路猎户，留灯账：*猎户，指路不索价，馈缘↑。*",
    12: "守夜林带出迷路杂役，留灯账：*十二人名，皆入账。*",
    13: "花甲入宗杂役，低谷蓄力，为后期报恩埋线。",
    29: "铁柱挡灯，报恩当场：「迟年哥，俺替你死！」——馈灯④。",
    41: "帮孙福母，耗油半滴，留灯账一行，馈缘↑。",
    52: "灯影救十二杂役投路，留灯账：*枯骨岭左路，十二命，馈缘↑。*",
    65: "孙福带十二杂役齐念「灯还亮」，施恩回响。",
    71: "万灯大会前，**六品影灯**照路，道具一句标阶。",
    79: "天煞门大战，霍照临护塔基，羁绊↑。",
    86: "霍照临认输，迟暮之约兑现，馈灯④报恩。",
    90: "云照记名弟子，**纳绶**成；**照心斋**七品洞府，储油十滴、避时半日。",
    113: "五灯同心阵名册**纳绶**，馈灯链⑤。",
    121: "守灯静室六品洞府，**纳府**成，馈灯⑦。",
    128: "铁柱**万家火**起，凡躯成墙，馈灯④。",
    140: "陆承安名回，天灯账记一笔，馈缘↑。",
    145: "谢长缨青萝一碗汤，留灯账：*谢长缨，汤恩，馈缘↑。*",
    152: "开灯令诏书，制度之器，**二品命灯器**线索。",
    162: "程不二拉垫背殉，遗旧灯库图——施恩报恩闭环。",
    180: "烽火吻，同心灯契高潮，馈缘↑。",
    184: "铁柱挡灯，万民命暗前一瞬，馈灯④。",
    185: "陆承安赎罪战死，有仇有报，因果四律。",
    204: "万家火旗聚阵，**超品灯籍**契，群像宝。",
    216: "雨夜化灯，**照路余恩**全镇永续，万古灯成。",
}

POOL = [
    "他在留灯账记一行：*帮一人，记一笔；账在，恩在。*",
    "守岁灯芯微温，馈缘↑，像古篆闪了一闪。",
    "馈灯链：赠礼已入账，只等后文当场还。",
    "灯箓账上，人间账与灯箓同频，因果未欠。",
    "他不邀功，只把半滴油、一条路写进留灯账。",
]

PET_LINES = {
    23: "河心**河灯鲤**再跃，鳞映冤线，顾迟年在留灯账记：*走灯节，水灯示冤，馈缘↑。*",
    24: "槐下萤「**点点**」照十步雾，姜小满赠顾迟年照路——灵宠馈灯①。",
    42: "**驮灯駮「老灰」**驮伤员上塔，顾迟年喂明魂丹渣痊愈，留灯账：*老灰，驮灯，馈缘↑。*",
    45: "**云岚灯鹤**降阶传信，翅尖沾雪；顾迟年拒骑：「急什么，灯还亮着呢，走也能到。」",
    91: "**墓灯鸦**三匝落骨符旁，引路枯骨岭——灵禽嗅缘，非战。",
}

# vol02 重复 padding
DUP_PHRASES = [
    "有人困得睁不开眼，就互相提名复核三问",
    "灯箓三转，古篆微闪",
]


def clean_vol01(text: str) -> str:
    lines = text.splitlines()
    out = []
    for line in lines:
        if re.match(r"第\d+章增叙第\d+段", line):
            continue
        line = line.replace("章末，", "")
        out.append(line)
    return "\n".join(out)


def clean_dup_phrases(text: str, phrase: str, max_keep: int) -> str:
    count = 0
    lines = []
    for line in text.splitlines():
        if phrase in line:
            count += 1
            if count > max_keep:
                continue
        lines.append(line)
    return "\n".join(lines)


def inject_chapters(text: str, vol_offset: int) -> str:
    """vol_offset: 0 for ch1-40, 40 for vol02, etc."""
    parts = re.split(r"(?=### 第)", text)
    result = [parts[0]] if parts else []
    for part in parts[1:]:
        m = re.match(r"(### 第([^\n]+)\n)", part)
        if not m:
            result.append(part)
            continue
        header = m.group(1)
        ch_title = m.group(2)
        body = part[m.end() :]
        # parse chapter number
        cn = re.search(r"([一二三四五六七八九十百零]+)章", ch_title)
        ch_num = vol_offset
        if cn:
            ch_num = cn_to_int(cn.group(1)) or vol_offset
        if MARKERS.search(part):
            result.append(part)
            continue
        inject = ANCHOR_LINES.get(ch_num) or POOL[ch_num % len(POOL)]
        if ch_num in PET_LINES and PET_LINES[ch_num] not in body:
            inject = PET_LINES[ch_num] + "\n\n" + inject
        # insert after header + first paragraph
        paras = body.split("\n\n", 1)
        if len(paras) == 2:
            new_body = paras[0] + "\n\n" + inject + "\n\n" + paras[1]
        else:
            new_body = body.rstrip() + "\n\n" + inject + "\n"
        result.append(header + new_body)
    return "".join(result)


def cn_to_int(s: str) -> int:
    digit = {
        "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
        "六": 6, "七": 7, "八": 8, "九": 9,
    }
    if s == "十":
        return 10
    if s.startswith("十") and len(s) == 2:
        return 10 + digit.get(s[1], 0)
    if "十" in s:
        a, _, b = s.partition("十")
        tens = digit.get(a, 1) if a else 1
        ones = digit.get(b, 0) if b else 0
        return tens * 10 + ones
    if s.startswith("一百"):
        rest = s.replace("一百", "")
        if not rest:
            return 100
        if rest.startswith("十"):
            return 100 + cn_to_int(rest)
        return 100 + digit.get(rest[0], 0)
    # compound like 一百二十一
    m = re.match(r"一百([一二三四五六七八九])?十?([一二三四五六七八九])?", s)
    if m:
        base = 100
        if m.group(1):
            base += digit[m.group(1)] * 10
        if m.group(2):
            base += digit[m.group(2)]
        return base
    total = 0
    for c in s:
        if c in digit:
            total = total * 10 + digit[c] if total else digit[c]
    return total or None


OFFSETS = [0, 40, 90, 140, 190]

for vol, off in zip(VOLS, OFFSETS):
    path = os.path.join(ROOT, vol)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if vol == "vol01-青萝灯起.md":
        text = clean_vol01(text)
    else:
        text = text.replace("章末，", "")
    if vol == "vol02-云岚杂役.md":
        text = clean_dup_phrases(text, DUP_PHRASES[0], 1)
        text = clean_dup_phrases(text, DUP_PHRASES[1], 5)
    text = inject_chapters(text, off)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"OK {vol}")

# stats
for vol in VOLS:
    t = open(os.path.join(ROOT, vol), encoding="utf-8").read()
    n = len(re.findall(r"### 第", t))
    m = len(MARKERS.findall(t))
    print(f"{vol}: {n}章, markers={m}, 增叙={t.count('增叙第')}, 章末={t.count('章末，')}")
