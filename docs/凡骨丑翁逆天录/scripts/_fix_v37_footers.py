# -*- coding: utf-8 -*-
import glob
import os
import re

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    m = re.search(r"ch(\d+)", os.path.basename(path))
    if not m or int(m.group(1)) > 49:
        continue
    lines = open(path, encoding="utf-8").read().splitlines()
    changed = False
    for i, line in enumerate(lines):
        if not line.startswith("（对照 `05`"):
            continue
        new = line
        new = new.replace("（对照 `05` · `17` §二 §", "（对照 `05` §")
        for tag in (
            " · v20坛腹微温",
            " · v20心记",
            " · v24",
            " · v28精修",
            " · v30读者+1",
            " · v31读者10",
            " · v32读者10",
            " · v33读者10",
            " · v35留存",
            " · **v26字闸2500～3000**",
        ):
            new = new.replace(tag, "")
        if "`17` §二" not in new:
            mm = re.match(r"（对照 `05` §([^·]+) · (.+)", new)
            if mm:
                new = f"（对照 `05` §{mm.group(1)} · `17` §二 · {mm.group(2)}"
        if "**v37正文迭代**" not in new:
            new = new.rstrip("）") + " · **v37正文迭代**）"
        if new != line:
            lines[i] = new
            changed = True
    if changed:
        open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
        print("fixed", os.path.basename(path))
