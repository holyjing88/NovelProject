#!/usr/bin/env python3
"""留存优先精修：去重/去模板尾 → 换章末悬念钩 → 补足 2000 字。"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose_utils import extract_body_and_footer, hz, norm

PROSE = Path(__file__).resolve().parent.parent / "prose"
LO, HI = 2000, 3000
CANON = re.compile(r"ch0(0[1-9]|[12][0-9]|30|3[1-9]|[4-5][0-9]|60|61)")

# 标杆章不自动改尾钩
SKIP = {"ch001-劫后余寿.md", "ch003-塔鸣初缘.md", "ch037-丹堂大炼.md", "ch049-挽月反戈.md", "ch055-杖剑出.md", "ch061-天试旨到.md"}

FILLER_RE = re.compile(
    r"^(塔鸣极轻|山门风过|风过山门|莫长春念：「[^」]+。」塔鸣轻荡|"
    r"围观弟子终于肯散|弟子终于肯散|他笑：「等|杖答：等)"
)

TEMPLATE_RE = re.compile(
    r"传到最后|添油加醋|踮脚像钩|哼里空一线|余波，还在外门盘桓|"
    r"柳青鸢远观，剑穗无风|霍镇山按刀，刀稳半寸|"
    r"还在弟子的舌根上滚|更深一层，|回头处，像下章|"
    r"盼九月老头下一份|像下章的灯"
)


def load_hooks() -> dict[str, str]:
    spec = importlib.util.spec_from_file_location("t", Path(__file__).parent / "thicken_to_2000.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CHAPTER_HOOKS


HOOKS = load_hooks()

# 章末悬念钩：戏内呈现，非「下一份」预告；每章唯一
RETENTION_END: dict[str, str] = {
    "ch002-师尊赠丹.md": "雨歇，册上「缘」字又亮一线，亮得像催他明日出门——续命丹在匣，该送的人，还在山上某处等着。",
    "ch004-杖中有灵.md": "演武场边，旧剑低鸣一声，鸣得像替赵玄机铁牌敲了记警钟——妒火起了，礼也该起了。",
    "ch005-旧剑新主.md": "霜华剑归鞘，鞘响清，清里像把「回赠」二字先刻在剑脊上，等下一阵风来取。",
    "ch006-霜华回赠.md": "半块灵石躺在案上，小，硬，硬得像一块还没送出去的胆——胆在，路才直。",
    "ch007-半块灵石.md": "顾小满攥石，指白，白里却稳。她不知这半块石会牵出多大浪，只知今日这一步，没歪。",
    "ch008-青狼袭村.md": "村口烟未散，狼嚎远，远里像妖潮在试青岚门的胆——胆在，杖在，礼还在路上。",
    "ch009-老不正经.md": "风大，正好把谣言吹歪一寸；歪了，才好把下一礼送到该送的人手里。",
    "ch010-药渣之心.md": "药渣入炉，炉温起，起得像把「苦里藏甜」四字先炼给全门看。",
    "ch011-丹堂夜语.md": "丹堂夜灯未灭，灭的是流言，亮的是妒与敬——敬多一寸，夜话才真。",
    "ch012-培元被扣.md": "培元丹匣扣在执法堂，扣得住丹，扣不住塔里那笔将起的账。",
    "ch013-执法堂辩.md": "堂上钟响，响在辩毕之后——辩出了轻重，还没辩出孙福膝下那声告状。",
    "ch014-孙福告状.md": "宗主轿影已在山门，轿未到，谣言先沸——沸到堂上，才肯裁。",
    "ch015-宗主裁断.md": "裁断落定，孙福膝软，柳青鸢眸光却亮——亮得像把东脉妖讯，也一并裁进了三月之约。",
    "ch016-赤焰来使.md": "赤焰旗去，血纹犹在门外土上，像七日之期已先咬了一口东脉。",
    "ch017-长老分裂.md": "长老会散，周霍各回，各回里仍有一句未说尽——说尽的，在厉无殇马蹄声里。",
    "ch018-厉无殇至.md": "宴庭灯亮，少谷主笑浅，笑里刀已出鞘半寸——半寸够全场寂然。",
    "ch019-宴庭对峙.md": "席散，帕角仍温，温得像把「和还是战」四个字，先揣进每个人袖里。",
    "ch020-一方手帕.md": "手帕定身一瞬，全场一寂——寂完，魔少脸白，青岚门却多了一张能谈判的牌。",
    "ch021-魔少出丑.md": "丑名出圈，圈外却有人笑——笑的是青岚门终于肯把礼，送到席面上。",
    "ch022-和还是战.md": "和战二字悬在殿上，悬得像一把还没落下去的刀；落下去之前，赵氏妒火先烫了一步。",
    "ch023-赵之妒火.md": "妒火在暗，情报在册——册厚一寸，厚得像把赵氏的路，也记进去了。",
    "ch024-小满情报.md": "册上枯叶证妖讯，证真了，卷末集结的鼓，就该响了。",
    "ch025-卷末集结.md": "集结令下，东脉风硬，硬里像把卷一最后一笔账，推到每个人面前。",
    "ch026-坊市闲逛.md": "名帖搁在茶摊，帖薄，意重——重得像白漱玉在远处，先记了一笔未见的缘。",
    "ch027-第二次妖讯.md": "柱前红贴验真，真了，赵氏收妒，霍氏收刀——刀在等下一阵妖风。",
    "ch028-赵之初见.md": "赵玄机回廊，铁牌在腰，仍不信。不信也好——不信的人，才肯把下一招用出来。百年前那一问，今夜才答了一半。",
    "ch029-闪回一瞬.md": "闪回里，少年赵氏抬头，眼里还有敬——敬若还在，百年后的妒，就还有救。",
    "ch030-卷终夜话.md": "卷一灯灭，塔影却亮，亮得像在卷二门口，先贴了一张请帖。",
    "ch031-商会女修.md": "秦商言合账，笑浅，笑里价已涨——涨的不是茶，是青岚门三月后的路。",
    "ch032-一盒茶饼.md": "茶饼入怀，情报出袖，袖空的人，反而把线送远了。",
    "ch033-公平买卖.md": "买卖响在坊市，响得像给东脉账本，先敲了一声开门鼓。",
    "ch034-东脉账本.md": "账本厚，厚里藏火——火不在纸，在谁肯认那一笔民散之险。",
    "ch035-宗主拍桌.md": "桌响，堂静，静里像把丹方残页四个字，先钉进每个人眼里。",
    "ch036-丹方残页.md": "残页在怀，页轻，意重——重得像七夜炉火，已在远处先亮一线。",
    "ch038-金丹成.md": "丹香未散，体统二字已在廊外等着——等着把成丹，走成门规。",
    "ch039-体统.md": "体统刀未出鞘，鞘响已够苏念慈隔窗一紧——紧完，赤焰又近一日。",
    "ch040-赤焰逼近.md": "韩铁山三日之期，像帖在东脉土上，土还温，温得像血旗先舔了一口。",
    "ch041-三十年.md": "三十年话才开个头，头在莫长春须眉上，眉上像又落了一层旧雪。",
    "ch042-百宝阁二次.md": "百宝阁价又敲了一遍，敲得像告诉全门——礼在价上，价在人心。",
    "ch043-赵之谋.md": "戌时将至，林苑竹静，静里像针——针未落，先疼在证字上。",
    "ch044-误闯.md": "止步三息，未入门，门在，浪也在——浪将湿，嚼将起。",
    "ch045-谣言浪.md": "浪起得凶，退得才快；凶浪尽头，挽月喉里那字，将熟未熟。",
    "ch046-宽恕.md": "思过崖风硬，妒火冷一寸——冷透了，小满那双眼，该亮了。",
    "ch047-小满觉醒.md": "金光敛去，路在册上，册在怀——怀暖，像半块石又长了一块。",
    "ch048-隐匿符.md": "符在袖，形在暗，暗线将走——走的不是正面，是子时那一息。",
    "ch050-赵罚.md": "罚轻，规立，立完东脉云低一线——低得像夜袭在门前先嗅了一口。",
    "ch051-夜袭预兆.md": "飞符入袖，青霜带腥，腥来，符将递，递符的人，不必是老头。",
    "ch052-夜袭备战.md": "三线布防，阵眼将明，明里藏疑——疑在周氏侧门，不在霍氏刀。",
    "ch053-杂役阵.md": "杂役阵成，石在脚，脚稳，暗线才走得直——直路尽头，是东脉夜战。",
    "ch054-东脉夜战.md": "夜战开幕，火起一线，线那头，杖剑尚未出，出则全场寂。",
    "ch056-双妖帅.md": "妖帅退半步，半步里妖核已入手——入手之前，杖剑还在袖里候着。",
    "ch057-周犹豫.md": "侧门闸纹微动，动得像和战二字，先在周德海须上停了一停。",
    "ch058-战后抚伤.md": "抚伤声轻，轻不过布告柱上金纹将贴的那一声哗响。",
    "ch059-赵死守.md": "赵守丹堂，丹在，人在，规也在——规立了，天试帖才肯到。",
    "ch060-天试帖至.md": "缘箓三转，帖在柱，柱响像卷二盖印——盖印之前，旨还在路上。",
}


def is_bad_para(p: str) -> bool:
    if FILLER_RE.match(p.strip()):
        return True
    if TEMPLATE_RE.search(p):
        return True
    if p.strip().startswith("塔鸣极轻"):
        return True
    if "塔鸣轻荡，荡完又静" in p and len(p) < 80:
        return True
    if "下一份，" in p or "下一份、" in p:
        return True
    if "下一章" in p and len(p) < 120:
        return True
    return False


def dedupe_paras(paras: list[str]) -> list[str]:
    """仅去完全重复段，不做子串吞并。"""
    kept: list[str] = []
    seen: set[str] = set()
    for p in paras:
        n = norm(p)
        if n in seen:
            continue
        seen.add(n)
        kept.append(p)
    return kept


def strip_tail_hooks(body: str) -> str:
    """仅从章末向前剥离模板钩段，不删正文中部。"""
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    while paras and is_bad_para(paras[-1]):
        paras.pop()
    while paras and (
        "下一份" in paras[-1]
        or ("下一章" in paras[-1] and len(paras[-1]) < 120)
        or (paras[-1].startswith("莫长春念") and len(paras[-1]) < 120)
        or (paras[-1].startswith("他念") and len(paras[-1]) < 120)
        or (paras[-1].startswith("塔中沉") and len(paras[-1]) < 100)
        or (paras[-1].startswith("塔鸣") and len(paras[-1]) < 80)
    ):
        paras.pop()
    return "\n\n".join(paras)


def ensure_hook(name: str, body: str) -> str:
    hook = RETENTION_END.get(name)
    if not hook:
        theme = HOOKS.get(name, "还礼有时")
        hook = f"风过山门，袖仍空，塔意却沉了一寸——沉里像把「{theme}」先铭于塔壁，等下一阵戏自己开门。"
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    while paras and (
        is_bad_para(paras[-1])
        or "下一份" in paras[-1]
        or norm(paras[-1]) == norm(hook)
        or (hook[:18] in paras[-1] and paras[-1] != hook)
    ):
        if norm(paras[-1]) == norm(hook):
            break
        paras.pop()
    if paras and norm(paras[-1]) == norm(hook):
        return "\n\n".join(paras)
    if paras and hook[:20] in paras[-1] and len(paras[-1]) < len(hook) + 30:
        return "\n\n".join(paras)
    return "\n\n".join(paras + [hook])


def scrub_preview_paras(body: str) -> str:
    """全文剔除「下一份/下一章」预告段与 rumor 模板段。"""
    paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
    return "\n\n".join(p for p in paras if not is_bad_para(p))


def polish_chapter(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    body, footer = extract_body_and_footer(text)
    before = hz(body)
    if path.name in SKIP:
        body = strip_tail_hooks(body)
        paras = dedupe_paras([p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()])
        body = "\n\n".join(paras)
        body = scrub_preview_paras(body)
        paras = [p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()]
        while paras and is_bad_para(paras[-1]):
            paras.pop()
        body = "\n\n".join(paras)
    else:
        body = strip_tail_hooks(body)
        paras = dedupe_paras([p.strip() for p in re.split(r"\n\n+", body.strip()) if p.strip()])
        body = "\n\n".join(paras)
        body = scrub_preview_paras(body)
        body = ensure_hook(path.name, body)
        pad = "弟子渐散，散里仍回头瞧一眼灰袍袖空——瞧得像瞧一眼九月还能走多久。"
        while hz(body) < LO and pad not in body:
            body = body.rstrip() + "\n\n" + pad
            if hz(body) > LO + 80:
                break
    if not footer:
        footer = f"---\n\n*（上架连载稿 · {path.stem.split('-', 1)[1]}）*\n"
    path.write_text(body.rstrip() + "\n\n" + footer, encoding="utf-8")
    return before, hz(body)


def main() -> None:
    rows = []
    for p in sorted(PROSE.glob("ch*.md")):
        if not CANON.match(p.name):
            continue
        rows.append((p.name, *polish_chapter(p)))
    below = [r for r in rows if r[2] < LO]
    filler = 0
    for p in sorted(PROSE.glob("ch*.md")):
        if CANON.match(p.name):
            t = p.read_text(encoding="utf-8")
            filler += t.count("塔鸣极轻，轻像")
    print(f"Retention-polished {len(rows)} chapters")
    print(f"below {LO}: {len(below)}")
    for n, b, a in sorted(below, key=lambda x: x[2]):
        print(f"  {n}: {b} -> {a}")
    print(f"template_tail_remaining: {filler}")
    subprocess.run([sys.executable, str(Path(__file__).parent / "count_prose.py")], check=True)


if __name__ == "__main__":
    main()
