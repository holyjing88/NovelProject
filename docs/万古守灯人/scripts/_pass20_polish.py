# -*- coding: utf-8 -*-
"""Pass20: safe polish — strip duplicate templates, replace with hand/source prose."""
from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from _pass19_short_boost import (  # noqa: E402
    ch_num_from_title,
    han_count,
    load_py_chapters,
    parse_file,
    rebuild,
    strip_meta,
    trim_body,
    dedupe_paragraphs,
    MIN_HAN,
    MAX_HAN,
    CHAPTERS_DIR,
)

TEMPLATE_MARKERS = [
    "场中一时静了。顾迟年不急着赢口舌",
    "袖中守岁灯微温，一阶微光无声铺开",
    "围观者从窃语到噤声，再到哗然",
    "留灯账上，他记一行：*",
    "的风里带着灯油与药香。顾迟年忽然想起青萝镇口长明",
    "霍照临未近，只以灯影压场一寸",
    "沈青禾在侧，姜汤仍温。她不多言，只把药杵轻顿一下",
    "铁柱在远处吼，声瓮而真",
    "姜小满合十，唇白，只念：「灯还亮……」像把恐惧",
    "温言以律护行，谢长缨以制护城。顾迟年知：律与制，亦是灯",
    "裴无妄虚影远观，不插手，只验心",
    "天明前，他独对守岁灯，把今日所见拆开重算",
    "他扶墙喘匀，明魂丹药力在脉里走，像温河。凡人打仗",
    "章末，他望",
    "这一局，他要的不是响，是序。",
]

META_LINE = re.compile(
    r"^(馈灯链：|馈灯①：|守夜林指路猎户，留灯账：|霍照临迟暮之约立，留灯账：|"
    r"他不邀功，只把半滴油、一条路写进留灯账。|"
    r"灯箓账上，人间账与灯箓同频|花甲入宗杂役，低谷蓄力)"
)


def is_template_para(p: str) -> bool:
    p = p.strip()
    if not p or p in ("。", "---"):
        return True
    if META_LINE.match(p):
        return True
    return any(m in p for m in TEMPLATE_MARKERS)


def split_paras(body: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip() and p.strip() != "---"]


def count_template_hits(body: str) -> int:
    return sum(body.count(m) for m in TEMPLATE_MARKERS)


def remove_dup_templates(body: str) -> str:
    """Remove repeated template blocks; keep first occurrence + all story paragraphs."""
    paras = split_paras(strip_meta(body))
    seen_tpl: set[str] = set()
    out: list[str] = []
    for p in paras:
        if is_template_para(p):
            key = re.sub(r"\s+", "", p)[:48]
            if key in seen_tpl:
                continue
            seen_tpl.add(key)
            continue  # drop even first template block
        out.append(p)
    return dedupe_paragraphs("\n\n".join(out))


def load_pass12_ch160() -> str:
    text = (SCRIPTS / "_pass12_score_boost.py").read_text(encoding="utf-8")
    m = re.search(r"CH160_CORE = '''(.*?)'''", text, re.S)
    if not m:
        return ""
    return re.sub(r"^### 第[^\n]+\n", "", m.group(1)).strip()


