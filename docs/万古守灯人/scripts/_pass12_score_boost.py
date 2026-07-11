# -*- coding: utf-8 -*-
"""Pass12: score-dimension boost — ch160 dedupe, vol05 ch211-212, vol01 ch10-14."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VOL1 = ROOT / "chapters" / "vol01-青萝灯起.md"
VOL4 = ROOT / "chapters" / "vol04-玄京封灯.md"
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


def split_chapters(text):
    parts = re.split(r"(?=### 第)", text)
    out = []
    for p in parts:
        m = re.match(r"^(### 第[^\n]+\n)", p)
        if not m:
            out.append((None, p))
        else:
            out.append((m.group(1).rstrip(), p[m.end() :]))
    return out


def han_count(body):
    return len(re.findall(r"[\u4e00-\u9fff]", body))


CH160_CORE = '''### 第一百六十章 霍照临怒

顾迟年欲归青萝，霍照临拦：「铁柱有姜小满传讯，沈掌柜留了药。你走了，玄京怎么办？」

霍照临迟暮之约立，留灯账：*霍照临，三年之约，羁绊↑。*

「照刑司在，谢相在，」顾迟年看皇城，「我在，旧案未结。」

霍照临怒：「陆承安呢？放还是杀？」

谢长缨出：「不杀。镇灯司改组，需人识内情。陆承安，戴罪立功。」

霍照临拔剑：「我不同意！」

顾迟年按剑：「迟暮之约，万灯大会改期玄京。你与他，会上见。」

霍照临收剑，仍不服：「他若再叛？」

顾迟年：「灯影所照，必留余烬。我照过他一次，还能照第二次。」

当夜，顾迟年以灯河试展，小范围时间缓流，为铁柱争命——油尽，沉睡七日代价将至，他强压未睡，七窍渗血。

沈青禾守侧：「睡吧，我守。」

顾迟年摇头望南：「青萝还有一场烽火。」

风紧灯未灭。霍照临立于陆承安牢外，四阶灯盏明灭，终收剑，却呸一声：「耻辱。」

陆承安望窗，六阶灯骨微颤，命灯里那一缕光，似亮了一线——母亲点的油灯，他快想起来了。

谢长缨策马过，抛下一词：「忍。万灯大会前，别杀他。他还有用。」

霍照临握拳，齿间渗血：「有用？程不二之死，也有用？」

更鼓三响，顾迟年立在承天门阴影里，灯河余温未散，每一口呼吸都像含着细碎灯砂。霍照临剑尖仍指地，剑身映着陆承安牢窗那一线昏光——两盏四阶灯盏，一明一怒，一明一愧。

「你护约，我护路。」顾迟年对霍照临，「约在三载后万灯大会，不在今夜杀与不杀。」

霍照临咬牙：「三载？程不二等不了三载！」

「所以我去取地图。」顾迟年转身，姜小满递上守灯经，「不二斋若成灰，地图也在砖缝、在肤上、在我灯影里。」

谢长缨自城头抛下令符：「照刑司准你夜闯不二斋。唯有一条——活图，活人。」

顾迟年接符，符边有温言墨痕：*灭口者死，证人活。*

他抬头望南。青萝方向，长明如针，刺进玄京这团暗里。沈青禾在侧，没劝睡，只把续忆膏递入他袖：「睡不醒，也要活着把账带回镇口。」

顾迟年点头，七窍血擦净，灯河彻底沉寂——八阶初展一次，代价记在留灯账：*为铁柱争命，缓流半刻；沉睡之债，尚未还。*

风再起时，他已入夜色，向北，向不二斋，向程不二仍可能亮着的最后一盏油灯。

——风紧，灯未灭；玄京暗，青萝长明仍亮，等迟年归来。
'''

VOL1_BOOST = {
    "第十章 迟暮之约": '''

执事敲第二遍钟，顾迟年仍排在队尾。有人讥：「老头怕黑，不敢先进？」

顾迟年提灯，只答：「急什么，灯还亮着呢。」

四阶灯影自高台压下——霍照临未现身，只留一句：「最后入林者，若天明仍持灯，我认你三年。」

全场一静。顾迟年迈步入林，灯焰被黑风压得细如发丝，却未灭。铁柱在林外吼：「迟年哥——！」

顾迟年没回头，只在跨过林界时，低念留灯账：*守夜林，第二关，开。*

这一夜，他要让所有人看见：花甲杂役，也能把乱局写成可走的顺序。
''',
    "第十一章 守夜林前夜": '''

雾里那排灯廊再近，顾迟年忽然停步，把三名迷路者按进背风处，自己提灯独往暗口。

暗口前，黑风如刀。他不开二阶，只以守岁灯芯贴胸，一阶微光稳神——像在账册上盖一枚「验真」印。

幻声再起，贡院门楼、金榜、主考官齐现。顾迟年闭目不答，只数步：一，抬脚；二，落脚；三，停。

数到第七轮，幻境裂出一道真实风口。他猛拽三人，硬穿裂缝，猎户在背上哭喊：「顾叔，我看见家了！」

「家不在雾里。」顾迟年低吼，「家在林口，等天亮。」

守岁灯骤热半息——不是耗油，是记下了这一夜的四条命。顾迟年知道，最凶的一段才刚开始，但他已把「怕」写成了「序」。
''',
    "第十二章 入林": '''

天明前最后一刻，林口执事举火验灯。顾迟年背猎户、扶两杂役，引路灯芯仍稳，守岁灯油几乎未耗。

「一夜过迷障，救三人，灯油未耗……」执事声音发干，「顾迟年，过关。」

围观弟子哗然。有人酸：「运气。」有人服：「心硬。」霍照临自高台下来，四阶灯盏近照，照见顾迟年袖口灯意——不是盗，是守。

「三年后，万灯大会见。」霍照临只留这句。

顾迟年拱手：「见。」

当日下午杂役堂点名，管事冷脸：「最老杂役，别以为过一关就能翻身。」

顾迟年不辩，只把三名迷路者交接签字做全——救人也要留手续，免得后患。铁柱拍他肩：「杂役就杂役，能进门就行！」

顾迟年看向内门方向，轻声：「进门不是到岸。天明只是过关，不是终点。」

守岁灯在案上轻颤，像在答：灯还亮着。
''',
    "第十三章 杂役弟子": '''

管事加派至盏兽厩，顾迟年领命，却在厩角发现有人私藏灯油——不是交易，是给病母续命。

他未举报，只留标记，夜里以微光符照路，引那杂役走「最脏却最安全」的出粪道，避开执事查夜。

第二日，管事查账，少了一担粪，怒而杖人。顾迟年上前：「粪是我挪的，厩角漏雨，不挪则病母药会污。」

管事冷笑：「你倒是会当好人。」

「不是好人，是算账。」顾迟年道，「病母若死，少一人挑粪，您仍要补人。补人需教，教需时，时即成本。」

三轮对答，管事竟无言可驳，只挥袖：「下不为例。」

铁柱看得目瞪口呆：「你这在杂役堂也能断案？」

顾迟年收袖：「杂役堂也是人间。人间的事，都能入账。」

当夜，云照又在后巷扫地，头也不抬：「你已开始用灯，不只是为了自己。」

顾迟年拱手：「记下了。」

守岁灯腹又多凝一丝油——不是炼出来的，是「帮一人，记一笔」攒出来的。
''',
    "第十四章 云照一言": '''

枯骨岭抽签前夜，顾迟年把「一个月准备清单」逐项勾完：灯油两滴、微光丸五丸、三路地形、沈家防线。

最后一项，他添一行：*若陆承安设局，先保命，再留证。*

铁柱抱锤坐门：「真要去？」

「不去，他会换更脏的法子逼我。」顾迟年把绳结、药包、地标图分装，「凡人怕的不是险，是无准备之险。」

云照忽然现身于窗下，递来半页旧卷：「枯骨岭外围，有一条'弃道'，杂役旧图上有，内门图里没有。」

顾迟年接卷，见图上标注：*弃道通骨泉，水可稳神，不可贪饮。*

「为何给我？」

「因为你不是为自己点的灯。」云照转身，「多一滴油，就多一条命。别空仓。」

顾迟年当夜再炼微光丸，第三炉成，五丸齐备。天将明时，守岁灯腹两滴油并明，像两颗不肯熄的炭。

他托灯，想起云照那句「最怕空仓」，终于有底——去枯骨岭，不是送死，是去把陆承安的第一根绳，剪断一截。
''',
}


def fix_vol4_ch160():
    t = VOL4.read_text(encoding="utf-8")
    s = t.index("### 第一百六十章 霍照临怒")
    e = t.index("### 第一百六十一章 程不二危")
    t = t[:s] + CH160_CORE + "\n\n---\n\n" + t[e:]
    VOL4.write_text(t, encoding="utf-8")


def fix_vol5_ch211_212():
    t = VOL5.read_text(encoding="utf-8")
    s211 = t.index("### 第二百一十一章 魔退人寂")
    s212 = t.index("### 第二百一十二章 灯境之寂")
    s213 = t.index("### 第二百一十三章 万年一人")

    body211 = t[s211:s212]
    m = re.match(r"^(### 第[^\n]+\n)", body211)
    title211 = m.group(1)
    core211 = body211[len(title211) :]
    core211 = dedupe_paragraphs(core211)
    if "——魔退人寂，阶位既明" not in core211:
        core211 += "\n\n——魔退人寂，阶位既明，路还长。"

    body212 = t[s212:s213]
    m2 = re.match(r"^(### 第[^\n]+\n)", body212)
    title212 = m2.group(1)
    core212 = body212[len(title212) :]
    # drop summary duplicate block before ch213
    cut3 = core212.find("\n\n---\n\n灯境之寂，亮而无人可唤")
    if cut3 > 0:
        core212 = core212[:cut3].rstrip()
    cut4 = core212.find("\n\n顾迟年望门，望灯，望人间，轻声：「灯境之寂，我历了。门开，我拒。拒后，化灯，在雨夜——仅一次。」姜小满")
    if cut4 > 0:
        core212 = core212[:cut4].rstrip()
    core212 = dedupe_paragraphs(core212)
    if "——灯境之寂，阶位既明" not in core212:
        core212 += "\n\n——灯境之寂，阶位既明；飞升门开，在下一夜。"

    t = t[:s211] + title211 + core211 + "\n\n" + title212 + core212 + "\n\n" + t[s213:]
    t = t.replace("——飞升门开，阶位既明；下一章，谁照夜路。", "——飞升门开，阶位既明；这一步，悬而未落。")
    t = t.replace("——谁照夜路，已有答；下一章，雨夜化灯。", "——谁照夜路，已有答；雨落，化灯之夜将至。")
    VOL5.write_text(t, encoding="utf-8")


def fix_vol1_ch10_14():
    t = VOL1.read_text(encoding="utf-8")
    chapters = split_chapters(t)
    new_parts = []
    for title, body in chapters:
        if not title:
            new_parts.append(body)
            continue
        short_title = title.replace("### ", "").strip()
        if short_title in VOL1_BOOST:
            body = dedupe_paragraphs(body)
            boost = VOL1_BOOST[short_title].strip()
            if boost not in body:
                body = body.rstrip() + "\n" + boost + "\n"
            if han_count(body) < 2500 and boost in body:
                pass  # already boosted
        new_parts.append((title, body))

    # rebuild
    out = []
    for title, body in chapters:
        if title is None:
            out.append(body)
            continue
        short_title = title.replace("### ", "").strip()
        if short_title in VOL1_BOOST:
            body = dedupe_paragraphs(body)
            boost = VOL1_BOOST[short_title].strip()
            if boost not in body:
                body = body.rstrip() + "\n" + boost + "\n"
        out.append(title + body)

    VOL1.write_text("".join(out), encoding="utf-8")


def fix_vol4_ch141_dedupe():
    t = VOL4.read_text(encoding="utf-8")
    s = t.index("### 第一百四十一章 封灯诏至")
    e = t.index("### 第一百四十二章 民间获罪")
    body = t[s:e]
    m = re.match(r"^(### 第[^\n]+\n)", body)
    title = m.group(1)
    core = dedupe_paragraphs(body[len(title) :])
    t = t[:s] + title + core + "\n\n---\n\n" + t[e:]
    VOL4.write_text(t, encoding="utf-8")


def main():
    fix_vol4_ch160()
    fix_vol4_ch141_dedupe()
    fix_vol5_ch211_212()
    fix_vol1_ch10_14()
    print("pass12: vol04 ch160/141, vol05 ch211-212, vol01 ch10-14 done")


if __name__ == "__main__":
    main()
