import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from prose_utils import body_chars
base = os.path.join(os.path.dirname(__file__), "..", "prose")
for i in range(111, 130):
    fn = sorted([f for f in os.listdir(base) if f.startswith("ch%03d-" % i)])[0]
    c = body_chars(open(os.path.join(base, fn), encoding="utf-8").read())
    print(i, c, "OK" if c >= 2050 else "SHORT")
