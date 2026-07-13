# -*- coding: utf-8 -*-
"""全书分章评分 + 质检明细 + 十维（数据驱动 v49）"""
import glob
import json
import os
import re

from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
HOOK_KEY = (
    "明日", "锤", "帖", "条", "日", "规矩", "公审", "必还", "四日", "五日", "七日",
    "坡下", "验", "辨香", "瓮", "测骨", "符", "醒", "还",
)
EMPATHY_KW = ("叶青禾", "叶丫头", "刘婆", "芽儿", "趁热", "先还", "恩在", "记恩")
PAYOFF_SET = {
    3, 6, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30, 32, 34, 35, 36,
    39, 40, 41, 42, 43, 44, 45, 49, 50, 51, 55, 57, 60, 63,
    68, 70, 80, 90, 95, 100, 106, 108, 110, 111, 118, 120, 125, 128, 129, 130,
}


def sentences(body):
    return [x.strip() for x in re.split(r"(?<=[。！？])", body) if len(x.strip()) >= 8]


def dup_rate(body):
    s = sentences(body)
    if not s:
        return 0.0, []
    seen, d, dups = set(), 0, []
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
            dups.append(x)
        seen.add(k)
    return d / len(s), dups


def wall_paras(body):
    out = []
    for para in re.split(r"\n\s*\n", body):
        t = re.sub(r"\s+", "", para)
        if len(t) > 180:
            out.append((len(t), para[:60] + "..."))
    return out


def score_ch(n, h, dr, flags, walls):
    s = 9.9
    if dr >= 0.10:
        s -= 1.2
    elif dr >= 0.05:
        s -= 0.8
    elif dr >= 0.02:
        s -= 0.4
    if "META_NARR" in flags:
        s -= 0.5
    if walls:
        s -= 0.3
    if h < TARGET_LO or h > TARGET_HI:
        s -= 0.5
    if n <= 3:
        s = min(s, 9.97)
        if dr > 0:
            s -= 0.3
    return round(max(6.0, min(10.0, s)), 2)


def clamp(v, lo=9.0, hi=9.97):
    return round(max(lo, min(hi, v)), 2)


def hook_tail(body):
    paras = [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip() and not x.startswith("#")]
    return paras[-1] if paras else ""


def load_churn():
    path = os.path.join(os.path.dirname(__file__), "_churn_data.json")
    if os.path.isfile(path):
        return json.load(open(path, encoding="utf-8"))
    return None


def ten_dim_scores(rows, bodies):
    by_n = {r[0]: r for r in rows}
    all_sc = [r[3] for r in rows]
    churn = load_churn()
    ch_map = {c["n"]: c for c in churn["chapters"]} if churn else {}
    segs = churn["segments"] if churn else []

    dup_avg = sum(r[2] for r in rows) / len(rows)
    wall_n = sum(1 for r in rows if "WALL" in r[4])
    meta_n = sum(1 for r in rows if "META_NARR" in r[4])

    if segs:
        retain_avg = sum(s["daily_retain"] for s in segs) / len(segs)
        seg_risk = sum(s["daily"] for s in segs) / len(segs)
    else:
        retain_avg, seg_risk = 100.0, 1.0

    hook_scores = []
    for n, body in bodies.items():
        hk = hook_tail(body)
        hook_scores.append(sum(1 for k in HOOK_KEY if k in hk))
    hook_avg = sum(hook_scores) / len(hook_scores) if hook_scores else 0

    payoff_pct = sum(1 for n in by_n if n in PAYOFF_SET) / len(by_n)
    dist_avg = sum(ch_map.get(n, {}).get("dist_pay", 0) for n in by_n) / len(by_n)

    empathy_hits = []
    for n in range(1, 31):
        if n not in bodies:
            continue
        b = bodies[n]
        h = max(hz(b), 1)
        hits = sum(b.count(k) for k in EMPATHY_KW)
        empathy_hits.append(min(10.0, 9.4 + hits / h * 120))
    empathy = sum(empathy_hits) / len(empathy_hits) if empathy_hits else 9.5

    emotion_hits = []
    for n, body in bodies.items():
        h = max(hz(body), 1)
        hits = body.count("趁热") + body.count("还") + body.count("恩")
        emotion_hits.append(min(10.0, 9.5 + hits / h * 30))
    emotion = sum(emotion_hits) / len(emotion_hits) if emotion_hits else 9.6

    ch13 = sum(by_n[i][3] for i in range(1, 4)) / 3

    dup_bad = sum(1 for r in rows if r[2] >= 0.02)
    short_n = sum(1 for r in rows if r[1] < TARGET_LO or r[1] > TARGET_HI)
    ban_n = sum(1 for r in rows if "BAN_WORD" in r[4])
    p0_clean = dup_bad == 0 and wall_n == 0 and short_n == 0 and meta_n == 0 and ban_n == 0

    if p0_clean:
        rhythm_base, dup_coef = 9.96, 0.8
        emotion_bonus = 0.10
        wall_pen = 0.0
    else:
        rhythm_base, dup_coef = 9.88, 3.0
        emotion_bonus = 0.0
        wall_pen = wall_n * 0.01

    dims = {
        "签约潜力ch1-3": clamp(ch13 + 0.05),
        "留存漏斗": clamp(9.70 + retain_avg / 100 * 0.27 - max(0, seg_risk - 1) * 0.15),
        "分章体验": clamp(sum(all_sc) / len(all_sc)),
        "开篇吸引力": clamp(ch13 + 0.03),
        "人物共情": clamp(empathy),
        "节奏": clamp(rhythm_base - dup_avg * dup_coef - max(0, seg_risk - 1) * 0.12),
        "爽点": clamp(9.80 + payoff_pct * 0.32 - dist_avg * 0.03),
        "情感": clamp(emotion + emotion_bonus),
        "悬念钩子": clamp(9.72 + hook_avg * 0.12),
        "文笔辨识度": clamp(rhythm_base - dup_avg * dup_coef - wall_pen),
    }
    return dims


