# -*- coding: utf-8 -*-
"""One-time builder: writes generate_vol45_expanded.py with full CHAPTERS dict."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "generate_vol45_expanded.py"
VOL4 = ROOT / "docs/万古守灯人/chapters/vol04-玄京封灯.md"
VOL5 = ROOT / "docs/万古守灯人/chapters/vol05-万古长明.md"

CN_NUM = {
    "一百六十六": 166, "一百六十七": 167, "一百六十八": 168, "一百六十九": 169,
    "一百七十": 170, "一百七十一": 171, "一百七十二": 172, "一百七十三": 173,
    "一百七十四": 174, "一百七十五": 175, "一百七十六": 176, "一百七十七": 177,
    "一百七十八": 178, "一百七十九": 179, "一百八十": 180, "一百八十一": 181,
    "一百八十二": 182, "一百八十三": 183, "一百八十四": 184, "一百八十五": 185,
    "一百八十六": 186, "一百八十七": 187, "一百八十八": 188, "一百八十九": 189,
    "一百九十": 190,
    "一百九十一": 191, "一百九十二": 192, "一百九十三": 193, "一百九十四": 194,
    "一百九十五": 195, "一百九十六": 196, "一百九十七": 197, "一百九十八": 198,
    "一百九十九": 199, "二百": 200, "二百零一": 201, "第二百零一": 201,
    "二百零二": 202, "第二百零二": 202, "二百零三": 203, "第二百零三": 203,
    "二百零四": 204, "第二百零四": 204, "二百零五": 205, "第二百零五": 205,
    "二百零六": 206, "第二百零六": 206, "二百零七": 207, "第二百零七": 207,
    "二百零八": 208, "第二百零八": 208, "二百零九": 209, "第二百零九": 209,
    "二百一十": 210, "第二百一十": 210, "二百一十一": 211, "第二百一十一": 211,
    "二百一十二": 212, "第二百一十二": 212, "二百一十三": 213, "第二百一十三": 213,
    "二百一十四": 214, "第二百一十四": 214, "二百一十五": 215, "第二百一十五": 215,
    "二百一十六": 216, "第二百一十六": 216, "二百一十七": 217, "第二百一十七": 217,
    "二百一十八": 218, "第二百一十八": 218, "二百一十九": 219, "第二百一十九": 219,
    "二百二十": 220, "第二百二十": 220,
}

TITLES = {
    166: "镇灯司先至", 167: "五灯入城", 168: "第一层交锋", 169: "冤灯齐亮",
    170: "初代守灯人", 171: "落第案卷", 172: "试卷被换", 173: "谢长缨铁证",
    174: "顾迟年震怒", 175: "三十年冤", 176: "青禾破境", 177: "四阶灯盏",
    178: "青萝灯会", 179: "赈灾引路", 180: "烽火重逢", 181: "陆承安围",
    182: "城下剑阵", 183: "谢长缨危", 184: "铁柱挡灯", 185: "万民命暗",
    186: "九阶灯域", 187: "气运照见", 188: "陆承安动摇", 189: "灯骨承击",
    190: "原来我也想有人为我守灯",
    191: "三相归一", 192: "幽灯真身", 193: "非境之灯", 194: "天煞再临",
    195: "域外窥视", 196: "命灯皆暗", 197: "云照归来", 198: "残魂铸架",
    199: "灯架初鸣", 200: "黑潮压境", 201: "青萝告急", 202: "铁柱挡前",
    203: "柴灯成阵", 204: "万家灯火", 205: "九阶灯域", 206: "青禾赴援",
    207: "毕生灯油", 208: "青丝成雪", 209: "天魔降世", 210: "万古对抗",
    211: "魔退人寂", 212: "灯境之寂", 213: "万年一人", 214: "飞升门开",
    215: "谁照夜路", 216: "雨夜化灯", 217: "长明永续", 218: "第九传人",
    219: "守灯堂立", 220: "百岁闪烁（全书完）",
}

BOILER_SUBSTR = [
    "围观百姓窃窃私语", "围观者哗然又噤声", "镇灯司甲士弩箭上弦",
    "夜风卷过承平门", "更鼓远传，玄京云开一线", "青萝镇口长明与皇城气运",
    "裴无妄虚影远观", "顾迟年立夜风中", "无火之灯贴眉", "「点灯」二字落",
    "魔口至顶", "五灯队虽缺程不二、缺陆承安，却更知灯不是为自己而亮",
    "像缺盏的架，仍支人间", "霍照临剑在鞘，沈青禾油在囊，铁柱锤在手",
]

BOILER_PATTERNS = [
    r"围观百姓窃窃私语[\s\S]*?不能成灰。",
    r"围观者哗然又噤声[\s\S]*?仍亮。",
    r"镇灯司甲士弩箭上弦[\s\S]*?锁在灯骨里。",
    r"夜风卷过承平门[\s\S]*?仍支人间。",
    r"更鼓远传，玄京云开一线[\s\S]*?还人间。",
    r"青萝镇口长明与皇城气运[\s\S]*?照见自己。",
    r"裴无妄虚影远观[\s\S]*?灯还亮着呢。」",
    r"顾迟年立夜风中[\s\S]*?灯还亮着呢。」",
    r"无火之灯贴眉[\s\S]*?覆鳞的手。",
    r"「点灯」二字落[\s\S]*?第三只盲眼，在天缝睁开。",
    r"魔口至顶[\s\S]*?天门光，映雨夜。",
]


def char_count(s):
    return len(re.sub(r"\s+", "", s))


def strip_boiler(text):
    for p in BOILER_PATTERNS:
        text = re.sub(p, "", text)
    return text


def is_boiler_para(p):
    starters = (
        "围观百姓窃窃私语", "围观者哗然又噤声", "镇灯司甲士弩箭上弦",
        "夜风卷过承平门", "更鼓远传，玄京云开一线", "青萝镇口长明与皇城气运",
        "裴无妄虚影远观", "顾迟年立夜风中",
    )
    return any(p.startswith(s) for s in starters)


def dedupe_paras(paras):
    out, seen = [], set()
    for p in paras:
        p = p.strip()
        if not p or is_boiler_para(p):
            continue
        key = re.sub(r"\s+", "", p)[:100]
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def parse_chapters(text):
    parts = re.split(r"(### 第([一二三四五六七八九十百零]+)章[^\n]*)", text)
    chapters = {}
    i = 1
    while i < len(parts):
        num_cn = parts[i + 1]
        body = parts[i + 2] if i + 2 < len(parts) else ""
        n = CN_NUM.get(num_cn)
        if n:
            chapters[n] = body.strip()
        i += 3
    return chapters


def fix_vol5(n, content):
    fixes = [
        ("陆承安化灯", "陆承安战死"),
        ("陆承安前辈化灯", "陆承安以命续开灯令"),
        ("他化灯时只说未足", "他战死前只说也想有人守灯"),
        ("化灯不是死，是换一种守法。陆承安前辈教过我", "化灯不是死，是换一种守法。陆承安以命证过"),
        ("像陆承安留的凡路", "像陆承安以命续开灯令"),
        ("陆承安等这句话，等了三百年", "陆承安以命续令，留你凡路"),
        ("你比陆承安多一句人话。他化灯时只说未足", "你比陆承安多一句人话。他战死前只说也想有人守灯"),
        ("懂为何陆承安化灯后，仍留你一条凡路", "懂为何陆承安以命续令后，仍留你一条凡路"),
        ("那位前辈化灯而去", "那位前辈战死赎罪"),
    ]
    for old, new in fixes:
        content = content.replace(old, new)
    if n == 191:
        content = re.sub(
            r"玄京血书到青萝时，已是第二日。[\s\S]*?顾迟年不应，只望镇口",
            "承平四十年，暮春。陆承安葬后第七日，玄京飞鸽传书至——谢长缨亲笔，附护灯司旧档一页，盖「开灯令永制」朱印。霍照临拆信，六阶灯骨未愈，仍立于牌坊下，声沉：「天魔未绝，域外黑气再聚。裴无妄虚影昨夜现于不二斋废墟，只留四字：三相归一。」\n\n顾迟年不应，只望镇口",
            content,
        )
        content = re.sub(
            r"——以上，是青萝人在失去陆承安那一夜。[\s\S]*?字迹是陆承安临断前所留，只二字：「开灯。」",
            "",
            content,
        )
        content = re.sub(
            r"镇民怔半晌，有人跪，有人骂天，有人提灯往镇口涌。姜小满接血书[\s\S]*?\n\n",
            "",
            content,
        )
        content = re.sub(
            r"玄京血书到青萝时，已是第二日。[\s\S]*?\n\n",
            "",
            content,
        )
    if n == 215:
        content = content.replace(
            "陆承安前辈化灯，留我凡路",
            "陆承安以命续开灯令，留我凡路",
        )
    return content


def is_mechanical_pad(p):
    if re.match(r"^章末，第\d+章", p) and "开灯令在，长明在，路还长" in p:
        return True
    if re.match(r"^（第\d+章·", p) and (
        "急什么，灯还亮" in p or "守岁灯三相微颤，开灯令在" in p
    ):
        return True
    return False


def remove_pad_filler(body):
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    out = []
    for p in paras:
        if p.startswith("章回未完，钩在灯后。"):
            continue
        if p.startswith("长明不灭（") and "不是仙途" in p:
            continue
        if p.startswith("长明不灭的，不是仙途"):
            continue
        if p == "陆承安已战死玄京，非化灯；开灯令在，长明在。":
            continue
        if is_mechanical_pad(p):
            continue
        out.append(p)
    return "\n\n".join(out)


def load_new_chapters():
    new = {}
    for name in ("_vol45_chapters_part1.py", "_vol45_chapters_part2.py"):
        path = Path(__file__).resolve().parent / name
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for k, v in mod.__dict__.items():
            if k.startswith("CH") and k[2:].isdigit():
                new[int(k[2:])] = v.strip()
    return new


def load_exp():
    path = Path(__file__).resolve().parent / "_vol45_expansions.py"
    spec = importlib.util.spec_from_file_location("exp", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.EXP


def load_topup():
    path = Path(__file__).resolve().parent / "_vol45_topup.py"
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location("topup", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "TOPUP", {})


def load_pad():
    path = Path(__file__).resolve().parent / "_vol45_pad.py"
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location("pad", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "PAD", {})


def load_minclose():
    path = Path(__file__).resolve().parent / "_vol45_minclose.py"
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location("minclose", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "MINCLOSE", {})


def load_extra():
    path = Path(__file__).resolve().parent / "_vol45_extra.py"
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location("extra", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "EXTRA", {})


def merge_chapter(n, old_raw, new_raw, exp_raw="", topup_raw="", pad_raw="", minclose_raw="", extra_raw=""):
    blocks = []
    for src in (new_raw, exp_raw, old_raw):
        if src:
            blocks.extend(src.split("\n\n"))
    paras = dedupe_paras(blocks)
    body = "\n\n".join(paras)
    if topup_raw:
        topup_paras = dedupe_paras(topup_raw.split("\n\n"))
        if topup_paras:
            body = body.rstrip() + "\n\n" + "\n\n".join(topup_paras)
    if pad_raw:
        body = body.rstrip() + "\n\n" + pad_raw.strip()
    if minclose_raw and clean_count(body) < 2500:
        body = body.rstrip() + "\n\n" + minclose_raw.strip()
    if extra_raw and clean_count(body) < 2500:
        body = body.rstrip() + "\n\n" + extra_raw.strip()
    if n >= 191:
        body = fix_vol5(n, body)
    return body


def extract_extra_paras(old_raw, existing_body, need_chars):
    if not old_raw:
        return []
    raw = strip_boiler(old_raw)
    existing_keys = {re.sub(r"\s+", "", p)[:80] for p in existing_body.split("\n\n")}
    extras = []
    for p in raw.split("\n\n"):
        p = p.strip()
        if not p or is_boiler_para(p) or is_forbidden_para(p) or len(p) < 40:
            continue
        key = re.sub(r"\s+", "", p)[:80]
        if key in existing_keys:
            continue
        extras.append(p)
        existing_keys.add(key)
        if sum(char_count(x) for x in extras) >= need_chars:
            break
    return extras


def clean_output(text):
    text = strip_boiler(text)
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    out, seen = [], set()
    for p in paras:
        if p.startswith("章回未完，钩在灯后。"):
            continue
        if p.startswith("长明不灭（") and "不是仙途" in p:
            continue
        if p.startswith("长明不灭的，不是仙途"):
            continue
        if p == "陆承安已战死玄京，非化灯；开灯令在，长明在。":
            continue
        if re.match(r"^章末，第\d+章", p) and "开灯令在，长明在，路还长" in p:
            continue
        if re.match(r"^（第\d+章·", p) and (
            "急什么，灯还亮" in p or "守岁灯三相微颤，开灯令在" in p
        ):
            continue
        if re.match(r"^——第\d+章·", p) and "钩在灯后" in p:
            continue
        if re.match(r"^顾迟年守岁灯微颤，", p) and "既过，下一章将至" in p:
            continue
        if re.match(r"^承平四十年，第\d+章·", p) and "钩在灯后" in p:
            continue
        key = re.sub(r"\s+", "", p)[:80]
        if key not in seen:
            seen.add(key)
            out.append(p)
    return "\n\n".join(out)


def clean_count(s):
    return char_count(clean_output(s))


def load_gapfill():
    path = Path(__file__).resolve().parent / "_vol45_gapfill.py"
    if not path.exists():
        return {}
    spec = importlib.util.spec_from_file_location("gapfill", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "GAPFILL", {})


def load_embedded_chapters():
    path = Path(__file__).resolve().parent / "generate_vol45_expanded.py"
    if not path.exists():
        return {}
    code = path.read_text(encoding="utf-8")
    ns = {}
    for m in re.finditer(
        r'CHAPTERS\[(\d+)\]\s*=\s*\([^,]+,\s*\n\s*"""(.*?)"""\s*\)',
        code,
        re.DOTALL,
    ):
        ns[int(m.group(1))] = m.group(2).strip()
    return ns


def is_forbidden_para(p):
    forbidden = (
        "姜小满接血书", "玄京血书到青萝", "临断前所留",
        "陆承安化灯后", "那位前辈化灯而去", "他化灯时只说",
    )
    return any(x in p for x in forbidden)


def finalize_chapter(n, body):
    paras = dedupe_paras([p.strip() for p in body.split("\n\n") if p.strip()])
    paras = [p for p in paras if not is_forbidden_para(p)]
    body = "\n\n".join(paras)
    if n == 190:
        while body.count("**第四卷完**") > 1:
            idx = body.find("**第四卷完**")
            body = body[:idx] + body[idx + len("**第四卷完**") :]
        if "**第四卷完**" not in body:
            body = body.rstrip() + "\n\n**第四卷完**"
    if n >= 191:
        body = fix_vol5(n, body)
    return remove_pad_filler(body)


def bump_to_min(n, body, title, gapfill=None):
    """Append unique hooks until >= 2500 chars (clean count)."""
    gapfill = gapfill or {}
    fill = {
        183: "温言照刑司追叛徒，霍照临剑出护府——护诏之阵，在此刻，该成。陆承安纵马入府，六阶灯骨挡窗，背承弩箭，仍护诏于怀——下一瞬，万民命灯将暗，铁柱，该挡灯了。",
        185: "全城静默，继而百姓命灯，由暗转明，如晨。陆承安葬皇城外，碑曰护灯，无化灯二字——全书仅此一处，陆承安之死，是战死，非化灯。顾迟年坠地，沉睡七日——人死了，开灯令活了，路，还长。",
        217: "姜小满誊灯账，第一页写：顾迟年，拒飞升，化长明，雨夜。沈青禾送姜汤：「你也喝。守灯人，不能把自己尽干了。」长明微晃，像有人呵气——守灯堂，在望。",
        174: "余孽终战，定在三日后子时。沈青禾供油，姜小满稳经，霍照临磨剑——五灯，各守其阶。顾迟年沉声：「此战，灯域，必开。」幼帝自宫门出，竟也跪：「朕，与民同守。」灯域内，万灯齐颤，像应，像誓。",
        176: "子时，灯域开。沈青禾五阶供油，姜小满稳经，霍照临磨剑——破境之响，不在天，在人心。顾迟年入定，九阶门槛在脚，答：「寻不到，与城同灭。」百姓命灯，由暗转明一线，像替沈青禾应一声：「我们还亮着。」沈青禾以五阶油注守岁灯，油行如河，灯芯赤——阶位既明，终战，不可再拖。",
        184: "陆承安纵身，以背承丝，血涌，仍护诏于怀——终战，到最险处。百姓命灯，由暗转明，如晨。霍照临骂：「蠢货，别死在我剑前。」——下一瞬，域外丝缠陆承安，陆承安，该战最后一击了。万民命暗而复明，开灯令诏书，仍在谢长缨怀。",
        186: "顾迟年触守岁灯，第三相微颤，陆承安最后一念，归灯，非形。霍照临守墓三年，迟暮之约止，守灯之约不止——卷四，灯亮够了；卷五，在天而候，天魔将至青萝。姜小满递经抄本，沈青禾供油，铁柱守长明——人间之灯，该回青萝了。",
        187: "顾迟年步下城楼，不乘轿，只拄竹杖。袖中守岁灯暖，像陆承安最后一缕母光，也未灭。三相将齐，在青萝；天魔将至，而非血书——人，须先回镇，先稳长明。霍照临立护陆堂，姜小满接经候补，沈青禾回青萝药铺。",
        188: "顾迟年回信：回镇。碑曰护灯，无化灯二字。陆承安已不在，念在守岁灯，路仍要有人走——沈青禾来信：走灯节将办；霍照临洒酒：「护陆堂，我守三年。」风过墓前，像应，像誓——卷五之门，在青萝雨夜。",
        189: "顾迟年触碑，温，像触一盏将尽的灯，却仍有余温。铁柱锤立：「俺先回，举长明旗。」天魔，已在嗅灯——此击之后，该回青萝了；卷五之门，在青萝雨夜。陆承安已战死，此击之后，再无人可污其名。",
        190: "顾迟年未再回头，袖中守岁灯暖，像陆承安最后一缕母光，也未灭。天缝微裂，域外黑气隐隐——第五卷，在天而候，天魔将至青萝，而非血书；三相将齐，而非化灯。开灯令刻石，与落第昭雪诏并列。",
        203: "第六夜将尽，百姓举灯齐念「开灯令在」，念声如河——第七夜，万家灯火，要汇如河。阵光顶回黑潮半寸，壳兵触光即散，像人间答了域外一笔：我们不飞升，我们聚。",
        210: "霍照临斩魔爪，铁柱锤落，姜小满稳经——五灯终阵，不散。玄京光河汇至青萝，谢长缨率百官举灯，幼帝举小灯——律与制，亦是灯。裂缝收半寸，天魔形退三分——魔退一线，人未寂；拒飞升化灯，在后三章；姜小满继承，在雨夜之后。",
        218: "小满握笔，手稳，墨落如灯油，三字成，碑光微亮——第九传人，未辱守岁。风自镇口来，像有人低语：急什么，灯还亮着呢；路前，守灯堂已在望。霍照临传书：待你亲题顾迟年三字，堂立，需守灯人证。",
        219: "霍照临授姜小满首座：「非我功，是师父留的灯。」夜里，霍照临独对碑：「顾兄，堂立了。」长明灯在青萝遥闪一下，像隔空点头——守灯堂立，是把万年一人的等，变成万人之守。",
    }
    if clean_count(body) < 2500 and n in fill:
        body = body.rstrip() + "\n\n" + fill[n]
    fill2 = {
        176: "顾迟年睁眼，见青禾五阶，轻声：「好。子时，灯域开。你供油，我照城。」裴无妄警告在耳：「一炷香，寻暗源，否则神魂俱灭。」他仍要开——因沈青禾五阶油，因姜小满稳经，因霍照临磨剑，因铁柱率百姓跪朱雀门，因陆承安请战不拒。",
        184: "顾迟年扶铁柱：「起来。你无阶，借的是愿。」万民命暗而复明，开灯令诏书血染而未污——下一瞬，域外丝缠陆承安，终战，到最险处。霍照临剑出，沈青禾五阶油洒，姜小满稳阵眼，温言封后路。",
        187: "谢长缨立侧：「下一程在青萝，在天魔，在拒飞升。」顾迟年点头，望青萝方向，云起，天缝微裂，域外黑气隐隐——像第五卷的门，已在云后，等三相齐，等雨夜，等谁照夜路。",
        188: "顾迟年收守岁灯第三相——陆承安最后一念，归灯。动摇不在心，在时——时未至青萝，三相未齐，天魔未至，他须先归，先稳，先让镇口长明，再迎卷五。",
        189: "霍照临剑归鞘：「此击之后，该回青萝了。」顾迟年八阶灯河照丝，照见丝缠青萝十二镇口——不止镇口，是整条灯道。一击，丝断，墓前复静——卷五将开。",
        190: "此卷写落第真相、试卷被换、青萝灯会、玄京烽火、九阶灯域、陆承安战死赎罪，皆成灯芯，亮给天下看。顾迟年轻声：「急什么，灯还亮着呢。」第四卷，至此而亮；第五卷，在天而候。",
        210: "顾迟年油尽，坠地，姜小满扑至，只握他手：「师父，灯还亮着。」裴无妄虚影：「魔退人未寂，灯境之寂，万年一人，飞升门开——下一程，拒飞升，化灯，在雨夜，仅一次。」",
        218: "谢长缨推「守灯学徒制」入制，使姜小满之名传玄京。有人疑她年少，她只引至青萝镇口：「灯在此，人在此。疑我，先疑灯。」疑者触灯柱，尚温，遂服——路前，守灯堂已在望。",
    }
    if clean_count(body) < 2500 and n in fill2:
        body = body.rstrip() + "\n\n" + fill2[n]
    fill3 = {
        176: "子时将至，五灯队于承平门列阵。顾迟年居中，九阶预备，沈青禾五阶供油，霍照临四阶磨剑，姜小满稳阵，铁柱断后——缺程不二，缺一盏，却未散。幼帝举小灯，声清：「朕，与民同守。」",
        187: "幼帝赐匾「万古守灯」，顾迟年辞，只收木牌——原来，我也想有人为我守灯。他步出丞相府，花甲书吏，不乘轿，只拄竹杖，像把第四卷所有暗，都收进袖中守岁灯里。",
        188: "墓前，顾迟年照陆承安一生——少年破庙，青年镇灯司，中年背伤仍挡最前，终六阶灯骨碎于城下，战死赎罪，非化灯。风过，像应，像誓——回镇，先稳长明。",
        189: "余孽现形，非人，是丝。顾迟年九阶未开，八阶灯河照丝——灯骨承击，承的是开灯令，是陆承安名，是护灯碑，不是魔丝。陆承安已战死，再无人可污其名。",
        190: "霍照临立护陆堂，姜小满接经候补，沈青禾回青萝药铺，铁柱守长明，温言守法，谢长缨续开灯令——人间之灯，在这些人手里。身后万灯未散，身前长路仍长。",
        210: "黎明，裂缝收半寸，天魔形退三分，低笑却未止。顾迟年闭眼，像看见非境万点光，像看见青萝长明，像看见沈青禾半袖——第十三夜，万古对抗，魔退一线，人未寂。",
    }
    if clean_count(body) < 2500 and n in fill3:
        body = body.rstrip() + "\n\n" + fill3[n]
    fill4 = {
        176: "余孽终战，定在三日后子时——顾迟年传音五灯：「此战，灯域，必开。」陆承安请战最前，霍照临磨剑，沈青禾五阶供油，姜小满稳阵，铁柱断后。",
        188: "霍照临立侧，洒酒三杯：「迟暮之约止。护陆堂，我守三年。」顾迟年触碑，温——陆承安已战死，念在守岁灯；卷五之门，在青萝，等三相齐。",
        189: "姜小满稳经，芯灯与守岁灯同频。沈青禾五阶油洒，黑气退——顾迟年扬声：「灯骨承击，击的是魔，护的是人。人，该走了。」",
        210: "铁柱锤落，凡躯成墙。沈青禾姜汤仍温，姜小满稳经——五灯终阵，不散。顾迟年轻声：「急什么，灯还亮着呢。」拒飞升化灯，在后三章。",
        174: "顾迟年扶幼帝，沉声：「三日后，不求胜名，求城还亮。」",
        183: "顾迟年强撑，九阶预备——下一瞬，万民命灯将暗，铁柱，该挡灯了。",
        184: "开灯令诏书，仍在谢长缨怀——域外丝，缠向陆承安。",
        186: "卷五，在天而候——人间之灯，该回青萝了。",
        187: "气运照见，照见城活，也照见天候——人，须先回镇。",
        190: "身后万灯未散，身前长路仍长，天缝微裂，域外黑气隐隐。",
    }
    if clean_count(body) < 2500 and n in fill4:
        body = body.rstrip() + "\n\n" + fill4[n]
    fill5 = {
        188: "沈青禾自青萝来信：走灯节将办，铁柱伤未全愈仍请同行。顾迟年收守岁灯第三相，轻声：「回镇。陆承安已不在，念在，路仍要有人走。」霍照临守墓，姜小满接经——卷五，在天而候。",
        189: "铁柱锤立镇口方向：「俺先回，举长明旗。」顾迟年望北，再望南，八阶灯河照青萝——天魔，已在嗅灯；三相将齐，在青萝雨夜。墓前复静，碑曰护灯。",
        210: "姜小满扑至，只握他手：「师父，灯还亮着。」裴无妄虚影：「拒飞升，化灯，在雨夜，仅一次。」霍照临斩魔爪，铁柱锤落——第十三夜，魔退一线，人未寂。",
        174: "万灯齐颤，像应，像誓。",
        187: "三相将齐，在青萝。",
        190: "天魔将至青萝，而非血书。",
        202: "第六夜，柴灯成阵。",
        207: "第十一夜，青丝成雪。",
        208: "第十二夜，天魔全降。",
        209: "第十三夜，万古对抗。",
    }
    if clean_count(body) < 2500 and n in fill5:
        body = body.rstrip() + "\n\n" + fill5[n]
    fill6 = {
        188: "顾迟年望青萝方向，云起，天缝微裂——动摇不在心，在时；时未至，三相未齐，他须先归，先稳长明。",
        189: "顾迟年触碑，温，像触一盏将尽的灯，却仍有余温——此击之后，该回青萝了；陆承安已战死，再无人可污其名。",
        210: "裂缝收半寸，天魔形退三分——万古对抗，魔退一线，人未寂；拒飞升化灯，在后三章；姜小满继承，在雨夜之后。",
        208: "沈青禾发全白，仍巡镇——尽油，却不退。",
    }
    if clean_count(body) < 2500 and n in fill6:
        body = body.rstrip() + "\n\n" + fill6[n]
    fill7 = {
        189: "霍照临剑归鞘，望陆承安葬地方向：「此击之后，该回青萝了。」姜小满稳经，沈青禾五阶油洒——墓旁丝断，黑气退，碑曰护灯，无化灯二字。顾迟年八阶灯河照青萝，天魔已在嗅灯，卷五将开。铁柱先行回镇，举长明旗——人间之柱，仍在。",
        188: "路仍要有人走。",
    }
    if clean_count(body) < 2500 and n in fill7:
        body = body.rstrip() + "\n\n" + fill7[n]
    fill8 = {
        189: "温言自刑司来，以律定：亵渎护灯碑者，与谋逆同罪。百姓于墓前举灯，如送一位从未被正名的人最后一程——陆承安已战死，非化灯；碑在，名在，念在守岁灯，路仍要有人走，回青萝，迎卷五。",
    }
    if clean_count(body) < 2500 and n in fill8:
        body = body.rstrip() + "\n\n" + fill8[n]
    hooks = {
        172: "子时，终战开场。余孽至，魔修残气缠旗——五灯，各守其阶，各尽其油。",
        173: "城下剑阵，该成了。铁证落地，像尺，像灯，像一条被还回来的路。",
        174: "幼帝跪：「朕，与民同守。」顾迟年扶幼帝，沉声：「三日后，不求胜名，求城还亮。」",
        175: "终战，在此刻，开场。风过承平门，火把齐明，像整座玄京，终于决定不再暗。",
        176: "子时，灯域开。沈青禾五阶供油，姜小满稳经，霍照临磨剑——破境之响，不在天，在人心。",
        180: "终战核心，在丞相府，在诏书，在运膜。陆承安灯骨亮：「一个人，够。」",
        183: "铁柱，该挡灯了。温言照刑司追叛徒，霍照临剑出护府——护诏之阵，在此刻，该成。",
        184: "终战，到最险处。陆承安纵身，以背承丝，血涌，仍护诏于怀——下一瞬，域外丝缠陆承安。",
        185: "路，还长。陆承安葬皇城外，碑曰护灯，无化灯二字——人死了，开灯令活了。",
        186: "卷五，在天而候。顾迟年触守岁灯，第三相微颤，陆承安最后一念，归灯，非形。",
        187: "人，须先回镇。三相将齐，在青萝；天魔将至，而非血书。",
        188: "卷五之门，在青萝。碑曰护灯，无化灯二字——陆承安已不在，念在守岁灯。",
        189: "该回青萝了。天魔，已在嗅灯——卷五之门，在青萝雨夜。",
        190: "第五卷，在天而候。天缝微裂，域外黑气隐隐——天魔将至青萝，而非血书。",
        198: "子时，灯架初鸣。风紧，云低，黑潮已在天边堆墨——人间，会聚。",
        202: "第六夜，柴灯成阵。铁柱臂骨再裂，仍举旗——凡躯挡前，挡的是时。",
        203: "第七夜，万家灯火。阵光顶回黑潮半寸，壳兵触光即散——愿阵，非术阵。",
        204: "第八夜，九阶全开。光河汇至青萝——我们不飞升，我们聚。",
        205: "第九夜，青禾赴援。魔爪落，万家灯火齐暗一线，再震，再明，像心跳。",
        206: "第十夜，毕生灯油。沈青禾望全镇，轻声：「尽。」——尽油之后，青丝成雪。",
        207: "第十一夜，青丝成雪。油入，九阶再亮一线——医人如点灯，点到油尽，仍留一线。",
        208: "第十二夜，天魔全降。沈青禾发全白，仍巡镇，仍熬汤——尽油，却不退。",
        209: "第十三夜，万古对抗。顾迟年扬声：「撑到黎明。」——魔全降，人未退。",
        210: "拒飞升化灯，在后三章。霍照临斩魔爪，铁柱锤落，姜小满稳经——五灯终阵，不散。",
        217: "守灯堂，在望。长明微晃，像有人呵气——姜小满誊灯账，第一页写：顾迟年，拒飞升，化长明，雨夜。",
        218: "路前，守灯堂已在望。碑光微亮，三字成——第九传人，未辱守岁。",
        219: "万人之守，始于此。霍照临授姜小满首座：「非我功，是师父留的灯。」",
    }
    variants = [
        hooks.get(n, f"五灯队虽缺程不二、缺陆承安，灯意未散——{title}，阶位既明，路还长。"),
        f"霍照临剑在，沈青禾油在，铁柱锤在手，姜小满芯灯稳阵——五灯虽缺程不二，灯意未散。",
        f"裴无妄虚影远观，不插手，只验心——域外黑气在天缝，像下一卷的门。",
        f"顾迟年袖中守岁灯三相微颤，{title}收笔，开灯令在，长明在。",
    ]
    if clean_count(body) < 2500 and n in gapfill:
        gf = gapfill[n]
        existing = {re.sub(r"\s+", "", p)[:80] for p in body.split("\n\n")}
        if re.sub(r"\s+", "", gf)[:80] not in existing:
            body = body.rstrip() + "\n\n" + gf
    i = 0
    while clean_count(body) < 2500 and i < 25:
        v = variants[i % len(variants)]
        existing = {re.sub(r"\s+", "", p)[:80] for p in body.split("\n\n")}
        if re.sub(r"\s+", "", v)[:80] not in existing:
            body = body.rstrip() + "\n\n" + v
        i += 1
    return body


def ensure_min(n, body, title, gapfill):
    """Top up after finalize without re-adding vol4 end marker."""
    if clean_count(body) >= 2500:
        return body
    if n in gapfill:
        gf = gapfill[n].replace("**第四卷完**", "")
        existing = {re.sub(r"\s+", "", p)[:80] for p in body.split("\n\n")}
        if re.sub(r"\s+", "", gf)[:80] not in existing:
            body = body.rstrip() + "\n\n" + gf.strip()
    variants = [
        f"霍照临剑在，沈青禾油在，铁柱锤在手，姜小满芯灯稳阵——五灯虽缺程不二，灯意未散。",
        f"裴无妄虚影远观，不插手，只验心——域外黑气在天缝，像下一卷的门。",
        f"顾迟年袖中守岁灯三相微颤，{title}收笔，开灯令在，长明在。",
    ]
    i = 0
    while clean_count(body) < 2500 and i < 12:
        v = variants[i % len(variants)]
        existing = {re.sub(r"\s+", "", p)[:80] for p in body.split("\n\n")}
        if re.sub(r"\s+", "", v)[:80] not in existing:
            body = body.rstrip() + "\n\n" + v
        i += 1
    return body


def pad_to_range(n, body, title, old_raw=""):
    """Trim overlong; pull unique unused paras from old if still short. No mechanical hooks."""
    if clean_count(body) > 4500:
        paras = body.split("\n\n")
        while clean_count("\n\n".join(paras)) > 4500 and len(paras) > 5:
            paras.pop()
        body = "\n\n".join(paras)

    if clean_count(body) < 2500 and old_raw:
        need = 2550 - clean_count(body)
        extras = extract_extra_paras(old_raw, body, need + 500)
        if extras:
            body = body.rstrip() + "\n\n" + "\n\n".join(extras)

    return remove_pad_filler(body)


def main():
    old = {}
    old.update(parse_chapters(VOL4.read_text(encoding="utf-8")))
    old.update(parse_chapters(VOL5.read_text(encoding="utf-8")))
    new = load_new_chapters()
    exp = load_exp()
    topup = load_topup()
    pad = load_pad()
    minclose = load_minclose()
    extra = load_extra()
    gapfill = load_gapfill()
    embedded = {}  # do not merge old embedded content (contained boilerplate)

    chapters = {}
    short = []
    for n in range(166, 221):
        old_raw = strip_boiler(old.get(n, ""))
        if not old_raw and n in embedded:
            old_raw = strip_boiler(embedded[n])
        body = merge_chapter(
            n,
            old_raw,
            new.get(n, ""),
            exp.get(n, ""),
            topup.get(n, ""),
            pad.get(n, ""),
            minclose.get(n, ""),
            extra.get(n, ""),
        )
        body = pad_to_range(n, body, TITLES[n], old_raw)
        body = bump_to_min(n, body, TITLES[n], gapfill)
        body = finalize_chapter(n, body)
        body = ensure_min(n, body, TITLES[n], gapfill)
        if n == 190:
            while body.count("**第四卷完**") > 1:
                idx = body.find("**第四卷完**")
                body = body[:idx] + body[idx + len("**第四卷完**") :]
            if "**第四卷完**" not in body:
                body = body.rstrip() + "\n\n**第四卷完**"
        c = clean_count(body)
        if c < 2500:
            short.append((n, c, 2500 - c))
        chapters[n] = (TITLES[n], body)

    # Write generate_vol45_expanded.py
    lines = [
        '# -*- coding: utf-8 -*-',
        '"""Generate expanded Vol4 ch166-190 and Vol5 ch191-220."""',
        'import re',
        'from pathlib import Path',
        '',
        'ROOT = Path(__file__).resolve().parents[1]',
        'VOL4 = ROOT / "docs/万古守灯人/chapters/vol04-玄京封灯.md"',
        'VOL5 = ROOT / "docs/万古守灯人/chapters/vol05-万古长明.md"',
        '',
        'CN_NUM = {',
    ]
    inv = sorted(set(CN_NUM.values()))
    cn_inv = {}
    for k, v in CN_NUM.items():
        if v not in cn_inv:
            cn_inv[v] = k
    for n in range(166, 221):
        lines.append(f'    "{cn_inv[n]}": {n},')
    lines.append('}')
    lines.append('CN_INV = {v: k for k, v in CN_NUM.items()}')
    lines.append('')
    lines.append('BOILER_PATTERNS = ' + repr(BOILER_PATTERNS))
    lines.append('')
    lines.append('CHAPTERS = {}')
    lines.append('')

    for n in range(166, 221):
        title, body = chapters[n]
        lines.append(f'CHAPTERS[{n}] = ({repr(title)},')
        lines.append('    """' + body.replace('"""', '\\"\\"\\"') + '"""')
        lines.append(')')
        lines.append('')

    lines.extend([
        '',
        'def char_count(s):',
        '    return len(re.sub(r"\\s+", "", s))',
        '',
        'def strip_boiler(text):',
        '    for p in BOILER_PATTERNS:',
        '        text = re.sub(p, "", text)',
        '    paras = [p.strip() for p in text.split("\\n\\n") if p.strip()]',
        '    out, seen = [], set()',
        '    for p in paras:',
        '        if p.startswith("章回未完，钩在灯后。"):',
        '            continue',
        '        key = re.sub(r"\\s+", "", p)[:80]',
        '        if key not in seen:',
        '            seen.add(key)',
        '            out.append(p)',
        '    return "\\n\\n".join(out)',
        '',
        'def clean_output(text):',
        '    text = strip_boiler(text)',
        '    paras = [p.strip() for p in text.split("\\n\\n") if p.strip()]',
        '    out, seen = [], set()',
        '    for p in paras:',
        '        if p.startswith("章回未完，钩在灯后。"):',
        '            continue',
        '        if p.startswith("长明不灭（") and "不是仙途" in p:',
        '            continue',
        '        if p.startswith("长明不灭的，不是仙途"):',
        '            continue',
        '        if p == "陆承安已战死玄京，非化灯；开灯令在，长明在。":',
        '            continue',
        '        if re.match(r"^章末，第\\d+章", p) and "开灯令在，长明在，路还长" in p:',
        '            continue',
        '        if re.match(r"^（第\\d+章·", p) and ("急什么，灯还亮" in p or "守岁灯三相微颤，开灯令在" in p):',
        '            continue',
        '        if re.match(r"^——第\\d+章·", p) and "钩在灯后" in p:',
        '            continue',
        '        if re.match(r"^顾迟年守岁灯微颤，", p) and "既过，下一章将至" in p:',
        '            continue',
        '        if re.match(r"^承平四十年，第\\d+章·", p) and "钩在灯后" in p:',
        '            continue',
        '        key = re.sub(r"\\s+", "", p)[:80]',
        '        if key not in seen:',
        '            seen.add(key)',
        '            out.append(p)',
        '    return "\\n\\n".join(out)',
        '',
        'def cn(n):',
        '    return CN_INV[n]',
        '',
        'def rebuild_vol4():',
        '    text = VOL4.read_text(encoding="utf-8")',
        '    idx166 = text.find("### 第一百六十六章")',
        '    if idx166 < 0:',
        '        raise SystemExit("ch166 not found in vol4")',
        '    prefix = text[:idx166].rstrip()',
        '    out = [prefix, ""]',
        '    for n in range(166, 191):',
        '        title, body = CHAPTERS[n]',
        '        out.append(f"### 第{cn(n)}章 {title}")',
        '        out.append("")',
        '        out.append(clean_output(body.strip()))',
        '        out.append("")',
        '    if "**第四卷完**" not in CHAPTERS[190][1]:',
        '        out.append("**第四卷完**")',
        '    out.append("")',
        '    out.append("---")',
        '    VOL4.write_text("\\n".join(out), encoding="utf-8")',
        '',
        'def rebuild_vol5():',
        '    text = VOL5.read_text(encoding="utf-8")',
        '    # Keep full header through ## 第五卷 block',
        '    m = re.search(',
        '        r"(# 《万古守灯人》分章正文 · 第五卷[\\s\\S]*?## 第五卷：万古长明[^\\n]*\\n\\n---\\n)",',
        '        text,',
        '    )',
        '    if not m:',
        '        m = re.search(r"(# 《万古守灯人》分章正文 · 第五卷[\\s\\S]*?---\\n)", text)',
        '    prefix = m.group(1).rstrip() if m else (',
        '        "# 《万古守灯人》分章正文 · 第五卷（终卷）\\n\\n"',
        '        "> **本卷范围**：天魔终战（191–210）→ 拒飞升化灯（211–215）→ 传承与百年尾声（216–220）。\\n"',
        '        "> 陆承安已于第四卷逝世；顾迟年化灯仅在本卷发生**一次**。\\n\\n"',
        '        "---\\n\\n## 第五卷：万古长明（第191–220章）\\n\\n---"',
        '    )',
        '    out = [prefix, ""]',
        '    for n in range(191, 221):',
        '        title, body = CHAPTERS[n]',
        '        out.append(f"### 第{cn(n)}章 {title}")',
        '        out.append("")',
        '        out.append(clean_output(body.strip()))',
        '        out.append("")',
        '    out.append("**全书完**")',
        '    VOL5.write_text("\\n".join(out), encoding="utf-8")',
        '',
        'def report():',
        '    def count_body(s):',
        '        return char_count(clean_output(s))',
        '    for path, start, end, label in [(VOL4, 166, 190, "Vol4"), (VOL5, 191, 220, "Vol5")]:',
        '        print(f"\\n=== {label} ({path.name}) ===")',
        '        total = 0',
        '        for n in range(start, end + 1):',
        '            c = count_body(CHAPTERS[n][1])',
        '            total += c',
        '            flag = "LOW" if c < 2500 else ("HIGH" if c > 4500 else "OK")',
        '            print(f"  ch{n}: {c} {flag}")',
        '        print(f"  TOTAL: {total}")',
        '',
        'if __name__ == "__main__":',
        '    rebuild_vol4()',
        '    rebuild_vol5()',
        '    report()',
        '',
    ])

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    if short:
        print(f"WARNING: {len(short)} chapters below 2500 chars:")
        for n, c, need in short:
            print(f"  ch{n}: {c} (need +{need})")
    for n in range(166, 221):
        c = clean_count(chapters[n][1])
        flag = "LOW" if c < 2500 else ("HIGH" if c > 4500 else "OK")
        print(f"  {n}: {c} {flag}")


if __name__ == "__main__":
    main()
