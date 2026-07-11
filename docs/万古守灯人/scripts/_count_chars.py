# -*- coding: utf-8 -*-
import re, sys
path = sys.argv[1]
text = open(path, encoding='utf-8').read()
for m in re.finditer(r'### (第[^\n]+)\n(.*?)(?=\n---\n|\n### |\Z)', text, re.S):
    title, body = m.group(1), m.group(2).strip()
    n = len(re.sub(r'\s', '', body))
    ok = 'OK' if 3500 <= n <= 4500 else ('LOW' if n < 3500 else 'HIGH')
    print(f"{title}: {n} [{ok}]")
