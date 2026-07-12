# -*- coding: utf-8 -*-
"""正文解析 · 字数统计（韩泥线）"""
from __future__ import annotations

import re

# v39b：留存优先 · 单章下限 1500 可接受；2000 为理想非硬闸
TARGET_LO = 1500
TARGET_HI = 3000
TARGET_IDEAL = 2000

FOOTER_TAG = re.compile(r"^\（对照 `05`", re.MULTILINE)


def hz(s: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)


def extract_body_and_footer(text: str) -> tuple[str, str]:
    m = re.search(r"\n---\n\n章末", text)
    if not m:
        m2 = re.search(r"\n\*\*状态\*\*", text)
        if m2:
            head = text[: m2.start()].rstrip()
            tail = text[m2.start() :]
            return head, tail
        return text.rstrip(), ""
    body = text[: m.start()].rstrip()
    footer = text[m.start() :]
    return body, footer


def body_chars(text: str) -> int:
    body, _ = extract_body_and_footer(text)
    return hz(body)
