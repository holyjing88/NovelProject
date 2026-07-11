# -*- coding: utf-8 -*-
"""Apply expanded chapters 66-78 to Volume 2 markdown."""
import re
from pathlib import Path
from _ch66_78_data import CHAPTERS

FILE = Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol02-云岚杂役.md')

TITLES = {
    66: '第五层影', 67: '塔六之壁', 68: '灯芯初现', 69: '千年灯芯',
    70: '炼灯进阶', 71: '万灯大会', 72: '霍照临威', 73: '迟暮之约',
    74: '四阶对五', 75: '灯影之术', 76: '亡父一面', 77: '霍照临泪', 78: '化敌为友',
}

CN = {
    66: '六十六', 67: '六十七', 68: '六十八', 69: '六十九', 70: '七十',
    71: '七十一', 72: '七十二', 73: '七十三', 74: '七十四', 75: '七十五',
    76: '七十六', 77: '七十七', 78: '七十八',
}


def count_chars(text):
    return len(re.sub(r'\s', '', text))


def dedupe(text):
    paras = [p.strip() for p in text.split('\n\n') if p.strip()]
    seen, out = set(), []
    for p in paras:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return '\n\n'.join(out)


def format_chapter(num, body):
    return f'### 第{CN[num]}章 {TITLES[num]}\n\n{body.strip()}'


def main():
    content = FILE.read_text(encoding='utf-8')
    start = content.find('### 第六十六章')
    end = content.find('### 第七十九章')
    if start == -1 or end == -1:
        raise SystemExit(f'boundaries not found: start={start}, end={end}')

    block_parts = []
    for i in range(66, 79):
        body = CHAPTERS[i].strip()
        block_parts.append(format_chapter(i, body))
        block_parts.append('\n\n---\n\n')
    new_block = ''.join(block_parts).rstrip('\n\n---\n\n') + '\n\n'

    new_content = content[:start] + new_block + content[end:]
    FILE.write_text(new_content, encoding='utf-8')

    print('Applied chapters 66-78 to', FILE)
    for i in range(66, 79):
        c = count_chars(CHAPTERS[i])
        status = 'OK' if 2500 <= c <= 4000 else ('SHORT' if c < 2500 else 'LONG')
        print(f'Ch{i}: {c} chars [{status}]')


if __name__ == '__main__':
    main()
