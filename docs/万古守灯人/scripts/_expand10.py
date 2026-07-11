# -*- coding: utf-8 -*-
import re
PATH = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_gen_chapters.py'
E10 = {
    "第二十二章 程不二": """
走灯夜至，顾迟年与铁柱分守一线，他赴废仓，铁柱守长明，像赵案时一样，信在分工，不在嘴。

程不二价目未结，他记：若活，第三份情报节上给；若死，当送终——奸商嘴毒，话却真。

袖中灯温，霍照临、陆承安、豪强，名在册，节上见。
""",
    "第二十三章 走灯节前": """
子时梆响，无主灯漂，全镇骇然。顾迟年声稳："不是鬼，是人做的！"提灯没入夜，沈青禾喊别跟，他答记着姜汤。

铁柱镇口棍横，温言岸上封河，燕不渡梆沉，里正祝词发颤——五人五线，合则破。

千盏无主灯如链，链头废仓，链尾全镇心。这一夜，豪强第一爪，赵案真尾，全在河里。
""",
    "第二十四章 百盏水灯": """
废仓取证，河面漂灯，神谕吓人，顾迟年只信一阶照惧、二阶惜用。温言拿人，他追河，里正稳民，沈青禾治伤，燕不渡断闸，铁柱守长明。

购地链霍家旁支在第三页，余孽在仓，豪强在远。半刻里，捕快扣人，逃者四，逃向镇外。

他与温言击掌："够一夜。"河尽，天明，网未收，钩已开——万灯大会的开场，藏在走灯节尾。
""",
    "第二十五章 灯落有冤": """
案破天明，河灯灭，谎破。顾迟年拒牌，只允看长明。沈青禾第三碗姜汤还，温言押余孽，购地链递，回文未知。

铁柱臂伤笑长明在，沈青禾说节后再说。二阶代价累，三阶不碰，留灯三策刻骨。

"赢一夜，赢一世还早。"陆承安记仇，霍照临记名，万灯在前——走灯节单元收钩，长明如钉，下一卷开。
""",
}
def count(s): return len(re.sub(r'\s', '', s.strip()))
text = open(PATH, encoding='utf-8').read()
for title, extra in E10.items():
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
