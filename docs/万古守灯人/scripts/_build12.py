# -*- coding: utf-8 -*-
import re, pathlib

def wc(s): return len(re.sub(r'\s','',s))

src = pathlib.Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_chapters_66_78_new.py')
ns = {}
exec(src.read_text(encoding='utf-8'), ns)
CH = ns['CHAPTERS']

CH[76] += '\n\n' + "姜小满扑来，哭：「师父，灯还亮！」顾迟年笑，血从唇角下：「亮……就继续。」铁柱爬回，抱他：「傻子！你命比俺重要？！」顾迟年失嗅觉，只看嘴动，仍笑：「错……命是自己的……灯是共的……」"
CH[77] += '\n\n' + "霍照临来访，赠灵药，眼仍红：「我守你，守到嗅觉回来。」顾迟年拍他肩：「起来。守灯堂，要建。别跪，跪多了，心灯也矮。」霍照临笑，泪却落：「固执老头。」"

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
