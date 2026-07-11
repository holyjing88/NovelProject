import re
with open(r'd:\0_games\0000ready\00000LegendOfTheElderCultivator\docs\../chapters/vol02-云岚杂役.md', encoding='utf-8') as f:
    c = f.read()
cn = {66:'六十六',67:'六十七',68:'六十八',69:'六十九',70:'七十',71:'七十一',72:'七十二',73:'七十三',74:'七十四',75:'七十五',76:'七十六',77:'七十七',78:'七十八',79:'七十九',80:'八十',81:'八十一',82:'八十二',83:'八十三',84:'八十四',85:'八十五',86:'八十六',87:'八十七',88:'八十八',89:'八十九',90:'九十'}
for num in range(66, 91):
    m = re.search(rf'### 第{cn[num]}章[^\n]*\n\n(.*?)(?=\n\n---\n\n### 第|\n\n\*\*第二卷完\*\*)', c, re.S)
    if m:
        body = m.group(1)
        n = len(re.sub(r'[\s\*#\-]','',body))
        status = 'OK' if 2500 <= n <= 4500 else ('SHORT' if n < 2500 else 'LONG')
        print(f'Ch{num}: {n} {status}')
    else:
        print(f'Ch{num}: MISSING')
filler = '围观弟子议论纷纷，声浪一层盖过一层'
print('filler count', c.count(filler))
print('第二卷完 count', c.count('**第二卷完**'))
