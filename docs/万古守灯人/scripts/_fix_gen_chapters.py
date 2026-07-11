# -*- coding: utf-8 -*-
"""Fix _gen_chapters.py: remove padding, dedupe, expand, rebuild from clean sources."""
import re
from pathlib import Path
from _unique_expansions import EXPANSIONS, count
from _ch17_24_exp import EXP17, EXP18, EXP19, EXP20, EXP21, EXP22, EXP23, EXP24
from _make_ch_txt import BASE
from chapter_ext import EXT
from _build_long_chapters import (
    S26, S27, S28, S29, S30, S31, S32, S33, S34,
    S35, S36, S37, S38, S39, S40,
)
from _ch27_40_exp import ALL as EXP_EXTRA
from _gap_fill import GAP

ROOT = Path(__file__).resolve().parent
GEN = ROOT / '_gen_chapters.py'
EXPANDED_MD = ROOT / '_ch16-40-expanded.md'

PAD = '顾迟年袖中守岁灯微温，像把这一段日子，也记进灯油里。他不炫，不冲，只备下一场更大的仗。铁柱在旁闷声问，他便答一句："急什么，灯还亮着呢。"这句话，像账，也像命。'

DROP_PATTERNS = [
    PAD,
    '案破天明，河灯尽灭，镇民似从梦中醒。有人哭，有人拜，有人仍信神谕，被里正喝止。',
    '案破天明，河灯灭，谎破。顾迟年拒牌，只允看长明。沈青禾第三碗姜汤还，温言押余孽，购地链递，回文未知。',
    '"赢一夜，赢一世还早。"',
    '风过林，如梆。万灯大会在前，第一卷走灯节单元，收钩在此，开钩在远。',
    '风如梆，钩在此，开钩在远——霍家线将浮，长明如钉，第一卷走灯节，收。',
]

EXTRA_EXP = {
    17: EXP17, 18: EXP18, 19: EXP19, 20: EXP20,
    21: EXP21, 22: EXP22, 23: EXP23, 24: EXP24,
}

LONG_SCENES = {
    26: S26, 27: S27, 28: S28, 29: S29, 30: S30, 31: S31, 32: S32,
    33: S33, 34: S34, 35: S35, 36: S36, 37: S37, 38: S38, 39: S39, 40: S40,
}

CN_NUM = {
    '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
    '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
    '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29, '三十': 30,
    '三十一': 31, '三十二': 32, '三十三': 33, '三十四': 34, '三十五': 35,
    '三十六': 36, '三十七': 37, '三十八': 38, '三十九': 39, '四十': 40,
}

SPLICE = '''
# ========== write expanded md ==========
from pathlib import Path
EXPANDED = Path(__file__).resolve().parent / "_ch16-40-expanded.md"
with open(EXPANDED, "w", encoding="utf-8") as f:
    for title, body, n in CHAPTERS:
        f.write(f"### {title}\\n\\n{body.strip()}\\n\\n---\\n\\n")

# ========== splice vol1 ==========
VOL1 = Path(__file__).resolve().parent / "../chapters/vol01-青萝灯起.md"
with open(VOL1, "r", encoding="utf-8") as f:
    original = f.read()

head_m = re.search(r"^(.*?)(?=^### 第十六章)", original, re.S | re.M)
if not head_m:
    raise SystemExit("Could not find ### 第十六章 in vol1")
head = head_m.group(1)

footer_m = re.search(r"(\\*\\*第一卷完\\*\\*.*)", original, re.S)
if not footer_m:
    raise SystemExit("Could not find **第一卷完** footer in vol1")
footer = footer_m.group(1)

parts = [head.rstrip(), ""]
for title, body, n in CHAPTERS:
    parts.append(f"### {title}")
    parts.append("")
    parts.append(body.strip())
    parts.append("")
    parts.append("---")
    parts.append("")
parts.append(footer.strip())

with open(VOL1, "w", encoding="utf-8") as f:
    f.write("\\n".join(parts) + "\\n")

print("Chapters defined:", len(CHAPTERS))
for t, _, n in CHAPTERS:
    flag = "OK" if 3500 <= n <= 4500 else ("SHORT" if n < 3500 else "LONG")
    print(f"  {t}: {n} [{flag}]")
print(f"Wrote {EXPANDED}")
print(f"Spliced {VOL1}")
'''


def chapter_num(title):
    m = re.search(r'第([一二三四五六七八九十百]+)章', title)
    return CN_NUM.get(m.group(1)) if m else None


