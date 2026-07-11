# -*- coding: utf-8 -*-
"""Scan vol03 chapters for duplicate paragraphs."""
import re
from pathlib import Path

VOL3 = Path(__file__).resolve().parents[1] / "chapters" / "vol03-幽灯枯骨.md"
CN = {
    "九十一": 91, "九十二": 92, "九十三": 93, "九十四": 94, "九十五": 95,
    "九十六": 96, "九十七": 97, "九十八": 98, "九十九": 99,
    "一百": 100, "一百零一": 101, "一百零二": 102, "一百零三": 103,
    "一百零四": 104, "一百零五": 105, "一百零六": 106, "一百零七": 107,
    "一百零八": 108, "一百零九": 109, "一百一十": 110, "一百一十一": 111,
    "一百一十二": 112, "一百一十三": 113, "一百一十四": 114, "一百一十五": 115,
    "一百一十六": 116, "一百一十七": 117, "一百一十八": 118, "一百一十九": 119,
    "一百二十": 120, "一百二十一": 121, "一百二十二": 122, "一百二十三": 123,
    "一百二十四": 124, "一百二十五": 125, "一百二十六": 126, "一百二十七": 127,
    "一百二十八": 128, "一百二十九": 129, "一百三十": 130, "一百三十一": 131,
    "一百三十二": 132, "一百三十三": 133, "一百三十四": 134, "一百三十五": 135,
    "一百三十六": 136, "一百三十七": 137, "一百三十八": 138, "一百三十九": 139,
    "一百四十": 140,
}


def cn_to_int(s):
    for k, v in sorted(CN.items(), key=lambda x: -len(x[0])):
        if k in s:
            return v
    return 0


def main():
    t = VOL3.read_text(encoding="utf-8")
    chunks = re.split(r"(?=^### 第)", t, flags=re.M)
    for ch in chunks:
        m = re.match(r"^### (第.+?章 .+)", ch)
        if not m:
            continue
        title = m.group(1)
        num = cn_to_int(title)
        if num < 118:
            continue
        body = ch[len(m.group(0)) :]
        paras = [
            x.strip()
            for x in re.split(r"\n\s*\n", body)
            if len(re.sub(r"\s", "", x)) > 35
        ]
        seen = {}
        dups = 0
        for para in paras:
            key = re.sub(r"\s+", "", para)
            if key in seen:
                dups += 1
            else:
                seen[key] = 1
        hz = len(re.sub(r"\s", "", body)) // 2
        flag = " ***" if dups >= 3 else (" **" if dups >= 1 else "")
        print(f"ch{num:03d} {title.split(' ',1)[1][:8]:8s} ~{hz:4d}字 paras={len(paras):2d} dup={dups}{flag}")


if __name__ == "__main__":
    main()
