# -*- coding: utf-8 -*-
"""Batch rename 万古守灯人 entities to avoid overlap with 还礼仙翁传."""
import os

ROOT = r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\万古守灯人"

# Longest-first to avoid partial replacements
REPLACEMENTS = [
    ("缘箓灯账", "灯箓账"),
    ("玄京符录司", "玄京灯符司"),
    ("照刑司符册", "照刑司灯符册"),
    ("幽灯符录", "幽灯灯符册"),
    ("符录司", "灯符司"),
    ("圣辉教廷", "照途教廷"),
    ("圣辉教", "照途教"),
    ("圣辉堂", "照途堂"),
    ("合欢宗", "双焰宗"),
    ("清虚子", "松云子"),
    ("清风观", "顺灯观"),
    ("苏照棠", "棠照绫"),
    ("执法堂", "执灯堂"),
    ("灵兽栏", "盏兽厩"),
    ("思过崖", "敛灯崖"),
    ("青岚坊", "云岚坊"),
    ("符录", "灯符册"),
    ("缘箓", "灯箓"),
    ("青岚门", "云岚宗"),
    ("黑风林外围旧图", "守夜林外围灯位图"),
    ("黑风林旧图", "守夜林外围灯位图"),
    ("青萝黑风林", "青萝守夜林"),
    ("黑风林", "守夜林"),
    ("小管事", "管慎"),
    # 还礼人物误入 → 灯道专名
    ("萧燃", "焚灯子·照焰"),
    ("韩铁山", "噬灯舵·吞名"),
    ("段承焰", "焚灯子·照焰"),
    ("噬宫主吞名", "噬灯舵·吞名"),
]

SKIP_DIRS = {".git", "__pycache__"}
SKIP_FILES = {"_apply_name_refactor.py", "_compare_names.py"}


def should_process(path: str) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in {".md", ".py", ".txt", ".bak_ch87_90"}


def main():
    changed_files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn in SKIP_FILES:
                continue
            path = os.path.join(dirpath, fn)
            if not should_process(path):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            except (UnicodeDecodeError, OSError):
                continue
            orig = text
            for old, new in REPLACEMENTS:
                text = text.replace(old, new)
            if text != orig:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(text)
                changed_files.append(path)
    print(f"Updated {len(changed_files)} files")
    for p in sorted(changed_files)[:40]:
        print(" ", p)
    if len(changed_files) > 40:
        print(f"  ... and {len(changed_files) - 40} more")


if __name__ == "__main__":
    main()
