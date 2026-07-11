# -*- coding: utf-8 -*-
"""Remove duplicate paragraphs in chapter bodies in _gen_chapters.py"""
import re

PATH = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_gen_chapters.py'

text = open(PATH, encoding='utf-8').read()

def dedupe_body(body):
    paras = [p.strip() for p in body.strip().split('\n\n') if p.strip()]
    seen = []
    for p in paras:
        if p not in seen:
            seen.append(p)
    return '\n\n'.join(seen)

def count(s):
    return len(re.sub(r'\s', '', s.strip()))

for m in list(re.finditer(r'add\("([^"]+)", """(.*?)"""', text, re.DOTALL)):
    title = m.group(1)
    if not title.startswith('第'):
        continue
    body = m.group(2)
    new_body = dedupe_body(body)
    if new_body != body.strip():
        n0 = count(body)
        n1 = count(new_body)
        text = text.replace(f'add("{title}", """{body}"""', f'add("{title}", """\n{new_body}\n"""', 1)
        print(f'{title}: {n0} -> {n1}')

open(PATH, 'w', encoding='utf-8').write(text)
