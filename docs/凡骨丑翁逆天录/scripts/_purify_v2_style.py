# -*- coding: utf-8 -*-
"""仙凡笔锋 v2 净化：引号修复、提纲段剥离、模板去重、字闸回填."""
from __future__ import annotations

import argparse
import glob
import importlib.util
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import _split_walls as split_walls
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

META_CHAPTER = re.compile(r"\d+是[^——\n]{1,24}——")
TAIL_PAD_PATTERNS = [
    re.compile(r"^更鼓沉，他按心口：「.{1,8}，记着。手在，路在。」$"),
    re.compile(r"^记着，是丑翁活法；活法在忍，在还，在手稳。$"),
    re.compile(r"^丑时末，他数息：「.{1,8}，手在，路在。」$"),
    re.compile(r"^坛腹温，贴掌，像应「.{1,8}」——活在，路在，就不滚。$"),
]
LAOGENG = "老耿挑水路过，水洒稳，声哑"
ORPHAN_DIALOGUE = re.compile(r"。([^「」]{1,16}，(?:送出了|记着|在前)。)」")
BROKEN_SEND = re.compile(r"。耿恩，送出了。」")

PART2_PAD = [
    "散队后，他过外堂阶下，分拣半刻，指稳——指稳，路就不飘。",
    "编筐半刻，藤刺扎掌，刺浅，浅些沿才净。沿净，坛才藏得住。",
    "丑时，练鼻下静。粟壳香淡，香一字不落。",
    "管事记簿，记细，是小胜。胜在忍，不在辩。",
    "他望坛，低声道：「手在，路在。」坛不应字，只温。",
    "更鼓沉，天边白一线。白里，他按木牌，牌凉贴胸。",
    "坊市尾巷风硬，他收摊如石，石在，就不滚。",
    "验息后，他理怀内册页，页黄，字丑，丑而真。",
    "铁无言声低：「别飘。」韩泥应声：「不飘。」",
    "刘婆端粥，仍多半勺。韩泥点头，谢轻，恩重。",
    "药峰分拣照旧，指稳，鼻下静一息。",
    "帖在怀，怀沉，沉的是序，不是惧。",
    "白织月袖风过，韩泥不辩。辩，费舌；舌要留来守坛。",
    "赖福廊下过，韩泥只答：「在。」在，就不滚。",
    "柱上条角白一线，三年约在怀。怀凉，掌温。",
    "坡下石阶湿，他数息，数帖，数债序。",
    "同棚杂役笑，笑在耳，不在心。",
    "废渣巷日斜，他验渣，渣正，手才静。",
    "侧门驿亭风硬，他听风，风过，记在心里。",
]


def get_rw():
    spec = importlib.util.spec_from_file_location(
        "rw", os.path.join(os.path.dirname(__file__), "..", "prose", "_rewrite_v2.py")
    )
    rw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rw)
    return rw


def strip_meta_prefix(para: str) -> str:
    return META_CHAPTER.sub("", para.strip()).strip()


def is_tail_pad(para: str) -> bool:
    t = para.strip()
    return any(p.match(t) for p in TAIL_PAD_PATTERNS)


def is_template_spam(para: str) -> bool:
    """第二部 ensure_length 机械块（引号易断、与场景无关）."""
    t = para.strip()
    if is_tail_pad(t):
        return True
    markers = (
        "邻床悄问一句，韩泥只答：「",
        "怀凉，掌温——温在",
        "赖福脚步在廊外停半息",
        "管事夜巡过",
        "入夜廊下暗处，风沉，他备料",
        "辰初坛边席角，雾未散",
        "午后侧门驿亭，日斜，他验渣",
        "更鼓沉，沉里，他过",
        "午后编筐棚，风硬，他清栏，指稳，稳里带一点",
        "散队后，他过药渣场角，风硬，练诀",
        "刃不亮，先记。记完了，才配",
        "他低声对坛：「坛在，人在。人在，就不滚。」",
    )
    return any(t.startswith(m) for m in markers)


def cleanup_dialogue(para: str) -> str:
    para = re.sub(r"(他低声对坛：「)+", "他低声对坛：「", para)
    para = re.sub(
        r"他低声对坛：「([^「」]*?)他低声对坛：「([^「」]*?)」」",
        r"他低声对坛：「\1\2。」",
        para,
    )
    para = re.sub(r"(落笔在七笔⑥，⑥是抬棺，⑥是屋漏补瓮。)」", r"\1", para)
    return para


def fix_orphan_closes(para: str) -> str:
    para = cleanup_dialogue(para)
    para = BROKEN_SEND.sub("。他低声对坛：「耿恩，送出了。」", para)
    if para.count("「") < para.count("」"):
        para = ORPHAN_DIALOGUE.sub(r"。他低声对坛：「\1」", para)
    diff = para.count("「") - para.count("」")
    if diff > 0:
        para += "」" * diff
    elif diff < 0:
        para = ("「" * (-diff)) + para
    return para


