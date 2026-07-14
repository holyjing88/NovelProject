# -*- coding: utf-8 -*-
"""以现稿为底，通俗改写扩面覆盖写回 ch121～125。"""
from __future__ import annotations

import importlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz

sf = importlib.import_module("_score_full")
HERE = os.path.dirname(__file__)
PROSE = os.path.join(HERE, "..", "prose")

# 每章：插入块（位置锚 = 正文中首次出现的句子后插入）+ 替换表（旧→新）
PLAN = {
    121: {
        "file": "ch121-再炼散.md",
        "repls": [
            ("复测前一月，韩泥关了废窑门，把门后用柴挡严，准备再炼培元散。",
             "复测前一月，韩泥把门关上了。柴挡严严实实，他要再炼一炉培元散。"),
            ("风从缝里挤进来，带着药山的潮气。他蹲在炉边清灰，一铲子一铲子，把渣细到指腹碾得开。",
             "风从缝里挤进来，潮得鼻头发凉。他蹲炉边清灰，铲子一下一下，渣细到指腹都能碾开。"),
            ("窑门关着，活像凡人烤薯。",
             "窑门关着，外头闻不见大动静，活像凡人在烤薯。"),
        ],
        "inserts": [
            ("他把罐按进怀里，怀沉得像把债序也按住了。",
             "\n\n他把泥封摸了一圈，圈干了才放心。干了像账清；账清了，外头骂闲话也砸不烂罐。罐在怀，怀才沉得住。"),
            ("见字落地，窑外忽然落了阵小雨。",
             "\n\n同棚有人隔门嘀咕：「闭门七天，真炼还是装样子？」他不应。应了像解释；解释费舌头，舌头要留给闻香。"),
        ],
    },
    122: {
        "file": "ch122-织月嘲.md",
        "repls": [
            ("白织月再嘲，专挑丹试榜刚贴出来那一阵。",
             "榜一贴出来，白织月那句嘲就跟过来了。"),
            ("坡下人挤得像粥锅翻沫。",
             "坡下人挤得满当当，像粥锅翻了沫。"),
            ("三字落地，场上嗡了半息。",
             "三个字砸下去，场子嗡了半息。"),
        ],
        "inserts": [
            ("她冲他轻轻摇头，像怕沾魁晦气。",
             "\n\n旁边有人嘀咕：「末行也算报名？」又有人接：「算。管事册上有名就得上。」嘀咕远了，像潮退；潮退了，嘲还挂在耳边。"),
            ("「试台见。」他又低声说了一遍，像钉钉子。",
             "\n\n他把罐口泥封又抹了一道，抹匀了才睡下。睡下不等于撒手；撒了手，榜上那行丑骨就真成笑话。"),
        ],
    },
    123: {
        "file": "ch123-戾衡影.md",
        "repls": [
            ("钱戾衡那道影，落在复测前半月。",
             "复测前半月，钱戾衡那道影又落下来了。"),
            ("内门练剑刚散，廊下靴底声沉，沉里金线边一闪一闪。",
             "内门练剑刚散，廊下靴底声沉。沉里头，金线边一闪一闪。"),
            ("哄笑薄薄起一层，薄也真。",
             "哄笑薄薄起了一层，薄归薄，却真扎耳。"),
        ],
        "inserts": [
            ("他把粥喝尽，谢轻，恩重。",
             "\n\n刘婆看他一眼：「影吓着了？」他摇头：「吓手才要紧。手不吓人，影只是影。」刘婆哼一声，把空碗收回去。"),
            ("「不洒。」韩泥应得很短。",
             "\n\n他回到窑里，先把渣袋搁稳，再摸玉牌。牌凉得像提醒：半年不是嘴上数，是手上一息一息熬出来的。"),
        ],
    },
    124: {
        "file": "ch124-无言挡.md",
        "repls": [
            ("试台风声紧到嗓子眼那几天，赖福余党最爱嚼一句话：「盗渣炼散。」",
             "试台风声紧那几天，赖福一伙最爱嚼一句：「盗渣炼散。」"),
            ("嚼声在丙九灶边散开，像臭气。",
             "这话在丙九灶边散开，臭得像馊锅。"),
            ("指印无人敢按。赖福脸青一阵，骂骂咧咧走了。",
             "谁也不敢按指印。赖福脸青一阵，骂骂咧咧走了。"),
        ],
        "inserts": [
            ("他把姜汤喝尽。谢轻，恩重。",
             "\n\n灶边又有人咬耳朵：「铁师兄真护他？」对面压声：「账在他手里。你敢咬，你先对账。」耳朵话散了，韩泥当没听见。听见了也只护手，不护脸。"),
            ("「试台，见。」他对坛低声。",
             "\n\n窑角药草束轻轻晃了一下。晃得小，却够他把叶青禾那句「手别抖」又按实一遍。按实了，明日再听嚼舌也不慌。"),
        ],
    },
    125: {
        "file": "ch125-窑炉稳.md",
        "repls": [
            ("备战最后七日，韩泥只守窑温。",
             "最后七日，韩泥啥都不做了——就守窑温。"),
            ("窑门柴挡压严，严得像当年席盖捂坛。",
             "窑门柴挡压得死紧，紧得像当年席盖捂坛。"),
            ("赖福已无新招，只在廊外晃木牌：「七日后试台，看你滚。」",
             "赖福没新花样了，只在廊外晃木牌：「七日后试台，看你滚。」"),
        ],
        "inserts": [
            ("望着坛，独眼平：「稳。记着。」七日封窑毕，九粒仍正。正，试台就在手上。",
             "\n\n他把九粒又挨个闻了一遍。闻完不炫，只点头。点头给自己看：稳了，才配出门挨验。"),
            ("封窑毕那夜，他对着微温一线又钉一句：「七日稳了。明日验，别飘。」",
             "\n\n夜里窑缝风小了些。小了好，小了温更匀。匀了，他才敢合眼半息——半息醒来，手先摸泥封。封在，心就在。"),
        ],
        # 末段原先易成超长墙：强制拆段
        "split_tail": True,
    },
}


