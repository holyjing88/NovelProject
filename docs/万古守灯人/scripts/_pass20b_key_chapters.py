# -*- coding: utf-8 -*-
"""Pass20b: replace key chapters with deduped source; dedupe echo spam."""
import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from _pass19_short_boost import (
    ch_num_from_title,
    han_count,
    load_py_chapters,
    parse_file,
    rebuild,
    dedupe_paragraphs,
    trim_body,
    MIN_HAN,
    MAX_HAN,
    CHAPTERS_DIR,
)
from _pass20_polish import remove_duplicate_templates_only, load_pass12_ch160

_expand = load_py_chapters(SCRIPTS / "_vol4_expand_all.py")
KEY_CHS = {
    160: remove_duplicate_templates_only(_expand.get(160, load_pass12_ch160() or "")),
    **{
        k: remove_duplicate_templates_only(v)
        for k, v in _expand.items()
        if k in {161, 162, 185, 186, 188, 189, 190, 210, 214, 215, 220}
    },
}


def fix_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    chunks = parse_file(text)
    n = 0
    new = []
    for title, body in chunks:
        num = ch_num_from_title(title)
        if num in KEY_CHS and KEY_CHS[num]:
            body = dedupe_paragraphs(KEY_CHS[num].strip())
            if han_count(body) > MAX_HAN:
                body = trim_body(body)
            if han_count(body) >= MIN_HAN:
                body = body + "\n" if not body.endswith("\n") else body
                n += 1
        else:
            cleaned = dedupe_paragraphs(remove_duplicate_templates_only(body))
            if MIN_HAN <= han_count(cleaned) <= MAX_HAN:
                body = cleaned if cleaned.endswith("\n") else cleaned + "\n"
        new.append((title, body))
    if n:
        path.write_text(rebuild(text, new), encoding="utf-8")
    return n


def main():
    total = 0
    for fp in sorted(CHAPTERS_DIR.glob("vol*.md")):
        c = fix_file(fp)
        if c:
            print(fp.name, c, "key chapters")
            total += c
    ok = under = over = 0
    for fp in sorted(CHAPTERS_DIR.glob("vol*.md")):
        for _, b in parse_file(fp.read_text(encoding="utf-8")):
            h = han_count(b)
            if h < MIN_HAN:
                under += 1
            elif h > MAX_HAN:
                over += 1
            else:
                ok += 1
    print(f"fixed {total} key inserts | OK {ok} UNDER {under} OVER {over}")


if __name__ == "__main__":
    main()
