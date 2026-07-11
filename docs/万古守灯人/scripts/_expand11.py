# -*- coding: utf-8 -*-
import re
PATH = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_gen_chapters.py'
E11 = {
    "第二十二章 程不二": "顾迟年提灯下山，像赵案那日，像堂上那日，像每一次灯在险处——节上，掌灯。",
    "第二十三章 走灯节前": "他逆岸而行，袖中灯灼，跳在全镇最大的谎上；废仓在前，长明在后，姜汤在沈青禾棚里还热。",
    "第二十四章 百盏水灯": "河面百盏水灯仍漂，他知：这一夜赢不全，赢一半也是赢；合则破，破则镇在，镇在则灯在。",
    "第二十五章 灯落有冤": "回宗路，风如梆，他袖中灯温，像走灯节收钩，也像万灯大会开钩——霍家线将浮，长明如钉。",
}
def count(s): return len(re.sub(r'\s', '', s.strip()))
text = open(PATH, encoding='utf-8').read()
for title, extra in E11.items():
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
