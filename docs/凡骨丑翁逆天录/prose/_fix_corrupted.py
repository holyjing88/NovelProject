# -*- coding: utf-8 -*-
"""Fix corrupted ch091-092, ch106-110."""
import re, os, glob, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
POLLUTE = re.compile(r'第\d+(次|更|回|声|笔)')

def cjk(t):
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', t))

def footer_of(path):
    return '---'.join(open(path, encoding='utf-8').read().split('---')[1:]).strip()

def strip_pollution(body):
    paras = []
    for p in body.split('\n\n'):
        p = p.strip()
        if not p or POLLUTE.search(p) or re.match(r'^\d+章·第\d+笔', p):
            continue
        paras.append(p)
    return '\n\n'.join(paras)

wf = open(os.path.join(BASE, '_write_final.py'), encoding='utf-8').read()
CH091 = re.search(r"CH091 = '''(.*?)'''", wf, re.S).group(1)
CH092 = re.search(r"CH092 = '''(.*?)'''", wf, re.S).group(1)
exp_block = 'EXPAND = {' + wf.split('EXPAND = {')[1].split('\nfor num in list(EXPAND.keys())')[0]
ns = {}
exec(exp_block, ns)
EXPAND = ns['EXPAND']

for fname, title, body, num in [
    ('ch091-废窑试炉.md', '第九十一章 废窑试炉', CH091, 91),
    ('ch092-废窑再试.md', '第九十二章 废窑再试', CH092, 92),
]:
    path = os.path.join(BASE, fname)
    footer = footer_of(path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n{body.strip()}\n\n---\n\n{footer}\n")
    print(f'fixed {fname}: {cjk(body)}')

subprocess.run(['python', os.path.join(BASE, '_expand_batch5.py')], cwd=BASE, check=True)
for num in range(106, 111):
    for path in glob.glob(os.path.join(BASE, f'ch{num:03d}-*.md')):
        text = open(path, encoding='utf-8').read()
        title = text.split('\n', 1)[0].replace('# ', '')
        footer = '---'.join(text.split('---')[1:]).strip()
        body = strip_pollution('\n'.join(text.split('---')[0].split('\n')[1:]).strip())
        if num in EXPAND and EXPAND[num].strip() not in body:
            body = body + '\n\n' + EXPAND[num].strip()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n{body}\n\n---\n\n{footer}\n")
        print(f'fixed {os.path.basename(path)}: {cjk(body)}')

subprocess.run(['python', os.path.join(BASE, '_count_chars.py')], cwd=BASE)
