# -*- coding: utf-8 -*-
"""One-shot stabilize ch079 + ch091-110 for ALL_OK.

✅ v49.3 · 终检后 ch091～110 稳定化（见 30 §7.3）
- 跑前确认 _v42_check 已 FAIL；跑后必 _v42_check + _score_full
"""
import glob
import importlib.util
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, extract_body_and_footer, hz
from _fix_prose_final import UNIQUE

ROOT = os.path.join(os.path.dirname(__file__), "..")
PROSE = os.path.join(ROOT, "prose")

spec = importlib.util.spec_from_file_location("rw", os.path.join(ROOT, "prose", "_rewrite_v2.py"))
rw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rw)

raw_txt = open(os.path.join(os.path.dirname(__file__), "ch091_110_bodies.txt"), encoding="utf-8").read()


def dup(t):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)


def write_ch(n, title, body, path):
    _, footer = extract_body_and_footer(open(path, encoding="utf-8").read())
    content = f"# {title}\n\n{body.strip()}\n\n{footer.strip()}\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    b, _ = extract_body_and_footer(content)
    return hz(b), dup(b)


# ch079 meta
p79 = sorted(glob.glob(os.path.join(PROSE, "ch079-*.md")))[0]
raw = open(p79, encoding="utf-8").read()
raw = raw.replace("经页黄边翻至下一章", "经页黄边再翻一线")
open(p79, "w", encoding="utf-8").write(raw)

# rewrite 93-110 via canonical script
rw.main()

# ch91 expand
for n in (91,):
    m = re.search(rf"===CH{n}===(.*?)===CH{n + 1}===", raw_txt, re.S)
    core = m.group(1).strip()
    core = re.split(r"\n(?=韩泥记\d+-\d+：|\d+章·第\d+笔)", core)[0].strip()
    for u in UNIQUE.get(n, []):
        if u.strip() not in core:
            core += "\n\n" + u.strip()
    core = rw.dedupe_paragraphs(rw.dedupe_sentences_light(rw.strip_pollution(core)))
    body = rw.ensure_length(core, n)
    path = sorted(glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md")))[0]
    h, d = write_ch(n, f"第九十一章 废窑试炉", body, path)
    print(f"ch{n:03d}", h, d)

# ch92 ensure only
m = re.search(r"===CH92===(.*?)===CH93===", raw_txt, re.S)
core = m.group(1).strip()
core = re.split(r"\n(?=韩泥记\d+-\d+：|\d+章·第\d+笔)", core)[0].strip()
core = rw.dedupe_paragraphs(rw.dedupe_sentences_light(core))
body = rw.ensure_length(core, 92)
hook = "柱上条角白一线，废窑火路熟半分——熟半分，够再备；明日倒渣，仍沿净，瓮温应一线。"
if hook not in body:
    body = body.rstrip() + "\n\n" + hook
path = sorted(glob.glob(os.path.join(PROSE, "ch092-*.md")))[0]
h, d = write_ch(92, "第九十二章 废窑再试", body, path)
print(f"ch092", h, d)

# dedupe 93-110 + meta fix
for n in range(93, 111):
    path = sorted(glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md")))[0]
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    lines = body.split("\n")
    title = lines[0] if lines[0].startswith("#") else ""
    core = "\n".join(lines[1:]).strip() if title else body
    core = rw.dedupe_paragraphs(rw.dedupe_sentences_light(rw.strip_pollution(core)))
    core = core.replace("序齐，下一章就炼", "序齐，清瘴丸才肯落怀")
    if hz(core) < TARGET_LO:
        core = rw.ensure_length(core, n)
    content = (f"{title}\n\n{core.strip()}\n\n{footer.strip()}\n" if title else f"{core.strip()}\n\n{footer.strip()}\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    b, _ = extract_body_and_footer(content)
    print(f"ch{n:03d}", hz(b), dup(b))
