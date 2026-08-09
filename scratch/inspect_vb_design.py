import re

html_path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html'
with open(html_path, encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

start_line = 0
end_line = 0
for i, line in enumerate(lines):
    if 'id="vb-tab-design"' in line:
        start_line = i + 1
        break

if start_line:
    print(f"Found #vb-tab-design at line {start_line}")
    for j in range(start_line - 5, min(len(lines), start_line + 150)):
        print(f"{j+1}: {lines[j].strip()}")
