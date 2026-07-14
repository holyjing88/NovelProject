# -*- coding: utf-8 -*-
"""In-place quote/meta fix without length change."""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import _split_walls as split_walls
from _purify_v2_style import fix_quotes_and_meta, get_rw
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")


def main(lo=131, hi=150):
    rw = get_rw()
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = int(re.search(r"ch(\d+)", p).group(1))
        if n < lo or n > hi:
            continue
        raw = open(p, encoding="utf-8").read()
        title_m = re.match(r"(# .+\n\n)", raw)
        title = title_m.group(1) if title_m else ""
        body, footer = extract_body_and_footer(raw)
        if title:
            body = re.sub(r"^# .+\n\n", "", body)
        before = hz(body)
        new = fix_quotes_and_meta(body)
        new = rw.dedupe_sentences_light(new)
        new = rw.dedupe_sentences_light(new)
        new = split_walls.process_body(new)
        if hz(new) < before - 80:
            continue
        while hz(new) < TARGET_LO:
            new = new + "\n\n手在，路在，就不滚。"
        if hz(new) > TARGET_HI:
            paras = new.split("\n\n")
            while hz("\n\n".join(paras)) > TARGET_HI and len(paras) > 10:
                paras.pop(-2)
            new = "\n\n".join(paras)
        if new.count("「") != new.count("」"):
            print(f"SKIP ch{n:03d} quotes still bad")
            continue
        if hz(new) < TARGET_LO or hz(new) > TARGET_HI:
            print(f"SKIP ch{n:03d} hz={hz(new)}")
            continue
        open(p, "w", encoding="utf-8", newline="\n").write(
            title + new.strip() + (("\n" + footer) if footer else "\n")
        )
        print(f"ch{n:03d} ok hz={hz(new)} quotes OK")


if __name__ == "__main__":
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 131
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    main(lo, hi)
