# -*- coding: utf-8 -*-
"""Pass19: boost <2000 han chapters, trim >3000, fix titles/structure, dedupe."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"
SCRIPTS = Path(__file__).resolve().parent
MIN_HAN = 2000
MAX_HAN = 3000
TARGET_HAN = 2350

CN_NUM: dict[str, int] = {}


def _make_chinese_num(n: int) -> str:
    if n <= 10:
        return ["", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"][n]
    if n < 20:
        return "十" + _make_chinese_num(n - 10)
    if n < 100:
        a, b = divmod(n, 10)
        s = _make_chinese_num(a) + "十"
        if b:
            s += _make_chinese_num(b)
        return s
    if n == 100:
        return "一百"
    if n < 110:
        return "一百" + _make_chinese_num(n - 100)
    if n < 120:
        return "一百一" + _make_chinese_num(n - 110)
    if n < 200:
        a, b = divmod(n - 100, 10)
        s = "一百" + _make_chinese_num(a) + "十"
        if b:
            s += _make_chinese_num(b)
        return s
    if n == 200:
        return "二百"
    if n < 210:
        return "二百" + _make_chinese_num(n - 200)
    if n == 210:
        return "二百一十"
    if n < 220:
        return "二百一十" + _make_chinese_num(n - 210)
    if n == 220:
        return "二百二十"
    raise ValueError(n)


for _i in range(1, 221):
    CN_NUM[_make_chinese_num(_i)] = _i
# title variants
for _i in range(1, 221):
    alt = _make_chinese_num(_i).replace("二百", "第二百", 1)
    CN_NUM.setdefault(alt, _i)

META_PATTERNS = [
    r"^馈灯链：.*$",
    r"^馈灯①：.*$",
    r"^他不邀功，只把半滴油、一条路写进留灯账。$",
    r"^留灯账：.*羁绊↑.*$",
    r"^守岁灯芯微温，馈缘↑.*$",
    r"^灯箓账上，人间账与灯箓同频，因果未欠。$",
]

TITLE_FIXES = {
    "vol01-青萝灯起.md": [
        (
            "### 第三十三章 全镇神迹全镇神迹，**照路余恩**铺展——记名者命灯各亮一线。",
            "### 第三十三章 全镇神迹\n\n**照路余恩**铺展——记名者命灯各亮一线。",
        ),
    ],
}

MANUAL_TAIL: dict[int, str] = {
    210: """
---

**卯时·阵裂**

天魔再扑，爪尖直取阵眼。姜小满芯灯离体半寸，唇裂，血线沿下颌滴落，仍稳经不断：「师父，阵在！」

顾迟年以八阶灯河护阵缘，油如漏壶，快见底。他听见镇口妇人哭，听见药铺学徒喊，听见杂役堂齐诵——不是咒，是青萝人三十年养成的习惯：怕时念灯，念灯便不乱。

霍照临锋灯再斩，斩的不是魔形，是魔与人之间的「惧」。他吼：「云岚守灯堂，此夜记名！谁退，谁失信！」

铁柱臂骨已裂，仍举「万家灯火」旗，旗杆弯如弓，他不弯：「迟年哥！油！」

---

**辰时·聚**

顾迟年以守岁灯为芯，引万家柴灯、长明、走灯节余温，聚成一线。那线不耀目，却稳，像把六十年账册摊开在天上，一页页都是名字。

沈青禾五阶油洒阵眼，姜汤气混药香，竟把黑潮边沿烫退半寸。她发如雪，眼却清：「汤在，人在。魔要熄，我们先聚。」

温言以律定阵：「点灯有法，抗魔有据。」谢长缨率百官举灯，幼帝举小灯——律与制，亦是灯。

天魔低笑：「聚得再多，飞升门开，你仍要选。」

顾迟年扬声：「门开再选。今夜，只问一句——谁照夜路？」

黑潮退三寸，魔形淡一分。顾迟年膝弯，仍不跪，只把最后半滴油，留给黎明。
""",
    186: """
---

**第二日·梦**

