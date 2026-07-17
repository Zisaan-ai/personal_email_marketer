import re

with open('xcomic.xyz/assets/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Match the split and push lines
pattern = re.compile(r'const parts = line\.split\('',''\)\.map\(p => p\.trim\(\)\);\s*leads\.push\(\{ email: parts\[0\], name: parts\[1\] \|\| '''', company: parts\[2\] \|\| '''' \}\);')

new_code = '''let emailPart = line.split(',')[0].trim();
            emailPart = emailPart.replace(/^[\"\\']|[\"\\']$/g, '');
            leads.push({ email: emailPart, name: '', company: '' });'''

new_content = pattern.sub(new_code, content)

with open('xcomic.xyz/assets/app.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Replaced {len(pattern.findall(content))} occurrences.')
