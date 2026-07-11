# -*- coding: utf-8 -*-
from pathlib import Path

VOL2 = Path(__file__).resolve().parents[1] / "chapters" / "vol02-云岚杂役.md"
MARKER = "*塔内验心，记一笔；账在，恩在。*"
INSERT = """

塔外，第六层灯焰忽灭，像有人把云岚后山的星都吹熄了。「完了？」有人低声。陆承安立主持台：「塔规如此，他若死在里面，也算咎由自取。」霍照临五阶灯影一照塔基：「谁动，我杀谁。」程不二报数：「塔内灯温未降，反升半线——他在活，不是盗。」沈青禾在青萝只对长明说：「灯还亮着，我就等。」孙福带十二杂役齐念：「灯还亮着呢。」——**照路余恩**，初显。"""


def main():
    text = VOL2.read_text(encoding="utf-8")
    idx = text.find(MARKER)
    if idx < 0:
        raise SystemExit("marker not found")
    end = idx + len(MARKER)
    rest = text[end:]
    if INSERT.strip() in text:
        print("already inserted")
        return
    # normalize: skip blank lines before ---
    m = rest.lstrip("\r\n")
    if not m.startswith("---"):
        raise SystemExit(f"unexpected after marker: {rest[:40]!r}")
    text = text[:end] + INSERT + "\n\n---" + m[3:]
    VOL2.write_text(text, encoding="utf-8")
    print("ch64 tower-outside scene inserted")


if __name__ == "__main__":
    main()
