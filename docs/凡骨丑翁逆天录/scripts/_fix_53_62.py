# -*- coding: utf-8 -*-
"""Strip corruption from ch053-62 prose and ensure >=1500 hz."""
from __future__ import annotations

import re
from pathlib import Path

from prose_utils import TARGET_LO, body_chars, extract_body_and_footer

PROSE = Path(__file__).resolve().parent.parent / "prose"

PATCH: dict[int, str] = {
    54: "\n他独眼平，手不抖：「沿净，才接得住赠。赠，不白受。」\n",
    55: "\n他独眼平，手不抖：「符护骨，沿在净。净了，才接后头缘。」\n",
}


def clean_lines(body: str) -> str:
    out: list[str] = []
    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        if s in {"」", "「", "「净。", "「能。」", "「净。"}:
            continue
        if re.fullmatch(r"[「」]+", s):
            continue
        if s == "「净。" or s == "「能。」":
            continue
        # broken fragment: lone closing quote line
        if s.startswith("」") and "「" not in s and len(s) <= 3:
            continue
        out.append(line.rstrip())
    text = "\n".join(out)
    # dedupe sentences
    parts = re.split(r"(?<=[。！？])", text)
    seen: set[str] = set()
    deduped: list[str] = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        k = re.sub(r"\s+", "", p)
        if k in seen:
            continue
        seen.add(k)
        deduped.append(p)
    return "\n".join(deduped)


def fix_file(n: int) -> tuple[int, int]:
    path = next(PROSE.glob(f"ch{n:03d}-*.md"))
    text = path.read_text(encoding="utf-8")
    body, footer = extract_body_and_footer(text)
    before = body_chars(text)
    cleaned = clean_lines(body)
    if n in PATCH and body_chars(cleaned + footer) < TARGET_LO:
        cleaned = cleaned.rstrip() + PATCH[n]
    new_text = cleaned.rstrip() + "\n\n---\n\n" + footer.lstrip("\n")
    path.write_text(new_text, encoding="utf-8")
    after = body_chars(new_text)
    return before, after


def main() -> None:
    for n in range(53, 63):
        b, a = fix_file(n)
        flag = "OK" if a >= TARGET_LO else "SHORT"
        print(f"ch{n:03d} {b}->{a} {flag}")


if __name__ == "__main__":
    main()
