# -*- coding: utf-8 -*-
import json, os
p = os.path.join(os.path.dirname(__file__), "_churn_data.json")
d = json.load(open(p, encoding="utf-8"))
for c in d["chapters"]:
    print(
        f"ch{c['n']:03d}\tdaily={c['daily_risk']}\tbatch={c['batch_risk']}\t"
        f"dr={c['daily_retain']}\tbr={c['batch_retain']}\tdup={c['dup']}\thook={c['hook_score']}"
    )
print("---SEG---")
for s in d["segments"]:
    print(f"{s['lo']}-{s['hi']}\t{s['name']}\tdaily={s['daily']}\tbatch={s['batch']}")
