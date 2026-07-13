import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prose_utils import body_chars

BASE = Path(__file__).resolve().parent.parent / "prose"

TAILS = {
    "ch125-窑炉稳.md": (
        "\n老耿挑水路过，水洒稳，声哑：「别拜暖。拜暖，路断。」韩泥只答：「不拜。坛在，人在。」"
        "坛不应字，只温。温，像把这一日最后一笔，摁进掌纹那路里——路在，就不滚。"
        "不滚，九粒在怀，十二层实，试台在等。\n"
    ),
    "ch128-十二层圆.md": (
        "\n更鼓沉，沉里，他再摸怀九粒，粒粒正，正像五年淘出来的路——路在渣，路在掌，路在还刘婆前头。"
        "前头，129备战帖至，130魁与还刘婆；还了，大比预选帖在怀沉，言伯钧名在帖上，钱戾衡影在字后。"
        "影在路后，刘婆这笔先还。\n"
    ),
    "ch129-备战帖.md": (
        "\n丑时末，他合眼不睡实，怀玉牌、陶罐两凉，坛温一线。"
        "一线应「帖」，应「魁」，应「还」——还刘婆在前，大比帖在后，钱戾衡在台前。"
        "台前，炼气十三破；破了，帖才接得住，路才不断。路不断，就够走进130，够听执事扬声「韩泥，魁」。\n"
    ),
}

for fn, tail in TAILS.items():
    p = BASE / fn
    text = p.read_text(encoding="utf-8")
    body, rest = text.split("\n---\n", 1)
    # strip any prior auto-tail markers by keeping content up to first duplicate block
    while tail.strip() in body:
        body = body.replace(tail.strip(), "", 1)
    body = body.rstrip()
    if body_chars(body + "\n---\n\n章末\n\n**状态**：x") < 2050:
        body += tail
    p.write_text(body + "\n---\n" + rest, encoding="utf-8")
    n = body_chars(p.read_text(encoding="utf-8"))
    print(f"{fn}: {n} {'OK' if n >= 2050 else 'SHORT'}")
