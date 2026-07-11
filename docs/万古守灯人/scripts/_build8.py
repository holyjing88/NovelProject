# -*- coding: utf-8 -*-
import re, pathlib

def wc(s): return len(re.sub(r'\s','',s))

src = pathlib.Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_66_78_new.py')
ns = {}
exec(src.read_text(encoding='utf-8'), ns)
CH = ns['CHAPTERS']

FIX = {
66: "塔钟未止，无人再骂。",
68: "云照夜访隔窗，经在灯里不在纸里，下半卷等你赢约再说。",
69: "承平三十八年秋，万灯大会，将至。",
70: "台下，竟有人莫名静了，像等灯幕升起。",
71: "台下，万人起立，像整座云岚宗同时屏息。",
72: "迟暮之约，至此而践，青萝三年约提前了结。",
73: "迟暮之约已践，霍照临化友，云岚宗风向变了。",
76: "云照长老步至阵前，帚一挥，陆承安话断，声不高，却压全场。执法长老色变，令锁陆承安。天煞门趁乱再扑，主峰危，云照抬头，守岁灯入她掌，七阶灯魂虚影在顶一闪，敌退三里。",
77: "孙福升管事，杂役堂改规：克扣月例者，烛火照账。有人嘀咕顾先生定规矩，顾迟年摆手：杂役堂规矩，众灯定的，不是我。姜小满侍药，沈青禾来信，程不二送补阳寿偏方，顾迟年照单全试，闻不出味，只凭姜小满点头：苦，腥，香。",
78: "霍照临献守灯堂匾额草稿，上写众灯相映。顾迟年改四字：先扫干净。霍照临大笑，仍用原字。陆承安囚敛灯崖，心腹尽捕，通敌信物搜出，实锤。顾迟年卧床养伤，仍分药给杂役，不张扬。化敌为友，不在嘴，在共扫一地渣。",
}

for i in range(66, 79):
    if i in FIX:
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
