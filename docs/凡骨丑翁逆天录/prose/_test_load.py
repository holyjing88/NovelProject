import re, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _atomic_write_all import EXPAND, TOPUP, TOPUP2, parts_for, cjk
print('EXPAND', len(EXPAND), sorted(EXPAND))
print('TOPUP', len(TOPUP))
print('TOPUP2', len(TOPUP2))
for n in [91,97,110]:
    print(n, cjk(parts_for(n)))
