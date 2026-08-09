import re

app_path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\app.js'
html_path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html'

with open(app_path, encoding='utf-8', errors='ignore') as f:
    app_text = f.read()

with open(html_path, encoding='utf-8', errors='ignore') as f:
    html_text = f.read()

pos = app_text.find('previewInbox')
if pos != -1:
    print("--- previewInbox JS implementation ---")
    print(app_text[pos:pos+1500])

print("\n--- Inbox Preview Modal HTML ---")
matches = re.finditer(r'(<div[^>]*id=["\'](?:inbox-preview|preview-modal|preview-body)[^"\']*["\'][^>]*>)', html_text)
for m in matches:
    print(m.group(0))
