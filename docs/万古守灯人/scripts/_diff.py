with open(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_bulk_expand.py', encoding='utf-8') as f:
    a = ''.join(f.readlines()[9:37])
with open(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_test66.py', encoding='utf-8') as f:
    b = f.read().split('66: """')[1].split('"""}')[0]
print('len a', len(a), 'len b', len(b))
if a != b:
    for i, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            print('diff at', i, repr(ca), ord(ca), repr(cb), ord(cb))
            break
    else:
        print('prefix equal, len diff', len(a)-len(b))
else:
    print('identical')
