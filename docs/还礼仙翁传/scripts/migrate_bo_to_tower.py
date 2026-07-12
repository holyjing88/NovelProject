# -*- coding: utf-8 -*-
"""Migrate 赠缘簿/簿/薄册 → 鸿蒙万缘塔 narrative. Run from repo root."""
import os, re, sys

ROOT = os.path.join(os.path.dirname(__file__), '..')
PROSE = os.path.join(ROOT, 'prose')

# Order matters: longer phrases first
REPLACEMENTS = [
    ('赠缘簿', '鸿蒙万缘塔'),
    ('识海中塔影', '识海中的万缘塔'),
    ('膝上册页', '闭目内视塔影'),
    ('册页一合', '塔影一敛'),
    ('册已无字', '塔壁无铭'),
    ('册上「缘」', '塔壁「缘」'),
    ('册上', '塔壁'),
    ('薄册', '万缘塔'),
    ('万缘塔', '识海中塔影'),
    ('塔影在识海', '万缘塔镇识海'),
    ('簿在袖', '万缘塔镇识海'),
    ('簿猛地一烫', '塔鸣大作'),
    ('簿微烫', '塔鸣微作'),
    ('簿一烫', '塔鸣'),
    ('塔壁浮字', '塔壁浮铭'),
    ('塔壁浮半句', '塔壁浮半铭'),
    ('簿上字成', '塔壁金铭成'),
    ('簿上字', '塔壁金铭'),
    ('簿上无字', '塔壁无铭'),
    ('塔壁无新铭', '塔寂无铭'),
    ('簿无字', '塔壁无铭'),
    ('初缘已记', '初缘铭定'),
    ('活路在簿上', '活路在塔里'),
    ('演给塔看', '演给塔看'),
    ('记簿', '记塔'),
    ('对簿', '对塔'),
    ('塔规', '塔规'),
    ('簿意', '塔意'),
    ('簿与', '塔与'),
    ('簿沉', '塔底一沉'),
    ('簿烫', '塔鸣'),
    ('簿浮', '塔壁浮铭'),
    ('簿合', '塔影静'),
    ('簿翻', '塔影自转'),
    ('塔记', '塔铭'),
    ('簿答', '塔鸣'),
    ('簿只', '塔只'),
    ('簿仍', '塔仍'),
    ('簿却', '塔却'),
    ('簿已', '塔已'),
    ('簿又', '塔又'),
    ('簿再', '塔再'),
    ('簿在', '塔在'),
    ('仍无簿', '仍无塔影'),
    ('她无塔', '她无神识之塔'),
    ('他无簿', '他无神识之塔'),
    ('袖中无簿', '识海无塔显'),
    ('无簿，', '塔不显，'),
    ('有簿', '有塔'),
    ('无簿', '塔不显'),
    ('簿内', '塔内'),
    ('人情账簿', '人情账'),
]

# Bare 簿 in cultivation context - after longer replacements
BARE_PATTERNS = [
    (r'莫长春(?:[^。\n]{0,20})簿', lambda m: m.group(0).replace('簿', '塔')),
    (r'袖中(?:[^。\n]{0,8})簿', lambda m: m.group(0).replace('簿', '塔影')),
]

SKIP_FILES = {'_topup.py', '_expand_final.py', '_expand_batch2.py', '_expand_batch2b.py', 'migrate_bo_to_tower.py'}

def migrate_text(text):
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    # Fix double replacements
    text = text.replace('鸿蒙万缘塔录', '鸿蒙万缘塔符阁')
    text = text.replace('万缘塔子', '万缘塔')
    text = text.replace('万缘塔镇识海中', '万缘塔镇识海')
    text = text.replace('识海中海', '识海')
    return text

def process_file(path, dry_run=False):
    with open(path, 'r', encoding='utf-8') as f:
        orig = f.read()
    new = migrate_text(orig)
    if new != orig:
        if not dry_run:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new)
        return True
    return False

def walk_md(base):
    changed = []
    for dirpath, _, files in os.walk(base):
        for fn in files:
            if not fn.endswith('.md'):
                continue
            if fn in SKIP_FILES:
                continue
            p = os.path.join(dirpath, fn)
            if process_file(p):
                changed.append(p)
    return changed

if __name__ == '__main__':
    dry = '--dry' in sys.argv
    bases = [ROOT, os.path.join(ROOT, 'chapters'), PROSE]
    all_changed = []
    for b in bases:
        if os.path.isdir(b):
            all_changed.extend(walk_md(b))
    # Rename ch003
    old003 = os.path.join(PROSE, 'ch003-簿上无名.md')
    new003 = os.path.join(PROSE, 'ch003-塔鸣初缘.md')
    if os.path.exists(old003) and not os.path.exists(new003):
        if not dry:
            os.rename(old003, new003)
        print('RENAMED', old003, '->', new003)
    print(f'Changed {len(all_changed)} files' + (' (dry run)' if dry else ''))
    for p in sorted(all_changed)[:30]:
        print(' ', os.path.relpath(p, ROOT))
    if len(all_changed) > 30:
        print(f'  ... and {len(all_changed)-30} more')
