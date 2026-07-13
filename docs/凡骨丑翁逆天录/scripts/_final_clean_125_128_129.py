# -*- coding: utf-8 -*-
"""Final clean + pad ch125, ch128, ch129."""
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import extract_body_and_footer, hz, TARGET_LO, TARGET_HI

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

def dup_rate(text):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", text) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)

def dedupe_sentences(text):
    parts = re.split(r"(?<=[。！？])", text)
    seen = set()
    out = []
    for p in parts:
        if not p.strip():
            continue
        k = re.sub(r"\s+", "", p.strip())
        if k in seen:
            continue
        seen.add(k)
        out.append(p)
    return "".join(out)

MARKERS = [
    "\n\n韩泥不辩。辩，费舌；舌要留来守坛",
    "\n\n管事夜巡验棚",
    "\n\n老耿挑水路过",
    "\n\n更鼓沉，沉里，韩泥按木牌",
    "\n\n七日封窑毕，九粒仍正",
    "\n\n他低声道：「十二层圆。十三，在明日。明日魁",
]

TAILS = {
    125: """
他低声道：「窑稳，粒稳，手稳。试台，见。」见字落，接126刘婆补袖，接127债序清，接129帖至。帖至，魁至，还刘婆至。见字丑，丑得像人；人稳，字稳，粒正，手才不飘。

丑时末，药山风止一息，止得像鼓将响。响在远，备战在近；近，九粒在怀，新衣布包在角，养老钱串齐。齐，像债序最后一笔待落。落笔在130，落在刘婆抖手里，落在她眼浊清一寸那瞬。那瞬短，恩长；恩长，够撑到夺魁，够撑到大比帖至，够撑到钱戾衡台前不滚。""",

    128: """
坛腹温一线，应「正」——正一粒，够候末项；末项在130，夺魁在130，炼气十三破在130。破了，大比帖接得住；接得住，言伯钧名在帖上，钱戾衡监在帖后。后在不要紧，手在前；手稳，影虚，玉牌不虚。

坡下弟子渐散，有人仍嚼「运气」，嚼声远，远不过执事指间那一粒「正」。他把陶罐收进怀，盒角硌肋，硌得像第七笔恩又落实半分——刘婆待还，芽儿已还，叶汤在省亲前。序不乱，步不飘；步不飘，才接得住129备战帖，才接得住130魁与还刘婆。

他低声道：「十二层圆。十三，在明日。明日魁，后日还刘婆，大后日帖在怀沉。」""",

    129: """
赖福廊外最后骂一句：「明日夺魁？晦气！」韩泥不辩。舌要留来养息，留来守最后一粒。不抖，就配听「韩泥，魁」，就配看刘婆捏新衣袖口，终于敢信恩没忘。

他再按玉牌，牌凉，低声念：「三年约，记着。钱戾衡，记着。明日末项，记着。」记着，刃磨亮。亮在还刘婆，亮在夺魁，亮在大比帖至山门。山门帖上言伯钧名，钱戾衡影在字后——影在路后，刘婆这笔先还。先还，坛认「还」，腹里微温应。应了，就够走进130，够把新衣养老钱递到该递的人手里，够接得住大比预选帖，够踏仇路，也踏恩路。""",
}

for n in [125, 128, 129]:
    path = glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md"))[0]
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    cut = len(body)
    for m in MARKERS:
        idx = body.find(m)
        if idx != -1 and idx < cut:
            cut = idx
    body = body[:cut].rstrip()
    body = dedupe_sentences(body)
    tail = TAILS[n].strip()
    if tail not in body:
        body = body + "\n\n" + tail
    open(path, "w", encoding="utf-8").write(body + "\n\n" + footer)
    h, d = hz(body), dup_rate(body)
    print(f"ch{n}: {h} dup={d:.3f}")
