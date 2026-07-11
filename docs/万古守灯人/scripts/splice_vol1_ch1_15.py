# -*- coding: utf-8 -*-
"""Splice fully expanded vol1 chapters 1-15 into main file."""
import re
from pathlib import Path

TARGET = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol01-青萝灯起.md")
CHDATA = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_vol1_ch1_15_full.md")

def count_cjk(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))

def main():
    text = TARGET.read_text(encoding='utf-8')
    body = CHDATA.read_text(encoding='utf-8')
    
    # split header / ch16+
    m16 = re.search(r'^### 第十六章', body, re.M)
    if not m16:
        # chdata is only ch1-15
        m16_file = re.search(r'^### 第十六章', text, re.M)
        if not m16_file:
            raise SystemExit('Chapter 16 not found in target')
        header = text[:m16_file.start()]
        tail = text[m16_file.start():]
    else:
        header = text.split('### 第一章')[0]
        tail = text[re.search(r'^### 第十六章', text, re.M).start():]
    
    new_text = header.rstrip() + '\n\n' + body.strip() + '\n\n---\n\n' + tail.lstrip()
    TARGET.write_text(new_text, encoding='utf-8')
    
    parts = re.split(r'(### 第[一二三四五六七八九十百]+章[^\n]*)', body)
    total = 0
    for i in range(1, len(parts), 2):
        t = parts[i]
        b = parts[i+1] if i+1 < len(parts) else ''
        c = count_cjk(b)
        total += c
        print(f'{t}: {c}')
    print(f'TOTAL: {total}, AVG: {total//15}')

if __name__ == '__main__':
    main()
