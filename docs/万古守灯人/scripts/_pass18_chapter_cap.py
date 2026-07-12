# -*- coding: utf-8 -*-
"""Pass18: cap chapters to 2000-3000 han (editor standard). Trim >3000."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
MIN_HAN = 2000
MAX_HAN = 3000
TARGET = 2950  # trim toward upper band, leave headroom

META_PATTERNS = [
    r"^馈灯链：.*$",
    r"^馈灯①：.*$",
    r"^他不邀功，只把半滴油、一条路写进留灯账。$",
    r"^留灯账：.*$",
    r"^守岁灯芯微温，馈缘↑.*$",
]


def han_count(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def dedupe_paragraphs(body):
    paras = re.split(r"\n\s*\n", body.strip())
    seen, out = [], []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        key = re.sub(r"\s+", "", p)
        if len(key) < 28:
            out.append(p)
            continue
        dup = False
        for sk in seen:
            if key == sk:
                dup = True
                break
            if len(key) > 45 and len(sk) > 45:
                a, b = (key, sk) if len(key) < len(sk) else (sk, key)
                if a in b and len(a) / len(b) > 0.62:
                    dup = True
                    break
        if not dup:
            seen.append(key)
            out.append(p)
    return "\n\n".join(out) + ("\n" if out else "")


def strip_meta_lines(body):
    lines = body.split("\n")
    out = []
    for line in lines:
        skip = False
        for pat in META_PATTERNS:
            if re.match(pat, line.strip()):
                skip = True
                break
        if not skip:
            out.append(line)
    return "\n".join(out)


def is_summary_para(p):
    """Trailing chapter-end summary / theme echo paragraphs."""
    key = re.sub(r"\s+", "", p)
    if len(key) < 20:
        return False
    markers = [
        "这一夜", "这一章", "天明只是", "不是到岸", "顾迟年知道",
        "凡人", "留灯", "急什么，灯还亮", "节奏", "爽不在",
        "后半夜", "天亮", "过关", "才刚开始",
    ]
    hits = sum(1 for m in markers if m in p)
    return hits >= 2 and len(key) < 120


def trim_body(body, max_han=MAX_HAN):
    body = strip_meta_lines(body)
    body = dedupe_paragraphs(body)
    if han_count(body) <= max_han:
        return body

    paras = [p.strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]

    # Drop trailing summary-style paragraphs first
    while paras and han_count("\n\n".join(paras)) > max_han:
        if is_summary_para(paras[-1]):
            paras.pop()
        else:
            break

    # Drop duplicate-ish trailing paras (similar to previous)
    while len(paras) > 3 and han_count("\n\n".join(paras)) > max_han:
        last, prev = paras[-1], paras[-2]
        k1, k2 = re.sub(r"\s+", "", last), re.sub(r"\s+", "", prev)
        if len(k1) > 30 and (k1 in k2 or k2 in k1 or k1[:40] == k2[:40]):
            paras.pop()
        else:
            break

    # Trim from end: remove shortest non-dialogue paragraphs
    while paras and han_count("\n\n".join(paras)) > max_han:
        # prefer removing last paragraph if long enough
        paras.pop()

    body = "\n\n".join(paras)
    if body and not body.endswith("\n"):
        body += "\n"
    return body


def process_file(path):
    text = path.read_text(encoding="utf-8")
    changed = []

    def repl(m):
        title = m.group(1)
        body = m.group(2)
        before = han_count(body)
        if before <= MAX_HAN:
            return m.group(0)
        new_body = trim_body(body)
        after = han_count(new_body)
        if after != before:
            changed.append((title.strip()[:30], before, after))
        return f"### {title}\n{new_body}"

    new_text = re.sub(
        r"### (第.{1,8}章[^\n]*)\n(.*?)(?=\n---\n|\n### 第|\Z)",
        repl,
        text,
        flags=re.S,
    )
    if changed:
        path.write_text(new_text, encoding="utf-8")
    return changed


def audit():
    over = under = ok = 0
    for fp in sorted(CHAPTERS.glob("vol*.md")):
        t = fp.read_text(encoding="utf-8")
        for m in re.finditer(
            r"### 第.{1,8}章[^\n]*\n(.*?)(?=\n---\n|\n### 第|\Z)", t, re.S
        ):
            c = han_count(m.group(1))
            if c > MAX_HAN:
                over += 1
            elif c < MIN_HAN:
                under += 1
            else:
                ok += 1
    print(f"OK {MIN_HAN}-{MAX_HAN}: {ok}  UNDER: {under}  OVER: {over}")


if __name__ == "__main__":
    all_changes = []
    for fp in sorted(CHAPTERS.glob("vol*.md")):
        ch = process_file(fp)
        all_changes.extend(ch)
    print(f"Trimmed {len(all_changes)} chapters")
    for title, b, a in sorted(all_changes, key=lambda x: x[1], reverse=True):
        print(f"  {b} -> {a}  {title}")
    audit()