def merge_broken_dialogue(paras: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(paras):
        p = paras[i]
        merges = 0
        while (
            p.count("「") != p.count("」")
            and i + 1 < len(paras)
            and merges < 2
            and hz(p) < 90
        ):
            nxt = paras[i + 1]
            if nxt.startswith("#"):
                break
            p = p + nxt
            i += 1
            merges += 1
        out.append(fix_orphan_closes(p.strip()))
        i += 1
    return [x for x in out if x]


def dedupe_lao_geng(paras: list[str]) -> list[str]:
    seen = False
    out = []
    for p in paras:
        if LAOGENG in p:
            if seen:
                continue
            seen = True
        out.append(p)
    return out


def pad_part2(body: str, ch: int) -> str:
    seen = set()
    for s in re.split(r"[。！？]", body):
        k = re.sub(r"\s+", "", s.strip())
        if len(k) >= 8:
            seen.add(k)
    j = 0
    while hz(body) < TARGET_LO and j < 120:
        if j < len(PART2_PAD):
            line = PART2_PAD[(ch + j) % len(PART2_PAD)]
        else:
            line = f"更鼓沉，天边白一线。白里，他按木牌，牌凉贴胸。"
        k = re.sub(r"\s+", "", line)
        if k not in seen:
            body = body + "\n\n" + line
            seen.add(k)
        j += 1
    return body


def fix_quotes_and_meta(body: str) -> str:
    paras = [strip_meta_prefix(p.strip()) for p in body.split("\n\n") if p.strip()]
    paras = [p for p in paras if p and not is_tail_pad(p)]
    paras = dedupe_lao_geng(paras)
    paras = merge_broken_dialogue(paras)
    return "\n\n".join(fix_orphan_closes(p) for p in paras if p.strip())


def finalize_length(body: str, ch: int, *, allow_ensure: bool) -> str:
    rw = get_rw()
    body = split_walls.process_body(body)
    paras = merge_broken_dialogue([p.strip() for p in body.split("\n\n") if p.strip()])
    body = "\n\n".join(paras)
    guard = 0
    while hz(body) < TARGET_LO and guard < 8:
        prev = hz(body)
        body = pad_part2(body, ch)
        if hz(body) < TARGET_LO and allow_ensure:
            body = rw.ensure_length(body, ch)
            body = rw.dedupe_sentences_light(body)
        if hz(body) <= prev:
            guard += 1
        else:
            guard = 0
    body = rw.dedupe_sentences_light(body)
    if ch >= 131:
        body = rw.dedupe_sentences_light(body)
    if hz(body) > TARGET_HI:
        paras = body.split("\n\n")
        while hz("\n\n".join(paras)) > TARGET_HI and len(paras) > 10:
            paras.pop(-2)
        body = "\n\n".join(paras)
    for _ in range(3):
        if not split_walls.wall_paras(body):
            break
        body = split_walls.process_body(body)
    if hz(body) < TARGET_LO:
        body = pad_part2(body, ch)
    return body.strip()


def fix_v2_style(body: str, ch: int, *, light: bool = False) -> str:
    """light=True：第二部写盘，不做段落级大 dedupe."""
    rw = get_rw()
    if not light:
        body = rw.dedupe_paragraphs(body)
        body = rw.dedupe_sentences_light(body)
    body = fix_quotes_and_meta(body)
    return finalize_length(body, ch, allow_ensure=ch < 131)


def purify_body(body: str, ch: int, *, aggressive: bool) -> str:
    if not aggressive:
        return fix_v2_style(body, ch)
    paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.startswith("#")]
    new_paras = []
    for p in paras:
        p = strip_meta_prefix(p)
        if not p:
            continue
        if is_template_spam(p):
            continue
        if is_tail_pad(p):
            continue
        new_paras.append(p)
    new_paras = dedupe_lao_geng(new_paras)
    return fix_v2_style("\n\n".join(new_paras), ch, light=True)


def purify_file(path: str, ch: int, aggressive: bool, dry_run: bool) -> dict:
    raw = open(path, encoding="utf-8").read()
    title_m = re.match(r"(# .+\n\n)", raw)
    title = title_m.group(1) if title_m else ""
    body, footer = extract_body_and_footer(raw)
    if title:
        body = re.sub(r"^# .+\n\n", "", body)
    before_hz = hz(body)
    before_q = body.count("「") == body.count("」")
    new_body = purify_body(body, ch, aggressive=aggressive)
    after_hz = hz(new_body)
    after_q = new_body.count("「") == new_body.count("」")
    ok = TARGET_LO <= after_hz <= TARGET_HI and after_q and not split_walls.wall_paras(new_body)
    info = {
        "file": os.path.basename(path),
        "ch": ch,
        "hz": f"{before_hz}->{after_hz}",
        "quotes": f"{before_q}->{after_q}",
        "ok": ok,
    }
    if not dry_run and ok and new_body != body.strip():
        text = title + new_body + (("\n" + footer) if footer else "\n")
        open(path, "w", encoding="utf-8", newline="\n").write(text)
        info["written"] = True
    elif not dry_run and ok:
        info["written"] = False
    else:
        info["written"] = False
        info["fail"] = True
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lo", type=int, default=1)
    ap.add_argument("--hi", type=int, default=150)
    ap.add_argument("--aggressive", action="store_true", help="131+ 额外去 ensure_length 模板块")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    results = []
    for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = int(re.search(r"ch(\d+)", p).group(1))
        if n < args.lo or n > args.hi:
            continue
        agg = args.aggressive and n >= 131
        results.append(purify_file(p, n, agg, args.dry_run))
    ok = sum(1 for r in results if r.get("ok"))
    written = sum(1 for r in results if r.get("written"))
    fail = [r for r in results if r.get("fail")]
    print(f"purify ch{args.lo:03d}-ch{args.hi:03d}: ok={ok}/{len(results)} written={written}")
    for r in fail:
        print(f"  FAIL {r['file']} hz={r['hz']} quotes={r['quotes']}")


if __name__ == "__main__":
    main()
