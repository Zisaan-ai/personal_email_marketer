import sys
import re
sys.stdout.reconfigure(encoding='utf-8')
content = open('index.html', encoding='utf-8').read()
match = re.search(r'const AUTH = \{.*?\n\s*\};\n', content, re.DOTALL)
if match:
    print(match.group(0))
else:
    print("AUTH object not found!")
