#!/usr/bin/env python3
"""正文/footer 解析与清理 · 统一口径（认首个 *（上架连载稿…）*）"""
from __future__ import annotations

import re

FOOTER_TAG = re.compile(r"^\*（上架连载稿[^\n]*）\*\s*$", re.MULTILINE)
FOOTER_SEP = re.compile(r"\n---\s*\n\s*$")

BOILERPLATE = (
    "的余波，还在外门盘桓",
    "余波还在东南",
    "哼里空一线——线若拉满",
    "踮脚像钩——钩向下章",
    "霍镇山按刀，刀稳半寸",
    "柳青鸢远观，剑穗无风，风像从塔意借来",
    "添油加醋，添到莫长春成了装神弄鬼",
    "风过山门，袖仍空，塔意却沉",
    "弟子终于肯散，散时仍有人忍不住再瞧一眼灰袍袖空",
    "他笑：「等。」",
    "他笑：「等。",
)


def hz(s: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)


def extract_body_and_footer(text: str) -> tuple[str, str]:
    """取第一个 footer 之前为正文；仅当 --- 紧贴 footer 前时才剥离。"""
    matches = list(FOOTER_TAG.finditer(text))
    if not matches:
        return text.rstrip(), ""
    fm = matches[0]
    head = text[: fm.start()]
    sep = FOOTER_SEP.search(head)
    if sep:
        body = head[: sep.start()].rstrip()
        footer = text[sep.start() : fm.end()].strip() + "\n"
    else:
        body = head.rstrip()
        tag = text[fm.start() : fm.end()].strip()
        footer = f"---\n\n{tag}\n"
    return body, footer


def clean_body(body: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    kept, seen = [], set()
    for p in paras:
        if any(m in p for m in BOILERPLATE):
            continue
        n = norm(p)
        if len(n) >= 36 and n in seen:
            continue
        if len(n) >= 36:
            seen.add(n)
        kept.append(p)
    return "\n\n".join(kept)


def body_chars(text: str) -> int:
    body, _ = extract_body_and_footer(text)
    return hz(clean_body(body))
