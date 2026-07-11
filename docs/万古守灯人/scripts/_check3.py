# -*- coding: utf-8 -*-
import ast
with open(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_bulk_expand.py', encoding='utf-8') as f:
    src = f.read()
# extract EXPAND dict source
start = src.index('EXPAND = {')
end = src.index('\n}\n\n\n# Read file')
exp_src = src[start:end+2]
for n in range(66, 91):
    if f'{n}:' not in exp_src:
        print('missing', n)
try:
    ast.parse(exp_src)
    print('EXPAND dict parses OK')
except SyntaxError as e:
    print('SyntaxError', e.lineno, e.msg)
    lines = exp_src.splitlines()
    for i in range(max(0,e.lineno-3), min(len(lines), e.lineno+2)):
        print(i+1, lines[i][:100])
