# -*- coding: utf-8 -*-
"""v44 爆款精修：去跨章套话 · 限坛温/叶汤远影 · 去 thicken 复读 · 单状态行"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, TARGET_HI, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
CHAPTERS = {n for n in range(1, 64)} | {130}
TANK_WARM_RANGE = set(range(51, 63))

# 跨章灌水套话（章内重复出现则只留首处）
BOILERPLATE = [
    "他低声道：「手稳，恩不断；恩不断，汤就不凉。」",
    "坛沿他仍擦。擦时指节白，白像证：辱在册，恩在胸，分列不混。",
    "还远不怕，怕的是汤凉——汤在叶铺，在刘婆灶，在心里。",
    "泥岗根在，坛沿在，还路在——还路在，手就在；手在，恩就不断。",
    "独眼平，像看秤——秤在，铺就不关；铺不关，汤就能还热。",
    "末席也是席，席在，手就稳——稳了，才配听帖，才配上路。",
    "恩不断，叶汤就还在前头。",
    "坛壁水汽爬半寸，敛。敛着，像替他守着。",
    "手别飘，恩不断。",
    "他是记心翁，恩仇都记在心里。",
    "舌轻，恩重。",
    "窄路也是路。",
    "克的是粮，克不走还路。",
    "腥沾袖，不贴胸。",
    "贴胸的，记在心里。",
    "秦霜远廊经过，一句：「心别邪。邪，符灭。」",
    "秦霜远廊一句：「心别邪。邪，恩断。」",
    "铁无言廊角，声低：「沿净，别拜邪。」",
    "韩泥「嗯」一声：「不拜。守沿，等缘。」",
]

SPLIT = re.compile(r"(?<=[。！？])")


def dedupe_sentences(text: str) -> str:
    chunks = [c.strip() for c in SPLIT.split(text) if c.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for c in chunks:
        key = re.sub(r"\s+", "", c)
        if len(key) < 6:
            out.append(c)
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return "".join(out)


def strip_markup_blocks(body: str) -> str:
    body = re.sub(r"<!-- v38-thicken -->.*?<!-- v38-topup -->", "", body, flags=re.S)
    body = re.sub(r"<!-- v42-topup -->", "", body)
    body = re.sub(r"<!-- v38-topup -->", "", body)
    body = re.sub(r"<!-- v38-thicken -->.*?<!-- v38-end -->", "", body, flags=re.S)
    return body


def limit_phrase(text: str, pattern: str, max_n: int) -> str:
    parts = SPLIT.split(text)
    out: list[str] = []
    count = 0
    for i, p in enumerate(parts):
        if not p.strip():
            continue
        if re.search(pattern, p):
            count += 1
            if count > max_n:
                continue
        out.append(p)
    return "".join(out)


def remove_boilerplate_dupes(body: str) -> str:
    for phrase in BOILERPLATE:
        first = True
        while phrase in body:
            if first:
                body = body.replace(phrase, phrase, 1)
                first = False
                rest = body.split(phrase, 1)
                if len(rest) > 1:
                    body = rest[0] + phrase + rest[1].replace(phrase, "")
            else:
                body = body.replace(phrase, "")
    return body


def fix_status_and_footer(raw: str) -> str:
    statuses = re.findall(r"\*\*状态\*\*：[^\n]+", raw)
    if len(statuses) > 1:
        keep = statuses[-1]
        raw = re.sub(r"\*\*状态\*\*：[^\n]+\n?", "", raw)
        if "---\n\n章末" in raw:
            raw = raw.replace("---\n\n章末", f"\n{keep}\n\n---\n\n章末", 1)
        elif "章末。" in raw:
            raw = raw.replace("章末。", f"{keep}\n\n章末。", 1)
    raw = re.sub(r" · \*\*v42起点10\*\*", "", raw)
    raw = re.sub(r"\*\*v41综合10\*\*", "", raw)
    if "对照" in raw and "v44爆款精修" not in raw:
        raw = re.sub(
            r"（对照 `05`[^）]+）",
            lambda m: m.group(0).rstrip("）") + " · **v44爆款精修**）",
            raw,
            count=1,
        )
    return raw


def process(path: str) -> tuple[int, int, int]:
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in CHAPTERS:
        return n, 0, 0

    raw = open(path, encoding="utf-8").read()
    raw = fix_status_and_footer(raw)
    body, footer = extract_body_and_footer(raw)
    before = hz(body)

    body = strip_markup_blocks(body)
    body = remove_boilerplate_dupes(body)
    body = dedupe_sentences(body)

    if n in TANK_WARM_RANGE:
        body = limit_phrase(body, r"坛腹微?温|坛温", 1)
        body = limit_phrase(body, r"叶汤远影", 1)

    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    after = hz(body)

    if after < TARGET_LO:
        # 不自动灌水；短章留给手工精修
        pass
    elif after > TARGET_HI:
        # 删末段重复句至上限内
        while hz(body) > TARGET_HI:
            paras = body.rsplit("\n\n", 1)
            if len(paras) < 2:
                break
            body = paras[0]
            if hz(body) < TARGET_LO:
                body = paras[0] + "\n\n" + paras[1]
                break

    new_raw = body + "\n\n" + footer if footer else body + "\n"
    open(path, "w", encoding="utf-8").write(new_raw)
    return n, before, hz(body)


def main():
    results = []
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        results.append(process(p))
    for n, b, a in results:
        if b != a:
            print(f"ch{n:03d}: {b} -> {a}")
    print("DONE", len(results))


if __name__ == "__main__":
    main()
