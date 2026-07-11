#!/usr/bin/env python3
"""Fix markdown links after moving 万古守灯人 docs to docs/万古守灯人/."""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MAP = {
    "02-原创小说剧情-万古守灯人.md": "02-原创小说剧情.md",
    "06-万古守灯人-衔接检查与修订说明.md": "06-衔接检查与修订说明.md",
    "07-万古守灯人-百万字扩充方案.md": "07-百万字扩充方案.md",
    "08-万古守灯人-新增章节细纲-第一卷.md": "08-新增章节细纲-第一卷.md",
    "09-万古守灯人-全书修订报告-第二轮.md": "09-全书修订报告-第二轮.md",
    "10-万古守灯人-五百万字全书架构.md": "10-五百万字全书架构.md",
    "10-万古守灯人-550万字全书架构.md": "10-550万字全书架构.md",
    "13-万古守灯人-整体层次结构图.md": "00-整体层次结构图.md",
    "14-万古守灯人-五大系统与500万剧情设计.md": "14-五大系统与500万剧情设计.md",
    "16-万古守灯人-全书审计报告-第三轮.md": "16-全书审计报告-第三轮.md",
    "17-万古守灯人-馈灯八步与扩展系统.md": "17-馈灯八步与扩展系统.md",
    "18-万古守灯人-全书审计报告-第四轮.md": "18-全书审计报告-第四轮.md",
    "19-万古守灯人-七教合流与正邪宗门设计.md": "19-七教合流与正邪宗门设计.md",
    "20-万古守灯人-全书审计报告-第五轮.md": "20-全书审计报告-第五轮.md",
    "21-万古守灯人-灯符册系统与品阶设计.md": "21-灯符册系统与品阶设计.md",
    "22-万古守灯人-全书审计报告-第六轮-灯符册.md": "22-全书审计报告-第六轮-灯符册.md",
    "05-万古守灯人-分章正文-目录.md": "chapters/README.md",
    "../chapters/vol01-青萝灯起.md": "chapters/vol01-青萝灯起.md",
    "../chapters/vol02-云岚杂役.md": "chapters/vol02-云岚杂役.md",
    "../chapters/vol03-幽灯枯骨.md": "chapters/vol03-幽灯枯骨.md",
    "../chapters/vol04-玄京封灯.md": "chapters/vol04-玄京封灯.md",
    "../chapters/vol05-万古长明.md": "chapters/vol05-万古长明.md",
}


def rel_link(from_file: Path, target: str) -> str:
    target_path = ROOT / target.replace("/", os.sep)
    rel = os.path.relpath(target_path, from_file.parent)
    return Path(rel).as_posix()


def fix_file(md: Path) -> bool:
    text = md.read_text(encoding="utf-8")
    orig = text
    for old, new in MAP.items():
        rel = rel_link(md, new)
        text = text.replace(f"](./{old})", f"](./{rel})")
        text = text.replace(f"]({old})", f"]({rel})")
        text = text.replace(f"./{old}", f"./{rel}")
    # bare filename leftovers (same dir references)
    for old, new in MAP.items():
        new_name = new.split("/")[-1]
        if md.parent.name == "chapters" and new.startswith("chapters/"):
            parent_rel = "../" + "/".join(new.split("/")[1:])
            text = text.replace(old, parent_rel if "vol" in new else "../" + new_name)
        else:
            rel = rel_link(md, new)
            text = text.replace(old, rel)
    if text != orig:
        md.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    n = 0
    for md in ROOT.rglob("*.md"):
        if fix_file(md):
            n += 1
    print(f"updated {n} markdown files under {ROOT}")


if __name__ == "__main__":
    main()
