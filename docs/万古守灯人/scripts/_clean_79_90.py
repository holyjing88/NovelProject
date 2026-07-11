# -*- coding: utf-8 -*-
import re
from pathlib import Path

path = Path(__file__).parent / "_chapters_79_90_new.py"
ns = {}
exec(path.read_text(encoding="utf-8"), ns)
CHAPTERS = ns["CHAPTERS"]

# Insert breaks before common duplicate-stitch points
STITCH = [
    "拜师礼后第三日", "云照又做了一件破例", "陆承安囚车过广场时", "云照失嗅后第一次",
    "年终联席会上", "裴无妄没入雪后", "一周过去，药房外", "血月当空那一战",
    "陆承安党羽开侧门", "次晨，顾迟年就按册",
]

def clean_chapter(text):
    text = text.replace("守灯山", "云岚宗")
    for s in STITCH:
        text = text.replace(s, "\n\n" + s)
    # normalize breaks
    text = re.sub(r"\n{3,}", "\n\n", text)
    paras = [p.strip() for p in re.split(r"\n\n+", text.strip()) if p.strip()]
    seen = set()
    out = []
    for p in paras:
        key = re.sub(r"[\s\*]", "", p)
        if len(key) < 8:  # skip tiny fragments
            continue
        if key not in seen:
            seen.add(key)
            out.append(p)
    return "\n\n".join(out)

def count_chars(text):
    return len(re.sub(r"[\s\*#\-]", "", text))

for i in range(79, 91):
    CHAPTERS[i] = clean_chapter(CHAPTERS[i])

lines = ['# -*- coding: utf-8 -*-', '"""Expanded chapters 79-90 for Volume 2 (body only, no headers)."""', '', 'CHAPTERS = {']
for i in range(79, 91):
    lines.append(f'    {i}: """{CHAPTERS[i]}""",')
lines.append('}')
lines.append('')
lines.append('if __name__ == "__main__":')
lines.append('    import re')
lines.append('    def count_chars(text):')
lines.append('        return len(re.sub(r"[\\s\\*#\\-]", "", text))')
lines.append('    print("Character counts (body only):")')
lines.append('    for i in range(79, 91):')
lines.append('        n = count_chars(CHAPTERS[i])')
lines.append('        flag = "OK" if 2500 <= n <= 4500 else ("LOW" if n < 2500 else "HIGH")')
lines.append('        print(f"  Ch{i}: {n} chars [{flag}]")')
lines.append('    total = sum(count_chars(CHAPTERS[i]) for i in range(79, 91))')
lines.append('    print(f"  Total 79-90: {total} chars")')
path.write_text('\n'.join(lines), encoding='utf-8')

for i in range(79, 91):
    n = count_chars(CHAPTERS[i])
    flag = "OK" if 2500 <= n <= 4500 else ("LOW" if n < 2500 else "HIGH")
    print(f"  Ch{i}: {n} chars [{flag}]")
