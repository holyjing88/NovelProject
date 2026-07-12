#!/usr/bin/env python3
"""一体化流水线：清理 → 加厚 → 再清理 → 补足 2000。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    py = sys.executable
    steps = [
        ("cleanup_prose.py", "清理 orphan/footer"),
        ("thicken_to_2000.py", "加厚"),
        ("cleanup_prose.py", "再清理模板段"),
        ("force_topup.py", "补足 2000"),
    ]
    for script, label in steps:
        print(f"\n=== {label} ===")
        subprocess.run([py, str(ROOT / script)], check=True)


if __name__ == "__main__":
    main()
