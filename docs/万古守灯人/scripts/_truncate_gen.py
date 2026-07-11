# -*- coding: utf-8 -*-
p = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_gen_chapters.py'
lines = open(p, encoding='utf-8').read().splitlines(True)
out = []
for l in lines:
    out.append(l)
    if l.strip() == 'print(f"  {t}: {n}")':
        break
open(p, 'w', encoding='utf-8').writelines(out)
print('truncated to', len(out), 'lines')
