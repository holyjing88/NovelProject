# -*- coding: utf-8 -*-
"""Merge expanded chapters 66-90 into Volume 2."""
import re
import importlib.util

FILE = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol02-云岚杂役.md'

CN_NUM = {
    66:'六十六',67:'六十七',68:'六十八',69:'六十九',70:'七十',
    71:'七十一',72:'七十二',73:'七十三',74:'七十四',75:'七十五',
    76:'七十六',77:'七十七',78:'七十八',79:'七十九',80:'八十',
    81:'八十一',82:'八十二',83:'八十三',84:'八十四',85:'八十五',
    86:'八十六',87:'八十七',88:'八十八',89:'八十九',90:'九十',
}

TITLES = {
    66:'第五层影',67:'塔六之壁',68:'灯芯初现',69:'千年灯芯',70:'炼灯进阶',
    71:'万灯大会',72:'霍照临威',73:'迟暮之约',74:'四阶对五',75:'灯影之术',
    76:'亡父一面',77:'霍照临泪',78:'化敌为友',79:'云照观战',80:'少胜一招',
    81:'小满拜师',82:'经在灯里',83:'守灯下半',84:'天煞来袭',85:'杂役殿后',
    86:'灯骨燃尽',87:'失嗅之价',88:'云照出手',89:'记名弟子',90:'灯还亮着',
}

def load_chapters(path):
    spec = importlib.util.spec_from_file_location('mod', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CHAPTERS

def count_chars(body):
    return len(re.sub(r'[\s\*#\-]', '', body))

chapters = {}
chapters.update(load_chapters(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_66_78_new.py'))
chapters.update(load_chapters(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_79_90_new.py'))

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Splice before chapter 66 (keep ch1-65)
marker = '### 第六十六章'
idx = content.find(marker)
if idx == -1:
    raise SystemExit('ch66 not found')

# Back up to preceding --- separator
sep = content.rfind('\n\n---\n\n', 0, idx)
if sep == -1:
    cut_before = idx
else:
    cut_before = sep + 2  # keep through ---

end_marker = '**第二卷完**'
end_idx = content.find(end_marker)
if end_idx == -1:
    raise SystemExit('volume end not found')

after_end = '\n\n---\n\n> 第三卷《幽灯集与枯骨岭》（第91–140章）见：`../chapters/vol03-幽灯枯骨.md`\n'

parts = []
for i in range(66, 91):
    body = chapters[i].strip()
    header = f"### 第{CN_NUM[i]}章 {TITLES[i]}"
    parts.append(header + '\n\n' + body)

new_block = '\n\n---\n\n'.join(parts)
new_content = content[:cut_before] + '\n\n---\n\n' + new_block + '\n\n' + end_marker + after_end

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Merged chapters 66-90')
for i in range(66, 91):
    body = chapters[i].strip()
    n = count_chars(body)
    status = 'OK' if 2500 <= n <= 4500 else ('SHORT' if n < 2500 else 'LONG')
    print(f'Ch{i}: {n} {status}')

filler = '围观弟子议论纷纷，声浪一层盖过一层'
print('filler count:', new_content.count(filler))
print('duplicate 第二卷完:', new_content.count('**第二卷完**'))
