#!/usr/bin/env python3
"""v17: 废止恩簿/袖中簿/恩仇记在心里/记在塔/塔在神识，统一为鸿蒙万缘塔措辞。"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

# 长串优先
REPLACEMENTS: list[tuple[str, str]] = [
    ("恩在塔，塔在识海", "识海深处，万缘塔影一荡"),
    ("恩仇都记在心里", "恩仇皆在塔壁金铭"),
    ("恩仇记在心里了", "塔壁金铭又亮一线"),
    ("恩仇记在心里", "塔壁金铭又亮"),
    ("像把将来要还的恩仇记在心里", "像塔壁又记下一缕待还之纹"),
    ("像把将来要用的恩仇记在心里", "像塔壁又记下一线待用之纹"),
    ("像把将来要查的恩仇记在心里", "像塔壁又浮一线待查之纹"),
    ("「恩簿。」莫长春笑，「恩仇都记在心里。」", "「万缘塔。」莫长春笑，「恩仇皆在塔壁金铭。」"),
    ("摸到恩簿的慌与喜", "摸到万缘塔虚影的慌与喜"),
    ("把死期当成恩簿截止日期", "把死期当成万缘塔铭文截止之期"),
    ("像把师恩先记在塔里", "像把师恩先入塔中"),
    ("恩先记在塔里", "师恩先入塔中"),
    ("记在塔里", "暂入塔中"),
    ("记在塔", "铭于塔壁"),
    ("塔在识海", "万缘塔镇识海"),
    ("袖中簿又浮半句", "塔壁又浮半句金铭"),
    ("袖中簿又浮", "塔壁又浮"),
    ("袖中簿无新字，却沉，像又记在心里", "塔壁无新铭，塔影却沉，像又浮半句金铭"),
    ("袖中簿无新字，却沉", "塔壁无新铭，塔影却沉"),
    ("袖中簿无大字，却烫", "塔壁无大字，塔影却烫"),
    ("袖中簿无字，却一烫", "塔壁无新铭，塔影却一烫"),
    ("袖中簿无字，却沉", "塔壁无新铭，塔影却沉"),
    ("袖中簿一烫，烫得像", "塔影一烫，烫得像"),
    ("袖中簿一烫", "塔影一烫"),
    ("袖中簿微烫", "塔影微烫"),
    ("袖中簿沉", "塔影沉"),
    ("袖中簿", "万缘塔"),
    ("恩簿", "万缘塔"),
    ("师恩簿源", "师恩塔源"),
    ("簿还未显形", "塔影还未凝实"),
    ("帖与簿意相合", "帖与塔意相合"),
    ("莫长春合簿", "莫长春收念"),
    ("他合簿", "他收念"),
    ("簿无新字", "塔壁无新铭"),
    ("册上「缘」字微亮", "塔壁「缘」字金铭微亮"),
    ("莫长春抚册", "莫长春抚杖"),
    ("演给簿看", "演给塔看"),
    ("账在塔，塔在识海", "识海深处，万缘塔影一荡"),
    # 簿 → 塔（勿误伤「杂役簿」）
    ("「什么簿？」", "「什么塔？」"),
    ("简与簿意相合", "简与塔意相合"),
    ("笑给簿听", "笑给塔听"),
    ("簿可小结算", "塔可小结算"),
    ("记在簿上", "铭于塔壁"),
    ("人情记簿上", "人情铭塔壁"),
    ("收进簿里", "收进塔壁"),
    ("缘已在簿", "缘已在塔"),
    ("舌快，簿慢", "舌快，塔慢"),
    ("簿记下了", "塔壁记下了"),
    ("簿会记", "塔会记"),
    ("自有簿记", "自有塔记"),
    ("簿记", "塔记"),
    ("若簿……真在你袖里", "若塔……真在你识海里"),
    ("这簿，认不认", "这塔，认不认"),
    ("师恩与簿规握手", "师恩与塔规握手"),
    ("簿规", "塔规"),
    ("簿认", "塔认"),
    ("簿翻页", "塔鸣"),
    ("像簿翻页", "像塔鸣"),
    ("簿在师兄袖里", "塔在师兄识海"),
    ("簿在袖中沉", "塔影在识海沉"),
    ("簿在袖中微烫", "塔影在识海微烫"),
    ("簿在袖中", "塔影在识海"),
    ("簿上浮半句", "塔壁浮半句"),
    ("簿上浮字", "塔壁浮字"),
    ("簿上浮", "塔壁浮"),
    ("簿上寿元", "塔壁寿元"),
    ("寿元在簿上", "寿元在塔壁"),
    ("簿上「三品」", "塔壁「三品」"),
    ("与簿上「三品」", "与塔壁「三品」"),
    ("没看簿", "没看塔壁"),
    ("闸纹与簿纹", "闸纹与塔纹"),
    ("袖中薄册", "识海中塔影"),
    ("尚未写名的簿", "尚未凝实的塔影"),
    ("薄册的轮廓", "塔影的轮廓"),
    ("簿已先热", "塔已先热"),
    ("她仍无簿", "她仍无塔"),
    ("她无簿", "她无塔"),
    ("不懂簿", "不懂塔"),
    ("缘字在袖中微亮", "缘字在识海微亮"),
    ("护法已在袖——袖空，塔意却沉", "护法已在识海——袖空，塔意却沉"),
]

FORBIDDEN = (
    "恩簿",
    "袖中簿",
    "恩仇都记在心里",
    "恩仇记在心里",
    "记在塔",
    "塔在识海",
    "恩在塔",
)

SCAN_DIRS = ("prose", "chapters", "scripts")
SCAN_ROOT_GLOBS = ("*.md",)


def apply_replacements(text: str) -> tuple[str, int]:
    count = 0
    for old, new in REPLACEMENTS:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
    return text, count


def scan_files() -> list[Path]:
    files: list[Path] = []
    for d in SCAN_DIRS:
        p = ROOT / d
        if p.is_dir():
            files.extend(p.rglob("*.md"))
            files.extend(p.rglob("*.py"))
    for pat in SCAN_ROOT_GLOBS:
        files.extend(ROOT.glob(pat))
    return sorted(p for p in set(files) if p.resolve() != SELF)


def main() -> None:
    changed: list[tuple[str, int]] = []
    for path in scan_files():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        new_text, n = apply_replacements(text)
        if n and new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed.append((str(path.relative_to(ROOT)), n))

    print(f"updated {len(changed)} files, {sum(c for _, c in changed)} replacements")
    for name, n in changed:
        print(f"  {name}: {n}")

    remain: list[tuple[str, str]] = []
    for path in scan_files():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for pat in FORBIDDEN:
            if pat in text:
                remain.append((str(path.relative_to(ROOT)), pat))
    if remain:
        print("REMAINING:")
        for name, pat in sorted(set(remain)):
            print(f"  {name}: {pat}")
    else:
        print("no forbidden terms remaining")


if __name__ == "__main__":
    main()
