lines = open(r'xcomic.xyz\assets\app.js', encoding='utf-8').readlines()
for i, l in enumerate(lines):
    if 'modal' in l.lower() and ('style.display' in l or 'classlist' in l.lower()):
        print(f'{i+1}: {l.strip()}')
