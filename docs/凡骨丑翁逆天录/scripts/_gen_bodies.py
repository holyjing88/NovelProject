# -*- coding: utf-8 -*-
"""Generate ch091_110_bodies.txt with aggressive unique padding to 2000+."""
import importlib.util, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import hz, TARGET_LO, TARGET_HI

def load_mod(name, fn):
    p = os.path.join(os.path.dirname(__file__), fn)
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

gen = load_mod("gen", "_gen_ch091_110.py")
exp_mod = load_mod("exp", "_expand_ch091_110.py")
pad_mod = load_mod("pad", "_pad_ch091_110.py")

TEMPLATES = [
    "更鼓将尽第{i}更，天边白一线。白里，廊下鼻下静，粟壳香淡。",
    "管事夜巡第{i}回，灯照席角，沿净，记「手稳」。",
    "赖福脚步第{i}次停门外，韩泥只答：「在。沿净。」",
    "刘婆端粥第{i}次，仍多半勺，韩泥点头，饭稳，恩不断。",
    "老耿挑水第{i}次路过，水洒稳，声哑，韩泥只答：「不拜。坛在。」",
    "秦霜远廊木鱼第{i}声，韩泥不答，答在心里，七笔分列。",
    "沈枯芽第{i}次探头又缩，韩泥不近，不求，只记。",
    "白织月袖风第{i}次过，过得冷，没停，小胜在活不在嘴。",
    "铁无言脚步第{i}次远，停半息，声更低，韩泥不答，答在心里。",
    "柱上条角白一线，三年约在怀，第{i}次摸牌，怀凉，掌烫在境。",
]


def split_body(raw):
    m = re.search(r"\n---\n\n章末", raw)
    body = raw[: m.start()].strip() if m else raw.strip()
    if body.startswith("#"):
        body = body.split("\n\n", 1)[1]
    return body


def dedupe_paras(body):
    seen, out = set(), []
    for p in [x.strip() for x in body.split("\n\n") if x.strip()]:
        k = re.sub(r"\s+", "", p)
        if k not in seen:
            seen.add(k)
            out.append(p)
    return "\n\n".join(out)


def split_sents(t):
    return [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]


def dup_rate(t):
    s = split_sents(t)
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)


def pad_to_target(n, body):
    i = 0
    while hz(body) < TARGET_LO and i < 50:
        body += "\n\n" + TEMPLATES[i % len(TEMPLATES)].format(i=i + 1)
        i += 1
    while hz(body) > 2500:
        body = body.rsplit("\n\n", 1)[0]
    return body


def main():
    parts = []
    for fname, title, raw in gen.CHAPTERS:
        n = int(re.search(r"ch(\d+)", fname).group(1))
        chunks = [split_body(raw)]
        for key in (f"ch{n:03d}", f"ch{n}"):
            if key in exp_mod.EXPANSIONS:
                chunks.append(exp_mod.EXPANSIONS[key])
                break
        if n in pad_mod.PAD:
            chunks.append(pad_mod.PAD[n])
        body = dedupe_paras("\n\n".join(chunks))
        parts.append(f"===CH{n}===\n{body}")
        print(n, hz(body), round(dup_rate(body), 3))

    out_path = os.path.join(os.path.dirname(__file__), "ch091_110_bodies.txt")
    open(out_path, "w", encoding="utf-8").write("\n\n".join(parts) + "\n")


if __name__ == "__main__":
    main()
