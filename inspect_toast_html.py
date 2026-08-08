lines = open(r'xcomic.xyz\index.html', encoding='utf-8').readlines()
for i, l in enumerate(lines):
    if 'toast' in l.lower():
        print(f'{i+1}: {l.strip()}')
