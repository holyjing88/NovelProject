# -*- coding: utf-8 -*-
"""Pass10 P0: dedupe vol04 ch187-190, vol05 ch211; fix ch64 feed marker."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
VOL2 = ROOT / "chapters" / "vol02-云岚杂役.md"
VOL4 = ROOT / "chapters" / "vol04-玄京封灯.md"
VOL5 = ROOT / "chapters" / "vol05-万古长明.md"


def dedupe_consecutive_lines(text):
    lines = text.split("\n")
    out, prev = [], None
    for line in lines:
        s = line.strip()
        if s and s == prev:
            continue
        out.append(line)
        if s:
            prev = s
    return "\n".join(out)


def dedupe_paragraphs(body):
    paras = re.split(r"\n\s*\n", body.strip())
    seen_keys = []
    out = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        key = re.sub(r"\s+", "", p)
        if len(key) < 28:
            out.append(p)
            continue
        dup = False
        for sk in seen_keys:
            if key == sk:
                dup = True
                break
            if len(key) > 45 and len(sk) > 45:
                shorter, longer = (key, sk) if len(key) < len(sk) else (sk, key)
                if shorter in longer and len(shorter) / len(longer) > 0.62:
                    dup = True
                    break
        if not dup:
            seen_keys.append(key)
            out.append(p)
    return "\n\n".join(out) + ("\n" if out else "")


def dedupe_from_chapter(text, start_marker):
    idx = text.find(start_marker)
    if idx < 0:
        return text, False
    head, rest = text[:idx], text[idx:]
    parts = re.split(r"(?=^### 第)", rest, flags=re.M)
    cleaned = []
    for part in parts:
        if not part.strip():
            continue
        m = re.match(r"^(### 第[^\n]+\n)", part)
        if not m:
            cleaned.append(part)
            continue
        title = m.group(1)
        body = part[len(title) :]
        body = dedupe_paragraphs(body)
        body = dedupe_consecutive_lines(body)
        cleaned.append(title + body)
    return head + "".join(cleaned), True


def dedupe_single_chapter(text, start_marker, end_marker):
    s = text.find(start_marker)
    if s < 0:
        return text, False
    e = text.find(end_marker, s + len(start_marker)) if end_marker else len(text)
    if e < 0:
        e = len(text)
    chunk = text[s:e]
    m = re.match(r"^(### 第[^\n]+\n)", chunk)
    if not m:
        return text, False
    title = m.group(1)
    body = chunk[len(title) :]
    body = dedupe_paragraphs(body)
    body = dedupe_consecutive_lines(body)
    new_chunk = title + body
    return text[:s] + new_chunk + text[e:], True


def fix_ch64(text):
    marker = "### 第六十四章 第三层雾"
    end = "### 第六十五章 第六层无心"
    s = text.find(marker)
    e = text.find(end, s)
    if s < 0 or e < 0:
        return text, False
    chunk = text[s:e]
    if "留灯账" in chunk or "馈灯" in chunk or "馈缘" in chunk:
        return text, False
    insert = "\n\n他在留灯账记一行：*塔内验心，记一笔；账在，恩在。*\n\n"
    # insert before final --- block or before end
    if "钟未响" in chunk:
        chunk = chunk.replace(
            "钟未响，芯未落。守岁灯在袖，迟暮之约未断，账算清，手不抖。",
            "钟未响，芯未落。守岁灯在袖，迟暮之约未断，账算清，手不抖。"
            + insert.strip()
            + "\n",
        )
    else:
        chunk = chunk.rstrip() + insert
    return text[:s] + chunk + text[e:], True


def main():
    changes = []

    t2 = VOL2.read_text(encoding="utf-8")
    t2, ok = fix_ch64(t2)
    if ok:
        VOL2.write_text(t2, encoding="utf-8")
        changes.append("vol02 ch64 feed marker")

    t4 = VOL4.read_text(encoding="utf-8")
    t4, ok4 = dedupe_from_chapter(t4, "### 第一百八十七章 气运照见")
    if ok4:
        VOL4.write_text(t4, encoding="utf-8")
        changes.append("vol04 ch187-190 dedupe")

    t5 = VOL5.read_text(encoding="utf-8")
    t5, ok5 = dedupe_single_chapter(
        t5,
        "### 第二百一十一章 魔退人寂",
        "### 第二百一十二章 灯境之寂",
    )
    if ok5:
        VOL5.write_text(t5, encoding="utf-8")
        changes.append("vol05 ch211 dedupe")

    print("done:", ", ".join(changes) or "no changes")


if __name__ == "__main__":
    main()
