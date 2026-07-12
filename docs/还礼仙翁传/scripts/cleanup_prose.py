#!/usr/bin/env python3
"""精修清理：剥离 footer 后 orphan、去重、去模板段。不自动加厚。"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from prose_utils import clean_body, extract_body_and_footer

ROOT = Path(__file__).resolve().parent.parent
PROSE = ROOT / "prose"
CANON = re.compile(r"ch0(0[1-9]|[12][0-9]|30|3[1-9]|[4-5][0-9]|60|61)")


def main() -> None:
    n = 0
    for p in sorted(PROSE.glob("ch*.md")):
        if not CANON.match(p.name):
            continue
        text = p.read_text(encoding="utf-8")
        body, footer = extract_body_and_footer(text)
        body = clean_body(body)
        if not footer:
            footer = f"---\n\n*（上架连载稿 · {p.stem.split('-', 1)[1]}）*\n"
        p.write_text(body.rstrip() + "\n\n" + footer, encoding="utf-8")
        n += 1
    print(f"Cleaned {n} chapters")
    subprocess.run([sys.executable, str(Path(__file__).parent / "count_prose.py")], check=True)


if __name__ == "__main__":
    main()
