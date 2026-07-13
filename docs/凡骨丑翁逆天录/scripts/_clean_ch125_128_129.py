# -*- coding: utf-8 -*-
"""Clean corrupted tails in ch125, ch128, ch129."""
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz, TARGET_LO, TARGET_HI

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

CLEAN_MARKERS = [
    "\n\n韩泥不辩。辩，费舌；舌要留来守坛，留来按罐。",
    "\n\n管事夜巡验棚，灯照席角",
    "\n\n老耿挑水路过",
    "\n\n试台，见。」",
    "\n\n十三，在明日。",
]

ENDINGS = {
    125: """他低声道：「窑稳，粒稳，手稳。试台，见。」见字落，接126刘婆补袖，接127债序清，接129帖至。帖至，魁至，还刘婆至。见字丑，丑得像人；人稳，字稳，粒正，手才不飘。""",
    128: """他低声道：「十二层圆。十三，在明日。明日魁，后日还刘婆，大后日帖在怀沉。」明日，部末夺魁，恩偿刘婆，帖至山门——山门帖上言伯钧名，钱戾衡影在字后，像仇在路后。路后不要紧，刘婆这笔先还。""",
    129: """丑时末，他再理布包——新衣叠实，钱串齐，陶罐封泥，九粒培元散在怀。怀沉，沉得像债序最后一笔待落。落笔在130，落在刘婆抖手里，落在她眼浊里清一寸那瞬。

外门弟子渐少，韩泥不近廊下笑。笑在耳，不在心——心在坛，坛腹温一线，温像应「帖」。帖至，大比影至，仇路明一寸；明一寸，省亲路也明一寸。

更鼓尽，天边全白。白里，试台鼓将响，响向末项，响向魁，响向还。还刘婆，是大比帖前最后一笔恩；恩还了，帖才接得住。接得住，钱戾衡名在帖后，后在不要紧，手在前。手稳，粒正，坛在，玉牌在。在，就够了。

山门帖角再掀，掀出「言伯钧」三字影。影淡，淡得像钱戾衡眼风暂退。暂退不要紧，记着。记着，刃亮，丹正，路不断——路不断，就够走进130，够把恩送到该送的人手里。

赖福廊外最后骂一句：「明日夺魁？晦气！」韩泥不辩。舌要留来养息，留来守最后一粒。不抖，就配听「韩泥，魁」，就配看刘婆捏新衣袖口，终于敢信恩没忘。""",
}

for n in [125, 128, 129]:
    path = glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md"))[0]
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    cut = len(body)
    for m in CLEAN_MARKERS:
        idx = body.find(m)
        if idx != -1 and idx < cut:
            cut = idx
    body = body[:cut].rstrip()
    if ENDINGS[n] not in body:
        body = body + "\n\n" + ENDINGS[n]
    open(path, "w", encoding="utf-8").write(body + "\n\n" + footer)
    print(f"ch{n}: {hz(body)} chars")
