# -*- coding: utf-8 -*-
import re, pathlib

def wc(s): return len(re.sub(r'\s','',s))

src = pathlib.Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_66_78_new.py')
ns = {}
exec(src.read_text(encoding='utf-8'), ns)
CH = ns['CHAPTERS']

FIX = {
69: "承平三十八年秋，万灯大会，将至。",
76: "亡父一面，万灯大会已照；陆承安通敌，此刻暴露；云照出手，宗门得喘。顾迟年笑，血从唇角下：「亮……就继续。」",
77: "铁柱泪如泉，却瓮声骂：「谁再让迟年哥挡幡，俺锤谁！」顾迟年轻声：「急什么，灯还亮着呢。」",
78: "顾迟年点头：「扫。扫净了，心才净。」",
}

for i in FIX:
    CH[i] = CH[i] + '\n\n' + FIX[i]

OUT = pathlib.Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_66_78_new.py')
lines = ['# -*- coding: utf-8 -*-', '"""Full expanded chapters 66-78 for Volume 2."""', '', 'CHAPTERS = {']
for i in range(66, 79):
    lines.append('    %d: """%s""",' % (i, CH[i]))
lines.append('}')
lines.append('')
OUT.write_text('\n'.join(lines), encoding='utf-8')

print('Written', OUT)
ok = short = 0
for i in range(66, 79):
    c = wc(CH[i])
    status = 'OK' if 2500 <= c <= 4500 else 'SHORT'
    if status == 'OK': ok += 1
    else: short += 1
    print('Ch%d: %d [%s]' % (i, c, status))
print('OK:%d SHORT:%d Total:%d' % (ok, short, sum(wc(CH[i]) for i in range(66,79))))