def normalize_para(p):
    return re.sub(r'\s+', '', p)


def clean_body(body, ch_num=None):
    body = body.replace(PAD, '')
    for drop in DROP_PATTERNS:
        if drop != PAD:
            body = body.replace(drop, '')
    paras = [p.strip() for p in re.split(r'\n\s*\n', body) if p.strip()]
    seen = set()
    unique = []
    for p in paras:
        key = normalize_para(p)
        if len(key) < 20:
            continue
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)
    return '\n\n'.join(unique)


def merged_body_26_40(num):
    """Base = BASE + long scenes only; supplemental via expand."""
    paras = list(BASE.get(num, [])) + list(LONG_SCENES[num])
    seen = set()
    unique = []
    for p in paras:
        key = normalize_para(p.strip())
        if len(key) < 20 or key in seen:
            continue
        seen.add(key)
        unique.append(p.strip())
    return '\n\n'.join(unique)


def expansion_pools(ch_num):
    pools = list(EXPANSIONS.get(ch_num, [])) + list(EXTRA_EXP.get(ch_num, []))
    from _more_unique import MORE
    from _final_unique import FINAL
    from _extra_fill import EXTRA as EXTRA_FILL
    from _last_fill import LAST as LAST_FILL
    from _force_fill import FORCE
    if ch_num >= 26:
        pools = (
            list(EXT.get(ch_num, []))
            + list(EXP_EXTRA.get(ch_num, []))
            + list(GAP.get(ch_num, []))
            + pools
            + list(MORE.get(ch_num, []))
            + list(FINAL.get(ch_num, []))
            + list(EXTRA_FILL.get(ch_num, []))
            + list(LAST_FILL.get(ch_num, []))
            + list(FORCE.get(ch_num, []))
        )
    else:
        pools = pools + list(MORE.get(ch_num, []))
    return pools


def expand_chapter(ch_num, body):
    body = clean_body(body, ch_num)
    expansions = expansion_pools(ch_num)
    idx = 0
    n = count(body)
    existing = {normalize_para(p) for p in body.split('\n\n') if p.strip()}
    while n < 3500:
        if idx < len(expansions):
            add = expansions[idx].strip()
            idx += 1
        else:
            break
        key = normalize_para(add)
        if key not in existing:
            body = body + '\n\n' + add
            existing.add(key)
            n = count(body)
    if n < 3500:
        raise SystemExit(f'Chapter {ch_num} still SHORT at {n} after expansions')
    if n > 4500:
        paras = [p.strip() for p in body.split('\n\n') if p.strip()]
        while count('\n\n'.join(paras)) > 4500 and len(paras) > 3:
            paras.pop()
        body = '\n\n'.join(paras)
    return body


def load_from_expanded_md():
    text = EXPANDED_MD.read_text(encoding='utf-8')
    chapters = {}
    for m in re.finditer(r'^### (第.+?章 .+?)\n\n(.*?)(?=\n\n---|\Z)', text, re.S | re.M):
        title = m.group(1)
        body = m.group(2).strip()
        num = chapter_num(title)
        if num:
            chapters[num] = (title, body)
    return chapters


def main():
    md_chapters = load_from_expanded_md()
    old = GEN.read_text(encoding='utf-8') if GEN.exists() else ''
    head = old.split('add("第十六章')[0].rstrip() if 'add("第十六章' in old else '# -*- coding: utf-8 -*-\nimport re\n\nCHAPTERS = []\n\ndef add(title, body):\n    n = len(re.sub(r\'\\s\', \'\', body))\n    CHAPTERS.append((title, body, n))'

    out = [head, '']
    results = []

    for num in range(16, 41):
        if num >= 26:
            title = md_chapters.get(num, (f'第{num}章', ''))[0]
            if num in md_chapters:
                title = md_chapters[num][0]
            else:
                from _build_long_chapters import CHAPTERS as LC
                title = [t for t, _ in LC if chapter_num(t) == num][0]
            body = merged_body_26_40(num)
        else:
            title, body = md_chapters[num]

        fixed = expand_chapter(num, body)
        n = count(fixed)
        results.append((title, n))
        out.append(f'add("{title}", """')
        out.append(fixed)
        out.append('""")')
        out.append('')

    out.append(SPLICE.strip())
    GEN.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'Fixed {GEN}')
    for title, n in results:
        flag = 'OK' if 3500 <= n <= 4500 else ('SHORT' if n < 3500 else 'LONG')
        print(f'  {title}: {n} [{flag}]')


if __name__ == '__main__':
    main()
