# -*- coding: utf-8 -*-
import re
PATH = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_gen_chapters.py'
E12 = {
    "第二十二章 程不二": "青萝在望，河将灯，灯将谎；他提灯，铁柱提棍，今夜掌灯，不问价，只问镇在不在。",
    "第二十四章 百盏水灯": "他与温言再击掌，无字契，合则破；河面最后一盏无主灯漂过药铺棚，像告别，也像向万灯大会发出的第一声梆。",
    "第二十五章 灯落有冤": "顾迟年望镇口长明，晨风里稳如钉；走灯节案结，豪强线未绝，万灯大会在前——第一卷此单元，收钩在此，开钩在远。",
}
def count(s): return len(re.sub(r'\s', '', s.strip()))
text = open(PATH, encoding='utf-8').read()
for title, extra in E12.items():
    pat = rf'(add\("{re.escape(title)}", """)(.*?)("""\))'
    m = re.search(pat, text, re.DOTALL)
    if not m: continue
    body = m.group(2).strip()
    n0 = count(body)
    if n0 >= 3500:
        print(title, n0, 'ok')
        continue
    new_body = body + '\n\n' + extra.strip()
    text = text[:m.start(2)] + '\n' + new_body + '\n' + text[m.end(2):]
    print(title, n0, '->', count(new_body))
open(PATH, 'w', encoding='utf-8').write(text)
