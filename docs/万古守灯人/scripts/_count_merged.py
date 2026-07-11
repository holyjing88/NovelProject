import re
from _make_ch_txt import BASE
from chapter_ext import EXT
from _build_long_chapters import (
    S26, S27, S28, S29, S30, S31, S32, S33, S34,
    S35, S36, S37, S38, S39, S40,
)
from _ch27_40_exp import ALL as EXP_EXTRA

SS = {26: S26, 27: S27, 28: S28, 29: S29, 30: S30, 31: S31, 32: S32,
      33: S33, 34: S34, 35: S35, 36: S36, 37: S37, 38: S38, 39: S39, 40: S40}

def count(s):
    return len(re.sub(r'\s', '', s))

def norm(p):
    return re.sub(r'\s+', '', p)

def merged(num):
    paras = list(BASE.get(num, [])) + list(EXT.get(num, [])) + list(SS[num])
    if num >= 26:
        paras += EXP_EXTRA.get(num, [])
    seen = set()
    unique = []
    for p in paras:
        k = norm(p)
        if len(k) < 20 or k in seen:
            continue
        seen.add(k)
        unique.append(p)
    return '\n\n'.join(unique)

for n in range(26, 41):
    b = merged(n)
    c = count(b)
    flag = 'OK' if c >= 3500 else 'SHORT'
    print(f'ch{n}: {c} [{flag}]')
