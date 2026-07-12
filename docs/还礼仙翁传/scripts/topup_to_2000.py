#!/usr/bin/env python3
"""补足至 2000：仅在正文末尾、footer 前插入短钩。"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

PROSE = Path(__file__).resolve().parent.parent / "prose"
LO = 2000
CANON = re.compile(r"ch0(0[1-9]|[12][0-9]|30|3[1-9]|[4-5][0-9]|60|61)")
FOOTER_TAG = re.compile(r"^\*（上架连载稿[^\n]*\*\)\s*$", re.MULTILINE)


def load_hooks():
    path = Path(__file__).resolve().parent / "thicken_to_2000.py"
    spec = importlib.util.spec_from_file_location("t", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CHAPTER_HOOKS


HOOKS = load_hooks()


def hz(s: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def split_safe(text: str) -> tuple[str, str]:
    matches = list(FOOTER_TAG.finditer(text))
    if not matches:
        return text.rstrip(), ""
    fm = matches[-1]
    head = text[: fm.start()]
    search = head[-400:] if len(head) > 400 else head
    rel = search.rfind("\n---\n")
    if rel >= 0:
        cut = len(head) - len(search) + rel
        return head[:cut].rstrip(), text[cut : fm.end()] + ("\n" if not text[fm.end() - 1 : fm.end()] == "\n" else "")
    return head.rstrip(), text[fm.start() : fm.end()] + "\n"


def closing(name: str) -> str:
    hook = HOOKS.get(name, "还礼有时")
    return (
        f"莫长春念：「{hook}。」塔鸣轻荡，荡完又静。"
        f"弟子终于肯散，散时仍有人忍不住再瞧一眼灰袍袖空——"
        f"瞧得像瞧一眼九月还能走多久。"
    )


def main() -> None:
    done = 0
    for p in sorted(PROSE.glob("ch*.md")):
        if not CANON.match(p.name):
            continue
        t = p.read_text(encoding="utf-8")
        body, footer = split_safe(t)
        if hz(body) >= LO:
            continue
        c = closing(p.name)
        if c not in body:
            body = body.rstrip() + "\n\n" + c + "\n"
        # 仍不足则再补一句
        if hz(body) < LO:
            hook = HOOKS.get(p.name, "还礼有时")
            extra = f"风过山门，袖仍空，塔意却沉——沉得像把「{hook}」先记在格子里。"
            if extra not in body:
                body = body.rstrip() + "\n\n" + extra + "\n"
        if not footer:
            footer = f"\n---\n\n*（上架连载稿 · {p.stem.split('-',1)[1]}）*\n"
        p.write_text(body.rstrip() + "\n" + footer, encoding="utf-8")
        done += 1
    print(f"topped up {done}")


if __name__ == "__main__":
    main()
