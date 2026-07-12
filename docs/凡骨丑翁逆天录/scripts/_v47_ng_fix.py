# -*- coding: utf-8 -*-
"""v47 · 嗯复读削减 + 脚注统一 v47爆款10"""
from __future__ import annotations

import glob
import os
import re

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
REPL = [
    "韩泥应声",
    "韩泥只答",
    "韩泥只点头",
    "韩泥应一声",
    "韩泥低声应",
    "韩泥不答",
]


def fix_ng(path: str) -> tuple[int, int]:
    n = int(re.search(r"ch(\d+)", path).group(1))
    raw = open(path, encoding="utf-8").read()
    cnt = raw.count("韩泥「嗯」一声")
    if cnt <= 1:
        return n, 0
    i = 0

    def sub(m):
        nonlocal i
        i += 1
        if i == 1:
            return m.group(0)
        return REPL[(i - 2) % len(REPL)]

    new = re.sub(r"韩泥「嗯」一声", sub, raw)
    if "v47爆款10" not in new and "对照" in new:
        new = new.replace("）", " · **v47爆款10**）", 1)
    if new != raw:
        open(path, "w", encoding="utf-8").write(new)
    return n, cnt - new.count("韩泥「嗯」一声")


def main():
    done = [fix_ng(p) for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md")))]
    print("FIXED", [(n, d) for n, d in done if d])


if __name__ == "__main__":
    main()
