with open(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_bulk_expand.py', encoding='utf-8') as f:
    lines = f.readlines()
chunk = ''.join(lines[9:37])  # content only
for i, c in enumerate(chunk):
    if c == '"' and chunk[i:i+3] != '"""':
        print('ascii quote at', i, repr(chunk[max(0,i-10):i+10]))
print('done, len', len(chunk))
