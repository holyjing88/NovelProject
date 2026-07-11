import ast
try:
    ast.parse(open('_build_long_chapters.py', encoding='utf-8').read())
    print('OK')
except SyntaxError as e:
    print('Error line', e.lineno, e.msg)
    lines = open('_build_long_chapters.py', encoding='utf-8').readlines()
    for i in range(max(0, e.lineno-2), min(len(lines), e.lineno+1)):
        print(f'{i+1}: {lines[i][:120]}...')

lines = open('_build_long_chapters.py', encoding='utf-8').readlines()
for n in [15, 16, 88]:
    line = lines[n]
    t = line.count('"""')
    print(f'line {n+1} triple={t} len={len(line)} end={repr(line[-10:])}')
