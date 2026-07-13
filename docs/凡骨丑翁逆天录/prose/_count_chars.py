# -*- coding: utf-8 -*-
import re, os, glob

base = os.path.dirname(os.path.abspath(__file__))
print(f"{'filename':<35} {'chars':>6}  {'status':>6}")
print('-' * 52)
for i in range(69, 111):
    files = glob.glob(os.path.join(base, f'ch{i:03d}-*.md'))
    for f in sorted(files):
        with open(f, encoding='utf-8') as fh:
            text = fh.read()
        parts = text.split('---')
        body = parts[0]
        lines = body.strip().split('\n')
        if lines and lines[0].startswith('#'):
            body = '\n'.join(lines[1:]).strip()
        cjk = len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', body))
        fname = os.path.basename(f)
        num = int(fname[2:5])
        if 72 <= num <= 78:
            status = 'OK' if cjk >= 2050 else 'UNDER'
        elif num in (81, 82) or 91 <= num <= 110:
            status = 'OK' if cjk >= 2000 else 'UNDER'
        else:
            status = '-'
        print(f'{fname:<35} {cjk:>6}  {status:>6}')
