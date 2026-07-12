# -*- coding: utf-8 -*-
import os, re
root = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\凡人修真传\prose\vol01'

replacements = [
    ('不能把账算死', '不能把恩算死'),
    ('册只记成恩', '心只记恩'),
    ('缘未落册', '缘未记心里'),
    ('册不收虚', '心不收虚'),
    ('他仍不蘸', '他仍不写'),
    ('按指试写', '心口试念'),
    ('血干，字不起', '念不出，记不实'),
    ('你信那块册', '你信那条规矩'),
    ('册也白记', '恩也落空'),
    ('从未开过的册', '从未落字的仇格'),
    ('册也硬', '心也沉'),
    ('册不温', '心未暖'),
    ('心在册', '心在心里'),
    ('比册还难抹', '比唾沫还难抹'),
    ('邪册', '邪物'),
    ('合上册', '合目不辩'),
    ('一本破册', '一条破规矩'),
    ('看怀册', '按心口'),
    ('沉册', '沉心'),
    ('交易不进册', '交易不进恩席'),
    ('情不进册', '情不进恩席'),
    ('进册的', '记心里的'),
    ('不是册写的', '不是心里记的'),
    ('不是册写', '不是心里记'),
    ('不在册', '不在恩席'),
    ('兄弟不进册', '兄弟不进恩席'),
    ('真在兄弟，不在册', '真在兄弟，不在恩席'),
    ('攀附是嘴的事，不是册写的', '攀附是嘴的事，不是心里记的'),
    ('活短了，册也白记', '活短了，恩也落空'),
    ('仇格冷，像另一本从未开过的册', '仇格冷，像从未落字的格'),
    ('恩只记心里——恩在心里，恩干净', '恩只记心里，恩干净'),
    ('册也硬，一外一内', '心也沉，一外一内'),
    ('册里藏昨夜抄的路', '帖里藏昨夜抄的路'),
    ('像翻一本写满「劣」字的名册', '像翻一张写满「劣」字的名帖'),
    ('名在册，却像不该在', '名在榜，却像不该在'),
]

def process(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    orig = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    return False

changed = [fn for fn in sorted(os.listdir(root)) if fn.endswith('.md') and process(os.path.join(root, fn))]
print('Pass3 changed', len(changed))
for fn in changed:
    print(fn)

for fn in sorted(os.listdir(root)):
    if not fn.endswith('.md'): continue
    with open(os.path.join(root, fn), encoding='utf-8') as f:
        body = f.read().split('## 本章自检')[0]
    bad = []
    for pat in ['记账', '账本', '账簿', '恩账', '阳账', '旧账', '不记账', '活账', '还账', '数账', '压册', '读册', '册会', '邪册', '破册', '怀册', '沉册', '心在册', '不进册', '不在册']:
        if pat in body:
            bad.append(pat)
    if '账' in body and '名册' not in body:
        # check if only 名册 contains 账... 账 is in 名册? no 册
        pass
    rem = [l for l in body.splitlines() if '账' in l and '名册' not in l and '报名册' not in l]
    if rem:
        print('账REMAIN', fn, len(rem))
    rem2 = [l for l in body.splitlines() if '册' in l and '名册' not in l and '报名册' not in l and '测灵名册' not in l]
    if rem2:
        print('册REMAIN', fn, len(rem2))
