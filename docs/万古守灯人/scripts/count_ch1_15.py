import re
from pathlib import Path
p = Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol01-青萝灯起.md')
t = p.read_text(encoding='utf-8')
ls = t.splitlines()
st = [(i, l.strip()) for i, l in enumerate(ls) if l.startswith('### 第')]
tot = 0
for idx in range(15):
    s = st[idx][0]
    e = st[idx+1][0]
    c = len(re.findall(r'[\u4e00-\u9fff]', '\n'.join(ls[s+1:e])))
    tot += c
    print(f'{st[idx][1]}: {c}')
print('TOTAL:', tot)
print('AVG:', tot // 15)
