import sys
sys.stdout.reconfigure(encoding='utf-8')

lines = open(r'xcomic.xyz\index.html', encoding='utf-8').readlines()
for i, l in enumerate(lines):
    if 'SUPPORT' in l and '=' in l and not 'onclick' in l and not 'class' in l:
        print(f'{i+1}: {l.strip()}')
