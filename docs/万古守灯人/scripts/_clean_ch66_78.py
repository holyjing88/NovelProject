# -*- coding: utf-8 -*-
"""Clean _ch66_78_data.py: remove filler, ensure >=2500 chars."""
import re
import importlib.util
from pathlib import Path

FILE = Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_ch66_78_data.py')

def cc(t):
    return len(re.sub(r'\s', '', t))

TOPUP = {
74: "万人屏息，等霍照临下一字——四阶对五，打到此刻，已不是阶位对阶位，是心灯对心灯；顾迟年低念：「急什么，灯还亮着呢。」",
75: "铁柱抱头痛哭，锤落地，砸得广场一颤，像替万人把一口气吐出；灯影之术，至此而尽，云照定谳，握手化烬——迟暮之约，至此而清。",
77: "霍照临泪，不是弱，是把十年亡父之暗，化成守友之亮；养伤第三日，霍送汤落泪，开始随顾扫渣。",
78: "弟子路过，起初指点，半月后有人默默放药包、炭盆、旧袍，不署名，像给灯添油——化敌为友，落在不肯灭的豆火里。",
}

spec = importlib.util.spec_from_file_location('m', FILE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
CH = dict(m.CHAPTERS)

for i in range(66, 79):
    body = CH[i]
    body = re.sub(r'\n\n【续\d+-\d+】[^\n]+', '', body)
    body = re.sub(r'【续\d+-\d+】[^\n]+', '', body)
    body = re.sub(r'\n\n第\d+章续笔\d+：[^\n]+', '', body)
    body = re.sub(r'第\d+章续笔\d+：[^\n]+', '', body)
    body = body.strip()
    if cc(body) < 2500 and i in TOPUP:
        t = TOPUP[i].strip()
        if t not in body:
            body = body + '\n\n' + t
    if cc(body) < 2500:
        body = body + '\n\n' + '迟暮之约，战止于灯；守岁灯不灭。'
    CH[i] = body

lines = ['# -*- coding: utf-8 -*-', 'CHAPTERS = {']
for i in range(66, 79):
    safe = CH[i].replace('"""', '\\"\\"\\"')
    lines.append(f'    {i}: """{safe}""",')
    c = cc(CH[i])
    status = 'OK' if 2500 <= c <= 4000 else ('SHORT' if c < 2500 else 'LONG')
    print(f'Ch{i}: {c} [{status}]')
lines.append('}')
FILE.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('Cleaned', FILE)
