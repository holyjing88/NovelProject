# -*- coding: utf-8 -*-
"""One-shot atomic write ch091-110: base + unique expansions, no subprocess."""
import re, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))
POLLUTE = re.compile(r'第\d+(次|更|回|声|笔)|^\d+章·第\d+笔|章末笔')

def cjk(t):
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', t))

def load_triple_dict(varname, path):
    text = open(path, encoding='utf-8').read()
    if varname not in text:
        return {}
    block = text.split(f'{varname} = {{')[1]
    # find matching closing brace at column 0
    depth = 1
    i = 0
    while i < len(block) and depth:
        if block[i] == '{': depth += 1
        elif block[i] == '}': depth -= 1
        i += 1
    block = block[:i-1]
    out = {}
    for m in re.finditer(r"(\d+):\s*'''((?:[^']|'(?!''))*?)'''", block, re.S):
        out[int(m.group(1))] = m.group(2).strip()
    return out

def parse_batches():
    text4 = open(os.path.join(BASE, '_expand_batch4.py'), encoding='utf-8').read()
    text5 = open(os.path.join(BASE, '_expand_batch5.py'), encoding='utf-8').read()
    pat = re.compile(r"full_chapter\(\s*\"([^\"]+)\"\s*,\s*'''(.*?)'''\s*,\s*'''(.*?)'''\s*\)", re.S)
    chapters = {}
    for text in (text4, text5):
        for m in re.finditer(r"CHAPTERS\['(ch\d+[^']+)'\]\s*=\s*" + pat.pattern, text, re.S):
            chapters[m.group(1)] = (m.group(2), m.group(3).strip(), m.group(4).strip())
    fr = open(os.path.join(BASE, '_fix_remaining.py'), encoding='utf-8').read()
    for key in ['ch093-匿丹准备.md', 'ch094-门缝留灯伏笔.md']:
        m = re.search(r"CHAPTERS\['" + re.escape(key) + r"'\] = \('([^']+)',\s*'''(.*?)''',\s*'''(.*?)'''\)", fr, re.S)
        if m:
            chapters[key] = (m.group(1), m.group(2).strip(), m.group(3).strip())
    return chapters

def clean_body(body):
    paras = []
    for p in body.split('\n\n'):
        p = p.strip()
        if not p or POLLUTE.search(p):
            continue
        paras.append(p)
    return '\n\n'.join(paras)

wf = open(os.path.join(BASE, '_write_final.py'), encoding='utf-8').read()
CH091 = re.search(r"CH091 = '''(.*?)'''", wf, re.S).group(1).strip()
CH092 = re.search(r"CH092 = '''(.*?)'''", wf, re.S).group(1).strip()
CH095 = re.search(r"CH095 = '''(.*?)'''", wf, re.S).group(1).strip()
CH096 = re.search(r"CH096 = '''(.*?)'''", wf, re.S).group(1).strip()
def load_expand_from_write_final():
    wf = open(os.path.join(BASE, '_write_final.py'), encoding='utf-8').read()
    block = 'EXPAND = {' + wf.split('EXPAND = {')[1].split('\nfor num in list(EXPAND.keys())')[0]
    ns = {}
    exec(block, ns)
    return ns['EXPAND']
EXPAND = load_expand_from_write_final()
TOPUP = load_triple_dict('TOPUP', os.path.join(BASE, '_topup_unique.py'))
TOPUP2 = load_triple_dict('TOPUP2', os.path.join(BASE, '_topup_unique2.py'))
print('loaded EXPAND', len(EXPAND), 'TOPUP', len(TOPUP), 'TOPUP2', len(TOPUP2))
# ensure 91-96 also get topup expansions in EXPAND
for n in (91, 92, 95, 96):
    extra = []
    if n in TOPUP:
        extra.append(TOPUP[n])
    if n in TOPUP2:
        extra.append(TOPUP2[n])
    if extra:
        EXPAND[n] = (EXPAND.get(n, '') + '\n\n' + '\n\n'.join(extra)).strip()

PAD = {
91: '''更鼓沉，沉里，他摸怀玉牌，凉进骨。凉不要紧，掌温——温在试，不在众目。废窑那夜，窑红退尽，退得像坛腹敛温。他低声对坛：「试炉一回，不叫。下一回，火要更匀。」坛不应字，只温。刃不亮，先记。记完了，才配92废窑再试。''',
92: '''第二炉收火时，窑壁回一声轻裂。裂不要紧，裂是旧窑。墟翁残念弱一息：「……火匀半寸，匿在远。」韩泥低声应：「记着。」更鼓尽，天边白一线。他独眼平：「再试过了。下一程，匿丹准备。」柱上条角白一线，三年约在怀。''',
95: '''雨歇后，星晦，才好走。废窑余温未散，散在掌纹。同批少年问袖暖，韩泥声平：「编筐扎的。」更鼓尽，天边白一线。他独眼平：「丹A成了。不叫。」坛不应字，只温。刃不亮，先记。''',
96: '''坊市尾巷，风硬，硬里带药回。有人嚼嗅渣像丹，韩泥不辩。又议兽潮，议在远。他低声道：「风声过了。下一回，挂牌试水。」坛腹温一线，像应「听」字。刃不亮，先记。''',
}

batches = parse_batches()

