with open('xcomic.xyz/assets/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = "                const parts = line.split(',').map(p => p.trim());\n\n                leads.push({ email: parts[0], name: parts[1] || '', company: parts[2] || '' });"

new_code = '''                let emailPart = line.split(',')[0].trim();
                emailPart = emailPart.replace(/^["']|["']$/g, '');
                leads.push({ email: emailPart, name: '', company: '' });'''

new_content = content.replace(target, new_code)

with open('xcomic.xyz/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Replaced {content.count(target)} occurrences.')
