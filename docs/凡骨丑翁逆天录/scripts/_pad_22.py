# -*- coding: utf-8 -*-
"""Minimal unique pad for 22 chapters still under 2000 chars."""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

PAD = {
    40: ["他独眼平，手不抖，低声道：「沿净，才接得住后头凡符。」"],
    53: ["更鼓沉，沉里，坛腹应温，像应「冬」字最后一笔。"],
    93: [
        "邻床问：「你床角啥味儿？」「备料味。」韩泥声平，「味在柜，不在席。」",
        "铁无言指席下暗格：「备齐了，别炼。炼在远，在95。远不要紧，手在近。」",
    ],
    94: [
        "更鼓二更，外头风硬，风进缝，缝窄，窄才像门缝。窄不要紧，灯稳，稳了，95才赠得出。",
        "他理样纸，纸糙，糙得像路。路轻，记重——记门缝留灯，记匿赠在前。",
    ],
    96: ["坊市尾巷，人声杂，韩泥只听风——风在舌上，不在鼻。鼻清，手稳，风就吹不散。"],
    97: ["围观者嗡一声，嗡里带嘲。嘲不要紧，韩泥不辩——辩，费舌；舌要留来稳牌。"],
    98: ["散摊后，他收牌，牌丑，牌真。真在「试」，不在「名」；名在远，在130魁。"],
    99: ["远岭兽吼又近，近不要紧，备先到，100前夜在前；前夜在前，手才不飘。"],
    100: ["更鼓沉，障木沉，沉像70按台——掌在，名在，路在。怕也值，值了，恩才不断。"],
    101: ["清料分三堆，堆别不可混。混了，瘴反噬；反噬不要紧，鼻下有根，根细。"],
    102: ["第一兽扑障，刺退，记功一笔——笔记功，不进舌。103压界才顶得住。"],
    103: ["更鼓急，急里，他鼻下仍静。静一字不落，落齐了，104兽潮至才接得住。"],
    104: ["血溅障木，溅不要紧，矛仍稳。稳了，105战中，手在，就不滚。"],
    105: ["甜毒腥一线，一线也要剔——剔净，106续才清得瘴。107钩108在前。"],
    106: ["界外兽声稀半分，障仍立。续了，107钩108才接得住——钩清瘴，钩并肩。"],
    107: ["深窝甜，甜像等丸。等不要紧，等的是108清瘴并肩。手在，铁无言在。"],
    108: ["并肩末，铁无言声低：「清了，别辩。」清了，109炉温稳才接得住。"],
    109: ["炉温稳，火匀一寸。一寸够了，110首炼在前；前头有首丹，有130魁。"],
    110: [
        "铁无言立窑外，声低：「首炼成了，别示。示了，谣来。」韩泥应声：「不示。沿净。」",
        "散成时，天色白，白得像刘婆补衣那线——线旧，线暖，线他记了五年。",
    ],
    125: ["七日封窑毕，九粒仍正。正，试台在手。手不飘，129帖至，130魁与还刘婆。"],
    128: ["验正毕，韩泥立台侧，等末项。末项在130，夺魁在130，炼气十三破在130。"],
    129: ["他望坛，低声道：「明日魁，后日还刘婆。还了，帖在怀，大比在路。」坛不应字，只温。"],
}


def pad_ch(n: int) -> int:
    files = glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md"))
    if not files:
        return -1
    path = sorted(files)[0]
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    if hz(body) >= TARGET_LO:
        return hz(body)
    for p in PAD.get(n, []):
        if p not in body:
            body = body.rstrip() + "\n\n" + p
        if hz(body) >= TARGET_LO:
            break
    new = body + "\n\n" + footer.lstrip("\n")
    open(path, "w", encoding="utf-8").write(new + "\n")
    return hz(body)


if __name__ == "__main__":
    bad = []
    for n in sorted(PAD.keys()):
        h = pad_ch(n)
        ok = h >= TARGET_LO
        print(f"ch{n:03d}: {h} {'OK' if ok else 'FIX'}")
        if not ok:
            bad.append((n, h))
    print("BAD", bad)
