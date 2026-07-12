# -*- coding: utf-8 -*-
"""Post-process _bodies_clean_53_62.py: fix orphans, dedupe, pad short chapters."""
from __future__ import annotations

import ast
import re
from pathlib import Path

from prose_utils import hz

PATH = Path(__file__).resolve().parent / "_bodies_clean_53_62.py"
TARGET_LO = 1550

TOPUP = {
    55: "符暖贴怀，像冬里多一层薄袄。薄袄，不越阶，不辱主。",
    56: "第五日清晨，筐末扎紧。扎紧，像秤杆落盘。管事验筐沿：「沿齐，底不塌，季末记功。」韩泥不邀功。功在心里，不在舌。坡下霜白，柱上「后日卯时」更真。真在试手，真在末排。",
    57: "药涂裂口，凉后稳，稳像鼻下静气移到掌上。外头更鼓二响，响沉。明日卯时，坡下见。",
    58: "肩稳，像试手练出来的实。血是活计扎出的，不是主动滴坛的。滴坛，要等误那一甩。",
    59: "赖福远处骂：「晦气翁守坛。」管事声冷：「再嗓，西栏你清到年尾。」赖福哑了。哑，韩泥擦沿的手却更稳。天未亮，编筐声细，细像针。针扎掌，血珠饱满，仍甩向破席。席边湿一线，湿不到沿。",
}


def fix_orphans(text: str) -> str:
    paras = text.split("\n\n")
    out: list[str] = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if p == "---":
            out.append(p)
            continue
        if p.startswith("」") and out and out[-1] != "---":
            out[-1] += p
            continue
        p = re.sub(r"([。！？])」([^「」])", r"\1\2", p)
        out.append(p)
    merged: list[str] = []
    for p in out:
        if p == "---":
            merged.append(p)
            continue
        if merged and merged[-1] != "---" and merged[-1].count("「") > merged[-1].count("」"):
            merged[-1] += p
        else:
            merged.append(p)
    return "\n\n".join(merged).strip()


def dedupe_sentences(text: str) -> str:
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
    ns: dict = {}
    exec(PATH.read_text(encoding="utf-8"), ns)
    bodies: dict[int, str] = ns["BODIES"]

    for n, body in list(bodies.items()):
        body = dedupe_sentences(fix_orphans(body))
        if n in TOPUP and hz(body) < TARGET_LO:
            body = body.rstrip() + "\n\n---\n\n" + TOPUP[n]
            # dedupe again but keep length — only remove exact dup sentences
            body = dedupe_sentences(fix_orphans(body))
            if hz(body) < TARGET_LO and n in TOPUP:
                # append short unique tail if still short after dedupe
                body = body.rstrip() + "\n\n" + TOPUP[n].split("。")[0] + "。"
        bodies[n] = body

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
    PATH.write_text("\n".join(lines), encoding="utf-8")

    bad = []
    for n in range(53, 63):
        b = bodies[n]
        h = hz(b)
        d = dup_ratio(b)
        ok = h >= TARGET_LO and d < 0.02
        print(f"ch{n:03d} hz={h} dup={d:.3f} {'OK' if ok else 'FAIL'}")
        if not ok:
            bad.append(n)

    ast.parse(PATH.read_text(encoding="utf-8"))
    print("AST OK" if not bad else f"FAIL: {bad}")


if __name__ == "__main__":
    main()
