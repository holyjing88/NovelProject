# -*- coding: utf-8 -*-
"""v37 正文 ch001-049 策划链对齐批处理：状态行 · 脚注 · 策划钩强化"""
from __future__ import annotations

import glob
import os
import re

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

STATE_VILLAGE = (
    "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · "
    "鸿蒙九劫瓮·眠 · 洞府·漏舍凡舍"
)
STATE_SECT = (
    "**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · "
    "鸿蒙九劫瓮·眠 · 宗门·丙九杂役 · 漏舍凡舍"
)

# 策划钩强化（`05`/`17` 对齐 · 插入末段前）
ENRICH: dict[int, str] = {
    1: (
        "韩泥望坛角，不知真名，只按祖辈手擦沿口——坛在，根在；"
        "根在，才撑得住村嘲与十二文小胜。"
    ),
    3: (
        "他摸碗沿，姜辛还在——七笔旧恩第一笔，热着记，凉着还。"
        "叶丫头不问灵根，只问烫，这问法，他记一辈子。"
    ),
    7: (
        "陈姑棉袄裹身，恩在心里落第三笔——冬寒压人，袄不压心；"
        "心记着，才穿得出井台半步。"
    ),
    9: (
        "沈枯芽粥稀，怯声真——七笔第五笔，芽儿恩不混邪；"
        "混了，心就乱，乱则还不了热汤。"
    ),
    12: (
        "张麻婆馒头顶饥，恩第四笔；赖扒皮克扣同章，仇苗初显。"
        "恩仇分列，不混，是记心翁的活法。"
    ),
    18: (
        "叶丫头针脚密，恩第一笔又深一分——衣破有人补，"
        "补的是路，路通向将来还烫。"
    ),
    24: (
        "公审证白落，赵哑口——恩第一笔在名节上兑现一半；"
        "另一半烫着还，还到省亲那日。"
    ),
    30: (
        "叶振东药入篓，恩第二笔实了——布衣省亲伏笔在药香里，"
        "辞村路开，坛应一步。"
    ),
    35: (
        "飞石落，她挡；他立誓必还——契字落心，不比落纸轻。"
        "符影应誓，恩不混辱，辱另记。"
    ),
    36: (
        "刘婆肘上布丑，粥边热在——宗门第七笔，泥岗六笔之外另记；"
        "分列，不混，才配活过克扣。"
    ),
    41: (
        "灰线在石上，手稳在掌——备检记名，正测仍末排；"
        "末排也是路，路通向嗅渣不漏。"
    ),
    44: (
        "嗅诀三句落破布角：静、列、漏——丹道辅线起，"
        "不越阶，只铺瓮醒前鼻下路。"
    ),
    49: (
        "四日条在柱，七笔在心——泥岗六笔、宗门一笔，分列不混；"
        "先听规矩，再验香，再学炼丹，先还叶丫头烫。"
    ),
}


def hz(s: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", s))


def body_of(text: str) -> str:
    m = re.search(r"\n---\n\n章末", text)
    body = text[: m.start()] if m else text
    body = re.sub(r"^#.*\n", "", body, count=1)
    return body.strip()


def upgrade_footer(text: str, n: int) -> str:
    m = re.search(r"（对照 `05`[^）]*）", text)
    if not m:
        return text
    old = m.group(0)
    new = re.sub(r"\*\*v[^*]+\*\*", "**v37正文迭代**", old)
    if "`17`" not in new:
        new = new.replace("（对照 `05` §", "（对照 `05` §", 1)
        mm = re.match(r"（对照 `05` §([^·]+) · (.+)", new)
        if mm and "`17`" not in mm.group(2):
            new = f"（对照 `05` §{mm.group(1)} · `17` §二 · {mm.group(2)}"
    return text.replace(old, new, 1)


def insert_state(text: str, n: int) -> str:
    state = STATE_SECT if n >= 31 else STATE_VILLAGE
    block = f"\n\n{state}\n"
    if state.strip() in text:
        return text
    return re.sub(r"(\n---\n\n章末。)", block + r"\1", text, count=1)


def insert_enrich(text: str, n: int) -> str:
    para = ENRICH.get(n)
    if not para or para in text:
        return text
    return re.sub(
        r"(\n---\n\n\*\*状态\*\*)",
        f"\n\n{para}\n\\1",
        text,
        count=1,
    )


def process_file(path: str) -> bool:
    m = re.search(r"ch(\d+)", os.path.basename(path))
    if not m:
        return False
    n = int(m.group(1))
    if n > 49:
        return False

    text = open(path, encoding="utf-8").read()
    orig = text
    text = upgrade_footer(text, n)
    text = insert_state(text, n)
    text = insert_enrich(text, n)

    if text != orig:
        open(path, "w", encoding="utf-8", newline="\n").write(text)
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        if process_file(path):
            changed += 1
            m = re.search(r"ch(\d+)", os.path.basename(path))
            n = int(m.group(1)) if m else 0
            if n <= 49:
                t = open(path, encoding="utf-8").read()
                print(f"ch{n:03d} hz={hz(body_of(t))} updated")
    print(f"done: {changed} files")


if __name__ == "__main__":
    main()
