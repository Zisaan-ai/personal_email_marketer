path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic_backend\bulk_campaign_sender.py'

with open(path, encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re

pos = text.find('replace')
while pos != -1:
    print(text[max(0, pos-200):min(len(text), pos+300)])
    print('='*50)
    pos = text.find('replace', pos+1)
