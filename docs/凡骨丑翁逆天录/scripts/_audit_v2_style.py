# -*- coding: utf-8 -*-
"""Audit 仙凡笔锋 v2 style markers — full book or range."""
import argparse
import glob
import os
import re
import sys

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")


def hz(t):
    return len(re.sub(r"\s+", "", t))


def load(n):
    for p in glob.glob(os.path.join(PROSE, f"ch{n:03d}-*.md")):
        raw = open(p, encoding="utf-8").read()
        body = raw.split("---")[0]
        body = re.sub(r"^#.*\n\n", "", body)
        return body.strip(), os.path.basename(p)
    return None, None


def analyze(body):
    sents = [s.strip() for s in re.split(r"(?<=[。！？])", body) if len(s.strip()) >= 4]
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    lens = [hz(s) for s in sents]
    short = sum(1 for l in lens if l <= 18) / max(len(lens), 1)
    markers = {
        "不要紧": len(re.findall(r"不要紧", body)),
        "短对话": len(re.findall(r"「[^」]{1,8}」", body)),
        "坛腹温": len(re.findall(r"坛腹温", body)),
        "更鼓沉": len(re.findall(r"更鼓沉", body)),
        "手在路在": len(re.findall(r"手在，路在", body)),
        "老耿挑水": len(re.findall(r"老耿挑水路过", body)),
        "章位自评": len(re.findall(r"\d+是.{1,8}章——", body)),
        "模板污染": len(re.findall(r"(更残第|丑时第)\d+", body)),
        "尾补按心口": len(re.findall(r"按心口：「.{1,8}，记着", body)),
        "尾补丑时末": len(re.findall(r"丑时末，他数息", body)),
        "长段120+": sum(1 for p in paras if hz(p) > 120),
        "禁词": sum(body.count(w) for w in ("恩册", "恩簿", "记账翁", "下一章", "这章", "读者若问")),
    }
    markers["均句长"] = round(sum(lens) / max(len(lens), 1), 1)
    markers["短句比"] = round(short, 3)
    markers["段数"] = len(paras)
    markers["引号配"] = body.count("「") == body.count("」")
    markers["orphan_quote"] = len(re.findall(r"「[^」]*$", body, re.M))
    return markers


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lo", type=int, default=1)
    ap.add_argument("--hi", type=int, default=150)
    ap.add_argument("--issues-only", action="store_true")
    args = ap.parse_args()

    groups = {
        "1-30": range(1, 31),
        "31-62": range(31, 63),
        "63-90": range(63, 91),
        "91-110": range(91, 111),
        "111-130": range(111, 131),
        "131-150": range(131, 151),
    }
    keys = [
        "不要紧", "短对话", "章位自评", "老耿挑水", "模板污染",
        "尾补按心口", "尾补丑时末", "禁词", "长段120+",
    ]
    print(f"=== 分组均值 ch{args.lo:03d}-ch{args.hi:03d} ===")
    for gname, chs in groups.items():
        chs = [c for c in chs if args.lo <= c <= args.hi]
        if not chs:
            continue
        acc = {k: 0.0 for k in keys}
        acc["均句长"] = acc["短句比"] = acc["段数"] = 0.0
        q_bad = 0
        n = 0
        for c in chs:
            body, _ = load(c)
            if not body:
                continue
            m = analyze(body)
            n += 1
            for k in keys:
                acc[k] += m[k]
            acc["均句长"] += m["均句长"]
            acc["短句比"] += m["短句比"]
            acc["段数"] += m["段数"]
            if not m["引号配"]:
                q_bad += 1
        if not n:
            continue
        print(f"\n{gname} (n={n}, 引号异常={q_bad}):")
        for k in keys:
            print(f"  {k}: {acc[k]/n:.2f}/章")
        print(f"  均句长: {acc['均句长']/n:.1f}  短句比: {acc['短句比']/n:.3f}")

    print(f"\n=== 逐章问题 ch{args.lo:03d}-ch{args.hi:03d} ===")
    issue_n = 0
    for c in range(args.lo, args.hi + 1):
        body, fn = load(c)
        if not body:
            continue
        m = analyze(body)
        flags = []
        if not m["引号配"]:
            flags.append("引号不配")
        if m["章位自评"] >= 1:
            flags.append(f"章位自评x{m['章位自评']}")
        if m["模板污染"] > 0:
            flags.append("模板污染")
        if m["禁词"] > 0:
            flags.append(f"禁词x{m['禁词']}")
        if m["老耿挑水"] >= 2:
            flags.append(f"老耿模板x{m['老耿挑水']}")
        if m["尾补按心口"] or m["尾补丑时末"]:
            flags.append("尾补模板")
        if m["短句比"] < 0.20 and c <= 110:
            flags.append(f"短句偏低({m['短句比']})")
        if flags:
            issue_n += 1
            if not args.issues_only or True:
                print(f"  ch{c:03d} {fn}: {', '.join(flags)}")
    print(f"\n共 {issue_n} 章有问题")


if __name__ == "__main__":
    main()
