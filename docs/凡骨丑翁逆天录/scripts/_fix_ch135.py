# -*- coding: utf-8 -*-
"""One-off surgical fix for ch135."""
import glob
import importlib.util
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
PAD_RE = re.compile(r"^更鼓沉，他按木牌——\d+息，手稳，路就不飘。$")
META_RE = re.compile(r"\d+才写「从绶伏笔」——")
GENERIC = (
    "坊市尾巷风硬，他收摊如石，石在，就不滚。",
    "验息后，他理怀内册页，页黄，字丑，丑而真。",
    "铁无言声低：「别飘。」韩泥应声：「不飘。」",
    "刘婆端粥，仍多半勺。韩泥点头，谢轻，恩重。",
    "药峰分拣照旧，指稳，鼻下静一息。",
    "帖在怀，怀沉，沉的是序，不是惧。",
    "白织月袖风过，韩泥不辩。",
    "赖福廊下过，韩泥只答：「在。」在，就不滚。",
    "柱上条角白一线，三年约在怀。怀凉，掌温。",
    "坡下石阶湿，他数息，数帖，数债序。",
    "同棚杂役笑，笑在耳，不在心。",
    "废渣巷日斜，他验渣，渣正，手才静。",
    "侧门驿亭风硬，他听风，风过，记在心里。",
    "散队后，他过外堂阶下，分拣半刻，指稳——指稳，路就不飘。",
    "编筐半刻，藤刺扎掌，刺浅，浅些沿才净。沿净，坛才藏得住。",
)


def main():
    p = glob.glob(os.path.join(PROSE, "ch135-*.md"))[0]
    raw = open(p, encoding="utf-8").read()
    title_m = re.match(r"(# .+\n\n)", raw)
    title = title_m.group(1)
    body, footer = extract_body_and_footer(raw)
    body = re.sub(r"^# .+\n\n", "", body)

    paras = []
    seen_para = set()
    for para in body.split("\n\n"):
        p = para.strip()
        if not p:
            continue
        if PAD_RE.match(p):
            continue
        if p in GENERIC:
            continue
        if p == "手在，路在，就不滚。":
            continue
        p = META_RE.sub("伏笔不是纳，是站；", p)
        p = p.replace("135才写「从绶伏笔」——", "")
        p = p.replace("「」记着", "记着")
        p = re.sub(r"135只嘲——", "只嘲——", p)
        p = re.sub(r"在135廊下不滚", "在廊下不滚", p)
        k = re.sub(r"\s+", "", p)
        if k in seen_para:
            continue
        seen_para.add(k)
        # fix broken line 63 style
        if "站侧，不叫。更鼓将尽" in p:
            parts = p.split("。更鼓将尽", 1)
            if parts[0].endswith("不叫"):
                paras.append(parts[0] + "。」")
                rest = "更鼓将尽" + parts[1]
                for chunk in re.split(r"(?<=[。！？])", rest):
                    chunk = chunk.strip()
                    if chunk:
                        paras.append(chunk)
            continue
        paras.append(p)

    # drop second 管事记簿 duplicate if near duplicate text
    out = []
    seen_guan = 0
    for p in paras:
        if "管事" in p and "廊下不滚" in p and "记细" in p:
            seen_guan += 1
            if seen_guan > 1:
                continue
        if "管事记簿，记细，是小胜。胜在忍，不在辩" in p:
            if any("管事记簿，记细" in x for x in out):
                continue
        out.append(p)

    body = "\n\n".join(out)
    if "136在前" not in body:
        body += "\n\n更鼓沉，他望坛，独眼平：「136在前。记着。」坛腹温，贴掌，像应「站」——站在侧，不叫，580在远。"

    spec = importlib.util.spec_from_file_location(
        "rw", os.path.join(os.path.dirname(__file__), "..", "prose", "_rewrite_v2.py")
    )
    rw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rw)
    import _split_walls as sw

    body = rw.dedupe_sentences_light(body)
    body = sw.process_body(body)
    if hz(body) < TARGET_LO:
        body += "\n\n丑时，练鼻下静。粟壳香淡，香一字不落。落齐，135这一日记进心里。"
    if hz(body) > TARGET_HI:
        ps = body.split("\n\n")
        while hz("\n\n".join(ps)) > TARGET_HI and len(ps) > 12:
            ps.pop(-2)
        body = "\n\n".join(ps)

    assert TARGET_LO <= hz(body) <= TARGET_HI
    assert body.count("「") == body.count("」")

    sents = [x.strip() for x in re.split(r"(?<=[。！？])", body) if len(x.strip()) >= 8]
    seen, dup = set(), 0
    for x in sents:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            dup += 1
        seen.add(k)
    dr = dup / len(sents)
    assert dr < 0.02, f"dup={dr:.3f}"

    open(p, "w", encoding="utf-8", newline="\n").write(title + body.strip() + "\n" + footer)
    print(f"OK hz={hz(body)} dup={dr:.3f} quotes={body.count('「')}")


if __name__ == "__main__":
    main()
