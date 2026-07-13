# -*- coding: utf-8 -*-
import importlib.util, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import hz

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

for fname, title, raw in gen.CHAPTERS:
    n = int(re.search(r"ch(\d+)", fname).group(1))
    chunks = [split_body(raw)]
    for key in (f"ch{n:03d}", f"ch{n}"):
        if key in exp.EXPANSIONS:
            chunks.append(exp.EXPANSIONS[key].strip())
            break
    if n in pad.PAD:
        chunks.append(pad.PAD[n].strip())
    body = "\n\n".join(chunks)
    print(n, hz(body))
