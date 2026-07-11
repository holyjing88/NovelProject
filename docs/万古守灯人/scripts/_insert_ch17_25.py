# -*- coding: utf-8 -*-
"""Insert chapters 17-25 into _gen_chapters.py"""
import re

SRC = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_gen_chapters.py'
ADD = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_ch17_25_additions.py'

with open(SRC, encoding='utf-8') as f:
    src = f.read()
with open(ADD, encoding='utf-8') as f:
    additions = f.read()

marker = '\nprint("Chapters defined:"'
if additions.strip() in src:
    print('Already inserted')
elif marker not in src:
    raise SystemExit('marker not found')
else:
    src = src.replace(marker, '\n' + additions + marker)
    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(src)
    print('Inserted OK')
