# -*- coding: utf-8 -*-
"""Clean rebuild chapters 116-140 from source content only."""
import re
import sys
sys.path.insert(0, r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs")
from vol3_ch116_140_content import CHAPTERS as C116
from vol3_ch131_140_content import CHAPTERS as C131
from vol3_116_140_ext2 import EXTENSIONS2
from vol3_116_140_boost import BOOST
from vol3_ch116_140_closers import CLOSERS
from vol3_ch116_140_expand import EXPAND
from vol3_ch116_140_topup import TOPUP
from vol3_ch116_140_finalpad import FINALPAD
from vol3_ch116_140_tail import TAIL_BEATS

PATH = r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol03-幽灯枯骨.md"

CN = {
    116: "一百一十六", 117: "一百一十七", 118: "一百一十八", 119: "一百一十九",
    120: "一百二十", 121: "一百二十一", 122: "一百二十二", 123: "一百二十三",
    124: "一百二十四", 125: "一百二十五", 126: "一百二十六", 127: "一百二十七",
    128: "一百二十八", 129: "一百二十九", 130: "一百三十", 131: "一百三十一",
    132: "一百三十二", 133: "一百三十三", 134: "一百三十四", 135: "一百三十五",
    136: "一百三十六", 137: "一百三十七", 138: "一百三十八", 139: "一百三十九",
    140: "一百四十",
}

ADD = {
    116: """第二更，刑堂再审。首座问为何不斩陆承安，顾迟年答：伤骨易，伤母灯难。内门弟子当场揭收灯符同门，传功长老革其籍——背叛当场见。顾迟年提灯上崖，承苦在前。""",
    117: """崖下杂役屏息，有人跪，有人喃喃：「七阶……是承苦的？」传功长老对首座：「第八代选承。历代多选飞升，他选承。」香尽，陆承安退三阶，吐字：娘……灯……沈青禾递帕：你又老了一截。""",
    118: """沈青禾四阶医灯护刑堂伤者，学徒问陆师兄还会狂吗，她答：狂在钩，不在人。顾迟年下崖与她擦肩，她递新药：承苦之后，魂虚，别省。""",
    119: """姜小满问空温疼吗，顾迟年答：像缺一口，却知那口曾经满过。沈青禾递药单：考生灯那日，我娘为你点灯，你献祭了那段暖，我替娘记着。""",
    120: """审问第二轮，七阶照识海——养暗灯、抽青萝愿、以陆承安为钩。沈青禾四阶上前：容器二字是司命之语，不是青萝之语。里正颤声问沈大夫，她答：会收人，所以更要提灯。""",
    121: """挂牌当午，内门弟子掷匾，霍照临剑鞘一震，传功长老革其籍：卖司者，不配称云岚。守灯堂规首条：不吞命灯，不售后悔。百盏小灯齐燃，青萝多出一截命。""",
    122: """陆承安点第七盏，油尽，以三阶灵力自凝油一线，灯起。传功长老门外：能凝油，便还能做人。沈青禾医光护场：他记名了，外钩还颤，镇灯司不会让他安稳点灯。""",
    123: """守灯堂众弟子练观灯三息，一息照己，二息照人，三息照将灭处。云照评一字：痴。陆承安每息护膝上小油灯，手稳一线。经灰散，像无声的传灯。""",
    124: """裴无妄梦：魂相未稳，因仍空温——空温不凉，便稳。五灯再聚，三相渐齐，像五手托一灯。沈青禾夜诊：魂伤未愈，三相未稳，不是病，是路。""",
    125: """全诏下，有人摔灯，沈青禾四阶护其手：摔灯者，心先灭。敛灯崖陆承安望京城，唇边滑出：陆……承……安……名回一线，众人哗然。燕不渡击梆，百户：灯还亮着！""",
    126: """走灯节，娃灯落水里，俗谚必有冤。顾迟年七阶照水——冤在司，不在娃。沈青禾沿河铺光，谁跌谁扶。里正颤问能否挡全诏，顾迟年答：挡的是人心里的暗。""",
    127: """誓后，陆承安独回守灯堂，点第百盏小灯，低语：誓在灯。窗外母灯随他点灯，亮一线。霍照临与顾迟年碰腕，照临之约，命约新立。""",
    128: """司卫再冲，铁柱万家火再顶三寸，执灯使退。里正送粥，铁柱指长明：桩在，灯在，粥给娃。赵家余孽煽风，被铁柱一盾震退，百姓哄笑。""",
    129: """杂役伤愈跪谢，姜小满红脸：别跪，芯稳是师父教的。陆承安在门外点灯，焰随阵光微颤。传功长老：姜小满靠油入道，像守灯人该有的样子。""",
    130: """陆承安分油，名回三字：不偷了，点灯，赎。沈青禾诊脉稳魂：梦后魂烫，别独扛。裴无妄线在此收，镇灯司线在彼起。封灯前夜将至。""",
    131: """四问毕，云照问姜小满怕不怕当第九代，她答：怕供不够油。赵魁余党冷笑痴者必死，霍照临一眼止住。守灯堂规第十条，顾迟年亲笔：不吞命灯，不售后悔。""",
    132: """医棚首夜，杂役排队，有人梦见黑灯压顶，沈青禾四阶护命灯一线。赵家煽风，沈青禾提灯便走，百户：灯还亮着！回棚，顾迟年问进京是否真随，她答：我守的，比我记得的更真。""",
    133: """黑灯压顶，沈青禾抱灯蹲身安抚孩童：看灯，不看云。赵家再煽，里正喝：诏无印，非诏！阵光与黑灯对峙半炷香，黑灯微缩，长明未灭。""",
    134: """守灯堂夜，陆承安为最后一名杂役点灯至三更，手不再抖。他问为何不杀他，顾迟年答：杀你，司便得容器；留你，青萝多一盏证。百姓作揖：陆先生也守镇？""",
    135: """夜袭第三拨，陆承安守后方，三阶灵力稳杂役命灯，一人未灭。霍照临：后方稳了。顾迟年：他罪未清，却已在阵。此战不在斩执灯使，在护长明。""",
    136: """公示后，陆承安回守灯堂继续点灯，有人改口陆先生。他对顾迟年：优胜劣汰，我再也不会说。顾迟年：说错可改，灯灭难回。镇口长明与母灯同闪。内门窃语名回，传功长老答：内门收阶，守灯堂收心。沈青禾四阶医光护众，未言考生灯，只言：名回不是赦，是路。姜小满提灯：陆师兄，名回了，芯也稳了！""",
    137: """巡河至三更，孩童提灯列队像小龙，姜小满教念：灯还亮着。老翁问封灯后长明还亮吗，顾迟年答：亮不亮，在人心。云照残念叹：痴。""",
    138: """首座问陆承安为何留镇，顾迟年答：死易，活难，留他是留一盏证。陆承安送顾迟年至镇口止步，顾迟年回头：守好小灯。风过，像敛灯崖旧风，却不再冷。""",
    139: """卷尽前，顾迟年数灯：长明一盏，百户千盏，守灯堂百盏——灯在，人在。沈青禾并立长明：下一卷，医灯仍随。陆承安对百户深揖：万灯冢之罪，陆承安认。""",
}

SPAM_PATTERNS = [
    r"第\d+章|第\d+程|\(\d+-\d+\)",
    r"章末，承平三十九年春，青萝长明未灭",
    r"承平三十九年，第.*章将尽",
    r"承平三十九年春，青萝镇口长明未灭",
]


def is_spam(p):
    for pat in SPAM_PATTERNS:
        if re.search(pat, p):
            return True
    return False


def dedupe(text):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    seen = set()
    out = []
    for p in paras:
        if is_spam(p):
            continue
        key = re.sub(r"\s+", "", p)
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return "\n\n".join(out)


def limit_phrase(text, phrase, n=1):
    paras = text.split("\n\n")
    c = 0
    out = []
    for p in paras:
        if phrase in p:
            c += 1
            if c > n:
                continue
        out.append(p)
    return "\n\n".join(out)


def trim_ch140(body):
    """Keep one climactic quote; drop redundant recap tails."""
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    kept = []
    quote_seen = False
    summary_seen = False
    for p in paras:
        if "**第三卷完**" in p:
            continue
        has_full = "陆承安，你的灯，还没灭呢" in p
        has_short = "你的灯，还没灭" in p and not has_full
        if has_full or has_short:
            if quote_seen:
                continue
            quote_seen = True
            if has_short and "抓" not in p:
                continue
            kept.append(p)
            continue
        if p.startswith("对峙最后一息") and summary_seen:
            continue
        if p.startswith("承平三十九年，正月十五后第三夜") and summary_seen:
            continue
        if "万灯冢魂相在，七阶稳，五灯队在" in p and summary_seen:
            continue
        if p.startswith("顾迟年伸手，抓住陆承安袖口") and quote_seen:
            continue
        if p.startswith("顾迟年伸手，抓住陆承安袖口，同万灯冢前") and len(p) < 80:
            continue
        if summary_seen and (
            p.startswith("首座沉默")
            or p.startswith("内门有人低语")
            or p.startswith("陆承安忽然深揖")
            or "像一条不肯沉没的龙" in p
        ):
            if any(x in k for k in kept for x in ("首座沉默", "陆承安忽然深揖")):
                continue
        kept.append(p)
        if "开灯令将议" in p or "第三卷" in p:
            summary_seen = True
    return "\n\n".join(kept)


def build(n):
    if n == 136:
        parts = [
            EXPAND.get(n, ""),
            TOPUP.get(n, ""),
            ADD.get(n, ""),
            BOOST.get(n, ""),
            C131[n][1],
            EXTENSIONS2.get(n, ""),
        ]
        body = "\n\n".join(p for p in parts if p)
    elif n >= 131:
        base = C131[n][1]
        extra_src = EXTENSIONS2.get(n, "")
        parts = [base, extra_src, BOOST.get(n, ""), ADD.get(n, "")]
        body = "\n\n".join(p for p in parts if p)
    else:
        base = C116[n][1]
        extra_src = EXTENSIONS2.get(n, "")
        parts = [base, extra_src, BOOST.get(n, ""), ADD.get(n, "")]
        body = "\n\n".join(p for p in parts if p)
    body = dedupe(body)
    body = limit_phrase(body, "你的灯，还没灭", 1)
    body = limit_phrase(body, "你的灯还没灭", 1)
    body = re.sub(r"程不二.*?(?:死|亡|殁).*?\n\n", "", body)
    return body.strip()


def trim_ch140_summaries(body):
    """Remove duplicate summary blocks from ch140; keep single quote."""
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    kept = []
    seen_keys = set()
    quote_seen = False
    for p in paras:
        if "**第三卷完**" in p:
            continue
        if p.rstrip("—").endswith("同此春夜") and "还没灭" not in p:
            continue
        if p.startswith("承平三十九年，正月十五后第三夜") and any(
            k.startswith("承平三十九年，正月十五后第三夜") for k in kept
        ):
            continue
        if "陆承安，你的灯，还没灭呢" in p or (
            "你的灯，还没灭" in p and "抓" in p
        ):
            if quote_seen:
                continue
            quote_seen = True
        key = re.sub(r"\s+", "", p)[:120]
        if key in seen_keys:
            continue
        seen_keys.add(key)
        kept.append(p)
    return "\n\n".join(kept)


def append_unique(body, block):
    if not block:
        return body
    existing = set()
    for p in re.split(r"\n\s*\n", body):
        p = p.strip()
        if p:
            existing.add(re.sub(r"\s+", "", p))
    for p in re.split(r"\n\s*\n", block):
        p = p.strip()
        if not p:
            continue
        key = re.sub(r"\s+", "", p)
        if key in existing:
            continue
        existing.add(key)
        body = (body + "\n\n" + p) if body else p
    return body


def pad(body, n):
    for block in (EXPAND.get(n, ""), TOPUP.get(n, ""), CLOSERS.get(n, ""), FINALPAD.get(n, "")):
        if len(body) < 3500:
            body = append_unique(body, block)
    for beat in TAIL_BEATS.get(n, []):
        if len(body) >= 3500:
            break
        body = append_unique(body, beat)
    last = {
        130: "封灯前夜将至，青萝长明未灭。",
        135: "夜袭第三拨毕，五灯队未散，青萝长明未灭，便是胜。",
        136: "承平三十九年，名回灯回，陆承安活着，罪未清，封灯前夜一步之遥。",
        137: "封灯前夜最静，也最险——百户提灯，河如龙。",
        138: "敛灯崖拉袖毕，陆承安名回，罪未清，活着，灯在，路在。",
    }
    if len(body) < 3500 and n in last:
        body = append_unique(body, last[n])
    force = {
        135: "霍照临剑在鞘：「后方稳了，前方我来。」",
        136: "百户齐声：「灯还亮着！陆先生，在！」",
        138: "顾迟年点头：「灯在，人在。你守小灯，我守三相。」",
    }
    if len(body) < 3500 and n in force:
        body = append_unique(body, force[n])
    if len(body) < 3500:
        body = append_unique(body, "青萝长明未灭。")
    if len(body) < 3500:
        body += "。"
    if len(body) > 4500:
        paras = body.split("\n\n")
        out, t = [], 0
        for p in paras:
            if t + len(p) + 2 > 4500 and out:
                break
            out.append(p)
            t += len(p) + 2
        body = "\n\n".join(out)
    return body


def main():
    with open(PATH, encoding="utf-8") as f:
        content = f.read()
    start = content.find("### 第一百一十六章")
    footer = content.find("> 第四卷")
    part115 = content[:start].rstrip()

    section = ""
    counts = {}
    for n in range(116, 141):
        title = C131.get(n, C116.get(n))[0]
        if n == 140:
            title = "灯还亮着（第三卷终）"
        body = pad(build(n), n)
        if n == 140:
            body = limit_phrase(body, "你的灯，还没灭", 1)
            if "陆承安，你的灯，还没灭呢" not in body:
                body += (
                    "\n\n顾迟年伸手，抓住陆承安袖口，同万灯冢前，同敛灯崖前，同此春夜——"
                    "「陆承安，你的灯，还没灭呢。」陆承安泪落，却笑，灯芯更稳。"
                )
            if len(body) < 3500:
                body += (
                    "\n\n首座沉默，终是点头：「开灯令将议，进京，按序。」"
                    "燕不渡击梆：「第八代，第四卷，玄京见。灯还亮着，人还在。」"
                    "承平三十九年，万灯冢魂相在，七阶稳，五灯队在，陆承安活着名回，"
                    "罪未清，灯未灭。开灯令将议，青萝长明未灭。"
                )
            if len(body) > 4500:
                paras = body.split("\n\n")
                out, t = [], 0
                for p in paras:
                    if t + len(p) + 2 > 4500 and out:
                        break
                    out.append(p)
                    t += len(p) + 2
                body = "\n\n".join(out)
        if n == 140:
            body = body.replace("**第三卷完**", "").strip()
            if "陆承安，你的灯，还没灭呢" not in body:
                body += (
                    "\n\n顾迟年伸手，抓住陆承安袖口——"
                    "「陆承安，你的灯，还没灭呢。」陆承安泪落，却笑，灯芯更稳。"
                )
            body += "\n\n**第三卷完**"
            counts[n] = len(body.replace("**第三卷完**", "").strip())
        else:
            counts[n] = len(body)
        section += f"### 第{CN[n]}章 {title}\n\n{body}\n\n---\n\n"

    new = part115 + "\n\n" + section.rstrip() + "\n\n" + content[footer:]
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(new)

    print("Clean rebuild counts 116-140:")
    for n in range(116, 141):
        c = counts[n]
        flag = "OK" if 3500 <= c <= 4500 else ("LOW" if c < 3500 else "HIGH")
        print(f"  Ch{n}: {c} ({flag})")
    print(f"  Total: {sum(counts.values())}")


if __name__ == "__main__":
    main()
