# -*- coding: utf-8 -*-
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

from _finalize_bodies import FULL_60_62


def hz(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))


for n in [61, 62]:
    b = FULL_60_62[n]
    sents = [s.strip() for s in re.split(r"[。！？\n]", b) if len(s.strip()) >= 4]
    seen = set()
    for s in sents:
        if s in seen:
            print(f"ch{n} DUP:", s)
        seen.add(s)
    print(f"ch{n} hz={hz(b)}")
