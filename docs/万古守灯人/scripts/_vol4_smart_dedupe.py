# -*- coding: utf-8 -*-
"""Smart dedupe for chapters 141-165: remove exact and near-duplicate paragraphs."""
import re
from difflib import SequenceMatcher
from pathlib import Path

VOL4 = Path(__file__).parent / "../chapters/vol04-玄京封灯.md"

# Fallback unique paragraphs if chapter drops below 2500 after dedupe
import importlib.util

_spec = importlib.util.spec_from_file_location(
    "rb", Path(__file__).parent / "_vol4_rebuild_141_165.py"
)
_rb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_rb)
FALLBACK = _rb.EXP


def split_paras(text: str) -> list:
    paras = []
    buf = []
    for line in text.split("\n"):
        if line.strip() == "":
            if buf:
                paras.append("\n".join(buf))
                buf = []
        else:
            buf.append(line)
    if buf:
        paras.append("\n".join(buf))
    return paras


def norm(s: str) -> str:
    return re.sub(r"\s", "", s)


def is_dup(a: str, b: str, threshold=0.95) -> bool:
    na, nb = norm(a), norm(b)
    if len(na) < 20 or len(nb) < 20:
        return na == nb
    # Remove if one paragraph is largely contained in another
    if len(na) > 80 and na in nb:
        return True
    if len(nb) > 80 and nb in na:
        return True
    if na[:50] == nb[:50] and abs(len(na) - len(nb)) < 30:
        return True
    return SequenceMatcher(None, na, nb).ratio() >= threshold


def dedupe(text: str) -> str:
    paras = split_paras(text)
    kept = []
    for p in paras:
        if not p.strip():
            continue
        dup = False
        for k in kept:
            if is_dup(p, k):
                dup = True
                break
        if not dup:
            kept.append(p)
    return "\n\n".join(kept)


def main():
    text = VOL4.read_text(encoding="utf-8")
    start = text.index("### 第一百四十一章")
    end = text.index("### 第一百六十六章")
    section = text[start:end]
    parts = re.split(r"(### 第[一百二三四五六七八九十百零]+章[^\n]+)", section)

    num_map = {
        "一百四十一": 141, "一百四十二": 142, "一百四十三": 143, "一百四十四": 144,
        "一百四十五": 145, "一百四十六": 146, "一百四十七": 147, "一百四十八": 148,
        "一百四十九": 149, "一百五十": 150, "一百五十一": 151, "一百五十二": 152,
        "一百五十三": 153, "一百五十四": 154, "一百五十五": 155, "一百五十六": 156,
        "一百五十七": 157, "一百五十八": 158, "一百五十九": 159, "一百六十": 160,
        "一百六十一": 161, "一百六十二": 162, "一百六十三": 163, "一百六十四": 164,
        "一百六十五": 165,
    }

    rebuilt = []
    counts = {}
    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        m = re.search(r"第([一百二三四五六七八九十百零]+)章", header)
        if not m or m.group(1) not in num_map:
            continue
        n = num_map[m.group(1)]
        body = body.split("\n---")[0].strip()
        body = dedupe(body)
        chars = len(norm(body))
        if chars < 2500 and n in FALLBACK:
            body = body.rstrip() + FALLBACK[n]
            chars = len(norm(body))
        counts[n] = chars
        rebuilt.extend([header, "", body, "", "---", ""])

    new_text = text[:start] + "\n".join(rebuilt) + text[end:]
    VOL4.write_text(new_text, encoding="utf-8")

    for n in sorted(counts):
        c = counts[n]
        flag = "OK" if 2500 <= c <= 4000 else "OUT"
        print(f"Ch {n}: {c} chars [{flag}]")


if __name__ == "__main__":
    main()
