# -*- coding: utf-8 -*-
"""v39 留存封顶：全局 PAD 清除 · thicken 精简 · 分段补强 · 2000 字闸"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _v38_fixup import (
    END_MARKER,
    TARGET_LO,
    THICKEN_MARKER,
    TOPUP_MARKER,
    apply_replacements,
    apply_retention_end,
    clean_thicken_dict,
    clean_thicken_text,
    ensure_length,
    insert_before_status,
    insert_topup,
    strip_markers,
    update_footer,
)
from prose_utils import body_chars, extract_body_and_footer, hz
from retention_data import THICKEN
from retention_topup import TOPUP

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

PAD_BLOCK = re.compile(
    r"\n*他按坛沿，只记，不飘。飘了，恩断；恩不断，手就稳，稳了，明日还有活，活才能还。"
    r"还远不怕，怕的是汤凉——汤在叶铺，在刘婆灶，在心里，心里那格留给烫，烫字不写，按在胃上。\n*",
    re.S,
)
PAD_LINE = re.compile(
    r"(?:坛沿一线温，像还路又近一分。近一分，手稳一分，恩不断一分。手稳，才配明日还有活；活，才配还。\n*)+",
    re.S,
)
META_FIX = (
    ("满在读者心，也在他心里", "满在心里，也在他心里"),
    ("读者怒值才值得", "怒值才值得"),
    ("读者能答", "旁人能答"),
    ("读者若问", "旁人若问"),
)

# 精简 thicken（覆盖 retention_data 冗长块）
THICKEN_OVERRIDE: dict[int, str] = {
    10: (
        "马春花嘲绝户，嘲像槌，槌不落心，落册上。册上两字，杀不死擦沿的手。"
        "旁人若问「为何还叶」，答在姜、在秤、在「趁热」——答不出文，答得出手。"
        "四恩在胸，「要还」定了；定了就不急，急像少年，他是记心翁。"
    ),
    24: (
        "公审证白落，赵哑口——爽不大，够清。叶证白像锤，锤在人心，不在舌。"
        "韩泥只「我记着」：恩还定了，一半名节，一半省亲那日；那日远，烫先不能凉。"
    ),
    35: (
        "飞石落她肩，誓落他心。必还——还先用丹，还先烫；三者分列，不混。"
        "五日测骨帖在柱，帖在，手就不能抖。符影一闪敛，敛像证：不求名，求还烫。"
    ),
    45: (
        "深秋末单交差，血至沿前止。七笔分列，不混——混，坡下站不住。"
        "瓮温加剧，关将近；将近，先数七笔，先还烫。"
    ),
}

# 戏内补强（热力图弱段 · 仅正文没有的信息）
BOOST: dict[int, str] = {
    13: "村人念帖，念到「卯时」便住——住，像怕念实了，锤就真落。韩泥不劝，只编筐：筐结实，才撑得到第三日坐末席。",
    14: "卖盐老汉愿帮一句，帮的是理，不是帮晦气。祠堂阶下，有人抄帖，抄得慢，慢里却实。",
    25: "里正差人送抄本，抄本上写：「沉丹宗验骨，十日后卯时，西驿见。」韩泥瞥一眼，独眼平：「十日，够辞村，够还一路恩。」",
    26: "荐帖风声贴柱角，角起，像门缝光。里正补一句：「八日后上路，误者不许。」八日，像还路的尺。",
    44: "坛腹微温一丝，应「静」字，不应慌。慌像少年，他是记心翁——翁慢，恩不凉；凉不得，叶汤还在前头等着。",
}


def scrub_pad(body: str) -> str:
    body = PAD_BLOCK.sub("\n\n", body)
    body = PAD_LINE.sub("", body)
    for old, new in META_FIX:
        body = body.replace(old, new)
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def dedupe_paragraphs(body: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", body) if p.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for p in paras:
        if p.startswith("<!--"):
            out.append(p)
            continue
        key = re.sub(r"\s+", "", p)
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return "\n\n".join(out)


def get_thicken(n: int) -> str:
    raw = THICKEN_OVERRIDE.get(n, THICKEN.get(n, ""))
    return clean_thicken_text(raw) if raw else ""


def process(path: str) -> tuple[int, int, bool]:
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n < 1 or n > 49:
        return 0, 0, False
    text = open(path, encoding="utf-8").read()
    before = body_chars(text)
    text = apply_replacements(text, n)
    body, footer = extract_body_and_footer(text)
    body = strip_markers(body)
    body = scrub_pad(body)
    body = dedupe_paragraphs(body)

    if n in BOOST and BOOST[n] not in body:
        # 插入末段叙事前
        anchor = "\n\n<!-- v38-thicken -->"
        if anchor in body:
            body = body.replace(anchor, "\n\n" + BOOST[n] + anchor, 1)
        elif "\n\n**状态**" in body:
            body = body.replace("\n\n**状态**", "\n\n" + BOOST[n] + "\n\n**状态**", 1)
        else:
            body = body + "\n\n" + BOOST[n]

    block = get_thicken(n)
    if block and block not in body:
        body = insert_before_status(body, THICKEN_MARKER, block)

    if n in TOPUP:
        body = insert_topup(body, TOPUP[n])

    body = ensure_length(body, n)
    body = apply_retention_end(body, n)
    body = scrub_pad(body)
    footer = update_footer(footer)
    new_text = body + "\n\n" + footer if footer else body + "\n"
    after = hz(extract_body_and_footer(new_text)[0])
    changed = new_text != text
    if changed:
        open(path, "w", encoding="utf-8", newline="\n").write(new_text)
    return before, after, changed


def main() -> None:
    updated = 0
    short = []
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        before, after, changed = process(path)
        n = int(re.search(r"ch(\d+)", path).group(1))
        if n > 49:
            continue
        if after < TARGET_LO:
            short.append((n, after))
        if changed:
            updated += 1
            print(f"ch{n:03d} {before}->{after}")
    print(f"updated {updated}, short {len(short)}")
    for n, c in short:
        print(f"  ch{n:03d} {c}")


if __name__ == "__main__":
    main()
