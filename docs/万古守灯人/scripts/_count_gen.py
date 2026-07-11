import re
from pathlib import Path
t = Path('_gen_chapters.py').read_text(encoding='utf-8')
for name in ['第二十六章 温言查案', '第二十七章 神谕真相', '第四十章 灯还亮着']:
    m = re.search(rf'add\("{re.escape(name)}", """(.*?)"""\)', t, re.S)
    if m:
        n = len(re.sub(r'\s', '', m.group(1)))
        print(name, n)
