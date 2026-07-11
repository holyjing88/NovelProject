#!/usr/bin/env python3
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
NOVEL = SCRIPTS.parent
CHAPTERS = NOVEL / "chapters"
PROJECT = NOVEL.parent.parent

REPLS = [
    (str(PROJECT / "docs" / "../chapters/vol01-青萝灯起.md"), str(CHAPTERS / "vol01-青萝灯起.md")),
    (str(PROJECT / "docs" / "../chapters/vol02-云岚杂役.md"), str(CHAPTERS / "vol02-云岚杂役.md")),
    (str(PROJECT / "docs" / "../chapters/vol03-幽灯枯骨.md"), str(CHAPTERS / "vol03-幽灯枯骨.md")),
    (str(PROJECT / "docs" / "../chapters/vol04-玄京封灯.md"), str(CHAPTERS / "vol04-玄京封灯.md")),
    (str(PROJECT / "docs" / "../chapters/vol05-万古长明.md"), str(CHAPTERS / "vol05-万古长明.md")),
    ("docs/万古守灯人/chapters/vol01-青萝灯起.md", "docs/万古守灯人/chapters/vol01-青萝灯起.md"),
    ("docs/万古守灯人/chapters/vol02-云岚杂役.md", "docs/万古守灯人/chapters/vol02-云岚杂役.md"),
    ("docs/万古守灯人/chapters/vol03-幽灯枯骨.md", "docs/万古守灯人/chapters/vol03-幽灯枯骨.md"),
    ("docs/万古守灯人/chapters/vol04-玄京封灯.md", "docs/万古守灯人/chapters/vol04-玄京封灯.md"),
    ("docs/万古守灯人/chapters/vol05-万古长明.md", "docs/万古守灯人/chapters/vol05-万古长明.md"),
    ("../chapters/vol01-青萝灯起.md", "../chapters/vol01-青萝灯起.md"),
    ("../chapters/vol02-云岚杂役.md", "../chapters/vol02-云岚杂役.md"),
    ("../chapters/vol03-幽灯枯骨.md", "../chapters/vol03-幽灯枯骨.md"),
    ("../chapters/vol04-玄京封灯.md", "../chapters/vol04-玄京封灯.md"),
    ("../chapters/vol05-万古长明.md", "../chapters/vol05-万古长明.md"),
    ('"docs" / "../chapters/vol02-云岚杂役.md"', '"docs" / "万古守灯人" / "chapters" / "vol02-云岚杂役.md"'),
    ('ROOT / "../chapters/vol01-青萝灯起.md"', 'ROOT / "万古守灯人" / "chapters" / "vol01-青萝灯起.md"'),
    ('ROOT / "../chapters/vol02-云岚杂役.md"', 'ROOT / "万古守灯人" / "chapters" / "vol02-云岚杂役.md"'),
    ('ROOT / "../chapters/vol03-幽灯枯骨.md"', 'ROOT / "万古守灯人" / "chapters" / "vol03-幽灯枯骨.md"'),
    ('ROOT / "../chapters/vol04-玄京封灯.md"', 'ROOT / "万古守灯人" / "chapters" / "vol04-玄京封灯.md"'),
    ('ROOT / "../chapters/vol05-万古长明.md"', 'ROOT / "万古守灯人" / "chapters" / "vol05-万古长明.md"'),
    ('VOL2 = ROOT / "../chapters/vol02-云岚杂役.md"', 'VOL2 = ROOT / "万古守灯人" / "chapters" / "vol02-云岚杂役.md"'),
    ('VOL4 = ROOT / "docs/万古守灯人/chapters/vol04-玄京封灯.md"', 'VOL4 = ROOT / "docs/万古守灯人/chapters/vol04-玄京封灯.md"'),
    ('VOL5 = ROOT / "docs/万古守灯人/chapters/vol05-万古长明.md"', 'VOL5 = ROOT / "docs/万古守灯人/chapters/vol05-万古长明.md"'),
]

n = 0
for py in SCRIPTS.glob("*.py"):
    text = py.read_text(encoding="utf-8")
    orig = text
    for old, new in REPLS:
        text = text.replace(old, new)
    if text != orig:
        py.write_text(text, encoding="utf-8")
        n += 1
print(f"updated {n} scripts")
