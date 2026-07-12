with open('frontend/assets/app.js', encoding='utf-8') as f:
    text = f.read()

res = []
for i, line in enumerate(text.splitlines()):
    if 'type="text"' in line and 'id="prop-' in line:
        if 'src' in line or 'img' in line or 'logo' in line:
            res.append(f'{i}: {line.strip()}')

with open('find_inputs.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(res))
