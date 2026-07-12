with open('frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'inst-subject' in l:
        print(f'{i}: {l.strip()[:100]}')
