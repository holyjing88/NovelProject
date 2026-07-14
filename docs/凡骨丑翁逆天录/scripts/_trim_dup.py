# -*- coding: utf-8 -*-
"""Trim duplicate sentences until dup < 2%."""
import glob
import importlib.util
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")


def dup_ratio(body):
    sents = [x.strip() for x in re.split(r"(?<=[。！？])", body) if len(x.strip()) >= 8]
    if not sents:
        return 0.0
    seen, d = set(), 0
    for x in sents:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(sents)


def get_rw():
    spec = importlib.util.spec_from_file_location(
        "rw", os.path.join(os.path.dirname(__file__), "..", "prose", "_rewrite_v2.py")
    )
    rw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rw)
    return rw


def main(chs):
    rw = get_rw()
    for n in chs:
        p = glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md"))[0]
        raw = open(p, encoding="utf-8").read()
        title_m = re.match(r"(# .+\n\n)", raw)
        title = title_m.group(1) if title_m else ""
        body, footer = extract_body_and_footer(raw)
        if title:
            body = re.sub(r"^# .+\n\n", "", body)
        for _ in range(8):
            dr = dup_ratio(body)
            if dr < 0.02:
                break
            nb = rw.dedupe_sentences_light(body)
            if nb == body or hz(nb) < TARGET_LO:
                break
            body = nb
        if hz(body) < TARGET_LO:
            body = body + "\n\n手在，路在，就不滚。"
        open(p, "w", encoding="utf-8", newline="\n").write(
            title + body.strip() + (("\n" + footer) if footer else "\n")
        )
        print(f"ch{n:03d} dup={dup_ratio(body):.3f} hz={hz(body)}")


if __name__ == "__main__":
    main([131, 133, 135, 141])
