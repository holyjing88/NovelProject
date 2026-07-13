# -*- coding: utf-8 -*-
import re, glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import hz, extract_body_and_footer

LINES = {
    51: "天边白一线，白像试手前三日也白了半分。白不要紧，手要紧。",
    52: "幼兽鼻息匀，匀得像西栏那一角草还留着他的麸皮角——角少，少也暖。",
    53: "外头风硬，风里无栖香全句。全句散了，散成柱上五日条那一息。",
    55: "丑时，他按席，席严，沿净。净，才接后头血近沿，接瓮醒那一误。",
    57: "药膏涂裂口最后一遍，凉后正。正，像鼻下静气移到掌上。",
}

for n, line in LINES.items():
    path = glob.glob(os.path.join("..", "prose", f"ch{n:03d}-*.md"))[0]
    raw = open(path, encoding="utf-8").read()
    body, _ = extract_body_and_footer(raw)
    if hz(body) >= 2000 or line in body:
        print(f"ch{n:03d}: skip {hz(body)}")
        continue
    m = re.search(r"\n---\n\n章末", raw)
    new_raw = raw[:m.start()] + "\n\n" + line + raw[m.start():]
    open(path, "w", encoding="utf-8").write(new_raw)
    nb, _ = extract_body_and_footer(new_raw)
    print(f"ch{n:03d}: {hz(body)} -> {hz(nb)}")
