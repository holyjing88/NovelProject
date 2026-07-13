# -*- coding: utf-8 -*-
"""v42/v48 起点标准校验：ch001-068 + ch130 · 2000～2500 字 · dup<2% · 无破壁"""
import glob, re, os, sys, json

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, TARGET_HI, extract_body_and_footer, hz

V42_CHAPTERS = {n for n in range(1, 69)} | {130}


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


def meta_ch(body):
    return re.findall(r"\bch0\d{2}\b", body)


short, over, high, meta, missing_status = [], [], [], [], []

for p in sorted(glob.glob(os.path.join("..", "prose", "ch*.md"))):
    n = int(re.search(r"ch(\d+)", p).group(1))
    if n not in V42_CHAPTERS:
        continue
    raw = open(p, encoding="utf-8").read()
    b, footer = extract_body_and_footer(raw)
    h, d = hz(b), dup(b)
    if h < TARGET_LO:
        short.append((n, h))
    if h > TARGET_HI:
        over.append((n, h))
    if d >= 0.02:
        high.append((n, round(d, 3), h))
    m = meta_ch(b)
    if m:
        meta.append((n, m))
    if "**状态**" not in raw:
        missing_status.append(n)

print("CHAPTERS", len(V42_CHAPTERS))
print("RANGE", f"{TARGET_LO}～{TARGET_HI}")
print("SHORT", short)
print("OVER", over)
print("HIGH_DUP", high)
print("META_CH", meta)
print("MISSING_STATUS", missing_status)

risks = []
churn_path = os.path.join(os.path.dirname(__file__), "_churn_data.json")
if os.path.isfile(churn_path):
    d = json.load(open(churn_path, encoding="utf-8"))
    risks = [c["n"] for c in d["chapters"] if c.get("daily_risk", 1) > 1.05]
print("CHURN_RISK", risks)

all_ok = (
    len(short) == 0
    and len(over) == 0
    and len(high) == 0
    and len(meta) == 0
    and len(missing_status) == 0
    and len(risks) == 0
)
print("ALL_OK", all_ok)