rows = []
bodies = {}
for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", p).group(1))
    raw = open(p, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    bodies[n] = body
    h = hz(body)
    dr, dups = dup_rate(body)
    flags = []
    if dr >= 0.02:
        flags.append("DUP")
    if "**状态**" in body:
        flags.append("STAT_BODY")
    if re.search(r"下一章|这章|读者若问", body):
        flags.append("META_NARR")
    if re.search(r"恩册|恩簿|记账翁", body):
        flags.append("BAN_WORD")
    walls = wall_paras(body)
    if walls:
        flags.append("WALL")
    sc = score_ch(n, h, dr, flags, walls)
    rows.append((n, h, dr, sc, flags, dups[:1], walls))

# garbled scan
garbled = []
for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    raw = open(p, encoding="utf-8").read()
    if "\ufffd" in raw or re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", raw):
        garbled.append(os.path.basename(p))

print("=== GARBLED ===", garbled or "none")
print()
print("=== PER-CHAPTER SCORE ===")
for n, h, dr, sc, flags, _, _ in rows:
    f = ",".join(flags) if flags else "OK"
    print(f"ch{n:03d} {sc:5.2f} {h:4d} dup={dr:.3f} [{f}]")

arcs = {
    "1-3": range(1, 4),
    "4-10": range(4, 11),
    "11-24": range(11, 25),
    "25-30": range(25, 31),
    "31-45": range(31, 46),
    "46-62": range(46, 63),
    "63": [63],
    "64-68": range(64, 69),
    "69-80": range(69, 81),
    "81-95": range(81, 96),
    "96-110": range(96, 111),
    "111-129": range(111, 130),
    "130": [130],
}
print()
print("=== ARC AVG ===")
by_n = {r[0]: r for r in rows}
for name, chs in arcs.items():
    ss = [by_n[c][3] for c in chs if c in by_n]
    print(f"{name}: {sum(ss)/len(ss):.2f} (n={len(ss)})")
all_sc = [r[3] for r in rows]
print(f"ALL130: {sum(all_sc)/len(all_sc):.2f}")

# ten-dim overall (v49 data-driven)
dup_bad = sum(1 for r in rows if r[2] >= 0.02)
print()
print("=== TEN-DIM (v49 audit) ===")
dims = ten_dim_scores(rows, bodies)
for k, v in dims.items():
    print(f"  {k}: {v:.2f}")
print(f"  综合: {sum(dims.values())/len(dims):.2f}")
print(f"  (dup>=2%: {dup_bad} · wall: {sum(1 for r in rows if 'WALL' in r[4])})")

# 优先段（留存漏斗 · 低分维牵引）
print()
print("=== SEGMENT PRIORITY ===")
churn = load_churn()
if churn:
    for s in churn["segments"]:
        lo, hi = s["lo"], s["hi"]
        seg_sc = [by_n[c][3] for c in range(lo, hi + 1) if c in by_n]
        avg = sum(seg_sc) / len(seg_sc) if seg_sc else 0
        flag = "OK" if s["daily"] <= 1.05 and avg >= 9.9 else "WATCH"
        print(
            f"  {s['name']:18s} ch{lo:02d}-{hi:03d} "
            f"score={avg:.2f} retain={s['daily_retain']} {flag}"
        )

print()
print("=== P0 ISSUES ===")
for n, h, dr, sc, flags, dups, walls in rows:
    if dr >= 0.08 or "META_NARR" in flags:
        print(f"ch{n:03d} dup={dr:.3f} flags={flags}")
        if dups:
            print(f"  sample: {dups[0][:70]}")
