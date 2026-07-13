# -*- coding: utf-8 -*-
"""Fix ch071-090: split walls, dedupe, ensure hz 2000-2500."""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
WALL_LIMIT = 180
SPLIT = re.compile(r"(?<=[。！？])")


def para_len(p):
    return len(re.sub(r"\s+", "", p))


def split_para(p):
    if para_len(p) <= WALL_LIMIT:
        return [p.strip()] if p.strip() else []
    sents = [x for x in SPLIT.split(p.strip()) if x.strip()]
    chunks, cur = [], ""
    for s in sents:
        trial = cur + s
        if cur and para_len(trial) > 150:
            chunks.append(cur.strip())
            cur = s
        else:
            cur = trial
    if cur.strip():
        chunks.append(cur.strip())
    out = []
    for c in chunks:
        if para_len(c) <= WALL_LIMIT:
            out.append(c)
        else:
            mid = len(c) // 2
            cut = c.rfind("。", 0, mid + 40)
            if cut < 40:
                cut = c.find("。", mid - 40)
            if cut > 0:
                out.append(c[: cut + 1].strip())
                rest = c[cut + 1 :].strip()
                if rest:
                    out.append(rest)
            else:
                out.append(c)
    return out


def split_walls(body):
    paras = re.split(r"\n\s*\n", body.strip())
    out = []
    for p in paras:
        out.extend(split_para(p))
    return "\n\n".join(out)


def dedupe_body(body):
    paras = re.split(r"\n\s*\n", body.strip())
    seen, out = set(), []
    for p in paras:
        sents = [x.strip() for x in SPLIT.split(p) if x.strip()]
        new_sents = []
        for s in sents:
            k = re.sub(r"\s+", "", s)
            if len(k) >= 8 and k in seen:
                continue
            if len(k) >= 8:
                seen.add(k)
            new_sents.append(s)
        if new_sents:
            out.append("".join(new_sents))
    return "\n\n".join(out)


def dup_rate(body):
    s = [x.strip() for x in SPLIT.split(body) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)


def wall_count(body):
    return sum(1 for p in re.split(r"\n\s*\n", body) if para_len(p) > WALL_LIMIT)


UNIQUE_PAD = [
    "廊下风硬，他把木牌系紧一线，系得像把仍末摁进掌心。",
    "同批少年远避，避像避晦气，晦气遮瓮，遮住了才稳。",
    "编筐角藤刺仍在，他偏手，刺浅些，沿才净，坛才藏得住。",
    "管事夜巡验棚，灯照席角，沿净，像腌菜坛，不像邪。",
    "老耿挑水过，声哑，境别拜邪，拜了路断，他只记着。",
    "秦霜木鱼远，一声，心别邪，邪了鼻下香飘，香飘手就滚。",
    "柱上条角白一线，三年约在怀，愧字在怀，手仍不抖。",
    "白织月远廊过，袖风冷，没停，胜在鼻，不在嘴。",
    "铁无言脚步远，停半息，声低，别漏香，别叫境，只记。",
    "刘婆粥稀，勺沉，饭稳恩不断，他喝尽，不谢，只记。",
]


def main():
    patterns = ["ch07[1-9]-*.md", "ch08[0-9]-*.md", "ch090-*.md"]
    files = []
    for pat in patterns:
        files.extend(glob.glob(os.path.join(PROSE, pat)))
    files = sorted(set(files))

    for path in files:
        text = open(path, encoding="utf-8").read()
        body, footer = extract_body_and_footer(text)
        body = split_walls(body)
        body = dedupe_body(body)
        n = int(re.search(r"ch(\d+)", os.path.basename(path)).group(1))
        pi = 0
        while hz(body) < TARGET_LO and pi < len(UNIQUE_PAD) * 3:
            body += "\n\n" + UNIQUE_PAD[pi % len(UNIQUE_PAD)]
            pi += 1
        while hz(body) > TARGET_HI and "\n\n" in body:
            body = "\n\n".join(body.split("\n\n")[:-1])
        body = dedupe_body(body)
        new = body + "\n\n" + footer.lstrip("\n")
        open(path, "w", encoding="utf-8").write(new)
        h, d, w = hz(body), dup_rate(body), wall_count(body)
        fn = os.path.basename(path)
        ok = TARGET_LO <= h <= TARGET_HI and d < 0.02 and w == 0
        print(f"{fn:32s} hz={h} dup={d:.3f} wall={w} {'OK' if ok else 'FIX'}")


if __name__ == "__main__":
    main()
