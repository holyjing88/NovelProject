# -*- coding: utf-8 -*-
"""ch001-049 弃书风险量化"""
import glob, re, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz

PAYOFF = {3, 6, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30, 32, 34, 35, 36, 39, 40, 41, 42, 43, 44, 45, 49}
HOOK_KEY = ("明日", "锤", "帖", "条", "日", "规矩", "公审", "必还", "四日", "五日", "七日", "坡下", "验", "辨香", "瓮")

def split_sents(t):
    return [s.strip() for s in re.split(r"(?<=[。！？])", t) if len(s.strip()) >= 8]

def dup_ratio(t):
    sents = split_sents(t)
    if not sents:
        return 0.0
    seen, dup = set(), 0
    for s in sents:
        k = re.sub(r"\s+", "", s)
        if k in seen:
            dup += 1
        seen.add(k)
    return dup / len(sents)

def shorten(s, n=36):
    s = re.sub(r"\s+", "", s)
    return s[:n]

chapters = []
for p in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "prose", "ch*.md"))):
    n = int(re.search(r"ch(\d+)", p).group(1))
    if n > 49:
        continue
    t = open(p, encoding="utf-8").read()
    body, _ = extract_body_and_footer(t)
    main = re.sub(r"<!-- v38-thicken -->.*?(?=<!-- v38-topup -->|<!-- v38-end -->|\*\*状态\*\*|$)", "", body, flags=re.S)
    main = re.sub(r"<!-- v38-topup -->.*?(?=<!-- v38-end -->|\*\*状态\*\*|$)", "", main, flags=re.S)
    main = re.sub(r"<!-- v38-end -->.*?(?=\*\*状态\*\*|$)", "", main, flags=re.S)
    th_m = re.search(r"<!-- v38-thicken -->(.*?)(?=<!-- v38-topup -->|<!-- v38-end -->|\*\*状态\*\*)", body, re.S)
    th = th_m.group(1) if th_m else ""
    hk_m = re.search(r"<!-- v38-end -->\s*\n\n(.+?)(?=\n\n\*\*状态\*\*)", body, re.S)
    hk = hk_m.group(1).strip() if hk_m else ""
    nxt = min([p for p in PAYOFF if p > n], default=50)
    dist = 0 if n in PAYOFF else nxt - n
    hook_score = sum(1 for k in HOOK_KEY if k in hk)
    chapters.append({
        "n": n,
        "hz": hz(body),
        "main_hz": hz(main),
        "th_pct": round(100 * hz(th) / max(hz(body), 1)),
        "dup": round(dup_ratio(body), 3),
        "th_dup": round(dup_ratio(th), 3) if th else 0,
        "hook_len": hz(hk),
        "hook_score": hook_score,
        "payoff": n in PAYOFF,
        "dist_pay": dist,
        "hook": shorten(hk),
    })

# 风险模型
for c in chapters:
    base = 2.0
    base += c["dup"] * 12          # 章内重复
    base += c["th_dup"] * 8
    base += max(0, c["th_pct"] - 25) * 0.08  # thicken占比过高
    base += max(0, c["dist_pay"] - 3) * 0.9  # 距爽点远
    base -= 2.5 if c["payoff"] else 0
    base -= min(c["hook_score"], 4) * 0.6
    base -= 0.4 if c["hz"] >= 2000 else 0
    base -= 0.3 if c["hook_len"] >= 45 and c["hook_score"] >= 2 else 0
    daily = min(10, max(1, round(base, 1)))
    # 养书：重复跨章叠加、thicken连读更痛
    batch = min(10, max(1, round(base + c["dup"] * 4 + (0.6 if c["th_pct"] > 20 else 0), 1)))
    c["daily_risk"] = daily
    c["batch_risk"] = batch
    c["daily_retain"] = 100 if daily <= 1.05 else max(0, min(100, round(110 - daily * 10)))
    c["batch_retain"] = 100 if batch <= 1.05 else max(0, min(100, round(110 - batch * 10)))

# 分段
SEGMENTS = [
    (1, 3, "入坑·热汤锚"),
    (4, 9, "泥岗蓄压·谣辱"),
    (10, 15, "十章自检·村议"),
    (16, 23, "公审倒计时"),
    (24, 24, "公审明爽"),
    (25, 30, "余波·辞村"),
    (31, 34, "西驿·丙九入门"),
    (35, 40, "挡石·克扣忍"),
    (41, 45, "备检·嗅诀路"),
    (46, 49, "卷末·七笔坡下"),
]

segs = []
for lo, hi, name in SEGMENTS:
    sub = [c for c in chapters if lo <= c["n"] <= hi]
    segs.append({
        "name": name,
        "lo": lo, "hi": hi,
        "daily": round(sum(c["daily_risk"] for c in sub) / len(sub), 1),
        "batch": round(sum(c["batch_risk"] for c in sub) / len(sub), 1),
        "daily_retain": 100 if round(sum(c["daily_risk"] for c in sub) / len(sub), 1) <= 1.05 else max(0, min(100, round(110 - (sum(c["daily_risk"] for c in sub) / len(sub)) * 10))),
        "batch_retain": 100 if round(sum(c["batch_risk"] for c in sub) / len(sub), 1) <= 1.05 else max(0, min(100, round(110 - (sum(c["batch_risk"] for c in sub) / len(sub)) * 10))),
        "dup_avg": round(sum(c["dup"] for c in sub) / len(sub), 3),
        "dist_max": max(c["dist_pay"] for c in sub),
    })

out = {"chapters": chapters, "segments": segs}
out_path = os.path.join(os.path.dirname(__file__), "_churn_data.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"written {out_path}")
