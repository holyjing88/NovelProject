# -*- coding: utf-8 -*-
import re
from pathlib import Path

transcript = Path(r'C:\Users\Administrator\.cursor\projects\d-0-games-0000ready-00000LegendOfTheElderCultivator\agent-transcripts\4ea2da5e-bd6e-4b0c-9a57-f63e8f3c55bd\subagents\f3b5ebf3-720e-4c73-9f96-8ca22c248202.jsonl')
out_dir = Path(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs')

text = transcript.read_text(encoding='utf-8')
idx = text.rfind('CHAPTERS = {')
if idx < 0:
    raise SystemExit('CHAPTERS block not found')
block = text[idx:]

for n in range(17, 23):
    pat = rf"{n}: '''(.*?)'''"
    m = re.search(pat, block, re.DOTALL)
    if not m:
        print(f'Ch{n}: FAIL')
        continue
    content = m.group(1).strip() + '\n'
    (out_dir / f'_ch{n}.txt').write_text(content, encoding='utf-8')
    chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    print(f'Ch{n}: {chars}')
