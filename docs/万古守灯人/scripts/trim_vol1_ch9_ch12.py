import re
from pathlib import Path

P = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_vol1_ch1_15_full.md")
S = P.read_text(encoding="utf-8")

heads = list(re.finditer(r"^###\s+第([一二三四五六七八九十]+)章\s+(.+)$", S, re.M))
chunks = []
for i, m in enumerate(heads):
    st = m.start()
    ed = heads[i + 1].start() if i + 1 < len(heads) else len(S)
    chunks.append(S[st:ed])

fallback = """
顾迟年把掌心贴在守岁灯上，不急着催火，只把那句口头禅又念了一遍：“急什么，灯还亮着呢。”
这一句落在别人耳里像慢，落在他心里却是刹车。人一旦乱，就会忘了前后账；账一断，路就断。
他再把眼前局势拆开：谁在明处叫嚣，谁在暗处观望，谁会在关键时刻倒向哪边。凡人式算计从来不是阴狠，而是把每一步都踩在实处。
周围人看他沉默，只当他老了怯了；却不知这老书吏每一次沉默，都在给下一次出手攒势。
"""


def count_cjk(text: str) -> int:
    return len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", text))


for idx in (9, 12):
    i = idx - 1
    while count_cjk(chunks[i]) > 4450 and fallback in chunks[i]:
        pos = chunks[i].rfind(fallback)
        chunks[i] = chunks[i][:pos] + chunks[i][pos + len(fallback):]

P.write_text("".join(chunks), encoding="utf-8")

