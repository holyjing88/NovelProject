#!/usr/bin/env python3
"""Batch cleanup: vol3 meta narration; vol5 duplicate tail padding."""
import re
from pathlib import Path

CHAPTERS = Path(__file__).resolve().parent.parent / "chapters"


def dedupe_paragraphs(text: str) -> str:
    paras = re.split(r"\n\s*\n", text.strip())
    seen = set()
    kept = []
    for p in paras:
        key = re.sub(r"\s+", "", p)
        if key in seen:
            continue
        seen.add(key)
        kept.append(p)
    return "\n\n".join(kept) + ("\n" if text.endswith("\n") else "")


def clean_vol3(text: str) -> str:
    text = text.replace("知下一章更险", "知下一夜更险")
    text = text.replace("下一章，更险", "下一夜，更险")
    text = text.replace("下一章更险", "下一夜更险")
    text = text.replace("下一章，陆承安", "下一夜，陆承安")
    text = text.replace("下一章，敛灯崖", "下一程，敛灯崖")
    text = re.sub(r"^章末，", "", text, flags=re.MULTILINE)
    return text


def clean_vol5_chapter(body: str) -> str:
    # Remove consecutive duplicate lines containing tail padding
    lines = body.split("\n")
    out = []
    prev_key = None
    for line in lines:
        key = re.sub(r"\s+", "", line)
        if "五灯虽缺程不二" in line and key == prev_key:
            continue
        if "霍照临剑在，沈青禾油在" in line and key == prev_key:
            continue
        out.append(line)
        if line.strip():
            prev_key = key
    body = "\n".join(out)
    # Dedupe identical paragraphs within chapter
    return dedupe_paragraphs(body)


def process_vol3():
    p = CHAPTERS / "vol03-幽灯枯骨.md"
    t = p.read_text(encoding="utf-8")
    parts = re.split(r"(?=### 第)", t)
    head, chs = parts[0], parts[1:]
    new_chs = []
    for ch in chs:
        m = re.match(r"(### 第[^\n]+\n)(.*)", ch, re.S)
        if not m:
            new_chs.append(ch)
            continue
        head_ch, body = m.group(1), m.group(2)
        body = clean_vol3(body)
        body = dedupe_paragraphs(body)
        new_chs.append(head_ch + body)
    p.write_text(head + "".join(new_chs), encoding="utf-8")
    print("vol3 cleaned")


def process_vol5():
    p = CHAPTERS / "vol05-万古长明.md"
    t = p.read_text(encoding="utf-8")
    parts = re.split(r"(?=### 第)", t)
    head, chs = parts[0], parts[1:]
    new_chs = []
    for ch in chs:
        m = re.match(r"(### 第[^\n]+\n)(.*)", ch, re.S)
        if not m:
            new_chs.append(ch)
            continue
        head_ch, body = m.group(1), m.group(2)
        body = clean_vol5_chapter(body)
        new_chs.append(head_ch + body)
    p.write_text(head + "".join(new_chs), encoding="utf-8")
    print("vol5 cleaned")


if __name__ == "__main__":
    process_vol3()
    process_vol5()
