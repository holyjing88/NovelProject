# -*- coding: utf-8 -*-
"""Repair ch091-092 to 2000+ chars using clean bodies + ensure_length."""
import glob
import importlib.util
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz
from _fix_prose_final import UNIQUE, expand_body

ROOT = os.path.join(os.path.dirname(__file__), "..")
PROSE = os.path.join(ROOT, "prose")

spec = importlib.util.spec_from_file_location("rw", os.path.join(ROOT, "prose", "_rewrite_v2.py"))
rw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rw)

raw_txt = open(os.path.join(ROOT, "scripts", "ch091_110_bodies.txt"), encoding="utf-8").read()

TITLES = {91: "第九十一章 废窑试炉", 92: "第九十二章 废窑再试"}


def extract(n: int) -> str:
    m = re.search(rf"===CH{n}===(.*?)===CH{n + 1}===", raw_txt, re.S)
    body = m.group(1).strip()
    body = re.split(r"\n(?=韩泥记\d+-\d+：|\d+章·第\d+笔)", body)[0].strip()
    return body


def dup(t):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)


for n in (91, 92):
    core = extract(n)
    for u in UNIQUE.get(n, []):
        if u.strip() not in core:
            core += "\n\n" + u.strip()
    body = expand_body(
        rw.dedupe_paragraphs(rw.dedupe_sentences_light(core)), n
    )
    if hz(body) < 2000:
        body = rw.ensure_length(body, n)
    path = sorted(glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md")))[0]
    _, footer = extract_body_and_footer(open(path, encoding="utf-8").read())
    content = f"# {TITLES[n]}\n\n{body.strip()}\n\n{footer.strip()}\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    b, _ = extract_body_and_footer(content)
    print(f"ch{n:03d} hz={hz(b)} dup={dup(b):.3f}")
