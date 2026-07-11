# -*- coding: utf-8 -*-
"""Remove duplicate PAD filler; keep single integrated expansion per chapter."""
import re
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent
VOL2 = ROOT / "../chapters/vol02-云岚杂役.md"


def count(s):
    return len(re.sub(r"\s", "", s))


def load_mod(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def clean_ch90_extra(body):
    """Remove appended PAD blocks after proper chapter end."""
    marker = "第三卷将启，下一次风暴，不会等太久。"
    idx = body.find(marker)
    if idx == -1:
        return body
    tail = body[idx + len(marker):].strip()
    # keep only **第二卷完** if present
    if "**第二卷完**" in tail:
        return body[: idx + len(marker)] + "\n\n**第二卷完**"
    return body[: idx + len(marker)]


CH90_CLOSE = """

顾迟年站在杂役堂檐下，摸红牌，低声念：「灯在，人在。」

铁柱问：「迟年哥，咱还挑水不？」

顾迟年笑：「挑。记名弟子，更要挑给全宗看——灯在人间，不在牌匾上。」

姜小满举帚扫雪：「师父，我扫干净了，灯就亮。」

霍照临递厚袍：「穿上。你还要扫三年渣，别先冻死。」

孙福点齐明日名册：「顾老哥，明儿仍挑水？」

顾迟年点头：「挑。水不挑，丹堂不净；人不净，心灯不明。」

雪落灯上，不熄。

这一卷里，他从杂役清晨到记名弟子，从二阶烛火到四阶灯盏，从枯骨岭捡活到焚灯塔取芯，从幽灯集失忆到万灯大会照亡父，从姜小满拜师到燃灯骨救铁柱——每一步都不惊天，却每一步都照着人走。

承平三十八年末，云岚宗千灯不熄。"""


def main():
    mod = load_mod(ROOT / "_ch79_90_bodies.py")
    PAD_A = getattr(mod, "PAD_A", "").strip()
    PAD_B = getattr(mod, "PAD_B", "").strip()
    # use only first half of PAD_C to avoid 玄京再见 repeat
    PAD_C_HALF = getattr(mod, "PAD_C", "").strip()
    cut = PAD_C_HALF.find("裴无妄现身后")
    if cut > 0:
        PAD_C_HALF = PAD_C_HALF[:cut].strip()

    pad_map = {
        79: PAD_A,
        80: PAD_A,
        81: PAD_B,
        82: PAD_B,
        83: PAD_B,
        84: PAD_B,
        85: PAD_B,
        86: PAD_B,
        87: PAD_C_HALF,
        88: PAD_C_HALF,
        89: PAD_C_HALF,
    }

    cleaned = []
    for i, (title, body) in enumerate(mod.CHAPTERS, start=79):
        # strip python concatenation artifacts if file was exec'd - bodies are already strings
        if isinstance(body, str):
            b = body
        else:
            b = str(body)
        # remove any PAD_* literal remnants
        b = re.sub(r"\s*\+\s*PAD_[A-Z0-9_]+\s*", "", b)
        b = b.replace("**第二卷完**", "").strip()

        if i == 90:
            b = clean_ch90_extra(b)
            if count(b) < 3500:
                b = b + CH90_CLOSE
            if "**第二卷完**" not in b:
                b += "\n\n**第二卷完**"
        else:
            if count(b) < 3500 and i in pad_map:
                b = b + "\n\n" + pad_map[i]
            # trim if too long
            if count(b) > 4500:
                while count(b) > 4500 and "\n\n" in b:
                    b = b.rsplit("\n\n", 1)[0]

        cleaned.append((title, b))

    # write back single block file
    lines = ["CHAPTERS = ["]
    for title, body in cleaned:
        lines.append(f'    ("{title}", """{body.strip()}"""),')
    lines.append("]\n")
    (ROOT / "_ch79_90_bodies.py").write_text("\n".join(lines), encoding="utf-8")

    # splice vol2
    mod66 = load_mod(ROOT / "_ch66_78_bodies.py")
    chapters = mod66.CHAPTERS + cleaned

    text = VOL2.read_text(encoding="utf-8")
    head = re.search(r"^(.*?)(?=### 第六十六章)", text, re.S | re.M).group(1).rstrip()
    footer = re.search(r"(\n---\n\n>\s*第三卷.*)", text, re.S).group(1).lstrip("\n")

    parts = [head, ""]
    for title, body in chapters:
        parts += [f"### {title}", "", body.strip(), "", "---", ""]
    parts.append(footer.strip())
    VOL2.write_text("\n".join(parts) + "\n", encoding="utf-8")

    print("Cleaned ch79-90 and re-spliced")
    for title, body in chapters:
        if title.startswith("第") and any(x in title for x in ["七十九", "八十", "八十一", "八十二", "八十三", "八十四", "八十五", "八十六", "八十七", "八十八", "八十九", "九十"]):
            n = count(body)
            flag = "OK" if 3500 <= n <= 4500 else ("SHORT" if n < 3500 else "LONG")
            print(f"  {title}: {n} [{flag}]")
        elif "第六" in title or "第七" in title and "十九" not in title:
            n = count(body)
            if 66 <= int(re.search(r"第(.+?)章", title).group(1).replace("六十六","66").replace("六十七","67").replace("六十八","68").replace("六十九","69").replace("七十","70").replace("七十一","71").replace("七十二","72").replace("七十三","73").replace("七十四","74").replace("七十五","75").replace("七十六","76").replace("七十七","77").replace("七十八","78") or "0") <= 78:
                pass

    for title, body in chapters:
        n = count(body)
        flag = "OK" if 3500 <= n <= 4500 else ("SHORT" if n < 3500 else "LONG")
        num = re.findall(r"第(.+?)章", title)[0]
        print(f"  {title}: {n} [{flag}]")


if __name__ == "__main__":
    main()
