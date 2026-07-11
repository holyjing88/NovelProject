# -*- coding: utf-8 -*-
"""Rebuild clean _gen_chapters.py: ch16-25 + ch26-40 txt + splice."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GEN = ROOT / "_gen_chapters.py"
CH_DIR = ROOT / "_chapters_txt"

TITLES = {
    26: "第二十六章 温言查案", 27: "第二十七章 神谕真相", 28: "第二十八章 豪强夜袭",
    29: "第二十九章 长明灯灭", 30: "第三十章 三十年记忆", 31: "第三十一章 幻影长明",
    32: "第三十二章 忘了落第", 33: "第三十三章 全镇神迹", 34: "第三十四章 霍照临再临",
    35: "第三十五章 赴宗门", 36: "第三十六章 杂役堂", 37: "第三十七章 铁柱醒来",
    38: "第三十八章 姜小满", 39: "第三十九章 迟暮未至", 40: "第四十章 灯还亮着",
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

def main():
    text = GEN.read_text(encoding='utf-8')
    # keep through end of chapter 25 only
    m = re.search(r'^(.*?add\("第二十五章 灯落有冤", """.*?"""\))', text, re.S)
    if not m:
        raise SystemExit('Could not find end of ch25')
    head = m.group(1).rstrip()

    out = [head, '']
    for n in range(26, 41):
        body = (CH_DIR / f'ch{n:02d}.txt').read_text(encoding='utf-8').strip()
        out.append(f'add("{TITLES[n]}", """')
        out.append(body)
        out.append('""")')
        out.append('')

    out.append(SPLICE.strip())
    GEN.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'Rebuilt {GEN} with ch16-40')

if __name__ == '__main__':
    main()