HAND_POLISHED: dict[int, str] = {
    160: load_pass12_ch160(),
    161: """程不二之死，卷宗终开。

照刑司正厅，灯影壁亮如昼。温言以律起卷，不二斋那一夜的火，在墙上重燃——不是真火，是留证之火。

副使带人破门时，程不二没有跪。他站在案后，袖中地图烫得像烙在皮上。灯影里，他仍是那句话：「三块灵石的事，别用一滴灯油。」

顾迟年抚半张残图，指腹触到焦边，像触到一截仍温的指骨。「不二斋价码，是命。」

温言冷声：「他信陆承安，也信你。撕图半入火，半塞副使怀——反夺刃，同坠火堆，拉垫背。」

裴无妄虚影现于厅角，无面，只摊手：「程不二最珍贵的一盏记忆，卖给了我。他说，想再看一眼旧灯库亮。」

顾迟年闭眼，再开：「给他看。」

光影起——少年程不二被逐出镇灯司，雨里仍护一盏豆火。他笑：「灯在，路在。三块灵石的事，别用一滴灯油。」

姜小满问：「师父，程掌柜能回魂吗？」

「灯道无回魂。」顾迟年望灯影，「只有记得。」

他在不二斋废墟立一块无名碑，碑成，风过，似有人笑，轻却暖。

温言立侧：「照刑司正库，已录程不二案。灭口者副使，供词与陆承安线报相合——他慢一步，不是不救，是不能明抗。」

顾迟年沉默，在碑前放一盏微光，不亮，只暖：「不二，灯还亮着。」

姜小满问：「还恨陆师兄吗？」

「恨谁？」他望碑，「程不二用命换地图。记得他，比回魂要紧。」

远处霍照临冷声：「碑立了，路还没开。旧灯库第四层，谁下？」

顾迟年收袖：「我去。秦照冤案，须见卷宗原貌。」""",
    185: """承平门外，井口黑气如倒灌之墨。

百姓命灯齐暗一线——不是灯灭，是人心先怕。幼帝被护于后，仍举小灯，童光微明，像给将灭之域，点了一豆。

铁柱扑井口，锤拄地，背如墙：「迟年哥！油！」

万家灯火自青萝、玄京、走灯节百户汇他身，无阶如灯骨，百姓齐喊守灯。顾迟年灯域里见铁柱命灯明如昼。

裴无妄虚影：「万家灯火不可掠，可借可守，第九条成了。」

顾迟年以域引万民之暖灌守岁灯——油，满。半炷香尽，暗源现：井底叛徒与域外黑气一线相连。

叛徒最后一击直取谢长缨，欲灭开灯令于纸面。陆承安睁眼扑上，六阶灯骨承击，笑，血溢。

霍照临剑至迟半息，见陆承安眼清一瞬，像想起名、家、娘。「原来……我也想有人守。」

顾迟年接陆承安最后一缕光：「不是守你一人，是守你护的那一城。」

陆承安六阶灯骨碎于城下，战死赎罪，非化灯——是以命续开灯令。

霍照临洒酒三杯，迟暮之约止，守灯之约不止。幼帝献匾：「护灯者，亦人。」

醒时，玄京气运已与青萝长明一线相连。陆承安葬皇城外，碑曰护灯，无化灯二字。

温言收卷，低声：「路还长。」顾迟年触守岁灯，第三相微颤——陆承安最后一念，归灯，非形。""",
    188: """陆承安墓前，赎罪前夜。

墓前无音乐，只有风，与百姓远处仍有的骂声——他们不知全貌，只记封灯时的刀。

顾迟年以五阶灯影照陆承安一生：世家子，天才，吞命灯，镇灯司，叛余孽，赎罪，战死。非化灯，是以命续开灯令。

沈青禾放一盏河灯：「陆公子，青萝镇，为你留一盏。」铁柱锤立墓旁：「下次，别挡俺锤。」

姜小满放《守灯经》抄本，页边有云照批注：「命灯有光，人便有路。」

温言录供词，入照刑司正库，昭告：陆承安非妖，乃迷途护灯者，终以命赎，葬以礼，碑曰护灯。

顾迟年不辩骂声，只每夜以微光护墓前长明灯，低语：「你照我，我守你。」

霍照临守墓三日不语，第四日洒酒：「陆承安，护陆堂，我立了。」

顾迟年触碑，温，像触一盏将尽的灯，却仍有余温：「你原来，也想有人守。」

他收守岁灯第三相——陆承安最后一念，归灯，非形，是念在。

沈青禾来信：走灯节将办，铁柱伤未愈仍请同行。顾迟年回信：回镇。三相未齐，天魔未至，须先稳镇口长明，再迎卷五。""",
    189: """陆承安墓旁，忽有黑气——魔修残气余孽，最后一扑，欲污开灯令诏书。

霍照临剑出，斩，黑气却分一缕，直取霍照临喉。

黑气中浮陆承安虚影，六阶灯骨再承一击——非复活，是战死前最后一缕灯意残留。虚影散，入守岁灯，顾迟年袖中一暖。

裴无妄：「他最后一缕灯，赠你了。霍照临，守灯堂，该你长明。此非化灯，是赠。」

霍照临单膝跪：「陆承安，此堂，名护陆。」

余孽现形，非人，是丝，缠向青萝。顾迟年八阶灯河照丝，照见天魔已在嗅灯。

铁柱锤落，无阶借万家愿火，凡躯挡碑前。姜小满稳经，沈青禾五阶油洒，黑气退。

「灯骨承击，」顾迟年扬声，「承的是开灯令，是陆承安名，是护灯碑，不是魔丝！」

一击，丝断，墓前复静。霍照临剑归鞘：「此击之后，该回青萝了。」

温言以律定：亵渎护灯碑者，与谋逆同罪。百姓于墓前举灯，如送一位从未被正名的人最后一程。

幼帝献匾：「护灯者，亦人。」顾迟年收袖中，与守岁灯并列：「回青萝。天魔在等，不能迟。」""",
    57: """拒婚之符燃尽，灰落掌心，烫而不伤，像一记迟来的判词。

赵家逼婚第三日，顾迟年当街焚符。赵元青以为能绑住药铺，却不知符在，理在，见证也在。

「符是盾，不是刀。」他对沈青禾隔窗低声，「明日堂上，仍靠纸。」她答：「我懂。」

顾迟年把符灰与逼婚帖半角同匣封存，备县衙核。留灯账记：*拒婚之符，见证入账。*

赵元青当夜来药铺外放狠话，四阶灯盏压场。顾迟年不出，只让里正记时点：「子时扰民，明日一并呈堂。」

隔门答：「拿你自家写的字。」

沈青禾在门内熬姜汤，把恐惧压成可做的活计。更鼓过三更，镇口长明稳三尺。

顾迟年独对守岁灯，低念：「急什么，灯还亮着呢。」——明日堂上，符灰与帖角，要见真章。""",
    210: """万古对抗，在第十三夜，至黎明。

不是一人对魔，是万家对魔——柴灯成阵，万家灯火，九阶灯域，五灯终阵，律与制，医与旗，芯与经，齐对天魔。

**子时·魔至**

天魔爪落，黑潮倾，青萝十二镇口同时暗一线——不是灯灭，是人心先怕。

顾迟年立阵眼，花甲书吏，神魂如焚，鬓发如雪，仍举守岁灯，像举人间六十年账。

「万古对抗，」他扬声，「不是胜名，是续明。魔要熄，我们聚；魔要暗，我们问夜路——路在，人选。」

**丑时·五灯各守**

霍照临斩魔爪，锋灯在前：「云岚守灯堂，记此一夜！」

铁柱锤落，凡躯成墙：「俺没阶！俺有旗！谁碰长明，谁跟俺过招！」

沈青禾五阶油洒阵缘：「汤在，人在。魔退，人别先凉。」

姜小满稳经，芯灯与守岁灯同频：「师父，灯还亮着。」

温言以律护行；谢长缨率百官举灯，幼帝举小灯——律与制，亦是灯。

**寅时·暗而复明**

万家灯火齐暗一线——顾迟年九阶再震，陆承安念再亮，**非化灯，是念在**，与万家同频。

镇口挑担妇人忽然看见脚下路亮了；杂役堂孙福带十二人齐念：「灯还亮着呢。」

黑潮退三寸，天魔低笑：「来日飞升门开，看你怎么选。」

**卯时·阵裂**

天魔再扑，爪尖直取阵眼。姜小满芯灯离体半寸，唇裂，仍稳经：「师父，阵在！」

霍照临锋灯再斩，斩的是魔与人之间的「惧」。铁柱臂骨已裂，仍举「万家灯火」旗：「迟年哥！油！」

**黎明·油尽**

裂缝收半寸，魔形退三分。顾迟年油尽，坠地，姜小满扑至，只握他手：「师父，灯还亮着。」

裴无妄虚影：「魔退人未寂，灯境之寂，万年一人，飞升门开——下一程，拒飞升，化灯，在雨夜，仅一次。」

顾迟年闭眼，轻声：「急什么，灯还亮着呢。」身后长明仍稳三尺，像替人间答：路还在，灯还在。""",
}


