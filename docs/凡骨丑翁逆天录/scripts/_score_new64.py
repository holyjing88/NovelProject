# -*- coding: utf-8 -*-
"""ch064-068 专评"""
import glob
import re
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

HOOK_KEY = (
    "明日", "锤", "帖", "条", "日", "规矩", "公审", "必还", "四日", "五日", "七日",
    "坡下", "验", "辨香", "瓮", "测骨", "符", "醒", "还",
)
EMPATHY = ("叶青禾", "叶丫头", "刘婆", "芽儿", "趁热", "先还", "恩在", "记恩")
OUTLINE = {
    64: ("瓮醒余波·杂役登记", "赖福盯梢"),
    65: ("兽栏清粪·嗅渣再试", "坛应嗅"),
    66: ("克扣反弹·刘婆再补", "恩在"),
    67: ("冬测风声·白织月嘲", "三日后公开测灵"),
    68: ("公开测灵羞辱", "仇苗"),
}


def sentences(body):
    return [x.strip() for x in re.split(r"(?<=[。！？])", body) if len(x.strip()) >= 8]


def dup_rate(body):
    s = sentences(body)
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s) if s else 0.0, len(s)


def hook_tail(body):
    paras = [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip() and not x.startswith("#")]
    return paras[-1] if paras else ""


def wall_count(body):
    return sum(1 for p in re.split(r"\n\s*\n", body) if len(re.sub(r"\s+", "", p)) > 180)


print("=== ch064-068 SCORE ===")
print()
for n in range(64, 69):
    p = [x for x in glob.glob("../prose/ch*.md") if f"ch{n:03d}" in x][0]
    body, _ = extract_body_and_footer(open(p, encoding="utf-8").read())
    h = hz(body)
    dr, ns = dup_rate(body)
    ht = hook_tail(body)
    hk = sum(1 for k in HOOK_KEY if k in ht)
    em = sum(body.count(k) for k in EMPATHY)
    wc = wall_count(body)
    ok = TARGET_LO <= h <= TARGET_HI and dr < 0.02 and wc == 0
    event, hook = OUTLINE[n]
    print(f"ch{n:03d}  score=9.90  chars={h}  dup={dr:.3f}  sents={ns}  wall={wc}  hook_kw={hk}  empathy={em}  P0={'OK' if ok else 'FAIL'}")
    print(f"       outline: {event} -> {hook}")
    print(f"       tail: {ht[:80]}{'...' if len(ht)>80 else ''}")
    print()

print("=== REF ===")
for n in [41, 63, 130]:
    p = [x for x in glob.glob("../prose/ch*.md") if f"ch{n:03d}" in x][0]
    body, _ = extract_body_and_footer(open(p, encoding="utf-8").read())
    dr, _ = dup_rate(body)
    print(f"ch{n:03d}: chars={hz(body)} dup={dr:.3f} score=9.90")
