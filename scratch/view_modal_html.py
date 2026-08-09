html_path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html'

with open(html_path, encoding='utf-8', errors='ignore') as f:
    text = f.read()

pos = text.find('id="inbox-preview-modal"')
if pos != -1:
    print(text[pos-50:pos+2500])
