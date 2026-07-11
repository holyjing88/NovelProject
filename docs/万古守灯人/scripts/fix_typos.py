# -*- coding: utf-8 -*-
"""Fix English typos and duplicate markers in 万古守灯人 chapter files."""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')

REPLACEMENTS = [
    ('unofficial 守灯使', '非正式守灯使'),
    (' unofficial ', ' 非正式 '),
    (' nightly ', ' 每夜 '),
    ('unfinished', '未竟'),
    (' blind time', ''),
    ('— blind time', ''),
    ('fear', '惧意'),
    (' deepest', ' 最深'),
    ('deepest', '最深'),
    (' largely spent', ' 大半耗尽'),
    ('Enough to darken a town', '足以让整个镇子陷入黑暗'),
    ('heroism alone', '单凭英雄气概'),
    ('Chief', '首席'),
    ('chief', '首席'),
]

DUP_PREFIXES = [
    '章末，第',
    '更鼓远传，玄京云开一线',
    '风过承平门，顾迟年',
    '青萝镇口长明与皇城气运',
    '裴无妄虚影远观，不插手',
]


def remove_dup_lines(text, prefixes):
    lines = text.split('\n')
    out = []
    removed = 0
    for line in lines:
        s = line.strip()
        if any(s.startswith(p) for p in prefixes) and len(s) > 60:
            removed += 1
            continue
        out.append(line)
    return '\n'.join(out), removed


def main():
    total_repl = 0
    total_dup = 0
    for fp in glob.glob(os.path.join(DOCS, '05-万古守灯人-分章正文-*.md')):
        if '目录' in fp:
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            t = f.read()
        orig = t
        for a, b in REPLACEMENTS:
            if a in t:
                t = t.replace(a, b)
        t, r = remove_dup_lines(t, DUP_PREFIXES)
        total_dup += r
        if t != orig:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(t)
            print(f'Fixed: {os.path.basename(fp)} (dup lines: {r})')
            total_repl += 1
    print(f'Files updated: {total_repl}, duplicate lines removed: {total_dup}')


if __name__ == '__main__':
    main()
