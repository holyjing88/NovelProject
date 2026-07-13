# -*- coding: utf-8 -*-
import re, glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import hz, extract_body_and_footer

def dup(t):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]
    if not s: return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen: d += 1
        seen.add(k)
    return d / len(s)

EXTRA = {
    51: "同批少年夜间碰他木牌：「三日后验啥？」韩泥只答：「验手。手正，丹才不歪。」",
    52: "铁无言第三趟巡栏，声低：「轮换夜，沿还净？」韩泥只答：「净。净了，才接得住冬深那一赠。」",
    54: "秦霜远廊最后一句：「沿净，才接得住赠。」韩泥不答，答在心里——心里七笔不混，沿才净。",
    55: "刘婆第四趟端姜汤，热：「符在怀，别傲。」韩泥喝尽：「不傲。傲，符灭。」搬柴第四趟，肩勒旧印，印深，沉得住。沉得住，符暖护骨，骨不寒，掌裂不僵。",
    53: "管事第三趟验柴垛，声沉：「纹直，记功在。」韩泥只点头。点头，像把窄路又摁实半寸。",
}

for n, line in EXTRA.items():
    path = glob.glob(os.path.join("..", "prose", f"ch{n:03d}-*.md"))[0]
    raw = open(path, encoding="utf-8").read()
    body, _ = extract_body_and_footer(raw)
    if hz(body) >= 2000:
        continue
    m = re.search(r"\n---\n\n章末", raw)
    new_raw = raw[:m.start()] + "\n\n" + line + "\n" + raw[m.start():]
    open(path, "w", encoding="utf-8").write(new_raw)

for n in range(51, 63):
    raw = open(glob.glob(os.path.join("..", "prose", f"ch{n:03d}-*.md"))[0], encoding="utf-8").read()
    b, _ = extract_body_and_footer(raw)
    d = dup(b)
    ok = 2000 <= hz(b) <= 2500 and d < 0.02
    print(f"ch{n:03d}: {hz(b)} dup={d:.3%} {'OK' if ok else 'FIX'}")