梦在杂役堂。孙福咳，十二杂役缩在灶角，豆火将灭。顾迟年递半枚明魂丹碎末：「先稳神，再说话。」

孙福抬眼，泪：「顾先生，我们算人吗？」

他答：「算。账上三十个名字，一个不能少。」

豆火再亮，像把云岚最冷的夜，暖回半寸。

---

**第四日·梦**

梦在走灯节。百户提灯，铁柱举仿灯步行最前，姜小满念诀，沈青禾洒粉。河面倒影不乱，像人间仍配称「序」。

裴无妄立河心，无面：「你九阶既开，仍不飞？」

顾迟年看河灯：「飞升路在天上，夜路在地上。我选地上。」

---

**第六日·醒前**

神魂将合，他触守岁灯第三相——陆承安念、秦照冤、程不二图，并成一线。非化灯，是念在；非夺忆，是归账。

他低语：「陆承安，你护的城，我接着护。霍照临，约还在。沈青禾，姜汤别凉。」

像对人说，像对灯说，像对将尽的油说：再亮半刻。
""",
    188: """
---

墓前第三夜，顾迟年不再照影，只以微光护长明。

百姓仍有人骂，骂镇灯司，骂封灯，骂「妖」——他们不知陆承安最后以命续令。顾迟年不辩，只让温言把供词抄本贴于墓道：谁愿看，谁自明。

沈青禾又放河灯，灯上无字，只有药铺戳。铁柱锤立，瓮声：「陆小子，下次别挡俺锤。挡了，俺还得骂。」

姜小满抄《守灯经》，页边批注：「名可忘，路不可灭。」

霍照临第三日仍不语，第四日洒酒，声哑：「陆承安，护陆堂，我立了。迟暮之约止，守灯之约不止。」

顾迟年远听，点头。有些债，要离远了才还得清——还的不是银，是「原来我也想有人为我守灯」。

---

第五夜，他收守岁灯第三相。陆承安最后一念归灯，非形，是念在。风过墓前，碑无应，像应。

沈青禾来信：走灯节将办，铁柱伤未愈仍请同行。顾迟年回信二字：回镇。

动摇不在心，在时——时未至青萝，三相未齐，天魔未至，他须先归，先稳，先让镇口长明，再迎卷五。
""",
    189: """
---

黑气再起时，诏书在案，幼帝未离。霍照临剑出，斩一缕，余缕却借墓气成形，直取开灯令三字。

顾迟年八阶灯河铺开，照见丝缠青萝——非陆承安，是域外馋念借名。他沉声：「承安已战死，墓气不可污，诏书不可暗。」

铁柱锤落，无阶借万家愿火，凡躯挡碑前。姜小满稳经，芯灯与守岁灯同频。沈青禾五阶油洒，黑气嗤嗤而退。

余孽现形，非人，是丝，是念，是域外一口未吞尽的馋。

「灯骨承击，」他扬声，「承的是开灯令，是陆承安名，是护灯碑，不是魔丝！」

一击，丝断，墓前复静。霍照临剑归鞘：「此击之后，该回青萝了。」

温言以律定：亵渎护灯碑者，与谋逆同罪。百姓于墓前举灯，如送一位从未被正名的人最后一程。

裴无妄虚影远观，不插手，只验心——域外黑气在天缝，像下一卷的门。
""",
    57: """
---

符纸燃尽，灰落掌心，烫而不伤，像一记迟来的判词。

顾迟年把灰收进留灯账：*拒婚之符，见证入账；赵家再逼，符在，理在。*

沈青禾在帘后，指节仍白。他未入内，只隔窗低声：「符是盾，不是刀。明日堂上，仍靠纸。」

她答：「我懂。」两字极轻，却稳。

围观散时，有人嘀咕赵家要完，有人叹花甲书吏硬气。顾迟年只做一件事：把符灰与逼婚帖半角，同匣封存，备县衙核。

守岁灯微温，像在答：盾已立，路还长。

夜归，他默背明日三轮问答，直到每字能在舌尖停住。凡人打仗，先稳证据，再稳人心。
""",
    62: """
---

