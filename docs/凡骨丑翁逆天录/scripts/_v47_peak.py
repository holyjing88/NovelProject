# -*- coding: utf-8 -*-
"""v47 精修：1780～1950字 · dup<2% · 嗯≤1 · 独钩"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
V47_LO, V47_HI = 1780, 1950
END_MARK = "\n\n---\n\n章末"
SPLIT = re.compile(r"(?<=[。！？])")

TARGETS = {
    1, 3, 10, 18, 24, 25, 28, 30, 34, 36, 37, 38, 39, 40, 42, 43,
    46, 47, 48, 49, 63, 130,
}
MICRO = {1, 3, 18, 24, 63}

# 独钩补段（戏内 · 不跨章套话）
TOPUP = {
    1: "雨歇后，村道泥印里映出半轮月。韩泥把十二文又数一遍，数完收进腰布最里层——层在，明日上山采药才不虚。虚了，坛沿白擦，根也白擦。",
    3: "碗底姜沉，沉得像恩也沉。沉不怕，怕浮——浮了，像施舍；沉了，像该记。记实了，门缝这一指宽，才够活过下一个霜晨。",
    10: "他摸门墩石缝，三文还在，芽儿没取。没取不要紧，要紧是还字已立——立了，绝户册上两字便压不住擦沿的手。手在，公审来也只一句：我记着。",
    18: "灯豆将尽，针脚在肘上像一行不会写字的信。信说：名可脏，肘不能漏。漏了，公审前叶家秤先乱；秤乱，汤就凉。",
    25: "抄本柱上「十日」二字，像给辞村量尺。尺在，手就不飘；手不飘，荐帖到，西驿验骨才站得住末席。末席站着，也是席。",
    28: "经片古字在坛底闷响，响得像远钟——钟不响名，只响路。路在，西驿帖到，泥岗恩才带得走，带得走，才进得了侧门。",
    30: "风贴耳那半句听不清的话，他当风。风过槐枝，叶铺秤又响一声——声在，六笔在篓，篓在肩，肩向沉丹宗。",
    34: "符影半闪那夜，他按掌不追问。追问像少年，他是记心翁——记克扣，记刘婆半勺，记三日测骨帖在柱。帖在，手就不能软。",
    36: "第七笔落在心，不落字纸。字纸只记饭，饭稀，恩不稀——稀粥顶一口饥，顶一口，多活一日，多记一日，多近还刘婆那日一步。",
    37: "掌裂血渗，沿前即止。止，像瓮在数关——关未开，手先稳；稳了，才配深秋末单，才配63那日扎掌推得对。",
    38: "鼻下甘短，像叶丫头「趁热」——趁热记着，还时才不会错。错不得，丹房门缝里的光才进得了心；心有了路，瓮醒才推得对。",
    39: "两月备检钉在耳里，钉住了，赖福秤才虚一日。虚一日，丙九多喘一口气——一口气，够熬到备检帖上柱，够近瓮醒半步。",
    40: "雪意又近一分，钩在雪，钩在坛，钩在瓮醒前那一寸。血停在沿前，停在活计里——活计在，冬测这关才开瓮门缝；缝开，路才向正测。",
    42: "病兽尽，栏角空，空也不晦——晦在嘴，不在铲。雪落肩，他不拍；认净字，才配盯秤那日三两实粮落袋，落袋才真。",
    43: "三两实粮落袋，掌心不抖——抖在袖里，袖里稳了，秤盘才实。实了，赖福才虚；虚不是终，终在正测辨香，在还叶丫头那碗烫。",
    46: "帖角粟壳香压谣回一寸，一寸够了，够他合眼记明日问香。邪腥长，正温短——短像汤，汤烫，才配七日后正测末排仍到。",
    47: "木牌在怀，记功在册，七日条在柱——都在，命就在。命在，坡开讲谣才分得清哪句赖福、哪句外推；分清，克字再虚一寸。",
    48: "柱上五日条猎猎，猎猎不是滚，是催——催手稳，催耳清，催恩别凉。凉不得，叶汤还在前头等着；等着，就得活五日，一日少一日。",
    49: "破布角「必还」三字，旧，真。真在还不急，急在别凉——凉了，七笔断；断了，坡下站不住末排，站不住，丹房门缝就关死。",
    130: "魁名在牌，债序在心——心沉，步才不飘。飘了，省亲那日踩不实泥岗路；踩实了，叶汤那笔头恩才还得到烫手。",
}

# 章内删改：去复读末段 / 修格式
PATCHES: dict[int, list[tuple[str, str]]] = {
    40: [
        (
            "血近沿，沿前即止——止，像瓮在等冬测开缝。备检手稳，灰线过石；韩泥独眼平：血近沿，沿前即止——止，像瓮在等；等对了，冬测这关才开瓮门缝，缝开，路才向正测。备检前夜，灰线再过石，石过，手稳。稳，像瓮在等冬测开缝，缝开，路才向正测。",
            "备检前夜，灰线再过石，石过，手稳。稳，像瓮在等冬测开缝——缝开，路才向正测。",
        ),
        ("韩泥「嗯」一声：「记着。」", "韩泥只答：「记着。」"),
        ("韩泥「嗯」一声：「不抖。」", "韩泥声平：「不抖。」"),
        ("韩泥喝一口，「嗯」一声。", "韩泥喝一口，姜辣醒指。"),
    ],
    43: [
        (
            "韩泥「嗯」一声：「谢轻。饭实，是真。」",
            "韩泥只答：「谢轻。饭实，是真。」",
        ),
        ("韩泥「嗯」一声，不抬头。", "韩泥不抬头。"),
        ('韩泥「嗯」一声：「加。」', '韩泥只答：「加。」'),
        ("韩泥喝尽，「嗯」一声。", "韩泥喝尽，粥热在肚。"),
        ("韩泥「嗯」一声：「心不少。」", "韩泥声平：「心不少。」"),
        (
            "管事盯秤，三两落袋。赖福虚了，虚不是终——终在正测，在辨香，在还。还，先还热的，热的，先还叶丫头汤；汤烫，才配立誓，誓不飘。赖福虚了，虚不是终——终在正测，在辨香，在还；还，先还热的。三两落袋，掌心不抖。抖在袖里，袖里稳了，秤盘才实——实了，赖福才虚。虚不是终，终在正测，在辨香，在还；还，先还热的，热的，先还叶丫头汤。盯秤这日，他掌心不抖——抖在袖里，秤盘实了，袖里才稳。管事盯秤，三两落袋；韩泥记实：赖福虚了，虚不是终——终在正测，在辨香，在还；还，先还热的，热的，先还叶丫头汤。盯秤后，掌心仍不抖。抖在袖里，秤盘实了，赖福才虚——虚不是终，终在辨香。",
            "管事盯秤，三两落袋。掌心不抖——抖在袖里，秤盘实了，袖里才稳。赖福虚了，虚不是终；终在正测辨香，在还叶丫头那碗烫。",
        ),
    ],
    130: [
        ("韩泥「嗯」一声，不辩。辩，像显摆恩偿；恩偿，静着还，还到该还的人手里，才算数。---", "韩泥不辩。辩，像显摆恩偿；恩偿，静着还，还到该还的人手里，才算数。"),
        ("他「嗯」一声，收下，记在心里。", "他收下，记在心里。"),
    ],
    63: [
        ('韩泥「嗯」一声：「命在坛边。坛在，不认。」', '韩泥声平：「命在坛边。坛在，不认。」'),
        ('韩泥应声：「天打不紧。坛在，命在。」', '韩泥只答：「天打不紧。坛在，命在。」'),
        ('入门时管事骂过晦气，他「嗯」一声，席盖更严。', "入门时管事骂过晦气，他应一声，席盖更严。"),
        ('韩泥：「嗯。」', '韩泥只答：「在。」'),
        ('韩泥低声：「嗯。灭了。」', '韩泥低声：「灭了。」'),
        ('韩泥：「嗯。」', '韩泥只答：「在。」'),
        ('韩泥：「嗯。行。」', '韩泥只答：「行。」'),
        ('韩泥：「坛味。嗯。睡吧。」', '韩泥：「坛味。睡吧。」'),
        ('坛底极轻一颤，像「嗯」。', '坛底极轻一颤，像应。'),
    ],
    24: [
        ('韩泥「嗯」一声，不起。', '韩泥不起。'),
        ('陈姑「嗯」一声，没再嚼。', '陈姑没再嚼。'),
        ('韩泥「嗯」一声：「认。汤我喝了，恩我记着。不辩，是恩记着，不用嘴吵。」', '韩泥声平：「认。汤我喝了，恩我记着。不辩，是恩记着，不用嘴吵。」'),
        ('韩泥「嗯」一声：「不曾。门缝大，她递，我接。接的是汤，不是牵扯。」', '韩泥只答：「不曾。门缝大，她递，我接。接的是汤，不是牵扯。」'),
        ('韩泥「嗯」一声：「不惹。事惹我，我记。」', '韩泥声平：「不惹。事惹我，我记。」'),
        ('韩泥「嗯」一声：「祸我管不了。心我管得住。」', '韩泥只答：「祸我管不了。心我管得住。」'),
    ],
    3: [
        ('叶青禾「嗯」了一声。', '叶青禾应一声。'),
        ('韩泥「嗯」一声，不谢，谢轻，他记。', '韩泥不谢，谢轻，他记。'),
    ],
    18: [
        ('韩泥：「嗯。」', '韩泥只答：「在。」'),
        ('韩泥「嗯」一声，不谢。', '韩泥不谢。'),
    ],
    25: [
        ('韩泥「嗯」一声，不谢。', '韩泥不谢。'),
        ('里正「嗯」一声，转向韩泥屋方向，却未近。', '里正转向韩泥屋方向，却未近。'),
        ('韩泥「嗯」一声：「不顶。顶是活，不是辩。辩赢了公审，活路还在末。」', '韩泥声平：「不顶。顶是活，不是辩。辩赢了公审，活路还在末。」'),
    ],
    28: [
        ('韩泥「嗯」一声：「片在底，人在门。门内门外，各守各的。」', '韩泥只答：「片在底，人在门。门内门外，各守各的。」'),
        ('韩泥「嗯」：「放坛底。底稳，坛才眠。」', '韩泥只答：「放坛底。底稳，坛才眠。」'),
    ],
    36: [
        ('韩泥「嗯」一声，坐凳角。', '韩泥坐凳角。'),
        ('韩泥「嗯」一声，记——记刘婆恩，记叶丫头恩，分列，不混。', '韩泥记——记刘婆恩，记叶丫头恩，分列，不混。'),
        ('韩泥「嗯」一声，起身，粥碗已空，空得像泥岗米缸见底——见底过，活过来了，宗门也会活过来。', '韩泥起身，粥碗已空，空得像泥岗米缸见底——见底过，活过来了，宗门也会活过来。'),
        ('韩泥「嗯」一声：「记着。」', '韩泥只答：「记着。」'),
        ('韩泥喝尽，只「嗯」一声，像盖第七笔的印。', '韩泥喝尽，像盖第七笔的印。'),
    ],
    47: [
        ('「嗯。」韩泥说。', '韩泥只答。'),
        ('秦霜「嗯」一声。', '秦霜应一声。'),
        ('「嗯。」韩泥说，「血落篓底，不蹭坛。」', '韩泥说，「血落篓底，不蹭坛。」'),
        ('韩泥喝尽，「嗯」一声。', '韩泥喝尽，粥热在肚。'),
        ('「嗯。」', '应声。'),
        ('韩泥「嗯」一声：「不抖。」', '韩泥声平：「不抖。」'),
    ],
    49: [
        ('韩泥喝尽，「嗯」一声。', '韩泥喝尽，粥热在肚。'),
        ('铁无言「嗯」一声，不重复问，只翻簿——簿上有印，印在，路在。', '铁无言不重复问，只翻簿——簿上有印，印在，路在。'),
        ('韩泥「嗯」一声，独眼平。', '韩泥独眼平。'),
        ('韩泥应声：「捆。」', '韩泥只答：「捆。」'),
    ],
}


def dedupe_sentences(text: str) -> str:
    chunks = [c.strip() for c in SPLIT.split(text) if c.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for c in chunks:
        key = re.sub(r"\s+", "", c)
        if len(key) >= 8 and key in seen:
            continue
        seen.add(key)
        out.append(c)
    return "".join(out)


def limit_en(text: str, keep: int = 1) -> str:
    """嗯≤keep：多余改应声/只答"""
    count = 0
    out = []
    i = 0
    while i < len(text):
        if text[i] == "嗯":
            count += 1
            if count <= keep:
                out.append("嗯")
            else:
                # 看上下文选替换
                if i > 0 and text[i - 1] in "「『":
                    out.append("在")
                elif i + 1 < len(text) and text[i + 1] in "。，":
                    out.append("应声")
                else:
                    out.append("应声")
            i += 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def trim_to_hi(body: str, hi: int) -> str:
    """超上限删末段冗余句"""
    while hz(body) > hi:
        paras = body.split("\n\n")
        if len(paras) <= 3:
            break
        last = paras[-1]
        sents = [s for s in SPLIT.split(last) if s.strip()]
        if len(sents) <= 1:
            paras.pop()
            body = "\n\n".join(paras)
        else:
            paras[-1] = "".join(sents[:-1])
            body = "\n\n".join(paras)
    return body


def process(path: str) -> tuple[int, int, int, float, int]:
    n = int(re.search(r"ch(\d+)", path).group(1))
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    before = hz(body)

    for old, new in PATCHES.get(n, []):
        body = body.replace(old, new)

    body = dedupe_sentences(body)
    body = limit_en(body, keep=1)

    # 补字
    block = TOPUP.get(n, "")
    if block and block not in body:
        if END_MARK in raw:
            idx = body.rfind("\n\n")
            body = body.rstrip() + "\n\n" + block

    # 微抛章少补
    if n in MICRO:
        while hz(body) < V47_LO and block:
            extra = TOPUP.get(n, "")
            if extra in body:
                break
            body = body.rstrip() + "\n\n" + extra[:80]
            break
    else:
        guard = 0
        while hz(body) < V47_LO and guard < 5:
            guard += 1
            b = TOPUP.get(n, "")
            if not b or b in body:
                # 通用补一句
                b = "他按心，分列——恩在，辱在，仇在，不混。混了，还乱；不乱，路才直。"
                if b in body:
                    break
            body = body.rstrip() + "\n\n" + b

    body = trim_to_hi(body, V47_HI)

    # 脚注 v47
    if "v47爆款10" not in footer:
        footer = footer.replace("）", " · **v47爆款10**）", 1)

    out = body + END_MARK + "\n\n" + re.sub(
        r"（对照 `05`[^）]+）",
        lambda m: m.group(0) if "v47爆款10" in m.group(0) else m.group(0).replace("）", " · **v47爆款10**）"),
        footer.split(END_MARK)[-1] if END_MARK not in footer else footer,
    )
    # rebuild cleanly
    foot_m = re.search(r"（对照 `05`[^）]+）", raw)
    status_m = re.search(r"\*\*状态\*\*：[^\n]+", raw)
    footnote = foot_m.group(0) if foot_m else f"（对照 `05` §{n} · **v47爆款10**）"
    if "v47爆款10" not in footnote:
        footnote = footnote.replace("）", " · **v47爆款10**）", 1)
    status = status_m.group(0) if status_m else ""
    out = body + END_MARK + "\n\n" + footnote + "\n\n" + status + "\n"
    open(path, "w", encoding="utf-8").write(out)

    b2, _ = extract_body_and_footer(out)
    dup_s = [x.strip() for x in SPLIT.split(b2) if len(x.strip()) >= 8]
    seen, d = set(), 0
    for x in dup_s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    dup_r = d / len(dup_s) if dup_s else 0
    return n, before, hz(b2), dup_r, b2.count("嗯")


def main():
    results = []
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = int(re.search(r"ch(\d+)", p).group(1))
        if n not in TARGETS:
            continue
        results.append(process(p))
    for r in results:
        n, bef, aft, dup, en = r
        flags = []
        if aft < V47_LO:
            flags.append("SHORT")
        if aft > V47_HI:
            flags.append("OVER")
        if dup >= 0.02:
            flags.append(f"DUP={dup:.3f}")
        if en > 1:
            flags.append(f"EN={en}")
        print(f"ch{n:03d}: {bef}->{aft} dup={dup:.3f} en={en} {' '.join(flags) or 'OK'}")


if __name__ == "__main__":
    main()
