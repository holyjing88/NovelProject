# -*- coding: utf-8 -*-
import re, glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import hz, extract_body_and_footer

LINES = {
    51: "夜雪又细，落肩即化。化不要紧，肩沉，沉得住，三日后手才正。",
    52: "轮换夜将尽，坛腹时温时凉，像瓮听西栏咳声——听，不应人，应冬。",
    53: "霜夜将尽，斧声歇，手还正。正，才配接后头凝丹那一关。",
    54: "雨歇了，轮换稳了，褐袍人还在。沿净，才接得住赠。",
    55: "五更前，柱上五日条猎猎作响。猎猎不是催滚，是催手正——手正，符护骨，瓮眠等缘。",
    57: "试手前夜，他合眼，不睡实。鼻下静，手上才静。静，才配末排。",
}

for n, line in LINES.items():
    path = glob.glob(os.path.join("..", "prose", f"ch{n:03d}-*.md"))[0]
    raw = open(path, encoding="utf-8").read()
    body, _ = extract_body_and_footer(raw)
    if hz(body) >= 2000:
        continue
    m = re.search(r"\n---\n\n章末", raw)
    if not m:
        continue
    # avoid dup insert
    if line in body:
        continue
    new_raw = raw[:m.start()] + "\n\n" + line + raw[m.start():]
    open(path, "w", encoding="utf-8").write(new_raw)
    nb, _ = extract_body_and_footer(new_raw)
    print(f"ch{n:03d}: {hz(body)} -> {hz(nb)}")