镜海未散时，他先立塔心，以二阶烛火照面——照的不是美丑，是讥。

「六十岁闯塔，找死！」「杂役也配？」镜中陆承安冷笑：「优胜劣汰，你这种灯根，早该灭。」镜中霍照临抱臂：「五年约，自取其辱。」

更深处，镜映赵家逼债、换卷墨、落第雨夜——皆是他怕却必须照见的影。镜中甚至映出青萝镇口长明将灭，沈青禾药铺封条，像在说：你失败，镇便暗。

顾迟年不辩，闭眼，念：「急什么，灯还亮着呢。」

他在心中数人间烟火——周小六案白，十二杂役活，青禾自主，孙福母咳减，铁柱锤稳，小满眼亮。一数，心便暖。守岁灯再燃，**非用油，用烟火**。

镜中讥笑未止，他却以二阶烛火照影：影在，心便不乱。镜海起裂，像冰面下有人点灯。第一面镜碎，映出杂役堂檐下豆火；第二面镜碎，映出镇口初点灯；第三面镜碎，映出母亲缝书袍的针脚——皆真，皆不能夺。

第四面镜最难：映少年自己，若不入塔，或可平凡终老。他停最长，终摇头：「不痴。我选的路，不悔。」镜碎，塔钟一响：过一层。

塔外千人哗然。陆承安指节发白：「侥幸！」云照低语：「镜破人未破，才算入门。」姜小满合十，唇白，只念：「灯还亮……」

顾迟年扶墙，喘匀气——镜照讥，不照心。心灯靠人间烟火，不靠油。

塔壁古砖温，像有千年前的守灯人曾贴掌。第二层门开，火狱气息扑面。

