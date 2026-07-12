# -*- coding: utf-8 -*-
"""v47 · 正文内嵌状态行移至章末 · 统一 ---/章末 结构"""
from __future__ import annotations

import glob
import os
import re

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
STATUS_RE = re.compile(
    r"\*\*状态\*\*：[^\n]+"
)
END_MARK = "\n\n---\n\n章末"


def fix_file(path: str) -> tuple[int, bool]:
    n = int(re.search(r"ch(\d+)", path).group(1))
    raw = open(path, encoding="utf-8").read()
    m = STATUS_RE.search(raw)
    if not m:
        return n, False
    status_line = m.group(0).strip()
    # remove status from anywhere
    text = raw[: m.start()] + raw[m.end() :]
    text = text.replace(status_line, "")
    # clean trailing whitespace / duplicate ---
    text = re.sub(r"\n-{3,}\s*\n*", "\n", text)
    text = text.rstrip()
    # rebuild footer
    foot_m = re.search(r"（对照 `05`[^）]+）", text)
    footnote = foot_m.group(0) if foot_m else f"（对照 `05` §{n} · **v47爆款10**）"
    if "v47爆款10" not in footnote:
        footnote = footnote.replace("）", " · **v47爆款10**）", 1)
    # strip old footer block after 章末 if messy
    if END_MARK in text:
        body = text.split(END_MARK, 1)[0].rstrip()
    elif "\n章末" in text:
        body = text.split("\n章末", 1)[0].rstrip()
    else:
        if foot_m:
            body = text[: foot_m.start()].rstrip()
        else:
            body = text.rstrip()
    out = body + END_MARK + "\n\n" + footnote + "\n\n" + status_line + "\n"
    open(path, "w", encoding="utf-8").write(out)
    return n, True


def main():
    fixed = [fix_file(p) for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md")))]
    done = [n for n, ok in fixed if ok]
    print("FIXED", len(done), done)


if __name__ == "__main__":
    main()
