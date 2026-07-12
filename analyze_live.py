
import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Download live app.js
import time
url = f'https://xcomic.xyz/assets/app.js?nocache={int(time.time())}'
with urllib.request.urlopen(url, context=ctx) as r:
    content = r.read().decode('utf-8', errors='ignore')

lines = content.splitlines()
print(f'Lines: {len(lines)}')

# Find the exact setupNavigation and check what's around it
for i, line in enumerate(lines):
    if 'setupNavigation' in line:
        print(f'Line {i+1}: {line[:100]}')

# Check for any code BETWEEN function definitions that might run at parse-time and throw
# Look for any immediate execution that could fail
print('\n--- TOP LEVEL CODE (not inside functions) ---')
in_block = 0
top_level_exec = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if not stripped or stripped.startswith('//'):
        continue
    
    # Rough block depth
    in_block += line.count('{') - line.count('}')
    
    # Look for lines that execute at top level (depth 0 or 1)
    if in_block <= 0:
        if stripped and not stripped.startswith('function ') and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*') and stripped not in ['{', '}', '};']:
            if len(stripped) > 5:
                top_level_exec.append(f'{i}: {stripped[:120]}')

print('\n'.join(top_level_exec[:50]))
