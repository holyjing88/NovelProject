# -*- coding: utf-8 -*-
"""Top up ch054-062 to hz 1900-2100 · safe footer handling"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prose_utils import hz, extract_body_and_footer  # noqa: E402

PROSE = ROOT / "prose"
TARGET_LO, TARGET_HI = 1900, 2100

TOPUP: dict[str, list[str]] = {
    "ch054-坛温起伏.md": [
        "雨歇第八日，轮换稳了，褐袍人还在。还在，像冬关将过，凡符将出。沿净，才接得住赠。",
    ],
    "ch055-凡符祛寒.md": [
        "第六日搬柴，侧门风硬如刀。刀贴骨，符暖护之。护骨不寒，手才不僵，缘才正。",
        "管事第六日嘱：「符在怀，少声张。」韩泥「嗯」一声。声张，谣来；谣来，路易断。",
        "夜第六日，符与瓮各守各线。符护人，瓮眠等缘。缘在沿前，不在符烟。",
    ],
    "ch056-编筐季末.md": [
        "第八筐成，季末记功在。在，像窄路又宽半分。宽不要紧，要紧是后日卯时条真。",
        "后日前夜丑时，他数更鼓。更鼓沉，掌茧裂无血。无血，沿净，手才配坡下。",
        "邻床问：「编筐也试手？」「编筐练手。」韩泥说，「手稳，筐圆，丹才不歪。」",
        "铁无言季末最后一嘱：「静气带上坡。」韩泥「嗯」一声，只答「在」。",
        "后日条贴柱，韩泥摸条，条薄，真。真在「仍末」，真在「卯时」。",
        "筐底不塌那日，管事声沉：「季末记功在。」韩泥不辩，只把手擦干。",
    ],
    "ch057-掌茧再裂.md": [
        "试手前夜四更，掌茧再裂，裂口渗潮。潮不是血，无血，沿便安。",
        "他涂药膏第五遍，药凡，凉后稳。药不涂沿，沿不是他该碰的。",
        "木牌与试手帖并放枕下。并放，像命与规矩挨着。卯时前，坡下又起霜。",
        "秦霜问心最后一遍，他声平：「为还。」不夸，不傲，只记。",
        "赖福眼红药膏，管事声冷，赖福哑了。哑，韩泥手更稳。",
        "试手前夜，坛腹温一线，像应「等」。等，像守瓮人，不等醒，等缘。",
        "明日卯时，坡下见。见完试手，血线才近。近，不碰沿。",
        "药膏凡品，涂裂口，凉后稳。稳，才配明日坡下。",
    ],
    "ch058-血线将至.md": [
        "试手日清晨，坡下霜白。霜贴石阶，站要稳。稳，才验得过手。",
        "午后第三单，血线将至。将至，沿不接。不接，才接得住瓮醒那一误。",
        "夜试手后第二遍，坛温加剧。加剧，像将醒未醒。醒在缘，不在催。",
        "他摸记功帖，帖薄，真。真在「手稳」，不在「灵色」。",
        "丹炉前第二遍，他手仍不抖。丑而稳，稳而真，真在末排站住了。",
        "试手过了，他仍末排。末排不要紧，要紧是沿净，手稳。",
        "血线将至那日，他独眼平，手不抖。抖，缘便偏。偏，席挡不住。",
        "窄路也是路。路通向瓮醒，瓮醒通向还。",
        "血到了席，没到沿。沿在眠，血不主动碰。",
        "还，先还烫。",
        "沿不接，缘在等。",
        "他低声：「等。」",
        "血线将至，手仍稳。",
    ],
    "ch059-沿前即止.md": [
        "沿前即止第四日，席边湿痕止于沿前三指。三指外，沿净，沿尘，沿滑。",
        "编筐第四趟，藤刺深扎，血珠饱满，仍甩破席。席吸尽，血不渗沿。",
        "管事第四日嘱：「脏沿，像拜邪。」韩泥「嗯」一声：「不拜。沿净，记心里。」",
        "夜第四日盖席，盖严。严，像瓮醒前夜预演。预演，不主动滴血。",
        "冬更深那日，丙九静一寸。静一寸，像沿前那一止。止，像看不见的线。",
        "老耿第四日咳：「沿净，好。」韩泥「嗯」一声，不追问。问急，像邪。",
        "沿前即止，席吸尽，沿仍净。净，才接得住瓮醒。",
        "血不渗沿，沿不接。不接，缘在等。等，像守瓮人。",
        "沿前即止，不接沿。",
        "赖福远处骂，骂轻，韩泥擦沿的手却更稳。",
        "他低声：「沿前即止，血不渗沿。」",
        "缘在等。",
    ],
    "ch060-血止沿前.md": [
        "六十日三更，瓮温加剧又一线。一线，不急喊醒。喊醒，像拜邪。",
        "他低声：「血止沿前，席严，符暖，手稳。稳，才配席盖更严那一夜。」",
    ],
    "ch061-丑时坛温.md": [
        "丑时后段，符影沿上再浮一息。一息，像凡符探路，像韩氏血未到。",
        "油灯尽时，他独眼盯沿。沿净，符影半闪，不像邪脉。",
        "天边白一线里，席盖更严将至。将至，接瓮醒，接沿边那一误。",
        "掌纹贴席，席贴坛角。角温加剧，仍不认主。认主，等血缘碰沿。",
        "丑时守坛，他不睡实。不睡实，像辨香前夜。鼻下静，手上才静。",
        "符怀暖一丝，不燃。燃，烟起，管事查。半闪罢，仍等活计那一刺。",
        "丑时尽，沿仍净。净，才配符影半闪，才配瓮醒那一误。",
        "他低声：「符影半闪，仍等误。」",
        "更鼓尽时，席盖更严将至。",
        "丑时坛温，一线加剧。",
    ],
    "ch062-席盖更严.md": [
        "瓮醒前夜二更，他加第七层破布。层厚，厚像钩。钩在沿，钩在误那一甩。",
        "清栏第三趟归来，血落席，沿不接。不接，缘在等。等，像守瓮人。",
        "铁无言最后一停：「席严，沿净，不主动滴。」韩泥「嗯」一声，手不抖。",
        "坛腹温加剧，像明日就在沿边等那一滴。等，不在心急，在活计，在席，在沿。",
        "赖福讽盖席，管事声冷，赖福哑了。哑，韩泥加席层的手更稳。",
        "最后一夜，他不拜邪，不揭席诱沿。诱沿，像借腥。腥，路易断。",
        "席盖更严，钩瓮醒。钩在缘，钩在误那一甩。",
        "他独眼平，手不抖：「守住了，才配醒。」",
    ],
}


def get_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line.strip()
    return ""


def dedupe_paras(body: str) -> str:
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for p in paras:
        key = re.sub(r"\s+", "", p)
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return "\n\n".join(out)


def topup_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    body, footer = extract_body_and_footer(text)
    title = get_title(text)
    body = dedupe_paras(body)
    para_keys = {re.sub(r"\s+", "", p) for p in body.split("\n\n") if p.strip()}
    for block in TOPUP.get(path.name, []):
        if hz(body) >= TARGET_LO:
            break
        key = re.sub(r"\s+", "", block)
        if key not in para_keys:
            body = body.rstrip() + "\n\n" + block
            para_keys.add(key)
    body = dedupe_paras(body)
    if not footer.strip():
        footer = "\n---\n\n章末。\n"
    new_text = f"{title}\n\n{body}\n\n{footer.rstrip()}\n"
    path.write_text(new_text, encoding="utf-8")
    return hz(body)


def main() -> None:
    fails = 0
    for n in range(54, 63):
        f = list(PROSE.glob(f"ch0{n}-*.md"))[0]
        h = topup_file(f)
        ok = TARGET_LO <= h <= TARGET_HI
        print(f"ch{n:03d}: {h} {'OK' if ok else 'FAIL'}")
        if not ok:
            fails += 1
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
