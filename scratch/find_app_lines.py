path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html'

with open(path, encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="app-page"' in line or '<aside class="sidebar"' in line or 'class="main-content"' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
