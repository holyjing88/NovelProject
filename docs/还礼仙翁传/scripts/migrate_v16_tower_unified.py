#!/usr/bin/env python3
"""v16: 塔无分层，万物皆可收存取 — 全局措辞迁移 + ch011-030 塔取放补丁"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PROSE = ROOT / "prose"
DOCS = ROOT

# 塔内分层 → 统一塔内（不误伤叙事「一层声浪」「围三层」等）
TOWER_REPL = [
    (r'缘阁门扉半开', '塔内微亮'),
    (r'缘阁门扉', '塔门'),
    (r'缘阁里', '塔中'),
    (r'缘阁中', '塔中'),
    (r'缘阁微亮', '塔内微亮'),
    (r'缘阁骤亮', '塔内骤亮'),
    (r'缘阁一亮', '塔内一亮'),
    (r'缘阁发烫', '塔内发烫'),
    (r'缘阁无剑', '塔中无剑'),
    (r'缘阁里并无新物', '塔中并无新物'),
    (r'缘阁里一点竹光', '塔中一点竹光'),
    (r'缘阁里竹杖横陈', '塔中竹杖横陈'),
    (r'缘阁', '塔中'),
    (r'符阁一亮', '塔内一亮'),
    (r'符阁', '塔中'),
    (r'资阁里摸出', '塔中摸出'),
    (r'资阁', '塔中'),
    (r'一念出阁', '一念出塔'),
    (r'一念归阁', '一念归塔'),
    (r'没入缘阁', '没入塔中'),
    (r'自缘阁取杖', '自塔中取杖'),
    (r'自缘阁落掌', '自塔中落掌'),
    (r'从缘阁取出', '从塔中取出'),
    (r'在阁里认主', '在塔中认主'),
    (r'回赠已在阁中', '回赠已在塔中'),
    (r'回赠已在缘阁', '回赠已在塔中'),
    (r'已在缘阁', '已在塔中'),
    (r'已在阁中', '已在塔中'),
    (r'一层\*\*缘阁\*\*', '塔内'),
    (r'识海一层\*\*缘阁\*\*', '塔内'),
    (r'识海一层缘阁', '塔内'),
    (r'一层缘阁', '塔内'),
    (r'九层塔影顶天立地', '一座塔影顶天立地'),
    (r'九层鸿蒙色', '鸿蒙色'),
    (r'直到他心念掠过第三层——金铭才浮', '直到他心念掠过塔壁——金铭才浮'),
    (r'实物入\*\*缘阁/资阁\*\*', '实物入塔'),
    (r'先入缘阁，意取即至', '先入塔中，意取即至'),
    (r'缘阁骤亮', '塔内骤亮'),
    (r'万缘塔\*\*符阁\*\*', '万缘塔内符箓格'),
    (r'符阁记塔铭', '塔内记符铭'),
    (r'先入缘阁/符阁/资阁', '先入塔中'),
    (r'缘阁/符阁/资阁', '塔中'),
    (r'缘阁亮', '塔内亮'),
    (r'意取或当场出塔', '意取或当场自塔中出'),
]

# ch011-030 专属塔取放补丁：(文件名, old, new) — old 须唯一或 replace_all
CH11_30_PATCHES = [
    ('ch011-丹堂夜语.md',
     '莫长春从袖中取出一只小匣',
     '莫长春袖空，一念出塔，一只小匣落掌'),
    ('ch011-丹堂夜语.md',
     '他收念',
     '他收念'),
    ('ch012-培元被扣.md',
     '莫长春不辩，只杖点地',
     '莫长春袖空，一念自塔中取杖，杖点地'),
    ('ch012-培元被扣.md',
     '他收念',
     '他收念'),
    ('ch013-执法堂辩.md',
     '莫长春拄杖立堂侧',
     '莫长春袖空，一念出塔，杖落掌，立堂侧'),
    ('ch014-孙福告状.md',
     '莫长春不急着辩',
     '莫长春袖空，杖自塔中落掌，不急着辩'),
    ('ch015-宗主裁断.md',
     '莫长春抚杖',
     '莫长春袖空，一念出塔，杖落膝，抚杖'),
    ('ch016-赤焰来使.md',
     '莫长春拄杖立庭',
     '莫长春袖空，一念自塔中取杖，立庭'),
    ('ch017-长老分裂.md',
     '莫长春不辩',
     '莫长春袖空，杖在塔中，不辩'),
    ('ch018-厉无殇至.md',
     '莫长春拄杖',
     '莫长春袖空，一念出塔，杖落掌'),
    ('ch021-魔少出丑.md',
     '莫长春收杖',
     '莫长春一念归塔，杖没入塔中，袖空'),
    ('ch022-和还是战.md',
     '莫长春拄杖立殿心',
     '莫长春袖空，一念出塔，杖落掌，立殿心'),
    ('ch023-赵之妒火.md',
     '他收念',
     '他收念'),
    ('ch024-小满情报.md',
     '莫长春把册收入袖中隔层',
     '莫长春把册一念归塔，抄本在掌，原本顾小满仍持'),
    ('ch025-卷末集结.md',
     '莫长春杖点灵田',
     '莫长春袖空，一念出塔，杖落掌，点灵田'),
    ('ch026-坊市闲逛.md',
     '莫长春从摊前拈起一张黄符',
     '莫长春袖空，灵石自塔中落指，付账，再一念将买来的黄符收入塔中'),
    ('ch027-第二次妖讯.md',
     '莫长春抚杖',
     '莫长春袖空，一念出塔，杖落膝，抚杖'),
    ('ch028-赵之初见.md',
     '莫长春拄杖',
     '莫长春袖空，一念自塔中取杖'),
    ('ch029-闪回一瞬.md',
     '万缘塔镇识海静',
     '万缘塔镇识海静，万物皆可藏，闪回亦在塔壁旧痕里'),
    ('ch030-卷终夜话.md',
     '莫长春杖横膝',
     '莫长春袖空，一念出塔，杖横膝'),
]

def apply_tower_repl(text: str) -> str:
    for old, new in TOWER_REPL:
        text = re.sub(old, new, text)
    return text

def process_file(path: Path, patches: list) -> bool:
    text = path.read_text(encoding='utf-8')
    orig = text
    text = apply_tower_repl(text)
    for fname, old, new in patches:
        if path.name == fname and old in text:
            text = text.replace(old, new)
    if text != orig:
        path.write_text(text, encoding='utf-8')
        return True
    return False

def process_doc(path: Path) -> bool:
    if not path.suffix == '.md':
        return False
    text = path.read_text(encoding='utf-8')
    orig = text
    text = apply_tower_repl(text)
    if text != orig:
        path.write_text(text, encoding='utf-8')
        return True
    return False

def main():
    changed = []
    # prose ch*.md
    for path in sorted(PROSE.glob('ch*.md')):
        if process_file(path, CH11_30_PATCHES):
            changed.append(f'prose/{path.name}')
    # key docs
    for rel in [
        '13-鸿蒙万缘塔系统.md', '04-修仙系统速查表.md', '02-原创剧情.md',
        'chapters/vol01-寿尽之前.md', 'chapters/EXPANSION-正文上架书写规范.md',
        'chapters/EXPANSION-起点内投策划案.md', 'chapters/AUDIT-全文校验第十五版.md',
        '10-符录系统.md',
    ]:
        p = DOCS / rel
        if p.exists() and process_doc(p):
            changed.append(rel)
    print(f'Updated {len(changed)} files')
    for c in changed:
        print(f'  {c}')

if __name__ == '__main__':
    main()
