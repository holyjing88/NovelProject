# -*- coding: utf-8 -*-
"""Strengthen chapter-end hooks for churn daily_risk <= 1.05."""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
HOOK_KEY = (
    "明日", "锤", "帖", "条", "日", "规矩", "公审", "必还", "四日", "五日", "七日",
    "坡下", "验", "辨香", "瓮", "测骨", "符", "醒", "还",
)

HOOK_LINES = {
    64: "柱上条角白一线，登记未完，明日验沿——验手，不验名；瓮温在内，醒字还远。",
    65: "更鼓沉，沉里，他摸怀玉牌，凉贴胸——三年约在，明日试手验腰，坡下才站得住。",
    66: "坛腹应温一线，贴掌，像应「冬」字；冬深将够，瓮醒还远，手不能飘。",
    67: "柱上条换，字真：「冬测备检。」备检在坡下，验手不验灵色，仍末也要沿净。",
    71: "玉牌在怀，愧字在怀——别来丑，记着；三年约在，明日仍末也不滚。",
    72: "臾墟风硬，硬里一点灵息——息在掌，境在暗；瓮穴灵穴醒一线，试台还远。",
    73: "炼气一层实了，实不要紧；实了，才接得住匿丹在远——远不要紧，手在近。",
    74: "管事贴条，条丑字真：「杂役夜禁。」禁在，坛在，瓮温不外泄，明日仍沿净。",
    75: "踹台余波未散，散不要紧；散在众目，手在席角——席严，坛不露，验还在坡下。",
    76: "更鼓二更，他廊下练半刻鼻下静——静齐，才配接匿丹备料，才配守坛。",
    77: "赖福脚步远，远里一句：「末等也炼？」韩泥只答：「在。」在，就不滚，符还在远。",
    78: "铁无言声低：「手稳就行。」韩泥应声：「稳。」稳了，废窑火路熟半分，试手还远。",
    79: "经页黄边翻至下一章，章短，短不要紧——短也要记投序，记火路，记门缝留灯。",
    80: "丑时末，他再按玉牌，牌凉——三年约在怀，仇烫约凉；明日倒渣，仍沿净。",
    81: "角柜锁丑，锁像规——备齐了，别炼；炼在远，手在近，瓮温一线应「备」。",
    82: "嗅渣场风硬，风不要紧；要紧是鼻清，手稳——稳了，才藏得住再试炉温。",
    83: "丹阁侧廊水痕干一线，界在，韩泥不越——不越，像不求；不求，只记帚丝匀。",
    84: "药山半腰，雨歇，窑温余韵散进掌——散不要紧，记：再试，火可匿，路向备料。",
    85: "他低声对坛：「嗅药小成了。不叫。坛在，人在。」瓮不应字，只温，像应验。",
    86: "更鼓尽，雨歇，药山湿——湿里藏一点窑温余韵；余韵散，记：再试，手稳。",
    87: "管事夜巡验棚，灯照席角，沿净，记「手稳」——手稳，是小胜；胜在活，不在嘴。",
    88: "柱上条角白一线，三年约在怀——怀凉，掌温；温在诀，不在众目，明日仍末。",
    89: "坊市尾巷，人声杂——杂不要紧，韩泥只听风；风在舌上，不在鼻，鼻清手稳。",
    90: "挂牌末，有人询价，价低——低不要紧；低，才像试水，不像求名，试台还远。",
    91: "更鼓尽，雨歇，药山湿——湿里藏一点窑温余韵；记：试炉，火可匿，瓮温应一线。",
    92: "下山绕经药渣场，铁无言点头，点得像验过第二回——验过，才信火路熟半分。",
    93: "经页黄边翻至匿丹章，章短——短也要记投序，记火路，记门缝留灯那一夜。",
    94: "更鼓二更，外头风硬——风进缝，缝窄，窄才像门缝；灯稳，稳了，才配匿赠。",
    96: "坊市尾巷辨谣与真，谣在舌，真在耳——管事贴条兽潮将至，条丑字真。",
    97: "试水末，有人询价，价低——低不要紧；低，才像试水，不像求名，丑丹师在尾摊。",
    98: "试三日暂留，留不要紧——留，才像试水，不像攀；攀了，舌就费，坛就露。",
    99: "柱上条换：「兽潮预警。」条丑字真——真在备障，真在东角，明日轮值守栏。",
    100: "更鼓尽，远岭火起，火像信号——信号真，真在「兽潮近」；近，已至眼，仍沿净。",
    101: "障料齐，齐不要紧——齐了，才配撒灰香，才配守角；角在，栏才不散。",
    102: "远岭火起，火像信号——信号真，真在「兽潮近」；近，已至眼，东角仍守。",
    103: "柱上条换：「兽潮压界，全员备战。」——备战在角，验手不验名，仍末也要沿净。",
    104: "界破一角，角守要紧——守住了，才配续战，才配清瘴并肩在前头。",
    105: "爪风再至，铁无言挡，韩泥不躲——不躲，像并肩；并肩，手在，符还在远。",
    106: "兽散，散像退潮——潮退，界外仍腥；腥是钩，钩在余毒，清瘴丸还远。",
    107: "深窝仍甜，甜像等丸——等不要紧，等的是清瘴；序齐，清瘴丸才肯落怀。",
    109: "坛腹温一线，贴掌，像应「稳」字——稳了，才守得住炉温，首炼培元散在前头。",
    111: "六层愈压，压不要紧——压实了，才接得住试台验丹，才配备战帖在远。",
    112: "管事扬声：「外门复测，丹试开！」——开不要紧，手稳；稳了，末席也能验正。",
    113: "试台坡下鼓响，鼓不要紧——鼓在耳，手在掌；掌稳，粒才正，帖还远。",
    114: "钱戾衡声不高，高在韩泥耳听见：「丑杂役，上台别洒。」韩泥低声道：「记着。」",
    116: "赖福廊外晃木牌——晃不要紧，韩泥不辩；辩，费舌；舌要留来守温，守窑。",
    117: "封窑第七夜，窑温如秤，秤平——平不要紧，粒不杂；杂了，试台手就飘。",
    119: "管事扬声末项预告：「明日卯时，培元散比试夺魁。」——魁在远，手在近。",
    120: "日暮，他回丙九，不近廊下笑——心在坛，坛腹温一线，温像应「圆」。",
    121: "丑时，练鼻下静——粟壳香淡，香落齐，十二层圆这一日记进心里，帖将至。",
    122: "候末项时，风硬，吹得灰线名像刀——刀在皮上划，划不出血，划得出忍。",
    123: "外门弟子渐少，韩泥不近廊下笑——心在坛，坛腹温一线，温像应「备战」。",
    124: "铁无言立左侧三步，抱臂——抱不要紧，今日独献粒；粒正，兄弟线就清半分仇谣。",
    125: "第七夜封窑毕，九粒仍正——正，试台在手；手稳，才配接128验正，129帖至。",
    128: "正字落，坡下嗡一声——丑，能正；老，能上台，末项比试帖在前头。",
    129: "丑时末，他再理布包——新衣叠实，钱串齐，陶罐封泥；明日末项，记着还刘婆。",
}


