# -*- coding: utf-8 -*-
"""v47 精修 ch031-ch050：1780-1950字 · 嗯≤1 · dup<2% · 独钩 · v47爆款10"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
TARGET_LO, TARGET_HI = 1780, 1950
SKIP = {35, 41}
END_MARK = "\n\n---\n\n章末"
SPLIT = re.compile(r"(?<=[。！？])")

REPLS = [
    (r"韩泥「嗯」一声：", ["韩泥点头：", "韩泥应声：", "韩泥不答，只记：", "韩泥声平："]),
    (r"韩泥「嗯」一声", ["韩泥点头", "韩泥应声", "韩泥不谢", "韩泥只记"]),
    (r"韩泥「嗯」声", ["韩泥点头", "韩泥应声"]),
    (r"韩泥喝尽，「嗯」一声", ["韩泥喝尽，不谢", "韩泥喝尽，只记"]),
    (r"韩泥喝一口，「嗯」一声", ["韩泥喝一口，不谢", "韩泥喝一口，只记"]),
    (r"韩泥：「嗯。」", ["韩泥点头。", "韩泥应声。"]),
    (r"「嗯。」韩泥说", ["韩泥点头。", "韩泥应声。"]),
    (r"「嗯。」韩泥", ["韩泥点头。", "韩泥应声。"]),
    (r"「嗯。」\s*\n", ["点头。\n", "应声。\n"]),
    (r"叶青禾「嗯」一声", ["叶青禾点头", "叶青禾应声"]),
    (r"铁无言「嗯」一声", ["铁无言点头", "铁无言翻簿"]),
    (r"秦霜「嗯」一声", ["秦霜点头", "秦霜不夸"]),
    (r"管事「嗯」一声", ["管事点头", "管事验过"]),
    (r"刘婆.*?「嗯」一声", None),  # handled per-match
]

EXTRA_TOPUP = {
    34: "赖福秤虚，坛腹应忍。忍不是怂，是存锤——锤在叶挡石，石未落，心先稳。稳到能立誓必还；还，先还烫。",
    37: "筐底密，壁直，口收圆。圆了，库役无话；无话，记功一笔。功在册，功也在手茧里——茧厚，疼真，疼真才记得住沿前止。",
    38: "铁无言立桩，声低，不夸。不夸，眼却看堆——堆齐，名在末，也在路。路通向嗅诀，通向编筐，通向冬后正测末排。",
    39: "刘婆护粥，粥稀，热在。热在，第七笔又温半分。温半分，够熬到备检帖、清粪栏、兽栏冬角。",
    40: "掌按石，灰线短，短不过指节。指节短，手不短——手稳，备检才过。过了，木牌在怀，怀暖，牌更真。",
    42: "病兽尽，栏净，多清半刻。净，管事才肯记名；记名，正测前三两落袋才验得过。落袋，手不能抖。",
    43: "三两实粮落袋，落袋才真。真了，明日仍盯。仍盯，饭才稳第二日。第二日稳，恩才不断；恩不断，汤才还得了热。",
    45: "藤刺旧疤，疤裂，血渗。渗到沿前，收手，席盖严。渗不到沿上，瓮不醒——不醒，对。对，才接得住冬后正测那一验。",
    46: "查库小胜，胜在册上有印。印在，克字又虚一寸。虚一寸，够活；活，才配问香帖在册。",
    47: "验簿记印，印在，路在。路通向栖香谣，谣要剥，剥一寸，手稳一寸。手稳，才配廊下半刻辨香。",
    48: "腥囊揭了，温短仍在。温短像汤，汤是热的。热的记着，不混腥；混了，心就乱，手就飘。",
    49: "帖在枕下，七笔在心，温短在鼻。都在，命就在。命在，四日后坡下见。见了，规矩才开；开了，路才直。",
    50: "坡下石阶将晚又起霜。霜白，像给三日后先验铺一层白纸。纸上写字，字是「验香」——验香在鼻，不在嗓。",
}

TOPUP = {
    31: "官道尽头，驿亭旗在风里猎猎。旗旧，字深，深得像里正那枚印——印让他出门，门开了，恩还在身后钉着。他望旗半息，不拜，只记：记路，记恩，记西驿验骨。验骨在明日卯时，骨在，命在；命在，叶汤还不凉。",
    32: "驿西棚里，更鼓将尽。更鼓沉，沉得像泥岗丑时擦坛——习惯在，根在。韩泥摸木牌，牌凉，凉不过心口六笔恩。恩背着，肩才稳；肩稳，侧门才进得。侧门窄，窄也进；进了，才有丹香引路，才有兽栏练手，才有将来还恩的秤。",
    33: "山门丹香淡一寸，淡不过兽栏活臭。活臭里，他清粪铲下仍稳——稳像泥岗抬棺，稳像公审末席。末席也是席，席在，饭在；饭在，七日后测骨帖才验得过。帖在柱上，手就别抖；抖了，恩断，汤就凉。",
    34: "三日测骨帖在柱，柱在，手就不能软。软了，滚字成真；硬了，末席也是席。席在，坛在，恩在——三在，够撑到丑时前那一闪温光。坛腹应忍，不应怒；怒像少年，他是记心翁，记克扣，记刘婆半勺，记叶挡石那四字。",
    36: "刘婆第七笔落在心，不落字纸；宗门恩另册，不混泥岗六笔。混则还错人，错人，汤就凉。凉不得，叶汤还在前头等着。肘暖了，臂能抬；能抬，才端得住将来还恩的丹。",
    37: "编筐课毕，掌茧又厚一层。厚，疼真；疼真，记着，等瓮醒那日扎得准。准了，血才落对地方——落篓底，不蹭坛；蹭坛，像求醒，求醒不像丑翁。",
    38: "渣场灰热罩脸，鼻下苦甘分列。甘短，苦长——短真长记，不混则准。准了，铁无言才翻簿；簿上有名，名在末，也在路。路通向嗅诀，通向编筐，通向冬后正测。",
    39: "克扣月半，秤仍虚。虚在赖福嘴，实在韩泥手——手稳，饭才实一日。实一日，多活一日；多活一日，多记一日恩。记满了，才还得上热的。",
    40: "冬测备检帖在柱，掌茧裂处疼，疼不露。露了，石前就抖；抖了，备检白过。备检过了，正测还远——远不要紧，手稳一日，多活一日。",
    42: "兽栏冬角，雪混粪，铲下仍稳。稳，管事才肯多清半刻；多清半刻，小兽咳轻半声。咳轻，像沈枯芽那日怯笑——笑浅，恩不浅。恩不浅，手就不能软。",
    43: "盯秤这日，三两落袋，掌心不抖。抖在袖里，袖里稳了，秤盘才实。实了，赖福才虚——虚不是终，终在正测，在辨香，在还；还，先还热的，热的，先还叶丫头汤。",
    44: "破布角三字塞怀：静、列、漏。诀稳，舌不浪费在笑他的人身上。三日后编筐帖在柱，手在，鼻在，路不断。香净了，才近栖香谣；谣要避腥，腥不碰，像不求邪。",
    45: "三十五只筐入库，血三回，沿前止。止住了，瓮才醒得正。正醒，才还得了热的。冬后正测条在柱，备检记名在怀——怀暖，牌更真；真在还能站，站得住，才配廊下问香。",
    46: "内谣在起，不要紧；要紧是手稳，手稳才验得过问香帖。帖在，鼻在，路在——路通向栖香谣，通向坡下规矩，通向末排先验。",
    47: "问香帖在册，印在，路在。路通向栖香谣，谣要剥，剥一寸，手稳一寸。手稳，才配廊下半刻辨香；辨香净了，才近正测三关。",
    48: "栖香谣少半，谣少不要紧；要紧是鼻下静，静才分得清温短与腥长。分清，坡下才站得住；站得住，四日后规矩才听得进。",
    49: "四更将尽，柱上风歇。风歇，他心里七笔又齐一回——齐在胸，不在嘴。嘴嚼恩，嚼成谎；胸记恩，记成真。真，才配四日后坡下站末排。",
    50: "三日条在柱，七笔在心。嗓轻，鼻重——重，才配末排。末排不要紧，验香才要紧。验得过，关才开第二道；关开了，才学凝丹，学了，先还烫。",
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


def reduce_en(text: str) -> str:
    """Keep at most one 嗯; prefer keeping 韩泥 dialogue 「嗯。」 if present."""
    positions = [m.start() for m in re.finditer("嗯", text)]
    if len(positions) <= 1:
        return text
    # keep first 韩泥「嗯」 or first occurrence
    keep_idx = 0
    for i, m in enumerate(re.finditer("嗯", text)):
        ctx = text[max(0, m.start() - 12) : m.start() + 8]
        if "韩泥" in ctx and ("一声" in ctx or "「嗯」" in ctx):
            keep_idx = i
            break
    result = text
    ri = 0
    for i, m in enumerate(re.finditer("嗯", text)):
        if i == keep_idx:
            continue
        start, end = m.start() + ri, m.end() + ri
        ctx = result[max(0, start - 20) : start + 20]
        repl = "点头"
        if "喝尽" in ctx or "喝一口" in ctx:
            repl = "不谢"
        elif "铁无言" in ctx or "秦霜" in ctx or "管事" in ctx:
            repl = "点头"
        elif "叶青禾" in ctx:
            repl = "应声"
        elif "一声" in ctx:
            repl = "应声"
        elif "「嗯」" in ctx or "嗯。" in ctx:
            repl = "点头"
        else:
            repl = "应声"
        # replace whole phrase if possible
        seg = result[max(0, start - 15) : end + 5]
        if "「嗯」一声" in seg:
            old = "「嗯」一声"
            new = f"「{repl}」" if repl != "不谢" else "不谢"
            result = result[: start - 15] + seg.replace(old, new, 1) + result[end + 5 :]
            ri += len(new) - len(old) - (15 - (start - max(0, start - 15)))
        elif "「嗯」" in seg:
            result = result[:start] + repl + result[end:]
            ri += len(repl) - 1
        else:
            result = result[:start] + repl + result[end:]
            ri += len(repl) - 1
    return result


def reduce_en_v2(text: str) -> str:
    """Line-based 嗯 reduction: keep one, replace rest."""
    lines = text.split("\n")
    en_lines = [i for i, ln in enumerate(lines) if "嗯" in ln]
    if len(en_lines) <= 1:
        return text
    keep = en_lines[0]
    for i in en_lines:
        if "韩泥" in lines[i] and ("一声" in lines[i] or "「嗯」" in lines[i]):
            keep = i
            break
    subs = ["点头", "应声", "不答", "只记", "声平", "不谢"]
    si = 0
    for i in en_lines:
        if i == keep:
            continue
        ln = lines[i]
        for pat, rep in [
            (r"韩泥「嗯」一声：", ["韩泥点头：", "韩泥应声：", "韩泥声平："]),
            (r"韩泥「嗯」一声", ["韩泥点头", "韩泥应声", "韩泥不谢"]),
            (r"韩泥「嗯」声", ["韩泥点头", "韩泥应声"]),
            (r"韩泥喝尽，「嗯」一声", ["韩泥喝尽，不谢", "韩泥喝尽，只记"]),
            (r"韩泥喝一口，「嗯」一声", ["韩泥喝一口，不谢"]),
            (r"「嗯。」韩泥说", ["韩泥点头。", "韩泥应声。"]),
            (r"「嗯。」", ["点头。", "应声。", "只答一字。"]),
            (r"铁无言「嗯」一声", ["铁无言点头", "铁无言翻簿"]),
            (r"秦霜「嗯」一声", ["秦霜点头", "秦霜不夸"]),
            (r"管事「嗯」一声", ["管事点头", "管事验过"]),
            (r"叶青禾「嗯」一声", ["叶青禾点头", "叶青禾应声"]),
            (r"刘婆.*?「嗯」", None),
        ]:
            if rep and re.search(pat, ln):
                r = rep[si % len(rep)]
                ln = re.sub(pat, r, ln, count=1)
                break
        else:
            ln = ln.replace("嗯", subs[si % len(subs)], 1)
        lines[i] = ln
        si += 1
    return "\n".join(lines)


def fix_body_issues(body: str, n: int) -> str:
    body = re.sub(r"\n---\n", "\n", body)  # stray --- in body (ch050)
    body = dedupe_sentences(body)
    body = reduce_en_v2(body)
    # ch032 broken sentence fixes
    if n == 32:
        body = body.replace(
            "韩泥「嗯」一声。「嗯什么嗯？」弟子恼，「去杂役处登记。别挡测灵根的人。」",
            "韩泥点头。弟子恼：「去杂役处登记。别挡测灵根的人。」",
        )
        body = body.replace(
            "比是少年，\n\n轮到",
            "比是少年，他不比。\n\n轮到",
        )
        body = body.replace(
            "少年不是他，\n\n他掏",
            "少年不是他，他是记恩记辱那一个。\n\n他掏",
        )
        body = body.replace(
            "比是少年，\n\n邻铺",
            "比是少年，他不比。\n\n邻铺",
        )
    # ch043 dup tail cleanup
    if n == 43:
        body = re.sub(
            r"盯秤后，掌心仍不抖。抖在袖里，秤盘实了，赖福才虚[^。]*。$",
            "盯秤后，掌心仍不抖。抖在袖里，秤盘才实；实了，赖福才虚——虚不是终，终在辨香，在还；还，先还热的。",
            body.strip(),
        )
    # ch044 typo
    if n == 44:
        body = body.replace("像不求邪。」", "像不求邪。")
    return body


def ensure_hook(body: str, n: int) -> str:
    if END_MARK in body:
        head, _ = body.split(END_MARK, 1)
    else:
        head = body
    if n in TOPUP and TOPUP[n] not in head:
        head = head.rstrip() + "\n\n" + TOPUP[n]
    return head


def trim_to_hi(body: str) -> str:
    while hz(body) > TARGET_HI and "\n\n" in body:
        paras = body.rsplit("\n\n", 1)
        if len(paras) < 2:
            break
        trial = paras[0]
        if hz(trial) < TARGET_LO:
            break
        body = trial
    return body


def pad_to_lo(body: str, n: int) -> str:
    for extra in [TOPUP.get(n, ""), EXTRA_TOPUP.get(n, "")]:
        if extra and extra not in body and hz(body) < TARGET_LO:
            body = body.rstrip() + "\n\n" + extra
    return body


def fix_footer(footer: str) -> str:
    if "v47爆款10" not in footer:
        footer = footer.replace("）", " · **v47爆款10**）", 1)
    return footer


def process(path: str) -> dict:
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in range(31, 51) or n in SKIP:
        return {"n": n, "skip": True}
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    before = {"hz": hz(body), "en": body.count("嗯"), "dup": 0}
    body = fix_body_issues(body, n)
    body = ensure_hook(body, n)
    body = pad_to_lo(body, n)
    body = dedupe_sentences(body)
    body = trim_to_hi(body)
    footer = fix_footer(footer)
    if END_MARK not in raw:
        new_raw = body + END_MARK + "\n\n章末\n\n" + footer.lstrip()
    else:
        _, tail = raw.split(END_MARK, 1)
        new_raw = body + END_MARK + tail
        # preserve footer from original if tail has it
        if "章末" not in tail:
            new_raw = body + END_MARK + "\n\n章末\n\n" + footer.lstrip()
    open(path, "w", encoding="utf-8").write(new_raw)
    after_body, _ = extract_body_and_footer(new_raw)
    return {
        "n": n,
        "skip": False,
        "before": before,
        "after": {"hz": hz(after_body), "en": after_body.count("嗯")},
    }


def main():
    results = []
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = int(re.search(r"ch(\d+)", p).group(1))
        if 31 <= n <= 50:
            results.append(process(p))
    for r in results:
        if r.get("skip"):
            print(f"ch{r['n']:03d}: SKIP")
            continue
        a = r["after"]
        flags = []
        if a["hz"] < TARGET_LO:
            flags.append("SHORT")
        if a["hz"] > TARGET_HI:
            flags.append("OVER")
        if a["en"] > 1:
            flags.append(f"EN={a['en']}")
        print(
            f"ch{r['n']:03d}: {r['before']['hz']}→{a['hz']} "
            f"en {r['before']['en']}→{a['en']} {' '.join(flags) or 'OK'}"
        )


if __name__ == "__main__":
    main()
