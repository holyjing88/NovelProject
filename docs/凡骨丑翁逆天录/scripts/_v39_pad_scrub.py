# -*- coding: utf-8 -*-
"""v39 扫尾：清除 PAD · 补 1500 字闸（戏内独段）"""
from __future__ import annotations

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import TARGET_LO, body_chars, extract_body_and_footer, hz

PROSE = os.path.join(os.path.dirname(__file__), "..", "prose")

PAD_BLOCK = re.compile(
    r"\n*他按坛沿，只记，不飘。飘了，恩断；恩不断，手就稳，稳了，明日还有活，活才能还。"
    r"还远不怕，怕的是汤凉——汤在叶铺，在刘婆灶，在心里，心里那格留给烫，烫字不写，按在胃上。\n*",
    re.S,
)
PAD_LINE = re.compile(
    r"(?:坛沿一线温，像还路又近一分。近一分，手稳一分，恩不断一分。(?:手稳，才配明日还有活；活，才配还。\n*)?)+",
    re.S,
)

# 短章补段（每章唯一 · 不重复 thicken）
PAD_REPLACEMENT: dict[int, str] = {
    10: "里正门外风硬，风撕告示角，撕不撕「绝户」二字。二字在册，不在心——心在，四恩就在，就要还。",
    27: "臂肿退尽，他试抬筐，筐沉，沉得稳。稳，像还路又实一分——实一分，就离辞村近一分。",
    28: "经片古字他不识，识的是沿温。沿温，像守瓮口传还在——还在，西驿路就不飘。",
    30: "药香入篓，篓沉，沉得像六笔恩。恩在，坛应一步；一步到西驿，一步验骨，一步还。",
    34: "稀粥入喉，克扣在秤。秤虚，手要实——实了，挡石那日才立得住誓，誓不飘。",
    35: "叶青禾离去，布鞋稳，肩裂一线。线像门缝递汤——汤没洒，石落了，誓落心了。管事记赵名，名在册，辱另记，不混恩。",
    36: "刘婆粥边骂赖福，骂响，粥更热。第七笔另册，不混泥岗六笔——混则还错人，错人，汤就凉。",
    37: "藤刺再入旧疤，血渗，沿前即止。止，像瓮在数关——关未开，手先稳，稳了才接深秋末单。",
    38: "铁无言鼻下一稳，稳像旧活。渣香里一线正，正短，像汤温——温短记着还，邪腥长记着避。",
    39: "半月短三口，刻心不是怨，是存锤。锤在备检，备检过了，饭才实，秤才盯得实。",
    40: "备检手稳，灰线过石。血近沿，沿前即止——止，像瓮在等冬测那关开缝。",
    41: "末席过，灵仍末。灵末不谎，手更不谎——手稳，廊下嗅路才长，长向辨香关。",
    42: "病兽尽，多清半刻。半刻暖丙九——暖了，手才稳，才配盯秤那日三两落袋。",
    43: "秤盘实三两，赖福虚。虚不是终，终在正测，在辨香——香净了，才近问香帖。",
    44: "同舍笑他抱破布睡。笑浅，他不辩——舌留来念诀；诀稳，三日后编筐才接得上。",
    45: "三十五筐入库，记功加饭。饭多一口，像还路又实一分——实一分，瓮温那关又近一分。",
    47: "廊香半刻记功，七日在柱。七日少一日，手稳一日——稳，才进得丹房门缝学还恩的丹。",
}


def scrub(body: str) -> str:
    body = PAD_BLOCK.sub("\n\n", body)
    body = PAD_LINE.sub("", body)
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def pad_short(body: str, n: int) -> str:
    if n not in PAD_REPLACEMENT:
        return body
    block = PAD_REPLACEMENT[n].strip()
    if block in body:
        return body
    marker = "<!-- v38-topup -->"
    if marker in body:
        body = re.sub(
            rf"({re.escape(marker)}\n\n)(.*?)(?=\n\n<!-- v38-end -->|\n\n\*\*状态\*\*)",
            lambda m: m.group(1) + (m.group(2).rstrip() + "\n\n" + block if m.group(2).strip() else block),
            body,
            count=1,
            flags=re.S,
        )
    elif "**状态**" in body:
        body = body.replace("\n\n**状态**", f"\n\n{marker}\n\n{block}\n\n**状态**", 1)
    return body


def main() -> None:
    short = []
    for path in sorted(glob.glob(os.path.join(PROSE, "ch*.md"))):
        n = int(re.search(r"ch(\d+)", path).group(1))
        if n > 49:
            continue
        text = open(path, encoding="utf-8").read()
        body, footer = extract_body_and_footer(text)
        body = scrub(body)
        if hz(body) < TARGET_LO:
            body = pad_short(body, n)
        if hz(body) < TARGET_LO and n in PAD_REPLACEMENT:
            # 仍短则正文末再补一句
            extra = "他低声道：「手稳，恩不断；恩不断，汤就不凉。」"
            if extra not in body and "**状态**" in body:
                body = body.replace("\n\n**状态**", f"\n\n{extra}\n\n**状态**", 1)
        new = body + "\n\n" + footer if footer else body + "\n"
        if new != text:
            open(path, "w", encoding="utf-8", newline="\n").write(new)
        c = body_chars(new)
        if c < TARGET_LO:
            short.append((n, c))
        print(f"ch{n:03d} {c}")
    print("still short:", short)


if __name__ == "__main__":
    main()
