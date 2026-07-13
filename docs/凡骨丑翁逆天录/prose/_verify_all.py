# -*- coding: utf-8 -*-
import sys, re, glob, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from prose_utils import body_chars, extract_body_and_footer, hz, TARGET_LO, TARGET_HI

def dup_rate(text):
    body, _ = extract_body_and_footer(text)
    sents = [s.strip() for s in re.split(r'[。！？]', body) if len(s.strip()) >= 8]
    if not sents: return 0
    seen, dup = set(), 0
    for s in sents:
        k = re.sub(r'\s+', '', s)
        if k in seen: dup += 1
        seen.add(k)
    return dup/len(sents)

def max_para(text):
    body, _ = extract_body_and_footer(text)
    paras = [p for p in body.split('\n\n') if p.strip() and not p.startswith('#')]
    return max((hz(p) for p in paras), default=0)

chs = list(range(93,111)) + [125,128,129]
bad = []
for n in chs:
    files = glob.glob(os.path.join(os.path.dirname(__file__), f'ch{n:03d}-*.md'))
    text = open(files[0], encoding='utf-8').read()
    bc = body_chars(text)
    dr = dup_rate(text)
    mp = max_para(text)
    body, _ = extract_body_and_footer(text)
    issues = []
    if bc < TARGET_LO: issues.append(f'SHORT={bc}')
    if bc > TARGET_HI: issues.append(f'LONG={bc}')
    if dr >= 0.02: issues.append(f'dup={dr:.1%}')
    if mp > 180: issues.append(f'WALL={mp}')
    if re.search(r'下一章|这章|读者若问|第\d+章', body): issues.append('META')
    if '**状态**' not in text: issues.append('NO_STATUS')
    if issues:
        bad.append((n, bc, ', '.join(issues)))
    else:
        print(f'ch{n:03d} {bc} OK dup={dr:.1%}')
print('ISSUES:', bad)