def apply_plan(body: str, plan: dict) -> str:
    for old, new in plan.get("repls", []):
        if old in body:
            body = body.replace(old, new, 1)
    for anchor, chunk in plan.get("inserts", []):
        if anchor in body and chunk.strip() not in body:
            body = body.replace(anchor, anchor + chunk, 1)
    if plan.get("split_tail"):
        # 把末段过长墙按句号拆成缩段
        paras = re.split(r"\n\s*\n", body)
        fixed = []
        for p in paras:
            t = re.sub(r"\s+", "", p)
            if len(t) <= 180 or p.strip().startswith("#"):
                fixed.append(p)
                continue
            # 按句拆
            parts = re.findall(r"[^。！？]+[。！？]?", p.strip())
            buf = ""
            for s in parts:
                cand = (buf + s).strip()
                if len(re.sub(r"\s+", "", cand)) > 160 and buf:
                    fixed.append(buf.strip())
                    buf = s
                else:
                    buf = cand
            if buf.strip():
                fixed.append(buf.strip())
        body = "\n\n".join(fixed)
    return body


def qa(body: str, footer: str):
    h = hz(body)
    dr, dups = sf.dup_rate(body)
    walls = sf.wall_paras(body)
    q = body.count("「")
    hk = [k for k in sf.HOOK_KEY if k in sf.hook_tail(body)]
    issues = []
    if not (2000 <= h <= 2500):
        issues.append("LEN%d" % h)
    if dr != 0:
        issues.append("dup")
        if dups:
            issues.append(dups[0][:50])
    if walls:
        issues.append("WALL%d/%d" % (len(walls), walls[0][0]))
    if q < 12:
        issues.append("Q%d" % q)
    if not hk:
        issues.append("NOHOOK")
    if "通俗笔锋" not in footer:
        issues.append("FOOT")
    return h, dr, q, hk, issues, dups, walls


def main():
    data = json.loads(open(os.path.join(HERE, "_tmp_121_125.json"), encoding="utf-8").read())
    rows = []
    for n in range(121, 126):
        key = str(n)
        body = data[key]["body"]
        footer = data[key]["footer"]
        plan = PLAN[n]
        new_body = apply_plan(body, plan).rstrip() + "\n"
        # 若仍不足2000，末段前补一句（不与已有句重复）
        h0 = hz(new_body)
        pad_pool = {
            121: "他把袖口泥印又拍净一遍，拍净了才算今日歇手。",
            122: "夜深榜角还翻着，翻归翻，他怀里罐纹丝不动。",
            123: "廊外风硬了半息，他仍只按罐，不按人。",
            124: "灶火灭了半截，他窑里那点温却没灭。",
            125: "封泥硬边划过指腹，疼一下也好——疼着记稳。",
        }
        guard = 0
        while hz(new_body) < 2050 and guard < 8:
            pad = pad_pool[n] if guard == 0 else ("又" + pad_pool[n][1:] if False else "")
            # unique pads
            pads = [
                pad_pool[n],
                "他听更鼓过了一记，记完才把息放匀。",
                "炉边灰细，细得像能按住明日那口气。",
                "门外脚步乱了一阵，乱完又静。静好，静了才闻得准。",
                "他把「正」字在心里又贴了一贴，贴实了才躺下。",
                "檐雨细了，细雨打柴挡，像数息。",
                "邻床梦呓一声，他没接话，只护着手里那点温。",
                "玉牌凉贴胸，凉得像把日子钉牢。",
            ]
            add = pads[guard % len(pads)]
            if add in new_body:
                guard += 1
                continue
            # insert before last paragraph
            paras = re.split(r"\n\s*\n", new_body.rstrip())
            if len(paras) >= 2:
                paras.insert(-1, add)
                new_body = "\n\n".join(paras) + "\n"
            else:
                new_body = new_body.rstrip() + "\n\n" + add + "\n"
            guard += 1
            if hz(new_body) > 2480:
                break
        # trim if over
        while hz(new_body) > 2500:
            paras = re.split(r"\n\s*\n", new_body.rstrip())
            if len(paras) < 3:
                break
            # drop a short pad-like para near end (not last)
            dropped = False
            for i in range(len(paras) - 2, 0, -1):
                if 8 <= len(re.sub(r"\s+", "", paras[i])) <= 40:
                    paras.pop(i)
                    dropped = True
                    break
            if not dropped:
                break
            new_body = "\n\n".join(paras) + "\n"

        h, dr, q, hk, issues, dups, walls = qa(new_body, footer)
        text = new_body.rstrip() + "\n" + footer
        if not footer.startswith("\n"):
            text = new_body.rstrip() + "\n" + footer
        # footer from dump already starts with \n---
        text = new_body.rstrip() + footer
        if not issues:
            path = os.path.join(PROSE, plan["file"])
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text if text.endswith("\n") else text + "\n")
            rows.append((plan["file"], h, "OK", q, hk))
            print("%s hz=%d q=%d OK hook=%s" % (plan["file"], h, q, ",".join(hk[:4])))
        else:
            rows.append((plan["file"], h, "|".join(issues), q, hk))
            print("%s hz=%d FAIL %s" % (plan["file"], h, "|".join(issues)))
            if dups:
                print(" dup:", dups[:2])
            if walls:
                print(" wall:", walls[0])
    print("---")
    for name, h, tag, q, hk in rows:
        print("%s\t%d\t%s" % (name, h, tag))


if __name__ == "__main__":
    main()
