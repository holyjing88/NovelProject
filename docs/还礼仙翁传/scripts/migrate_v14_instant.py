#!/usr/bin/env python3
"""v14: 大小回赠皆即时 — 正文/文档措辞迁移"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PROSE = ROOT / "prose"

# (old, new) 顺序执行
REPLACEMENTS = [
    ("像延迟层落账：", "像余波钩："),
    ("也像给读者留的延迟层：", "也像给读者留的余波钩："),
    ("暂存，待后兑", "大鸣，当息已兑"),
    ("延迟的爽点不在", "爽点不止在"),
    ("小回赠却已在路上", "回赠却已在袖中"),
    ("大因果已在远处敲门", "余波已在远处敲门"),
    ("簿无大字", "塔壁无铭"),
    ("塔壁无新铭", "塔壁无铭"),
    ("簿无字", "塔壁无铭"),
    ("小因果今夜兑尽，大因果还在", "回赠今夜兑清，余波还在"),
    ("大因果，却未兑尽", "余波，却未平息"),
    ("大因果还在后头，像妖潮", "余波还在前头，像妖潮"),
    ("大还礼还在后头", "名场面还在前头"),
    ("手帕定身只是小回赠，", "手帕定身当场兑清，"),
    ("丹堂夜语只是小回赠，", "丹堂夜语当场兑清，"),
    ("隐匿符只是小回赠，", "隐匿符当场兑清，"),
    ("一剑斩金丹只是小兑，", "一剑当场兑清；余波钩在"),
    ("才是大还礼的前奏", "还在前头"),
]

# regex: ——XXX只是小YYY，ZZZ还在前头  → 回赠已即时；余波钩在ZZZ
PATTERN_PRELUDE = re.compile(
    r"——[^。]+只是小[^。]+，([^。]+)还在前头"
)
PATTERN_PRELUDE2 = re.compile(
    r"——[^。]+只是小[^。]+，([^。]+)还在前头"
)

def fix_prelude_line(text: str) -> str:
    def repl(m):
        target = m.group(1).strip()
        return f"——回赠已即时；余波钩在{target}还在前头"
    return PATTERN_PRELUDE.sub(repl, text)

def fix_prelude_line2(text: str) -> str:
    """——备战只是小阵，夜战还在前头 等变体"""
    return re.sub(
        r"——([^。]+)只是小[^，。]+，([^。]+)还在前头",
        r"——回赠已即时；余波钩在\2还在前头",
        text,
    )

def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = fix_prelude_line2(text)
    # ch006 特例
    text = text.replace(
        "霜华回赠只是小回赠，药渣之心还在前头",
        "霜华当场兑清；余波钩在药渣之心还在前头",
    )
    text = text.replace(
        "破境只是小境，赵之初见还在前头",
        "破境当场兑清；余波钩在赵之初见还在前头",
    )
    text = text.replace(
        "堂上辩只是小定场，孙福告状还在前头",
        "堂上辩当场兑清；余波钩在孙福告状还在前头",
    )
    text = text.replace(
        "闪回只是小忆，卷终夜话还在前头",
        "闪回当场落定；余波钩在卷终夜话还在前头",
    )
    text = text.replace(
        "流言只是小浪，药渣之心还在前头",
        "流言当场压下；余波钩在药渣之心还在前头",
    )
    text = text.replace(
        "册子只是小账，东脉备战还在前头",
        "册子当场兑清；余波钩在东脉备战还在前头",
    )
    text = text.replace(
        "坊市烟火只是小暖，第二次妖讯还在前头",
        "坊市烟火当场暖过；余波钩在第二次妖讯还在前头",
    )
    text = text.replace(
        "赵之初见只是小问，闪回一瞬还在前头",
        "赵之初见当场落定；余波钩在闪回一瞬还在前头",
    )
    text = text.replace(
        "残页只是小赠，丹堂大炼还在前头",
        "残页当场兑清；余波钩在丹堂大炼还在前头",
    )
    text = text.replace(
        "七夜大炼只是小成，金丹成还在前头",
        "七夜大炼当场成炉；余波钩在金丹成还在前头",
    )
    text = text.replace(
        "金丹成只是小回赠，谣言浪还在前头",
        "金丹成当场兑清；余波钩在谣言浪还在前头",
    )
    text = text.replace(
        "谣言达峰只是小浪，宽恕还在前头",
        "谣言达峰当场压下；余波钩在宽恕还在前头",
    )
    text = text.replace(
        "夜战只是小开幕，一剑斩金丹还在前头",
        "夜战当场开幕；余波钩在一剑斩金丹还在前头",
    )
    text = text.replace(
        "双妖帅只是小斩，战后抚伤还在前头",
        "双妖帅当场斩清；余波钩在战后抚伤还在前头",
    )
    text = text.replace(
        "宽恕只是小留路，赵死守还在前头",
        "宽恕当场留路；余波钩在赵死守还在前头",
    )
    text = text.replace(
        "培元被扣只是小账，堂上辩还在前头",
        "培元被扣当场记账；余波钩在堂上辩还在前头",
    )
    text = text.replace(
        "孙福告状只是小浪，宗主裁断还在前头",
        "孙福告状当场压下；余波钩在宗主裁断还在前头",
    )
    text = text.replace(
        "小扣是饵，大还礼还在后头",
        "小扣当场记清；名场面还在前头",
    )
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False

def main():
    changed = []
    for path in sorted(PROSE.glob("ch*.md")):
        if process_file(path):
            changed.append(path.name)
    print(f"Updated {len(changed)} prose files:")
    for n in changed:
        print(f"  {n}")

if __name__ == "__main__":
    main()
