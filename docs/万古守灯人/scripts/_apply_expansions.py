# -*- coding: utf-8 -*-
"""Apply chapter expansions 17-40 to volume 1."""
import re
from pathlib import Path

PATH = Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol01-青萝灯起.md')

CN = {
    17: '十七', 18: '十八', 19: '十九', 20: '二十', 21: '二十一', 22: '二十二',
    23: '二十三', 24: '二十四', 25: '二十五', 26: '二十六', 27: '二十七', 28: '二十八',
    29: '二十九', 30: '三十', 31: '三十一', 32: '三十二', 33: '三十三', 34: '三十四',
    35: '三十五', 36: '三十六', 37: '三十七', 38: '三十八', 39: '三十九', 40: '四十',
}

# Load chapter bodies from companion files ch17.txt ... ch40.txt if present
CHAPTERS = {}
for n in range(17, 41):
    f = PATH.parent / f'_ch{n}.txt'
    if f.exists():
        CHAPTERS[n] = f.read_text(encoding='utf-8').strip() + '\n'

def main():
    text = PATH.read_text(encoding='utf-8')
    for num, content in sorted(CHAPTERS.items()):
        cn = CN[num]
        pattern = rf'### 第{cn}章[^\n]*\n.*?(?=\n---\n\n### 第|\n---\n\n> 第二卷)'
        text, n = re.subn(pattern, content.rstrip(), text, count=1, flags=re.DOTALL)
        chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        print(f'Ch{num:02d}: replaced={n}, chars={chars}')
    PATH.write_text(text, encoding='utf-8')

if __name__ == '__main__':
    main()
