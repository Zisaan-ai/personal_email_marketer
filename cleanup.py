import re

with open('backend/main.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove test reply endpoint
text = re.sub(r'@app\.get\(\'/api/track/test_reply/.*?return \{"status": "Reply injected"\}\n', '', text, flags=re.DOTALL)

# Remove run test endpoint
text = re.sub(r'@app\.get\(\'/api/run_test.*?return \{"status": "success", "message": "Test campaigns with opens, clicks, replies created"\}\n', '', text, flags=re.DOTALL)

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Cleaned up test endpoints')
