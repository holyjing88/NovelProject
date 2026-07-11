# -*- coding: utf-8 -*-
"""Pass14: Qidian 10-point boost — golden ch1-3, vol05 ch210 padding, doc sync."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VOL1 = ROOT / "chapters" / "vol01-青萝灯起.md"
VOL5 = ROOT / "chapters" / "vol05-万古长明.md"


def dedupe_paragraphs(body):
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


CH1_TAIL = """他独自回阁楼，守岁灯放在父亲旧匣上。匣底有张黄纸，是他幼年时父亲教他认的第一个字——「灯」。他忽然想起父亲说过的半句：「迟年，灯在人在。」另半句，父亲咽了回去，像怕说多了，会把什么招回来。

顾迟年取纸，研墨，在灯下写下册名：**留灯账**。

第一行：*承平三十七年，秋，为自己与青萝镇口长明，点火。*

第二行：*沈青禾，认债不逃，记一笔。*

第三行：*赵福，逼债砸寿，记一笔；待堂上核。*

写至此处，守岁灯芯微温，像有人在账页右下角按了一枚看不见的印。顾迟年合上纸——册不在纸上，在灯腹里；纸只是书吏的习惯。

他对着灯火低语：「明日堂上，我不靠仙法赢，靠纸赢。仙法只续长明，不替我省一个字。」

窗外雨线如针。赵家方向，尚有狗吠。顾迟年把斗笠挂好——凡人打仗，先得睡够一个时辰。"""

CH1_REMOVE = """顾迟年把寿宴前后每一句话拆开重算：谁在逼债，谁在围观，谁在等他失态。凡人式算计讲究先稳人心再稳证据，他宁可慢半步，也不肯在县衙前把后手亮尽。夜雨敲窗，他反复默背明日堂问三轮，直到每个字都能在舌尖停住。"""

CH2_REMOVE_START = "回屋后，顾迟年把守岁灯放在案中，拿细棉布一寸寸擦拭"
CH2_TAIL = """天将明，他在纸边写下留灯账续行：*长明灯，雨夜续火一回；更夫见证，不索价。*

守岁灯腹那丝薄油，比昨夜厚了一线。顾迟年合上眼，只睡一个时辰。醒来时，县衙方向的锣，已在远方响第一声。"""

CH3_REMOVE = """药铺门口议论如潮，顾迟年不争输赢先争次序。他让见证人按时点排位，让证词按事实落纸，让情绪留到最后。围观者从看戏到哗然，他心里却只记着一件事：明日堂上，赵家必须先乱。"""

CH3_TAIL = """县衙门前，赵元青已率十余家丁列阵，四阶灯盏在额前微亮，压得百姓不敢抬头。顾迟年却只做两件事：把文书袋按次序摆好；把守岁灯压在袋底。

里正低声问：「你真告？」

顾迟年答：「我不告人，我告纸。」

堂鼓三响，县令升堂。赵福把借据呈上，声如滚雷：「沈氏欠债不还，请大人断！」

顾迟年出列，不跪，只拱手：「大人，草民顾迟年，请核纸、核墨、核账——核完，再断。」

堂上一静。赵元青眉峰一沉，四阶灯影向顾迟年压来一寸。

守岁灯在袖中骤热——一阶微光，照见的不是术，是赵福肩角那一线虚。

顾迟年抬眼，声音依旧温吞，却落字如钉：「急什么，灯还亮着呢。」

——堂上见纸，是灯路第二战。"""


def boost_ch1():
    t = VOL1.read_text(encoding="utf-8")
    if "留灯账续行" in t[:8000] and CH1_TAIL[:20] in t:
        print("ch1 already boosted")
        return
    if CH1_REMOVE in t:
        t = t.replace(CH1_REMOVE, CH1_TAIL, 1)
    elif CH1_TAIL not in t:
        anchor = "他送她出门，雨又落了下来，像有人在夜幕里掐着鼓点。顾迟年心里明白，明日县衙只是第一刀。真正的刀，藏在赵元青还没出鞘的后手里。"
        if anchor in t:
            t = t.replace(anchor, anchor + "\n\n" + CH1_TAIL, 1)
    VOL1.write_text(t, encoding="utf-8")
    print("ch1 boosted")


def boost_ch2():
    t = VOL1.read_text(encoding="utf-8")
    s = t.index("### 第二章 无字书册")
    e = t.index("### 第三章 守岁灯亮")
    body = t[s:e]
    if CH2_TAIL.strip() in body and CH2_REMOVE_START not in body:
        print("ch2 already boosted")
        return
    # remove duplicate mid-ch2 block
    idx = body.find(CH2_REMOVE_START)
    if idx > 0:
        # keep through first 守岁灯亮在案上 paragraph ending
        keep_end = body.rfind("这场仗还没开始，他却已把后手摆到第三层。")
        if keep_end > 0:
            body = body[: keep_end + len("这场仗还没开始，他却已把后手摆到第三层。")] + "\n\n" + CH2_TAIL + "\n"
            t = t[:s] + body + t[e:]
    VOL1.write_text(t, encoding="utf-8")
    print("ch2 boosted")


def boost_ch3():
    t = VOL1.read_text(encoding="utf-8")
    if CH3_TAIL[:15] in t:
        print("ch3 already boosted")
        return
    if CH3_REMOVE in t:
        t = t.replace(CH3_REMOVE, CH3_TAIL, 1)
    else:
        anchor = "顾迟年没回头。他知道堂上才是硬仗，药铺门前只是前哨。可前哨稳住了，第一口气就不会乱。"
        if anchor in t:
            t = t.replace(anchor, anchor + "\n\n" + CH3_TAIL, 1)
    VOL1.write_text(t, encoding="utf-8")
    print("ch3 boosted")


def clean_vol5_pre210():
    t = VOL5.read_text(encoding="utf-8")
    s = t.index("### 第二百一十章 万古对抗")
    pre = t[:s]
    # remove duplicate blocks before ch210 title
    marker = "第十二夜，顾迟年九阶再开，以万家愿齐对魔爪——撑到黎明，便是万古对抗。"
    if pre.count(marker) > 1:
        first = pre.index("---\n\n第十二夜，天魔全形现")
        # keep up through line 2725 single block, cut 2727-2742 style
        cut_start = pre.find("\n\n第十二夜，顾迟年九阶再开，以万家愿齐对魔爪——撑到黎明，便是万古对抗。", first)
        if cut_start > 0:
            cut_end = pre.rfind("\n\n### 第二百一十章 万古对抗")
            if cut_end < 0:
                cut_end = len(pre)
            # find last good paragraph before duplicates
            good = pre.rfind("第十二夜，魔全降，人未退；第十三夜，万古对抗。")
            if good > 0:
                pre = pre[: good + len("第十二夜，魔全降，人未退；第十三夜，万古对抗。")] + "\n\n"
                t = pre + t[s:]
                VOL5.write_text(t, encoding="utf-8")
                print("vol05 pre-210 cleaned")
                return
    # fallback: dedupe section before ch210
    parts = pre.rsplit("---", 1)
    if len(parts) == 2:
        tail = dedupe_paragraphs(parts[1])
        t = parts[0] + "---\n\n" + tail + "\n\n" + t[s:]
        VOL5.write_text(t, encoding="utf-8")
        print("vol05 pre-210 deduped")


def main():
    boost_ch1()
    boost_ch2()
    boost_ch3()
    clean_vol5_pre210()
    print("pass14 done")


if __name__ == "__main__":
    main()
