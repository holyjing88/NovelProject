# -*- coding: utf-8 -*-
"""Dedupe all 30 target chapters; re-topup if below 1200."""
import re, os, subprocess

base = r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\还礼仙翁传\prose'
TARGET = 1200

FILES = [
    'ch021-魔少出丑.md','ch022-和还是战.md','ch023-赵之妒火.md','ch024-小满情报.md','ch025-卷末集结.md',
    'ch026-坊市闲逛.md','ch027-第二次妖讯.md','ch028-赵之初见.md','ch029-闪回一瞬.md','ch031-商会女修.md',
    'ch033-公平买卖.md','ch034-东脉账本.md','ch035-宗主拍桌.md','ch036-丹方残页.md','ch037-丹堂大炼.md',
    'ch039-体统.md','ch040-赤焰逼近.md','ch041-三十年.md','ch042-百宝阁二次.md','ch043-赵之谋.md',
    'ch044-误闯.md','ch045-谣言浪.md','ch046-宽恕.md','ch047-小满觉醒.md','ch049-挽月反戈.md',
    'ch050-赵罚.md','ch051-夜袭预兆.md','ch052-夜袭备战.md','ch053-杂役阵.md','ch057-周犹豫.md',
    'ch058-战后抚伤.md','ch059-赵死守.md',
]

def count_body(text):
    m = re.search(r'^#.*?\n\n(.*?)\n\n---\n\n\*（上架', text, re.S)
    body = m.group(1) if m else text
    return len(re.findall(r'[\u4e00-\u9fff]', body))

def make_ch(title, body, footer):
    return f"# {title}\n\n{body.strip()}\n\n---\n\n{footer}\n"

def parse_ch(text):
    title_m = re.search(r'^# (.+)', text)
    footer_m = re.search(r'(\*（上架[^\n]*）\*)', text)
    body_m = re.search(r'^#.*?\n\n(.*?)\n\n---\n\n\*（上架', text, re.S)
    return title_m.group(1), body_m.group(1).strip(), footer_m.group(1)

def dedupe_body(body):
    paras = [p.strip() for p in body.split('\n\n') if p.strip()]
    seen = set()
    out = []
    for p in paras:
        key = re.sub(r'\s+', '', p)
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return '\n\n'.join(out)

for fn in FILES:
    path = os.path.join(base, fn)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    title, body, footer = parse_ch(text)
    body = dedupe_body(body)
    out = make_ch(title, body, footer)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'{count_body(out):4d} {fn}')

# Re-run topup for any short
subprocess.run(['python', os.path.join(base, '_topup.py')], check=True)

print('--- final ---')
for fn in FILES:
    c = count_body(open(os.path.join(base, fn), encoding='utf-8').read())
    print(f'{c:4d} {fn}')
