# -*- coding: utf-8 -*-
import glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')

FILLER = (
    '塔外风声如刀，内门钟声如鼓。顾迟年不抬头，只以二阶烛火护住袖中豆火——示人是二阶，'
    '照路却已到三阶门槛。铁柱在远处瓮声骂娘，姜小满在杂役堂点灯，沈青禾在青萝熬药，'
    '程不二在坊市倒货，裴无妄在幽灯集数愿，陆承安在东峰塑真相，霍照临在闭关里凝五阶灯影，'
    '云照长老在藏经阁守半卷经。各忙各的，唯守岁灯不灭。'
)

FILLER2 = (
    '云岚宗钟又响一声，内外门各忙各的。顾迟年摸袖中守岁灯，豆火温温，像青萝镇口长明。'
    '迟暮之约还剩两年，霍照临的五阶灯影在远处如悬雷，万灯大会终将照面。他不急，只把守岁灯往袖里藏深，'
    '转身时袍角带风，像一名普通老杂役。可孙福、铁柱、姜小满，以及那些默默抱拳的人，'
    '都知这老头点的不是自己的命灯，是众人的路。'
)

FILLER2B = (
    '赵魁在暗处骂，陆承安在东峰冷笑，霍照临在塔下抱臂。顾迟年都不看，只看守岁灯。'
    '豆火虽小，却照见该照的路。他再把袍角理平，像普通老杂役那样，继续走该走的路——'
    '扫渣、挑水、带队、入塔，哪一步都急不得。'
)

EN_REPL = [
    ('unofficial 守灯使', '非正式守灯使'),
    (' unofficial ', ' 非正式 '),
    (' nightly ', ' 每夜 '),
    ('unfinished', '未竟'),
    ('truth 不只一种写法', '真相不只一种写法'),
    (' blind time', ''),
    ('— blind time', ''),
]

VOL4_DUP_PREFIXES = [
    '灯域未全开，巷战先起，烽火照夜。沈青禾穿烟越火寻顾迟年',
    '烽火巷战，沈青禾寻顾迟年重逢',
    '烽火重逢，沈青禾照顾迟年背',
    '府塌，梁压谢长缨，陆承安撑梁',
    '梁下顾迟年灯域震，见谢长缨命灯明',
    '陆承安死，顾迟年接最后一缕母光',
    '陆承安死，背承击，血染诏书',
    '墓前顾迟年以五阶灯影照陆承安一生',
    '墓前灯影照陆承安一生',
    '陆承安墓旁忽有黑气，魔修残气',
    '墓旁黑气最后一扑',
    '虚影入守岁灯，霍照临：「此堂，名护陆。」',
    '震怒非为己，为程不二、铁柱、秦照',
    '震怒之后是静。顾迟年入定',
    '不二斋火案牵出镇灯司黑账，赃银如山',
    '温言连审三日，百姓命灯明一线。陆承安戴枷入司',
    '幼帝与万民同举灯，开灯令刻石永镇',
    '更鼓远传，玄京云开一线',
    '夜风卷过承平门，城楼灯旗猎猎。百姓举灯相随',
    '青萝镇口长明与皇城气运，在这一夜像被一根看不见的灯芯串起',
    '裴无妄虚影远观，不插手，只一句：「卷四将尽，卷五在天。」',
    '顾迟年立夜风中，望灯，望城，望路',
    '霍照临立墓前，像接过了陆承安未走完的阶',
    '圣旨到，追复顾迟年贡院名次',
    '陆承安能下床，瘦如枯骨',
    '借万民一日暖，守岁灯满溢',
    '沈青禾四阶灯盏成后油仍不稳',
    '城南赈灾，沈青禾四阶灯盏照路',
    '万灯大会前，沈青禾率青萝灯会最后一次',
    '井底禁术未止，魔修残气欲吞全城',
    '铁柱挡井，无阶如灯骨',
    '铁柱挡井，万家灯火汇身',
    '禁术爆，丞相府塌，梁木如龙',
    '云岚宗钟又响一声，内外门各忙各的',
    '赵魁在暗处骂，陆承安在东峰冷笑',
]


def remove_filler(text, filler):
    n = text.count(filler)
    while filler in text:
        text = text.replace('\n\n' + filler + '\n\n', '\n\n')
        text = text.replace('\n' + filler + '\n', '\n')
        text = text.replace(filler, '')
    return text, n


def remove_dup_summary_lines(text, prefixes):
    lines = text.split('\n')
    out = []
    removed = 0
    for line in lines:
        s = line.strip()
        if not s:
            out.append(line)
            continue
        if any(s.startswith(p) for p in prefixes) and len(s) > 80:
            removed += 1
            continue
        out.append(line)
    return '\n'.join(out), removed


def main():
    f2 = os.path.join(DOCS, '../chapters/vol02-云岚杂役.md')
    with open(f2, 'r', encoding='utf-8') as f:
        c = f.read()
    total = 0
    for filler in (FILLER, FILLER2, FILLER2B):
        c, n = remove_filler(c, filler)
        total += n
    with open(f2, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'Vol2 filler removed: {total}')

    f4 = os.path.join(DOCS, '../chapters/vol04-玄京封灯.md')
    with open(f4, 'r', encoding='utf-8') as f:
        c = f.read()
    c, r = remove_dup_summary_lines(c, VOL4_DUP_PREFIXES)
    with open(f4, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'Vol4 duplicate summary lines removed: {r}')

    for fp in glob.glob(os.path.join(DOCS, '05-万古守灯人-分章正文-*.md')):
        if '目录' in fp:
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            t = f.read()
        orig = t
        for a, b in EN_REPL:
            t = t.replace(a, b)
        if t != orig:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(t)
            print(f'English fixed: {os.path.basename(fp)}')


if __name__ == '__main__':
    main()
