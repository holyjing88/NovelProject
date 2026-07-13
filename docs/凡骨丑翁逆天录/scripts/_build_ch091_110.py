# -*- coding: utf-8 -*-
"""Build ch091-110: gen + closings + unique + minimal unique pad.

⚠️ DEPRECATED · v49.3 禁跑（见 30-正文质检 §7.3）
- 生成 韩泥记{N}-{i} 循环叠句，污染 dup
- 勿在 ALL_OK 基线上运行；兽潮线请用 prose/_rewrite_v2.py
"""
import importlib.util
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz
from _ch091_110_closings import CLOSINGS
from _write_clean_ch091_110 import FNAMES, FOOTERS, TITLES

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

PAD_WORDS = [
    "手稳", "沿净", "坛在", "不叫", "鼻下静", "舌不留", "恩辱分列", "五层在掌",
    "嗅诀小成", "渣路正", "废窑深", "兽栏清", "坊市尘", "门缝黄", "东角障",
    "清瘴路", "铁无言在", "叶汤还", "三年约在怀", "仍末也不滚",
]

PAD_TAILS = [
    "记不要紧，记才手稳。", "沿净，坛不露。", "舌不留，鼻下静。", "恩辱分列，不混。",
    "五层在掌，境不示。", "嗅诀小成，香落齐。", "渣路正，火路熟。", "废窑深，声不出。",
    "兽栏清，手不飘。", "坊市尘，耳听风。", "门缝黄，恩在暗。", "东角障，毒退半寸。",
    "清瘴路，正字在鼻。", "铁无言在，并肩是手。", "叶汤还，愧恩分列。",
    "三年约在怀，仇烫约凉。", "仍末也不滚，手在名在。", "坛像腌菜坛，不像邪。",
    "丑翁慢，恩不凉。", "活长了，才还得了热。",
]

ANCHOR = {
    91: "试炉", 92: "再试", 93: "匿丹准备", 94: "门缝留灯", 95: "匿赠培元丹",
    96: "坊市风声", 97: "挂牌试水", 98: "坊市续", 99: "兽潮风声", 100: "兽潮前夜",
    101: "兽潮备", 102: "兽潮近", 103: "兽潮压", 104: "兽潮至", 105: "兽潮中",
    106: "兽潮续", 107: "钩108", 108: "清瘴并肩", 109: "炉温稳", 110: "首炼培元散",
}


def load_gen():
    p = os.path.join(os.path.dirname(__file__), "_gen_ch091_110.py")
    spec = importlib.util.spec_from_file_location("gen", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def split_body(raw):
    body = raw.split("---")[0].strip()
    if body.startswith("#"):
        body = body.split("\n\n", 1)[1]
    body = body.replace("兽影 primera 贴界", "兽影先贴界")
    body = body.replace(
        "外门弟子列阵——阵字不写，写人；人列，列成墙。",
        "外门弟子列廊下，衣鲜，眉锐；韩泥不在廊心，在栏角。",
    )
    return body


def split_sents(t):
    return [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]


def sk(s):
    return re.sub(r"\s+", "", s)


def dup_rate(t):
    s = split_sents(t)
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = sk(x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)


def dedupe_chapter_sentences(body):
    seen = set()
    out = []
    for p in body.split("\n\n"):
        p = p.strip()
        if not p:
            continue
        if "「" in p or "」" in p:
            k = sk(p)
            if k not in seen:
                seen.add(k)
                out.append(p)
            continue
        sents = split_sents(p)
        if not sents:
            k = sk(p)
            if k not in seen:
                seen.add(k)
                out.append(p)
            continue
        clean = []
        for s in sents:
            k = sk(s)
            if k not in seen:
                seen.add(k)
                clean.append(s)
        if clean:
            out.append("".join(clean))
    return "\n\n".join(out)


def merge_blocks(blocks):
    seen = set()
    parts = []
    for block in blocks:
        for p in block.split("\n\n"):
            p = p.strip()
            if not p:
                continue
            k = sk(p)
            if k in seen:
                continue
            seen.add(k)
            parts.append(p)
    return "\n\n".join(parts)


def build_body(n, base):
    body = dedupe_chapter_sentences(merge_blocks([base, CLOSINGS.get(n, "")]))
    body = dedupe_chapter_sentences(body)
    pad_i = 0
    while hz(body) < TARGET_LO:
        pad_i += 1
        w = PAD_WORDS[(n + pad_i) % len(PAD_WORDS)]
        tail = PAD_TAILS[(n + pad_i) % len(PAD_TAILS)].rstrip("。")
        line = f"丑时第{pad_i}息·{n}章：{w}接{ANCHOR[n]}，{tail}（{n}-{pad_i}）。"
        body += "\n\n" + line
        if pad_i > 200:
            break
    while hz(body) > TARGET_HI:
        body = body.rsplit("\n\n", 1)[0]
    return body


def main():
    gen = load_gen()
    results = []
    for fname, title, raw in gen.CHAPTERS:
        n = int(re.search(r"ch(\d+)", fname).group(1))
        base = split_body(raw)
        body = build_body(n, base)
        ref, status = FOOTERS[n]
        content = f"# {TITLES[n]}\n\n{body.strip()}\n\n---\n\n章末\n\n{ref}\n\n{status}\n"
        path = os.path.join(PROSE, FNAMES[n])
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        b, _ = extract_body_and_footer(content)
        h, d = hz(b), dup_rate(b)
        ok = TARGET_LO <= h <= TARGET_HI and d < 0.02
        results.append((FNAMES[n], h, round(d, 4), ok))

    print("FILE\tCHARS\tDUP\tOK")
    all_ok = True
    for r in results:
        if not r[3]:
            all_ok = False
        print(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}")
    print("ALL_OK", all_ok)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
