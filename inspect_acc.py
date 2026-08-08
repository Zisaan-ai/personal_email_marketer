lines = open(r'xcomic.xyz\assets\sending_accounts.js', encoding='utf-8').readlines()
for i, l in enumerate(lines):
    if 'undefined' in l:
        print(f'{i+1}: {l.strip()}')
