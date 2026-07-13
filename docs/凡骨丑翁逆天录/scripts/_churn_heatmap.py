# -*- coding: utf-8 -*-
"""ch001-129 + ch130 弃书风险量化（起点留存）"""
import glob, re, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, TARGET_IDEAL, extract_body_and_footer, hz

V42_CHAPTERS = {n for n in range(1, 130)} | {130}

PAYOFF = {
    3, 6, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30, 32, 34, 35, 36,
    39, 40, 41, 42, 43, 44, 45, 49, 50, 51, 55, 57, 60, 63,
    68, 70, 80, 90, 95, 100, 106, 108, 110, 111, 118, 120, 125, 128, 129, 130,
}
HOOK_KEY = (
    "明日", "锤", "帖", "条", "日", "规矩", "公审", "必还", "四日", "五日", "七日",
    "坡下", "验", "辨香", "瓮", "测骨", "符", "醒", "还",
)

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
    if n not in V42_CHAPTERS:
        continue
    t = open(p, encoding="utf-8").read()
    body, _ = extract_body_and_footer(t)
    main = re.sub(r"<!-- v38-thicken -->.*?(?=<!-- v38-topup -->|<!-- v42-topup -->|<!-- v38-end -->|\*\*状态\*\*|$)", "", body, flags=re.S)
    main = re.sub(r"<!-- v38-topup -->.*?(?=<!-- v42-topup -->|<!-- v38-end -->|\*\*状态\*\*|$)", "", main, flags=re.S)
    main = re.sub(r"<!-- v42-topup -->.*?(?=<!-- v38-end -->|\*\*状态\*\*|$)", "", main, flags=re.S)
    main = re.sub(r"<!-- v38-end -->.*?(?=\*\*状态\*\*|$)", "", main, flags=re.S)
    th_m = re.search(r"<!-- v38-thicken -->(.*?)(?=<!-- v38-topup -->|<!-- v42-topup -->|<!-- v38-end -->|\*\*状态\*\*)", body, re.S)
    th = th_m.group(1) if th_m else ""
    hk_m = re.search(r"<!-- v38-end -->\s*\n\n(.+?)(?=\n\n\*\*状态\*\*)", body, re.S)
    hk = hk_m.group(1).strip() if hk_m else ""
    if not hk:
        # 无 v38-end 标记时取章末前两段
        paras = [x.strip() for x in re.split(r"\n\n+", body) if x.strip() and not x.startswith("<!--")]
        hk = paras[-1] if paras else ""
    nxt = min([p for p in PAYOFF if p > n], default=131)
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

for c in chapters:
    n = c["n"]
    base = 2.0
    base += c["dup"] * 12
    base += c["th_dup"] * 8
    base += max(0, c["th_pct"] - 25) * 0.08
    if n >= 64:
        # 一部续写 arc：里程碑稀疏，dist 惩罚放宽
        base += max(0, c["dist_pay"] - 12) * 0.22
        base -= min(c["hook_score"], 4) * 0.85
        base -= 0.35 if c["hook_len"] >= 35 and c["hook_score"] >= 1 else 0
    else:
        base += max(0, c["dist_pay"] - 3) * 0.9
        base -= min(c["hook_score"], 4) * 0.6
        base -= 0.3 if c["hook_len"] >= 45 and c["hook_score"] >= 2 else 0
    base -= 2.5 if c["payoff"] else 0
    base -= 0.4 if c["hz"] >= TARGET_LO else 0
    base -= 0.5 if c["hz"] >= TARGET_IDEAL else 0
    if n >= 64 and c["hz"] >= TARGET_LO and c["dup"] < 0.02:
        base -= 1.1
    daily = min(10, max(1, round(base, 1)))
    batch = min(10, max(1, round(base + c["dup"] * 4 + (0.6 if c["th_pct"] > 20 else 0), 1)))
    c["daily_risk"] = daily
    c["batch_risk"] = batch
    c["daily_retain"] = 100 if daily <= 1.05 else max(0, min(100, round(110 - daily * 10)))
    c["batch_retain"] = 100 if batch <= 1.05 else max(0, min(100, round(110 - batch * 10)))

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
    (50, 55, "正测·商队·凡符"),
    (56, 62, "坛温加剧·钩63"),
    (63, 63, "瓮醒样板"),
    (64, 68, "瓮醒余波·冬测续"),
    (69, 80, "踹台·炼气初境"),
    (81, 95, "暗修·匿丹"),
    (96, 110, "兽潮·首炼"),
    (111, 129, "炼气后期·复测备战"),
    (130, 130, "还刘婆样板"),
]

segs = []
for lo, hi, name in SEGMENTS:
    sub = [c for c in chapters if lo <= c["n"] <= hi]
    if not sub:
        continue
    avg_daily = sum(c["daily_risk"] for c in sub) / len(sub)
    avg_batch = sum(c["batch_risk"] for c in sub) / len(sub)
    segs.append({
        "name": name,
        "lo": lo, "hi": hi,
        "daily": round(avg_daily, 1),
        "batch": round(avg_batch, 1),
        "daily_retain": 100 if avg_daily <= 1.05 else max(0, min(100, round(110 - avg_daily * 10))),
        "batch_retain": 100 if avg_batch <= 1.05 else max(0, min(100, round(110 - avg_batch * 10))),
        "dup_avg": round(sum(c["dup"] for c in sub) / len(sub), 3),
        "dist_max": max(c["dist_pay"] for c in sub),
    })

out = {"chapters": chapters, "segments": segs, "version": "v42"}
out_path = os.path.join(os.path.dirname(__file__), "_churn_data.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"written {out_path} ({len(chapters)} chapters)")
