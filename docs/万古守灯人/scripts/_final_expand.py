# -*- coding: utf-8 -*-
"""Final pass: append supplement files _supNN.txt to chapters."""
import re
from pathlib import Path

PATH = Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol01-青萝灯起.md')
DOC = PATH.parent
CN = {n: {16:'十六',17:'十七',18:'十八',19:'十九',20:'二十',21:'二十一',22:'二十二',
         23:'二十三',24:'二十四',25:'二十五',26:'二十六',27:'二十七',28:'二十八',
         29:'二十九',30:'三十',31:'三十一',32:'三十二',33:'三十三',34:'三十四',
         35:'三十五',36:'三十六',37:'三十七',38:'三十八',39:'三十九',40:'四十'}[n]
      for n in range(16,41)}

def main():
    text = PATH.read_text(encoding='utf-8')
    for num in range(16, 41):
        sf = DOC / f'_sup{num}.txt'
        if not sf.exists():
            continue
        sup = sf.read_text(encoding='utf-8').strip()
        cn = CN[num]
        pattern = rf'(### 第{cn}章[^\n]*\n.*?)(\n---\n)'
        m = re.search(pattern, text, flags=re.DOTALL)
        if not m:
            print(f'Ch{num}: skip')
            continue
        body = m.group(1)
        if sup in body:
            print(f'Ch{num}: already')
            continue
        body = body + '\n' + sup
        text = text[:m.start()] + body + m.group(2) + text[m.end():]
        chars = len(re.findall(r'[\u4e00-\u9fff]', body))
        print(f'Ch{num}: now {chars}')
    PATH.write_text(text, encoding='utf-8')

if __name__ == '__main__':
    main()
