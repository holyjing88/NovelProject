# -*- coding: utf-8 -*-
import re
text = open(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_ch17_25_additions.py', encoding='utf-8').read()
for m in re.finditer(r'add\("([^"]+)"', text):
    title = m.group(1)
    start = m.end()
    rest = text[start:]
    if rest.lstrip().startswith(','):
        rest = rest.lstrip()[1:]
    body_match = re.match(r'\s*"""(.*?)"""', rest, re.DOTALL)
    if body_match:
        body = body_match.group(1)
        n = len(re.sub(r'\s', '', body))
        ok = 'OK' if 3500 <= n <= 4500 else 'SHORT' if n < 3500 else 'LONG'
        print(f'{title}: {n} [{ok}]')
