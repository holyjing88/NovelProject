# -*- coding: utf-8 -*-
"""Dedupe PAD appendages in ch87-89; expand ch90."""
import re
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VOL2 = ROOT / "../chapters/vol02-云岚杂役.md"

EXP87 = """
黑布遮眼演练最后一轮，顾迟年带队走完应急阵。摘下布时手心全是汗，却一步未错。云照看着他：「你们今天补上的，是我的缺，也是你们将来的缺。」众人沉默行礼。

演练记录命名《失嗅应战录》，列入大典后常训。顾迟年在末页写「靠人不靠神」，姜小满补「靠队不靠命」。云照圈了一圈，算作认可。

次晨公告墙贴新训令：核心队每月一次失感演练。姜小满抄进日课簿，页角添八字：以众补缺，以稳补险。顾迟年每逢夜训前先看一眼，谁也不再把失嗅当作一人秘密，而当作全队战术现实。

雨停后，霍照临把误差簿摔在案上：「你三次提前半息，明天再抢，我踢你下主位。」顾迟年拱手：「记下了。」铁柱旁听，瓮声嘀咕：「霍师兄骂人像骂人，可手一直给迟年哥递水。」

孙福把「多源报位」编成六步口诀，贴满值房。新人一听就会，老人嫌烦，孙福只指旧档：「烦，比死好。」满堂一静，背诀声反而齐了。

大典前最后一夜，顾迟年独坐檐下，摸守岁灯。灯芯金红微跳，像应青萝镇口长明。他低声：「急什么，灯还亮着呢。」风过，无香，有心。"""

EXP88 = """
授牌后，顾迟年首个记名任务是护送典礼名册入封录阁。程不二配双人核验三道封印，孙福盯印泥，铁柱外圈押道。顾迟年笑：「护册比护人还紧。」

姜小满授牌后没休息，进偏殿补「观礼压心训练」——十几人围看，逼自己在目光中稳呼吸。练到最后，掌心火丝稳得像拉直的线。云照道：「记名不是名分，是在所有眼睛看你时，仍能做对。」

云照召集新记名弟子讲第一课：你们不是被选中的幸运者，而是被选中的补位者。哪里最缺人，你们就去哪里。顾迟年听完，反而更踏实——路看得见脚印该落哪。

收尾时主峰人群散尽，顾迟年与姜小满并肩抬空灯架下阶，肩膀被木梁压得发疼，都没松手。山门外远钟敲响：不是礼成，是开工。

云照单独交记名期任务册：每旬后线值守、每战后复盘、带一名一阶微光新弟子。末页批注：记名弟子先学带人，再学胜人。顾迟年把册按在心口，木牌重量第一次真正落地。"""

EXP89 = """
三日后扫渣队交阶段报告：残符二百一十三枚、异常灯器十九件、疑似封灯纹草稿六份、未登记钥匙四十七次，全部追溯到人。云照拍板：扫渣报告月度必交。铁柱苦脸，孙福认真：「写得清，才不再踩同一个坑。」

同日晚，封灯仓外围再现可疑脚印。扫渣队十息内封线、报位、核验，截获两名探子。霍照临值夜簿写四字：可独当线。顾迟年看见，心里比领牌那天更热。

孙福把值夜簿包好，说来年新人入训要当示例。铁柱笑骂「你比先生还先生」，却把扫渣流程又背一遍。守灯这门课，一页一页传下去，也在复盘里一字一字磨实。

夜里风紧，封灯仓外只剩雪落声。顾迟年巡完一圈回望主峰，第一次生出「我们真能把风挡住」的实感。值夜簿「渣净率」数字不好看，却每夜上升——记名弟子该做的，正是把这些难看但有用的数字抬高。

有人称「顾先生」，他摆手：「叫老头。」记名弟子，名在木牌，职在渣堆。灯不容尘，手不停，心不松。"""

EXP90 = """
顾迟年抚守岁灯，对姜小满道：「裴先生是卖记忆的商人，也是提醒人——灯油尽时，别乱付账。」

主峰钟声在黎明前再响，像对过去告别，也像向未来点灯。云照、霍照临、姜小满、程不二、铁柱、孙福与顾迟年在主阶短暂并肩，无人多言，只各自看了一眼灯。那盏灯经历过冲阵、谣战、失嗅、囚案、封风，仍稳稳亮着。

顾迟年默念：承平三十八年已尽，守灯之事未尽。风会再起，敌会再来，裴无妄也终会现身，但他们已不是旧日那群慌乱少年。

云照看向北城，缓缓道：「把第三卷值夜表提前一月。」霍照临应声，程不二已翻开新簿。顾迟年握紧记名牌，预感清晰：下一次风暴来时，他们会更疼，却也更稳。北风掠檐，主灯火芯轻轻一跳，像应答。承平三十八年最后一页合拢，下一页已被灯光照开。"""


def count(s):
    return len(re.sub(r"\s", "", s))


def main():
    spec = importlib.util.spec_from_file_location("m", ROOT / "_ch79_90_bodies.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    fixed = []
    for title, body in mod.CHAPTERS:
        b = body
        if "后段日常看着平静" in b:
            b = b.split("后段日常看着平静")[0].rstrip()
        if title.startswith("第八十七章"):
            b = b + EXP87
        elif title.startswith("第八十八章"):
            b = b + EXP88
        elif title.startswith("第八十九章"):
            b = b + EXP89
        elif title.startswith("第九十章"):
            if "**第二卷完**" in b:
                b = b.replace("**第二卷完**", "").strip()
            b = b + EXP90 + "\n\n**第二卷完**"
        fixed.append((title, b.strip()))

    lines = ["CHAPTERS = ["]
    for title, body in fixed:
        lines.append(f'    ("{title}", """{body}"""),')
    lines.append("]\n")
    (ROOT / "_ch79_90_bodies.py").write_text("\n".join(lines), encoding="utf-8")

    spec66 = importlib.util.spec_from_file_location("m66", ROOT / "_ch66_78_bodies.py")
    m66 = importlib.util.module_from_spec(spec66)
    spec66.loader.exec_module(m66)
    chapters = m66.CHAPTERS + fixed

    text = VOL2.read_text(encoding="utf-8")
    head = re.search(r"^(.*?)(?=### 第六十六章)", text, re.S | re.M).group(1).rstrip()
    footer = re.search(r"(\n---\n\n>\s*第三卷.*)", text, re.S).group(1).lstrip("\n")
    parts = [head, ""]
    for t, b in chapters:
        parts += [f"### {t}", "", b, "", "---", ""]
    parts.append(footer.strip())
    VOL2.write_text("\n".join(parts) + "\n", encoding="utf-8")

    nums = {"六十六":66,"六十七":67,"六十八":68,"六十九":69,"七十":70,"七十一":71,"七十二":72,"七十三":73,"七十四":74,"七十五":75,"七十六":76,"七十七":77,"七十八":78,"七十九":79,"八十":80,"八十一":81,"八十二":82,"八十三":83,"八十四":84,"八十五":85,"八十六":86,"八十七":87,"八十八":88,"八十九":89,"九十":90}
    for t, b in chapters:
        for k, v in nums.items():
            if k in t:
                n = count(b)
                flag = "OK" if 3500 <= n <= 4500 else ("SHORT" if n < 3500 else "LONG")
                print(f"ch{v}: {n} [{flag}]")
                break
    vol = VOL2.read_text(encoding="utf-8")
    print("dupe投石", vol.count("投石入水"))
    print("dupe第二卷完", vol.count("**第二卷完**"))


if __name__ == "__main__":
    main()
