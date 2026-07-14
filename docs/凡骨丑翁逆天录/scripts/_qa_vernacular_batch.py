# -*- coding: utf-8 -*-
"""批量质检：白话返工章。用法: python _qa_vernacular_batch.py 15 50"""
import importlib
import sys
from pathlib import Path

from prose_utils import extract_body_and_footer, hz, TARGET_HI, TARGET_LO

sf = importlib.import_module("_score_full")
prose = Path(__file__).resolve().parent.parent / "prose"


def qa_range(lo, hi):
    bad = []
    for i in range(lo, hi + 1):
        fs = list(prose.glob("ch%03d-*.md" % i))
        if not fs:
            bad.append((i, "MISSING"))
            print("ch%03d MISSING" % i)
            continue
        body, footer = extract_body_and_footer(fs[0].read_text(encoding="utf-8"))
        h = hz(body)
        dr, dups = sf.dup_rate(body)
        walls = sf.wall_paras(body)
        flags = []
        if dr >= 0.02:
            flags.append("DUP")
        if walls:
            flags.append("WALL")
        if "**状态**" in body:
            flags.append("STAT_BODY")
        if "下一章" in body or "读者若问" in body:
            flags.append("META")
        sc = sf.score_ch(i, h, dr, flags, walls, body=body, footer=footer)
        hk = [k for k in sf.HOOK_KEY if k in sf.hook_tail(body)]
        issues = []
        if not (TARGET_LO <= h <= TARGET_HI):
            issues.append("LEN%d" % h)
        if dr >= 0.02:
            issues.append("dup")
        if walls:
            issues.append("WALL")
        if "通俗笔锋" not in footer:
            issues.append("FOOT")
        if body.count("「") < 12:
            issues.append("Q%d" % body.count("「"))
        if not hk:
            issues.append("NOHOOK")
        for ban in ("恩辱分列", "分列不混", "怒值满", "仙凡笔锋", "药峰分拣"):
            if ban in body:
                issues.append("BAN:" + ban)
                break
        tag = "OK" if not issues and sc >= 9.9 else "|".join(issues) or ("sc%.2f" % sc)
        if tag != "OK":
            bad.append((i, tag))
        print("ch%03d %5.2f hz=%d dup=%.3f q=%d %s" % (i, sc, h, dr, body.count("「"), tag))
    print("--- bad=%d ---" % len(bad))
    return bad


if __name__ == "__main__":
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    qa_range(lo, hi)
