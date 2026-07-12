#!/usr/bin/env python3
"""轻量精修：footer 归位、剔除模板段、精确去重（不删加厚正文）。"""
from __future__ import annotations

import re
from pathlib import Path

PROSE = Path(__file__).resolve().parent.parent / "prose"
CANONICAL_RE = re.compile(r"ch0(0[1-9]|[12][0-9]|30|3[1-9]|[4-5][0-9]|60|61)")
FOOTER_START = re.compile(r"\n---\n+\*（上架连载稿[^\n]*\*\)\s*")

BOILERPLATE_MARKERS = (
    "的余波，还在外门盘桓",
    "哼里空一线——线若拉满",
    "踮脚像钩——钩向下章",
    "盘桓里掺敬，敬里掺怕，怕里掺盼",
    "添油加醋，添到莫长春成了装神弄鬼",
    "莫长春望天，星稀，袖仍空，空里像",
    "塔鸣极轻，轻像还礼未完",
    "回头处，下章的灯亮了一线",
    "苏念慈隔窗，妒里掺敬，低声：「别传成辱。」顾小满扫阶",
    "霍镇山按刀，刀稳半寸，稳里战意仍热",
    "弟子讲碎又拼，拼得像戏本",
    "礼不在舌，在塔里",
    "风过，袖仍空，塔意却沉。莫长春不辩，只把",
)

V16_FIXES = (
    ("莫长春未进门，只在门外廊柱旁拄杖", "莫长春未进门，袖空，一念出塔，杖立门外廊柱旁"),
    ("莫长春门外杖点地", "莫长春袖空，一念出塔，门外杖点地"),
    ("莫长春杖点廊石", "莫长春袖空，一念出塔，杖点廊石"),
    ("只在门外廊柱旁拄杖", "袖空，一念出塔，只在门外廊柱旁杖立"),
)


def hz(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def split_parts(text: str) -> tuple[str, str]:
    m = FOOTER_START.search(text)
    if not m:
        return text.rstrip(), ""
    body = text[: m.start()].rstrip()
    rest = text[m.start() :]
    end = rest.find("）*")
    if end >= 0:
        line_end = rest.find("\n", end)
        footer = rest[: line_end + 1].rstrip() + "\n" if line_end >= 0 else rest
    else:
        footer = rest
    return body, footer


def is_boilerplate(para: str) -> bool:
    return any(m in para for m in BOILERPLATE_MARKERS)


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)


def light_dedupe(text: str) -> str:
    paragraphs = [p.strip() for p in re.split(r"\n\n+", text.strip()) if p.strip()]
    kept: list[str] = []
    seen: set[str] = set()
    for p in paragraphs:
        if is_boilerplate(p):
            continue
        n = norm(p)
        if n in seen:
            continue
        seen.add(n)
        kept.append(p)
    return "\n\n".join(kept) + ("\n" if kept else "")


def polish_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    before = hz(re.sub(r"\n---\n+.*", "", text, flags=re.DOTALL))
    body, footer = split_parts(text)
    for old, new in V16_FIXES:
        body = body.replace(old, new)
    body = light_dedupe(body)
    if not footer:
        tag = path.name.replace(".md", "").split("-", 1)[-1]
        footer = f"\n---\n\n*（上架连载稿 · {tag}）*\n"
    new_text = body.rstrip() + "\n" + footer
    after = hz(body)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return {"name": path.name, "before": before, "after": after, "changed": new_text != text}


def main() -> None:
    rows = [polish_file(p) for p in sorted(PROSE.glob("ch*.md")) if CANONICAL_RE.match(p.name)]
    print(f"light polish: {sum(1 for r in rows if r['changed'])}/{len(rows)} changed")


if __name__ == "__main__":
    main()
