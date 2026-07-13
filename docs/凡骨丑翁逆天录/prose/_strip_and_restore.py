# -*- coding: utf-8 -*-
"""Strip garbage padding; restore clean chapters from _write_final."""
import re, os, glob, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
GARBAGE = re.compile(r'^\d+章·第\d+笔')

def clean_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    parts = text.split('---')
    title = parts[0].split('\n', 1)[0]
    body_lines = parts[0].split('\n')[1:]
    clean_lines = [ln for ln in body_lines if not GARBAGE.match(ln.strip())]
    body = '\n'.join(clean_lines).strip()
    body = re.sub(r'更鼓将尽，天边白一线。白里，廊下鼻下静半刻，粟壳香淡。', '', body)
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    footer = '---'.join(parts[1:]).strip()
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"{title}\n\n{body}\n\n---\n\n{footer}\n")

# restore from write_final first
subprocess.run(['python', os.path.join(BASE, '_write_final.py')], cwd=BASE, check=True)

for i in range(91, 111):
    for path in glob.glob(os.path.join(BASE, f'ch{i:03d}-*.md')):
        clean_file(path)

subprocess.run(['python', os.path.join(BASE, '_count_chars.py')], cwd=BASE)
