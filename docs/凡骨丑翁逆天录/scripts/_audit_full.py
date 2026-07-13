# -*- coding: utf-8 -*-
"""全书正文质检：重复/乱码/结构"""
import collections
import glob
import os
import re

from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")


def sentences(body):
    return [x.strip() for x in re.split(r"(?<=[。！？])", body) if len(x.strip()) >= 8]


def dup_info(body):
    s = sentences(body)
    seen, d, dups = set(), 0, []
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
            dups.append(x)
        seen.add(k)
    return (d / len(s) if s else 0), dups


rows = []
all_sents = collections.defaultdict(list)

for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    n = int(re.search(r"ch(\d+)", p).group(1))
    raw = open(p, encoding="utf-8").read()
    body, _ = extract_body_and_footer(raw)
    h = hz(body)
    dr, dups = dup_info(body)
    flags = []
    if h < TARGET_LO:
        flags.append("SHORT")
    if h > TARGET_HI:
        flags.append("OVER")
    if dr >= 0.02:
        flags.append(f"DUP{dr:.3f}")
    if "**状态**" in body:
        flags.append("STAT_BODY")
    if "---" not in raw:
        flags.append("NO_SEP")
    if re.search(r"\bch0\d{2}\b", body):
        flags.append("META_CH")
    # 引号未闭合：行内「多于」
    for line in body.splitlines():
        if line.count("「") != line.count("」") and ("「" in line or "」" in line):
            flags.append("QUOTE")
            break
    # 叙述对白粘连
    if re.search(r"。[^\n「」\s][^\n]{0,8}：", body):
        flags.append("GLUE")
    if len(re.findall(r"韩泥[「\"]?嗯", body)) > 1:
        flags.append("NG_MULTI")
    if "下一章" in body or "这章" in body or "读者" in body:
        flags.append("META_NARR")
    for s in sentences(body):
        all_sents[re.sub(r"\s+", "", s)].append(n)
    rows.append((n, h, dr, flags, dups[:2]))

print("=== SUMMARY ===")
print("chapters", len(rows))
print("short", sum(1 for r in rows if "SHORT" in r[3]))
print("over", sum(1 for r in rows if "OVER" in r[3]))
print("dup>=2%", sum(1 for r in rows if r[2] >= 0.02))
print("any_flag", sum(1 for r in rows if r[3]))
print()
print("=== DUP >= 2% ===")
for n, h, dr, flags, dups in sorted(rows, key=lambda x: -x[2]):
    if dr >= 0.02:
        sample = dups[0][:55] if dups else ""
        print(f"ch{n:03d} {h} dup={dr:.3f} | {sample}")
print()
print("=== OTHER FLAGS ===")
for n, h, dr, flags, _ in rows:
    other = [f for f in flags if not f.startswith("DUP")]
    if other:
        print(f"ch{n:03d} {other}")
print()
print("=== CROSS-CH SENTENCE (>=3 ch) ===")
cross = [(k, chs) for k, chs in all_sents.items() if len(set(chs)) >= 3 and len(k) >= 12]
cross.sort(key=lambda x: -len(set(x[1])))
for k, chs in cross[:20]:
    print(f"{len(set(chs))}ch {sorted(set(chs))} | {k[:50]}")
