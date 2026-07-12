# -*- coding: utf-8 -*-
"""Fix structure then bump hz to 1900-2100"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prose_utils import hz, extract_body_and_footer  # noqa: E402

PROSE = ROOT / "prose"
TARGET_LO, TARGET_HI = 1900, 2100

BUMP: dict[str, list[str]] = {
    "ch054-坛温起伏.md": [
        "雨歇第八日，轮换稳了，褐袍人还在。还在，像冬关将过，凡符将出。沿净，才接得住赠。",
    ],
    "ch055-凡符祛寒.md": [
        "僧影散尽后，驿亭空。空，像凡符使命落了地。",
        "符贴怀第六日，他不燃不示，沿在净。",
    ],
    "ch056-编筐季末.md": [
        "第八筐成，季末记功在。在，像窄路又宽半分。",
        "后日条贴柱，韩泥摸条，条薄，真。真在「仍末」，真在「卯时」。",
    ],
    "ch057-掌茧再裂.md": [
        "试手前夜四更，掌茧再裂，裂口渗潮。潮不是血，无血，沿便安。",
        "明日卯时，坡下见。见完试手，血线才近。近，不碰沿。",
        "药膏凡品，涂裂口，凉后稳。稳，才配明日坡下。",
        "试手前夜，手仍稳。",
    ],
    "ch058-血线将至.md": [
        "试手日清晨，坡下霜白。霜贴石阶，站要稳。稳，才验得过手。",
        "血线将至，沿仍不接。不接，才接得住瓮醒那一误。",
        "他低声：「等。」",
        "血线将至，手仍稳。",
    ],
    "ch059-沿前即止.md": [
        "沿前即止第四日，席边湿痕止于沿前三指。三指外，沿净，沿尘，沿滑。",
        "他低声：「沿前即止，血不渗沿。」",
        "冬更深，沿前即止那日，席严，沿净，手稳。",
    ],
    "ch060-血止沿前.md": [
        "六十日三更，瓮温加剧又一线。一线，不急喊醒。喊醒，像拜邪。",
        "血止沿前，不急醒。",
        "他低声：「加剧是缘，不是命。」",
    ],
    "ch061-丑时坛温.md": [
        "丑时后段，符影沿上再浮一息。一息，像凡符探路，像韩氏血未到。",
        "丑时坛温，符影半闪。半闪罢，仍等活计那一刺。",
        "更鼓尽时，席盖更严将至。",
    ],
    "ch062-席盖更严.md": [
        "瓮醒前夜二更，他加第七层破布。层厚，厚像钩。钩在沿，钩在误那一甩。",
        "席盖更严，钩瓮醒。钩在缘，钩在误那一甩。",
        "他独眼平，手不抖：「守住了，才配醒。」",
        "稳，才配瓮醒。",
    ],
}


def strip_title_from_body(body: str) -> str:
    lines = body.splitlines()
    while lines and (not lines[0].strip() or lines[0].startswith("# ")):
        lines.pop(0)
    return "\n".join(lines).strip()


def bump_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    body, footer = extract_body_and_footer(text)
    body = strip_title_from_body(body)
    title = next(l.strip() for l in text.splitlines() if l.startswith("# "))
    keys = {re.sub(r"\s+", "", p) for p in body.split("\n\n") if p.strip()}
    for block in BUMP.get(path.name, []):
        if hz(body) >= TARGET_LO:
            break
        k = re.sub(r"\s+", "", block)
        if k not in keys:
            body = body.rstrip() + "\n\n" + block
            keys.add(k)
    path.write_text(f"{title}\n\n{body.rstrip()}\n\n{footer.rstrip()}\n", encoding="utf-8")
    return hz(body)


def main() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "_fix_ch054_062.py")], check=False)
    fails = 0
    for n in range(54, 63):
        f = list(PROSE.glob(f"ch0{n}-*.md"))[0]
        h = bump_file(f)
        titles = sum(1 for l in f.read_text(encoding="utf-8").splitlines() if l.startswith("# "))
        ok = TARGET_LO <= h <= TARGET_HI and titles == 1
        print(f"ch{n:03d}: {h} titles={titles} {'OK' if ok else 'FAIL'}")
        if not ok:
            fails += 1
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
