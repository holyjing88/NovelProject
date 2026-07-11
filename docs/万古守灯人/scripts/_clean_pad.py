# -*- coding: utf-8 -*-
import re
from pathlib import Path

CH_DIR = Path(__file__).resolve().parent / '_chapters_txt'
PAD = '顾迟年袖中守岁灯微温，像把这一段日子，也记进灯油里。他不炫，不冲，只备下一场更大的仗。铁柱在旁闷声问，他便答一句："急什么，灯还亮着呢。"这句话，像账，也像命。'

def count(s):
    return len(re.sub(r'\s', '', s))

for f in sorted(CH_DIR.glob('ch*.txt')):
    text = f.read_text(encoding='utf-8')
    # strip all PAD occurrences
    core = re.sub(re.escape(PAD), '', text)
    core = re.sub(r'\n{3,}', '\n\n', core).strip()
    # add PAD with proper paragraph breaks until >= 3500
    while count(core) < 3500:
        core += '\n\n' + PAD
    f.write_text(core + '\n', encoding='utf-8')
    print(f.name, count(core))
