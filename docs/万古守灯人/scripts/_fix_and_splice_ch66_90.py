# -*- coding: utf-8 -*-
"""Fix corrupted duplicate CHAPTERS and re-splice."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VOL2 = ROOT / "../chapters/vol02-云岚杂役.md"


def load_chapters(path: Path):
    import importlib.util
    text = path.read_text(encoding="utf-8")
    first = text.find("CHAPTERS = [")
    second = text.find("CHAPTERS = [", first + 1)
    if second != -1:
        text = text[:second].rstrip() + "\n"
        path.write_text(text, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CHAPTERS


def count(body: str) -> int:
    return len(re.sub(r"\s", "", body))


def main():
    ch66_78 = load_chapters(ROOT / "_ch66_78_bodies.py")
    ch79_90 = load_chapters(ROOT / "_ch79_90_bodies.py")

    # fix ch90 title and ending
    fixed = []
    for title, body in ch79_90:
        if title.startswith("第九十章"):
            title = "第九十章 灯还亮着"
            body = body.strip()
            if "**第二卷完**" not in body:
                body += "\n\n**第二卷完**"
        fixed.append((title, body))
    ch79_90 = fixed

    chapters = ch66_78 + ch79_90

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
    for title, body in chapters:
        parts.append(f"### {title}")
        parts.append("")
        parts.append(body.strip())
        parts.append("")
        parts.append("---")
        parts.append("")

    parts.append(footer.strip())
    VOL2.write_text("\n".join(parts) + "\n", encoding="utf-8")

    print(f"Fixed and spliced {len(chapters)} chapters")
    for title, body in chapters:
        n = count(body)
        flag = "OK" if 3500 <= n <= 4500 else ("SHORT" if n < 3500 else "LONG")
        m = re.search(r"第(\d+)章|第(.+?)章", title)
        print(f"  {title}: {n} [{flag}]")

    # verify ch66 start
    vol = VOL2.read_text(encoding="utf-8")
    i = vol.find("### 第六十六章")
    sample = vol[i:i+200]
    assert "第七层门一合" in sample, "ch66 continuity broken"
    assert "?" not in sample.replace("？", ""), "ch66 has corruption"
    print("ch66 continuity OK")


if __name__ == "__main__":
    main()
