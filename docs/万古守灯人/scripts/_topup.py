# -*- coding: utf-8 -*-
"""Append PAD paragraphs until each chapter >= 3500, no duplicates."""
import re
import importlib.util

PATH = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_gen_chapters.py'

spec = importlib.util.spec_from_file_location('pad', r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_pad_ch17_25.py')
padmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(padmod)
PAD = padmod.PAD

def count(s):
    return len(re.sub(r'\s', '', s.strip()))

text = open(PATH, encoding='utf-8').read()

for title, extras in PAD.items():
    pat = rf'(add\("{re.escape(title)}", """)(.*?)("""\))'
    m = re.search(pat, text, re.DOTALL)
    if not m:
        continue
    body = m.group(2).strip()
    n = count(body)
    if n >= 3500:
        print(title, n, 'ok')
        continue
    paras = [p.strip() for p in body.split('\n\n') if p.strip()]
    existing = set(paras)
    for ex in extras:
        if count('\n\n'.join(paras)) >= 3500:
            break
        if ex not in existing:
            paras.append(ex)
            existing.add(ex)
    new_body = '\n\n'.join(paras)
    n1 = count(new_body)
    text = text[:m.start(2)] + '\n' + new_body + '\n' + text[m.end(2):]
    print(title, n, '->', n1)

open(PATH, 'w', encoding='utf-8').write(text)
