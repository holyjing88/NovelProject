# -*- coding: utf-8 -*-
"""v42 末轮补写：剩余短章补至≥2000 · 修复重复状态行"""
import glob, re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_IDEAL, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
V42 = {n for n in range(1, 64)} | {130}

# 每章 2～4 句，确保未出现
TAIL = {
    27: [
        "公审前夜，他试抬药篓，篓沉得稳。稳，像臂还能护芽儿——护得住，徒恩才不白记。",
        "臂肿退尽，他仍去集尾。集尾只看筐，不看脸；脸丑，筐紧，紧就能活到锤落。",
    ],
    40: ["备检前夜，灰线再过石，石过，手稳。稳，像瓮在等冬测开缝，缝开，路才向正测。"],
    42: ["兽栏夜，他多清半刻粪。半刻暖丙九，暖了，手才稳，才配盯秤那日三两落袋。"],
    43: ["盯秤后，掌心仍不抖。抖在袖里，秤盘实了，赖福才虚——虚不是终，终在辨香。"],
    50: ["三日条贴柱，他摸木牌，牌边磨毛。毛得像七笔——笔在，手就不飘，飘了香就飘。"],
    52: ["丑时二更，坛腹温一线。温短，像听商队铃远；铃远，界还在，缘还在等冬深。"],
    54: ["雨后天晴，他数息五遍。遍遍落在「沿净」二字——净了，起伏才不当醒。"],
    55: [
        "符怀暖第三日，西栏风硬，手不僵。僵，藤刺偏；不偏，试手才不滚，滚了恩断。",
        "僧影已远，符仍凡。凡，够活命；活命，才还恩——还，先还叶丫头那碗热汤。",
    ],
    56: ["季末夜，他擦沿三遍。沿净，席严，才接血近沿——近，不碰沿，碰要等误。"],
    57: ["试手前夜，他立末排数息。数到五，掌裂不要紧，要紧是手正，正就够还恩前活命。"],
    58: ["血线前夜，他盖席再严一层。层厚，厚像守六十日；六十日净，沿才接得住误。"],
    59: ["沿前夜，他揭席看沿无尘。无尘，盖严，严像最后一夜守；守住了，才配瓮醒。"],
    60: ["雪停夜，沿上无血，他低声对坛：「你再眠半夜。半夜后，缘满不满，看活计。」"],
    61: ["符影半闪那夜，他不燃符，只暖一丝。一丝，够扛丑时寒；寒不要紧，沿净要紧。"],
    62: ["席盖严夜，血甩破席，沿仍净。净了，丑时将至，将至接瓮醒那一误，误了根在。"],
}


def append_before_anchor(body: str, text: str) -> str:
    text = text.strip()
    if not text or text in body:
        return body
    for anchor in ("\n\n**状态**", "\n\n<!-- v38-end -->", "\n\n---\n\n章末"):
        if anchor in body:
            return body.replace(anchor, f"\n\n{text}{anchor}", 1)
    return body + f"\n\n{text}"


def clean_footer(footer: str) -> str:
    # 脚注区重复状态行剔除
    lines = footer.split("\n")
    out, seen_st = [], False
    for ln in lines:
        if ln.startswith("**状态**"):
            if seen_st:
                continue
            seen_st = True
        out.append(ln)
    return "\n".join(out)


for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in V42:
        continue
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    for s in TAIL.get(n, []):
        if hz(body) >= TARGET_IDEAL:
            break
        body = append_before_anchor(body, s)
    footer = clean_footer(footer)
    open(path, "w", encoding="utf-8", newline="\n").write(body + ("\n\n" + footer if footer else ""))

short = []
for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", path).group(1))
    if n not in V42:
        continue
    b, _ = extract_body_and_footer(open(path, encoding="utf-8").read())
    if hz(b) < TARGET_IDEAL:
        short.append((n, hz(b)))
print("still <2000:", short)
