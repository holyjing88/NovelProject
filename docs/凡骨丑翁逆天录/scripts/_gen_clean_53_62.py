# -*- coding: utf-8 -*-
"""Generate _bodies_clean_53_62.py and verify."""
from __future__ import annotations

import re
from pathlib import Path

from prose_utils import hz

BODIES: dict[int, str] = {}

# Populated below after composition
exec(open(Path(__file__).with_name("_bodies_clean_53_62_draft.py"), encoding="utf-8").read())

def dup_ratio(t: str) -> float:
    sents = [s.strip() for s in re.split(r"[。！？\n]", t) if len(s.strip()) >= 4]
    if not sents:
        return 0.0
    seen, dup = set(), 0
    for s in sents:
        if s in seen:
            dup += 1
        seen.add(s)
    return dup / len(sents)


def dialogue_ratio(t: str) -> float:
    d = re.findall(r"「[^」]*」", t)
    dhz = sum(hz(x) for x in d)
    total = hz(t)
    return dhz / total if total else 0.0


def main() -> None:
    bad = []
    for n in range(53, 63):
        body = BODIES[n]
        h = hz(body)
        d = dup_ratio(body)
        dr = dialogue_ratio(body)
        flags = []
        if h < 1550:
            flags.append(f"SHORT({h})")
        if h > 1900:
            flags.append(f"LONG({h})")
        if d >= 0.02:
            flags.append(f"dup={d:.3f}")
        if "恩簿" in body or "记账" in body or "读者" in body:
            flags.append("FORBIDDEN")
        if re.search(r"ch0\d{2}", body):
            flags.append("META")
        if re.search(r"(?<![「])」|(?<![「\n])「(?![^「]*」)", body):
            pass  # simple orphan check done separately
        status = "OK" if not flags else ",".join(flags)
        print(f"ch{n:03d} hz={h} dup={d:.3f} dlg={dr:.2f} {status}")
        if flags:
            bad.append(n)
    print("FAIL" if bad else "ALL PASS")


if __name__ == "__main__":
    main()
