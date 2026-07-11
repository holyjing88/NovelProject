import re
from pathlib import Path

P = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_vol1_ch1_15_full.md")
s = P.read_text(encoding="utf-8")

heads = list(re.finditer(r"^###\s+第([一二三四五六七八九十]+)章\s+(.+)$", s, re.M))
parts = []
for i, m in enumerate(heads):
    st = m.start()
    ed = heads[i + 1].start() if i + 1 < len(heads) else len(s)
    parts.append(s[st:ed])


def drop_last_round(chunk: str, stage: str) -> str:
    pat = re.compile(
        rf"\n{re.escape(stage)}里风声一阵紧一阵，.*?像在旧账本上重重压下一个朱点。\n\n",
        re.S,
    )
    matches = list(pat.finditer(chunk))
    if not matches:
        return chunk
    m = matches[-1]
    return chunk[:m.start()] + "\n" + chunk[m.end():]


# 第9章
parts[8] = drop_last_round(parts[8], "外门广场")
# 第12章
parts[11] = drop_last_round(parts[11], "迷障幻境")

P.write_text("".join(parts), encoding="utf-8")

