# -*- coding: utf-8 -*-
"""Splice expanded ch66-90 into Vol2."""
import re
from pathlib import Path
from _ch66_78_bodies import CHAPTERS as CH66_78
from _ch79_90_bodies import CHAPTERS as CH79_90

ROOT = Path(__file__).resolve().parent
VOL2 = ROOT / "../chapters/vol02-云岚杂役.md"

CHAPTERS = CH66_78 + CH79_90


def count(body: str) -> int:
    return len(re.sub(r"\s", "", body))


def main():
    text = VOL2.read_text(encoding="utf-8")

    head_m = re.search(r"^(.*?)(?=### 第六十六章)", text, re.S | re.M)
    if not head_m:
        raise SystemExit("Could not find ### 第六十六章")
    head = head_m.group(1).rstrip()

    footer_m = re.search(r"(\n---\n\n>\s*第三卷.*)", text, re.S)
    if not footer_m:
        raise SystemExit("Could not find vol3 footer")
    footer = footer_m.group(1).lstrip("\n")

    parts = [head, ""]
    for title, body in CHAPTERS:
        parts.append(f"### {title}")
        parts.append("")
        parts.append(body.strip())
        parts.append("")
        parts.append("---")
        parts.append("")

    parts.append(footer.strip())

    VOL2.write_text("\n".join(parts) + "\n", encoding="utf-8")

    print(f"Spliced {len(CHAPTERS)} chapters into {VOL2.name}")
    for title, body in CHAPTERS:
        n = count(body)
        flag = "OK" if 3500 <= n <= 4500 else ("SHORT" if n < 3500 else "LONG")
        num = re.search(r"第(.+?)章", title)
        label = num.group(1) if num else title
        print(f"  ch{label}: {n} [{flag}]")


if __name__ == "__main__":
    main()
