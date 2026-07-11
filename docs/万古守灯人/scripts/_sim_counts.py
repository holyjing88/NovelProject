import re
from _fix_gen_chapters import (
    load_from_expanded_md, clean_body, expansion_pools,
    merged_body_26_40, count, normalize_para,
)

def expand(num, body):
    body = clean_body(body, num)
    pools = expansion_pools(num)
    existing = {normalize_para(p) for p in body.split('\n\n') if p.strip()}
    n = count(body)
    for add in pools:
        k = normalize_para(add)
        if k not in existing:
            body += '\n\n' + add
            existing.add(k)
            n = count(body)
            if n >= 3500:
                break
    return n

for num in range(16, 41):
    if num >= 26:
        body = merged_body_26_40(num)
    else:
        body = load_from_expanded_md()[num][1]
    c = expand(num, body)
    flag = 'OK' if 3500 <= c <= 4500 else ('SHORT' if c < 3500 else 'LONG')
    print(f'ch{num}: {c} [{flag}]')
