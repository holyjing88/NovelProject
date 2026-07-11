with open(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\_bulk_expand.py', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(8, 38):
    line = lines[i].rstrip('\n')
    if line.endswith('\\'):
        print('backslash end', i+1, repr(line))
    if '\x00' in line:
        print('null', i+1)
    # check for weird quotes
    for j, c in enumerate(line):
        if ord(c) in (0x201c, 0x201d, 0xff02):
            print('fancy quote', i+1, j, hex(ord(c)))
