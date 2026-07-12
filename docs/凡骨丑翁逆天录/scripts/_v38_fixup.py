# -*- coding: utf-8 -*-
"""v38 扫尾：去元叙事 · 精简 THICKEN · 补 1500 字闸 · 重刷章末钩"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, body_chars, extract_body_and_footer, hz
from retention_data import REPLACE_PAIRS, RETENTION_END, THICKEN, THICKEN_OVERRIDE
from retention_topup import FILL, TOPUP

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
THICKEN_MARKER = "<!-- v38-thicken -->"
END_MARKER = "<!-- v38-end -->"
TOPUP_MARKER = "<!-- v38-topup -->"

BOILERPLATE = (
    "他按坛沿，只记，不飘——不飘，才还得了烫；烫在叶汤，在刘婆粥，在七笔里。",
    "丑骨末席，丙九杂役，手稳称命——命在，坛在，恩在，下一章帖谣秤香才扣得住。",
    "泥岗根在，坛沿在，还路在——还路在，手就在；手在，恩就不断。",
)

META_END = re.compile(
    r"\s*他独眼平，手不抖：钩在谣、帖、秤、香、公审、西驿、瓮温里——钩一紧，读者别走；走了，叶丫头那碗热汤就白烫。?\s*记着。?",
    re.S,
)
META_INLINE = (
    ("读者自检近一步", "十章自检近一步"),
    ("读者近答「为何还叶」", "旁人近答「为何还叶」"),
    ("立得住，读者才爽", "立得住，名节才爽"),
    ("读者能答「为何还叶」", "旁人能答「为何还叶」"),
    ("读者若问「为何还叶」", "旁人若问「为何还叶」"),
    ("读者才肯等", "名节才立得住"),
    ("读者下一章就要爽", "锤落，才是明爽"),
    ("才配五十章坡下三关", "才配坡下三关规矩"),
    ("凉了，白写", "凉了，恩就假"),
)

# 仍不足 TARGET_LO 时的通用补尾（戏内 · 不重复章末钩；v39b 下限 1500）
PAD_TAIL = (
    "他按坛沿，只记，不飘。飘了，恩断；恩不断，手就稳，稳了，明日还有活，活才能还。"
    "还远不怕，怕的是汤凉——汤在叶铺，在刘婆灶，在心里，心里那格留给烫，烫字不写，按在胃上。"
)


def chapter_num(path: str) -> int:
    m = re.search(r"ch(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else 0


def clean_thicken_text(text: str) -> str:
    text = text.strip()
    for old, new in META_INLINE:
        text = text.replace(old, new)
    # split into sentence chunks
    chunks = [c.strip() for c in re.split(r"(?<=[。！？])", text) if c.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for c in chunks:
        if c in BOILERPLATE:
            continue
        key = re.sub(r"\s+", "", c)
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return "".join(out)


def clean_thicken_dict() -> dict[int, str]:
    return {n: clean_thicken_text(t) for n, t in THICKEN.items()}


def strip_markers(body: str) -> str:
    body = re.sub(
        rf"\n*{re.escape(THICKEN_MARKER)}.*?(?=\n\n{re.escape(TOPUP_MARKER)}|\n\n{re.escape(END_MARKER)}|\n\n\*\*状态\*\*|\n\n---\n\n章末|$)",
        "",
        body,
        flags=re.S,
    )
    body = re.sub(
        rf"\n*{re.escape(TOPUP_MARKER)}.*?(?=\n\n{re.escape(END_MARKER)}|\n\n\*\*状态\*\*|\n\n---\n\n章末|$)",
        "",
        body,
        flags=re.S,
    )
    body = re.sub(
        rf"\n*{re.escape(END_MARKER)}.*?(?=\n\n\*\*状态\*\*|\n\n---\n\n章末|$)",
        "",
        body,
        flags=re.S,
    )
    for old, new in META_INLINE:
        body = body.replace(old, new)
    body = META_END.sub("", body)
    return body.rstrip()


def apply_replacements(text: str, n: int) -> str:
    for old, new, chapters in REPLACE_PAIRS:
        if n in chapters and old in text:
            text = text.replace(old, new, 1)
    return text


def insert_topup(body: str, block: str) -> str:
    block = block.strip()
    if not block:
        return body
    if TOPUP_MARKER in body:
        # 合并到已有 topup 块
        body = re.sub(
            rf"({re.escape(TOPUP_MARKER)}\n\n)(.*?)(?=\n\n{re.escape(END_MARKER)}|\n\n\*\*状态\*\*|\n\n---\n\n章末)",
            lambda m: m.group(1) + (m.group(2).rstrip() + "\n\n" + block if m.group(2).strip() else block),
            body,
            count=1,
            flags=re.S,
        )
        return body
    return insert_before_status(body, TOPUP_MARKER, block)


def ensure_length(body: str, n: int) -> str:
    """补 TOPUP/FILL 独段，不注入 PAD 套话。"""
    guard = 0
    while hz(body) < TARGET_LO and guard < 5:
        guard += 1
        if n in TOPUP and TOPUP[n] not in body:
            body = insert_topup(body, TOPUP[n])
            continue
        if n in FILL and FILL[n] not in body:
            body = insert_topup(body, FILL[n])
            continue
        break
    return body


def insert_before_status(body: str, marker: str, block: str) -> str:
    insert = f"\n\n{marker}\n\n{block.strip()}"
    if "**状态**" in body:
        return body.replace("\n\n**状态**", insert + "\n\n**状态**", 1)
    if "\n\n---\n\n章末" in body:
        return body.replace("\n\n---\n\n章末", insert + "\n\n---\n\n章末", 1)
    return body + insert


def default_status(n: int) -> str:
    if n >= 31:
        return "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠 · 宗门·丙九杂役 · 漏舍凡舍"
    return "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠 · 洞府·漏舍凡舍"


def ensure_status(body: str, n: int) -> str:
    if "**状态**" in body:
        return body
    st = default_status(n)
    if "\n\n---\n\n章末" in body:
        return body.replace("\n\n---\n\n章末", f"\n\n{st}\n\n\n---\n\n章末", 1)
    return body + f"\n\n{st}\n\n"


def apply_retention_end(body: str, n: int) -> str:
    if n not in RETENTION_END:
        return body
    end = RETENTION_END[n].strip()
    anchor = "\n\n**状态**" if "**状态**" in body else "\n\n---\n\n章末"
    if anchor not in body:
        return body
    head, tail = body.split(anchor, 1)
    paras = [p.strip() for p in re.split(r"\n\n+", head.strip()) if p.strip()]
    if paras and hz(paras[-1]) < 90 and END_MARKER not in paras[-1] and TOPUP_MARKER not in paras[-1]:
        paras = paras[:-1]
    head = "\n\n".join(paras)
    return f"{head}\n\n{END_MARKER}\n\n{end}{anchor}{tail}"


def update_footer(footer: str) -> str:
    if "v38留存" not in footer:
        footer = footer.replace("**v37正文迭代**", "**v37正文迭代** · **v38留存**")
    if "v39封顶" not in footer:
        footer = footer.replace("**v38留存**", "**v38留存** · **v39封顶**")
        if "v39封顶" not in footer:
            footer = footer.replace("**v26字闸**", "**v26字闸** · **v39封顶**")
            footer = footer.replace("**v33读者10**", "**v39封顶**")
            footer = footer.replace("**v32读者10**", "**v39封顶**")
            footer = footer.replace("**v31读者10**", "**v39封顶**")
            footer = footer.replace("**v30读者+1**", "**v39封顶**")
    footer = footer.replace("读者能答还六笔恩", "旁人能答还六笔恩")
    return footer


def process(path: str, thicken: dict[int, str]) -> tuple[int, int, bool]:
    n = chapter_num(path)
    if n < 1 or n > 49:
        return 0, 0, False
    text = open(path, encoding="utf-8").read()
    before = body_chars(text)
    text = apply_replacements(text, n)
    body, footer = extract_body_and_footer(text)
    body = strip_markers(body)

    if n in thicken and thicken[n].strip():
        block = thicken[n].strip()
        if block not in body:
            body = insert_before_status(body, THICKEN_MARKER, block)

    if n in TOPUP:
        body = insert_topup(body, TOPUP[n])

    body = ensure_length(body, n)
    body = apply_retention_end(body, n)
    body = ensure_length(body, n)
    body = ensure_status(body, n)
    footer = update_footer(footer)
    new_text = body + "\n\n" + footer if footer else body + "\n"
    after = hz(extract_body_and_footer(new_text)[0])
    changed = new_text != text
    if changed:
        open(path, "w", encoding="utf-8", newline="\n").write(new_text)
    return before, after, changed


def main() -> None:
    thicken = clean_thicken_dict()
    updated = 0
    short: list[tuple[int, int]] = []
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        before, after, changed = process(path, thicken)
        n = chapter_num(path)
        if n > 49:
            continue
        if after < TARGET_LO:
            short.append((n, after))
        if changed:
            updated += 1
            print(f"ch{n:03d} {before}->{after}")
    print(f"updated {updated}, still short {len(short)}")
    for n, c in short:
        print(f"  ch{n:03d} {c}")


if __name__ == "__main__":
    main()
