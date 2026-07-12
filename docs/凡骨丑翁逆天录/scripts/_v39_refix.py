# -*- coding: utf-8 -*-
"""对非 P0 章重跑 v38_fixup（保留 ch013-016/044 P0 成果）"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import _v38_fixup as f

SKIP = {13, 14, 15, 16, 44}
thicken = f.clean_thicken_dict()
updated = 0
short = []
for path in sorted(glob.glob(os.path.join(f.PROSE, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n > 49 or n in SKIP:
        continue
    before, after, changed = f.process(path, thicken)
    if after < f.TARGET_LO:
        short.append((n, after))
    if changed:
        updated += 1
        print(f"ch{n:03d} {before}->{after}")
print(f"updated {updated}, short {len(short)}", short)
