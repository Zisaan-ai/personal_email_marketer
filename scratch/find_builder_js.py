import re

html_path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html'
app_path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\app.js'

with open(html_path, encoding='utf-8', errors='ignore') as f:
    html = f.read()

with open(app_path, encoding='utf-8', errors='ignore') as f:
    app = f.read()

print("--- Drag/Drop in index.html ---")
for m in re.finditer(r'(ondragover|ondrop|ondragstart)=["\']([^"\']*)["\']', html):
    print(m.group(0))

print("\n--- Functions related to canvas/blocks in app.js ---")
for m in re.finditer(r'function\s+([a-zA-Z0-9_]*block[a-zA-Z0-9_]*|create[a-zA-Z0-9_]*|add[a-zA-Z0-9_]*)\s*\(', app, re.IGNORECASE):
    print(m.group(1))
