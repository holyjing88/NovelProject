#!/usr/bin/env python3
"""最小精修：仅删 footer 后 orphan、模板段、精确重复段。"""
from __future__ import annotations

import re
from pathlib import Path

PROSE = Path(__file__).resolve().parent.parent / "prose"
CANON = re.compile(r"ch0(0[1-9]|[12][0-9]|30|3[1-9]|[4-5][0-9]|60|61)")
FOOTER_TAG = re.compile(r"^\*（上架连载稿[^\n]*\*\)\s*$", re.MULTILINE)

BOILERPLATE = (
    "的余波，还在外门盘桓",
    "哼里空一线——线若拉满",
    "踮脚像钩——钩向下章",
    "盘桓里掺敬，敬里掺怕，怕里掺盼",
    "添油加醋，添到莫长春成了装神弄鬼",
    "霍镇山按刀，刀稳半寸，稳里战意仍热",
    "柳青鸢远观，剑穗无风，风像从塔意借来",
)


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)


def split_safe(text: str) -> tuple[str, str]:
    matches = list(FOOTER_TAG.finditer(text))
    if not matches:
        return text.rstrip(), ""
    fm = matches[-1]
    head = text[: fm.start()]
    search = head[-400:] if len(head) > 400 else head
    rel = search.rfind("\n---\n")
    if rel >= 0:
        cut = len(head) - len(search) + rel
        body = head[:cut].rstrip()
        footer = text[cut : fm.end()]
    else:
        body = head.rstrip()
        footer = text[fm.start() : fm.end()]
    return body, footer if footer.endswith("\n") else footer + "\n"


def clean(body: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    kept, seen = [], set()
    for p in paras:
        if any(m in p for m in BOILERPLATE):
            continue
        n = norm(p)
        if n in seen:
            continue
        seen.add(n)
        kept.append(p)
    return "\n\n".join(kept) + ("\n" if kept else "")


def main() -> None:
    n = 0
    for p in sorted(PROSE.glob("ch*.md")):
        if not CANON.match(p.name):
            continue
        t = p.read_text(encoding="utf-8")
        body, footer = split_safe(t)
        body = clean(body)
        if not footer:
            footer = f"\n---\n\n*（上架连载稿 · {p.stem.split('-',1)[1]}）*\n"
        new = body.rstrip() + "\n" + footer
        if new != t:
            p.write_text(new, encoding="utf-8")
            n += 1
    print(f"minimal refine: {n} files")


if __name__ == "__main__":
    main()
