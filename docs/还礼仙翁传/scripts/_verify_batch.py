#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from prose_utils import hz, extract_body_and_footer

prose = Path(__file__).parent.parent / "prose"
names = [
    "ch028-赵之初见.md", "ch029-闪回一瞬.md", "ch030-卷终夜话.md",
    "ch031-商会女修.md", "ch032-一盒茶饼.md", "ch033-公平买卖.md",
    "ch034-东脉账本.md", "ch035-宗主拍桌.md", "ch036-丹方残页.md",
    "ch038-金丹成.md", "ch039-体统.md", "ch040-赤焰逼近.md",
    "ch041-三十年.md", "ch042-百宝阁二次.md",
]
for n in names:
    body, _ = extract_body_and_footer((prose / n).read_text(encoding="utf-8"))
    c = hz(body)
    print(f"{n}\t{c}\t{'OK' if 2000 <= c <= 2600 else ('LOW' if c < 2000 else 'HIGH')}")
