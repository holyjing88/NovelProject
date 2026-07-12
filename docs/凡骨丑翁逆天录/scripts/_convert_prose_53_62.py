# -*- coding: utf-8 -*-
"""Convert prose ch053-062 to ch050 paragraph format (v3)."""
from __future__ import annotations

import re
from pathlib import Path

from prose_utils import extract_body_and_footer, hz

PROSE = Path(__file__).resolve().parent.parent / "prose"
OUT = Path(__file__).resolve().parent / "_bodies_clean_53_62.py"

TARGET_LO = 1550
TARGET_HI = 1900

# Padding handled by _postprocess_bodies.py
PAD: dict[int, str] = {}


def is_orphan(s: str) -> bool:
    s = s.strip()
    if s in {"」", "「"} or re.fullmatch(r"[「」]+", s):
        return True
    if s.startswith("」") and "「" not in s and len(s) <= 4:
        return True
    return False


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
        open_q = prev.count("「") - prev.count("」")
        if open_q > 0:
            out[-1] = prev + s
        elif not re.search(r"[。！？]$", prev):
            out[-1] = prev + s
        else:
            out.append(s)
    return out


def to_paragraphs(chunks: list[str], max_hz: int = 170) -> list[str]:
    paras: list[str] = []
    buf = ""
    bhz = 0
    for c in chunks:
        if c == "---":
            if buf:
                paras.append(buf)
                buf = ""
                bhz = 0
            paras.append("---")
            continue
        sents = [x for x in re.split(r"(?<=[。！？])", c) if x.strip()]
        for sent in sents:
            sh = hz(sent)
            if "「" in sent and sh > 50:
                if buf:
                    paras.append(buf)
                    buf = ""
                    bhz = 0
                paras.append(sent)
                continue
            if bhz + sh > max_hz and buf:
                paras.append(buf)
                buf = sent
                bhz = sh
            else:
                buf += sent
                bhz += sh
    if buf:
        paras.append(buf)
    return paras


def fix_orphan_paragraphs(paras: list[str]) -> list[str]:
    fixed: list[str] = []
    for p in paras:
        if p == "---":
            fixed.append(p)
            continue
        p = p.strip()
        if p.startswith("」") and fixed and fixed[-1] != "---":
            fixed[-1] += p
            continue
        fixed.append(p)
    out: list[str] = []
    for p in fixed:
        if p == "---":
            out.append(p)
            continue
        if out and out[-1] != "---" and out[-1].count("「") > out[-1].count("」"):
            out[-1] += p
        else:
            out.append(p)
    return out


def dedupe_sentences_in_body(text: str) -> str:
    paras = text.split("\n\n")
    seen: set[str] = set()
    out: list[str] = []
    for p in paras:
        if p == "---":
            out.append(p)
            continue
        sents = [x for x in re.split(r"(?<=[。！？])", p) if x.strip()]
        kept: list[str] = []
        for s in sents:
            k = re.sub(r"\s+", "", s)
            if k in seen:
                continue
            seen.add(k)
            kept.append(s)
        if kept:
            out.append("".join(kept))
    return "\n\n".join(out).strip()


def body_from_prose(raw: str) -> str:
    lines = [ln.rstrip() for ln in raw.splitlines()]
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    merged = merge_lines(lines)
    paras = fix_orphan_paragraphs(to_paragraphs(merged))
    return "\n\n".join(paras).strip()


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
        text = path.read_text(encoding="utf-8")
        body, _ = extract_body_and_footer(text)
        cleaned = dedupe_sentences_in_body(body_from_prose(body))
        if n in PAD and hz(cleaned) < TARGET_LO:
            cleaned = cleaned.rstrip() + "\n\n" + PAD[n].strip()
            cleaned = dedupe_sentences_in_body(cleaned)
        bodies[n] = cleaned
        h = hz(cleaned)
        d = dup_ratio(cleaned)
        flags = []
        if h < TARGET_LO:
            flags.append("SHORT")
        if h > TARGET_HI:
            flags.append("LONG")
        if d >= 0.02:
            flags.append(f"dup={d:.3f}")
        if re.search(r"\n」|^」", cleaned):
            flags.append("ORPHAN")
        print(f"ch{n:03d} hz={h} dup={d:.3f} {' '.join(flags) or 'OK'}")

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
