lines = open(r'xcomic.xyz\assets\app.js', encoding='utf-8').readlines()
for i, l in enumerate(lines):
    if 'addEventListener' in l and 'click' in l:
        print(f'{i+1}: {l.strip()}')
