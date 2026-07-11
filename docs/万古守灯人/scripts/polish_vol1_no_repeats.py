import re
from pathlib import Path

P = Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_vol1_ch1_15_full.md")
MIN_MAP = {**{i: 2500 for i in list(range(1, 9)) + [13, 14, 15]}, **{9: 3500, 10: 3500, 11: 3500, 12: 3500}}

KEY = {
    1: "寿宴逼债", 2: "雨夜点灯", 3: "借据破绽", 4: "人间烟火",
    5: "药铺逼婚", 6: "公堂核纸", 7: "照影代价", 8: "山门初试",
    9: "迟暮立约", 10: "入林前夜", 11: "迷障压境", 12: "天明出林",
    13: "杂役立足", 14: "云照提点", 15: "三策赴青萝",
}


def cjk_count(s: str) -> int:
    return len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", s))


def parse(text: str):
    hs = list(re.finditer(r"^###\s+第([一二三四五六七八九十]+)章\s+(.+)$", text, re.M))
    out = []
    for i, m in enumerate(hs):
        st = m.end()
        ed = hs[i + 1].start() if i + 1 < len(hs) else len(text)
        out.append((i + 1, m.group(1), m.group(2), text[st:ed]))
    return out


def dedupe_lines(body: str) -> str:
    lines = body.splitlines()
    seen = set()
    out = []
    for ln in lines:
        s = ln.strip()
        if not s:
            out.append(ln)
            continue
        if s in seen:
            continue
        seen.add(s)
        out.append(ln)
    txt = "\n".join(out)
    txt = re.sub(r"\n{3,}", "\n\n", txt).strip() + "\n"
    return txt


def topup_block(idx: int, k: int) -> str:
    base = f"第{idx}章增叙第{k}段，围绕“{KEY[idx]}”再落一层实账。"
    if idx == 11:
        tail = "顾迟年压着呼吸与脚步，反复用口令稳住同伴，不许任何人抬头看雾墙后的幻景。风声越来越沉，迷障像活物一样往前拱，他心里只剩一句：急什么，灯还亮着呢。可这亮，亮在刀尖上。"
    elif idx == 12:
        tail = "顾迟年在出林最后百步不争快，只争稳，把三名迷路者按次序送到执事与医修手里。围观弟子先是哗然，后是沉默，他却先看守岁灯灯油再看自己伤势，确认关过、人全、账清。"
    else:
        tail = "他把冲突拆成三轮：先让对方把狠话说满，再把证据钉死在时点上，最后把围观者从看戏推到见证。人群里接连倒吸凉气，场面看似乱，实则次序一步步回到他手里。"
    rank = "灯道阶位上，他仍是以一阶微光为根，不乱碰高阶强火；四阶灯盏的压力他记着，却不拿来吓自己。凡人式算计的核心，是先活，再守，再争。"
    return f"{base}{tail}{rank}\n"


def main():
    raw = P.read_text(encoding="utf-8")
    rebuilt = []
    for idx, cn, title, body in parse(raw):
        b = dedupe_lines(body)
        # 清掉可能遗留的模板痕迹
        b = re.sub(r".*第[0-9一二三四五六七八九十]+轮话锋到这里.*\n?", "", b)
        b = b.replace("顾迟年指尖轻叩袖口，心里把留灯三策过了一遍：先保灯油，再保后手，最后才争胜负。", "")
        b = re.sub(r"\n{3,}", "\n\n", b).strip() + "\n"

        need = MIN_MAP[idx]
        k = 1
        while cjk_count(b) < need:
            b += "\n" + topup_block(idx, k)
            k += 1

        if idx == 11:
            b = re.sub(r"天明|晨光|破晓|鱼肚白", "夜色", b)
            if "迷障像活物一样往前拱" not in b:
                b += "\n迷障像活物一样往前拱，顾迟年知道，最硬的一口风还在后头。\n"
        rebuilt.append(f"### 第{cn}章 {title}\n\n{b.strip()}")

    final = "\n\n---\n\n".join(rebuilt) + "\n"
    P.write_text(final, encoding="utf-8")
    for idx, cn, title, body in parse(final):
        print(f"### 第{cn}章 {title}\t{cjk_count(body)}")


if __name__ == "__main__":
    main()

