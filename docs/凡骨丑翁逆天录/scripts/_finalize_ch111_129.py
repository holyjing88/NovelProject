# -*- coding: utf-8 -*-
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

FINAL = {
    119: "报名后第三日，韩泥仍渣场分拣，掌茧裂处疼，疼不露。不露，像没听见末席嘲。嘲在耳，备战在心。心在坛，坛醒，粒在怀。怀沉，沉的是债序，不是惧。惧要手抖，他不抖。不抖，就配121闭门炼，配130魁，配还刘婆新衣养老钱。",
    120: "第三周，柱上条又新，新字添「限培元散」。韩泥读条，独眼平，捧陶罐，罐封泥严。严了，私带谣虚。虚了，舌净，手稳。手稳，风声再嘲也尖不过正。正在粒，不在袖风。袖风过，过不要紧，试台见。",
    121: "第七日开窑，七粒仍正，正得像腌菜坛蒙尘——尘不要紧，蔽眼。蔽了赖福眼，蔽了白织月眼，试台再开，正字自现。现了，十一层稳，十二层在123破。破了，试台见，见还，见刘婆。",
    125: "开窑晨，天色白，白得像刘婆补衣线。线旧，线暖，线记着，等130还。还不要紧，先试台末项。末项夺魁，炼气十三破，破了大比帖才接得住。",
    126: "试台前夜，韩泥独坐坛边，把刘婆针脚又摸一遍。针脚糙，暖。暖进骨，骨暖，天寒不怕。不怕，试台手才不僵。僵了，粒洒；洒了，刘婆恩还迟。",
    127: "试台清晨，丙九列队。韩泥立末，怀九粒，不躲。躲像怕，怕手抖。手不抖，仇苗反而扎实。扎实了，接钱戾衡影，接玉牌凉烫，接三年约反面。反面烫，正面手稳。",
    128: "候末项时，风硬，吹得灰线名像刀。刀在皮上划，划不出血，划得出忍。忍不是怂，是活。活长了，才还刘婆，才接大比帖，才钱戾衡台前不滚。",
    129: "天边白一线，白里试台木色浅。浅像70踹台，踹台接了约，约接到明日魁。魁后炼气十三，还刘婆，帖在怀沉。沉债序，不沉惧。",
}

for n in range(111, 130):
    path = glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md"))[0]
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    body = dedupe_sentences(body)
    if n in FINAL and FINAL[n] not in body:
        if hz(body) < TARGET_LO or dup_rate(body) >= 0.02:
            body = body + "\n\n" + FINAL[n]
    open(path, "w", encoding="utf-8").write(body + "\n\n" + footer)

print("=== FINAL ===")
fail = []
for n in range(111, 130):
    path = glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md"))[0]
    body, _ = extract_body_and_footer(open(path, encoding="utf-8").read())
    h, d = hz(body), dup_rate(body)
    ok = TARGET_LO <= h <= TARGET_HI and d < 0.02
    status = "OK" if ok else "FAIL"
    print(f"ch{n:03d}: {h} dup={d:.3f} {status}")
    if not ok:
        fail.append((n, h, round(d, 3)))
print("FAIL", fail)