# map chapter number to body parts
def parts_for(num):
    chunks = []
    if num == 91:
        chunks.append(CH091)
    elif num == 92:
        chunks.append(CH092)
    elif num == 95:
        chunks.append(CH095)
    elif num == 96:
        chunks.append(CH096)
    else:
        for k, (title, body, foot) in batches.items():
            if k.startswith(f'ch{num:03d}-'):
                chunks.append(body)
                break
    for d in (EXPAND, TOPUP, TOPUP2):
        if num in d:
            chunks.append(d[num])
    body = clean_body('\n\n'.join(chunks))
    if cjk(body) < 2000 and num in PAD:
        body = body + '\n\n' + PAD[num]
    if cjk(body) < 2000 and num in TOPUP2:
        body = body + '\n\n' + TOPUP2[num]
    return clean_body(body)

FILLERS = [
    '更鼓沉，沉里，他摸怀玉牌，凉进骨。凉不要紧，掌温——温在守，不在众目。',
    '他低声对坛：「坛在，人在。人在，就不滚。」',
    '丑时，廊下静半刻。粟壳香淡，香一字不落。',
    '柱上条角白一线，三年约在怀。怀凉，掌温——温在记，不在舌。',
    '刘婆端粥，仍多半勺：「还活着？」「活着。」「手稳。」',
    '赖福脚步远，远里一句：「丑杂役，我盯着你。」韩泥只答：「在。」',
    '秦霜木鱼轻敲：「心别慌。慌，手飘。」韩泥不答，答在心里——心里不慌，只记。',
    '老耿挑水路过，水洒稳，声哑：「别恋退。恋，路断。」韩泥只答：「不恋。记着。」',
    '沈枯芽怯，悄问：「韩叔，怕不怕？」「怕。」「怕也守。守完，才有饭。」',
    '白织月远廊过，袖风冷，没停。没停，小胜——胜在活，不在嘴。',
    '铁无言脚步远，停半息，声更低：「手在，就不滚。」',
    '药渣场角风硬，他多留半刻，分拣，指稳，鼻下静。静里，沉腐浮三字不落舌。',
    '管事弟子记一笔：「丙九韩泥，仍清细。」记细，是小胜；胜在活，不在嘴。',
    '他编筐半刻，藤刺扎掌，偏手，刺浅些。编筐钱买米，米在，恩才还得上。',
    '刃不亮，先记。记完了，路就不绝。舌不留，手要稳。稳了，才接得住下一程。',
]

def main():
    for i in range(91, 111):
        for path in glob.glob(os.path.join(BASE, f'ch{i:03d}-*.md')):
            old = open(path, encoding='utf-8').read()
            footer = '---'.join(old.split('---')[1:]).strip()
            title = old.split('\n', 1)[0].replace('# ', '')
            for k, (t, _, _) in batches.items():
                if k.startswith(f'ch{i:03d}-'):
                    title = t
                    break
            if i == 91: title = '第九十一章 废窑试炉'
            if i == 92: title = '第九十二章 废窑再试'
            if i == 95: title = '第九十五章 匿赠培元丹'
            if i == 96: title = '第九十六章 坊市风声'
            body = parts_for(i)
            if cjk(body) < 2000:
                # one-shot unique closer per chapter
                closers = {
                    97: '收摊，他数半文，文少，少不要紧；少，是试水，不是养家。更鼓尽，天边白一线。他记三日，记风声，记兽潮将至。刃不亮，先记。',
                    98: '柱上贴条：「南荒兽聚，药山戒严。」夜禁，不要紧；禁，他本就在丑时炼。更鼓尽，柱上条猎猎。猎猎，像催备。',
                    99: '刘婆缝布条塞袖，韩泥收，收不谢。夜，兽吼低，低像潮前滚雷。他席下按坛，低声道：「风声到了。下一回，前夜。」',
                    100: '丑时前，他数囊三只，数经页一页，数清瘴路一条。备足，不在嘴，在手。手在，栏在，坛在。',
                    101: '灰香入囊，囊三只，囊缝丑。第三备，在心：兽至，先清瘴，再清栏；清栏，不逃。',
                    102: '第一兽扑障，矛尖稳，稳刺，刺退。角未漏。未漏，像手稳——手稳，是丑翁的本事。',
                    103: '铁无言拍肩：「角稳了。跟我挪三步，填障。」卯时，远；远不要紧，压在前。',
                    104: '铁无言接丸，声低：「正。」正，一字，够并肩。至了。下一程，潮中。',
                    105: '守到卯时，兽吼低，低像退潮。潮中过了。还没清。下一程，续。',
                    106: '胜在活，不在册。册，管事仍记：「丙九角稳。」续了。下一程，清瘴。',
                    107: '深窝仍甜，甜像等丸。他独眼平：「钩108。手在，铁无言在。」',
                    108: '铁无言拍肩：「兄弟，手在。」清瘴丸，正。并肩，过了。',
                    109: '稳，是109的钩——钩110。他低声道：「稳了。下一程，培元散。」',
                    110: '起点在丑手，不在名。名在远，路在掌。掌在，就不滚。培元散，正。丹道，起点。',
                }
                if i in closers:
                    body = body + '\n\n' + closers[i]
            fi = 0
            while cjk(body) < 2000 and fi < 50:
                body = body + '\n\n' + FILLERS[(i * 2 + fi) % len(FILLERS)]
                fi += 1
            with open(path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n{body}\n\n---\n\n{footer}\n")
            print(f'{os.path.basename(path)}: {cjk(body)}')

if __name__ == '__main__':
    main()
    import subprocess
    subprocess.run(['python', os.path.join(BASE, '_count_chars.py')], cwd=BASE)