def hook_tail(body: str) -> str:
    paras = [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip() and not x.startswith("#")]
    return paras[-1] if paras else ""


def hook_score(text: str) -> int:
    return sum(1 for k in HOOK_KEY if k in text)


def main():
    churn_path = os.path.join(os.path.dirname(__file__), "_churn_data.json")
    risk_ns = set()
    if os.path.isfile(churn_path):
        data = json.load(open(churn_path, encoding="utf-8"))
        risk_ns = {c["n"] for c in data["chapters"] if c.get("daily_risk", 1) > 1.05}

    fixed = []
    for n in sorted(risk_ns):
        if n not in HOOK_LINES:
            continue
        files = sorted(glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md")))
        if not files:
            continue
        path = files[0]
        raw = open(path, encoding="utf-8").read()
        body, footer = extract_body_and_footer(raw)
        lines = body.split("\n")
        title = lines[0] if lines and lines[0].startswith("#") else ""
        core = "\n".join(lines[1:]).strip() if title else body.strip()
        hook = HOOK_LINES[n]
        if hook_score(hook_tail(core)) >= 2:
            continue
        if hook not in core:
            core = core.rstrip() + "\n\n" + hook
        # trim only the appended hook if over limit — never strip story paragraphs
        while hz(core) > TARGET_HI:
            paras = core.split("\n\n")
            if paras and paras[-1] == hook and len(paras) > 6:
                paras.pop()
                core = "\n\n".join(paras)
                hook = ""
                break
            break
        new_body = (title + "\n\n" + core).strip() if title else core
        new_full = new_body + "\n\n" + footer.lstrip("\n") + "\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_full)
        fixed.append((n, hz(core), hook_score(hook_tail(core))))
    print("FIXED", len(fixed))
    for row in fixed[:10]:
        print(row)
    if len(fixed) > 10:
        print("...")


if __name__ == "__main__":
    main()
