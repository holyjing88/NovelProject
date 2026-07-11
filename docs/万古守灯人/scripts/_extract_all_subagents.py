# -*- coding: utf-8 -*-
"""Extract all subagent chapters and fix titles."""
import re
from pathlib import Path

BASE = Path(r'C:\Users\Administrator\.cursor\projects\d-0-games-0000ready-00000LegendOfTheElderCultivator\agent-transcripts\4ea2da5e-bd6e-4b0c-9a57-f63e8f3c55bd\subagents')
OUT = Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs')

TITLES = {
    17: '赵家逼婚', 18: '烛火照账', 19: '里正翻案', 20: '废丹渣', 21: '炼灯初成', 22: '程不二',
    23: '走灯节前', 24: '百盏水灯', 25: '灯落有冤', 26: '温言查案', 27: '神谕真相', 28: '豪强夜袭（铺垫）',
    29: '长明灯灭', 30: '三十年记忆', 31: '幻影长明', 32: '忘了落第', 33: '全镇神迹', 34: '霍照临再临',
    35: '赴宗门', 36: '杂役堂', 37: '铁柱醒来', 38: '姜小满', 39: '迟暮未至', 40: '灯还亮着（第一卷终）',
}
CN = {17:'十七',18:'十八',19:'十九',20:'二十',21:'二十一',22:'二十二',23:'二十三',24:'二十四',25:'二十五',
      26:'二十六',27:'二十七',28:'二十八',29:'二十九',30:'三十',31:'三十一',32:'三十二',33:'三十三',34:'三十四',
      35:'三十五',36:'三十六',37:'三十七',38:'三十八',39:'三十九',40:'四十'}

transcripts = list(BASE.glob('*.jsonl'))

def extract_all():
    found = {}
    for tp in transcripts:
        text = tp.read_text(encoding='utf-8')
        idx = text.rfind('CHAPTERS = {')
        if idx < 0:
            continue
        block = text[idx:]
        for n in range(17, 41):
            if n in found:
                continue
            pat = rf"{n}: '''(.*?)'''"
            m = re.search(pat, block, re.DOTALL)
            if m:
                found[n] = m.group(1).strip()
    return found

def normalize(n, body):
    title = TITLES[n]
    header = f'### 第{CN[n]}章 {title}'
    # strip old headers
    body = re.sub(r'^#+\s*第.+?\n', '', body)
    body = re.sub(r'^第.+?回.+?\n+', '', body)
    body = re.sub(r'^诗曰：.*?(?=\n\n)', '', body, flags=re.DOTALL)
    body = body.strip()
    # continuity fixes
    body = body.replace('长明镇', '青萝镇')
    body = body.replace('照影宗', '云岚宗')
    return header + '\n\n' + body + '\n'

def main():
    found = extract_all()
    for n in sorted(found):
        content = normalize(n, found[n])
        (OUT / f'_ch{n}.txt').write_text(content, encoding='utf-8')
        chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        print(f'Ch{n:02d}: {chars} [{ "OK" if chars>=2500 else "LOW"}]')
    print(f'Extracted {len(found)} chapters')

if __name__ == '__main__':
    main()
