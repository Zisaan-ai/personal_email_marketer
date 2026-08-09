import os
import re

html_path = r'C:\Users\higan\.gemini\antigravity\scratch\personal_email_marketer\xcomic.xyz\index.html'
with open(html_path, encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("--- Visual Builder Views/Tabs in index.html ---")
matches = re.finditer(r'(<div[^>]*id=["\']([^"\']*visual[^"\']*|[^"\']*vb[^"\']*)["\'][^>]*>)', text, re.IGNORECASE)
for m in matches:
    print(m.group(1)[:150])

print("\n--- Visual Builder Class Names ---")
class_matches = set(re.findall(r'class=["\']([^"\']*(?:visual|builder|editor|vb-)[^"\']*)["\']', text, re.IGNORECASE))
for c in list(class_matches)[:30]:
    print(" -", c)
