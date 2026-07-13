# -*- coding: utf-8 -*-
import json
import os

path = os.path.join(os.path.dirname(__file__), "_churn_data.json")
d = json.load(open(path, encoding="utf-8"))

print("=== SEGMENTS (by daily risk desc) ===")
for s in sorted(d["segments"], key=lambda x: -x["daily"]):
    print(
        f"{s['name']:20s} ch{s['lo']:02d}-{s['hi']:03d} "
        f"daily={s['daily']} retain={s['daily_retain']} dup={s['dup_avg']} dist_max={s['dist_max']}"
    )

print("\n=== HIGH RISK (>1.05) ===")
for c in sorted(d["chapters"], key=lambda x: -x["daily_risk"]):
    if c["daily_risk"] > 1.05:
        print(
            f"ch{c['n']:03d} daily={c['daily_risk']} dup={c['dup']} "
            f"hook={c['hook_score']} payoff={c['payoff']} dist={c['dist_pay']}"
        )

print("\n=== WEAK HOOK (score<2, no payoff) ===")
for c in d["chapters"]:
    if c["hook_score"] < 2 and not c["payoff"]:
        print(f"ch{c['n']:03d} hook={c['hook_score']} dist={c['dist_pay']}")
