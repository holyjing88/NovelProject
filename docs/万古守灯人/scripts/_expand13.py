# -*- coding: utf-8 -*-
import re
PATH = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_gen_chapters.py'
E = {
    "第二十四章 百盏水灯": "半刻里，镇静了半分，像谎被戳了一个洞，洞后仍是夜。",
    "第二十五章 灯落有冤": "他收袖，灯温，像把走灯节这一夜，正式关进第一卷的章末。",
}
def count(s): return len(re.sub(r'\s', '', s.strip()))
text = open(PATH, encoding='utf-8').read()
for title, extra in E.items():
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
