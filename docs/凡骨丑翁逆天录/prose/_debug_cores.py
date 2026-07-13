# -*- coding: utf-8 -*-
import re, sys
sys.path.insert(0, "../scripts")
from prose_utils import hz

fr = open("_fix_remaining.py", encoding="utf-8").read()
for key in ["ch093-匿丹准备.md", "ch094-门缝留灯伏笔.md"]:
    m = re.search(r"CHAPTERS\['" + re.escape(key) + r"'\] = \('[^']+', '''(.*?)''',", fr, re.S)
    print(key, hz(m.group(1)) if m else "NOT FOUND")

b4 = open("_expand_batch4.py", encoding="utf-8").read()
for m in re.finditer(r"CHAPTERS\['(ch09[^']+)'\].*?'''(.*?)''',", b4, re.S):
    print(m.group(1), hz(m.group(2)))
