# -*- coding: utf-8 -*-
import json, os
p = os.path.join(os.path.dirname(__file__), "_churn_data.json")
d = json.load(open(p, encoding="utf-8"))
for s in d["segments"]:
    print(f"{s['lo']:02d}-{s['hi']:02d} {s['name']}: daily={s['daily']} retain={s['daily_retain']}% batch={s['batch']} bretain={s['batch_retain']}%")
hi = sorted([c for c in d["chapters"] if c["daily_risk"] > 1.5], key=lambda x: -x["daily_risk"])[:12]
print("--- high risk ---")
for c in hi:
    print(f"ch{c['n']:03d} risk={c['daily_risk']} dup={c['dup']} hook={c['hook_score']}/{c['hook_len']} dist={c['dist_pay']}")
