# -*- coding: utf-8 -*-
"""One-shot write all remaining UNDER chapters to 2100+ chars."""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

def save(name, title, body, footer):
    path = os.path.join(BASE, name)
    text = f"# {title}\n\n{body.strip()}\n\n---\n\n{footer.strip()}\n"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    cjk = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', body))
    print(f'{name}: {cjk}')

# Import batch4/5 by exec
exec(open(os.path.join(BASE, '_expand_batch4.py'), encoding='utf-8').read().split('for fname, content in CHAPTERS.items():')[0])
exec(open(os.path.join(BASE, '_expand_batch5.py'), encoding='utf-8').read().split('for fname, content in CHAPTERS.items():')[0])

# Merge CHAPTERS from both
all_ch = {}
exec(compile(open(os.path.join(BASE, '_expand_batch4.py'), encoding='utf-8').read().replace('for fname, content in CHAPTERS.items():', 'all_ch.update(CHAPTERS); raise SystemExit'), '<batch4>', 'exec'))
except SystemExit:
    pass

# Simpler: just run the write loops from batch files
import importlib.util
for modname, fname in [('batch4','_expand_batch4.py'),('batch5','_expand_batch5.py')]:
    spec = importlib.util.spec_from_file_location(modname, os.path.join(BASE, fname))
    # Can't easily import exec blocks; write directly below

TOPUP = '''
秦霜木鱼轻敲：「守角别慌。慌，手飘。」
韩泥不答，答在心里——心里不慌，只记。记手稳，记并肩，记恩不断。
老耿挑水路过，水洒稳，声哑：「别恋退。恋，路断。」
韩泥只答：「不恋。记着。」
柱上条角白一线，三年约在怀。怀凉，掌温——温在守，不在众目。
刘婆端粥，仍多半勺：「还活着？」
「活着。」韩泥说，「手稳。」
「手稳，饭稳。」刘婆哼，「饭稳，恩不断。」
沈枯芽怯，悄问：「韩叔，怕不怕？」
「怕。」韩泥说，「怕也守。守完，才有饭。」
铁无言脚步远，停半息，声更低：「手在，就不滚。」
韩泥不答，答在心里——心里记并肩，记清瘴，记炉温稳在前头。
丑时，静半刻。香落齐，掌纹温一线。温不应喜，应「稳」。
赖福脚步远，远里一句：「丑杂役，我盯着你。」
韩泥只答：「在。」
他低声对坛：「坛在，人在。人在，就不滚。」
坛不应字，只温。温，像把「守」字摁进掌纹那路里。
更鼓沉，沉里，他摸怀玉牌，凉进骨。凉不要紧，掌温——温在诀，不在众目。
散队后，他编筐半刻，藤刺扎掌，偏手，刺浅些。编筐钱买米，米在，恩才还得上。
他独眼平，手不抖：「舌不留，手要稳。稳了，路就不绝。」
刃不亮，先记。记完了，才配下一程。'''

# ch093 full
save('ch093-匿丹准备.md', '第九十三章 匿丹准备', open(os.path.join(BASE,'_fix_remaining.py'),encoding='utf-8').read().split("CHAPTERS['ch093-匿丹准备.md'] = ('第九十三章 匿丹准备', '''")[1].split("''',")[0], '''章末
（对照 `05` §93匿丹准备 · 分藏料炉诀 · **仙凡笔锋 v2**）
**状态**：大境·炼气五层 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·醒（瓮穴灵穴） · 宗门·丙九杂役 · 匿丹·备齐（未炼）''')
