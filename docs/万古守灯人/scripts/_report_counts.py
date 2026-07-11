import re
from pathlib import Path
exec(Path('_gen_chapters.py').read_text(encoding='utf-8').split('# ========== write expanded md')[0])
for t, _, n in CHAPTERS:
    if '第二十六章' <= t.split()[0] <= '第四十章' or t.startswith('第二') or t.startswith('第三') or t.startswith('第四'):
        if any(x in t for x in ['第二十六','第二十七','第二十八','第二十九','第三十','第三十一','第三十二','第三十三','第三十四','第三十五','第三十六','第三十七','第三十八','第三十九','第四十']):
            flag = 'OK' if 3500 <= n <= 4500 else ('SHORT' if n < 3500 else 'LONG')
            print(f'{t}: {n} [{flag}]')
