
import urllib.request, ssl, time, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

files = [
    f'https://xcomic.xyz/assets/ai_features.js?v={int(time.time())}',
    f'https://xcomic.xyz/assets/deliverability_v2.js?v={int(time.time())}',
    f'https://xcomic.xyz/assets/sending_accounts.js?v={int(time.time())}',
    f'https://xcomic.xyz/assets/templates.js?v={int(time.time())}',
]

for url in files:
    name = url.split('/')[-1].split('?')[0]
    try:
        with urllib.request.urlopen(url, context=ctx) as r:
            content = r.read().decode('utf-8', errors='ignore')
        lines = content.splitlines()
        opens = content.count('{')
        closes = content.count('}')
        parens_o = content.count('(')
        parens_c = content.count(')')
        print(f'{name}: lines={len(lines)}, braces diff={opens-closes}, parens diff={parens_o-parens_c}')
        
        # Check for top-level immediately executed code that could throw
        in_block = 0
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            in_block += line.count('{') - line.count('}')
            if in_block <= 0 and stripped and not stripped.startswith('//') and not stripped.startswith('*'):
                if 'document.' in stripped or 'querySelector' in stripped:
                    print(f'  WARNING: Top-level DOM access at line {i}: {stripped[:80]}')
    except Exception as e:
        print(f'{name}: ERROR - {e}')
    print()
