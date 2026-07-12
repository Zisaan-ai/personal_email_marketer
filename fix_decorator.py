with open('backend/main.py', encoding='utf-8') as f:
    text = f.read()

import re

# Remove the misplaced decorator from magic_login
text = re.sub(r'@app\.post\(\"/api/auth/token\", response_model=Token\)\n+@app\.get\(\"/api/auth/magic\"\)', '@app.get("/api/auth/magic")', text)

# Remove any existing decorators on login_for_access_token just in case
text = text.replace('@app.post("/api/auth/token", response_model=Token)\ndef login_for_access_token(', 'def login_for_access_token(')

# Add the decorator back to login_for_access_token
text = text.replace('def login_for_access_token(', '@app.post("/api/auth/token", response_model=Token)\ndef login_for_access_token(')

with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed token decorator')
