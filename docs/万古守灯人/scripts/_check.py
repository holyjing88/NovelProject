with open(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_bulk_expand.py', encoding='utf-8') as f:
    lines = f.readlines()
chunk = ''.join(lines[8:38])
print('triple quote count', chunk.count('"""'))
idx = 0
while True:
    i = chunk.find('"""', idx)
    if i == -1: break
    print('at', i, repr(chunk[max(0,i-20):i+25]))
    idx = i + 3
