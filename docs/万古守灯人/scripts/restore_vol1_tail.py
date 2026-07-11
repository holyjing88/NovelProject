# -*- coding: utf-8 -*-
"""Splice expanded ch1-15 and restore original ch16-40 tail."""
import re
from pathlib import Path

TARGET = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol01-青萝灯起.md")
EXPANDED = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_vol1_ch1_15_full.md")
TAIL = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_vol1_ch16_40_original.md")

def count_cjk(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))

def main():
    text = TARGET.read_text(encoding='utf-8')
    expanded = EXPANDED.read_text(encoding='utf-8').strip()
    tail = TAIL.read_text(encoding='utf-8').strip()

    header = text[:re.search(r'^### 第一章', text, re.M).start()].rstrip()
    new_text = header + '\n\n' + expanded + '\n\n---\n\n' + tail + '\n'
    TARGET.write_text(new_text, encoding='utf-8')

    parts = re.split(r'(### 第[一二三四五六七八九十百]+章[^\n]*)', expanded)
    total = 0
    for i in range(1, len(parts), 2):
        if i + 1 >= len(parts):
            break
        c = count_cjk(parts[i + 1])
        total += c
        print(f"{parts[i]}: {c}")
    print(f"TOTAL ch1-15: {total}")
    print("Ch16 restored:", "赵元青罚银后怀恨" in new_text)
    print("Vol1 end:", "第一卷完" in new_text)

if __name__ == '__main__':
    main()
