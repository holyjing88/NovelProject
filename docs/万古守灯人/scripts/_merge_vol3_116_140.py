# -*- coding: utf-8 -*-
"""Merge expanded chapters 116-140 into vol3 main file."""
import re
import importlib.util
from pathlib import Path

FILE = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol03-幽灯枯骨.md")
MARKER = "### 第一百一十六章"
FOOTER = """---

> 第四卷《玄京风云》（第141–190章）见：`../chapters/vol04-玄京封灯.md`
"""

NUM_CN = {
    116: "一百一十六", 117: "一百一十七", 118: "一百一十八", 119: "一百一十九",
    120: "一百二十", 121: "一百二十一", 122: "一百二十二", 123: "一百二十三",
    124: "一百二十四", 125: "一百二十五", 126: "一百二十六", 127: "一百二十七",
    128: "一百二十八", 129: "一百二十九", 130: "一百三十", 131: "一百三十一",
    132: "一百三十二", 133: "一百三十三", 134: "一百三十四", 135: "一百三十五",
    136: "一百三十六", 137: "一百三十七", 138: "一百三十八", 139: "一百三十九",
    140: "一百四十",
}


def load_chapters(path):
    spec = importlib.util.spec_from_file_location("m", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.CHAPTERS


def count(body):
    return len(re.sub(r"\s", "", body))


def main():
    c1 = load_chapters(Path(__file__).parent / "vol3_ch116_140_content.py")
    c2 = load_chapters(Path(__file__).parent / "vol3_ch131_140_content.py")
    chapters = {**c1, **c2}

    raw = FILE.read_text(encoding="utf-8")
    idx = raw.find(MARKER)
    if idx < 0:
        raise SystemExit("marker not found")
    prefix = raw[:idx].rstrip() + "\n\n---\n\n"

    blocks = []
    total = 0
    print("Chapter char counts (non-whitespace):")
    for n in range(116, 141):
        title, body = chapters[n]
        cn = NUM_CN[n]
        blocks.append(f"### 第{cn}章 {title}\n\n{body.strip()}\n")
        c = count(body)
        total += c
        print(f"  第{cn}章 {title}: {c}")
    print(f"  TOTAL 116-140: {total}")

    out = prefix + "\n---\n\n".join(blocks) + "\n\n" + FOOTER
    FILE.write_text(out, encoding="utf-8")
    print(f"Written to {FILE}")


if __name__ == "__main__":
    main()