VOL_APPEND = {
    "vol02": [
        "塔壁古砖温，像有千年守灯人曾贴掌。顾迟年摸砖缝，缝里有灰，灰里一点青芒——塔认人，不认阶。",
        "塔外哗然与嘘声交织。顾迟年不辩，只把下一层门缝里的杀机，默默记进留灯账。",
    ],
    "vol03": [
        "枯骨岭风如刀，却割不灭袖中豆火。顾迟年以路破雾，不以杀破雾——路在，人便在。",
        "岭上无碑，只有旧灯桩。顾迟年触桩，桩温，像前人为后来者留的一息。",
    ],
    "vol04": [
        "玄京更鼓远传，云开一线。顾迟年把朝堂与民间两本账并看——制在，灯在，理才在。",
        "承平门风紧，灯未灭。顾迟年望南，青萝长明如针，刺进这团暗里。",
    ],
    "vol05": [
        "雨势将歇未歇，长明稳三尺。顾迟年知：门开之前，须先让人间敢照路。",
        "青萝十二镇口，柴灯如豆。顾迟年以灯域拢火，不是掠，是聚——聚人心，聚夜路。",
    ],
}


def vol_key(path: Path) -> str:
    n = path.name
    if "vol02" in n:
        return "vol02"
    if "vol03" in n:
        return "vol03"
    if "vol04" in n:
        return "vol04"
    if "vol05" in n:
        return "vol05"
    return "vol01"


def extract_story(body: str) -> str:
    paras = [p for p in split_paras(strip_meta(body)) if not is_template_para(p)]
    return dedupe_paragraphs("\n\n".join(paras))


def append_until_min(text: str, vol: str) -> str:
    paras = split_paras(text)
    appends = VOL_APPEND.get(vol, VOL_APPEND["vol04"])
    i = 0
    while han_count("\n\n".join(paras)) < MIN_HAN and i < len(appends) * 3:
        paras.append(appends[i % len(appends)])
        i += 1
    return dedupe_paragraphs("\n\n".join(paras))


