# -*- coding: utf-8 -*-
"""Repair ch054-062 structure · dedupe titles · fix footers · hz 1900-2100"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prose_utils import hz, extract_body_and_footer  # noqa: E402

PROSE = ROOT / "prose"
TARGET_LO, TARGET_HI = 1900, 2100

FOOTERS = {
    54: ("§54坛温起伏 · 褐袍人候冬", "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    55: ("§55凡符祛寒 · 老耿引僧赠符", "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍 · 符·凡符祛寒（凡品·防）"),
    56: ("§56编筐季末 · 掌茧裂无血", "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    57: ("§57掌茧再裂 · 试手前夜", "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    58: ("§58血线将至 · 试手过手稳", "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    59: ("§59沿前即止 · 血不渗沿", "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    60: ("§60血止沿前 · 瓮温加剧", "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    61: ("§61丑时坛温 · 符影半闪", "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
    62: ("§62席盖更严 · 钩瓮醒", "大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍"),
}

# Import topup blocks from sibling script
from _topup_ch055_062 import TOPUP  # noqa: E402


def make_footer(n: int) -> str:
    ref, status = FOOTERS[n]
    return f"""---
章末。

（对照 `05` {ref} · **v45爆款10**）
**状态**：{status}
"""


def clean_body(raw: str) -> tuple[str, str]:
    """Extract single title + body prose, drop footer junk."""
    lines = raw.splitlines()
    title = ""
    rest: list[str] = []
    for line in lines:
        if line.startswith("# ") and not title:
            title = line.strip()
            continue
        if line.startswith("# "):
            continue  # duplicate titles
        if line.strip() == "---" or line.strip() == "章末。":
            break
        if line.startswith("（对照 `05`") or line.startswith("**状态**"):
            break
        rest.append(line)
    body = "\n".join(rest).strip()
    return title, body


def dedupe_paras(body: str) -> str:
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for p in paras:
        key = re.sub(r"\s+", "", p)
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return "\n\n".join(out)


def repair_file(path: Path, n: int) -> int:
    title, body = clean_body(path.read_text(encoding="utf-8"))
    body = dedupe_paras(body)
    fname = path.name
    para_keys = {re.sub(r"\s+", "", p) for p in body.split("\n\n") if p.strip()}
    for block in TOPUP.get(fname, []):
        if hz(body) >= TARGET_LO:
            break
        key = re.sub(r"\s+", "", block)
        if key not in para_keys:
            body = body.rstrip() + "\n\n" + block
            para_keys.add(key)
    body = dedupe_paras(body)
    if not title:
        title = f"# 第{'五十四' if n==54 else ''}"  # fallback
    text = f"{title}\n\n{body}\n\n{make_footer(n)}"
    path.write_text(text, encoding="utf-8")
    return hz(body)


def main() -> None:
    # Regenerate from rewrite script first
    subprocess.run([sys.executable, str(ROOT / "scripts" / "_rewrite_ch054_062.py")], check=False)

    fails = 0
    for n in range(54, 63):
        f = list(PROSE.glob(f"ch0{n}-*.md"))[0]
        h = repair_file(f, n)
        ok = TARGET_LO <= h <= TARGET_HI
        print(f"ch{n:03d} ({f.name}): {h} {'OK' if ok else 'FAIL'}")
        if not ok:
            fails += 1
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
