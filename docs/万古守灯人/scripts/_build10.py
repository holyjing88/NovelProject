# -*- coding: utf-8 -*-
import re, pathlib

def wc(s): return len(re.sub(r'\s','',s))

src = pathlib.Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_66_78_new.py')
ns = {}
exec(src.read_text(encoding='utf-8'), ns)
CH = ns['CHAPTERS']

FIX = {
69: "焚灯塔顶残灯，似遥遥应和。备战第十日，云岚宗张灯结彩，各峰弟子议论纷纷，阶位清清楚楚：霍照临五阶灯影，顾迟年四阶灯盏半边，陆承安四阶灯盏。",
73: "霍照临笑，眼仍红：「固执老头。」「急什么，」顾迟年道，「灯还亮着呢。」",
76: "云照长老抬头，守岁灯自顾迟年怀中起，入她掌——千年灯芯之力，借她一瞬，七阶灯魂虚影在顶一闪！敌退三里，宗门得喘。围观震场，阶位清清楚楚：七阶灯魂借千年灯芯，六阶灯骨强燃余温，五阶灯影锁敌，四阶灯盏照证。",
77: "云照坐榻边：「灯骨强燃，五感失嗅觉，或一年，或永。阳寿再折三年。」顾迟年笑：「不说我也知道少。够活到下一场就行。」霍照临请命守崖，冷面如铁。陆承安囚敛灯崖，隔崖传话，无人听见，只见口型冷笑。",
78: "夜风紧，顾迟年望主峰：「天煞门未绝，陆承安未判，不能睡。」霍照临道：「我守夜。」顾迟年笑：「你也睡。灯要轮着亮。」化敌为友，霍扫丹渣，守灯堂将起；顾迟年仍是杂役，扫渣挑水，不少一件。",
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
