# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "prose" / "ch043-盯秤.md"
raw = p.read_text(encoding="utf-8")
marker = "他低声道：「三两实粮落袋，落袋才真。真了，明日仍盯。仍盯，饭才稳第二日。」"
idx = raw.find(marker)
if idx < 0:
    raise SystemExit("marker not found")
head = raw[: idx + len(marker)]
new_end = """

管事盯秤，三两落袋。掌心不抖——抖在袖里，秤盘实了，袖里才稳。赖福虚了，虚不是终；终在正测辨香，在还叶丫头那碗烫。秤稳，仇记着；记着，才配等正测末排仍到。

坛沿温一线，温应「实」字，不应骂。实字丑，丑翁专精——专精在忍，专精在记，专精在等瓮醒。

---

章末

（对照 `05` §克扣升级 · 管事当众盯秤 · **v28精修** · **v45爆款10** · **v47爆款10**）

**状态**：大境·凡人 · 资质·丑骨末席（伪灵根） · 鸿蒙九劫瓮·眠（瓮温加剧） · 宗门·丙九杂役 · 漏舍凡舍
"""
p.write_text(head + new_end, encoding="utf-8")
print("fixed ch043")
