# -*- coding: utf-8 -*-
"""Parse batch4/5 chapter bodies without executing."""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

def parse_full_chapters(path):
    text = open(path, encoding='utf-8').read()
    out = {}
    pat = re.compile(
        r"CHAPTERS\['(ch\d+[^']+)'\]\s*=\s*full_chapter\(\s*\"([^\"]+)\"\s*,\s*'''(.*?)'''\s*,\s*'''(.*?)'''\s*\)",
        re.S,
    )
    for m in pat.finditer(text):
        out[m.group(1)] = (m.group(2), m.group(3).strip(), m.group(4).strip())
    return out

def parse_fix_remaining():
    text = open(os.path.join(BASE, '_fix_remaining.py'), encoding='utf-8').read()
    out = {}
    for key in ['ch093-匿丹准备.md', 'ch094-门缝留灯伏笔.md']:
        m = re.search(
            r"CHAPTERS\['" + re.escape(key) + r"'\] = \('([^']+)',\s*'''(.*?)''',\s*'''(.*?)'''\)",
            text, re.S)
        if m:
            out[key] = (m.group(1), m.group(2).strip(), m.group(3).strip())
    return out

if __name__ == '__main__':
    b4 = parse_full_chapters(os.path.join(BASE, '_expand_batch4.py'))
    b5 = parse_full_chapters(os.path.join(BASE, '_expand_batch5.py'))
    fr = parse_fix_remaining()
    import re as r
    def cjk(s): return len(r.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', s))
    for k,v in sorted({**b4,**b5,**{kk:(vv[0],vv[1],vv[2]) for kk,vv in fr.items()}}.items()):
        print(k, cjk(v[1]))