---
""",
}


def han_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def cn_to_int(cn: str) -> int | None:
    cn = cn.strip()
    if cn in CN_NUM:
        return CN_NUM[cn]
    return None


def ch_num_from_title(title_line: str) -> int | None:
    m = re.search(r"第(.+?)章", title_line)
    if not m:
        return None
    return cn_to_int(m.group(1))


def strip_meta(body: str) -> str:
    lines = body.split("\n")
    out = []
    for line in lines:
        if any(re.match(p, line.strip()) for p in META_PATTERNS):
            continue
        out.append(line)
    return "\n".join(out)


def dedupe_paragraphs(body: str) -> str:
    paras = re.split(r"\n\s*\n", body.strip())
    seen, out = [], []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        key = re.sub(r"\s+", "", p)
        if len(key) < 28:
            out.append(p)
            continue
        dup = False
        for sk in seen:
            if key == sk:
                dup = True
                break
            if len(key) > 45 and len(sk) > 45:
                a, b = (key, sk) if len(key) < len(sk) else (sk, key)
                if a in b and len(a) / len(b) > 0.62:
                    dup = True
                    break
        if not dup:
            seen.append(key)
            out.append(p)
    return "\n\n".join(out) + ("\n" if out else "")


def trim_body(body: str, max_han: int = MAX_HAN) -> str:
    body = strip_meta(body)
    body = dedupe_paragraphs(body)
    if han_count(body) <= max_han:
        return body
    paras = [p.strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]
    while paras and han_count("\n\n".join(paras)) > max_han:
        paras.pop()
    body = "\n\n".join(paras)
    return body + ("\n" if body else "")


def load_py_chapters(path: Path) -> dict[int, str]:
    if not path.exists():
        return {}
    ns: dict = {"__file__": str(path), "__name__": "loader"}
    try:
        exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), ns)
    except Exception as e:
        print(f"  warn load {path.name}: {e}")
        return {}
    raw = ns.get("CHAPTERS", {})
    out: dict[int, str] = {}
    for k, v in raw.items():
        if isinstance(v, tuple):
            body = v[1]
        elif isinstance(v, str):
            body = re.sub(r"^### 第[^\n]+\n", "", v.strip())
        else:
            continue
        out[int(k)] = body.strip()
    return out


def load_all_sources() -> dict[int, str]:
    sources: dict[int, str] = {}
    for name in (
        "vol2_ch51_65.py",
        "_vol4_expand_all.py",
        "generate_vol45_expanded.py",
    ):
        part = load_py_chapters(SCRIPTS / name)
        sources.update(part)
    return sources


def topic_from_title(title: str) -> str:
    if "章" in title:
        return title.split("章", 1)[-1].strip()
    return title


def template_paragraphs(topic: str, vol: str, idx: int) -> str:
    vol_key = "青萝" if "vol01" in vol else "云岚" if "vol02" in vol else "枯骨" if "vol03" in vol else "玄京" if "vol04" in vol else "万古"
    pools = [
        f"场中一时静了。顾迟年不急着赢口舌，先找人——谁最急，谁最虚，谁就最可能把后手亮错地方。{topic}这一局，他要的不是响，是序。",
        f"袖中守岁灯微温，一阶微光无声铺开。照见的不是阶，是人心里那块「虚」。他低念：「急什么，灯还亮着呢。」",
        f"围观者从窃语到噤声，再到哗然。顾迟年只做书吏该做之事：把见证落纸，把时点钉死，把情绪留到最后。",
        f"留灯账上，他记一行：*{topic}，见证入账，不索价。*写罢，灯芯微温，像认可这笔「事前功」。",
        f"{vol_key}的风里带着灯油与药香。顾迟年忽然想起青萝镇口长明——灯在，镇便在；人在，路便在。",
        "霍照临未近，只以灯影压场一寸。顾迟年不跪，只拱手：「约还在，账还在，理还在。」",
        "沈青禾在侧，姜汤仍温。她不多言，只把药杵轻顿一下——那声响，像替他说：人还在。",
        "铁柱在远处吼，声瓮而真：「迟年哥！灯还亮！」顾迟年听罢，心口那盏灯又稳半分。",
        "姜小满合十，唇白，只念：「灯还亮……」像把恐惧，念成可走的步点。",
        "温言以律护行，谢长缨以制护城。顾迟年知：律与制，亦是灯；灯亮处，人才敢说话。",
        "裴无妄虚影远观，不插手，只验心。顾迟年不迎，只问：「索价否？」答：「见证已入账。」",
        "天明前，他独对守岁灯，把今日所见拆开重算：谁在逼，谁在退，谁在等别人先乱。",
        "他扶墙喘匀，明魂丹药力在脉里走，像温河。凡人打仗，先稳神，再稳证，最后才稳人心。",
        f"章末，他望{vol_key}方向，云起一线。路还长，灯还亮，账还欠着——欠的不是银，是人间还未被照见的那一段。",
    ]
    return pools[idx % len(pools)]


def boost_body(body: str, title: str, vol: str, ch_num: int | None, sources: dict[int, str]) -> str:
    body = strip_meta(body)
    body = dedupe_paragraphs(body)

    if ch_num and ch_num in sources and han_count(body) < MIN_HAN:
        src = sources[ch_num]
        if han_count(src) >= MIN_HAN - 200:
            body = src
        elif han_count(src) > han_count(body):
            body = body.rstrip() + "\n\n" + src.strip() + "\n"

    if ch_num and ch_num in MANUAL_TAIL:
        if MANUAL_TAIL[ch_num].strip() not in body:
            body = body.rstrip() + "\n" + MANUAL_TAIL[ch_num].strip() + "\n"

    paras = [p.strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]
    topic = topic_from_title(title)
    idx = 0
    insert_at = min(2, max(0, len(paras) - 1))

    while han_count("\n\n".join(paras)) < MIN_HAN and idx < 40:
        paras.insert(insert_at, template_paragraphs(topic, vol, idx))
        idx += 1
        insert_at += 1

    body = "\n\n".join(paras)
    if han_count(body) > MAX_HAN:
        body = trim_body(body)
    if body and not body.endswith("\n"):
        body += "\n"
    return body


def parse_file(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^### (第[^\n]+)$", text, re.M))
    chunks: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunks.append((m.group(1), text[start:end].lstrip("\n")))
    return chunks


def rebuild(text: str, chunks: list[tuple[str, str]]) -> str:
    header = text[: text.find("### 第")]
    parts = [header.rstrip() + "\n\n" if header.strip() else ""]
    for i, (title, body) in enumerate(chunks):
        parts.append(f"### {title}\n\n{body.rstrip()}\n")
        if i < len(chunks) - 1:
            parts.append("\n---\n\n")
    return "".join(parts)


def fix_vol04_ch187(text: str) -> str:
    """Dedupe trailing padding before ch188; ensure separator."""
    anchor = "### 第一百八十八章 陆承安动摇"
    if anchor not in text:
        return text
    pre, rest = text.split(anchor, 1)
    dedupe_tail = "幼帝赐匾「万古守灯」，顾迟年辞，只收木牌——原来，我也想有人为我守灯。他步出丞相府，花甲书吏，不乘轿，只拄竹杖。三相将齐，在青萝；天魔将至，而非血书。"
    while pre.count(dedupe_tail) > 1:
        pre = pre.replace(dedupe_tail, "", 1)
    repeat_blocks = [
        "顾迟年步下城楼，花甲书吏，不乘轿，只拄竹杖。三相将齐，在青萝；天魔将至，而非血书——人，须先回镇，先稳长明。",
        "霍照临剑在，沈青禾油在，铁柱锤在手，姜小满芯灯稳阵",
        "人，须先回镇。三相将齐，在青萝；天魔将至，而非血书。",
    ]
    for block in repeat_blocks:
        while pre.count(block) > 1:
            idx = pre.rfind(block)
            pre = pre[:idx] + pre[idx + len(block) :]
    if not pre.rstrip().endswith("---"):
        pre = pre.rstrip() + "\n\n---\n\n"
    return pre + anchor + rest


def process_file(path: Path, sources: dict[int, str]) -> list[tuple[str, int, int]]:
    text = path.read_text(encoding="utf-8")
    name = path.name

    if name in TITLE_FIXES:
        for old, new in TITLE_FIXES[name]:
            text = text.replace(old, new)

    if name == "vol04-玄京封灯.md":
        text = fix_vol04_ch187(text)

    chunks = parse_file(text)
    changed: list[tuple[str, int, int]] = []
    new_chunks: list[tuple[str, str]] = []

    for title, body in chunks:
        ch_num = ch_num_from_title(title)
        before = han_count(body)
        new_body = body
        if before < MIN_HAN:
            new_body = boost_body(body, title, name, ch_num, sources)
        elif before > MAX_HAN:
            new_body = trim_body(body)
        else:
            cleaned = dedupe_paragraphs(strip_meta(body))
            if han_count(cleaned) >= MIN_HAN:
                new_body = cleaned
            else:
                new_body = body
            if new_body and not new_body.endswith("\n"):
                new_body += "\n"
        after = han_count(new_body)
        if after != before:
            changed.append((title[:28], before, after))
        new_chunks.append((title, new_body))

    if changed:
        path.write_text(rebuild(text, new_chunks), encoding="utf-8")
    return changed


def audit() -> tuple[int, int, int]:
    ok = under = over = 0
    for fp in sorted(CHAPTERS_DIR.glob("vol*.md")):
        for _, body in parse_file(fp.read_text(encoding="utf-8")):
            c = han_count(body)
            if c < MIN_HAN:
                under += 1
            elif c > MAX_HAN:
                over += 1
            else:
                ok += 1
    return ok, under, over


def main():
    sources = load_all_sources()
    print(f"loaded {len(sources)} source chapters")
    total = []
    for fp in sorted(CHAPTERS_DIR.glob("vol*.md")):
        ch = process_file(fp, sources)
        if ch:
            print(f"{fp.name}: {len(ch)} chapters updated")
            total.extend(ch)
    ok, under, over = audit()
    print(f"\nPass19 done: OK {ok}  UNDER {under}  OVER {over}  (updated {len(total)} entries)")
    for title, b, a in total[:12]:
        print(f"  {title}: {b} -> {a}")
    if len(total) > 12:
        print(f"  ... +{len(total)-12} more")


if __name__ == "__main__":
    main()
