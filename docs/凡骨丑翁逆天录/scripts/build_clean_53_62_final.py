# -*- coding: utf-8 -*-
"""Build final _bodies_clean_53_62.py from prose with padding."""
from __future__ import annotations

import re
from pathlib import Path

from prose_utils import extract_body_and_footer, hz

PROSE = Path(__file__).resolve().parent.parent / "prose"
OUT = Path(__file__).resolve().parent / "_bodies_clean_53_62.py"
TARGET_LO = 1550

PAD: dict[int, str] = {
    55: "僧离亭那日，他符藏怀，不示，不燃，像经片挪了地方。",
    56: "季末第五日，筐末扎紧，扎紧像秤杆落盘，落盘手还在。管事验筐底：「底不塌，季末记功。」韩泥不邀功。",
    57: "试手前夜，药涂裂口，凉后稳，稳像鼻下静移到掌上。外头更鼓二响，响沉。明日卯时，坡下见。",
    58: "试手日午后，肩稳，像坡下站出来的实，实不在灵，在手。血到了席，没到沿，沿不接。",
    59: "沿前即止那日，席边湿一线，湿不到沿，沿不接，缘在等。赖福远处骂，骂轻，韩泥擦沿的手却更稳。清晨霜白，丙九静一寸，静一寸，像沿前那一止。他独眼平，手不抖：「沿前即止，不接沿。」坛腹温一线，贴掌，像听「止」字。",
}


def is_orphan(s: str) -> bool:
    s = s.strip()
    return s in {"「", "」"} or (s.startswith("」") and "「" not in s and len(s) <= 4)


def merge_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if is_orphan(s):
            if out and s.startswith("」"):
                out[-1] += s
            continue
        if s == "---":
            out.append("---")
            continue
        if not out or out[-1] == "---":
            out.append(s)
            continue
        prev = out[-1]
        if prev.count("「") > prev.count("」") or not re.search(r"[。！？]$", prev):
            out[-1] = prev + s
        else:
            out.append(s)
    return out


def to_body(raw: str) -> str:
    lines = [ln.rstrip() for ln in raw.splitlines()]
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    merged = merge_lines(lines)
    paras: list[str] = []
    buf = ""
    for m in merged:
        if m == "---":
            if buf:
                paras.append(buf)
                buf = ""
            paras.append("---")
        else:
            if buf and hz(buf) + hz(m) > 170:
                paras.append(buf)
                buf = m
            else:
                buf += m
    if buf:
        paras.append(buf)
    text = "\n\n".join(paras)
    text = re.sub(r"\n\n」", "", text)
    text = re.sub(r"^」", "", text)
    return text.strip()


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


def main() -> None:
    bodies: dict[int, str] = {}
    for n in range(53, 63):
        path = next(PROSE.glob(f"ch{n:03d}-*.md"))
        body, _ = extract_body_and_footer(path.read_text(encoding="utf-8"))
        text = to_body(body)
        if n in PAD and hz(text) < TARGET_LO:
            text = text.rstrip() + "\n\n---\n\n" + PAD[n]
        bodies[n] = text
        h = hz(text)
        d = dup_ratio(text)
        ok = h >= TARGET_LO and h <= 1900 and d < 0.02
        print(f"ch{n:03d} hz={h} dup={d:.3f} {'OK' if ok else 'FAIL'}")

    lines = [
        "# -*- coding: utf-8 -*-",
        '"""Clean chapter bodies 53-62 — ch050 prose format."""',
        "",
        "BODIES = {",
    ]
    for n in range(53, 63):
        escaped = bodies[n].replace('"""', '\\"\\"\\"')
        comma = "," if n < 62 else ""
        lines.append(f'    {n}: """{escaped}"""{comma}')
    lines.append("}")
    lines.extend(
        [
            "",
            "",
            'if __name__ == "__main__":',
            "    import re",
            "    from prose_utils import hz",
            "",
            "    def dup_ratio(t: str) -> float:",
            '        sents = [s.strip() for s in re.split(r"[。！？\\n]", t) if len(s.strip()) >= 4]',
            "        if not sents:",
            "            return 0.0",
            "        seen, dup = set(), 0",
            "        for s in sents:",
            "            if s in seen:",
            "                dup += 1",
            "            seen.add(s)",
            "        return dup / len(sents)",
            "",
            "    for n in range(53, 63):",
            "        body = BODIES[n]",
            '        print(f"ch{n:03d} hz={hz(body)} dup={dup_ratio(body):.3f}")',
            "",
        ]
    )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
