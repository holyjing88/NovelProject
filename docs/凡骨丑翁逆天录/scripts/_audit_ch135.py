# -*- coding: utf-8 -*-
import glob
import re
import sys

sys.path.insert(0, ".")
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

p = glob.glob("../prose/ch135-*.md")[0]
raw = open(p, encoding="utf-8").read()
body, _ = extract_body_and_footer(raw)
body = re.sub(r"^# .+\n\n", "", body)

sents = [x.strip() for x in re.split(r"(?<=[。！？])", body) if len(x.strip()) >= 8]
seen = {}
dups = []
for i, x in enumerate(sents):
    k = re.sub(r"\s+", "", x)
    if k in seen:
        dups.append((seen[k], i, x))
    else:
        seen[k] = i

print("HZ", hz(body), f"({TARGET_LO}-{TARGET_HI})")
print("DUP", len(dups))
for a, b, x in dups:
    print(f"  [{a}] vs [{b}]", x[:72])

print("LONG_PARAS")
for i, para in enumerate(body.split("\n\n")):
    t = re.sub(r"\s+", "", para)
    if len(t) > 180:
        print(f"  #{i+1} len={len(t)}")

print("QUOTES", body.count("「") == body.count("」"))
print("META", re.findall(r"ch\d{3}|135才写|才写「", body))