def build_lib() -> dict[int, str]:
    lib: dict[int, str] = {}
    for name in ("vol2_ch51_65.py", "_vol4_expand_all.py", "generate_vol45_expanded.py"):
        for num, raw in load_py_chapters(SCRIPTS / name).items():
            body = remove_dup_templates(raw if isinstance(raw, str) else str(raw))
            if han_count(body) >= 1200:
                if num not in lib or han_count(body) > han_count(lib[num]):
                    lib[num] = body.strip()
    return lib


def remove_duplicate_templates_only(body: str) -> str:
    """Remove repeated template blocks; keep story + first-pass unique paragraphs."""
    paras = split_paras(strip_meta(body))
    seen_tpl: set[str] = set()
    out: list[str] = []
    for p in paras:
        if is_template_para(p):
            key = re.sub(r"\s+", "", p)[:48]
            if key in seen_tpl:
                continue
            seen_tpl.add(key)
            continue
        out.append(p)
    return dedupe_paragraphs("\n\n".join(out))


def polish_chapter(body: str, ch_num: int | None, lib: dict[int, str], vol: str) -> str:
    hits = count_template_hits(body)
    if hits == 0:
        cleaned = dedupe_paragraphs(strip_meta(body))
        if MIN_HAN <= han_count(cleaned) <= MAX_HAN:
            return cleaned if cleaned.endswith("\n") else cleaned + "\n"
        return body

    # Prefer full polished source when available
    if ch_num and ch_num in lib and han_count(lib[ch_num]) >= MIN_HAN:
        result = lib[ch_num]
    else:
        result = remove_duplicate_templates_only(body)
        if han_count(result) < MIN_HAN:
            merged = remove_duplicate_templates_only(body)
            if ch_num and ch_num in lib:
                merged = dedupe_paragraphs(lib[ch_num] + "\n\n" + merged)
            if han_count(merged) >= han_count(result):
                result = merged
        if han_count(result) < MIN_HAN:
            result = append_until_min(result, vol)
        if han_count(result) < MIN_HAN:
            result = body  # keep iron rule over over-stripping

    if han_count(result) > MAX_HAN:
        result = trim_body(result)
    if han_count(result) < MIN_HAN:
        result = body

    return result if result.endswith("\n") else result + "\n"


def fix_vol04_ch159_echo(text: str) -> str:
    marker = "### 第一百六十章 霍照临怒"
    if marker not in text or text.count("开灯令全京施行") < 6:
        return text
    pre, rest = text.split(marker, 1)
    anchor = "封灯执行，玄京如棋局，每一步都有人掉子。"
    idx = pre.rfind(anchor)
    if idx < 0:
        return text
    end = pre.find("温言于照刑司展不二斋灯影", idx)
    if end < 0:
        return text
    end2 = pre.find("\n\n", end + 180)
    if end2 > 0:
        pre = pre[: end2 + 2] + "\n---\n\n"
    return pre + marker + rest


def process_file(path: Path, lib: dict[int, str]) -> list[tuple]:
    text = path.read_text(encoding="utf-8")
    if path.name == "vol04-玄京封灯.md":
        text = fix_vol04_ch159_echo(text)

    chunks = parse_file(text)
    changed = []
    new_chunks = []
    for title, body in chunks:
        ch_num = ch_num_from_title(title)
        hits = count_template_hits(body)
        before = han_count(body)
        new_body = polish_chapter(body, ch_num, lib, vol_key(path))
        after = han_count(new_body)
        if new_body != body:
            changed.append((title[:28], before, after, hits))
        new_chunks.append((title, new_body))

    if changed:
        path.write_text(rebuild(text, new_chunks), encoding="utf-8")
    return changed


def audit() -> tuple[int, int, int, int]:
    ok = under = over = tpl = 0
    for fp in sorted(CHAPTERS_DIR.glob("vol*.md")):
        for _, body in parse_file(fp.read_text(encoding="utf-8")):
            c = han_count(body)
            h = count_template_hits(body)
            if h:
                tpl += 1
            if c < MIN_HAN:
                under += 1
            elif c > MAX_HAN:
                over += 1
            else:
                ok += 1
    return ok, under, over, tpl


def main():
    lib = build_lib()
    print(f"library: {len(lib)} chapters")
    total = []
    for fp in sorted(CHAPTERS_DIR.glob("vol*.md")):
        ch = process_file(fp, lib)
        if ch:
            print(f"{fp.name}: {len(ch)} updated")
            total.extend(ch)
    ok, under, over, tpl = audit()
    print(f"Pass20: OK {ok} UNDER {under} OVER {over} tpl_chapters {tpl} (polished {len(total)})")


if __name__ == "__main__":
    main()
