# -*- coding: utf-8 -*-
"""Second pass: fix remaining 簿 references in cultivation context."""
import os, re

ROOT = os.path.join(os.path.dirname(__file__), '..')

REPLACEMENTS = [
    ('ch003-簿上无名', 'ch003-塔鸣初缘'),
    ('第 3 章 · 簿上无名', '第 3 章 · 塔鸣初缘'),
    ('缘箓簿', '缘塔'),
    ('丹道簿上', '丹堂谱上'),
    ('寿元在塔壁', '寿元在塔壁金铭'),
    ('落在簿上', '落在塔铭'),
    ('落在塔铭上', '落在塔铭'),
    ('鸿蒙万缘塔上，洞府', '塔壁浮铭，洞府'),
    ('鸿蒙万缘塔上，', '塔壁'),
    ('簿上善缘', '塔壁善缘'),
    ('簿上又沉', '塔底又沉'),
    ('簿上记', '塔铭记'),
    ('簿上显示', '塔影显现'),
    ('簿上文字', '塔壁金铭'),
    ('簿上闪', '塔壁一闪'),
    ('簿上金光', '塔鸣金光'),
    ('簿上因果', '塔底因果'),
    ('簿上缘字', '塔壁缘字'),
    ('簿上跳动', '塔鸣'),
    ('簿上微涨', '塔底微涨'),
    ('簿上「缘」', '塔壁「缘」'),
    ('簿上规则', '塔壁金铭'),
    ('簿上**缘箓', '塔壁**缘箓'),
    ('簿上**缘', '塔壁**缘'),
    ('簿上因果涌动', '塔底因果涌动'),
    ('簿上丁级', '塔影丁级'),
    ('簿上闪「假缘」', '塔壁一闪「假缘」'),
    ('簿上记诺', '塔铭记诺'),
    ('簿上记。', '塔铭记。'),
    ('一枚丹堂，一枚簿上记', '一枚丹堂，一枚塔铭记'),
    ('收簿入怀', '识海塔定'),
    ('对方临终赠簿', '对方乃馈元天尊尘念，葬仪即记号'),
    ('对方赠万缘塔', '对方乃馈元天尊尘念'),
    ('临终赠簿', '临终留诀'),
    ('簿灵显', '塔鸣显'),
    ('簿上名字', '塔壁名字'),
    ('簿上缘字黯淡', '塔壁缘字黯淡'),
    ('簿上又颤', '塔鸣又颤'),
    ('簿上记着呢', '塔里记着呢'),
    ('用「簿上一颤」', '用「塔鸣一荡」'),
    ('塔壁浮现', '塔壁浮现'),
    ('簿上异变', '塔影异变'),
    ('簿上再议', '塔里再议'),
    ('全在簿上', '全在塔铭'),
    ('与塔壁「三品」', '与塔壁「三品」'),
    ('与簿上', '与塔壁'),
    ('「簿……又记了？」', '「塔……又鸣了？」'),
    ('簿无风自动', '塔影无风自明'),
    ('簿……又记', '塔……又鸣'),
    ('馈缘+10 落在簿上', '馈缘+10 落在塔铭'),
]

SKIP = {'migrate_bo_to_tower.py', 'fix_bo_round2.py'}

def fix(text):
    for a, b in REPLACEMENTS:
        text = text.replace(a, b)
    # Generic 簿上 -> 塔壁 when not 宗门
    text = re.sub(r'(?<!宗门)(?<!脉案)(?<!执法堂)簿上', '塔壁', text)
    return text

changed = []
for dirpath, _, files in os.walk(ROOT):
    for fn in files:
        if not fn.endswith('.md') or fn in SKIP:
            continue
        p = os.path.join(dirpath, fn)
        with open(p, 'r', encoding='utf-8') as f:
            o = f.read()
        n = fix(o)
        if n != o:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(n)
            changed.append(p)

print(f'Round2: {len(changed)} files')
for p in sorted(changed)[:25]:
    print(' ', os.path.relpath(p, ROOT))
