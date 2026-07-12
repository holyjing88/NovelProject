# -*- coding: utf-8 -*-
"""v47 精修：嗯≤1 · 去重末段 · 链式短句改钩 · 补字至1780+ · 脚注v47"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, TARGET_HI, extract_body_and_footer, hz
from v47_topup_data import HOOKS, TOPUP

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
TARGET_CH = {2} | set(range(4, 31)) - {18, 24}
IDEAL_LO = 1780
IDEAL_HI = 1950
END_MARK = "\n\n---\n\n章末"
SPLIT = re.compile(r"(?<=[。！？])")
EN_RE = re.compile(r"韩泥[「\"]?嗯[」\"]?(?:一声|声)?(?:[，,][^：:]*?)?[：:]?")
ALT_EN = ["应声", "只答", "只点头", "不接话", "只道"]
DEFAULT_STATUS = (
    "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · "
    "鸿蒙九劫瓮·眠 · 洞府·漏舍凡舍"
)


def fix_en_count(body: str) -> str:
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        full = m.group(0)
        if count == 0:
            count += 1
            return full
        alt = ALT_EN[(count - 1) % len(ALT_EN)]
        count += 1
        # preserve dialogue after colon
        if "：" in full or ":" in full:
            tail = full.split("：", 1)[-1].split(":", 1)[-1]
            if tail and tail != full:
                prefix = full[: full.rfind(tail)]
                return prefix.replace("韩泥「嗯」一声", f"韩泥{alt}").replace(
                    "韩泥「嗯」声", f"韩泥{alt}"
                ).replace("韩泥「嗯」", f"韩泥{alt}")
        return full.replace("韩泥「嗯」一声", f"韩泥{alt}").replace(
            "韩泥「嗯」声", f"韩泥{alt}"
        ).replace("韩泥「嗯」", f"韩泥{alt}")

    body = EN_RE.sub(repl, body)
    # standalone 「嗯。」
    if count > 1:
        body = re.sub(r"(?<=[。！？\n])「嗯。」", "「好。」", body, count=count - 1)
    return body


def dedupe_body(body: str) -> str:
    paras = body.split("\n\n")
    out_paras: list[str] = []
    global_seen: set[str] = set()
    for para in paras:
        if para.strip().startswith("#"):
            out_paras.append(para)
            continue
        chunks = [c.strip() for c in SPLIT.split(para) if c.strip()]
        kept = []
        for c in chunks:
            key = re.sub(r"\s+", "", c)
            if len(key) >= 8 and key in global_seen:
                continue
            global_seen.add(key)
            kept.append(c)
        if kept:
            out_paras.append("".join(kept))
    return "\n\n".join(out_paras)


def trim_chain_ending(body: str, n: int) -> str:
    """Replace only the last paragraph if it is chain-short-sentence padding."""
    hook = HOOKS.get(n)
    if not hook:
        return body
    if END_MARK in body:
        head, tail = body.split(END_MARK, 1)
    else:
        head, tail = body, ""
    paras = [p for p in head.split("\n\n") if p.strip()]
    if not paras:
        return body
    last = paras[-1]
    sents = [s.strip() for s in SPLIT.split(last) if s.strip()]
    is_chain = len(sents) >= 2 and all(
        len(re.sub(r"\s+", "", s)) <= 28 for s in sents
    )
    if is_chain and hook not in last:
        paras[-1] = hook
    elif hook not in "".join(paras[-2:]):
        paras.append(hook)
    head = "\n\n".join(paras)
    return head + (END_MARK + tail if END_MARK in body else "")


def insert_before_end(body: str, block: str) -> str:
    block = block.strip()
    if not block or block in body:
        return body
    if END_MARK in body:
        head, tail = body.split(END_MARK, 1)
        return head.rstrip() + "\n\n" + block + END_MARK + tail
    return body.rstrip() + "\n\n" + block


def fix_footer(footer: str, n: int) -> str:
    if not footer.strip():
        footer = f"\n\n---\n\n章末\n\n（对照 `05` §{n} · **v47爆款10**）\n\n{DEFAULT_STATUS}\n"
    if "v47爆款10" not in footer:
        footer = footer.replace("）", " · **v47爆款10**）", 1)
    # ensure status in footer only
    if "**状态**" not in footer:
        footer = footer.rstrip() + "\n\n" + DEFAULT_STATUS + "\n"
    return footer


def remove_status_from_body(body: str) -> str:
    return re.sub(r"\n?\*\*状态\*\*：[^\n]+\n?", "", body)


def process(path: str) -> tuple[int, int, int, int]:
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in TARGET_CH:
        return n, 0, 0, 0

    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    before = hz(body)

    body = remove_status_from_body(body)
    body = fix_en_count(body)
    body = dedupe_body(body)
    body = trim_chain_ending(body, n)
    body = dedupe_body(body)

    # topup to ideal range
    blocks = list(TOPUP.get(n, []))
    bi = 0
    guard = 0
    while hz(body) < IDEAL_LO and guard < 15:
        guard += 1
        if bi < len(blocks):
            body = insert_before_end(body, blocks[bi])
            bi += 1
            body = dedupe_body(body)
            continue
        break

    # trim if over ideal (keep above TARGET_LO)
    if hz(body) > IDEAL_HI:
        while hz(body) > IDEAL_HI and "\n\n" in body:
            paras = body.rsplit("\n\n", 1)
            if len(paras) < 2:
                break
            trial = paras[0]
            if hz(trial) < TARGET_LO:
                break
            body = trial

    footer = fix_footer(footer, n)
    out = body + footer
    open(path, "w", encoding="utf-8").write(out)
    after = hz(body)
    en = len(re.findall(r"韩泥[「\"]?嗯", body))
    return n, before, after, en


def main():
    results = []
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        r = process(p)
        if r[1] or r[2]:
            results.append(r)
    for n, b, a, en in results:
        flag = []
        if a < IDEAL_LO:
            flag.append("LOW")
        if a > IDEAL_HI:
            flag.append("HIGH")
        if en > 1:
            flag.append(f"en={en}")
        print(f"ch{n:03d}: {b}->{a} {' '.join(flag) if flag else 'OK'}")
    print("DONE", len(results))


if __name__ == "__main__":
    main()
