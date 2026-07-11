# -*- coding: utf-8 -*-
import re
from pathlib import Path

text = Path('_gen_chapters.py').read_text(encoding='utf-8')
pat = re.compile(r'add\("(第.+?章 .+?)", """(.*?)"""\)', re.S)
print('| 章 | 标题 | 字数 | 状态 |')
print('|---:|------|-----:|:----:|')
for m in pat.finditer(text):
    title = m.group(1)
    body = m.group(2)
    n = len(re.sub(r'\s', '', body))
    num_m = re.search(r'第(.+?)章', title)
    ch = num_m.group(1) if num_m else '?'
    sub = title.split(' ', 1)[-1] if ' ' in title else ''
    flag = 'OK' if 3500 <= n <= 4500 else ('SHORT' if n < 3500 else 'LONG')
    print(f'| {ch} | {sub} | {n} | {flag} |')
