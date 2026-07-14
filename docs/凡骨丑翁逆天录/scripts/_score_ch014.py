# -*- coding: utf-8 -*-
import re
import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz, TARGET_LO, TARGET_HI

spec = importlib.util.spec_from_file_location(
    "sf", os.path.join(os.path.dirname(__file__), "_score_full.py")
)
# Avoid executing module main by loading only functions - parse manually
import ast

src = open("_score_full.py", encoding="utf-8").read()
# execute only defs by cutting at "rows = []"
cut = src.split("\nrows = []")[0]
ns = {}
exec(compile(cut, "_score_full.py", "exec"), ns)

raw = open("../prose/ch014-村议.md", encoding="utf-8").read()
body, footer = extract_body_and_footer(raw)
h = hz(body)
dr, dups = ns["dup_rate"](body)
walls = ns["wall_paras"](body)
flags = []
if dr >= 0.02:
    flags.append("DUP")
if walls:
    flags.append("WALL")
if re.search(r"下一章|这章|读者若问", body):
    flags.append("META_NARR")
sc = ns["score_ch"](14, h, dr, flags, walls, body=body, footer=footer)
hk = ns["hook_tail"](body)
hook_n = sum(1 for k in ns["HOOK_KEY"] if k in hk)
print(f"hz={h} ok={TARGET_LO<=h<=TARGET_HI} need={max(0,TARGET_LO-h)}")
print(f"dup={dr:.3f} walls={len(walls)} flags={flags or ['OK']}")
print(f"quotes={body.count('「')} hook_hits={hook_n} vernacular={'通俗笔锋' in footer}")
print(f"score={sc:.2f}")
print("tail:", hk[:80])
if dups:
    print("dups", dups[:3])
