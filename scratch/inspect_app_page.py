path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html'

with open(path, encoding='utf-8', errors='ignore') as f:
    text = f.read()

pos = text.find('id="app-page"')
if pos != -1:
    print(text[pos:pos+1500])
