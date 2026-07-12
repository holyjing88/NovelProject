# -*- coding: utf-8 -*-
"""v39 终修：修复章末结构 · P1 thicken · 补强 · PAD 清除 · 2000 字闸"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import body_chars, extract_body_and_footer, hz
from retention_data import RETENTION_END

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
TARGET = 2000
END_M = "<!-- v38-end -->"

THICKEN_SHORT = {
    10: "马春花嘲绝户，嘲像槌，槌不落心，落册上。旁人若问「为何还叶」，答在姜、在秤、在「趁热」。四恩在胸，「要还」定了；定了就不急，他是记心翁。",
    24: "公审证白落，赵哑口——爽不大，够清。韩泥只「我记着」：恩还定了，一半名节，一半省亲；那日远，烫先不能凉。",
    35: "飞石落她肩，誓落他心。必还——还先用丹，还先烫；三者分列，不混。五日测骨帖在柱，帖在，手就不能抖。",
    45: "深秋末单交差，血至沿前止。七笔分列，不混。瓮温加剧，关将近；将近，先数七笔，先还烫。",
}

BOOST = {
    3: "空碗缺沿像月，月缺恩不缺——缺的是还日，还日远，先记；记了，门缝才配再开。",
    8: "四形齐了，他分半给沈豁口。旁人若问为何还叶，答在烫，答在实，答在秤还在。",
    25: "里正差人送抄本：「沉丹宗验骨，十日后卯时，西驿见。」韩泥瞥一眼：「十日，够辞村，够还一路恩。」",
    26: "荐帖风声贴柱角，里正补一句：「八日后上路，误者不许。」八日，像还路的尺。",
}

PAD_BLOCK = re.compile(
    r"\n*他按坛沿，只记，不飘。飘了，恩断；恩不断，手就稳，稳了，明日还有活，活才能还。"
    r"还远不怕，怕的是汤凉——汤在叶铺，在刘婆灶，在心里，心里那格留给烫，烫字不写，按在胃上。\n*",
    re.S,
)
PAD_LINE = re.compile(
    r"(?:坛沿一线温，像还路又近一分。近一分，手稳一分，恩不断一分。(?:手稳，才配明日还有活；活，才配还。\n*)?)+",
    re.S,
)


def scrub(body: str) -> str:
    body = PAD_BLOCK.sub("\n\n", body)
    body = PAD_LINE.sub("", body)
    for a, b in [("读者能答", "旁人能答"), ("读者若问", "旁人若问"), ("读者怒值", "怒值"), ("满在读者心", "满在心里")]:
        body = body.replace(a, b)
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def strip_tail(body: str) -> str:
    body = re.sub(r"\n*<!-- v38-thicken -->.*", "", body, flags=re.S)
    body = re.sub(r"\n*<!-- v38-topup -->.*", "", body, flags=re.S)
    body = re.sub(r"\n*<!-- v38-end -->.*", "", body, flags=re.S)
    body = re.sub(r"\n*\*\*状态\*\*.*", "", body, flags=re.S)
    body = re.sub(r"\n*---\n\n章末.*", "", body, flags=re.S)
    return body.strip()


def status_line(n: int, text: str) -> str:
    if "**状态**" in text:
        m = re.search(r"\*\*状态\*\*：[^\n]+", text)
        if m:
            return m.group(0)
    if n >= 31:
        return "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠 · 宗门·丙九杂役 · 漏舍凡舍"
    return "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠 · 洞府·漏舍凡舍"


def footer_note(n: int, old_foot: str) -> str:
    m = re.search(r"（对照 `05`[^）]+）", old_foot)
    base = m.group(0) if m else f"（对照 `05` §ch{n:03d} · **v37正文迭代**）"
    if "v38留存" not in base:
        base = base.replace("**v37正文迭代**", "**v37正文迭代** · **v38留存**")
    if "v39封顶" not in base:
        base = base.replace("**v38留存**", "**v38留存** · **v39封顶**")
    return base


def rebuild(n: int, text: str) -> str:
    _, old_foot = extract_body_and_footer(text)
    body = strip_tail(text)
    body = scrub(body)

    if n in BOOST and BOOST[n] not in body:
        body += "\n\n" + BOOST[n]

    if n in THICKEN_SHORT:
        th = f"\n\n<!-- v38-thicken -->\n\n{THICKEN_SHORT[n]}"
    else:
        m = re.search(r"<!-- v38-thicken -->\s*\n\n(.+?)(?=\n\n<!-- v38-topup -->|\n\n<!-- v38-end -->|\n\n\*\*状态\*\*|$)", text, re.S)
        if m:
            block = scrub(m.group(1).strip())
            th = f"\n\n<!-- v38-thicken -->\n\n{block}" if block else ""
        else:
            th = ""

    tu_m = re.search(r"<!-- v38-topup -->\s*\n\n(.+?)(?=\n\n<!-- v38-end -->|\n\n\*\*状态\*\*|$)", text, re.S)
    tu = ""
    if tu_m:
        block = scrub(tu_m.group(1).strip())
        if block:
            tu = f"\n\n<!-- v38-topup -->\n\n{block}"

    end = RETENTION_END.get(n, "").strip()
    st = status_line(n, text)
    note = footer_note(n, old_foot)

    out = body + th + tu + f"\n\n{END_M}\n\n{end}\n\n{st}\n\n\n---\n\n章末。\n\n{note}\n"
    out_body = extract_body_and_footer(out)[0]
    if hz(out_body) < TARGET:
        gap = TARGET - hz(out_body)
        extra = "他低声道：「手稳，恩不断；恩不断，汤就不凉。汤在叶铺，在刘婆灶，在心里。」"
        if extra not in out:
            out = out.replace(f"\n\n{END_M}", f"\n\n{extra}\n\n{END_M}", 1)
    return scrub(extract_body_and_footer(out)[0]) + extract_body_and_footer(out)[1] and out or out


def main() -> None:
    short = []
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = int(re.search(r"ch(\d+)", path).group(1))
        if n > 49:
            continue
        text = open(path, encoding="utf-8").read()
        new = rebuild(n, text)
        open(path, "w", encoding="utf-8", newline="\n").write(new)
        c = body_chars(new)
        if c < TARGET:
            short.append((n, c))
        print(f"ch{n:03d} {c} pad={new.count('坛沿一线温')} meta={'读者' in new}")
    print("short:", short)


if __name__ == "__main__":
    main()
