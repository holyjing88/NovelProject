# -*- coding: utf-8 -*-
import re
path = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol01-青萝灯起.md'
text = open(path, encoding='utf-8').read()
idx = text.find('### 第十六章')
text = text[idx:]
for m in re.finditer(r'### (第[^\n]+)\n(.*?)(?=\n---\n|\Z)', text, re.S):
    title, body = m.group(1), m.group(2).strip()
    if '第一卷完' in body:
        body = body.split('**第一卷完**')[0].strip()
    n = len(re.sub(r'\s', '', body))
    ok = 'OK' if 3500 <= n <= 4500 else ('LOW' if n < 3500 else 'HIGH')
    print(f'{title}: {n} [{ok}]')
