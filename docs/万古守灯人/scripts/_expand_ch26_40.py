# -*- coding: utf-8 -*-
"""Build expanded ch26-40 into _gen_chapters.py with splice logic."""
import re
from pathlib import Path

ROOT = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs")
GEN = ROOT / "_gen_chapters.py"
VOL1 = ROOT / "../chapters/vol01-青萝灯起.md"
EXPANDED = ROOT / "_ch16-40-expanded.md"

def count(body):
    return len(re.sub(r'\s', '', body))

# Import chapter bodies from separate module (will be rewritten with full length)
from _ch26_40_bodies import ALL as CH26_40

def build_gen_tail():
    lines = ['\n']
    for title, body in CH26_40:
        # escape triple quotes in body
        safe = body.replace('"""', '\\"\\"\\"')
        lines.append(f'add("{title}", """')
        lines.append(safe.strip())
        lines.append('""")\n')
    lines.append('''
# ========== write expanded md ==========
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

footer_m = re.search(r"(\*\*第一卷完\*\*.*)", original, re.S)
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
''')
    return ''.join(lines)

if __name__ == "__main__":
    for title, body in CH26_40:
        n = count(body)
        print(f"{title}: {n}")
