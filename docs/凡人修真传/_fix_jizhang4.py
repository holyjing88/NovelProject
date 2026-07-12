# -*- coding: utf-8 -*-
"""Pass 4: 记账/册隐喻 → 记在心里"""
import re
from pathlib import Path

ROOT = Path(__file__).parent / "prose" / "vol01"

REPL = [
    ("不能先把账算死", "不能把路封死"),
    ("按心口，按指：", "按心口，默念："),
    ("他试按指，想写「路」字", "他心口试念「路」字"),
    ("不按指，却同样不能乱记", "只默记心里，却同样不能乱记"),
    ("添头他心领，不按指", "添头他心领，只记心里"),
    ("未成，不按指", "未成，不念于口"),
    ("他默想，不按指，只念恩八行", "他默想，不写心外，只念恩八行"),
    ("他默想，不按指，只按恩", "他默想，不写心外，只念恩"),
    ("债未成实，实不收指——指，留给还的日", "恩未成实，实不落心——心，留给还的日"),
    ("记，按指，指印红，红如恩血，恩不写字，记，等还", "帖边按指印，印红；恩记在骨，不在纸，记，等还"),
    ("字浮，沉，阳温顶格", "二字入心，沉，阳温顶格"),
    ("他试写「山」字", "他心口试念「山」字"),
    ("他又试写「滚石」二字，血仍干", "他又心口试念「滚石」二字，念不出"),
    ("不在恩席", "不进恩念"),
    ("不进恩席", "不进恩念"),
    ("交易不进恩席", "交易不进恩念"),
    ("情不进恩席", "情不进恩念"),
    ("兄弟不进恩席", "兄弟不进恩念"),
    ("不抢恩席", "不抢恩念"),
    ("留在刘婆，留给必还。还，要台", "留给刘婆，留给必还。还，要台"),  # no-op guard
    ("他按仇格，仇格冷", "他按心口，心里仇处冷"),
    ("陈寻按仇格，仍无字", "陈寻按心口，仇仍无字"),
    ("他指腹蹭过仇，仇格冷", "他指腹蹭过心口，心里仇处冷"),
    ("仇格冷，像另一本从未落字的仇格", "心里仇处冷，像一处从未落字的仇"),
    ("仇格仍空", "心里仇处仍空"),
    ("己路，不抢恩席。席，留给", "己路，不抢恩念。念，留给"),
    ("像有人在里面翻页，翻得很轻", "像心过一巡，巡得很轻"),
    ("舌会乱，心不乱，翻的是页，页里八笔仍温", "舌会乱，心不乱，心过一巡，八笔仍温"),
    ("仇格，泼水痕淡", "心里仇处，泼水痕淡"),
    ("计恩席", "计恩念"),
    ("兄弟本就不该落进恩席", "兄弟本就不该落进恩念"),
    ("兄弟不进恩席，却在人身旁", "兄弟不进恩念，却在人身旁"),
    ("兄弟不进恩席，誓不进字", "兄弟不进恩念，誓不进字"),
    ("他不进恩席", "他不进恩念"),
]

changed = []
for fp in sorted(ROOT.glob("*.md")):
    text = fp.read_text(encoding="utf-8")
    orig = text
    for old, new in REPL:
        text = text.replace(old, new)
    if text != orig:
        fp.write_text(text, encoding="utf-8")
        changed.append(fp.name)

print(f"Pass4 changed {len(changed)}")
for n in changed:
    print(n)

# report remain
pat = re.compile(
    r"记账|账本|账簿|恩账|阳账|旧账|还账|活账|不按指|恩席|仇格|"
    r"邪册|破册|怀册|沉册|蘸血|账算|实不收指|试写.*血|按指.*恩血"
)
for fp in sorted(ROOT.glob("*.md")):
    for i, line in enumerate(fp.read_text(encoding="utf-8").splitlines(), 1):
        if pat.search(line) and "按指" not in line or (
            "按指" in line and pat.search(line) and "身契" not in line and "玉牌" not in line
            and "侧廊" not in line and "排队" not in line and "执事" not in line
            and "自检" not in line
        ):
            if pat.search(line):
                print(f"REMAIN {fp.name}:{i} {line[:80]}")
