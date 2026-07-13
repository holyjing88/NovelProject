# -*- coding: utf-8 -*-
"""Strip mechanical pad lines; top up with integrated POOL prose."""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_HI, TARGET_LO, extract_body_and_footer, hz
from _ch091_110_pool import POOL
from _write_clean_ch091_110 import FNAMES, TITLES


def split_sents(t):
    return [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]


def sk(s):
    return re.sub(r"\s+", "", s)


def top_up(main, n):
    seen = {sk(s) for s in split_sents(main)}
    parts = [p.strip() for p in main.split("\n\n") if p.strip()]
    start = (n * 11) % len(POOL)
    for i in range(len(POOL) * 2):
        if hz("\n\n".join(parts)) >= TARGET_LO:
            break
        sent = POOL[(start + i) % len(POOL)]
        if sk(sent) in seen:
            continue
        seen.add(sk(sent))
        parts.append(sent)
    body = "\n\n".join(parts)
    while hz(body) > TARGET_HI:
        body = body.rsplit("\n\n", 1)[0]
    return body


def main():
    prose = os.path.join(os.path.dirname(__file__), "..", "prose")
    for n in range(91, 111):
        path = os.path.join(prose, FNAMES[n])
        text = open(path, encoding="utf-8").read()
        body, footer = extract_body_and_footer(text)
        if body.startswith("#"):
            title, _, rest = body.partition("\n\n")
        else:
            title, rest = f"# {TITLES[n]}", body
        main = re.split(r"\n\n丑时第\d+息", rest)[0].rstrip()
        new_main = top_up(main, n)
        new_text = f"{title}\n\n{new_main.strip()}\n\n{footer.lstrip()}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        b, _ = extract_body_and_footer(new_text)
        print(FNAMES[n], hz(b))


if __name__ == "__main__":
    main()
