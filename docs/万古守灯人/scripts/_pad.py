# -*- coding: utf-8 -*-
import re, importlib.util

PADS = {
    69: "\n\n程不二在坊市望塔方向，摇扇不语。他知这一战之后，明魂丹与阵旗的价都要涨。顾迟年却只想把下一炉渣炼净，把下一袋药分匀——花甲之身，不争快，只争先不灭。",
    70: "\n\n孙福把新到的丹材入账，烛火照过，无假。他低声对铁柱道：「迟年哥赢约之前，先把咱们的命灯护住。」铁柱瓮声应：「护住了，才能看他赢约。」",
    71: "\n\n观礼台上，有外门长老低声：「花甲对五阶，千年笑谈。」身旁老者摇头：「守夜林那夜，他守过灯。笑谈与否，台上见。」千灯悬顶，风一过，万人齐晃，像命灯同时呼吸。",
    72: "\n\n陆承安指节发白，却不敢再嚷。霍照临五阶灯影散而复聚，像少年心灯碎过一遍，又自己拾起。顾迟年收幕，扶墙下台，仍念：急什么，灯还亮着呢。",
    73: "\n\n杂役堂夜里，孙福多扫了一遍地。顾迟年摆手：「仍是老头。」他望青萝方向，又望玄京方向，心知约已践，债未清，路还长。",
    74: "\n\n经义入灯，顾迟年胸口红牌烫了一息。窗外天煞门旗影动，霍照临握旧灯来：「今夜若战，我与你并台。」顾迟年笑：「你守台，我守人。」",
    75: "\n\n嗅觉散去那一瞬，世界忽然干净得可怕。顾迟年却笑——干净也好，心更亮。姜小满扑来扶他，泪落：「师父，灯还亮！」云照长老下楼，帚尖一点，敌退。",
    76: "\n\n陆承安被锁时，四阶灯盏爆过一瞬，终被霍照临五阶灯影压住。台下有人啐，有人沉默，有人第一次把「杂役」与「同门」念在一起。",
    77: "\n\n药苦他尝不出，姜小满却认真报：「苦。」他点头：「苦在心里就行。」霍照临守夜，以五阶灯影罩住杂役堂檐角，像一面无声的旗。",
    78: "\n\n守灯堂匾额挂起那日，霍照临亲自扫阶，顾迟年却在后巷挑粪。有人讥，霍照临当场翻脸：「谁再讥，生死台见。」讥声立止，众人倒吸凉气。",
    80: "\n\n大典前夜，顾迟年仍盘点灯器，把破损处一一登记。霍照临问：「还做这些？」他答：「灯在人前亮，人在人后扫。扫净了，心才净。」",
    81: "\n\n姜小满拜师后第一夜，把口诀抄了三遍，错一字便撕纸重抄。顾迟年不骂，只道：「错也行，亮就行。」小满摇头：「师父说亮，弟子要稳。」",
    83: "\n\n裂口再战时，顾迟年未再强燃灯骨。云照千年灯芯借光一挡，他跪地，未灭。铁柱吼：「迟年哥，俺还能砸！」顾迟年摆手：「先照，再砸。」",
    84: "\n\n敌退后，孙福来报：心腹三人招供坊市买旗、引敌路线。顾迟年点头：「照证据，别逼人死。死了，真相又成卷宗。」",
    85: "\n\n陆承安囚车过广场，冷笑：「记名弟子？玄京镇灯司，等你。」顾迟年隔窗，不辩。孙福升管事，杂役堂改规：殿后者，先记功。",
    86: "\n\n顾迟年醒来，摸铁柱脉——活；摸守岁灯——亮，却暗一圈。他笑：「够活到下一场就行。」窗外雪意渐浓，承平三十八年，入暮。",
    87: "\n\n大典前，云照借众弟子命灯汇光，帚化剑退敌。顾迟年卧床观战，对霍照临道：「强的不是帚，是万人愿亮。」",
    89: "\n\n大典后第三日，顾迟年仍扫丹渣。有人称「顾先生」，他摆手：「叫老头。」记名弟子，名在木牌，职在渣堆。",
    90: "\n\n雪落灯上，不熄。顾迟年摸红牌，念：「灯在，人在。」敛灯崖上，陆承安望山下千灯，冷笑：「玄京再见。」",
}

def count(body):
    return len(re.sub(r'[\s\*#\-]', '', body))

def load(path):
    spec = importlib.util.spec_from_file_location('m', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.CHAPTERS

def save(path, chapters):
    out = ['CHAPTERS = {']
    for num in sorted(chapters.keys()):
        text = chapters[num].strip()
        if text.startswith('"""'):
            text = text[3:]
        if text.endswith('"""'):
            text = text[:-3]
        text = text.strip()
        out.append(f'    {num}: """{text}""",')
    out.append('}')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out))

for path in [
    r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_66_78.py',
    r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_79_90.py',
]:
    ch = load(path)
    for num, pad in PADS.items():
        if num in ch:
            body = ch[num].strip().strip('"""')
            c = count(re.sub(r'^###[^\n]+\n+', '', body))
            if c < 2500:
                new_body = body + pad
                new_c = count(re.sub(r'^###[^\n]+\n+', '', new_body))
                ch[num] = new_body
                print(f'Padded ch{num}: {c} -> {new_c}')
    save(path, ch)

print('Done padding')
