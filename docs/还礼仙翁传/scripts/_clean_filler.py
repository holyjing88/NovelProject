#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""移除误插垫字段，恢复 v16 收束，补至≥2000。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hand_polish_strip import polish_body
from prose_utils import extract_body_and_footer, hz

PROSE = Path(__file__).resolve().parent.parent / "prose"
LO = 2000

FOOTER_ENDINGS = {
    "ch029-闪回一瞬.md": "莫长春袖空，一念收塔，杖落掌，声轻：「天试门前，还有一场大还。还不了，就别先算。旧收，夜话要来。下一份，卷终夜话。」",
    "ch030-卷终夜话.md": "莫长春袖空，一念收塔，杖落掌，声轻：「卷二起，商会女修至。修亮，价硬。」",
    "ch031-商会女修.md": "莫长春袖空，一念收塔，杖落掌，声轻：「修走，饼要来。饼轻，线重。下一份，一盒茶饼。」",
    "ch032-一盒茶饼.md": "莫长春袖空，一念收塔，杖落掌，声轻：「饼完，买卖要公。公比饼响，响里见真章。下一份，公平买卖。」",
    "ch033-公平买卖.md": "莫长春袖空，一念出塔，杖点简角，不撕，只记。声轻：「下一份，东脉账本——账比价厚，厚里藏火。」",
    "ch034-东脉账本.md": "莫长春袖空，一念收塔，杖落掌，声轻：「账厚，桌要拍。拍响，定调。下一份，宗主拍桌。」",
    "ch035-宗主拍桌.md": "莫长春袖空，一念出塔，杖点案角，不撕，只记。声轻：「拍响，页要来。丹方残页，轻里藏丹。」",
    "ch036-丹方残页.md": "莫长春袖空，一念收塔，杖落掌，声轻：「页活，炼要来。大炼比页响，响里见金丹。下一份，丹堂大炼。」",
    "ch039-体统.md": "莫长春袖空，一念收塔，杖落掌，声轻：「统小，火要来。火近，礼更烫。下一份，赤焰逼近。」",
    "ch040-赤焰逼近.md": "莫长春袖空，一念出塔，杖点旗角，不撕，只记。声轻：「火近，年要来。三十年，比旗长。下一份，三十年。」",
    "ch041-三十年.md": "莫长春袖空，一念收塔，杖落掌，声轻：「话完，阁要开。百宝阁二次，轻里藏价。」",
    "ch042-百宝阁二次.md": "莫长春袖空，一念收塔，杖落掌，声轻：「钉小，谋要来。谋比钉毒，毒在身边。」",
}

TOPUP = {
    "ch029-闪回一瞬.md": "风大，桂香扑脸，像有人从百年外走来，又停在门口，不进门——不进，才是还礼。",
    "ch030-卷终夜话.md": "赵玄机立执法堂阶上，听「缘箓二转」风传，指节叩铁牌——妒与服绞在一起，墨里仍留一寸空。",
    "ch032-一盒茶饼.md": "弟子围驿道，围「茶饼换情报」，围得像看一场亏本却乐意的买卖——简已进柳青鸢案，案上像多了一柄看不见的刀。",
    "ch033-公平买卖.md": "茶饼入驿那夜，简上「佯攻」二字像鼓，「夜袭」二字像刀——刀还没落，鼓先响，响得全宗睡不着。",
    "ch034-东脉账本.md": "霍镇山再骂：「表厚，盾更硬！」年轻长老围抄「谁守田」三字，抄得像抄门规——规在，根就在。",
    "ch035-宗主拍桌.md": "林挽月立廊外，听「东脉不让」，终未近。顾小满值夜，指节白——不让字一落，杂役也不能退。",
    "ch036-丹方残页.md": "阶下弟子屏息，全宗都在等延迟的那一声「成」——成不在噪，在炉；不在门内，在廊外那一杖点地的声。",
    "ch039-体统.md": "验丹文书到，全宗围金丹，不围嘴。体统还在嚼，嚼不过验丹钟响——子时之前，东脉旗更红。",
    "ch040-赤焰逼近.md": "周德海立后阵棚，令旗迟迟不落。莫长春低声：「四月够送。子时到了，看谁先露怯。」风腥，旗远，像刀已提名。",
    "ch041-三十年.md": "弟子在前堂猜七种版本，版本里都没有后院并排的两盏灯——灯在，话在，战在近，等在收。",
    "ch042-百宝阁二次.md": "弟子围驿外，围「半块茶饼再送」，围得像看亏本乐意——记得恩的人，不走绝路。",
}


def strip_filler(body: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    kept = []
    for p in paras:
        if "塔意沉一寸" in p:
            continue
        if "莫长春不辩，只记这一日的礼" in p:
            continue
        if p.startswith("还礼路长，一步是一记"):
            continue
        kept.append(p)
    return "\n\n".join(kept)


def ensure_ending(body: str, ending: str) -> str:
    if "一念收塔" in body or "一念出塔" in body.split("下一份")[-1]:
        # 保留已有收束，去掉重复收束前垫字即可
        if ending.split("，")[0] in body:
            return body
    body = body.rstrip()
    if ending not in body:
        body = body + "\n\n" + ending
    return body


def main() -> None:
    targets = list(FOOTER_ENDINGS.keys()) + ["ch028-赵之初见.md", "ch038-金丹成.md"]
    for name in sorted(set(targets)):
        p = PROSE / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        body, footer = extract_body_and_footer(text)
        body = strip_filler(body)
        body = polish_body(body)
        if name in FOOTER_ENDINGS:
            body = ensure_ending(body, FOOTER_ENDINGS[name])
        if name in TOPUP and hz(body) < LO:
            t = TOPUP[name]
            if t not in body:
                body = body.rstrip() + "\n\n" + t
        if not footer:
            footer = f"---\n\n*（上架连载稿 · {p.stem.split('-', 1)[1]}）*\n"
        p.write_text(body.rstrip() + "\n\n" + footer, encoding="utf-8")
        c = hz(body)
        st = "OK" if LO <= c <= 2600 else ("LOW" if c < LO else "HIGH")
        print(f"{name}: {c} ({st})")


if __name__ == "__main__":
    main()
