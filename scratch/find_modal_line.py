html_path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html'

with open(html_path, encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'inbox-preview-modal' in line or 'INBOX PREVIEW' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
