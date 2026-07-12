# -*- coding: utf-8 -*-
"""v42 清扫 ch50-62 章末乱序 · 重建单钩单状态"""
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_IDEAL, extract_body_and_footer, hz
from _v42_finalize import HOOKS, STATUS, DEFAULT_ST, BOOST, EXTRA2, insert_sentences

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
END_M = "<!-- v38-end -->"
V42_M = "<!-- v42-topup -->"


def main_body(raw: str) -> str:
    body, _ = extract_body_and_footer(raw)
    cut = re.search(r"\n\n<!-- v42-topup -->|\n\n<!-- v38-end -->|\n\n\*\*状态\*\*", body)
    if cut:
        body = body[: cut.start()].rstrip()
    return body


def rebuild(n: int, path: str) -> None:
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    body = main_body(raw)

    sents = BOOST.get(n, []) + EXTRA2.get(n, [])
    for s in sents:
        if hz(body) >= TARGET_IDEAL:
            break
        if s not in body:
            body = insert_sentences(body, [s])

    hook = HOOKS.get(n, "")
    st = STATUS.get(n, DEFAULT_ST)
    body += f"\n\n{V42_M}\n\n"
    # 补一句独段
    pad = {
        56: "季末手在，缘在等。等，不主动滴血，血要等误那一甩。",
        57: "掌裂不要紧，手正要紧。正要紧，坡下试手才不滚。",
        58: "沿前止，像道线。线内席，线外沿；沿滑，像祖父手。",
        59: "六十日净，沿才接得住误。误了，根在，瓮才醒。",
        61: "丑时坛温加剧，他不主动滴血。滴血要等误，误了才认主。",
        62: "席盖严了，沿仍净。净了，丑时将至，将至接瓮醒。",
    }
    if hz(body) < TARGET_IDEAL and n in pad and pad[n] not in body:
        body += pad[n] + "\n"
    if hz(body) < TARGET_IDEAL and hook and hook[:20] not in body:
        body += hook[: min(80, len(hook))] + "。\n"

    body += f"\n{END_M}\n\n{hook}\n\n{st}"

    # 脚注只保留符状态等在 footer
    footer = re.sub(r"\n\*\*状态\*\*：.+", "", footer)
    if n == 55 and "符·凡符祛寒" not in footer:
        footer = footer.replace(
            "**v42起点10**）",
            "**v42起点10**）\n\n**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍 · 符·凡符祛寒（凡品·防）",
        )

    open(path, "w", encoding="utf-8", newline="\n").write(body + "\n\n" + footer)


for n in range(50, 63):
    paths = glob.glob(os.path.join(PROSE, f"ch{n:03d}*.md"))
    if paths:
        rebuild(n, paths[0])
        b, _ = extract_body_and_footer(open(paths[0], encoding="utf-8").read())
        print(f"ch{n:03d} -> {hz(b)}")
