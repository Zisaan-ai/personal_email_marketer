import re

app_path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\assets\app.js'

with open(app_path, encoding='utf-8', errors='ignore') as f:
    text = f.read()

pos = text.find('window.drag')
if pos != -1:
    print("Found window.drag:")
    print(text[pos:pos+1200])

pos2 = text.find('bindBlockEvents')
if pos2 != -1:
    print("\nFound bindBlockEvents:")
    print(text[pos2:pos2+1200])
