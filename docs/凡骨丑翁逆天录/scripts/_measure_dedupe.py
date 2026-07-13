# -*- coding: utf-8 -*-
import importlib.util, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import hz, TARGET_LO

def load_mod(fn):
    p = os.path.join(os.path.dirname(__file__), fn)
    spec = importlib.util.spec_from_file_location("m", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

gen = load_mod("_gen_ch091_110.py")
exp = load_mod("_expand_ch091_110.py")
pad = load_mod("_pad_ch091_110.py")

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

def dedupe_sents(body):
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    out, global_seen = [], set()
    for p in paras:
        pk = re.sub(r"\s+", "", p)
        if pk in global_seen:
            continue
        if "「" in p or "」" in p or len(p) < 25:
            global_seen.add(pk)
            out.append(p)
            continue
        sents = [x.strip() for x in re.split(r"(?<=[。！？])", p) if len(x.strip()) >= 8]
        clean = []
        for s in sents:
            sk = re.sub(r"\s+", "", s)
            if sk not in global_seen:
                global_seen.add(sk)
                clean.append(s)
        if clean:
            out.append("".join(clean))
    return "\n\n".join(out)

def dup(t):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]
    if not s: return 0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen: d += 1
        seen.add(k)
    return d / len(s)

for fname, title, raw in gen.CHAPTERS:
    n = int(re.search(r"ch(\d+)", fname).group(1))
    chunks = [split_body(raw)]
    for key in (f"ch{n:03d}", f"ch{n}"):
        if key in exp.EXPANSIONS:
            chunks.append(exp.EXPANSIONS[key].strip())
            break
    if n in pad.PAD:
        chunks.append(pad.PAD[n].strip())
    body = dedupe_sents(dedupe_paras("\n\n".join(chunks)))
    print(n, hz(body), round(dup(body), 4))
