#!/usr/bin/env python3
"""逐章手修基线：剥离垫字/模板段/重复段，输出缺字数报告。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose_utils import extract_body_and_footer, hz, norm

PROSE = Path(__file__).resolve().parent.parent / "prose"
LO, HI = 2000, 3000
CANON = re.compile(r"ch0(0[1-9]|[12][0-9]|30|3[1-9]|[4-5][0-9]|60|61)")

# 不手修的标杆章（已精修）
SKIP = {"ch001-劫后余寿.md", "ch003-塔鸣初缘.md", "ch037-丹堂大炼.md", "ch049-挽月反戈.md", "ch055-杖剑出.md", "ch061-天试旨到.md"}

FILLER_SUB = (
    "山门风过，袖仍空",
    "塔鸣轻荡，荡完又静",
    "风过山门，袖仍空",
    "弟子终于肯散，散时仍有人忍不住再瞧一眼灰袍袖空",
)

TEMPLATE_SUB = (
    "传到最后，只剩",
    "有人说",
    "莫长春袖空，杖在塔中，不辩，只记",
    "莫长春袖空，杖在塔中，不坐，只立",
    "莫长春袖空，杖在塔中，立阶外",
    "围观弟子屏息，屏息等",
    "塔鸣极轻，轻像",
    "塔鸣极轻，轻得像",
    "落进识海。莫长春念",
    "哼里空一线",
    "踮脚像钩",
    "余波还在",
    "添油加醋",
)

# 整段模板（ rumor 汇总段）
TEMPLATE_LINE = re.compile(
    r"^.{0,8}(那日|之后|那夜|事后)，.+传到最后"
)


def is_filler(p: str) -> bool:
    if any(s in p for s in FILLER_SUB):
        return True
    if len(p) < 80 and any(s in p for s in TEMPLATE_SUB):
        if "塔鸣极轻" in p or "山门风过" in p or "塔鸣轻荡" in p:
            return True
    # 纯垫字短段
    if norm(p) in {
        norm("山门风过，袖仍空，塔意却沉了一寸。"),
        norm("莫长春念：「还礼有时。」塔鸣轻荡，荡完又静。"),
    }:
        return True
    return False


def is_template_summary(p: str) -> bool:
    if TEMPLATE_LINE.search(p.replace("\n", "")):
        return True
    if p.count("有人说") >= 2:
        return True
    if "传到最后" in p and "说莫长春" in p:
        return True
    if norm(p).startswith(norm("莫长春袖空")) and "不辩" in p and len(p) < 120:
        return True
    return False


def polish_body(body: str) -> str:
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    kept: list[str] = []
    seen: set[str] = set()
    for p in paras:
        if is_filler(p) or is_template_summary(p):
            continue
        if any(s in p for s in ("的余波，还在外门盘桓", "霍镇山按刀，刀稳半寸", "柳青鸢远观，剑穗无风")):
            continue
        n = norm(p)
        # 去重复：归一化后相同，或一方包含另一方（摘要重复正文）
        dup = False
        for s in seen:
            if len(n) >= 50 and len(s) >= 50:
                if n in s or s in n:
                    dup = True
                    break
        if dup:
            continue
        if len(n) >= 30 and n in seen:
            continue
        if len(n) >= 30:
            seen.add(n)
        kept.append(p)
    return "\n\n".join(kept)


def main() -> None:
    rows = []
    for p in sorted(PROSE.glob("ch*.md")):
        if not CANON.match(p.name):
            continue
        if p.name in SKIP:
            continue
        text = p.read_text(encoding="utf-8")
        body, footer = extract_body_and_footer(text)
        before = hz(body)
        cleaned = polish_body(body)
        after = hz(cleaned)
        if not footer:
            footer = f"---\n\n*（上架连载稿 · {p.stem.split('-', 1)[1]}）*\n"
        p.write_text(cleaned.rstrip() + "\n\n" + footer, encoding="utf-8")
        rows.append((p.name, before, after))

    print(f"Polished {len(rows)} chapters (skipped {len(SKIP)})")
    below = [(n, b, a) for n, b, a in rows if a < LO]
    print(f"below {LO}: {len(below)}")
    for n, b, a in sorted(below, key=lambda x: x[2]):
        print(f"  {n}: {b} -> {a} (need {LO - a})")
    ok = sum(1 for _, _, a in rows if LO <= a <= HI)
    print(f"in_range: {ok}/{len(rows)}")


if __name__ == "__main__":
    main()
