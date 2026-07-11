# -*- coding: utf-8 -*-
import re
import importlib.util
from pathlib import Path

def load(path):
    spec = importlib.util.spec_from_file_location("m", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.CHAPTERS

def count(body):
    return len(re.sub(r"\s", "", body))

for path in [
    Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\vol3_ch116_140_content.py"),
    Path(r"d:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\vol3_ch131_140_content.py"),
]:
    chapters = load(path)
    total = 0
    print(path.name)
    for k in sorted(chapters):
        title, body = chapters[k]
        n = count(body)
        total += n
        ok = "OK" if 2500 <= n <= 4000 else "WARN"
        print(f"  {k} {title}: {n} [{ok}]")
    print(f"  subtotal: {total}\n")
