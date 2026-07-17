with open('xcomic.xyz/assets/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = "        visibleLines.forEach((line, index) => {\n\n            const parts = line.split(',').map(p => p.trim());\n\n            const email = parts[0] || '';\n\n            const name = parts[1] || 'Unknown';\n\n            const company = parts[2] || '';"

new_code = '''        visibleLines.forEach((line, index) => {
            let email = line.split(',')[0].trim();
            email = email.replace(/^["']|["']$/g, '');
            const name = 'Unknown';
            const company = '';'''

new_content = content.replace(target, new_code)

with open('xcomic.xyz/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Replaced {content.count(target)} occurrences.')
