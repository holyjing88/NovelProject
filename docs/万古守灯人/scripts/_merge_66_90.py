# -*- coding: utf-8 -*-
"""Merge chapters 66-90 into Volume 2 markdown."""
import re
import importlib.util

FILE = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol02-云岚杂役.md'

def load_chapters(path):
    spec = importlib.util.spec_from_file_location('mod', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CHAPTERS

def count_chars(text):
    body = re.sub(r'^###[^\n]+\n+', '', text.strip())
    return len(re.sub(r'[\s\*#\-]', '', body))

# Load 79-90 from subagent file
chapters = load_chapters(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_79_90.py')

# Try load 66-78 if available
path_66_78 = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_66_78.py'
import os
if os.path.exists(path_66_78):
    chapters.update(load_chapters(path_66_78))
else:
    print('WARNING: _chapters_66_78.py not found, using _expand_66_90.py for 66-78')
    chapters.update(load_chapters(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_expand_66_90.py'))

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('### 第六十六章 第五层影')
end = content.find('**第二卷完**')
if start == -1 or end == -1:
    raise SystemExit(f'boundaries not found: {start} {end}')

new_block = '\n\n---\n\n'.join(chapters[i].strip() for i in range(66, 91))
new_content = content[:start] + new_block + '\n\n' + content[end:]

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Merged chapters 66-90')
for i in range(66, 91):
    if i in chapters:
        print(f'Ch{i}: {count_chars(chapters[i])} chars')
