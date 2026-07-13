# -*- coding: utf-8 -*-
"""Strip 更残第/丑时第; refill via ensure_length (仙凡 v2 templates, no 更残第).

✅ v49.3 · 模板净化（见 30 §7.3）
- 保留原有叙事核，只删机械「更残第N息」句
- 不足 2000 字时用 chapter_expansions + 仙凡模板池补字
"""
import glob
import importlib.util
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz
from late_expansions import LATE, LATE2, FINAL, TOPUP

ROOT = os.path.join(os.path.dirname(__file__), "..")
PROSE = os.path.join(ROOT, "prose")

spec = importlib.util.spec_from_file_location("rw", os.path.join(ROOT, "prose", "_rewrite_v2.py"))
rw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rw)

FILLER_RE = re.compile(r"(丑时第|更残第)\d+息")
PURGE_CH = [125, 128, 129]  # ch091–110 已由 fix_ch091_110 净化，勿重跑

LATE_META = {
    125: (
        "第一百二十五章 窑炉稳",
        "ch125-窑炉稳.md",
        "章末\n\n（对照 `05` §125备战七日封窑稳温 · 炼气十二层圆满 · **仙凡笔锋 v2**）\n\n**状态**：大境·炼气十二层 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·醒（瓮穴灵穴） · 宗门·丙九杂役 · 药山废窑 · 契·三年约玉牌",
    ),
    128: (
        "第一百二十八章 十二层圆",
        "ch128-十二层圆.md",
        "章末\n\n（对照 `05` §128试台验丹正 · 炼气十二层圆满 · 钩129备战帖 · **仙凡笔锋 v2**）\n\n**状态**：大境·炼气十二层（十三将至） · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·醒（瓮穴灵穴） · 宗门·外门复测试台 · 契·三年约玉牌",
    ),
    129: (
        "第一百二十九章 备战帖",
        "ch129-备战帖.md",
        "章末\n\n（对照 `05` §129备战收官 · 大比帖将至 · 钩130还刘婆夺魁 · **仙凡笔锋 v2**）\n\n**状态**：大境·炼气十二层（明日十三） · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·醒（瓮穴灵穴） · 宗门·外门复测末项前夜 · 契·三年约玉牌",
    ),
}


def count_fillers(text: str) -> int:
    return len(FILLER_RE.findall(text))


def dup(t):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)


def strip_filler_lines(body: str) -> str:
    out_paras = []
    for para in re.split(r"\n\s*\n", body):
        lines = [ln for ln in para.splitlines() if ln.strip() and not FILLER_RE.search(ln)]
        if lines:
            out_paras.append("\n".join(lines).strip())
    return "\n\n".join(out_paras)


def sentence_keys(text: str):
    keys = set()
    for sent in re.split(r"(?<=[。！？])", text):
        s = sent.strip()
        if len(s) < 8:
            continue
        keys.add(re.sub(r"\s+", "", s))
    return keys


def filter_new_block(block: str, seen: set) -> str:
    out = []
    for full in re.split(r"(?<=[。！？])", block):
        s = full.strip()
        if not s:
            continue
        k = re.sub(r"\s+", "", s)
        if len(s) >= 8 and k in seen:
            continue
        seen.add(k)
        out.append(full)
    return "".join(out).strip()


def merge_late_body(core: str, n: int) -> str:
    seen = sentence_keys(core)
    body = core
    for block in (LATE.get(n, ""), LATE2.get(n, ""), FINAL.get(n, "")):
        block = block.strip()
        if not block:
            continue
        add = filter_new_block(block, seen)
        if add:
            body = body + "\n\n" + add if body else add
    body = rw.dedupe_paragraphs(rw.dedupe_sentences_light(rw.strip_pollution(body)))
    if hz(body) < TARGET_LO:
        body = rw.ensure_length(body, n)
        body = rw.dedupe_sentences_light(body)
    topup = TOPUP.get(n, "").strip()
    if topup and hz(body) < TARGET_LO:
        seen = sentence_keys(body)
        add = filter_new_block(topup, seen)
        if add:
            body = body + "\n\n" + add
    return body


def rebuild_late_chapter(n: int) -> tuple:
    """Rebuild ch125/128/129 from clean cores + late_expansions (not polluted disk)."""
    title, fname, footer = LATE_META[n]
    key = fname
    core = rw.strip_pollution(rw.CORES_LATE[key].strip())
    core = merge_late_body(core, n)

    if hz(core) > TARGET_HI:
        paras = core.split("\n\n")
        while hz("\n\n".join(paras)) > TARGET_HI and len(paras) > 6:
            paras.pop(-2)
        core = "\n\n".join(paras)

    path = os.path.join(PROSE, fname)
    content = rw.fc(title, core, footer)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    b, _ = extract_body_and_footer(content)
    fillers = count_fillers(b)
    return n, hz(b), dup(b), fillers, fillers


def process_chapter(n: int) -> tuple:
    if n in LATE_META:
        return rebuild_late_chapter(n)

    path = sorted(glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md")))[0]
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    lines = body.split("\n")
    title = lines[0] if lines and lines[0].startswith("#") else ""
    core = "\n".join(lines[1:]).strip() if title else body

    fillers_before = count_fillers(core)
    core = strip_filler_lines(core)
    core = rw.dedupe_paragraphs(rw.dedupe_sentences_light(rw.strip_pollution(core)))
    core = core.replace("序齐，下一章就炼", "序齐，清瘴丸才肯落怀")
    core = rw.ensure_length(core, n)

    if hz(core) > TARGET_HI:
        paras = core.split("\n\n")
        while hz("\n\n".join(paras)) > TARGET_HI and len(paras) > 6:
            paras.pop(-2)
        core = "\n\n".join(paras)

    fillers_after = count_fillers(core)
    content = (
        f"{title}\n\n{core.strip()}\n\n{footer.strip()}\n" if title else f"{core.strip()}\n\n{footer.strip()}\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    b, _ = extract_body_and_footer(content)
    return n, hz(b), dup(b), fillers_before, fillers_after


def main():
    before = sum(
        count_fillers(extract_body_and_footer(open(p, encoding="utf-8").read())[0])
        for n in PURGE_CH
        for p in glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md"))
    )
    print(f"BEFORE filler lines: {before}")

    bad = []
    for n in PURGE_CH:
        n, h, d, fb, fa = process_chapter(n)
        ok = TARGET_LO <= h <= TARGET_HI and d < 0.02 and fa == 0
        print(f"ch{n:03d}", h, f"dup={d:.3f}", f"fillers={fa}", "OK" if ok else "FAIL")
        if not ok:
            bad.append(n)

    after = sum(
        count_fillers(extract_body_and_footer(open(p, encoding="utf-8").read())[0])
        for n in PURGE_CH
        for p in glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md"))
    )
    print(f"AFTER filler lines: {after}")
    if bad:
        print("NEEDS_MANUAL", bad)
        return 1
    print("PURGE_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
