# -*- coding: utf-8 -*-
"""仅清除 PAD 套话与重复「坛沿一线温」，不改其他正文。"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import body_chars, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")
PAD_BLOCK = re.compile(
    r"\n*他按坛沿，只记，不飘。飘了，恩断；恩不断，手就稳，稳了，明日还有活，活才能还。"
    r"还远不怕，怕的是汤凉——汤在叶铺，在刘婆灶，在心里，心里那格留给烫，烫字不写，按在胃上。\n*",
    re.S,
)
PAD_LINE = re.compile(
    r"(?:坛沿一线温，像还路又近一分。近一分，手稳一分，恩不断一分。(?:手稳，才配明日还有活；活，才配还。\n*)?)+",
    re.S,
)
META = (
    ("满在读者心，也在他心里", "满在心里，也在他心里"),
    ("读者怒值才值得", "怒值才值得"),
    ("读者能答", "旁人能答"),
    ("读者若问", "旁人若问"),
    ("读者才肯", "名节才"),
    ("读者下一章", "锤落"),
)

def scrub(text: str) -> str:
    body, foot = extract_body_and_footer(text)
    body = PAD_BLOCK.sub("\n\n", body)
    body = PAD_LINE.sub("", body)
    for a, b in META:
        body = body.replace(a, b)
        foot = foot.replace(a, b)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return (body + "\n\n" + foot) if foot else body + "\n"

n = 0
for p in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
    ch = int(re.search(r"ch(\d+)", p).group(1))
    if ch > 49:
        continue
    t = open(p, encoding="utf-8").read()
    new = scrub(t)
    if new != t:
        open(p, "w", encoding="utf-8", newline="\n").write(new)
        n += 1
    print(f"ch{ch:03d} {body_chars(new)} pad={new.count('坛沿一线温')} reader={'读者' in new}")
print(f"scrubbed {n}")
