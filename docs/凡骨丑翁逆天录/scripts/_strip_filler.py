# -*- coding: utf-8 -*-
"""Strip 丑时第N息 filler and report counts."""
import re, glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import hz, extract_body_and_footer, TARGET_LO, TARGET_HI

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
FILLER = re.compile(r"^丑时第\d+息.*$", re.MULTILINE)


def dup(t):
    s = [x.strip() for x in re.split(r"(?<=[。！？])", t) if len(x.strip()) >= 8]
    if not s:
        return 0.0
    seen, d = set(), 0
    for x in s:
        k = re.sub(r"\s+", "", x)
        if k in seen:
            d += 1
        seen.add(k)
    return d / len(s)


def strip_file(path):
    raw = open(path, encoding="utf-8").read()
    body, footer = extract_body_and_footer(raw)
    # strip filler lines
    lines = body.split("\n")
    cleaned = []
    for line in lines:
        if FILLER.match(line.strip()):
            continue
        cleaned.append(line)
    body2 = "\n".join(cleaned)
    body2 = re.sub(r"\n{3,}", "\n\n", body2).strip()
    title = body2.split("\n\n")[0] if body2.startswith("#") else raw.split("\n\n")[0]
    if body2.startswith("#"):
        main = body2.split("\n\n", 1)[1]
    else:
        main = body2
    full = title + "\n\n" + main + "\n\n" + footer.lstrip("\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write(full.strip() + "\n")
    return hz(title + "\n\n" + main)


def main():
    files = sorted(
        glob.glob(os.path.join(PROSE, "ch09[1-9]-*.md"))
        + glob.glob(os.path.join(PROSE, "ch10[0-9]-*.md"))
        + glob.glob(os.path.join(PROSE, "ch110-*.md"))
    )
    print("After strip:")
    for p in files:
        h = strip_file(p)
        raw = open(p, encoding="utf-8").read()
        b, _ = extract_body_and_footer(raw)
        print(os.path.basename(p), hz(b), "need", max(0, TARGET_LO - hz(b)))


if __name__ == "__main__":
    main()
